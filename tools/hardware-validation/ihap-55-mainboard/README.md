# IHAP-55 mainboard validation harness

## Pre-fabrication

```bash
python3 host/ihap55_contract_check.py
python3 host/ihap55_sim.py
python3 -m unittest discover -s host/tests -v
```

Revision-A expected result: contract PASS, 28/28 continuous corner-screen cases PASS, 8 unit tests PASS.

## Fabricated board

```bash
python3 -m pip install -r host/requirements.txt
python3 host/ihap55_board_test.py --port /dev/ttyACM0 --profile standard
python3 host/ihap55_board_test.py --port /dev/ttyACM0 --profile precision
```

The physical runner is independent from simulation: a simulated PASS cannot satisfy a fabricated-board gate.

## Firmware lineage

Reuse/port the already validated IHAP-50 code for DHT11, BME280, OLED, LD2410C, door and spare-pin checks. Add TLA2024 rail-health reads plus the JSON command protocol in `docs/evidence/IHAP-55/board-self-test-protocol.md`. Until the IHAP-55 board firmware builds against the selected ESP-IDF revision, firmware build remains `[UNVALIDATED]`.
