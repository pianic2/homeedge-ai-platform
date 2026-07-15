#!/usr/bin/env python3
"""Resilient IHAP-45 serial capture for ESP32-C3 native USB resets."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

import ihap45

DEFAULT_RECONNECT_TIMEOUT_SECONDS = 30.0
DEFAULT_RECONNECT_POLL_SECONDS = 0.25


@dataclass(frozen=True)
class PortIdentity:
    requested_path: str
    vid: int | None = None
    pid: int | None = None
    serial_number: str | None = None
    location: str | None = None


def discover_identity(requested_path: str, list_ports_module: Any) -> PortIdentity:
    requested_real = os.path.realpath(requested_path)
    for info in list_ports_module.comports():
        device_real = os.path.realpath(str(info.device))
        if str(info.device) == requested_path or device_real == requested_real:
            return PortIdentity(
                requested_path=requested_path,
                vid=getattr(info, "vid", None),
                pid=getattr(info, "pid", None),
                serial_number=getattr(info, "serial_number", None),
                location=getattr(info, "location", None),
            )
    return PortIdentity(requested_path=requested_path)


def select_port(identity: PortIdentity, list_ports_module: Any) -> str | None:
    if Path(identity.requested_path).exists():
        return identity.requested_path

    ports = list(list_ports_module.comports())
    if identity.serial_number:
        matches = [str(info.device) for info in ports if getattr(info, "serial_number", None) == identity.serial_number]
        if len(matches) == 1:
            return matches[0]

    if identity.vid is not None and identity.pid is not None and identity.location:
        matches = [
            str(info.device)
            for info in ports
            if getattr(info, "vid", None) == identity.vid
            and getattr(info, "pid", None) == identity.pid
            and getattr(info, "location", None) == identity.location
        ]
        if len(matches) == 1:
            return matches[0]

    if identity.vid is not None and identity.pid is not None:
        matches = [
            str(info.device)
            for info in ports
            if getattr(info, "vid", None) == identity.vid and getattr(info, "pid", None) == identity.pid
        ]
        if len(matches) == 1:
            return matches[0]

    requested_name = Path(identity.requested_path).name
    family = "ttyACM" if requested_name.startswith("ttyACM") else "ttyUSB" if requested_name.startswith("ttyUSB") else None
    if family:
        matches = [str(info.device) for info in ports if Path(str(info.device)).name.startswith(family)]
        if len(matches) == 1:
            return matches[0]
    return None


def wait_for_port(
    identity: PortIdentity,
    list_ports_module: Any,
    *,
    timeout_seconds: float,
    poll_seconds: float,
) -> str:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        selected = select_port(identity, list_ports_module)
        if selected:
            return selected
        time.sleep(poll_seconds)
    raise ihap45.HarnessError(
        f"Serial device did not reappear within {timeout_seconds:.1f}s: {identity.requested_path}"
    )


def append_record(paths: dict[str, Path], record: dict[str, Any], run_id: str, host_timestamp: str) -> str | None:
    forbidden = ihap45.pressure_fields_in(record)
    if forbidden:
        raise ihap45.HarnessError(f"Firmware emitted forbidden pressure fields: {sorted(forbidden)}")

    record_type = record.get("record_type")
    if record_type == "sample":
        errors = ihap45.validate_sample_record(record)
        if errors:
            raise ihap45.HarnessError(f"Invalid sample record: {'; '.join(errors)}; record={record}")
    elif record_type not in {"harness_boot", "sensor_probe"}:
        return None

    ihap45.append_jsonl(
        paths["samples"],
        {
            **record,
            "run_id": run_id,
            "host_timestamp_utc": host_timestamp,
            "phase": ihap45.current_phase(paths["phase"]),
        },
    )
    return str(record_type)


def capture_resilient(
    *,
    port: str,
    baud: int,
    run_dir: Path,
    run_id: str,
    plan_path: Path,
    duration_seconds: float | None,
    reconnect_timeout_seconds: float,
    reconnect_poll_seconds: float,
    quiet: bool,
) -> None:
    try:
        import serial
        from serial.tools import list_ports
    except ImportError as exc:
        raise ihap45.HarnessError("pyserial is required. Install host/requirements.txt") from exc

    paths = ihap45.initialize_run(run_dir, run_id, port, baud, plan_path)
    metadata = ihap45.load_json(paths["metadata"])
    identity = discover_identity(port, list_ports)
    started = time.monotonic()
    parsed_samples = 0
    boot_records = 0
    probe_records = 0
    reconnect_count = 0
    port_history: list[str] = []
    connection: Any | None = None

    if not quiet:
        print(f"Capturing {port} at {baud} baud into {run_dir}")
        print("The collector survives ESP32-C3 USB disconnect/re-enumeration after RST.")

    try:
        with paths["serial"].open("a", encoding="utf-8", newline="\n") as raw_log:
            while True:
                if duration_seconds is not None and time.monotonic() - started >= duration_seconds:
                    break

                if connection is None:
                    selected_port = wait_for_port(
                        identity,
                        list_ports,
                        timeout_seconds=reconnect_timeout_seconds,
                        poll_seconds=reconnect_poll_seconds,
                    )
                    try:
                        connection = serial.Serial(port=selected_port, baudrate=baud, timeout=1.0)
                    except (serial.SerialException, OSError):
                        connection = None
                        time.sleep(reconnect_poll_seconds)
                        continue
                    port_history.append(selected_port)
                    if not quiet:
                        action = "Connected" if reconnect_count == 0 else "Reconnected"
                        print(f"{action}: {selected_port}")

                try:
                    payload = connection.readline()
                except (serial.SerialException, OSError) as exc:
                    reconnect_count += 1
                    if not quiet:
                        print(
                            f"Serial connection interrupted ({exc}); waiting for USB device to reappear...",
                            file=sys.stderr,
                        )
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

                record = ihap45.parse_firmware_json(text)
                if record is None:
                    continue
                record_type = append_record(paths, record, run_id, host_timestamp)
                if record_type == "sample":
                    parsed_samples += 1
                elif record_type == "harness_boot":
                    boot_records += 1
                elif record_type == "sensor_probe":
                    probe_records += 1
    except KeyboardInterrupt:
        if not quiet:
            print("\nCapture stopped by operator.")
    finally:
        if connection is not None:
            try:
                connection.close()
            except Exception:
                pass
        metadata.update(
            {
                "status": "captured",
                "completed_at_utc": ihap45.utc_now(),
                "parsed_sample_records": parsed_samples,
                "boot_records": boot_records,
                "probe_records": probe_records,
                "serial_reconnect_count": reconnect_count,
                "serial_port_history": port_history,
            }
        )
        ihap45.atomic_write_text(paths["metadata"], json.dumps(metadata, indent=2, ensure_ascii=False) + "\n")


def validate_startup(run_dir: Path) -> list[str]:
    records = ihap45.read_jsonl(ihap45.run_paths(run_dir)["samples"])
    errors: list[str] = []
    boot_records = [record for record in records if record.get("record_type") == "harness_boot"]
    probes = [record for record in records if record.get("record_type") == "sensor_probe"]
    samples = [record for record in records if record.get("record_type") == "sample"]
    required = {"DHT11-OWNED-01", "DHT22-OWNED-01", "BME280-OWNED-01"}
    valid_sensors = {record.get("sensor_id") for record in samples if record.get("valid") is True}

    if not boot_records:
        errors.append("missing harness_boot record")
    if len(boot_records) > 1:
        errors.append(f"multiple harness_boot records observed: {len(boot_records)}")
    if not any(
        probe.get("chip_id") == "0x60"
        and probe.get("detected_type") == "BME280"
        and probe.get("humidity_supported") is True
        and probe.get("status") == "OK"
        for probe in probes
    ):
        errors.append("missing successful BME280 sensor_probe with chip ID 0x60")
    if missing := required.difference(valid_sensors):
        errors.append(f"missing valid samples from {sorted(missing)}")
    if any(ihap45.pressure_fields_in(record) for record in records):
        errors.append("pressure field detected")
    return errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command, help_text in (
        ("capture", "Capture a full run and reconnect automatically after USB reset"),
        ("preflight", "Capture a short startup qualification with automatic USB reconnect"),
    ):
        subparser = subparsers.add_parser(command, help=help_text)
        subparser.add_argument("--port", required=True)
        subparser.add_argument("--baud", type=int, default=ihap45.DEFAULT_BAUD)
        subparser.add_argument("--run-id", required=command == "capture")
        subparser.add_argument("--output-root", default=str(ihap45.DEFAULT_OUTPUT_ROOT))
        subparser.add_argument("--plan", default="config/test-plan.json")
        subparser.add_argument("--reconnect-timeout-seconds", type=float, default=DEFAULT_RECONNECT_TIMEOUT_SECONDS)
        subparser.add_argument("--reconnect-poll-seconds", type=float, default=DEFAULT_RECONNECT_POLL_SECONDS)
        subparser.add_argument("--quiet", action="store_true")
        if command == "preflight":
            subparser.add_argument("--duration-seconds", type=float, default=120.0)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    run_id = args.run_id or f"IHAP45-PREFLIGHT-{time.strftime('%Y%m%d-%H%M%S')}"
    run_dir = Path(args.output_root) / run_id
    try:
        capture_resilient(
            port=args.port,
            baud=args.baud,
            run_dir=run_dir,
            run_id=run_id,
            plan_path=Path(args.plan),
            duration_seconds=args.duration_seconds if args.command == "preflight" else None,
            reconnect_timeout_seconds=args.reconnect_timeout_seconds,
            reconnect_poll_seconds=args.reconnect_poll_seconds,
            quiet=args.quiet,
        )
        if args.command == "preflight":
            errors = validate_startup(run_dir)
            if errors:
                for error in errors:
                    print(f"ERROR: {error}", file=sys.stderr)
                raise ihap45.HarnessError("Resilient preflight failed")
            print(f"Resilient preflight passed. Evidence: {run_dir}")
    except ihap45.HarnessError as exc:
        print(f"IHAP-45 ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
