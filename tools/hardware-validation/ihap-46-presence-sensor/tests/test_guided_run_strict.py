from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
HOST = ROOT / "host"
if str(HOST) not in sys.path:
    sys.path.insert(0, str(HOST))

import ihap46  # type: ignore

SPEC = importlib.util.spec_from_file_location(
    "guided_run_strict", HOST / "guided_run_strict.py"
)
assert SPEC and SPEC.loader
strict = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(strict)


class StrictGuidedRunTests(unittest.TestCase):
    def append_sample(
        self,
        run_dir: Path,
        received_ms: int,
        presence: bool,
    ) -> None:
        ihap46.append_jsonl(
            run_dir / "records.jsonl",
            {
                "received_at_epoch_ms": received_ms,
                "source": {
                    "record_type": "sample",
                    "ld2410c": {"uart_presence": presence},
                },
            },
        )

    def test_clear_start_snapshot_requires_stable_clear_window(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            run_dir = Path(directory)
            self.append_sample(run_dir, 1_000, False)
            self.append_sample(run_dir, 2_000, False)
            self.append_sample(run_dir, 4_100, False)
            snapshot = strict.clear_start_snapshot(
                run_dir,
                ["ld2410c_uart"],
                1_000,
                3_000,
                now_ms=4_100,
            )

        self.assertEqual("PASS", snapshot["status"])
        self.assertEqual(3_100, snapshot["stable_clear_ms"])
        self.assertEqual({"ld2410c_uart": False}, snapshot["latest_states"])

    def test_clear_start_snapshot_restarts_after_presence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            run_dir = Path(directory)
            self.append_sample(run_dir, 1_000, False)
            self.append_sample(run_dir, 2_000, True)
            self.append_sample(run_dir, 3_000, False)
            self.append_sample(run_dir, 4_000, False)
            snapshot = strict.clear_start_snapshot(
                run_dir,
                ["ld2410c_uart"],
                1_000,
                3_000,
                now_ms=4_000,
            )

        self.assertEqual("WAIT", snapshot["status"])
        self.assertEqual(1_000, snapshot["stable_clear_ms"])

    def test_onset_integrity_rejects_preexisting_presence(self) -> None:
        plan = {
            "schema_version": "1.0.0",
            "issue": "IHAP-46",
            "scenarios": [
                {
                    "id": "ENTER_ROOM",
                    "title": "Enter",
                    "duration_s": 30,
                    "repetitions": 1,
                    "ground_truth": "present_moving",
                    "door_state": "open",
                    "expected": {
                        "ld2410c_uart": {
                            "min_presence_ratio": 0.8,
                            "max_onset_ms": 2_000,
                        }
                    },
                }
            ],
        }
        results = {
            "warnings": [],
            "summary": {},
            "intervals": [
                {
                    "scenario_id": "ENTER_ROOM",
                    "repetition": 1,
                    "start_epoch_ms": 10_000,
                    "sensors": {
                        "ld2410c_uart": {
                            "sample_count": 300,
                            "presence_count": 300,
                            "presence_ratio": 1.0,
                            "first_true_latency_ms": 31,
                            "status": "PASS",
                            "failures": [],
                        }
                    },
                    "status": "PASS",
                }
            ],
        }
        records = [
            {
                "received_at_epoch_ms": 9_950,
                "source": {
                    "record_type": "sample",
                    "ld2410c": {"uart_presence": True},
                },
            }
        ]

        updated = strict.apply_onset_integrity(results, records, plan)
        metrics = updated["intervals"][0]["sensors"]["ld2410c_uart"]

        self.assertEqual("FAIL", metrics["status"])
        self.assertIsNone(metrics["first_true_latency_ms"])
        self.assertEqual(31, metrics["raw_first_true_latency_ms"])
        self.assertEqual("FAIL", updated["summary"]["status"])
        self.assertEqual(1, updated["summary"]["failed"])

    def test_onset_integrity_accepts_fresh_clear_precondition(self) -> None:
        plan = {
            "schema_version": "1.0.0",
            "issue": "IHAP-46",
            "scenarios": [
                {
                    "id": "ENTER_ROOM",
                    "title": "Enter",
                    "duration_s": 30,
                    "repetitions": 1,
                    "ground_truth": "present_moving",
                    "door_state": "open",
                    "expected": {
                        "ld2410c_uart": {
                            "min_presence_ratio": 0.8,
                            "max_onset_ms": 2_000,
                        }
                    },
                }
            ],
        }
        results = {
            "warnings": [],
            "summary": {},
            "intervals": [
                {
                    "scenario_id": "ENTER_ROOM",
                    "repetition": 1,
                    "start_epoch_ms": 10_000,
                    "sensors": {
                        "ld2410c_uart": {
                            "sample_count": 300,
                            "presence_count": 290,
                            "presence_ratio": 0.966,
                            "first_true_latency_ms": 650,
                            "status": "PASS",
                            "failures": [],
                        }
                    },
                    "status": "PASS",
                }
            ],
        }
        records = [
            {
                "received_at_epoch_ms": 9_950,
                "source": {
                    "record_type": "sample",
                    "ld2410c": {"uart_presence": False},
                },
            }
        ]

        updated = strict.apply_onset_integrity(results, records, plan)
        metrics = updated["intervals"][0]["sensors"]["ld2410c_uart"]

        self.assertEqual("PASS", metrics["status"])
        self.assertEqual(False, metrics["pre_start_presence"])
        self.assertEqual(650, metrics["first_true_latency_ms"])
        self.assertEqual("PASS", updated["summary"]["status"])


if __name__ == "__main__":
    unittest.main()
