from __future__ import annotations

import importlib.util
import sys
import types
import unittest
from pathlib import Path

# Import the reconnect logic without requiring hardware.
ihap45_stub = types.ModuleType("ihap45")
ihap45_stub.DEFAULT_BAUD = 115200
ihap45_stub.DEFAULT_OUTPUT_ROOT = Path("runs")
ihap45_stub.HarnessError = RuntimeError
sys.modules["ihap45"] = ihap45_stub

MODULE_PATH = Path(__file__).resolve().parents[1] / "ihap45_resilient.py"
SPEC = importlib.util.spec_from_file_location("ihap45_resilient", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
resilient = importlib.util.module_from_spec(SPEC)
sys.modules["ihap45_resilient"] = resilient
SPEC.loader.exec_module(resilient)


class PortInfo:
    def __init__(self, device: str, *, vid=None, pid=None, serial_number=None, location=None):
        self.device = device
        self.vid = vid
        self.pid = pid
        self.serial_number = serial_number
        self.location = location


class ListPorts:
    def __init__(self, ports):
        self.ports = ports

    def comports(self):
        return list(self.ports)


class PortSelectionTests(unittest.TestCase):
    def test_selects_reenumerated_device_by_serial_number(self) -> None:
        identity = resilient.PortIdentity(
            requested_path="/missing/ttyACM0",
            vid=0x303A,
            pid=0x1001,
            serial_number="ABC",
            location="1-2",
        )
        ports = ListPorts(
            [PortInfo("/dev/ttyACM1", vid=0x303A, pid=0x1001, serial_number="ABC", location="1-2")]
        )
        self.assertEqual(resilient.select_port(identity, ports), "/dev/ttyACM1")

    def test_does_not_guess_when_multiple_same_family_ports_exist(self) -> None:
        identity = resilient.PortIdentity(requested_path="/missing/ttyACM0")
        ports = ListPorts([PortInfo("/dev/ttyACM1"), PortInfo("/dev/ttyACM2")])
        self.assertIsNone(resilient.select_port(identity, ports))

    def test_selects_unique_same_vid_pid_device(self) -> None:
        identity = resilient.PortIdentity(requested_path="/missing/device", vid=0x303A, pid=0x1001)
        ports = ListPorts([PortInfo("/dev/ttyACM3", vid=0x303A, pid=0x1001)])
        self.assertEqual(resilient.select_port(identity, ports), "/dev/ttyACM3")


if __name__ == "__main__":
    unittest.main()
