from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
import sys
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "ihap45.py"
SPEC = importlib.util.spec_from_file_location("ihap45", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
ihap45 = importlib.util.module_from_spec(SPEC)
sys.modules["ihap45"] = ihap45
SPEC.loader.exec_module(ihap45)


class ParserTests(unittest.TestCase):
    def test_parse_firmware_json_ignores_logs(self) -> None:
        self.assertIsNone(ihap45.parse_firmware_json("I (123) boot: message"))

    def test_parse_firmware_json_accepts_object(self) -> None:
        record = ihap45.parse_firmware_json('{"record_type":"sample"}')
        self.assertEqual(record, {"record_type": "sample"})

    def test_sample_validation_accepts_valid_sample_without_pressure(self) -> None:
        record = {
            "record_type": "sample",
            "schema_version": "1.0.0",
            "batch_id": 1,
            "uptime_ms": 5000,
            "sensor_id": "DHT11-OWNED-01",
            "sensor_type": "DHT11",
            "valid": True,
            "error_code": None,
            "temperature_c": 23.0,
            "humidity_percent": 50.0,
            "read_duration_us": 4100,
        }
        self.assertEqual(ihap45.validate_sample_record(record), [])

    def test_sample_validation_rejects_pressure_field(self) -> None:
        record = {
            "record_type": "sample",
            "schema_version": "1.0.0",
            "batch_id": 1,
            "uptime_ms": 5000,
            "sensor_id": "BME280-OWNED-01",
            "sensor_type": "BME280",
            "valid": True,
            "error_code": None,
            "temperature_c": 23.0,
            "humidity_percent": 50.0,
            "read_duration_us": 9000,
            "pressure_hpa": 1013.2,
        }
        errors = ihap45.validate_sample_record(record)
        self.assertTrue(any("forbidden pressure fields" in error for error in errors))


class RunValidationTests(unittest.TestCase):
    def _write_jsonl(self, path: Path, records: list[dict]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as stream:
            for record in records:
                stream.write(json.dumps(record) + "\n")

    def test_minimal_complete_run_passes_with_warning_without_reference(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            run_dir = root / "run"
            paths = ihap45.run_paths(run_dir)
            (run_dir / "raw").mkdir(parents=True)
            plan = {
                "required_sensor_ids": ["DHT11-OWNED-01", "DHT22-OWNED-01", "BME280-OWNED-01"],
                "forbidden_fields": ["pressure"],
                "phases": [{"name": "baseline", "minimum_seconds": 0, "kind": "plateau"}],
                "validation": {
                    "minimum_valid_samples_per_sensor": 1,
                    "minimum_completeness_percent": 100.0,
                    "require_bme280_chip_id": "0x60",
                },
            }
            plan_path = root / "plan.json"
            plan_path.write_text(json.dumps(plan), encoding="utf-8")
            paths["metadata"].write_text(json.dumps({"run_id": "TEST"}), encoding="utf-8")
            paths["markers"].parent.mkdir(parents=True, exist_ok=True)
            self._write_jsonl(
                paths["markers"],
                [
                    {
                        "record_type": "phase_marker",
                        "schema_version": "1.0.0",
                        "run_id": "TEST",
                        "host_timestamp_utc": "2026-07-15T10:00:00.000Z",
                        "phase": "baseline",
                        "note": None,
                    }
                ],
            )
            paths["reference"].touch()
            records = [
                {
                    "record_type": "harness_boot",
                    "schema_version": "1.0.0",
                    "measurement_channels": ["temperature_c", "humidity_percent"],
                    "host_timestamp_utc": "2026-07-15T10:00:00.000Z",
                    "phase": "baseline",
                },
                {
                    "record_type": "sensor_probe",
                    "schema_version": "1.0.0",
                    "sensor_id": "BME280-OWNED-01",
                    "chip_id": "0x60",
                    "detected_type": "BME280",
                    "humidity_supported": True,
                    "status": "OK",
                    "host_timestamp_utc": "2026-07-15T10:00:00.100Z",
                    "phase": "baseline",
                },
            ]
            for sensor_id, sensor_type in (
                ("DHT11-OWNED-01", "DHT11"),
                ("DHT22-OWNED-01", "DHT22"),
                ("BME280-OWNED-01", "BME280"),
            ):
                records.append(
                    {
                        "record_type": "sample",
                        "schema_version": "1.0.0",
                        "batch_id": 1,
                        "uptime_ms": 5000,
                        "sensor_id": sensor_id,
                        "sensor_type": sensor_type,
                        "valid": True,
                        "error_code": None,
                        "temperature_c": 23.0,
                        "humidity_percent": 50.0,
                        "read_duration_us": 5000,
                        "host_timestamp_utc": "2026-07-15T10:00:01.000Z",
                        "phase": "baseline",
                    }
                )
            self._write_jsonl(paths["samples"], records)
            result = ihap45.validate_run(run_dir, plan_path)
            self.assertTrue(result.ok, result.errors)
            self.assertTrue(any("no independent reference" in warning for warning in result.warnings))

    def test_bmp280_probe_is_blocking(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            run_dir = root / "run"
            paths = ihap45.run_paths(run_dir)
            (run_dir / "raw").mkdir(parents=True)
            plan = {
                "required_sensor_ids": [],
                "forbidden_fields": ["pressure"],
                "phases": [],
                "validation": {
                    "minimum_valid_samples_per_sensor": 0,
                    "minimum_completeness_percent": 0.0,
                    "require_bme280_chip_id": "0x60",
                },
            }
            plan_path = root / "plan.json"
            plan_path.write_text(json.dumps(plan), encoding="utf-8")
            paths["metadata"].write_text(json.dumps({"run_id": "TEST"}), encoding="utf-8")
            paths["markers"].parent.mkdir(parents=True, exist_ok=True)
            paths["markers"].touch()
            paths["reference"].touch()
            self._write_jsonl(
                paths["samples"],
                [
                    {
                        "record_type": "harness_boot",
                        "schema_version": "1.0.0",
                        "measurement_channels": ["temperature_c", "humidity_percent"],
                        "host_timestamp_utc": "2026-07-15T10:00:00.000Z",
                        "phase": "unclassified",
                    },
                    {
                        "record_type": "sensor_probe",
                        "schema_version": "1.0.0",
                        "sensor_id": "BME280-OWNED-01",
                        "chip_id": "0x58",
                        "detected_type": "BMP280",
                        "humidity_supported": False,
                        "status": "REJECTED_NOT_BME280",
                        "host_timestamp_utc": "2026-07-15T10:00:00.100Z",
                        "phase": "unclassified",
                    },
                ],
            )
            result = ihap45.validate_run(run_dir, plan_path)
            self.assertFalse(result.ok)
            self.assertTrue(any("missing successful BME280 probe" in error for error in result.errors))


class MetricsTests(unittest.TestCase):
    def test_summary_numeric_and_percentile(self) -> None:
        summary = ihap45.summarize_numeric([1.0, 2.0, 3.0])
        self.assertEqual(summary["median"], 2.0)
        self.assertEqual(summary["min"], 1.0)
        self.assertEqual(ihap45.percentile([1.0, 2.0, 3.0, 4.0], 0.5), 2.5)


if __name__ == "__main__":
    unittest.main()
