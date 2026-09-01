#!/usr/bin/env python3
"""Staged ESP32-C3 stability diagnostic for IHAP-45 brownout isolation."""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

import ihap45
from ihap45_resilient import discover_identity, wait_for_port

DEFAULT_DURATION_SECONDS = 300.0
DEFAULT_STARTUP_TIMEOUT_SECONDS = 45.0
DEFAULT_RECONNECT_TIMEOUT_SECONDS = 30.0
DEFAULT_RECONNECT_POLL_SECONDS = 0.25


@dataclass(frozen=True)
class StabilityEvaluation:
    passed: bool
    errors: list[str]
    warnings: list[str]


def evaluate_stability(
    *,
    boot_records: int,
    brownout_lines: int,
    disconnects_after_start: int,
    valid_sample_records: int,
    completed_window: bool,
) -> StabilityEvaluation:
    errors: list[str] = []
    warnings: list[str] = []
    if boot_records == 0:
        errors.append("no harness_boot observed after operator reset")
    elif boot_records > 1:
        errors.append(f"unexpected reboot observed: {boot_records} harness_boot records")
    if brownout_lines:
        errors.append(f"brownout detector triggered {brownout_lines} time(s)")
    if disconnects_after_start:
        errors.append(f"USB disconnected {disconnects_after_start} time(s) after qualification start")
    if not completed_window:
        errors.append("stability qualification window did not complete")
    if valid_sample_records == 0:
        warnings.append("no valid sensor samples observed; acceptable only for board-only isolation")
    return StabilityEvaluation(passed=not errors, errors=errors, warnings=warnings)


def append_structured_record(
    paths: dict[str, Path],
    record: dict[str, Any],
    run_id: str,
    host_timestamp: str,
) -> None:
    if ihap45.pressure_fields_in(record):
        raise ihap45.HarnessError("firmware emitted a forbidden pressure field")
    record_type = record.get("record_type")
    if record_type == "sample":
        sample_errors = ihap45.validate_sample_record(record)
        if sample_errors:
            raise ihap45.HarnessError(f"invalid sample record: {'; '.join(sample_errors)}")
    elif record_type not in {"harness_boot", "sensor_probe"}:
        return
    ihap45.append_jsonl(
        paths["samples"],
        {
            **record,
            "run_id": run_id,
            "host_timestamp_utc": host_timestamp,
            "phase": "stability_diagnostic",
        },
    )


def run_stability(
    *,
    port: str,
    baud: int,
    run_dir: Path,
    run_id: str,
    label: str,
    duration_seconds: float,
    startup_timeout_seconds: float,
    reconnect_timeout_seconds: float,
    reconnect_poll_seconds: float,
    quiet: bool,
) -> StabilityEvaluation:
    try:
        import serial
        from serial.tools import list_ports
    except ImportError as exc:
        raise ihap45.HarnessError("pyserial is required. Install host/requirements.txt") from exc

    paths = ihap45.initialize_run(run_dir, run_id, port, baud, Path("stability-diagnostic"))
    metadata = ihap45.load_json(paths["metadata"])
    metadata.update(
        {
            "diagnostic": "functional_stability_only",
            "configuration_label": label,
            "qualification_duration_seconds": duration_seconds,
            "qualification_started_at_utc": None,
            "measurement_claim": "no quantitative power characterization",
        }
    )
    ihap45.atomic_write_text(paths["metadata"], json.dumps(metadata, indent=2) + "\n")

    identity = discover_identity(port, list_ports)
    connection: Any | None = None
    first_boot_monotonic: float | None = None
    command_started = time.monotonic()
    boot_records = 0
    brownout_lines = 0
    disconnects_before_start = 0
    disconnects_after_start = 0
    valid_sample_records = 0
    completed_window = False
    port_history: list[str] = []

    if not quiet:
        print(f"IHAP-45 stability diagnostic: {label}")
        print(f"Evidence directory: {run_dir}")
        print("Press RST once after the collector reports Connected.")

    try:
        with paths["serial"].open("a", encoding="utf-8", newline="\n") as raw_log:
            while True:
                if first_boot_monotonic is None:
                    if time.monotonic() - command_started > startup_timeout_seconds:
                        break
                elif time.monotonic() - first_boot_monotonic >= duration_seconds:
                    completed_window = True
                    break

                if connection is None:
                    selected_port = wait_for_port(
                        identity,
                        list_ports,
                        timeout_seconds=reconnect_timeout_seconds,
                        poll_seconds=reconnect_poll_seconds,
                    )
                    try:
                        connection = serial.Serial(selected_port, baudrate=baud, timeout=1.0)
                    except (serial.SerialException, OSError):
                        connection = None
                        time.sleep(reconnect_poll_seconds)
                        continue
                    port_history.append(selected_port)
                    if not quiet:
                        print(f"Connected: {selected_port}")

                try:
                    payload = connection.readline()
                except (serial.SerialException, OSError) as exc:
                    if first_boot_monotonic is None:
                        disconnects_before_start += 1
                        stage = "before qualification start"
                    else:
                        disconnects_after_start += 1
                        stage = "after qualification start"
                    if not quiet:
                        print(f"Serial interrupted {stage} ({exc}); reconnecting...", file=sys.stderr)
                    try:
                        connection.close()
                    except Exception:
                        pass
                    connection = None
                    continue

                if not payload:
                    continue

                text = payload.decode("utf-8", errors="replace").rstrip("\r\n")
                host_timestamp = ihap45.utc_now()
                raw_log.write(f"{host_timestamp}\t{text}\n")
                raw_log.flush()
                if not quiet:
                    print(text)

                if "Brownout detector was triggered" in text:
                    brownout_lines += 1

                record = ihap45.parse_firmware_json(text)
                if record is None:
                    continue

                record_type = record.get("record_type")
                if record_type == "harness_boot":
                    boot_records += 1
                    if first_boot_monotonic is None:
                        first_boot_monotonic = time.monotonic()
                        metadata["qualification_started_at_utc"] = host_timestamp
                        ihap45.atomic_write_text(paths["metadata"], json.dumps(metadata, indent=2) + "\n")
                        if not quiet:
                            print(f"Qualification window started: {duration_seconds:.0f}s")
                    append_structured_record(paths, record, run_id, host_timestamp)
                elif first_boot_monotonic is not None:
                    append_structured_record(paths, record, run_id, host_timestamp)
                    if record_type == "sample" and record.get("valid") is True:
                        valid_sample_records += 1
    except KeyboardInterrupt:
        if not quiet:
            print("\nDiagnostic stopped by operator.")
    finally:
        if connection is not None:
            try:
                connection.close()
            except Exception:
                pass

    evaluation = evaluate_stability(
        boot_records=boot_records,
        brownout_lines=brownout_lines,
        disconnects_after_start=disconnects_after_start,
        valid_sample_records=valid_sample_records,
        completed_window=completed_window,
    )
    metadata.update(
        {
            "status": "passed" if evaluation.passed else "failed",
            "completed_at_utc": ihap45.utc_now(),
            "boot_records": boot_records,
            "brownout_lines": brownout_lines,
            "disconnects_before_start": disconnects_before_start,
            "disconnects_after_start": disconnects_after_start,
            "valid_sample_records": valid_sample_records,
            "completed_window": completed_window,
            "serial_port_history": port_history,
            "errors": evaluation.errors,
            "warnings": evaluation.warnings,
        }
    )
    ihap45.atomic_write_text(paths["metadata"], json.dumps(metadata, indent=2) + "\n")
    (run_dir / "stability-summary.json").write_text(
        json.dumps(
            {
                "run_id": run_id,
                "configuration_label": label,
                "passed": evaluation.passed,
                "errors": evaluation.errors,
                "warnings": evaluation.warnings,
                "boot_records": boot_records,
                "brownout_lines": brownout_lines,
                "disconnects_before_start": disconnects_before_start,
                "disconnects_after_start": disconnects_after_start,
                "valid_sample_records": valid_sample_records,
                "completed_window": completed_window,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return evaluation


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", required=True)
    parser.add_argument("--label", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--baud", type=int, default=ihap45.DEFAULT_BAUD)
    parser.add_argument("--output-root", default=str(ihap45.DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--duration-seconds", type=float, default=DEFAULT_DURATION_SECONDS)
    parser.add_argument("--startup-timeout-seconds", type=float, default=DEFAULT_STARTUP_TIMEOUT_SECONDS)
    parser.add_argument("--reconnect-timeout-seconds", type=float, default=DEFAULT_RECONNECT_TIMEOUT_SECONDS)
    parser.add_argument("--reconnect-poll-seconds", type=float, default=DEFAULT_RECONNECT_POLL_SECONDS)
    parser.add_argument("--quiet", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = run_stability(
            port=args.port,
            baud=args.baud,
            run_dir=Path(args.output_root) / args.run_id,
            run_id=args.run_id,
            label=args.label,
            duration_seconds=args.duration_seconds,
            startup_timeout_seconds=args.startup_timeout_seconds,
            reconnect_timeout_seconds=args.reconnect_timeout_seconds,
            reconnect_poll_seconds=args.reconnect_poll_seconds,
            quiet=args.quiet,
        )
    except ihap45.HarnessError as exc:
        print(f"IHAP-45 ERROR: {exc}", file=sys.stderr)
        return 2
    for warning in result.warnings:
        print(f"WARNING: {warning}", file=sys.stderr)
    if not result.passed:
        for error in result.errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 2
    print("IHAP-45 stability diagnostic passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
