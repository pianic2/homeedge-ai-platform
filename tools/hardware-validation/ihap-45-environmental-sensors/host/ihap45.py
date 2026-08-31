#!/usr/bin/env python3
"""IHAP-45 serial capture, phase marking, validation and analysis tool."""

from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

SCHEMA_VERSION = "1.0.0"
DEFAULT_BAUD = 115200
DEFAULT_OUTPUT_ROOT = Path("runs")
PRESSURE_FIELDS = {"pressure", "pressure_pa", "pressure_hpa"}
SAMPLE_REQUIRED_FIELDS = {
    "record_type",
    "schema_version",
    "batch_id",
    "uptime_ms",
    "sensor_id",
    "sensor_type",
    "valid",
    "error_code",
    "temperature_c",
    "humidity_percent",
    "read_duration_us",
}


class HarnessError(RuntimeError):
    """Actionable validation or acquisition error."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def atomic_write_text(path: Path, content: str) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(content, encoding="utf-8")
    temporary.replace(path)


def append_jsonl(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as stream:
        json.dump(record, stream, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
        stream.write("\n")
        stream.flush()


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise HarnessError(f"Missing JSON file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise HarnessError(f"Invalid JSON in {path}: {exc}") from exc


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise HarnessError(f"Missing JSONL file: {path}")
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                value = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise HarnessError(f"Invalid JSONL at {path}:{line_number}: {exc}") from exc
            if not isinstance(value, dict):
                raise HarnessError(f"JSONL record is not an object at {path}:{line_number}")
            records.append(value)
    return records


def parse_firmware_json(line: str) -> dict[str, Any] | None:
    stripped = line.strip()
    if not stripped.startswith("{") or not stripped.endswith("}"):
        return None
    try:
        value = json.loads(stripped)
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


def pressure_fields_in(record: dict[str, Any]) -> set[str]:
    return PRESSURE_FIELDS.intersection(record)


def validate_sample_record(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = SAMPLE_REQUIRED_FIELDS.difference(record)
    if missing:
        errors.append(f"missing fields: {sorted(missing)}")
    forbidden = pressure_fields_in(record)
    if forbidden:
        errors.append(f"forbidden pressure fields: {sorted(forbidden)}")
    if record.get("record_type") != "sample":
        errors.append("record_type is not sample")
    if record.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"unsupported schema_version: {record.get('schema_version')!r}")
    if not isinstance(record.get("valid"), bool):
        errors.append("valid must be boolean")
    if record.get("valid") is True:
        for field in ("temperature_c", "humidity_percent"):
            value = record.get(field)
            if not isinstance(value, (int, float)) or not math.isfinite(float(value)):
                errors.append(f"{field} must be finite for a valid sample")
        humidity = record.get("humidity_percent")
        if isinstance(humidity, (int, float)) and not 0.0 <= float(humidity) <= 100.0:
            errors.append("humidity_percent outside 0..100")
        if record.get("error_code") is not None:
            errors.append("valid sample must have null error_code")
    else:
        if record.get("error_code") in (None, ""):
            errors.append("invalid sample must contain error_code")
    return errors


def run_paths(run_dir: Path) -> dict[str, Path]:
    return {
        "metadata": run_dir / "run-metadata.json",
        "phase": run_dir / "current-phase.txt",
        "markers": run_dir / "markers.jsonl",
        "reference": run_dir / "reference.jsonl",
        "serial": run_dir / "raw" / "serial.log",
        "samples": run_dir / "raw" / "samples.jsonl",
        "results": run_dir / "results",
    }


def initialize_run(run_dir: Path, run_id: str, port: str, baud: int, plan_path: Path) -> dict[str, Path]:
    paths = run_paths(run_dir)
    if run_dir.exists() and any(run_dir.iterdir()):
        raise HarnessError(f"Run directory already exists and is not empty: {run_dir}")
    (run_dir / "raw").mkdir(parents=True, exist_ok=True)
    paths["phase"].write_text("unclassified\n", encoding="utf-8")
    paths["markers"].touch()
    paths["reference"].touch()
    paths["serial"].touch()
    paths["samples"].touch()
    metadata = {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "status": "capturing",
        "started_at_utc": utc_now(),
        "completed_at_utc": None,
        "serial_port": port,
        "baud": baud,
        "test_plan": str(plan_path),
        "comparison_scope": "relative_unless_reference_observations_exist",
        "measurement_channels": ["temperature_c", "humidity_percent"],
        "operator": "Project Owner",
    }
    atomic_write_text(paths["metadata"], json.dumps(metadata, indent=2, ensure_ascii=False) + "\n")
    append_jsonl(
        paths["markers"],
        {
            "record_type": "phase_marker",
            "schema_version": SCHEMA_VERSION,
            "run_id": run_id,
            "host_timestamp_utc": metadata["started_at_utc"],
            "phase": "unclassified",
            "note": "Capture started",
        },
    )
    return paths


def current_phase(path: Path) -> str:
    try:
        phase = path.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        return "unclassified"
    return phase or "unclassified"


def capture_serial(
    *,
    port: str,
    baud: int,
    run_dir: Path,
    run_id: str,
    plan_path: Path,
    duration_seconds: float | None = None,
    quiet: bool = False,
) -> None:
    try:
        import serial
    except ImportError as exc:
        raise HarnessError("pyserial is required. Install host/requirements.txt") from exc

    paths = initialize_run(run_dir, run_id, port, baud, plan_path)
    metadata = load_json(paths["metadata"])
    started = time.monotonic()
    parsed_samples = 0
    boot_records = 0
    probe_records = 0

    try:
        with serial.Serial(port=port, baudrate=baud, timeout=1.0) as connection, paths["serial"].open(
            "a", encoding="utf-8", newline="\n"
        ) as raw_log:
            connection.reset_input_buffer()
            if not quiet:
                print(f"Capturing {port} at {baud} baud into {run_dir}")
                print("Use a second terminal with: python host/ihap45.py mark ...")
            while True:
                if duration_seconds is not None and time.monotonic() - started >= duration_seconds:
                    break
                payload = connection.readline()
                if not payload:
                    continue
                text = payload.decode("utf-8", errors="replace").rstrip("\r\n")
                host_timestamp = utc_now()
                raw_log.write(f"{host_timestamp}\t{text}\n")
                raw_log.flush()
                if not quiet:
                    print(text)

                record = parse_firmware_json(text)
                if record is None:
                    continue
                forbidden = pressure_fields_in(record)
                if forbidden:
                    raise HarnessError(f"Firmware emitted forbidden pressure fields: {sorted(forbidden)}")

                record_type = record.get("record_type")
                if record_type == "harness_boot":
                    boot_records += 1
                    append_jsonl(
                        paths["samples"],
                        {
                            **record,
                            "run_id": run_id,
                            "host_timestamp_utc": host_timestamp,
                            "phase": current_phase(paths["phase"]),
                        },
                    )
                elif record_type == "sensor_probe":
                    probe_records += 1
                    append_jsonl(
                        paths["samples"],
                        {
                            **record,
                            "run_id": run_id,
                            "host_timestamp_utc": host_timestamp,
                            "phase": current_phase(paths["phase"]),
                        },
                    )
                elif record_type == "sample":
                    errors = validate_sample_record(record)
                    if errors:
                        raise HarnessError(f"Invalid sample record: {'; '.join(errors)}; record={record}")
                    append_jsonl(
                        paths["samples"],
                        {
                            **record,
                            "run_id": run_id,
                            "host_timestamp_utc": host_timestamp,
                            "phase": current_phase(paths["phase"]),
                        },
                    )
                    parsed_samples += 1
    except KeyboardInterrupt:
        if not quiet:
            print("\nCapture stopped by operator.")
    finally:
        metadata.update(
            {
                "status": "captured",
                "completed_at_utc": utc_now(),
                "parsed_sample_records": parsed_samples,
                "boot_records": boot_records,
                "probe_records": probe_records,
            }
        )
        atomic_write_text(paths["metadata"], json.dumps(metadata, indent=2, ensure_ascii=False) + "\n")


def command_mark(args: argparse.Namespace) -> None:
    run_dir = Path(args.run_dir)
    paths = run_paths(run_dir)
    metadata = load_json(paths["metadata"])
    plan = load_json(Path(args.plan)) if args.plan else None
    if plan is not None:
        allowed = {phase["name"] for phase in plan.get("phases", [])}
        allowed.add("unclassified")
        if args.phase not in allowed:
            raise HarnessError(f"Unknown phase {args.phase!r}; allowed: {sorted(allowed)}")
    atomic_write_text(paths["phase"], args.phase + "\n")
    record = {
        "record_type": "phase_marker",
        "schema_version": SCHEMA_VERSION,
        "run_id": metadata["run_id"],
        "host_timestamp_utc": utc_now(),
        "phase": args.phase,
        "note": args.note,
    }
    append_jsonl(paths["markers"], record)
    print(f"Phase set to {args.phase!r} for {metadata['run_id']}")


def command_reference(args: argparse.Namespace) -> None:
    run_dir = Path(args.run_dir)
    paths = run_paths(run_dir)
    metadata = load_json(paths["metadata"])
    if not math.isfinite(args.temperature_c):
        raise HarnessError("Reference temperature must be finite")
    if not math.isfinite(args.humidity_percent) or not 0.0 <= args.humidity_percent <= 100.0:
        raise HarnessError("Reference humidity must be finite and within 0..100")
    record = {
        "record_type": "reference_observation",
        "schema_version": SCHEMA_VERSION,
        "run_id": metadata["run_id"],
        "host_timestamp_utc": utc_now(),
        "phase": current_phase(paths["phase"]),
        "source_id": args.source_id,
        "temperature_c": args.temperature_c,
        "humidity_percent": args.humidity_percent,
        "note": args.note,
    }
    append_jsonl(paths["reference"], record)
    print("Reference observation recorded")


def parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def percentile(values: Sequence[float], p: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = (len(ordered) - 1) * p
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] * (1.0 - fraction) + ordered[upper] * fraction


def median_absolute_deviation(values: Sequence[float]) -> float | None:
    if not values:
        return None
    med = statistics.median(values)
    return statistics.median(abs(value - med) for value in values)


def summarize_numeric(values: Sequence[float]) -> dict[str, float | int | None]:
    if not values:
        return {"count": 0, "mean": None, "median": None, "stddev": None, "mad": None, "min": None, "max": None}
    return {
        "count": len(values),
        "mean": statistics.fmean(values),
        "median": statistics.median(values),
        "stddev": statistics.stdev(values) if len(values) > 1 else 0.0,
        "mad": median_absolute_deviation(values),
        "min": min(values),
        "max": max(values),
    }


@dataclass(frozen=True)
class ValidationResult:
    errors: list[str]
    warnings: list[str]
    summary: dict[str, Any]

    @property
    def ok(self) -> bool:
        return not self.errors


def validate_run(run_dir: Path, plan_path: Path) -> ValidationResult:
    paths = run_paths(run_dir)
    plan = load_json(plan_path)
    metadata = load_json(paths["metadata"])
    records = read_jsonl(paths["samples"])
    markers = read_jsonl(paths["markers"])
    errors: list[str] = []
    warnings: list[str] = []

    forbidden_fields = set(plan.get("forbidden_fields", [])) | PRESSURE_FIELDS
    for index, record in enumerate(records):
        found = forbidden_fields.intersection(record)
        if found:
            errors.append(f"record {index} contains forbidden fields {sorted(found)}")

    boot_records = [record for record in records if record.get("record_type") == "harness_boot"]
    probe_records = [record for record in records if record.get("record_type") == "sensor_probe"]
    samples = [record for record in records if record.get("record_type") == "sample"]

    if not boot_records:
        errors.append("missing harness_boot record")
    else:
        expected_channels = ["temperature_c", "humidity_percent"]
        if any(record.get("measurement_channels") != expected_channels for record in boot_records):
            errors.append(f"harness_boot does not declare exactly {expected_channels}")
        if len(boot_records) > 1:
            warnings.append(f"{len(boot_records)} boot records observed; check for reset loops")

    expected_chip_id = plan.get("validation", {}).get("require_bme280_chip_id", "0x60")
    successful_probe = any(
        record.get("sensor_id") == "BME280-OWNED-01"
        and record.get("chip_id") == expected_chip_id
        and record.get("detected_type") == "BME280"
        and record.get("humidity_supported") is True
        and record.get("status") == "OK"
        for record in probe_records
    )
    if not successful_probe:
        errors.append(f"missing successful BME280 probe with chip ID {expected_chip_id}")

    required_sensor_ids = set(plan.get("required_sensor_ids", []))
    sample_sensor_ids = {record.get("sensor_id") for record in samples}
    missing_sensors = required_sensor_ids.difference(sample_sensor_ids)
    if missing_sensors:
        errors.append(f"missing sensor samples: {sorted(missing_sensors)}")

    invalid_schema_records = 0
    for sample in samples:
        sample_errors = validate_sample_record(sample)
        if sample_errors:
            invalid_schema_records += 1
            errors.append(f"invalid sample batch={sample.get('batch_id')} sensor={sample.get('sensor_id')}: {'; '.join(sample_errors)}")
            if invalid_schema_records >= 20:
                errors.append("additional invalid sample errors truncated")
                break

    expected_phases = {phase["name"] for phase in plan.get("phases", [])}
    observed_phases = {record.get("phase") for record in markers} | {record.get("phase") for record in samples}
    missing_phases = expected_phases.difference(observed_phases)
    if missing_phases:
        errors.append(f"missing required phases: {sorted(missing_phases)}")

    phase_durations: dict[str, float] = defaultdict(float)
    valid_timestamps = sorted(
        (parse_timestamp(record["host_timestamp_utc"]), str(record.get("phase", "unclassified")))
        for record in samples
        if record.get("record_type") == "sample" and record.get("host_timestamp_utc")
    )
    for (first_time, first_phase), (second_time, _) in zip(valid_timestamps, valid_timestamps[1:]):
        delta = (second_time - first_time).total_seconds()
        if 0.0 <= delta <= 30.0:
            phase_durations[first_phase] += delta
    for phase in plan.get("phases", []):
        actual = phase_durations.get(phase["name"], 0.0)
        minimum = float(phase.get("minimum_seconds", 0))
        if actual + 1.0 < minimum:
            errors.append(f"phase {phase['name']} duration {actual:.1f}s below minimum {minimum:.1f}s")

    per_sensor: dict[str, dict[str, Any]] = {}
    min_valid = int(plan.get("validation", {}).get("minimum_valid_samples_per_sensor", 1))
    min_completeness = float(plan.get("validation", {}).get("minimum_completeness_percent", 0.0))
    max_batches = max((int(sample.get("batch_id", 0)) for sample in samples), default=0)
    for sensor_id in sorted(required_sensor_ids):
        sensor_samples = [sample for sample in samples if sample.get("sensor_id") == sensor_id]
        valid_samples = [sample for sample in sensor_samples if sample.get("valid") is True]
        completeness = (len(sensor_samples) / max_batches * 100.0) if max_batches else 0.0
        valid_ratio = (len(valid_samples) / len(sensor_samples) * 100.0) if sensor_samples else 0.0
        if len(valid_samples) < min_valid:
            errors.append(f"{sensor_id} has {len(valid_samples)} valid samples; minimum is {min_valid}")
        if completeness < min_completeness:
            errors.append(f"{sensor_id} completeness {completeness:.2f}% below {min_completeness:.2f}%")
        per_sensor[sensor_id] = {
            "sample_records": len(sensor_samples),
            "valid_samples": len(valid_samples),
            "completeness_percent": completeness,
            "valid_percent": valid_ratio,
            "errors": dict(Counter(sample.get("error_code") for sample in sensor_samples if not sample.get("valid"))),
        }

    references = read_jsonl(paths["reference"]) if paths["reference"].exists() else []
    if not references:
        warnings.append("no independent reference observations; absolute accuracy metrics are not available")

    summary = {
        "run_id": metadata.get("run_id"),
        "sample_records": len(samples),
        "boot_records": len(boot_records),
        "probe_records": len(probe_records),
        "phase_durations_seconds": dict(phase_durations),
        "per_sensor": per_sensor,
        "reference_observations": len(references),
    }
    return ValidationResult(errors=errors, warnings=warnings, summary=summary)


def nearest_reference(
    sample_time: datetime,
    references: Sequence[dict[str, Any]],
    max_seconds: float,
) -> dict[str, Any] | None:
    candidates: list[tuple[float, dict[str, Any]]] = []
    for reference in references:
        timestamp = reference.get("host_timestamp_utc")
        if not timestamp:
            continue
        distance = abs((parse_timestamp(timestamp) - sample_time).total_seconds())
        if distance <= max_seconds:
            candidates.append((distance, reference))
    return min(candidates, key=lambda item: item[0])[1] if candidates else None


def response_time_seconds(
    records: Sequence[dict[str, Any]],
    field: str,
    transition_phase: str,
    target_phase: str,
    prior_phase: str,
) -> float | None:
    transition_records = [
        record
        for record in records
        if record.get("phase") in {transition_phase, target_phase} and record.get("valid")
    ]
    transition_records.sort(key=lambda record: parse_timestamp(record["host_timestamp_utc"]))
    target_records = [record for record in records if record.get("phase") == target_phase and record.get("valid")]
    prior_records = [record for record in records if record.get("phase") == prior_phase and record.get("valid")]
    values_target = [float(record[field]) for record in target_records if isinstance(record.get(field), (int, float))]
    values_prior = [float(record[field]) for record in prior_records if isinstance(record.get(field), (int, float))]
    if not transition_records or not values_target or not values_prior:
        return None
    start_value = statistics.median(values_prior)
    end_value = statistics.median(values_target[-max(3, len(values_target) // 4) :])
    delta = end_value - start_value
    if abs(delta) < 1e-9:
        return None
    threshold = start_value + 0.9 * delta
    start_time = parse_timestamp(transition_records[0]["host_timestamp_utc"])
    for record in transition_records:
        value = record.get(field)
        if not isinstance(value, (int, float)):
            continue
        reached = float(value) >= threshold if delta > 0 else float(value) <= threshold
        if reached:
            return (parse_timestamp(record["host_timestamp_utc"]) - start_time).total_seconds()
    return None


def compute_analysis(run_dir: Path, plan_path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    paths = run_paths(run_dir)
    plan = load_json(plan_path)
    records = read_jsonl(paths["samples"])
    samples = [record for record in records if record.get("record_type") == "sample"]
    references = read_jsonl(paths["reference"]) if paths["reference"].exists() else []
    required_sensor_ids = list(plan.get("required_sensor_ids", []))
    max_reference_seconds = float(plan.get("validation", {}).get("maximum_reference_join_seconds", 60))

    summary: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "run_id": load_json(paths["metadata"]).get("run_id"),
        "generated_at_utc": utc_now(),
        "measurement_channels": ["temperature_c", "humidity_percent"],
        "comparison_scope": "absolute_and_relative" if references else "relative_only",
        "per_sensor": {},
        "pairwise": {},
    }

    comparison_rows: list[dict[str, Any]] = []
    samples_by_sensor: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for sample in samples:
        samples_by_sensor[str(sample.get("sensor_id"))].append(sample)
        row = dict(sample)
        if sample.get("valid") and sample.get("host_timestamp_utc"):
            reference = nearest_reference(parse_timestamp(sample["host_timestamp_utc"]), references, max_reference_seconds)
            if reference is not None:
                row["reference_temperature_c"] = reference["temperature_c"]
                row["reference_humidity_percent"] = reference["humidity_percent"]
                row["temperature_error_c"] = float(sample["temperature_c"]) - float(reference["temperature_c"])
                row["humidity_error_percent"] = float(sample["humidity_percent"]) - float(reference["humidity_percent"])
        comparison_rows.append(row)

    plateau_phases = {phase["name"] for phase in plan.get("phases", []) if phase.get("kind") == "plateau"}
    for sensor_id in required_sensor_ids:
        sensor_records = samples_by_sensor.get(sensor_id, [])
        valid = [record for record in sensor_records if record.get("valid") is True]
        temperatures = [float(record["temperature_c"]) for record in valid]
        humidities = [float(record["humidity_percent"]) for record in valid]
        durations = [float(record["read_duration_us"]) for record in sensor_records if isinstance(record.get("read_duration_us"), (int, float))]
        per_phase: dict[str, Any] = {}
        for phase in sorted(plateau_phases):
            phase_records = [record for record in valid if record.get("phase") == phase]
            per_phase[phase] = {
                "temperature_c": summarize_numeric([float(record["temperature_c"]) for record in phase_records]),
                "humidity_percent": summarize_numeric([float(record["humidity_percent"]) for record in phase_records]),
            }
        reference_rows = [row for row in comparison_rows if row.get("sensor_id") == sensor_id and "temperature_error_c" in row]
        reference_metrics: dict[str, Any] | None = None
        if reference_rows:
            temp_errors = [float(row["temperature_error_c"]) for row in reference_rows]
            humidity_errors = [float(row["humidity_error_percent"]) for row in reference_rows]
            reference_metrics = {
                "matched_observations": len(reference_rows),
                "temperature_bias_c": statistics.fmean(temp_errors),
                "temperature_mae_c": statistics.fmean(abs(value) for value in temp_errors),
                "temperature_rmse_c": math.sqrt(statistics.fmean(value * value for value in temp_errors)),
                "humidity_bias_percent": statistics.fmean(humidity_errors),
                "humidity_mae_percent": statistics.fmean(abs(value) for value in humidity_errors),
                "humidity_rmse_percent": math.sqrt(statistics.fmean(value * value for value in humidity_errors)),
            }
        summary["per_sensor"][sensor_id] = {
            "records": len(sensor_records),
            "valid_records": len(valid),
            "valid_percent": (len(valid) / len(sensor_records) * 100.0) if sensor_records else 0.0,
            "error_counts": dict(Counter(record.get("error_code") for record in sensor_records if not record.get("valid"))),
            "temperature_c": summarize_numeric(temperatures),
            "humidity_percent": summarize_numeric(humidities),
            "read_duration_us": {
                **summarize_numeric(durations),
                "p95": percentile(durations, 0.95),
            },
            "per_phase": per_phase,
            "response_seconds": {
                "humidity_ramp_up": response_time_seconds(
                    valid, "humidity_percent", "humidity_ramp_up", "humidity_high_plateau", "baseline"
                ),
                "temperature_ramp_up": response_time_seconds(
                    valid, "temperature_c", "temperature_ramp_up", "temperature_high_plateau", "humidity_final_recovery"
                ),
            },
            "reference_metrics": reference_metrics,
        }

    samples_by_batch: dict[int, dict[str, dict[str, Any]]] = defaultdict(dict)
    for sample in samples:
        if sample.get("valid") is True:
            samples_by_batch[int(sample["batch_id"])][str(sample["sensor_id"])] = sample
    for left_index, left_sensor in enumerate(required_sensor_ids):
        for right_sensor in required_sensor_ids[left_index + 1 :]:
            temp_deltas: list[float] = []
            humidity_deltas: list[float] = []
            for batch in samples_by_batch.values():
                if left_sensor in batch and right_sensor in batch:
                    temp_deltas.append(float(batch[left_sensor]["temperature_c"]) - float(batch[right_sensor]["temperature_c"]))
                    humidity_deltas.append(float(batch[left_sensor]["humidity_percent"]) - float(batch[right_sensor]["humidity_percent"]))
            key = f"{left_sensor}__minus__{right_sensor}"
            summary["pairwise"][key] = {
                "matched_batches": len(temp_deltas),
                "temperature_delta_c": summarize_numeric(temp_deltas),
                "humidity_delta_percent": summarize_numeric(humidity_deltas),
            }

    return summary, comparison_rows


def write_comparison_csv(path: Path, rows: Sequence[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = sorted({key for row in rows for key in row})
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_report_html(run_dir: Path, summary: dict[str, Any], rows: Sequence[dict[str, Any]]) -> None:
    try:
        import pandas as pd
        import plotly.express as px
        import plotly.io as pio
    except ImportError as exc:
        raise HarnessError("pandas and plotly are required. Install host/requirements.txt") from exc

    valid_rows = [row for row in rows if row.get("record_type") == "sample" and row.get("valid") is True]
    frame = pd.DataFrame(valid_rows)
    if frame.empty:
        raise HarnessError("No valid samples available for report generation")
    frame["host_timestamp_utc"] = pd.to_datetime(frame["host_timestamp_utc"], utc=True)

    figures = []
    for field, title, axis_title in (
        ("temperature_c", "Temperature timeline", "Temperature (°C)"),
        ("humidity_percent", "Relative humidity timeline", "Relative humidity (%)"),
    ):
        figure = px.line(
            frame,
            x="host_timestamp_utc",
            y=field,
            color="sensor_id",
            line_group="sensor_id",
            hover_data=["phase", "batch_id", "read_duration_us"],
            title=title,
        )
        figure.update_yaxes(title=axis_title)
        figures.append(figure)

    plateau = frame[frame["phase"].astype(str).str.contains("plateau|baseline|recovery", regex=True)]
    if not plateau.empty:
        temp_box = px.box(
            plateau,
            x="phase",
            y="temperature_c",
            color="sensor_id",
            points=False,
            title="Temperature distribution by stable phase",
        )
        temp_box.update_xaxes(tickangle=35)
        figures.append(temp_box)
        humidity_box = px.box(
            plateau,
            x="phase",
            y="humidity_percent",
            color="sensor_id",
            points=False,
            title="Humidity distribution by stable phase",
        )
        humidity_box.update_xaxes(tickangle=35)
        figures.append(humidity_box)

    figure_html = "\n".join(
        pio.to_html(figure, include_plotlyjs=True if index == 0 else False, full_html=False)
        for index, figure in enumerate(figures)
    )
    cards = []
    for sensor_id, metrics in summary["per_sensor"].items():
        cards.append(
            f"""
            <section class="card">
              <h3>{sensor_id}</h3>
              <p><strong>Valid:</strong> {metrics['valid_records']} / {metrics['records']} ({metrics['valid_percent']:.2f}%)</p>
              <p><strong>Errors:</strong> <code>{json.dumps(metrics['error_counts'], ensure_ascii=False)}</code></p>
              <p><strong>Median read latency:</strong> {metrics['read_duration_us']['median']} µs</p>
              <p><strong>Temperature MAD:</strong> {metrics['temperature_c']['mad']}</p>
              <p><strong>Humidity MAD:</strong> {metrics['humidity_percent']['mad']}</p>
            </section>
            """
        )
    scope_text = (
        "Absolute and relative comparison; independent reference observations were matched."
        if summary["comparison_scope"] == "absolute_and_relative"
        else "Relative comparison only. No independent reference was available; absolute accuracy remains UNVALIDATED."
    )
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>IHAP-45 Environmental Sensor Report</title>
<style>
body {{ font-family: system-ui, sans-serif; margin: 0; background: #f4f5f7; color: #172b4d; }}
main {{ max-width: 1280px; margin: auto; padding: 24px; }}
header, .card, .panel {{ background: white; border-radius: 12px; padding: 18px; margin-bottom: 18px; box-shadow: 0 2px 10px rgba(0,0,0,.08); }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fit,minmax(260px,1fr)); gap: 16px; }}
.warning {{ border-left: 5px solid #ffab00; }}
code {{ white-space: pre-wrap; }}
</style>
</head>
<body><main>
<header>
<h1>IHAP-45 Environmental Sensor Comparative Report</h1>
<p><strong>Run:</strong> {summary['run_id']}</p>
<p><strong>Generated:</strong> {summary['generated_at_utc']}</p>
<p><strong>Measurement channels:</strong> temperature and humidity only.</p>
</header>
<section class="panel warning"><strong>Evidence boundary:</strong> {scope_text}</section>
<section class="grid">{''.join(cards)}</section>
<section class="panel">{figure_html}</section>
<section class="panel"><h2>Machine-readable summary</h2><pre><code>{json.dumps(summary, indent=2, ensure_ascii=False)}</code></pre></section>
</main></body></html>"""
    (run_dir / "results" / "report.html").write_text(html, encoding="utf-8")


def command_validate(args: argparse.Namespace) -> None:
    result = validate_run(Path(args.run_dir), Path(args.plan))
    print(json.dumps(result.summary, indent=2, ensure_ascii=False))
    for warning in result.warnings:
        print(f"WARNING: {warning}", file=sys.stderr)
    if result.errors:
        for error in result.errors:
            print(f"ERROR: {error}", file=sys.stderr)
        raise HarnessError(f"Run validation failed with {len(result.errors)} error(s)")
    print("Run validation completed with no blocking errors.")


def command_analyze(args: argparse.Namespace) -> None:
    run_dir = Path(args.run_dir)
    validation = validate_run(run_dir, Path(args.plan))
    if validation.errors and not args.allow_incomplete:
        for error in validation.errors:
            print(f"ERROR: {error}", file=sys.stderr)
        raise HarnessError("Analysis blocked because validation failed; use --allow-incomplete only for diagnostics")
    summary, rows = compute_analysis(run_dir, Path(args.plan))
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    (results_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_comparison_csv(results_dir / "comparison.csv", rows)
    write_report_html(run_dir, summary, rows)
    print(f"Analysis written to {results_dir}")


def command_preflight(args: argparse.Namespace) -> None:
    run_id = args.run_id or f"IHAP45-PREFLIGHT-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    run_dir = Path(args.output_root) / run_id
    capture_serial(
        port=args.port,
        baud=args.baud,
        run_dir=run_dir,
        run_id=run_id,
        plan_path=Path(args.plan),
        duration_seconds=args.duration_seconds,
        quiet=args.quiet,
    )
    records = read_jsonl(run_paths(run_dir)["samples"])
    samples = [record for record in records if record.get("record_type") == "sample"]
    probes = [record for record in records if record.get("record_type") == "sensor_probe"]
    errors: list[str] = []
    required = {"DHT11-OWNED-01", "DHT22-OWNED-01", "BME280-OWNED-01"}
    valid_sensors = {record.get("sensor_id") for record in samples if record.get("valid") is True}
    if missing := required.difference(valid_sensors):
        errors.append(f"no valid preflight samples from {sorted(missing)}")
    if not any(
        probe.get("chip_id") == "0x60"
        and probe.get("detected_type") == "BME280"
        and probe.get("humidity_supported") is True
        and probe.get("status") == "OK"
        for probe in probes
    ):
        errors.append("owned purple breakout did not qualify as BME280 chip ID 0x60")
    if any(pressure_fields_in(record) for record in records):
        errors.append("pressure field detected")
    boot_count = sum(record.get("record_type") == "harness_boot" for record in records)
    if boot_count == 0:
        errors.append("no harness boot record")
    elif boot_count > 1:
        errors.append(f"multiple boot records ({boot_count}) indicate a possible reset loop")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        raise HarnessError("Preflight failed")
    print(f"Preflight passed. Evidence: {run_dir}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    capture = subparsers.add_parser("capture", help="Capture firmware serial output into a run directory")
    capture.add_argument("--port", required=True)
    capture.add_argument("--baud", type=int, default=DEFAULT_BAUD)
    capture.add_argument("--run-id", required=True)
    capture.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    capture.add_argument("--plan", default="config/test-plan.json")
    capture.add_argument("--quiet", action="store_true")

    preflight = subparsers.add_parser("preflight", help="Run a short qualification capture")
    preflight.add_argument("--port", required=True)
    preflight.add_argument("--baud", type=int, default=DEFAULT_BAUD)
    preflight.add_argument("--run-id")
    preflight.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    preflight.add_argument("--plan", default="config/test-plan.json")
    preflight.add_argument("--duration-seconds", type=float, default=120.0)
    preflight.add_argument("--quiet", action="store_true")

    mark = subparsers.add_parser("mark", help="Change the active environmental phase")
    mark.add_argument("--run-dir", required=True)
    mark.add_argument("--phase", required=True)
    mark.add_argument("--note", default=None)
    mark.add_argument("--plan", default="config/test-plan.json")

    reference = subparsers.add_parser("reference", help="Record an independent reference observation")
    reference.add_argument("--run-dir", required=True)
    reference.add_argument("--source-id", required=True)
    reference.add_argument("--temperature-c", required=True, type=float)
    reference.add_argument("--humidity-percent", required=True, type=float)
    reference.add_argument("--note", default=None)

    validate = subparsers.add_parser("validate", help="Validate evidence completeness and invariants")
    validate.add_argument("--run-dir", required=True)
    validate.add_argument("--plan", default="config/test-plan.json")

    analyze = subparsers.add_parser("analyze", help="Generate CSV, JSON and interactive HTML results")
    analyze.add_argument("--run-dir", required=True)
    analyze.add_argument("--plan", default="config/test-plan.json")
    analyze.add_argument("--allow-incomplete", action="store_true")

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "capture":
            capture_serial(
                port=args.port,
                baud=args.baud,
                run_dir=Path(args.output_root) / args.run_id,
                run_id=args.run_id,
                plan_path=Path(args.plan),
                quiet=args.quiet,
            )
        elif args.command == "preflight":
            command_preflight(args)
        elif args.command == "mark":
            command_mark(args)
        elif args.command == "reference":
            command_reference(args)
        elif args.command == "validate":
            command_validate(args)
        elif args.command == "analyze":
            command_analyze(args)
        else:
            parser.error(f"Unsupported command: {args.command}")
    except HarnessError as exc:
        print(f"IHAP-45 ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
