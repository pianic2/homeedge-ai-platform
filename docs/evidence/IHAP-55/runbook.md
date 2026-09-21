# IHAP-55 owner verification runbook

Run from the repository root on branch `ihap-55-integrated-modular-edge-pcb`.

```bash
python3 tools/hardware-validation/ihap-55-mainboard/host/ihap55_contract_check.py
python3 tools/hardware-validation/ihap-55-mainboard/host/ihap55_sim.py
python3 tools/hardware-validation/ihap-55-mainboard/host/ihap55_power_math.py
python3 -m unittest discover -s tools/hardware-validation/ihap-55-mainboard/host/tests -v
```

Firmware build on this machine (ESP-IDF v6.0.1 is already installed):

```bash
source /home/optimus/.espressif/v6.0.1/esp-idf/export.sh
cd tools/hardware-validation/ihap-55-mainboard/firmware
idf.py set-target esp32c3
idf.py build
cd ../../../..
```

KiCad 10.0.6 is installed as a user Flatpak on this machine. When a complete native schematic/PCB has been committed, execute these gates; today the inputs are absent and neither gate is a PASS:

```bash
flatpak run --command=kicad-cli org.kicad.KiCad --version
flatpak run --command=kicad-cli org.kicad.KiCad sch erc --severity-all --exit-code-violations -o docs/evidence/IHAP-55/erc-report.txt hardware/edge-mainboard/homeedge-edge-mainboard.kicad_sch
flatpak run --command=kicad-cli org.kicad.KiCad pcb drc --severity-all --exit-code-violations --schematic-parity -o docs/evidence/IHAP-55/drc-report.txt hardware/edge-mainboard/homeedge-edge-mainboard.kicad_pcb
```

Future `IHAP55-BOARD-01`, only after fabrication is explicitly authorized and connector/battery polarity is checked:

```bash
source /home/optimus/.espressif/v6.0.1/esp-idf/export.sh
cd tools/hardware-validation/ihap-55-mainboard/firmware
idf.py -p /dev/ttyACM0 flash
cd ../../../..
python3 -m venv /tmp/ihap55-board-venv
/tmp/ihap55-board-venv/bin/pip install -r tools/hardware-validation/ihap-55-mainboard/host/requirements.txt
/tmp/ihap55-board-venv/bin/python tools/hardware-validation/ihap-55-mainboard/host/ihap55_board_test.py --port /dev/ttyACM0 --profile standard --out docs/evidence/IHAP-55/runs/IHAP55-BOARD-01.json
```

Use `--profile precision` when the installed environmental module is BME280. Confirm the USB device path after reset/re-enumeration. The JSON self-test is diagnostic; separately execute calibrated DMM/oscilloscope/load/thermal and transfer validation for ADR-0007. Do not interpret an output JSON or firmware build as physical power qualification.

Before final I2C/DHT pull-up population, characterize each owned breakout **unpowered and disconnected**: measure resistance from SDA to its VCC pin and SCL to VCC on OLED and BME280, and DHT DATA to VCC on the DHT11 module; record both meter polarities and module markings. Treat semiconductor paths or unstable readings as inconclusive. Compute the parallel effective resistance of all installed module resistors plus any proposed board resistor; leave board footprints DNP until the resulting pull-up current and I2C 30–70% rise time are checked on the assembled cable at 100 kHz. The preliminary estimate `tr≈0.8473×Req×Cbus` uses measured/estimated cable and module capacitance; a scope measurement on the real bus closes the physical gate.
