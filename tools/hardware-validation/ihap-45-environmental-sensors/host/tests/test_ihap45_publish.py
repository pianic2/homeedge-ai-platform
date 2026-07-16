from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

HOST_DIR = Path(__file__).resolve().parents[1]

IHAP45_SPEC = importlib.util.spec_from_file_location("ihap45", HOST_DIR / "ihap45.py")
assert IHAP45_SPEC is not None and IHAP45_SPEC.loader is not None
ihap45 = importlib.util.module_from_spec(IHAP45_SPEC)
sys.modules["ihap45"] = ihap45
IHAP45_SPEC.loader.exec_module(ihap45)

FINAL_GATE_SPEC = importlib.util.spec_from_file_location("ihap45_final_gate", HOST_DIR / "ihap45_final_gate.py")
assert FINAL_GATE_SPEC is not None and FINAL_GATE_SPEC.loader is not None
final_gate = importlib.util.module_from_spec(FINAL_GATE_SPEC)
sys.modules["ihap45_final_gate"] = final_gate
FINAL_GATE_SPEC.loader.exec_module(final_gate)

PUBLISH_SPEC = importlib.util.spec_from_file_location("ihap45_publish", HOST_DIR / "ihap45_publish.py")
assert PUBLISH_SPEC is not None and PUBLISH_SPEC.loader is not None
publisher = importlib.util.module_from_spec(PUBLISH_SPEC)
sys.modules["ihap45_publish"] = publisher
PUBLISH_SPEC.loader.exec_module(publisher)


class PublisherTests(unittest.TestCase):
    def test_safe_filename_removes_path_and_shell_characters(self) -> None:
        self.assertEqual(publisher.safe_filename(" IHAP45/RUN 01;rm "), "IHAP45-RUN-01-rm")

    def test_forbidden_pressure_key_is_detected_recursively(self) -> None:
        findings = publisher.recursively_find_forbidden_keys({"results": {"pressure_hpa": 1013.0}})
        self.assertEqual(findings, ["$.results.pressure_hpa"])

    def test_stability_summary_is_allow_listed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            run_dir = Path(temp_dir) / "run"
            run_dir.mkdir()
            (run_dir / "stability-summary.json").write_text(
                json.dumps({
                    "run_id": "IHAP45-STABILITY-S4",
                    "configuration_label": "S4-all-three-sensors",
                    "passed": True,
                    "errors": [],
                    "warnings": [],
                    "boot_records": 1,
                    "brownout_lines": 0,
                    "disconnects_before_start": 1,
                    "disconnects_after_start": 0,
                    "valid_sample_records": 180,
                    "completed_window": True,
                    "unexpected_raw_line": "must not be copied",
                }),
                encoding="utf-8",
            )
            (run_dir / "run-metadata.json").write_text(
                json.dumps({
                    "run_id": "IHAP45-STABILITY-S4",
                    "qualification_duration_seconds": 300,
                    "serial_port_history": ["/dev/ttyACM0"],
                    "started_at_utc": "2026-07-15T00:00:00Z",
                }),
                encoding="utf-8",
            )
            summary = publisher.sanitize_stability(run_dir)
            serialized = json.dumps(summary)
            self.assertTrue(summary["passed"])
            self.assertEqual(summary["qualification_duration_seconds"], 300)
            self.assertNotIn("unexpected_raw_line", serialized)
            self.assertNotIn("serial_port_history", serialized)
            self.assertNotIn("/dev/ttyACM0", serialized)
            self.assertNotIn("started_at_utc", serialized)

    def test_environmental_publisher_applies_strict_gate(self) -> None:
        gate_result = SimpleNamespace(
            passed=False,
            errors=["brownout detector triggered 1 time(s)"],
            warnings=[],
            summary={"boot_records": 1, "probe_records": 1, "brownout_events": 1},
        )
        validation = SimpleNamespace(
            errors=[],
            warnings=[],
            summary={
                "sample_records": 3,
                "phase_durations_seconds": {},
                "per_sensor": {},
                "reference_observations": 0,
            },
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            plan = root / "plan.json"
            plan.write_text(json.dumps({"plan_id": "TEST"}), encoding="utf-8")
            with (
                patch.object(publisher.ihap45_final_gate, "evaluate_final_gate", return_value=gate_result),
                patch.object(publisher.ihap45, "validate_run", return_value=validation),
                patch.object(publisher.ihap45, "compute_analysis", return_value=({"run_id": "RUN", "per_sensor": {}}, [])),
                patch.object(publisher.ihap45, "run_paths", return_value={"samples": root / "samples.jsonl"}),
                patch.object(publisher.ihap45, "read_jsonl", return_value=[]),
            ):
                summary = publisher.sanitize_environmental(root, plan)
        self.assertEqual(summary["status"], "failed")
        self.assertFalse(summary["validation_passed"])
        self.assertEqual(summary["validation"]["brownout_events"], 1)
        self.assertIn("brownout detector triggered 1 time(s)", summary["validation"]["errors"])

    def test_output_writer_refuses_pressure_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaises(publisher.PublicationError):
                publisher.write_outputs(Path(temp_dir), "unsafe", {"pressure": 1}, "# unsafe")

    def test_output_writer_creates_only_summary_pair(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            json_path, markdown_path = publisher.write_outputs(
                root, "stability-safe", {"status": "passed"}, "# Safe summary"
            )
            self.assertEqual(sorted(path.name for path in root.iterdir()), [
                "stability-safe.summary.json",
                "stability-safe.summary.md",
            ])
            self.assertTrue(json_path.exists())
            self.assertTrue(markdown_path.exists())


if __name__ == "__main__":
    unittest.main()
