from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

HOST_DIR = Path(__file__).resolve().parents[1]

IHAP45_SPEC = importlib.util.spec_from_file_location("ihap45", HOST_DIR / "ihap45.py")
assert IHAP45_SPEC is not None and IHAP45_SPEC.loader is not None
ihap45 = importlib.util.module_from_spec(IHAP45_SPEC)
sys.modules["ihap45"] = ihap45
IHAP45_SPEC.loader.exec_module(ihap45)

GATE_SPEC = importlib.util.spec_from_file_location("ihap45_final_gate", HOST_DIR / "ihap45_final_gate.py")
assert GATE_SPEC is not None and GATE_SPEC.loader is not None
gate = importlib.util.module_from_spec(GATE_SPEC)
sys.modules["ihap45_final_gate"] = gate
GATE_SPEC.loader.exec_module(gate)


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as stream:
        for record in records:
            stream.write(json.dumps(record) + "\n")


class FinalGateTests(unittest.TestCase):
    def create_run(self, root: Path, extra_records: list[dict] | None = None, brownout: bool = False) -> tuple[Path, Path]:
        run_dir = root / "run"
        paths = ihap45.run_paths(run_dir)
        (run_dir / "raw").mkdir(parents=True)
        paths["metadata"].write_text(json.dumps({"run_id": "RUN-01"}), encoding="utf-8")
        paths["reference"].touch()
        write_jsonl(
            paths["markers"],
            [{"record_type": "phase_marker", "phase": "baseline", "host_timestamp_utc": "2026-07-15T00:00:00Z"}],
        )
        paths["serial"].write_text("Brownout detector was triggered\n" if brownout else "", encoding="utf-8")

        boot = {
            "record_type": "harness_boot",
            "measurement_channels": ["temperature_c", "humidity_percent"],
            "host_timestamp_utc": "2026-07-15T00:00:00Z",
            "phase": "baseline",
        }
        probe = {
            "record_type": "sensor_probe",
            "sensor_id": "BME280-OWNED-01",
            "chip_id": "0x60",
            "detected_type": "BME280",
            "humidity_supported": True,
            "status": "OK",
            "host_timestamp_utc": "2026-07-15T00:00:00Z",
            "phase": "baseline",
        }
        samples = []
        for sensor_id, sensor_type in (
            ("DHT11-OWNED-01", "DHT11"),
            ("DHT22-OWNED-01", "DHT22"),
            ("BME280-OWNED-01", "BME280"),
        ):
            samples.append(
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
                    "read_duration_us": 1000,
                    "host_timestamp_utc": "2026-07-15T00:00:01Z",
                    "phase": "baseline",
                }
            )
        write_jsonl(paths["samples"], [boot, probe, *samples, *(extra_records or [])])

        plan_path = root / "plan.json"
        plan_path.write_text(
            json.dumps(
                {
                    "required_sensor_ids": ["DHT11-OWNED-01", "DHT22-OWNED-01", "BME280-OWNED-01"],
                    "forbidden_fields": ["pressure", "pressure_pa", "pressure_hpa"],
                    "phases": [{"name": "baseline", "minimum_seconds": 0, "kind": "plateau"}],
                    "validation": {
                        "minimum_valid_samples_per_sensor": 1,
                        "minimum_completeness_percent": 100.0,
                        "require_bme280_chip_id": "0x60",
                    },
                }
            ),
            encoding="utf-8",
        )
        return run_dir, plan_path

    def test_complete_single_boot_run_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            run_dir, plan_path = self.create_run(Path(temp_dir))
            result = gate.evaluate_final_gate(run_dir, plan_path)
            self.assertTrue(result.passed)
            self.assertEqual(result.summary["boot_records"], 1)
            self.assertEqual(result.summary["brownout_events"], 0)

    def test_second_boot_and_brownout_fail(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            second_boot = {
                "record_type": "harness_boot",
                "measurement_channels": ["temperature_c", "humidity_percent"],
                "host_timestamp_utc": "2026-07-15T00:00:02Z",
                "phase": "baseline",
            }
            run_dir, plan_path = self.create_run(Path(temp_dir), [second_boot], brownout=True)
            result = gate.evaluate_final_gate(run_dir, plan_path)
            self.assertFalse(result.passed)
            self.assertTrue(any("exactly one harness_boot" in error for error in result.errors))
            self.assertTrue(any("brownout detector" in error for error in result.errors))


if __name__ == "__main__":
    unittest.main()
