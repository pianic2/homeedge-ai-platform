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

GUIDE_SPEC = importlib.util.spec_from_file_location("ihap45_phase_guide", HOST_DIR / "ihap45_phase_guide.py")
assert GUIDE_SPEC is not None and GUIDE_SPEC.loader is not None
guide = importlib.util.module_from_spec(GUIDE_SPEC)
sys.modules["ihap45_phase_guide"] = guide
GUIDE_SPEC.loader.exec_module(guide)


class PhaseGuideTests(unittest.TestCase):
    def test_zero_duration_plan_marks_all_phases(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            run_dir = root / "run"
            plan_path = root / "plan.json"
            ihap45.initialize_run(run_dir, "RUN-01", "/dev/null", 115200, plan_path)
            plan_path.write_text(
                json.dumps(
                    {
                        "phases": [
                            {"name": "warmup", "minimum_seconds": 0},
                            {"name": "baseline", "minimum_seconds": 0},
                        ]
                    }
                ),
                encoding="utf-8",
            )
            prompts = iter(["", ""])
            output: list[str] = []
            completed = guide.run_guide(
                run_dir,
                plan_path,
                input_fn=lambda _prompt: next(prompts),
                sleep_fn=lambda _seconds: None,
                monotonic_fn=lambda: 0.0,
                output=output.append,
            )
            self.assertTrue(completed)
            markers = ihap45.read_jsonl(ihap45.run_paths(run_dir)["markers"])
            self.assertEqual([record["phase"] for record in markers[-2:]], ["warmup", "baseline"])
            summary = json.loads((run_dir / "phase-guide-summary.json").read_text(encoding="utf-8"))
            self.assertEqual(summary["status"], "completed")

    def test_stop_aborts_before_next_marker(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            run_dir = root / "run"
            plan_path = root / "plan.json"
            ihap45.initialize_run(run_dir, "RUN-02", "/dev/null", 115200, plan_path)
            plan_path.write_text(json.dumps({"phases": [{"name": "warmup", "minimum_seconds": 0}]}), encoding="utf-8")
            completed = guide.run_guide(
                run_dir,
                plan_path,
                input_fn=lambda _prompt: "STOP",
                output=lambda _message: None,
            )
            self.assertFalse(completed)
            markers = ihap45.read_jsonl(ihap45.run_paths(run_dir)["markers"])
            self.assertEqual(len(markers), 1)


if __name__ == "__main__":
    unittest.main()
