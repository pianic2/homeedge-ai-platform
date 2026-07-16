#!/usr/bin/env python3
"""Capture IHAP-47 firmware output without committing raw logs.

The script stores complete serial text locally, extracts JSON records, and lets the
operator append structured manual observations. It deliberately does not decide
whether a sensor passed.
"""

from __future__ import annotations

import argparse
import json
import queue
import re
import sys
import threading
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
    """Redact unique MAC-like identifiers from on-screen output only."""
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
            observations=(directory / "operator-observations.jsonl").open(
                "w", encoding="utf-8"
            ),
        )

    def close(self) -> None:
        self.serial_log.close()
        self.records.close()
        self.observations.close()


def serial_reader(
    connection: serial.Serial,
    files: SessionFiles,
    stop_event: threading.Event,
    terminal_queue: "queue.Queue[str]",
) -> None:
    while not stop_event.is_set():
        try:
            raw = connection.readline()
        except serial.SerialException as exc:
            terminal_queue.put(f"[serial-error] {exc}\n")
            stop_event.set()
            return

        if not raw:
            continue

        line = raw.decode("utf-8", errors="replace")
        files.serial_log.write(line)
        files.serial_log.flush()

        record = parse_json_record(line)
        if record is not None:
            files.records.write(json.dumps(record, separators=(",", ":")) + "\n")
            files.records.flush()

        terminal_queue.put(redact_console_text(line))


def terminal_writer(
    terminal_queue: "queue.Queue[str]", stop_event: threading.Event
) -> None:
    while not stop_event.is_set() or not terminal_queue.empty():
        try:
            text = terminal_queue.get(timeout=0.2)
        except queue.Empty:
            continue
        print(text, end="", flush=True)


def write_session_manifest(
    directory: Path, args: argparse.Namespace, ended_at: str | None = None
) -> None:
    manifest = {
        "schema_version": "1.0.0",
        "issue": "IHAP-47",
        "session_id": directory.name,
        "started_at_utc": args.started_at,
        "ended_at_utc": ended_at,
        "serial_baud": args.baud,
        "serial_port_recorded": False,
        "raw_logs_repository_allowed": False,
        "physical_results_validated": False,
        "notes": [
            "The serial port path is intentionally omitted from the manifest.",
            "Raw serial.log and records.jsonl are local working files and must not be committed.",
        ],
    }
    (directory / "session.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )


def append_observation(files: SessionFiles, payload_text: str) -> None:
    try:
        payload = json.loads(payload_text)
    except json.JSONDecodeError as exc:
        print(f"Invalid observation JSON: {exc}", file=sys.stderr)
        return

    if not isinstance(payload, dict):
        print("Observation must be a JSON object.", file=sys.stderr)
        return

    forbidden_keys = {"mac", "mac_address", "address", "serial_number", "local_path"}
    if forbidden_keys.intersection(payload):
        print(
            "Observation contains a forbidden sensitive key: "
            + ", ".join(sorted(forbidden_keys.intersection(payload))),
            file=sys.stderr,
        )
        return

    record = {
        "record_type": "operator_observation",
        "schema_version": "1.0.0",
        "observed_at_utc": utc_now(),
        **payload,
    }
    files.observations.write(json.dumps(record, separators=(",", ":")) + "\n")
    files.observations.flush()
    print("Observation recorded locally.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", required=True, help="Serial device, for example /dev/ttyACM0")
    parser.add_argument("--baud", type=int, default=115200)
    parser.add_argument("--output-root", type=Path, default=Path("output"))
    parser.add_argument("--session-id", default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    args.started_at = utc_now()
    session_id = args.session_id or safe_session_id()

    try:
        files = SessionFiles.create(args.output_root, session_id)
    except FileExistsError:
        print(f"Session directory already exists: {args.output_root / session_id}", file=sys.stderr)
        return 2

    write_session_manifest(files.directory, args)

    try:
        connection = serial.Serial(args.port, args.baud, timeout=0.2)
    except serial.SerialException as exc:
        files.close()
        print(f"Unable to open serial port: {exc}", file=sys.stderr)
        return 2

    stop_event = threading.Event()
    terminal_queue: "queue.Queue[str]" = queue.Queue()
    reader = threading.Thread(
        target=serial_reader,
        args=(connection, files, stop_event, terminal_queue),
        daemon=True,
    )
    writer = threading.Thread(
        target=terminal_writer,
        args=(terminal_queue, stop_event),
        daemon=True,
    )
    reader.start()
    writer.start()

    print(f"Local session: {files.directory}")
    print("Firmware commands are sent as typed.")
    print('@observe {"specimen_id":"MC38-A",...} stores a local observation.')
    print("@quit ends the session.")

    try:
        while not stop_event.is_set():
            try:
                command = input()
            except EOFError:
                command = "@quit"

            if command.strip() == "@quit":
                stop_event.set()
                break

            if command.startswith("@observe "):
                append_observation(files, command[len("@observe ") :].strip())
                continue

            if not command.strip():
                continue

            try:
                connection.write((command.rstrip("\r\n") + "\n").encode("utf-8"))
                connection.flush()
            except serial.SerialException as exc:
                print(f"Unable to send command: {exc}", file=sys.stderr)
                stop_event.set()
                break
    except KeyboardInterrupt:
        stop_event.set()
    finally:
        stop_event.set()
        reader.join(timeout=2)
        writer.join(timeout=2)
        connection.close()
        write_session_manifest(files.directory, args, ended_at=utc_now())
        files.close()

    print(f"Capture ended. Raw local files remain under {files.directory}")
    print(f"Next: python scripts/build_report.py {files.directory}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
