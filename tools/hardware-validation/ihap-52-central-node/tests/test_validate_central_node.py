import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'validate_central_node.py'
SPEC = importlib.util.spec_from_file_location('ihap52_validate', SCRIPT)
assert SPEC and SPEC.loader
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


def good_snapshot(throttle=0):
    return {
        'repository': {
            'commit': {'returncode': 0, 'stdout': 'abc'},
            'branch': {'returncode': 0, 'stdout': 'ihap-52-central-node-hardware-decision'},
            'status': {'returncode': 0, 'stdout': ''},
        },
        'system': {
            'raspberry_model': 'Raspberry Pi 4 Model B Rev 1.5',
            'architecture': 'aarch64',
            'logical_cpus': 4,
            'memory': {'MemTotal': 8_000_000_000},
            'os_release': {'PRETTY_NAME': 'Raspberry Pi OS'},
            'graphics_devices': ['card0', 'renderD128'],
            'boot_id': 'boot-a',
            'uptime_seconds': 100.0,
        },
        'storage': {'filesystem_total_bytes': 30_000_000_000},
        'network': {'wifi_interfaces': [{'name': 'wlan0', 'operstate': 'up', 'has_ip': True}]},
        'raspberry_pi': {'throttled_before': {'value': throttle}},
    }


class TestIHAP52Validation(unittest.TestCase):
    def test_pi4_preflight_happy_path(self):
        manual = {'a2_confirmed': True, 'rpios_lite64_confirmed': True, 'psu_rating': '5.1V 3A'}
        checks = mod.evaluate_preflight(good_snapshot(), 'pi4-reference', manual)
        self.assertTrue(all(checks.values()))

    def test_graphics_device_is_observation_not_mvp_gate(self):
        snapshot = good_snapshot()
        snapshot['system']['graphics_devices'] = []
        manual = {'a2_confirmed': True, 'rpios_lite64_confirmed': True, 'psu_rating': '5.1V 3A'}
        checks = mod.evaluate_preflight(snapshot, 'pi4-reference', manual)
        self.assertNotIn('graphics_compute_device', checks)
        self.assertTrue(all(checks.values()))

    def test_pi4_requires_vcgencmd(self):
        snapshot = good_snapshot(None)
        checks = mod.evaluate_preflight(snapshot, 'pi4-reference')
        self.assertFalse(checks['vcgencmd_available'])
        self.assertFalse(checks['clean_throttle_history_before_run'])

    def test_pi4_requires_clean_throttle_history(self):
        checks = mod.evaluate_preflight(good_snapshot(1 << 16), 'pi4-reference')
        self.assertFalse(checks['clean_throttle_history_before_run'])

    def test_manual_evidence_is_gate(self):
        manual = {'a2_confirmed': False, 'rpios_lite64_confirmed': True, 'psu_rating': '5.1V 3A'}
        checks = mod.evaluate_preflight(good_snapshot(), 'pi4-reference', manual)
        self.assertFalse(checks['manual_a2_confirmed'])

    def test_equivalent_profile_does_not_require_vcgencmd(self):
        snapshot = good_snapshot(None)
        snapshot['system']['raspberry_model'] = None
        snapshot['system']['architecture'] = 'x86_64'
        checks = mod.evaluate_preflight(snapshot, 'equivalent')
        self.assertNotIn('vcgencmd_available', checks)
        self.assertTrue(all(checks.values()))

    def test_final_rejects_storage_hash_mismatch(self):
        payload = {
            'storage_smoke': {'bytes_written': 128, 'bytes_requested': 128, 'bytes_read': 128, 'hash_match': False, 'temporary_file_removed': True},
            'stress': {'worker_exitcodes': [0, 0, 0, 0]},
            'raspberry_pi': {'throttled_after': {'value': 0}},
            'system': {'boot_id': 'boot-a'},
            'system_after': {'boot_id': 'boot-a'},
            'oom_observation': {'available': False, 'oom_pattern_seen': None},
        }
        checks = mod.evaluate_final(payload, 'pi4-reference')
        self.assertFalse(checks['storage_integrity'])

    def test_final_rejects_any_throttle_history(self):
        payload = {
            'storage_smoke': {'bytes_written': 128, 'bytes_requested': 128, 'bytes_read': 128, 'hash_match': True, 'temporary_file_removed': True},
            'stress': {'worker_exitcodes': [0, 0, 0, 0]},
            'raspberry_pi': {'throttled_after': {'value': 1 << 18}},
            'system': {'boot_id': 'boot-a'},
            'system_after': {'boot_id': 'boot-a'},
            'oom_observation': {'available': True, 'oom_pattern_seen': False},
        }
        checks = mod.evaluate_final(payload, 'pi4-reference')
        self.assertFalse(checks['no_pi_throttle_or_undervoltage'])

    def test_run_directory_never_overwrites(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            first = mod.make_run_dir(base)
            first.mkdir()
            second = mod.make_run_dir(base)
            self.assertNotEqual(first, second)


if __name__ == '__main__':
    unittest.main()
