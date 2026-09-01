#!/usr/bin/env python3
"""Publish allow-listed IHAP-45 aggregate evidence without copying raw telemetry."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import ihap45
import ihap45_final_gate

PUBLICATION_SCHEMA_VERSION = "1.0.0"
FORBIDDEN_PUBLISHED_KEYS = {"pressure", "pressure_pa", "pressure_hpa"}


class PublicationError(RuntimeError):
    """Raised when a source run cannot be safely summarized."""


def safe_filename(value: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip()).strip("-._")
    if not normalized:
        raise PublicationError("run identifier cannot be converted to a safe filename")
    return normalized


def load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise PublicationError(f"missing source file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise PublicationError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise PublicationError(f"expected a JSON object in {path}")
    return value


def recursively_find_forbidden_keys(value: Any, path: str = "$") -> list[str]:
    findings: list[str] = []
    if isinstance(value, Mapping):
        for key, nested in value.items():
            key_text = str(key)
            if key_text in FORBIDDEN_PUBLISHED_KEYS:
                findings.append(f"{path}.{key_text}")
            findings.extend(recursively_find_forbidden_keys(nested, f"{path}.{key_text}"))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            findings.extend(recursively_find_forbidden_keys(nested, f"{path}[{index}]"))
    return findings


def write_outputs(output_dir: Path, stem: str, summary: dict[str, Any], markdown: str) -> tuple[Path, Path]:
    forbidden = recursively_find_forbidden_keys(summary)
    if forbidden:
        raise PublicationError(f"summary contains forbidden pressure fields: {forbidden}")
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{stem}.summary.json"
    markdown_path = output_dir / f"{stem}.summary.md"
    json_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")
    markdown_path.write_text(markdown.rstrip() + "\n", encoding="utf-8")
    return json_path, markdown_path


def metric_value(metrics: Mapping[str, Any] | None, field: str) -> Any:
    return None if metrics is None else metrics.get(field)


def format_number(value: Any, digits: int = 3) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return f"{value:.{digits}f}"
    return str(value)


def sanitize_stability(run_dir: Path) -> dict[str, Any]:
    source = load_object(run_dir / "stability-summary.json")
    metadata = load_object(run_dir / "run-metadata.json")
    run_id = str(source.get("run_id") or metadata.get("run_id") or run_dir.name)
    return {
        "publication_schema_version": PUBLICATION_SCHEMA_VERSION,
        "evidence_type": "functional_stability_summary",
        "run_id": run_id,
        "configuration_label": source.get("configuration_label"),
        "status": "passed" if source.get("passed") is True else "failed",
        "passed": source.get("passed") is True,
        "qualification_duration_seconds": metadata.get("qualification_duration_seconds"),
        "completed_window": source.get("completed_window") is True,
        "boot_records": int(source.get("boot_records", 0)),
        "brownout_events": int(source.get("brownout_lines", 0)),
        "usb_disconnects_after_start": int(source.get("disconnects_after_start", 0)),
        "valid_sample_records": int(source.get("valid_sample_records", 0)),
        "errors": list(source.get("errors", [])),
        "warnings": list(source.get("warnings", [])),
        "measurement_claim": "functional stability only; no quantitative power characterization",
        "source_data_policy": "raw local run retained or reproducible; raw telemetry not published",
    }


def stability_markdown(summary: Mapping[str, Any]) -> str:
    errors = summary.get("errors") or []
    warnings = summary.get("warnings") or []
    error_lines = "\n".join(f"- {item}" for item in errors) if errors else "- none"
    warning_lines = "\n".join(f"- {item}" for item in warnings) if warnings else "- none"
    return f"""# IHAP-45 Functional Stability Summary — {summary['run_id']}

**Configuration:** `{summary.get('configuration_label')}`  
**Status:** `{str(summary.get('status')).upper()}`  
**Scope:** functional stability only; no quantitative power characterization

## Aggregate result

| Check | Result |
|---|---:|
| Qualification duration | {format_number(summary.get('qualification_duration_seconds'), 1)} s |
| Completed window | {format_number(summary.get('completed_window'))} |
| Boot records | {format_number(summary.get('boot_records'))} |
| Brownout events | {format_number(summary.get('brownout_events'))} |
| USB disconnects after start | {format_number(summary.get('usb_disconnects_after_start'))} |
| Valid sample records | {format_number(summary.get('valid_sample_records'))} |

## Errors

{error_lines}

## Warnings

{warning_lines}

## Evidence boundary

The serial log and individual samples remain local and are not included in the repository. This file was produced from allow-listed aggregate fields by `host/ihap45_publish.py`.
"""


def first_successful_probe(records: Sequence[dict[str, Any]]) -> dict[str, Any] | None:
    for record in records:
        if (
            record.get("record_type") == "sensor_probe"
            and record.get("sensor_id") == "BME280-OWNED-01"
            and record.get("chip_id") == "0x60"
            and record.get("detected_type") == "BME280"
            and record.get("humidity_supported") is True
            and record.get("status") == "OK"
        ):
            return {
                "sensor_id": "BME280-OWNED-01",
                "i2c_address": record.get("i2c_address"),
                "chip_id": record.get("chip_id"),
                "detected_type": record.get("detected_type"),
                "humidity_supported": True,
                "status": "OK",
            }
    return None


def first_boot_metadata(records: Sequence[dict[str, Any]]) -> dict[str, Any] | None:
    for record in records:
        if record.get("record_type") == "harness_boot":
            return {
                "firmware": record.get("firmware"),
                "idf_version": record.get("idf_version"),
                "sample_interval_ms": record.get("sample_interval_ms"),
                "measurement_channels": record.get("measurement_channels"),
                "pins": record.get("pins"),
                "i2c_frequency_hz": record.get("i2c_frequency_hz"),
            }
    return None


def sanitize_environmental(run_dir: Path, plan_path: Path) -> dict[str, Any]:
    # Publication is an acceptance action, so it must execute the same strict gate
    # that checks reboot count, BME280 identity and serial-log brownouts.
    gate = ihap45_final_gate.evaluate_final_gate(run_dir, plan_path)
    validation = ihap45.validate_run(run_dir, plan_path)
    analysis, _rows = ihap45.compute_analysis(run_dir, plan_path)
    plan = load_object(plan_path)
    records = ihap45.read_jsonl(ihap45.run_paths(run_dir)["samples"])

    publication_errors = list(gate.errors)
    publication_warnings = list(dict.fromkeys([*validation.warnings, *gate.warnings]))
    status = "passed" if gate.passed and not publication_errors else "failed"

    sanitized_per_sensor: dict[str, Any] = {}
    for sensor_id, metrics in analysis.get("per_sensor", {}).items():
        sanitized_per_sensor[str(sensor_id)] = {
            "records": metrics.get("records"),
            "valid_records": metrics.get("valid_records"),
            "valid_percent": metrics.get("valid_percent"),
            "error_counts": metrics.get("error_counts"),
            "temperature_c": metrics.get("temperature_c"),
            "humidity_percent": metrics.get("humidity_percent"),
            "read_duration_us": metrics.get("read_duration_us"),
            "per_phase": metrics.get("per_phase"),
            "response_seconds": metrics.get("response_seconds"),
            "reference_metrics": metrics.get("reference_metrics"),
        }

    return {
        "publication_schema_version": PUBLICATION_SCHEMA_VERSION,
        "evidence_type": "environmental_comparison_summary",
        "run_id": analysis.get("run_id") or run_dir.name,
        "plan_id": plan.get("plan_id"),
        "status": status,
        "validation_passed": status == "passed",
        "comparison_scope": analysis.get("comparison_scope"),
        "measurement_channels": ["temperature_c", "humidity_percent"],
        "firmware": first_boot_metadata(records),
        "qualified_bme280": first_successful_probe(records),
        "validation": {
            "errors": publication_errors,
            "warnings": publication_warnings,
            "sample_records": validation.summary.get("sample_records"),
            "boot_records": gate.summary.get("boot_records"),
            "probe_records": gate.summary.get("probe_records"),
            "brownout_events": gate.summary.get("brownout_events"),
            "phase_durations_seconds": validation.summary.get("phase_durations_seconds"),
            "per_sensor": validation.summary.get("per_sensor"),
            "reference_observations": validation.summary.get("reference_observations"),
        },
        "results": {
            "per_sensor": sanitized_per_sensor,
            "pairwise": analysis.get("pairwise", {}),
        },
        "limitations": [
            "Raw serial and per-sample telemetry are local-only and are not published.",
            "Absolute accuracy is unvalidated unless comparison_scope is absolute_and_relative and reference metrics exist.",
            "Results apply to the owned specimens and executed placement, not every unit of each sensor family.",
            "Pressure is outside scope and must not appear in the published schema.",
            "Power consumption, rail capacity and autonomy are outside IHAP-45.",
        ],
        "source_data_policy": "raw local run retained or reproducible; allow-listed aggregate summary only",
    }


def environmental_markdown(summary: Mapping[str, Any]) -> str:
    validation = summary.get("validation", {})
    results = summary.get("results", {})
    firmware = summary.get("firmware") or {}
    probe = summary.get("qualified_bme280") or {}

    sensor_rows: list[str] = []
    for sensor_id, metrics in (results.get("per_sensor") or {}).items():
        temperature = metrics.get("temperature_c") or {}
        humidity = metrics.get("humidity_percent") or {}
        latency = metrics.get("read_duration_us") or {}
        sensor_rows.append(
            "| {sensor} | {valid}/{records} | {valid_percent}% | {temp_mean} | {temp_std} | {rh_mean} | {rh_std} | {latency} |".format(
                sensor=sensor_id,
                valid=format_number(metrics.get("valid_records")),
                records=format_number(metrics.get("records")),
                valid_percent=format_number(metrics.get("valid_percent"), 2),
                temp_mean=format_number(metric_value(temperature, "mean")),
                temp_std=format_number(metric_value(temperature, "stddev")),
                rh_mean=format_number(metric_value(humidity, "mean")),
                rh_std=format_number(metric_value(humidity, "stddev")),
                latency=format_number(metric_value(latency, "median"), 1),
            )
        )
    if not sensor_rows:
        sensor_rows.append("| none | n/a | n/a | n/a | n/a | n/a | n/a | n/a |")

    phase_rows = [
        f"| `{phase}` | {format_number(seconds, 1)} |"
        for phase, seconds in (validation.get("phase_durations_seconds") or {}).items()
    ] or ["| none | n/a |"]
    error_lines = "\n".join(f"- {item}" for item in validation.get("errors", [])) or "- none"
    warning_lines = "\n".join(f"- {item}" for item in validation.get("warnings", [])) or "- none"

    return f"""# IHAP-45 Environmental Comparison Summary — {summary['run_id']}

**Status:** `{str(summary.get('status')).upper()}`  
**Plan:** `{summary.get('plan_id')}`  
**Comparison scope:** `{summary.get('comparison_scope')}`  
**Published channels:** temperature and relative humidity only

## Harness identity

| Field | Value |
|---|---|
| Firmware | `{firmware.get('firmware')}` |
| ESP-IDF | `{firmware.get('idf_version')}` |
| Sample interval | {format_number(firmware.get('sample_interval_ms'))} ms |
| BME280 address | `{probe.get('i2c_address')}` |
| BME280 chip ID | `{probe.get('chip_id')}` |
| Humidity supported | {format_number(probe.get('humidity_supported'))} |

## Validation

| Check | Value |
|---|---:|
| Sample records | {format_number(validation.get('sample_records'))} |
| Boot records | {format_number(validation.get('boot_records'))} |
| Probe records | {format_number(validation.get('probe_records'))} |
| Brownout events | {format_number(validation.get('brownout_events'))} |
| Independent reference observations | {format_number(validation.get('reference_observations'))} |

### Errors

{error_lines}

### Warnings

{warning_lines}

## Phase coverage

| Phase | Observed duration (s) |
|---|---:|
{chr(10).join(phase_rows)}

## Aggregate sensor results

| Sensor | Valid | Valid % | Mean °C | SD °C | Mean RH % | SD RH | Median read µs |
|---|---:|---:|---:|---:|---:|---:|---:|
{chr(10).join(sensor_rows)}

## Evidence boundary

No serial log, individual sample, marker stream, reference-observation stream, per-sample CSV, workstation path or embedded interactive telemetry is included. Pairwise aggregates, per-phase aggregates, response estimates and optional aggregate reference metrics remain available in the companion JSON summary.

A `PASSED` summary establishes only that the committed protocol and strict final gate were met by the owned specimens in the executed setup. It does not establish universal sensor-family behavior, final enclosure fitness, calibrated accuracy without an independent reference, or power-system characterization.
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    stability = subparsers.add_parser("stability", help="publish a sanitized stability summary")
    stability.add_argument("--run-dir", required=True)
    stability.add_argument("--output-dir", default="../../../docs/evidence/IHAP-45/summaries")

    environmental = subparsers.add_parser("environmental", help="publish a sanitized environmental summary")
    environmental.add_argument("--run-dir", required=True)
    environmental.add_argument("--plan", default="config/test-plan.json")
    environmental.add_argument("--output-dir", default="../../../docs/evidence/IHAP-45/summaries")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    run_dir = Path(args.run_dir)
    output_dir = Path(args.output_dir)
    try:
        if args.command == "stability":
            summary = sanitize_stability(run_dir)
            stem = f"stability-{safe_filename(str(summary['run_id']))}"
            markdown = stability_markdown(summary)
        else:
            summary = sanitize_environmental(run_dir, Path(args.plan))
            stem = f"environmental-{safe_filename(str(summary['run_id']))}"
            markdown = environmental_markdown(summary)
        json_path, markdown_path = write_outputs(output_dir, stem, summary, markdown)
    except (PublicationError, ihap45.HarnessError, OSError, ValueError, TypeError) as exc:
        print(f"IHAP-45 PUBLICATION ERROR: {exc}", file=sys.stderr)
        return 2

    print(f"Sanitized JSON: {json_path}")
    print(f"Sanitized Markdown: {markdown_path}")
    print("Review both files and git diff before staging. Raw run files were not copied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
