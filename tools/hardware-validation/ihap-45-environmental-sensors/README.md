# IHAP-45 Environmental Sensor Validation Harness

**Issue:** IHAP-45 — Environmental Sensor Decision — DHT11 vs DHT22 vs BME280  
**Purpose:** controlled, parallel qualification of the three owned environmental-sensor modules  
**Status:** firmware and host tooling physically exercised; staged stability gate reported passed; controlled 115-minute run ready

This directory is deliberately named `ihap-45-environmental-sensors`:

- `IHAP` matches the Jira project key;
- `environmental-sensors` avoids implying that atmospheric pressure belongs to the MVP;
- pressure acquisition is disabled and no pressure field is emitted or accepted.

The harness is validation tooling. It is not production firmware and does not freeze the final wiring owned by IHAP-50.

## 1. Test subjects

| Sensor ID | Owned module | Interface | Qualification objective |
|---|---|---|---|
| `DHT11-OWNED-01` | blue DHT11-compatible three-pin breakout | proprietary single-wire | communication stability, response, repeatability |
| `DHT22-OWNED-01` | white DHT22/AM2302-compatible three-pin breakout | proprietary single-wire | communication stability, response, repeatability |
| `BME280-OWNED-01` | purple `BME/BMP280` / `GYBMEP` four-pin breakout | I2C | address, chip identity, humidity support, response, repeatability |

The purple PCB is accepted for this owned specimen only after runtime probing:

- observed I2C address: `0x76`;
- observed chip ID: `0x60`;
- detected type: `BME280`;
- humidity supported: `true`.

BMP280-class IDs `0x58`, `0x56` and `0x57` remain rejected because humidity is unavailable.

## 2. Validation wiring

Use board silkscreen labels, not breadboard row assumptions.

| Module pin | ESP32-C3 connection | Default GPIO |
|---|---|---:|
| DHT11 `+` | `3.3V` | — |
| DHT11 `out` | digital input/output | GPIO3 |
| DHT11 `-` | `GND` | — |
| DHT22 `+` | `3.3V` | — |
| DHT22 `out` | digital input/output | GPIO4 |
| DHT22 `-` | `GND` | — |
| BME280 `VIN` | `3.3V` | — |
| BME280 `GND` | `GND` | — |
| BME280 `SDA` | I2C SDA | GPIO5 |
| BME280 `SCL` | I2C SCL | GPIO6 |

Constraints:

1. Do not use GPIO2; ADR-0001 excludes it from the conservative application profile.
2. Power all three modules from 3.3 V.
3. Use one common ground.
4. Keep the qualified pull-up and breakout configuration unchanged during comparative testing.
5. The pin allocation is a validation-harness allocation, not final product wiring.

## 3. Physical arrangement

For the comparative run:

- keep the ESP32-C3 outside the controlled enclosure when practical;
- place only the sensing modules inside;
- keep sensing elements at equivalent height and orientation;
- keep approximately equal cable lengths;
- avoid chamber walls, wet surfaces, direct airflow, direct heat and condensation;
- maintain a small gap between modules;
- do not move the sensors between phases unless the run is aborted and restarted.

Placement-induced bias remains a separate risk to be recorded under IHAP-45 and followed through IHAP-50/IHAP-51.

## 4. Prerequisites

- ESP-IDF with ESP32-C3 support;
- Python 3.11 or later recommended;
- USB data cable connected directly to the PC;
- optional independent thermo-hygrometer.

Without an independent reference, the output is a relative comparison and must not be presented as absolute accuracy validation.

Host setup:

```bash
cd tools/hardware-validation/ihap-45-environmental-sensors
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r host/requirements.txt
python -m unittest discover -s host/tests -v
```

## 5. Build and flash

```bash
cd firmware
idf.py set-target esp32c3
idf.py build
idf.py -p /dev/ttyACM0 flash
cd ..
```

Do not run `idf.py monitor` at the same time as a host capture command.

The validation firmware delays application startup after reset so Linux can recreate the ESP32-C3 native-USB serial device before one-shot metadata are emitted.

## 6. Resilient preflight

```bash
python host/ihap45_resilient.py preflight \
  --port /dev/ttyACM0 \
  --plan config/test-plan.json \
  --duration-seconds 120
```

After `Connected`, press `RST` exactly once.

The preflight requires:

- one boot metadata record;
- a successful BME280 probe with chip ID `0x60`;
- temperature and humidity channels only;
- valid samples from all three sensors;
- no pressure field;
- no repeated boot.

An initial integrated preflight correctly exposed a brownout. The validator was not weakened. A staged five-minute functional-stability procedure was then added and the Project Owner reported the required follow-up configurations as passed.

See [`BROWNOUT-DIAGNOSTIC.md`](BROWNOUT-DIAGNOSTIC.md).

## 7. Controlled 115-minute acquisition

Follow [`RUNBOOK-115-MINUTES.md`](RUNBOOK-115-MINUTES.md).

Terminal 1:

```bash
python host/ihap45_resilient.py capture \
  --port /dev/ttyACM0 \
  --run-id IHAP45-RUN-01 \
  --plan config/test-plan.json
```

After `Connected`, press `RST` once and wait for boot, successful probe and one complete three-sensor batch.

Terminal 2:

```bash
python host/ihap45_phase_guide.py \
  --run-dir runs/IHAP45-RUN-01 \
  --plan config/test-plan.json
```

The guide explicitly asks the operator to confirm each environmental condition, writes the phase marker and times the minimum duration. The plan contains twelve phases totalling 115 minimum minutes.

Safety rules:

- no direct water, mist or steam;
- no flame, heat gun, hair dryer or direct hot/cold airflow;
- use separated sealed warm/cold masses and separated humidity/dry sources;
- stop if condensation appears;
- stay within every candidate's declared operating range;
- do not call the setup a calibrated chamber without calibration evidence.

## 8. Strict acceptance and local analysis

After the phase guide completes, wait for one additional complete sample batch and stop capture with `Ctrl+C`.

Run the strict gate:

```bash
python host/ihap45_final_gate.py \
  --run-dir runs/IHAP45-RUN-01 \
  --plan config/test-plan.json
```

The strict gate blocks:

- missing or multiple boot records;
- any brownout line;
- missing successful BME280 probe;
- missing or short phases;
- insufficient completeness or valid samples;
- forbidden pressure fields.

When it passes, generate the local report:

```bash
python host/ihap45.py analyze \
  --run-dir runs/IHAP45-RUN-01 \
  --plan config/test-plan.json
```

Local outputs include aggregate JSON, per-sample CSV and an interactive HTML report. All remain under ignored `runs/` storage.

## 9. Summary-only repository publication

Raw telemetry must not be committed. `runs/` is ignored and the evidence directory has additional deny-list patterns.

Publish a stability summary:

```bash
python host/ihap45_publish.py stability \
  --run-dir runs/IHAP45-STABILITY-S4 \
  --output-dir ../../../docs/evidence/IHAP-45/summaries
```

Publish the environmental summary:

```bash
python host/ihap45_publish.py environmental \
  --run-dir runs/IHAP45-RUN-01 \
  --plan config/test-plan.json \
  --output-dir ../../../docs/evidence/IHAP-45/summaries
```

The publisher creates only allow-listed `*.summary.json` and `*.summary.md` files. It does not copy:

- serial logs;
- individual samples;
- marker or reference streams;
- workstation paths or port history;
- per-sample CSV;
- interactive HTML containing the underlying sample stream.

Review the generated files and `git diff` before staging.

See:

- [`docs/evidence/IHAP-45/README.md`](../../../docs/evidence/IHAP-45/README.md)
- [`docs/evidence/IHAP-45/STATUS.md`](../../../docs/evidence/IHAP-45/STATUS.md)
- [`docs/evidence/IHAP-45/PUBLICATION-POLICY.md`](../../../docs/evidence/IHAP-45/PUBLICATION-POLICY.md)

## 10. Evidence semantics

The harness may support claims about:

- observed communication success or failure;
- owned BME280 chip identity and address;
- sample completeness and error rates;
- relative disagreement, noise, response and repeatability;
- optional aggregate reference-error metrics when an independent reference exists.

It does not prove by itself:

- calibration;
- absolute accuracy without an independent reference;
- universal behavior of all DHT11, DHT22 or BME280 modules;
- seller or lot reproducibility;
- final enclosure performance;
- current draw, rail capacity, regulator capability or autonomy;
- production, medical, precision, safety or certification maturity.

Unsupported claims remain `[UNVALIDATED]`.

## 11. Decision boundary

Completing the run does not automatically select the sensor. The Project Owner reviews the sanitized summaries and resolves `PO-45-01` and `PO-45-02`. Only then is the single decision ADR drafted.
