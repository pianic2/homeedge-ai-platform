from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

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

    def test_occupied_start_snapshot_passes_with_stable_presence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            run_dir = Path(directory)
            self.append_sample(run_dir, 1_000, True)
            self.append_sample(run_dir, 2_000, True)
            self.append_sample(run_dir, 4_100, True)
            snapshot = strict.occupied_start_snapshot(
                run_dir,
                ["ld2410c_uart"],
                1_000,
                3_000,
                now_ms=4_100,
            )

        self.assertEqual("PASS", snapshot["status"])
        self.assertEqual(3_100, snapshot["stable_occupied_ms"])
        self.assertEqual({"ld2410c_uart": True}, snapshot["latest_states"])

    def test_occupied_start_snapshot_waits_without_sample_or_when_clear(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            run_dir = Path(directory)
            no_sample = strict.occupied_start_snapshot(
                run_dir, ["ld2410c_uart"], 1_000, 1_000, now_ms=2_000
            )
            self.append_sample(run_dir, 2_000, False)
            clear = strict.occupied_start_snapshot(
                run_dir, ["ld2410c_uart"], 1_000, 1_000, now_ms=2_000
            )

        self.assertEqual("WAIT", no_sample["status"])
        self.assertEqual(0, no_sample["sample_count"])
        self.assertEqual("WAIT", clear["status"])
        self.assertEqual({"ld2410c_uart": False}, clear["latest_states"])

    def test_occupied_start_snapshot_rejects_stale_sample(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            run_dir = Path(directory)
            self.append_sample(run_dir, 1_000, True)
            snapshot = strict.occupied_start_snapshot(
                run_dir,
                ["ld2410c_uart"],
                1_000,
                0,
                now_ms=2_001,
            )

        self.assertEqual("WAIT", snapshot["status"])
        self.assertEqual(1_001, snapshot["latest_sample_age_ms"])

    def test_occupied_countdown_requires_presence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            run_dir = Path(directory)
            current_ms = 10_000
            self.append_sample(run_dir, current_ms, True)
            with mock.patch.object(strict.ihap46, "epoch_ms", return_value=current_ms):
                self.assertTrue(
                    strict.countdown_finished_occupied(run_dir, ["ld2410c_uart"])
                )
            self.append_sample(run_dir, current_ms + 100, False)
            with mock.patch.object(strict.ihap46, "epoch_ms", return_value=current_ms + 100):
                self.assertFalse(
                    strict.countdown_finished_occupied(run_dir, ["ld2410c_uart"])
                )

    def test_occupied_gate_timeout_preserves_failure_event(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            run_dir = Path(directory)
            scenario = {"id": "EXIT_CLEAR"}
            with self.assertRaises(ihap46.HarnessError):
                strict.wait_for_occupied_start(
                    run_dir,
                    scenario,
                    1,
                    ["ld2410c_uart"],
                    timeout_seconds=0,
                )
            events = list(ihap46.iter_jsonl(run_dir / "capture-events.jsonl"))

        self.assertEqual(
            ["offset_occupied_gate_started", "offset_occupied_gate_failed"],
            [event["event"] for event in events],
        )
        self.assertEqual(["ld2410c_uart"], events[-1]["sensor_channels"])

    def test_selected_transition_channels_are_limited_to_run_selection(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            run_dir = Path(directory)
            ihap46.write_json(
                run_dir / "run.json",
                {"selected_sensor_channels": ["ld2410c_uart"]},
            )
            scenario = {
                "id": "EXIT_CLEAR",
                "expected_transition": "occupied_to_empty",
                "expected": {
                    "ld2410c_uart": {},
                    "ld2410c_out": {},
                    "pir_out": {},
                },
            }
            channels = strict.selected_transition_sensor_ids(
                run_dir, scenario, "occupied_to_empty"
            )

        self.assertEqual(("ld2410c_uart",), channels)

    def test_selected_start_state_channels_are_limited_to_run_selection(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            run_dir = Path(directory)
            ihap46.write_json(
                run_dir / "run.json",
                {"selected_sensor_channels": ["ld2410c_uart"]},
            )
            scenario = {
                "id": "SEATED_STILL",
                "required_start_state": "occupied",
                "expected": {
                    "ld2410c_uart": {},
                    "ld2410c_out": {},
                    "pir_out": {},
                },
            }
            channels = strict.selected_start_state_sensor_ids(
                run_dir, scenario, "occupied"
            )

        self.assertEqual(("ld2410c_uart",), channels)

    def test_clear_gate_lifecycle_events_use_selected_channels(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            run_dir = Path(directory)
            ihap46.write_json(
                run_dir / "run.json",
                {"selected_sensor_channels": ["ld2410c_uart"]},
            )
            self.append_sample(run_dir, 5_000, False)
            self.append_sample(run_dir, 6_000, False)
            self.append_sample(run_dir, 8_000, False)
            scenario = {"id": "ENTER_ROOM"}
            with mock.patch.object(
                strict.ihap46,
                "epoch_ms",
                side_effect=[5_000, 5_000, 8_000, 8_000],
            ), mock.patch.object(strict.time, "monotonic", return_value=0), mock.patch.object(
                strict.time, "sleep"
            ):
                strict.wait_for_clear_start(
                    run_dir,
                    scenario,
                    1,
                    ["ld2410c_uart"],
                    stable_seconds=3,
                    timeout_seconds=90,
                )
            events = list(ihap46.iter_jsonl(run_dir / "capture-events.jsonl"))

        self.assertEqual(
            ["ld2410c_uart"], events[0]["sensor_channels"]
        )
        self.assertEqual(
            ["ld2410c_uart"], events[1]["sensor_channels"]
        )

    def test_occupied_countdown_restart_event_is_recorded(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            run_dir = Path(directory)
            ihap46.write_json(
                run_dir / "run.json",
                {"selected_sensor_channels": ["ld2410c_uart"]},
            )
            scenario = {
                "id": "EXIT_CLEAR",
                "title": "Exit",
                "expected_transition": "occupied_to_empty",
                "expected": {"ld2410c_uart": {"max_presence_ratio": 0.4}},
                "duration_s": 0,
                "repetitions": 1,
                "ground_truth": "empty",
                "door_state": "closed",
            }
            action = {
                "purpose": "leave",
                "start_action": "LEAVE THE ROOM",
                "setup": [],
                "during_capture": ["leave"],
                "invalid_if": [],
            }
            with mock.patch("builtins.input", return_value=""), mock.patch.object(
                strict, "wait_for_occupied_start", return_value={}
            ) as gate, mock.patch.object(
                strict, "countdown_finished_occupied", side_effect=[False, True]
            ), mock.patch.object(strict.time, "sleep"), mock.patch.object(
                strict.time, "monotonic", return_value=0
            ), mock.patch.object(base := strict.base, "append_marker"):
                strict.strict_run_interval(run_dir, scenario, action, 1, 1.0)
            events = list(ihap46.iter_jsonl(run_dir / "capture-events.jsonl"))

        self.assertEqual(2, gate.call_count)
        self.assertIn(
            "offset_countdown_restarted", [event["event"] for event in events]
        )

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

    def test_clear_integrity_rejects_preexisting_clear_state(self) -> None:
        plan = {
            "schema_version": "1.0.0",
            "issue": "IHAP-46",
            "scenarios": [
                {
                    "id": "EXIT_CLEAR",
                    "title": "Exit",
                    "duration_s": 60,
                    "repetitions": 1,
                    "ground_truth": "empty",
                    "door_state": "closed",
                    "expected": {
                        "ld2410c_uart": {
                            "max_presence_ratio": 0.25,
                            "max_clear_ms": 10_000,
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
                    "scenario_id": "EXIT_CLEAR",
                    "repetition": 1,
                    "start_epoch_ms": 10_000,
                    "sensors": {
                        "ld2410c_uart": {
                            "sample_count": 600,
                            "presence_count": 0,
                            "presence_ratio": 0.0,
                            "first_true_latency_ms": None,
                            "first_false_latency_ms": 0,
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

        self.assertEqual("FAIL", metrics["status"])
        self.assertIsNone(metrics["first_false_latency_ms"])
        self.assertEqual(0, metrics["raw_first_false_latency_ms"])
        self.assertEqual("FAIL", updated["summary"]["status"])

    def test_clear_integrity_accepts_fresh_occupied_precondition(self) -> None:
        plan = {
            "schema_version": "1.0.0",
            "issue": "IHAP-46",
            "scenarios": [
                {
                    "id": "EXIT_CLEAR",
                    "title": "Exit",
                    "duration_s": 60,
                    "repetitions": 1,
                    "ground_truth": "empty",
                    "door_state": "closed",
                    "expected": {
                        "ld2410c_uart": {
                            "max_presence_ratio": 0.25,
                            "max_clear_ms": 10_000,
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
                    "scenario_id": "EXIT_CLEAR",
                    "repetition": 1,
                    "start_epoch_ms": 10_000,
                    "sensors": {
                        "ld2410c_uart": {
                            "sample_count": 600,
                            "presence_count": 20,
                            "presence_ratio": 0.033,
                            "first_true_latency_ms": 0,
                            "first_false_latency_ms": 2_000,
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

        self.assertEqual("PASS", metrics["status"])
        self.assertEqual(True, metrics["pre_start_presence"])
        self.assertEqual(2_000, metrics["first_false_latency_ms"])
        self.assertEqual("PASS", updated["summary"]["status"])


if __name__ == "__main__":
    unittest.main()
