#!/usr/bin/env python3
"""Guided low-touch IHAP-47 physical validation.

The operator performs only physical actions. The runner drives the firmware,
captures raw serial evidence locally, detects stable state changes, counts
cycles, and writes a machine-readable result. No manual JSON entry is needed.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, TextIO

import serial

MAC_PATTERN = re.compile(r"\b(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}\b")
ANSI_PATTERN = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def safe_session_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def redact_console_text(text: str) -> str:
    return MAC_PATTERN.sub("<REDACTED_MAC>", ANSI_PATTERN.sub("", text))


def parse_json_record(line: str) -> dict[str, Any] | None:
    candidate = ANSI_PATTERN.sub("", line).strip()
    if not candidate.startswith("{"):
        return None
    try:
        value = json.loads(candidate)
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


@dataclass
class SessionFiles:
    directory: Path
    serial_log: TextIO
    records: TextIO
    observations: TextIO

    @classmethod
    def create(cls, output_root: Path, session_id: str) -> "SessionFiles":
        directory = output_root / session_id
        directory.mkdir(parents=True, exist_ok=False)
        return cls(
            directory=directory,
            serial_log=(directory / "serial.log").open("w", encoding="utf-8"),
            records=(directory / "records.jsonl").open("w", encoding="utf-8"),
            observations=(directory / "operator-observations.jsonl").open("w", encoding="utf-8"),
        )

    def close(self) -> None:
        self.serial_log.close()
        self.records.close()
        self.observations.close()

    def observation(self, payload: dict[str, Any]) -> None:
        record = {
            "record_type": "operator_observation",
            "schema_version": "1.0.0",
            "observed_at_utc": utc_now(),
            **payload,
        }
        self.observations.write(json.dumps(record, separators=(",", ":")) + "\n")
        self.observations.flush()


class Harness:
    def __init__(self, connection: serial.Serial, files: SessionFiles) -> None:
        self.connection = connection
        self.files = files

    def _read_record(self, deadline: float) -> dict[str, Any] | None:
        while time.monotonic() < deadline:
            raw = self.connection.readline()
            if not raw:
                continue
            line = raw.decode("utf-8", errors="replace")
            self.files.serial_log.write(line)
            self.files.serial_log.flush()
            print(redact_console_text(line), end="", flush=True)
            record = parse_json_record(line)
            if record is not None:
                self.files.records.write(json.dumps(record, separators=(",", ":")) + "\n")
                self.files.records.flush()
                return record
        return None

    def send(self, command: str) -> None:
        self.connection.write((command.rstrip("\r\n") + "\n").encode("utf-8"))
        self.connection.flush()

    def wait_for(self, record_type: str, timeout_s: float = 3.0) -> dict[str, Any]:
        deadline = time.monotonic() + timeout_s
        while time.monotonic() < deadline:
            record = self._read_record(deadline)
            if record is None:
                break
            if record.get("record_type") == "error":
                raise RuntimeError(
                    f"Firmware error {record.get('error_code')}: {record.get('message')}"
                )
            if record.get("record_type") == record_type:
                return record
        raise TimeoutError(f"Timed out waiting for firmware record: {record_type}")

    def snapshot(self) -> dict[str, Any]:
        self.send("snapshot")
        return self.wait_for("snapshot")

    def begin(self, test_id: str, specimen_id: str) -> dict[str, Any]:
        self.send(f"begin {test_id} {specimen_id}")
        return self.wait_for("capture_started")

    def status(self) -> dict[str, Any]:
        self.send("status")
        return self.wait_for("status")

    def end(self) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        self.send("end")
        transitions: list[dict[str, Any]] = []
        deadline = time.monotonic() + 5.0
        while time.monotonic() < deadline:
            record = self._read_record(deadline)
            if record is None:
                break
            record_type = record.get("record_type")
            if record_type == "error":
                raise RuntimeError(
                    f"Firmware error {record.get('error_code')}: {record.get('message')}"
                )
            if record_type == "raw_transition":
                transitions.append(record)
            elif record_type == "capture_ended":
                return record, transitions
        raise TimeoutError("Timed out waiting for capture_ended")

    def wait_for_stable_level(
        self,
        target_level: int,
        *,
        stable_ms: int,
        movement_timeout_s: float,
        poll_ms: int,
    ) -> None:
        stable_since: float | None = None
        deadline = time.monotonic() + movement_timeout_s
        while time.monotonic() < deadline:
            status = self.status()
            level = int(status.get("last_level", -1))
            now = time.monotonic()

            if level == target_level:
                if stable_since is None:
                    stable_since = now
                elif (now - stable_since) * 1000 >= stable_ms:
                    return
            else:
                stable_since = None

            time.sleep(poll_ms / 1000.0)

        raise TimeoutError(
            f"Target level {target_level} did not remain stable for {stable_ms} ms"
        )


def capture_movement(
    harness: Harness,
    *,
    specimen_id: str,
    test_id: str,
    target_level: int,
    instruction: str,
    stable_ms: int,
    movement_timeout_s: float,
    poll_ms: int,
) -> dict[str, Any]:
    started = harness.begin(test_id, specimen_id)
    initial_level = int(started["initial_level"])
    if initial_level == target_level:
        harness.end()
        raise RuntimeError(
            f"Cannot start {test_id}: sensor is already at target level {target_level}"
        )

    print(f"\n>>> {instruction}")
    harness.wait_for_stable_level(
        target_level,
        stable_ms=stable_ms,
        movement_timeout_s=movement_timeout_s,
        poll_ms=poll_ms,
    )
    ended, transitions = harness.end()

    offsets = [
        int(item["offset_us"])
        for item in transitions
        if isinstance(item.get("offset_us"), (int, float))
    ]
    span_us = max(offsets) - min(offsets) if len(offsets) >= 2 else 0

    return {
        "test_id": test_id,
        "initial_level": initial_level,
        "target_level": target_level,
        "final_level": int(ended["final_level"]),
        "transition_count": int(ended["transition_count"]),
        "raw_transition_span_us": span_us,
        "buffer_overflow": bool(ended.get("buffer_overflow", False)),
        "pass": (
            int(ended["final_level"]) == target_level
            and int(ended["transition_count"]) >= 1
            and not bool(ended.get("buffer_overflow", False))
        ),
    }


def write_manifest(
    directory: Path,
    *,
    started_at: str,
    ended_at: str | None,
    baud: int,
    cycles: int,
    specimen_id: str,
) -> None:
    manifest = {
        "schema_version": "1.0.0",
        "issue": "IHAP-47",
        "mode": "guided-low-touch",
        "session_id": directory.name,
        "started_at_utc": started_at,
        "ended_at_utc": ended_at,
        "serial_baud": baud,
        "serial_port_recorded": False,
        "specimen_id": specimen_id,
        "requested_cycles": cycles,
        "raw_logs_repository_allowed": False,
        "physical_results_validated": False,
        "notes": [
            "The serial port path is intentionally omitted.",
            "serial.log and records.jsonl are local raw evidence and must not be committed.",
            "The runner performs data entry automatically; operator actions are physical only.",
        ],
    }
    (directory / "session.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", required=True)
    parser.add_argument("--baud", type=int, default=115200)
    parser.add_argument("--specimen", default="MC38-A")
    parser.add_argument("--cycles", type=int, default=20)
    parser.add_argument("--stable-ms", type=int, default=150)
    parser.add_argument("--poll-ms", type=int, default=50)
    parser.add_argument("--movement-timeout-s", type=float, default=20.0)
    parser.add_argument("--output-root", type=Path, default=Path("output"))
    parser.add_argument("--session-id", default=None)
    parser.add_argument(
        "--skip-failure-modes",
        action="store_true",
        help="Skip disconnect and GPIO-to-GND observations.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.cycles < 3:
        print("--cycles must be at least 3", file=sys.stderr)
        return 2
    if args.stable_ms < 50:
        print("--stable-ms must be at least 50", file=sys.stderr)
        return 2

    started_at = utc_now()
    session_id = args.session_id or safe_session_id()

    try:
        files = SessionFiles.create(args.output_root, session_id)
    except FileExistsError:
        print(f"Session already exists: {args.output_root / session_id}", file=sys.stderr)
        return 2

    write_manifest(
        files.directory,
        started_at=started_at,
        ended_at=None,
        baud=args.baud,
        cycles=args.cycles,
        specimen_id=args.specimen,
    )

    try:
        connection = serial.Serial(args.port, args.baud, timeout=0.15)
    except serial.SerialException as exc:
        files.close()
        print(f"Unable to open serial port: {exc}", file=sys.stderr)
        return 2

    harness = Harness(connection, files)
    result: dict[str, Any] = {
        "schema_version": "1.0.0",
        "issue": "IHAP-47",
        "mode": "guided-low-touch",
        "specimen_id": args.specimen,
        "started_at_utc": started_at,
        "sample_period_us": 250,
        "mapping": {},
        "cycle_test": {},
        "failure_modes": {},
        "decision_gate_pass": False,
    }

    exit_code = 1
    try:
        print("\nIHAP-47 LOW-TOUCH VALIDATION")
        print("No JSON entry. Follow the physical prompts only.\n")

        input("1/3  Put the magnet FAR (>=100 mm), then press Enter once...")
        far = harness.snapshot()
        far_level = int(far["raw_level"])
        result["mapping"]["far_level"] = far_level
        files.observation(
            {
                "specimen_id": args.specimen,
                "test": "continuity",
                "magnet_position": "far",
                "circuit": str(far["circuit_state"]),
                "raw_level": far_level,
                "source": "guided_runner",
            }
        )
        if far_level != 1:
            raise RuntimeError(f"Expected FAR raw level 1, observed {far_level}")

        input("2/3  Put the magnet NEAR and aligned, then press Enter once...")
        near = harness.snapshot()
        near_level = int(near["raw_level"])
        result["mapping"]["near_level"] = near_level
        files.observation(
            {
                "specimen_id": args.specimen,
                "test": "continuity",
                "magnet_position": "near",
                "circuit": str(near["circuit_state"]),
                "raw_level": near_level,
                "source": "guided_runner",
            }
        )
        if near_level != 0:
            raise RuntimeError(f"Expected NEAR raw level 0, observed {near_level}")

        input("3/3  Return the magnet FAR, then press Enter once...")
        start = harness.snapshot()
        if int(start["raw_level"]) != 1:
            raise RuntimeError("Cycle test must start with magnet FAR / raw level 1")

        print(
            f"\nAUTOMATED CYCLE TEST — {args.cycles} complete cycles.\n"
            "From now on DO NOT TYPE ANYTHING. Move the magnet only when prompted.\n"
        )

        movements: list[dict[str, Any]] = []
        for cycle in range(1, args.cycles + 1):
            close_result = capture_movement(
                harness,
                specimen_id=args.specimen,
                test_id=f"CYCLE_{cycle:03d}_CLOSE",
                target_level=0,
                instruction=f"Cycle {cycle}/{args.cycles}: move magnet NEAR",
                stable_ms=args.stable_ms,
                movement_timeout_s=args.movement_timeout_s,
                poll_ms=args.poll_ms,
            )
            movements.append(close_result)

            open_result = capture_movement(
                harness,
                specimen_id=args.specimen,
                test_id=f"CYCLE_{cycle:03d}_OPEN",
                target_level=1,
                instruction=f"Cycle {cycle}/{args.cycles}: move magnet FAR",
                stable_ms=args.stable_ms,
                movement_timeout_s=args.movement_timeout_s,
                poll_ms=args.poll_ms,
            )
            movements.append(open_result)
            print(f"    cycle {cycle}/{args.cycles} complete")

        raw_transition_counts = [item["transition_count"] for item in movements]
        bounce_movements = sum(1 for count in raw_transition_counts if count > 1)
        max_span_us = max((item["raw_transition_span_us"] for item in movements), default=0)
        mismatches = sum(1 for item in movements if not item["pass"])
        overflow_count = sum(1 for item in movements if item["buffer_overflow"])

        result["cycle_test"] = {
            "complete_cycles": args.cycles,
            "stable_movements": len(movements),
            "mismatches": mismatches,
            "buffer_overflows": overflow_count,
            "movements_with_multiple_raw_transitions": bounce_movements,
            "max_raw_transition_span_us": max_span_us,
            "sample_period_us": 250,
            "stable_window_ms": args.stable_ms,
            "movements": movements,
            "pass": mismatches == 0 and overflow_count == 0,
        }
        files.observation(
            {
                "specimen_id": args.specimen,
                "test": "cycle",
                "cycles": args.cycles,
                "stable_movements": len(movements),
                "mismatches": mismatches,
                "buffer_overflows": overflow_count,
                "movements_with_multiple_raw_transitions": bounce_movements,
                "max_raw_transition_span_us": max_span_us,
                "source": "guided_runner",
            }
        )

        failure_pass = True
        if not args.skip_failure_modes:
            print("\nFAILURE-MODE CHECK — only two setup changes.")
            input(
                "Keep magnet NEAR. Disconnect ONE sensor conductor, then press Enter once..."
            )
            disconnected = harness.snapshot()
            disconnected_level = int(disconnected["raw_level"])
            result["failure_modes"]["disconnected_conductor_level"] = disconnected_level
            files.observation(
                {
                    "specimen_id": args.specimen,
                    "test": "failure_mode",
                    "case": "one_conductor_disconnected",
                    "raw_level": disconnected_level,
                    "source": "guided_runner",
                }
            )

            input(
                "Reconnect sensor. Connect GPIO6 to GND for the bench check, then press Enter once..."
            )
            shorted = harness.snapshot()
            shorted_level = int(shorted["raw_level"])
            result["failure_modes"]["gpio_to_ground_level"] = shorted_level
            files.observation(
                {
                    "specimen_id": args.specimen,
                    "test": "failure_mode",
                    "case": "gpio_to_ground",
                    "raw_level": shorted_level,
                    "source": "guided_runner",
                }
            )
            failure_pass = disconnected_level == 1 and shorted_level == 0
            input("Remove the GPIO6-to-GND bench short and restore normal wiring. Press Enter...")

        result["failure_modes"]["pass"] = failure_pass
        result["pull_up_bench_adequate"] = (
            result["cycle_test"]["pass"]
            and result["mapping"]["far_level"] == 1
            and result["mapping"]["near_level"] == 0
        )
        result["decision_gate_pass"] = (
            result["mapping"]["far_level"] == 1
            and result["mapping"]["near_level"] == 0
            and bool(result["cycle_test"]["pass"])
            and failure_pass
        )
        result["ended_at_utc"] = utc_now()

        (files.directory / "guided-result.json").write_text(
            json.dumps(result, indent=2) + "\n", encoding="utf-8"
        )

        print("\nRESULT")
        print(f"  mapping FAR/NEAR: {far_level}/{near_level}")
        print(f"  cycles: {args.cycles}/{args.cycles}")
        print(f"  mismatches: {mismatches}")
        print(f"  movements with >1 raw transition: {bounce_movements}/{len(movements)}")
        print(f"  buffer overflows: {overflow_count}")
        print(f"  decision gate: {'PASS' if result['decision_gate_pass'] else 'FAIL'}")
        exit_code = 0 if result["decision_gate_pass"] else 1

    except (KeyboardInterrupt, EOFError):
        print("\nRun aborted by operator.", file=sys.stderr)
        result["aborted"] = True
        result["ended_at_utc"] = utc_now()
        (files.directory / "guided-result.json").write_text(
            json.dumps(result, indent=2) + "\n", encoding="utf-8"
        )
        exit_code = 130
    except (RuntimeError, TimeoutError, serial.SerialException) as exc:
        print(f"\nSTOP: {exc}", file=sys.stderr)
        result["error"] = str(exc)
        result["ended_at_utc"] = utc_now()
        (files.directory / "guided-result.json").write_text(
            json.dumps(result, indent=2) + "\n", encoding="utf-8"
        )
        exit_code = 1
    finally:
        connection.close()
        ended_at = result.get("ended_at_utc", utc_now())
        write_manifest(
            files.directory,
            started_at=started_at,
            ended_at=str(ended_at),
            baud=args.baud,
            cycles=args.cycles,
            specimen_id=args.specimen,
        )
        files.close()

    print(f"\nRaw evidence preserved locally: {files.directory}")
    if exit_code == 0:
        report_script = Path(__file__).with_name("build_report.py")
        try:
            subprocess.run(
                [sys.executable, str(report_script), str(files.directory)],
                check=True,
            )
        except subprocess.CalledProcessError as exc:
            print(
                f"Report generation failed after a valid run: {exc}. Raw evidence is preserved.",
                file=sys.stderr,
            )
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
