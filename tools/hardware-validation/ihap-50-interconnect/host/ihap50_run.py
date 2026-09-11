#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import serial
from serial import SerialException

from evaluator import combine, evaluate_boot, evaluate_door_phase, evaluate_samples

BAUD = 115200
BOOT_TIMEOUT_S = 35
RECONNECT_TIMEOUT_S = 20


def extract_json(line: str) -> dict | None:
    start = line.find("{")
    end = line.rfind("}")
    if start < 0 or end <= start:
        return None
    try:
        value = json.loads(line[start : end + 1])
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


def ask_yes(prompt: str) -> bool:
    while True:
        answer = input(f"{prompt} [y/n]: ").strip().lower()
        if answer in {"y", "yes", "s", "si", "sì"}:
            return True
        if answer in {"n", "no"}:
            return False
        print("Rispondi y/n.")


class Collector:
    def __init__(self, port: str, raw_path: Path):
        self.port = port
        self.raw_path = raw_path
        self.ser: serial.Serial | None = None
        self.raw = raw_path.open("a", encoding="utf-8")

    def close(self) -> None:
        if self.ser is not None:
            try:
                self.ser.close()
            except Exception:
                pass
            self.ser = None
        self.raw.close()

    def _connect(self, timeout_s: float = RECONNECT_TIMEOUT_S) -> None:
        deadline = time.monotonic() + timeout_s
        last_error: Exception | None = None
        while time.monotonic() < deadline:
            try:
                self.ser = serial.Serial(self.port, BAUD, timeout=1.0)
                time.sleep(0.25)
                self.ser.reset_input_buffer()
                return
            except (SerialException, OSError) as exc:
                last_error = exc
                time.sleep(0.5)
        raise RuntimeError(f"Impossibile aprire {self.port}: {last_error}")

    def discard_pending(self, context: str) -> None:
        """Discard records queued before an operator-confirmed acquisition boundary.

        integrated_sample is emitted every five seconds. While the operator reads a
        prompt or changes a physical condition, several old samples can accumulate
        in the host serial buffer. They must never be attributed to the condition
        confirmed after ENTER.
        """
        if self.ser is None or not self.ser.is_open:
            self._connect()
        assert self.ser is not None
        try:
            pending = self.ser.in_waiting
            self.ser.reset_input_buffer()
        except (SerialException, OSError) as exc:
            self.ser = None
            raise RuntimeError(f"Impossibile pulire il buffer seriale per {context}: {exc}") from exc
        print(f"  acquisition boundary [{context}]: scartati {pending} byte pre-condizione")

    def read_record(self, timeout_s: float) -> dict:
        deadline = time.monotonic() + timeout_s
        while time.monotonic() < deadline:
            if self.ser is None or not self.ser.is_open:
                self._connect()
            try:
                raw = self.ser.readline()
            except (SerialException, OSError):
                try:
                    self.ser.close()
                except Exception:
                    pass
                self.ser = None
                continue
            if not raw:
                continue
            line = raw.decode("utf-8", errors="replace").rstrip("\r\n")
            stamp = datetime.now(timezone.utc).isoformat()
            self.raw.write(f"{stamp}\t{line}\n")
            self.raw.flush()
            record = extract_json(line)
            if record is not None:
                return record
        raise TimeoutError(f"Nessun record JSON utile entro {timeout_s:.0f}s")

    def wait_for_type(self, record_type: str, timeout_s: float) -> dict:
        deadline = time.monotonic() + timeout_s
        while time.monotonic() < deadline:
            record = self.read_record(max(1.0, deadline - time.monotonic()))
            if record.get("record_type") == record_type:
                return record
        raise TimeoutError(f"Record {record_type!r} non ricevuto")

    def collect_samples(self, count: int, timeout_per_sample_s: float = 8.0) -> list[dict]:
        samples: list[dict] = []
        last_seq: int | None = None
        while len(samples) < count:
            sample = self.wait_for_type("integrated_sample", timeout_per_sample_s)
            seq = sample.get("seq")
            if isinstance(seq, int) and last_seq is not None and seq <= last_seq:
                continue
            if isinstance(seq, int):
                last_seq = seq
            samples.append(sample)
            print(
                f"  sample {len(samples)}/{count}: "
                f"SEQ={sample.get('seq')} "
                f"OLED={sample.get('oled_ok')} "
                f"RADAR={sample.get('radar_fresh')} "
                f"DOOR={sample.get('door_raw')}"
            )
        return samples


def make_summary(
    run_id: str,
    profile: str,
    commit: str,
    boot: dict,
    baseline: list[dict],
    visual_confirmed: bool,
    connector_review: bool,
    door_phases: dict[str, list[dict]],
    result,
) -> dict:
    return {
        "schema_version": "1.1",
        "run_id": run_id,
        "issue": "IHAP-50",
        "profile": profile,
        "commit": commit,
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "boot": boot,
        "operator_checks": {
            "oled_full_on_visible": visual_confirmed,
            "connector_pin_order_and_polarity_reviewed": connector_review,
        },
        "baseline_sample_count": len(baseline),
        "door_phases": {
            name: [
                {
                    "seq": sample.get("seq"),
                    "door_raw": sample.get("door_raw"),
                    "oled_ok": sample.get("oled_ok"),
                    "radar_fresh": sample.get("radar_fresh"),
                }
                for sample in samples
            ]
            for name, samples in door_phases.items()
        },
        "checks": result.checks,
        "errors": result.errors,
        "result": "PASS" if result.passed else "FAIL",
        "claim_boundary": "Integrated prototype interconnect evidence only; not final PCB/power/certification evidence.",
    }


def write_markdown(summary: dict, path: Path) -> None:
    checks = "\n".join(
        f"- [{'x' if ok else ' '}] `{name}`" for name, ok in summary["checks"].items()
    )
    errors = summary["errors"] or ["None"]
    path.write_text(
        "\n".join(
            [
                f"# {summary['run_id']} — IHAP-50 integrated gate",
                "",
                f"- Profile: `{summary['profile']}`",
                f"- Commit: `{summary['commit']}`",
                f"- Result: **{summary['result']}**",
                f"- Captured UTC: `{summary['captured_at_utc']}`",
                "",
                "## Checks",
                "",
                checks,
                "",
                "## Errors",
                "",
                *[f"- {error}" for error in errors],
                "",
                "## Evidence boundary",
                "",
                summary["claim_boundary"],
                "",
                "Raw serial data stays local under `runs/` and must not be committed by default.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="IHAP-50 guided integrated interconnect gate")
    parser.add_argument("--port", required=True, help="Serial device, e.g. /dev/ttyACM0")
    parser.add_argument("--profile", required=True, choices=("standard", "precision"))
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--commit", required=True, help="git rev-parse HEAD used for the run")
    parser.add_argument("--samples", type=int, default=6)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.samples < 6:
        print("--samples deve essere >= 6", file=sys.stderr)
        return 2

    run_dir = Path(__file__).resolve().parents[1] / "runs" / args.run_id
    if run_dir.exists():
        print(f"Run ID già esistente: {run_dir}. Usa un nuovo --run-id.", file=sys.stderr)
        return 2
    run_dir.mkdir(parents=True)

    collector = Collector(args.port, run_dir / "serial.log")
    door_phases: dict[str, list[dict]] = {}

    try:
        print("\nIHAP-50 — integrated interconnect gate")
        print(f"Profile: {args.profile}")
        print("Controlla il cablaggio a dispositivo SPENTO prima di continuare.")
        connector_review = ask_yes("Hai verificato pin-order, polarità e GND comune contro il runbook?")
        if not connector_review:
            raise RuntimeError("Connector/polarity review non confermata")

        print(f"\nApro {args.port}. Premi RST una volta quando richiesto.")
        collector._connect()
        input("Premi INVIO, poi premi RST sull'ESP32-C3 una volta: ")
        boot = collector.wait_for_type("boot", BOOT_TIMEOUT_S)
        boot_result = evaluate_boot(boot, args.profile)
        print(f"Boot gate: {'PASS' if boot_result.passed else 'FAIL'}")
        if boot_result.errors:
            print("  " + ", ".join(boot_result.errors))
        if not boot_result.passed:
            raise RuntimeError(
                "Boot gate non coerente con il profilo richiesto; correggi il setup prima dell'acquisizione: "
                + ", ".join(boot_result.errors)
            )

        visual_confirmed = ask_yes("All'avvio l'OLED si è illuminato completamente per circa 1 secondo e poi è tornato normale?")

        collector.discard_pending("baseline")
        print(f"\nRaccolgo {args.samples} sample baseline freschi (~{args.samples * 5}s).")
        baseline = collector.collect_samples(args.samples)
        sample_result = evaluate_samples(baseline, args.profile, args.samples)

        results = [boot_result, sample_result]

        if args.profile == "standard":
            phases = (
                ("open", 1, "Porta/sensore FAR: magnete lontano, contatto aperto"),
                ("closed", 0, "Porta/sensore NEAR: magnete vicino, contatto chiuso"),
                ("disconnected", 1, "Scollega UN SOLO conduttore del MC-38 dal circuito"),
            )
            for name, expected, instruction in phases:
                print(f"\nDOOR {name.upper()}: {instruction}.")
                input("Quando la condizione è stabile, premi INVIO: ")
                collector.discard_pending(f"door-{name}")
                phase_samples = collector.collect_samples(2)
                door_phases[name] = phase_samples
                results.append(evaluate_door_phase(phase_samples, expected, name))
            print("\nRicollega il conduttore MC-38 scollegato prima di terminare.")

        manual_result = type(boot_result)(
            passed=visual_confirmed and connector_review,
            checks={
                "operator_oled_visual_confirmation": visual_confirmed,
                "operator_connector_polarity_review": connector_review,
            },
            errors=[
                name
                for name, ok in {
                    "operator_oled_visual_confirmation": visual_confirmed,
                    "operator_connector_polarity_review": connector_review,
                }.items()
                if not ok
            ],
        )
        results.append(manual_result)
        combined = combine(*results)

        summary = make_summary(
            args.run_id,
            args.profile,
            args.commit,
            boot,
            baseline,
            visual_confirmed,
            connector_review,
            door_phases,
            combined,
        )
        (run_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
        write_markdown(summary, run_dir / "summary.md")

        print(f"\nFINAL GATE: {summary['result']}")
        if summary["errors"]:
            print("Errori:")
            for error in summary["errors"]:
                print(f"  - {error}")
        print(f"Evidence locale: {run_dir}")
        return 0 if combined.passed else 2

    except (RuntimeError, TimeoutError, SerialException, OSError, KeyboardInterrupt) as exc:
        failure = {
            "schema_version": "1.1",
            "run_id": args.run_id,
            "issue": "IHAP-50",
            "profile": args.profile,
            "commit": args.commit,
            "result": "ABORTED",
            "error": str(exc),
            "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        }
        (run_dir / "aborted.json").write_text(json.dumps(failure, indent=2) + "\n", encoding="utf-8")
        print(f"\nABORTED: {exc}", file=sys.stderr)
        return 2
    finally:
        collector.close()


if __name__ == "__main__":
    raise SystemExit(main())
