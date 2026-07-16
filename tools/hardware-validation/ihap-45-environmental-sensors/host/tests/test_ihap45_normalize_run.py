from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

HOST_DIR = Path(__file__).resolve().parents[1]
for module_name in ("ihap45", "ihap45_normalize_run"):
    module_path = HOST_DIR / f"{module_name}.py"
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

ihap45 = sys.modules["ihap45"]
normalizer = sys.modules["ihap45_normalize_run"]


class NormalizeRunTests(unittest.TestCase):
    def write_jsonl(self, path: Path, records: list[dict]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as stream:
            for record in records:
                stream.write(json.dumps(record) + "\n")

    def sample(self, sensor_id: str, batch_id: int, timestamp: str) -> dict:
        return {
            "record_type": "sample",
            "schema_version": "1.0.0",
            "batch_id": batch_id,
            "uptime_ms": batch_id * 5000,
            "sensor_id": sensor_id,
            "sensor_type": "DHT11",
            "valid": True,
            "error_code": None,
            "temperature_c": 23.0,
            "humidity_percent": 50.0,
            "read_duration_us": 1000,
            "run_id": "IHAP45-RUN-01",
            "host_timestamp_utc": timestamp,
            "phase": "warmup",
        }

    def test_normalization_drops_preboot_samples_and_preserves_source(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            output = root / "normalized"
            paths = ihap45.run_paths(source)
            (source / "raw").mkdir(parents=True)
            paths["phase"].write_text("final_recovery\n", encoding="utf-8")
            paths["metadata"].write_text(json.dumps({"run_id": "IHAP45-RUN-01"}), encoding="utf-8")
            self.write_jsonl(
                paths["samples"],
                [
                    self.sample("DHT11-OWNED-01", 29, "2026-07-15T16:00:00.000Z"),
                    {
                        "record_type": "harness_boot",
                        "schema_version": "1.0.0",
                        "host_timestamp_utc": "2026-07-15T16:00:05.000Z",
                    },
                    self.sample("DHT11-OWNED-01", 1, "2026-07-15T16:00:10.000Z"),
                ],
            )
            paths["serial"].write_text(
                '2026 old {"record_type":"sample"}\n'
                '2026 boot {"record_type":"harness_boot"}\n'
                '2026 new {"record_type":"sample"}\n',
                encoding="utf-8",
            )
            self.write_jsonl(
                paths["markers"],
                [
                    {"host_timestamp_utc": "2026-07-15T16:00:00.000Z", "phase": "unclassified"},
                    {"host_timestamp_utc": "2026-07-15T16:00:10.000Z", "phase": "warmup"},
                ],
            )
            self.write_jsonl(paths["reference"], [])

            result = normalizer.normalize_run(source, output)

            self.assertEqual(result["dropped_structured_records"], 1)
            self.assertEqual(result["boot_records"], 1)
            retained = ihap45.read_jsonl(ihap45.run_paths(output)["samples"])
            self.assertEqual(retained[0]["record_type"], "harness_boot")
            self.assertEqual(len(retained), 2)
            original = ihap45.read_jsonl(paths["samples"])
            self.assertEqual(len(original), 3)
            self.assertTrue((output / "normalization-summary.json").exists())

    def test_normalization_rejects_multiple_boots(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            output = root / "normalized"
            paths = ihap45.run_paths(source)
            (source / "raw").mkdir(parents=True)
            paths["metadata"].write_text(json.dumps({"run_id": "run"}), encoding="utf-8")
            paths["phase"].write_text("warmup\n", encoding="utf-8")
            self.write_jsonl(
                paths["samples"],
                [
                    {"record_type": "harness_boot", "host_timestamp_utc": "2026-01-01T00:00:00Z"},
                    {"record_type": "harness_boot", "host_timestamp_utc": "2026-01-01T00:01:00Z"},
                ],
            )
            paths["serial"].write_text(
                '{"record_type":"harness_boot"}\n{"record_type":"harness_boot"}\n', encoding="utf-8"
            )
            self.write_jsonl(paths["markers"], [])
            self.write_jsonl(paths["reference"], [])
            with self.assertRaises(normalizer.NormalizationError):
                normalizer.normalize_run(source, output)


if __name__ == "__main__":
    unittest.main()
