# IHAP-46 — Presence Sensor Validation Harness

Laboratory-only validation package for comparing the owned LD2410C specimen with an identified PIR alternative under the IHAP-46 decision boundary.

This package does **not** select a sensor, modify the MVP firmware, create an ADR, validate power consumption, freeze final wiring, or authorize alarm/security claims. Detailed radar telemetry is captured only as controlled engineering evidence. The only permitted production semantic remains the boolean `presence_detected` state `[UNVALIDATED]`.

## Current checkpoint

Implemented:

- ESP-IDF test firmware for LD2410C UART telemetry;
- optional LD2410C digital output sampling;
- optional PIR digital output sampling;
- reset-tolerant host serial capture;
- ground-truth scenario markers;
- JSON results and a self-contained interactive HTML report;
- configurable scenario matrix;
- host-side automated tests.

Not performed yet:

- physical execution;
- exact module/revision qualification;
- electrical-level acceptance;
- PIR specimen selection;
- sensor decision;
- ADR or BOM update.

## Directory structure

```text
config/test-plan.json       scenario matrix and trial evaluation thresholds
firmware/                   ESP-IDF laboratory firmware
host/ihap46.py              capture, mark, report and self-test CLI
host/requirements.txt       host runtime dependency
runs/                       generated locally; do not commit raw runs by default
tests/test_ihap46.py        host-side automated tests
```

## Electrical stop gate

Before connecting any signal pin, identify the exact module and verify its pinout and output logic levels.

Initial RX-only LD2410C evidence can reuse the historical prototype path:

```text
LD2410C VCC -> board 5 V rail
LD2410C GND -> board GND
LD2410C TX  -> ESP32-C3 GPIO5
```

The defaults deliberately keep these paths disabled until explicitly configured:

```text
ESP32-C3 TX -> LD2410C RX
LD2410C OUT -> ESP32-C3 GPIO
PIR OUT     -> ESP32-C3 GPIO
```

Enable them through `idf.py menuconfig` only after the specimen and logic-level checks. These are temporary laboratory connections; IHAP-50 owns final wiring.

## Firmware build

From `firmware/` with ESP-IDF 6.x activated:

```bash
idf.py set-target esp32c3
idf.py menuconfig
idf.py build
idf.py -p /dev/ttyACM0 flash
```

The firmware emits newline-delimited JSON at 115200 baud. LD2410C UART is read at 256000 baud. A boot record is emitted once and sample records are emitted at the configured period.

## Host setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r host/requirements.txt
python host/ihap46.py validate-plan
python host/ihap46.py list-scenarios
```

## Preflight

The collector automatically waits for `/dev/ttyACM0` to reappear after an ESP32-C3 reset instead of aborting the run.

```bash
python host/ihap46.py preflight \
  --port /dev/ttyACM0 \
  --seconds 20
```

Preflight requires:

- a parsed harness boot record;
- sample records;
- at least one fresh, valid LD2410C UART target-data frame.

## Controlled capture

Terminal 1:

```bash
python host/ihap46.py capture \
  --port /dev/ttyACM0 \
  --run-id IHAP46-RUN-01 \
  --plan config/test-plan.json
```

Terminal 2, at scenario start:

```bash
python host/ihap46.py mark \
  --run-id IHAP46-RUN-01 \
  --scenario ROOM_EMPTY_BASELINE \
  --phase start \
  --repetition 1 \
  --note "room empty; door closed"
```

At scenario end:

```bash
python host/ihap46.py mark \
  --run-id IHAP46-RUN-01 \
  --scenario ROOM_EMPTY_BASELINE \
  --phase end \
  --repetition 1
```

Stop capture with `Ctrl+C` only after closing the current interval.

## Report

```bash
python host/ihap46.py report \
  --run-id IHAP46-RUN-01 \
  --plan config/test-plan.json
```

Generated under `runs/IHAP46-RUN-01/`:

- `serial.log` — complete decoded console stream;
- `records.jsonl` — parsed JSON records with host timestamps;
- `marks.jsonl` — manual ground-truth markers;
- `capture-events.jsonl` — serial connect/disconnect/reconnect history;
- `results.json` — machine-readable evaluation;
- `report.html` — self-contained interactive human-readable report.

## Synthetic self-test

This checks the host pipeline without hardware:

```bash
python host/ihap46.py selftest \
  --output runs/IHAP46-SELFTEST
```

## Automated tests

```bash
python -m unittest discover -s tests -v
```

The thresholds in `config/test-plan.json` are trial criteria for the controlled comparison. They do not establish manufacturer accuracy, security reliability, statistical generalizability, battery feasibility, or final Project Owner acceptance.
