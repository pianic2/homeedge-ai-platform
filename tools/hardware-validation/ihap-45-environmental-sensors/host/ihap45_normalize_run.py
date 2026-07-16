#!/usr/bin/env python3
"""Create a derived IHAP-45 run containing only evidence from the first captured harness boot onward."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Sequence

import ihap45


class NormalizationError(RuntimeError):
    """Raised when a source run cannot be normalized without ambiguity."""


def write_jsonl(path: Path, records: Sequence[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        for record in records:
            json.dump(record, stream, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
            stream.write("\n")


def records_at_or_after_timestamp(records: Sequence[dict[str, Any]], timestamp: str) -> list[dict[str, Any]]:
    return [
        record
        for record in records
        if not record.get("host_timestamp_utc") or str(record.get("host_timestamp_utc")) >= timestamp
    ]


def normalize_run(source_dir: Path, output_dir: Path) -> dict[str, Any]:
    if source_dir.resolve() == output_dir.resolve():
        raise NormalizationError("source and output run directories must be different")
    if output_dir.exists() and any(output_dir.iterdir()):
        raise NormalizationError(f"output directory already exists and is not empty: {output_dir}")

    source_paths = ihap45.run_paths(source_dir)
    records = ihap45.read_jsonl(source_paths["samples"])
    boot_indices = [index for index, record in enumerate(records) if record.get("record_type") == "harness_boot"]
    if not boot_indices:
        raise NormalizationError("source run contains no harness_boot record")
    if len(boot_indices) != 1:
        raise NormalizationError(
            f"source run contains {len(boot_indices)} harness_boot records; normalization cannot hide a reboot"
        )

    first_boot_index = boot_indices[0]
    dropped_records = records[:first_boot_index]
    retained_records = records[first_boot_index:]
    first_boot = retained_records[0]
    first_boot_timestamp = str(first_boot.get("host_timestamp_utc") or "")
    if not first_boot_timestamp:
        raise NormalizationError("captured harness_boot has no host_timestamp_utc")
    if any(record.get("record_type") == "harness_boot" for record in retained_records[1:]):
        raise NormalizationError("unexpected reboot appears after the normalization boundary")

    output_paths = ihap45.run_paths(output_dir)
    (output_dir / "raw").mkdir(parents=True, exist_ok=True)
    output_paths["results"].mkdir(parents=True, exist_ok=True)
    write_jsonl(output_paths["samples"], retained_records)

    serial_lines = source_paths["serial"].read_text(encoding="utf-8", errors="replace").splitlines()
    serial_boot_indices = [
        index for index, line in enumerate(serial_lines) if '"record_type":"harness_boot"' in line
    ]
    if len(serial_boot_indices) != 1:
        raise NormalizationError(
            f"serial log contains {len(serial_boot_indices)} harness_boot lines; expected exactly one"
        )
    retained_serial_lines = serial_lines[serial_boot_indices[0] :]
    output_paths["serial"].write_text("\n".join(retained_serial_lines) + "\n", encoding="utf-8")

    markers = ihap45.read_jsonl(source_paths["markers"]) if source_paths["markers"].exists() else []
    references = ihap45.read_jsonl(source_paths["reference"]) if source_paths["reference"].exists() else []
    retained_markers = records_at_or_after_timestamp(markers, first_boot_timestamp)
    retained_references = records_at_or_after_timestamp(references, first_boot_timestamp)
    write_jsonl(output_paths["markers"], retained_markers)
    write_jsonl(output_paths["reference"], retained_references)

    if source_paths["phase"].exists():
        shutil.copy2(source_paths["phase"], output_paths["phase"])
    else:
        output_paths["phase"].write_text("final_recovery\n", encoding="utf-8")

    metadata = ihap45.load_json(source_paths["metadata"])
    normalized_metadata = {
        **metadata,
        "normalization": {
            "method": "retain records from first captured harness_boot onward",
            "source_run_directory_name": source_dir.name,
            "derived_run_directory_name": output_dir.name,
            "first_retained_boot_timestamp_utc": first_boot_timestamp,
            "dropped_structured_records": len(dropped_records),
            "dropped_record_types": dict(Counter(str(record.get("record_type")) for record in dropped_records)),
            "dropped_serial_lines": serial_boot_indices[0],
            "dropped_markers": len(markers) - len(retained_markers),
            "dropped_reference_observations": len(references) - len(retained_references),
            "source_run_preserved": True,
        },
        "status": "normalized",
    }
    ihap45.atomic_write_text(
        output_paths["metadata"],
        json.dumps(normalized_metadata, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
    )

    sample_records = [record for record in retained_records if record.get("record_type") == "sample"]
    sensor_batch_keys = [
        (str(record.get("sensor_id")), int(record.get("batch_id", -1))) for record in sample_records
    ]
    duplicate_sensor_batches = len(sensor_batch_keys) - len(set(sensor_batch_keys))
    if duplicate_sensor_batches:
        raise NormalizationError(
            f"normalized run still contains {duplicate_sensor_batches} duplicate sensor/batch records"
        )

    summary = {
        "source_run_directory_name": source_dir.name,
        "derived_run_directory_name": output_dir.name,
        "run_id": metadata.get("run_id", source_dir.name),
        "first_retained_boot_timestamp_utc": first_boot_timestamp,
        "dropped_structured_records": len(dropped_records),
        "dropped_record_types": dict(Counter(str(record.get("record_type")) for record in dropped_records)),
        "dropped_serial_lines": serial_boot_indices[0],
        "retained_structured_records": len(retained_records),
        "retained_sample_records": len(sample_records),
        "retained_markers": len(retained_markers),
        "retained_reference_observations": len(retained_references),
        "boot_records": sum(record.get("record_type") == "harness_boot" for record in retained_records),
        "duplicate_sensor_batch_records": duplicate_sensor_batches,
        "source_run_preserved": True,
    }
    (output_dir / "normalization-summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    return summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-run-dir", required=True)
    parser.add_argument("--output-run-dir", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        summary = normalize_run(Path(args.source_run_dir), Path(args.output_run_dir))
    except (NormalizationError, ihap45.HarnessError, OSError, ValueError, TypeError) as exc:
        print(f"IHAP-45 NORMALIZATION ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    print("Source run preserved. Run validation and analysis against the derived directory.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
