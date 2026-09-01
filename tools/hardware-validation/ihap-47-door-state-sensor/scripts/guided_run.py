#!/usr/bin/env python3
"""Low-touch guided validation for IHAP-47.

Normal operator work is physical only: place/move the magnet when prompted and
perform two controlled wiring changes. The runner handles commands, counting,
raw logging and structured evidence.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, TextIO

import serial

MAC_RE = re.compile(r"\b(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}\b")
ANSI_RE = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def session_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def parse_record(line: str) -> dict[str, Any] | None:
    clean = ANSI_RE.sub("", line).strip()
    if not clean.startswith("{"):
        return None
    try:
        value = json.loads(clean)
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


class Evidence:
    def __init__(self, root: Path, sid: str) -> None:
        self.dir = root / sid
        self.dir.mkdir(parents=True, exist_ok=False)
        self.serial: TextIO = (self.dir / "serial.log").open("w", encoding="utf-8")
        self.records: TextIO = (self.dir / "records.jsonl").open("w", encoding="utf-8")
        self.observations: TextIO = (
            self.dir / "operator-observations.jsonl"
        ).open("w", encoding="utf-8")

    def close(self) -> None:
        self.serial.close()
        self.records.close()
        self.observations.close()

    def observation(self, payload: dict[str, Any]) -> None:
        row = {
            "record_type": "operator_observation",
            "schema_version": "1.0.0",
            "observed_at_utc": utc_now(),
            **payload,
        }
        self.observations.write(json.dumps(row, separators=(",", ":")) + "\n")
        self.observations.flush()


class Harness:
    def __init__(self, ser: serial.Serial, evidence: Evidence) -> None:
        self.ser = ser
        self.evidence = evidence

    def send(self, command: str) -> None:
        self.ser.write((command + "\n").encode())
        self.ser.flush()

    def next_record(self, deadline: float) -> dict[str, Any] | None:
        while time.monotonic() < deadline:
            raw = self.ser.readline()
            if not raw:
                continue
            line = raw.decode("utf-8", errors="replace")
            self.evidence.serial.write(line)
            self.evidence.serial.flush()
            print(MAC_RE.sub("<REDACTED_MAC>", ANSI_RE.sub("", line)), end="", flush=True)

            record = parse_record(line)
            if record is None:
                continue
            self.evidence.records.write(json.dumps(record, separators=(",", ":")) + "\n")
            self.evidence.records.flush()
            return record
        return None

    def wait(self, wanted: str, timeout: float = 3.0) -> dict[str, Any]:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            record = self.next_record(deadline)
            if record is None:
                break
            if record.get("record_type") == "error":
                raise RuntimeError(
                    f"{record.get('error_code')}: {record.get('message')}"
                )
            if record.get("record_type") == wanted:
                return record
        raise TimeoutError(f"Timeout waiting for {wanted}")

    def snapshot(self) -> dict[str, Any]:
        self.send("snapshot")
        return self.wait("snapshot")

    def begin(self, test_id: str, specimen: str) -> dict[str, Any]:
        self.send(f"begin {test_id} {specimen}")
        return self.wait("capture_started")

    def status(self) -> dict[str, Any]:
        self.send("status")
        return self.wait("status")

    def end(self) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        self.send("end")
        transitions: list[dict[str, Any]] = []
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            record = self.next_record(deadline)
            if record is None:
                break
            kind = record.get("record_type")
            if kind == "error":
                raise RuntimeError(
                    f"{record.get('error_code')}: {record.get('message')}"
                )
            if kind == "raw_transition":
                transitions.append(record)
            elif kind == "capture_ended":
                return record, transitions
        raise TimeoutError("Timeout waiting for capture_ended")

    def wait_stable(
        self,
        target: int,
        *,
        stable_ms: int,
        poll_ms: int,
        timeout_s: float,
    ) -> None:
        stable_since: float | None = None
        deadline = time.monotonic() + timeout_s
        while time.monotonic() < deadline:
            level = int(self.status().get("last_level", -1))
            now = time.monotonic()
            if level == target:
                stable_since = stable_since or now
                if (now - stable_since) * 1000 >= stable_ms:
                    return
            else:
                stable_since = None
            time.sleep(poll_ms / 1000)
        raise TimeoutError(f"Level {target} never remained stable for {stable_ms} ms")


def movement(
    h: Harness,
    *,
    specimen: str,
    test_id: str,
    target: int,
    prompt: str,
    stable_ms: int,
    poll_ms: int,
    timeout_s: float,
) -> dict[str, Any]:
    started = h.begin(test_id, specimen)
    if int(started["initial_level"]) == target:
        h.end()
        raise RuntimeError(f"{test_id} started already at target level {target}")

    print(f"\n>>> {prompt}")
    h.wait_stable(
        target,
        stable_ms=stable_ms,
        poll_ms=poll_ms,
        timeout_s=timeout_s,
    )
    ended, transitions = h.end()

    offsets = [
        int(r["offset_us"])
        for r in transitions
        if isinstance(r.get("offset_us"), (int, float))
    ]
    span = max(offsets) - min(offsets) if len(offsets) > 1 else 0
    count = int(ended["transition_count"])
    overflow = bool(ended.get("buffer_overflow", False))
    final = int(ended["final_level"])

    return {
        "test_id": test_id,
        "initial_level": int(started["initial_level"]),
        "target_level": target,
        "final_level": final,
        "transition_count": count,
        "raw_transition_span_us": span,
        "buffer_overflow": overflow,
        "pass": final == target and count >= 1 and not overflow,
    }


def write_manifest(
    directory: Path,
    *,
    started: str,
    ended: str | None,
    baud: int,
    specimen: str,
    cycles: int,
) -> None:
    data = {
        "schema_version": "1.0.0",
        "issue": "IHAP-47",
        "mode": "guided-low-touch",
        "started_at_utc": started,
        "ended_at_utc": ended,
        "serial_baud": baud,
        "serial_port_recorded": False,
        "specimen_id": specimen,
        "requested_cycles": cycles,
        "raw_logs_repository_allowed": False,
        "physical_results_validated": False,
        "notes": [
            "serial.log and records.jsonl are local raw evidence and must not be committed.",
            "Normal execution requires no manual JSON entry.",
        ],
    }
    (directory / "session.json").write_text(
        json.dumps(data, indent=2) + "\n", encoding="utf-8"
    )


def args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--port", required=True)
    p.add_argument("--baud", type=int, default=115200)
    p.add_argument("--specimen", default="MC38-A")
    p.add_argument("--cycles", type=int, default=20)
    p.add_argument("--stable-ms", type=int, default=150)
    p.add_argument("--poll-ms", type=int, default=50)
    p.add_argument("--movement-timeout-s", type=float, default=20)
    p.add_argument("--output-root", type=Path, default=Path("output"))
    p.add_argument("--session-id")
    p.add_argument("--skip-failure-modes", action="store_true")
    return p.parse_args()


def main() -> int:
    a = args()
    if a.cycles < 3:
        print("--cycles must be >= 3", file=sys.stderr)
        return 2

    started = utc_now()
    sid = a.session_id or session_id()
    try:
        ev = Evidence(a.output_root, sid)
    except FileExistsError:
        print(f"Session exists: {a.output_root / sid}", file=sys.stderr)
        return 2

    write_manifest(
        ev.dir,
        started=started,
        ended=None,
        baud=a.baud,
        specimen=a.specimen,
        cycles=a.cycles,
    )

    try:
        ser = serial.Serial(a.port, a.baud, timeout=0.15)
    except serial.SerialException as exc:
        ev.close()
        print(f"Cannot open serial port: {exc}", file=sys.stderr)
        return 2

    h = Harness(ser, ev)
    result: dict[str, Any] = {
        "schema_version": "1.0.0",
        "issue": "IHAP-47",
        "mode": "guided-low-touch",
        "specimen_id": a.specimen,
        "started_at_utc": started,
        "sample_period_us": 250,
        "mapping": {},
        "cycle_test": {},
        "failure_modes": {},
        "decision_gate_pass": False,
    }
    rc = 1

    try:
        print("\nIHAP-47 LOW-TOUCH VALIDATION")
        print("No JSON. No manual cycle counting. Follow physical prompts only.\n")

        input("Put magnet FAR (>=100 mm), then press Enter...")
        far = h.snapshot()
        far_level = int(far["raw_level"])
        ev.observation(
            {
                "specimen_id": a.specimen,
                "test": "continuity",
                "magnet_position": "far",
                "circuit": far["circuit_state"],
                "raw_level": far_level,
                "source": "guided_runner",
            }
        )
        if far_level != 1:
            raise RuntimeError(f"FAR must be raw 1; observed {far_level}")

        input("Put magnet NEAR and aligned, then press Enter...")
        near = h.snapshot()
        near_level = int(near["raw_level"])
        ev.observation(
            {
                "specimen_id": a.specimen,
                "test": "continuity",
                "magnet_position": "near",
                "circuit": near["circuit_state"],
                "raw_level": near_level,
                "source": "guided_runner",
            }
        )
        if near_level != 0:
            raise RuntimeError(f"NEAR must be raw 0; observed {near_level}")

        input("Return magnet FAR, then press Enter...")
        if int(h.snapshot()["raw_level"]) != 1:
            raise RuntimeError("Cycle test must start FAR / raw 1")

        result["mapping"] = {"far_level": far_level, "near_level": near_level}

        print(
            f"\nAUTOMATED TEST: {a.cycles} complete cycles.\n"
            "From now on, only move the magnet when prompted.\n"
        )

        moves: list[dict[str, Any]] = []
        for cycle in range(1, a.cycles + 1):
            moves.append(
                movement(
                    h,
                    specimen=a.specimen,
                    test_id=f"CYCLE_{cycle:03d}_CLOSE",
                    target=0,
                    prompt=f"{cycle}/{a.cycles} — move magnet NEAR",
                    stable_ms=a.stable_ms,
                    poll_ms=a.poll_ms,
                    timeout_s=a.movement_timeout_s,
                )
            )
            moves.append(
                movement(
                    h,
                    specimen=a.specimen,
                    test_id=f"CYCLE_{cycle:03d}_OPEN",
                    target=1,
                    prompt=f"{cycle}/{a.cycles} — move magnet FAR",
                    stable_ms=a.stable_ms,
                    poll_ms=a.poll_ms,
                    timeout_s=a.movement_timeout_s,
                )
            )
            print(f"    cycle {cycle}/{a.cycles} complete")

        mismatches = sum(not m["pass"] for m in moves)
        overflows = sum(m["buffer_overflow"] for m in moves)
        multi = sum(m["transition_count"] > 1 for m in moves)
        max_span = max((m["raw_transition_span_us"] for m in moves), default=0)

        cycle_pass = mismatches == 0 and overflows == 0
        result["cycle_test"] = {
            "complete_cycles": a.cycles,
            "stable_movements": len(moves),
            "mismatches": mismatches,
            "buffer_overflows": overflows,
            "movements_with_multiple_raw_transitions": multi,
            "max_raw_transition_span_us": max_span,
            "sample_period_us": 250,
            "stable_window_ms": a.stable_ms,
            "movements": moves,
            "pass": cycle_pass,
        }
        ev.observation(
            {
                "specimen_id": a.specimen,
                "test": "cycle",
                "cycles": a.cycles,
                "stable_movements": len(moves),
                "mismatches": mismatches,
                "buffer_overflows": overflows,
                "movements_with_multiple_raw_transitions": multi,
                "max_raw_transition_span_us": max_span,
                "source": "guided_runner",
            }
        )

        failure_pass = True
        if not a.skip_failure_modes:
            print("\nFAILURE-MODE CHECK — two physical setup changes only.")
            input(
                "Move magnet NEAR, keep it there, disconnect ONE sensor conductor, "
                "then press Enter..."
            )
            disconnected = int(h.snapshot()["raw_level"])
            ev.observation(
                {
                    "specimen_id": a.specimen,
                    "test": "failure_mode",
                    "case": "one_conductor_disconnected",
                    "raw_level": disconnected,
                    "source": "guided_runner",
                }
            )

            input(
                "Reconnect sensor, move magnet FAR, connect GPIO6 directly to GND "
                "for the low-voltage bench check, then press Enter..."
            )
            grounded = int(h.snapshot()["raw_level"])
            ev.observation(
                {
                    "specimen_id": a.specimen,
                    "test": "failure_mode",
                    "case": "gpio_to_ground",
                    "raw_level": grounded,
                    "source": "guided_runner",
                }
            )
            input("Remove the GPIO6-to-GND link and restore normal wiring. Press Enter...")

            result["failure_modes"] = {
                "disconnected_conductor_level": disconnected,
                "gpio_to_ground_level": grounded,
                "pass": disconnected == 1 and grounded == 0,
            }
            failure_pass = bool(result["failure_modes"]["pass"])
        else:
            result["failure_modes"] = {"skipped": True, "pass": True}

        result["pull_up_bench_adequate"] = cycle_pass
        result["decision_gate_pass"] = cycle_pass and failure_pass
        result["ended_at_utc"] = utc_now()
        rc = 0 if result["decision_gate_pass"] else 1

    except (KeyboardInterrupt, EOFError):
        result["aborted"] = True
        result["ended_at_utc"] = utc_now()
        rc = 130
    except (RuntimeError, TimeoutError, serial.SerialException) as exc:
        result["error"] = str(exc)
        result["ended_at_utc"] = utc_now()
        print(f"\nSTOP: {exc}", file=sys.stderr)
        rc = 1
    finally:
        ser.close()
        (ev.dir / "guided-result.json").write_text(
            json.dumps(result, indent=2) + "\n", encoding="utf-8"
        )
        write_manifest(
            ev.dir,
            started=started,
            ended=str(result.get("ended_at_utc", utc_now())),
            baud=a.baud,
            specimen=a.specimen,
            cycles=a.cycles,
        )
        ev.close()

    print(f"\nRaw evidence preserved: {ev.dir}")
    if rc == 0:
        print("\nRESULT")
        print(f"  cycles: {a.cycles}/{a.cycles}")
        print(f"  mismatches: {result['cycle_test']['mismatches']}")
        print(
            "  movements with >1 raw transition: "
            f"{result['cycle_test']['movements_with_multiple_raw_transitions']}/"
            f"{result['cycle_test']['stable_movements']}"
        )
        print(f"  buffer overflows: {result['cycle_test']['buffer_overflows']}")
        print(f"  decision gate: {'PASS' if result['decision_gate_pass'] else 'FAIL'}")
        try:
            subprocess.run(
                [sys.executable, str(Path(__file__).with_name("build_report.py")), str(ev.dir)],
                check=True,
            )
        except subprocess.CalledProcessError as exc:
            print(f"Report generation failed; raw evidence is safe: {exc}", file=sys.stderr)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
