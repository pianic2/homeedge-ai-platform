import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from evaluator import EXPECTED_PINS, combine, evaluate_boot, evaluate_door_phase, evaluate_samples


def boot(profile: str) -> dict:
    return {
        "record_type": "boot",
        "firmware": "ihap50-integrated-interconnect-harness",
        "pins": EXPECTED_PINS,
        "adc_spare_pull_test": True,
        "digital_spare_pull_test": True,
        "radar_tx_service_configured": False,
        "detected_profile": profile,
        "bme280_present": profile == "precision",
        "oled_visual_transfer_ok": True,
    }


def sample(profile: str, door_raw: int = 1) -> dict:
    precision = profile == "precision"
    return {
        "record_type": "integrated_sample",
        "profile": profile,
        "oled_ok": True,
        "bme280_present": precision,
        "bme280_ok": precision,
        "bme280_chip_id": "0x60" if precision else "0x00",
        "dht11_ok": not precision,
        "dht11_status": "OK" if not precision else "NO_RESPONSE",
        "radar_fresh": True,
        "radar_valid_frames": 20,
        "radar_invalid_frames": 0,
        "radar_uart_bytes": 1000,
        "door_raw": door_raw,
    }


class EvaluatorTests(unittest.TestCase):
    def test_standard_profile_passes(self):
        result = combine(
            evaluate_boot(boot("standard"), "standard"),
            evaluate_samples([sample("standard") for _ in range(6)], "standard"),
        )
        self.assertTrue(result.passed, result.errors)

    def test_precision_profile_ignores_absent_dht(self):
        result = combine(
            evaluate_boot(boot("precision"), "precision"),
            evaluate_samples([sample("precision") for _ in range(6)], "precision"),
        )
        self.assertTrue(result.passed, result.errors)

    def test_wrong_adc_mapping_fails_boot(self):
        candidate = boot("standard")
        candidate["pins"] = dict(EXPECTED_PINS)
        candidate["pins"]["adc_spare"] = 10
        result = evaluate_boot(candidate, "standard")
        self.assertFalse(result.passed)
        self.assertIn("pins", result.errors)

    def test_service_tx_enabled_fails_boot(self):
        candidate = boot("standard")
        candidate["radar_tx_service_configured"] = True
        result = evaluate_boot(candidate, "standard")
        self.assertFalse(result.passed)
        self.assertIn("radar_service_tx_disabled", result.errors)

    def test_precision_requires_bme_identity(self):
        samples = [sample("precision") for _ in range(6)]
        samples[-1]["bme280_chip_id"] = "0x58"
        result = evaluate_samples(samples, "precision")
        self.assertFalse(result.passed)
        self.assertIn("bme280_identity", result.errors)

    def test_radar_invalid_frame_fails(self):
        samples = [sample("standard") for _ in range(6)]
        samples[-1]["radar_invalid_frames"] = 1
        result = evaluate_samples(samples, "standard")
        self.assertFalse(result.passed)
        self.assertIn("radar_no_invalid_frames", result.errors)

    def test_door_open_closed_disconnected(self):
        self.assertTrue(evaluate_door_phase([sample("standard", 1), sample("standard", 1)], 1, "open").passed)
        self.assertTrue(evaluate_door_phase([sample("standard", 0), sample("standard", 0)], 0, "closed").passed)
        self.assertTrue(evaluate_door_phase([sample("standard", 1), sample("standard", 1)], 1, "disconnected").passed)


if __name__ == "__main__":
    unittest.main()
