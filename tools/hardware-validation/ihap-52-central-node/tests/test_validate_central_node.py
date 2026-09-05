import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "validate_central_node.py"
SPEC = importlib.util.spec_from_file_location("ihap52_validate", SCRIPT)
assert SPEC and SPEC.loader
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


def good_snapshot(throttle=0):
    return {
        "repository": {
            "commit": {"returncode": 0, "stdout": "abc"},
            "branch": {"returncode": 0, "stdout": "ihap-52-central-node-hardware-decision"},
            "status": {"returncode": 0, "stdout": ""},
        },
        "system": {
            "raspberry_model": "Raspberry Pi 4 Model B Rev 1.5",
            "architecture": "aarch64",
            "logical_cpus": 4,
            "memory": {"MemTotal": 8_000_000_000},
            "os_release": {"PRETTY_NAME": "Debian GNU/Linux 13 (trixie)"},
            "graphics_devices": ["card0", "renderD128"],
            "boot_id": "boot-a",
            "uptime_seconds": 100.0,
        },
        "storage": {"filesystem_total_bytes": 30_000_000_000},
        "network": {"wifi_interfaces": [{"name": "wlan0", "operstate": "up", "has_ip": True}]},
        "raspberry_pi": {"throttled_before": {"value": throttle}},
    }


def good_final_payload(after=0, samples=None):
    return {
        "storage_smoke": {
            "bytes_written": 128,
            "bytes_requested": 128,
            "bytes_read": 128,
            "hash_match": True,
            "temporary_file_removed": True,
        },
        "stress": {
            "worker_exitcodes": [0, 0, 0, 0],
            "samples": samples or [],
        },
        "raspberry_pi": {"throttled_after": {"value": after}},
        "system": {"boot_id": "boot-a"},
        "system_after": {"boot_id": "boot-a"},
        "oom_observation": {"available": True, "oom_pattern_seen": False},
    }


class TestIHAP52Validation(unittest.TestCase):
    def test_pi4_preflight_happy_path_a1(self):
        manual = {"sd_application_class": "A1", "rpios_lite64_confirmed": True, "psu_rating": "5V 2.5A"}
        checks = mod.evaluate_preflight(good_snapshot(), "pi4-reference", manual)
        self.assertTrue(all(checks.values()))

    def test_pi4_preflight_happy_path_a2(self):
        manual = {"sd_application_class": "A2", "rpios_lite64_confirmed": True, "psu_rating": "5.1V 3A"}
        checks = mod.evaluate_preflight(good_snapshot(), "pi4-reference", manual)
        self.assertTrue(all(checks.values()))

    def test_graphics_device_is_observation_not_mvp_gate(self):
        snapshot = good_snapshot()
        snapshot["system"]["graphics_devices"] = []
        manual = {"sd_application_class": "A1", "rpios_lite64_confirmed": True, "psu_rating": "5.1V 3A"}
        checks = mod.evaluate_preflight(snapshot, "pi4-reference", manual)
        self.assertNotIn("graphics_compute_device", checks)
        self.assertTrue(all(checks.values()))

    def test_pi4_requires_vcgencmd(self):
        snapshot = good_snapshot(None)
        checks = mod.evaluate_preflight(snapshot, "pi4-reference")
        self.assertFalse(checks["vcgencmd_available"])
        self.assertFalse(checks["clean_throttle_history_before_run"])

    def test_pi4_requires_clean_throttle_history(self):
        checks = mod.evaluate_preflight(good_snapshot(1 << 16), "pi4-reference")
        self.assertFalse(checks["clean_throttle_history_before_run"])

    def test_unsupported_sd_class_is_rejected(self):
        manual = {"sd_application_class": "OTHER", "rpios_lite64_confirmed": True, "psu_rating": "5.1V 3A"}
        checks = mod.evaluate_preflight(good_snapshot(), "pi4-reference", manual)
        self.assertFalse(checks["manual_sd_application_class_supported"])

    def test_1_55a_psu_is_rejected(self):
        manual = {"sd_application_class": "A1", "rpios_lite64_confirmed": True, "psu_rating": "5V 1.55A"}
        checks = mod.evaluate_preflight(good_snapshot(), "pi4-reference", manual)
        self.assertTrue(checks["manual_psu_rating_parseable"])
        self.assertFalse(checks["manual_psu_supported_for_pi4"])

    def test_2_5a_psu_is_accepted_for_bounded_reference_run(self):
        manual = {"sd_application_class": "A1", "rpios_lite64_confirmed": True, "psu_rating": "5V 2.5A"}
        checks = mod.evaluate_preflight(good_snapshot(), "pi4-reference", manual)
        self.assertTrue(checks["manual_psu_supported_for_pi4"])

    def test_unparseable_psu_is_rejected(self):
        manual = {"sd_application_class": "A1", "rpios_lite64_confirmed": True, "psu_rating": "phone charger"}
        checks = mod.evaluate_preflight(good_snapshot(), "pi4-reference", manual)
        self.assertFalse(checks["manual_psu_rating_parseable"])
        self.assertFalse(checks["manual_psu_supported_for_pi4"])

    def test_equivalent_profile_does_not_require_vcgencmd(self):
        snapshot = good_snapshot(None)
        snapshot["system"]["raspberry_model"] = None
        snapshot["system"]["architecture"] = "x86_64"
        checks = mod.evaluate_preflight(snapshot, "equivalent")
        self.assertNotIn("vcgencmd_available", checks)
        self.assertTrue(all(checks.values()))

    def test_final_rejects_storage_hash_mismatch(self):
        payload = good_final_payload()
        payload["storage_smoke"]["hash_match"] = False
        checks = mod.evaluate_final(payload, "pi4-reference")
        self.assertFalse(checks["storage_integrity"])

    def test_final_separates_thermal_throttle_from_undervoltage(self):
        payload = good_final_payload(after=1 << 18)
        checks = mod.evaluate_final(payload, "pi4-reference")
        self.assertTrue(checks["no_pi_undervoltage"])
        self.assertFalse(checks["no_pi_frequency_cap_or_throttle"])
        self.assertTrue(checks["no_pi_soft_temperature_limit"])

    def test_final_separates_undervoltage_from_thermal_throttle(self):
        payload = good_final_payload(after=1 << 16)
        checks = mod.evaluate_final(payload, "pi4-reference")
        self.assertFalse(checks["no_pi_undervoltage"])
        self.assertTrue(checks["no_pi_frequency_cap_or_throttle"])
        self.assertTrue(checks["no_pi_soft_temperature_limit"])

    def test_final_rejects_throttle_seen_during_stress_even_if_after_clear(self):
        samples = [{"throttled": {"value": 1 << 1}}]
        payload = good_final_payload(after=0, samples=samples)
        checks = mod.evaluate_final(payload, "pi4-reference")
        self.assertFalse(checks["no_pi_frequency_cap_or_throttle"])

    def test_throttle_flag_decode(self):
        value = (1 << 1) | (1 << 17)
        flags = mod.throttle_flags(value)
        self.assertIn("current_frequency_capped", flags)
        self.assertIn("historical_frequency_capped", flags)
        self.assertNotIn("current_undervoltage", flags)

    def test_run_directory_never_overwrites(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            first = mod.make_run_dir(base)
            first.mkdir()
            second = mod.make_run_dir(base)
            self.assertNotEqual(first, second)


if __name__ == "__main__":
    unittest.main()
