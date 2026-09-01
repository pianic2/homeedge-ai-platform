#!/usr/bin/env python3
"""Strict acceptance gate for the complete IHAP-45 environmental run."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

import ihap45


@dataclass(frozen=True)
class FinalGateResult:
    passed: bool
    errors: list[str]
    warnings: list[str]
    summary: dict[str, Any]


def evaluate_final_gate(run_dir: Path, plan_path: Path) -> FinalGateResult:
    validation = ihap45.validate_run(run_dir, plan_path)
    paths = ihap45.run_paths(run_dir)
    records = ihap45.read_jsonl(paths["samples"])
    errors = list(validation.errors)
    warnings = list(validation.warnings)

    boot_records = [record for record in records if record.get("record_type") == "harness_boot"]
    probes = [record for record in records if record.get("record_type") == "sensor_probe"]
    successful_probes = [
        record
        for record in probes
        if record.get("sensor_id") == "BME280-OWNED-01"
        and record.get("chip_id") == "0x60"
        and record.get("detected_type") == "BME280"
        and record.get("humidity_supported") is True
        and record.get("status") == "OK"
    ]

    if len(boot_records) != 1:
        errors.append(f"strict gate requires exactly one harness_boot; observed {len(boot_records)}")
    if not successful_probes:
        errors.append("strict gate requires a successful BME280 probe with chip ID 0x60")

    serial_text = paths["serial"].read_text(encoding="utf-8", errors="replace") if paths["serial"].exists() else ""
    brownout_events = serial_text.count("Brownout detector was triggered")
    if brownout_events:
        errors.append(f"brownout detector triggered {brownout_events} time(s)")

    metadata = ihap45.load_json(paths["metadata"])
    summary = {
        "run_id": metadata.get("run_id", run_dir.name),
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "boot_records": len(boot_records),
        "probe_records": len(probes),
        "successful_bme280_probes": len(successful_probes),
        "brownout_events": brownout_events,
        "sample_records": validation.summary.get("sample_records"),
        "phase_durations_seconds": validation.summary.get("phase_durations_seconds"),
        "per_sensor": validation.summary.get("per_sensor"),
        "reference_observations": validation.summary.get("reference_observations"),
        "measurement_channels": ["temperature_c", "humidity_percent"],
        "raw_data_policy": "local_only",
    }
    return FinalGateResult(passed=not errors, errors=errors, warnings=warnings, summary=summary)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--plan", default="config/test-plan.json")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    run_dir = Path(args.run_dir)
    try:
        result = evaluate_final_gate(run_dir, Path(args.plan))
    except (ihap45.HarnessError, OSError, ValueError) as exc:
        print(f"IHAP-45 FINAL GATE ERROR: {exc}", file=sys.stderr)
        return 2

    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    (results_dir / "final-gate-summary.json").write_text(
        json.dumps(result.summary, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )

    for warning in result.warnings:
        print(f"WARNING: {warning}", file=sys.stderr)
    if not result.passed:
        for error in result.errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Strict gate failed. Local summary: {results_dir / 'final-gate-summary.json'}", file=sys.stderr)
        return 2

    print("IHAP-45 strict full-run gate passed.")
    print(f"Local aggregate gate summary: {results_dir / 'final-gate-summary.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
