# IHAP-45 Environmental Sensor Validation Harness

**Issue:** IHAP-45 — Environmental Sensor Decision — DHT11 vs DHT22 vs BME280  
**Purpose:** controlled, parallel qualification of the three owned environmental-sensor modules  
**Status:** test tooling prepared; physical execution and firmware build remain `[UNVALIDATED]` until run by the Project Owner

This directory is deliberately named `ihap-45-environmental-sensors`:

- `IHAP`, not `IHAL`, matches the Jira project key;
- `environmental-sensors` avoids implying that atmospheric pressure belongs to the MVP;
- pressure acquisition is disabled and no pressure field is emitted by the firmware or host tools.

The harness is validation tooling. It is not the production firmware under `firmware/room-env-node/` and it does not freeze the final wiring owned by IHAP-50.

## 1. Test subjects

| Sensor ID | Owned module | Interface | Qualification objective |
|---|---|---|---|
| `DHT11-OWNED-01` | Blue DHT11-compatible three-pin breakout | proprietary single-wire | communication stability, response, repeatability |
| `DHT22-OWNED-01` | White DHT22/AM2302-compatible three-pin breakout | proprietary single-wire | communication stability, response, repeatability |
| `BME280-OWNED-01` | Purple `BME/BMP280` / `GYBMEP` four-pin breakout | I2C | electrical safety, address, chip identity, humidity support, response, repeatability |

The purple PCB is not accepted as BME280 from photography alone. The harness probes `0x76` and `0x77` and reads register `0xD0`:

- `0x60`: BME280 candidate, temperature and humidity enabled;
- `0x58`, `0x56`, `0x57`: BMP280-class device, rejected for IHAP-45 because humidity is unavailable;
- any other value: unsupported or unidentified device.

## 2. Validation wiring

Use the board silkscreen labels, not breadboard row assumptions.

| Module pin | ESP32-C3 connection | Default GPIO |
|---|---|---:|
| DHT11 `+` | `3.3V` | — |
| DHT11 `out` | digital input/output | GPIO3 |
| DHT11 `-` | `GND` | — |
| DHT22 `+` | `3.3V` | — |
| DHT22 `out` | digital input/output | GPIO4 |
| DHT22 `-` | `GND` | — |
| BME/BMP `VIN` | `3.3V` only for the first qualification | — |
| BME/BMP `GND` | `GND` | — |
| BME/BMP `SDA` | I2C SDA | GPIO5 |
| BME/BMP `SCL` | I2C SCL | GPIO6 |

Constraints:

1. Do not use GPIO2; ADR-0001 excludes it from the conservative application profile.
2. Power all three modules from 3.3 V for the first qualification.
3. Use one common ground.
4. Do not add external pull-ups before checking the breakout. The photographed DHT breakouts visibly contain passive components and the BME/BMP board contains interface circuitry, but exact values and rail connections remain `[UNVALIDATED]`.
5. Before connecting SDA/SCL to the ESP32-C3, verify with a multimeter that their idle voltage does not exceed the 3.3 V logic domain.
6. The pin allocation is a validation-harness allocation, not final wiring.

### Physical arrangement

For the comparative run:

- keep the ESP32-C3 outside the controlled chamber when practical;
- place only the three sensors inside;
- keep sensing elements at the same height and orientation;
- keep approximately equal cable lengths;
- avoid contact with chamber walls, wet surfaces, direct airflow, direct heat and condensation;
- keep a small gap between modules so one PCB does not shade or heat another.

Placement-induced bias is a separate risk to be recorded under IHAP-45 and later verified with IHAP-50/IHAP-51. This harness first compares the sensors under the most equivalent placement achievable.

## 3. Prerequisites

- ESP-IDF with ESP32-C3 support. The firmware uses the bus-device I2C API from `driver/i2c_master.h`.
- Python 3.11 or later recommended.
- USB data cable.
- Optional independent thermo-hygrometer. Without it, the output is a relative comparison and must not be presented as absolute accuracy validation.

Host setup:

```bash
cd tools/hardware-validation/ihap-45-environmental-sensors
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r host/requirements.txt
python -m unittest discover -s host/tests -v
```

## 4. Build and flash

```bash
cd tools/hardware-validation/ihap-45-environmental-sensors/firmware
idf.py set-target esp32c3
idf.py build
idf.py -p /dev/ttyACM0 flash
```

Do not run `idf.py monitor` at the same time as the host capture command because both processes would compete for the serial port.

Firmware defaults may be changed through:

```bash
idf.py menuconfig
```

Menu: `IHAP-45 validation harness`.

## 5. Preflight

Before the long run:

```bash
python host/ihap45.py preflight --port /dev/ttyACM0
```

The command records approximately two minutes of data and requires:

- firmware boot metadata;
- all three sensor IDs;
- a BME280 chip ID of `0x60`;
- exactly the temperature and humidity measurement channels;
- at least one valid sample from each sensor;
- no repeated ESP reset loop.

A BMP280 identification is a hard stop, not a partial success.

## 6. Full acquisition

Create a run:

```bash
python host/ihap45.py capture \
  --port /dev/ttyACM0 \
  --run-id IHAP45-RUN-01 \
  --plan config/test-plan.json
```

The capture process creates:

```text
runs/IHAP45-RUN-01/
├── current-phase.txt
├── markers.jsonl
├── reference.jsonl
├── run-metadata.json
└── raw/
    ├── serial.log
    └── samples.jsonl
```

From a second terminal, mark each phase exactly when the environmental action starts:

```bash
python host/ihap45.py mark \
  --run-dir runs/IHAP45-RUN-01 \
  --phase baseline \
  --note "Stable room conditions"
```

Optional independent reference observation:

```bash
python host/ihap45.py reference \
  --run-dir runs/IHAP45-RUN-01 \
  --source-id THERMO-HYGROMETER-01 \
  --temperature-c 23.4 \
  --humidity-percent 51.2
```

Reference values are never fabricated. When no reference file contains observations, absolute-error metrics are omitted and the report labels the outcome as relative comparison only.

## 7. Test phases

`config/test-plan.json` defines the required phase names and minimum durations. The operator controls the environment; the host tool only timestamps and validates the evidence.

Safety and validity rules:

- no direct water, mist or steam on electronics;
- no direct heat gun, hair dryer or flame;
- use sealed warm/cold masses and separated humidity sources;
- stop if condensation appears;
- do not exceed the declared operating range of any candidate;
- do not call the setup a calibrated chamber unless calibration evidence exists.

## 8. Validation and analysis

After capture:

```bash
python host/ihap45.py validate \
  --run-dir runs/IHAP45-RUN-01 \
  --plan config/test-plan.json

python host/ihap45.py analyze \
  --run-dir runs/IHAP45-RUN-01 \
  --plan config/test-plan.json
```

Generated result files:

```text
runs/IHAP45-RUN-01/results/
├── comparison.csv
├── summary.json
└── report.html
```

The self-contained HTML report includes interactive temperature/humidity timelines, per-phase statistics, error counts, read latency, pairwise deltas, response-time estimates and optional reference-error metrics.

## 9. Evidence semantics

This harness may support claims about:

- observed communication success or failure;
- BME/BMP chip identity from `0xD0`;
- observed I2C address;
- observed sample completeness;
- observed errors and read latency;
- relative disagreement, noise, response and repeatability in the executed setup.

It does not prove, by itself:

- calibration;
- absolute accuracy without an independent reference;
- universal behavior of all DHT11, DHT22 or BME280 modules;
- exact seller/lot reproducibility;
- final enclosure performance;
- power consumption, rail capacity or autonomy;
- production, medical, precision, safety or certification maturity.

Unproven claims remain `[UNVALIDATED]`.

## 10. Stop boundary

The preparation tranche ends when:

- host unit tests pass;
- firmware source and configuration exist;
- wiring and execution commands are documented;
- the evidence scaffold exists;
- no physical test has been executed by the assistant.

Firmware build, flashing, wiring, environmental manipulation and evidence capture require the Project Owner at the hardware bench.
