from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "ihap45_publish_html.py"
SPEC = importlib.util.spec_from_file_location("ihap45_publish_html", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
module = importlib.util.module_from_spec(SPEC)
sys.modules["ihap45_publish_html"] = module
SPEC.loader.exec_module(module)


class AggregateHtmlPublicationTests(unittest.TestCase):
    def minimal_summary(self) -> dict:
        sensor = {
            "records": 10,
            "valid_records": 10,
            "valid_percent": 100.0,
            "error_counts": {},
            "temperature_c": {"mean": 23.0, "stddev": 0.1},
            "humidity_percent": {"mean": 50.0, "stddev": 0.2},
            "read_duration_us": {"median": 1000.0},
            "per_phase": {
                phase: {
                    "temperature_c": {"mean": 23.0},
                    "humidity_percent": {"mean": 50.0},
                }
                for phase in module.PHASE_ORDER
            },
        }
        return {
            "publication_schema_version": "1.0.0",
            "evidence_type": "environmental_comparison_summary",
            "run_id": "IHAP45-RUN-TEST",
            "plan_id": "IHAP45-QUALIFICATION-01",
            "status": "passed",
            "comparison_scope": "relative_only",
            "qualified_bme280": {"chip_id": "0x60", "i2c_address": "0x76"},
            "validation": {
                "sample_records": 30,
                "boot_records": 1,
                "errors": [],
                "warnings": [],
                "phase_durations_seconds": {"baseline": 600.0},
            },
            "results": {
                "per_sensor": {sensor_id: sensor for sensor_id in module.SENSOR_ORDER},
                "pairwise": {},
            },
            "limitations": ["Relative comparison only."],
        }

    def test_load_summary_rejects_raw_timestamp_key(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "summary.json"
            summary = self.minimal_summary()
            summary["host_timestamp_utc"] = "2026-07-15T00:00:00Z"
            path.write_text(json.dumps(summary), encoding="utf-8")
            with self.assertRaises(module.HtmlPublicationError):
                module.load_summary(path)

    def test_render_contains_aggregate_boundary_without_sample_payloads(self) -> None:
        rendered = module.render(self.minimal_summary())
        self.assertIn("aggregate statistics only", rendered)
        self.assertIn("IHAP45-RUN-TEST", rendered)
        self.assertNotIn("host_timestamp_utc", rendered)
        self.assertNotIn("batch_id", rendered)

    def test_main_writes_summary_html(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "environmental-IHAP45-RUN-TEST.summary.json"
            source.write_text(json.dumps(self.minimal_summary()), encoding="utf-8")
            result = module.main(["--summary", str(source)])
            output = source.with_suffix(".html")
            self.assertEqual(result, 0)
            self.assertTrue(output.exists())
            self.assertIn("Aggregate evidence", output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
