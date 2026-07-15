from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("ihap46", ROOT / "host" / "ihap46.py")
assert SPEC and SPEC.loader
ihap46 = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = ihap46
SPEC.loader.exec_module(ihap46)


class PlanTests(unittest.TestCase):
    def setUp(self) -> None:
        self.plan = json.loads((ROOT / "config" / "test-plan.json").read_text(encoding="utf-8"))

    def test_canonical_plan_is_valid(self) -> None:
        self.assertEqual([], ihap46.validate_plan(self.plan))
        self.assertGreaterEqual(len(self.plan["scenarios"]), 10)

    def test_duplicate_scenario_is_rejected(self) -> None:
        invalid = copy.deepcopy(self.plan)
        invalid["scenarios"].append(copy.deepcopy(invalid["scenarios"][0]))
        errors = ihap46.validate_plan(invalid)
        self.assertTrue(any("duplicate scenario id" in error for error in errors))

    def test_invalid_threshold_is_rejected(self) -> None:
        invalid = copy.deepcopy(self.plan)
        invalid["scenarios"][0]["expected"]["ld2410c_uart"]["max_presence_ratio"] = 1.5
        errors = ihap46.validate_plan(invalid)
        self.assertTrue(any("between 0 and 1" in error for error in errors))


class ParsingTests(unittest.TestCase):
    def test_decode_json_record_ignores_boot_noise(self) -> None:
        self.assertIsNone(ihap46.decode_json_record("I (123) boot: message"))
        record = ihap46.decode_json_record('{"record_type":"sample","seq":1}')
        self.assertEqual("sample", record["record_type"])

    def test_nested_sensor_normalization(self) -> None:
        source = {
            "ld2410c": {"uart_presence": True, "out": 0},
            "pir": {"out": 1},
        }
        self.assertIs(ihap46.normalize_sensor_value(source, "ld2410c_uart"), True)
        self.assertIs(ihap46.normalize_sensor_value(source, "ld2410c_out"), False)
        self.assertIs(ihap46.normalize_sensor_value(source, "pir_out"), True)


class AnalysisTests(unittest.TestCase):
    def setUp(self) -> None:
        self.plan = json.loads((ROOT / "config" / "test-plan.json").read_text(encoding="utf-8"))
        self.plan["scenarios"] = [
            {
                "id": "TEST_PRESENT",
                "title": "fixture present",
                "required": True,
                "duration_s": 10,
                "repetitions": 1,
                "ground_truth": "present_moving",
                "door_state": "closed",
                "instructions": "fixture",
                "expected": {
                    "ld2410c_uart": {"min_presence_ratio": 0.8, "max_onset_ms": 2000},
                    "ld2410c_out": {"min_presence_ratio": 0.8},
                    "pir_out": {"min_presence_ratio": 0.5},
                },
            }
        ]

    def test_build_intervals_and_evaluate(self) -> None:
        markers = [
            {"scenario_id": "TEST_PRESENT", "repetition": 1, "phase": "start", "at_epoch_ms": 1000},
            {"scenario_id": "TEST_PRESENT", "repetition": 1, "phase": "end", "at_epoch_ms": 11000},
        ]
        intervals, warnings = ihap46.build_intervals(markers, self.plan)
        self.assertEqual([], warnings)
        self.assertEqual(1, len(intervals))

        records = []
        for index in range(10):
            present = index >= 1
            records.append({
                "received_at_epoch_ms": 1000 + index * 1000,
                "source": {
                    "record_type": "sample",
                    "ld2410c": {"uart_presence": present, "out": present},
                    "pir": {"out": index >= 3},
                },
            })
        result = ihap46.evaluate_interval(intervals[0], records, self.plan["scenarios"][0])
        self.assertEqual("PASS", result["status"])
        self.assertEqual(1000, result["sensors"]["ld2410c_uart"]["first_true_latency_ms"])
        self.assertAlmostEqual(0.9, result["sensors"]["ld2410c_uart"]["presence_ratio"])

    def test_missing_samples_fail(self) -> None:
        interval = ihap46.ScenarioInterval(
            scenario_id="TEST_PRESENT",
            repetition=1,
            start_ms=1000,
            end_ms=2000,
            ground_truth="present_moving",
            door_state="closed",
            note="",
        )
        result = ihap46.evaluate_interval(interval, [], self.plan["scenarios"][0])
        self.assertEqual("FAIL", result["status"])
        self.assertIn("no samples", result["sensors"]["ld2410c_uart"]["failures"])

    def test_end_without_start_is_reported(self) -> None:
        intervals, warnings = ihap46.build_intervals(
            [{"scenario_id": "TEST_PRESENT", "repetition": 1, "phase": "end", "at_epoch_ms": 2000}],
            self.plan,
        )
        self.assertEqual([], intervals)
        self.assertTrue(any("without start" in warning for warning in warnings))

    def test_report_is_self_contained(self) -> None:
        results = {
            "run_id": "TEST-RUN",
            "generated_at": "2026-07-15T00:00:00Z",
            "record_count": 10,
            "warnings": [],
            "summary": {"status": "PASS", "intervals": 1, "passed": 1, "failed": 0},
            "intervals": [
                {
                    "scenario_id": "TEST_PRESENT",
                    "repetition": 1,
                    "ground_truth": "present_moving",
                    "sensors": {
                        "ld2410c_uart": {
                            "sample_count": 10,
                            "presence_ratio": 1.0,
                            "first_true_latency_ms": 0,
                            "status": "PASS",
                            "failures": [],
                        }
                    },
                }
            ],
        }
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "report.html"
            ihap46.render_report(results, output)
            text = output.read_text(encoding="utf-8")
            self.assertIn("IHAP-46 Presence Sensor Evidence", text)
            self.assertIn("TEST_PRESENT", text)
            self.assertNotIn("https://", text)


if __name__ == "__main__":
    unittest.main()
