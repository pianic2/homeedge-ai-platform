from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
HOST = ROOT / "host"
if str(HOST) not in sys.path:
    sys.path.insert(0, str(HOST))

import ihap46  # type: ignore

SPEC = importlib.util.spec_from_file_location("guided_run", HOST / "guided_run.py")
assert SPEC and SPEC.loader
guided_run = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(guided_run)


class GuidedRunTests(unittest.TestCase):
    def setUp(self) -> None:
        self.plan = {
            "schema_version": "1.0.0",
            "issue": "IHAP-46",
            "scenarios": [
                {
                    "id": "REQUIRED",
                    "title": "Required scenario",
                    "required": True,
                    "duration_s": 65,
                    "repetitions": 2,
                    "ground_truth": "empty",
                    "door_state": "closed",
                    "expected": {
                        "ld2410c_uart": {"max_presence_ratio": 0.1},
                        "pir_out": {"max_presence_ratio": 0.1},
                    },
                },
                {
                    "id": "OPTIONAL",
                    "title": "Optional scenario",
                    "required": False,
                    "duration_s": 30,
                    "repetitions": 1,
                    "ground_truth": "adjacent_activity",
                    "door_state": "closed",
                    "expected": {
                        "ld2410c_uart": {"max_presence_ratio": 0.1}
                    },
                },
            ],
        }

    def test_default_selection_excludes_optional(self) -> None:
        selected = guided_run.select_scenarios(self.plan, [], False)
        self.assertEqual(["REQUIRED"], [item["id"] for item in selected])

    def test_explicit_selection_preserves_requested_order(self) -> None:
        selected = guided_run.select_scenarios(
            self.plan, ["OPTIONAL", "REQUIRED"], False
        )
        self.assertEqual(["OPTIONAL", "REQUIRED"], [item["id"] for item in selected])

    def test_effective_plan_contains_only_selected_sensor(self) -> None:
        selected = guided_run.select_scenarios(self.plan, ["REQUIRED"], False)
        effective = guided_run.build_effective_plan(
            self.plan, selected, ["ld2410c_uart"]
        )
        self.assertEqual(
            ["ld2410c_uart"],
            list(effective["scenarios"][0]["expected"]),
        )
        self.assertEqual(["ld2410c_uart"], effective["selected_sensor_channels"])

    def test_operator_actions_require_human_instructions(self) -> None:
        payload = {
            "schema_version": "1.0.0",
            "issue": "IHAP-46",
            "actions": {
                "REQUIRED": {
                    "purpose": "purpose",
                    "setup": ["setup"],
                    "during_capture": ["act"],
                    "invalid_if": ["invalid"],
                },
                "OPTIONAL": {
                    "purpose": "purpose",
                    "setup": ["setup"],
                    "during_capture": ["act"],
                    "invalid_if": ["invalid"],
                },
            },
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "actions.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            loaded = guided_run.load_actions(path, self.plan)
        self.assertEqual(
            "act", loaded["actions"]["REQUIRED"]["during_capture"][0]
        )

    def test_sensor_specific_scenario_is_skipped_when_channel_missing(self) -> None:
        actions = {
            "actions": {
                "REQUIRED": {},
                "OPTIONAL": {
                    "required_sensor_channels": ["ld2410c_uart", "ld2410c_out"]
                },
            }
        }
        selected = guided_run.filter_scenarios_for_sensors(
            self.plan["scenarios"], actions, ["ld2410c_uart"], []
        )
        self.assertEqual(["REQUIRED"], [item["id"] for item in selected])

    def test_scenario_card_is_actionable(self) -> None:
        action = {
            "purpose": "Verify an empty room.",
            "setup": ["Close the door."],
            "during_capture": ["Keep the room empty."],
            "invalid_if": ["A person enters."],
        }
        card = guided_run.scenario_card(self.plan["scenarios"][0], action, 1)
        self.assertIn("Durata registrata: 01:05", card)
        self.assertIn("Keep the room empty.", card)
        self.assertIn("A person enters.", card)


if __name__ == "__main__":
    unittest.main()
