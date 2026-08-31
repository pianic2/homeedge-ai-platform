from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

HOST_DIR = Path(__file__).resolve().parents[1]
for module_name in ("ihap45", "ihap45_resilient"):
    module_path = HOST_DIR / f"{module_name}.py"
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

STABILITY_PATH = HOST_DIR / "ihap45_stability.py"
SPEC = importlib.util.spec_from_file_location("ihap45_stability", STABILITY_PATH)
assert SPEC is not None and SPEC.loader is not None
stability = importlib.util.module_from_spec(SPEC)
sys.modules["ihap45_stability"] = stability
SPEC.loader.exec_module(stability)


class StabilityEvaluationTests(unittest.TestCase):
    def test_clean_window_passes(self) -> None:
        result = stability.evaluate_stability(
            boot_records=1,
            brownout_lines=0,
            disconnects_after_start=0,
            valid_sample_records=180,
            completed_window=True,
        )
        self.assertTrue(result.passed)
        self.assertEqual(result.errors, [])

    def test_brownout_and_second_boot_are_blocking(self) -> None:
        result = stability.evaluate_stability(
            boot_records=2,
            brownout_lines=1,
            disconnects_after_start=1,
            valid_sample_records=60,
            completed_window=True,
        )
        self.assertFalse(result.passed)
        self.assertTrue(any("unexpected reboot" in error for error in result.errors))
        self.assertTrue(any("brownout" in error for error in result.errors))
        self.assertTrue(any("USB disconnected" in error for error in result.errors))

    def test_board_only_without_samples_is_warning_not_failure(self) -> None:
        result = stability.evaluate_stability(
            boot_records=1,
            brownout_lines=0,
            disconnects_after_start=0,
            valid_sample_records=0,
            completed_window=True,
        )
        self.assertTrue(result.passed)
        self.assertTrue(any("board-only" in warning for warning in result.warnings))

    def test_incomplete_window_fails(self) -> None:
        result = stability.evaluate_stability(
            boot_records=1,
            brownout_lines=0,
            disconnects_after_start=0,
            valid_sample_records=3,
            completed_window=False,
        )
        self.assertFalse(result.passed)
        self.assertTrue(any("did not complete" in error for error in result.errors))


if __name__ == "__main__":
    unittest.main()
