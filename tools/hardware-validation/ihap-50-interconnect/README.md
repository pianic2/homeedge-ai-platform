# IHAP-50 — Integrated Interconnect Validation

**Issue:** IHAP-50 — Interconnect and Prototype Assembly Decision  
**Purpose:** reproducible physical gate for the **Accepted** IHAP-50 reference interconnect contract  
**Status:** validation complete — `IHAP50-STANDARD-11` PASS + `IHAP50-PRECISION-01` PASS; retained as regression/reproduction runbook  
**Scope:** validation harness only; not product firmware, final PCB validation, or power-subsystem validation

## 1. What this gate proves

This harness physically validated the IHAP-50 prototype implementation of the Accepted contract:

- the Accepted ESP32-C3 pin allocation boots and remains recoverable;
- GPIO5 remains usable as the ADC-capable engineering spare and GPIO10 as a digital spare;
- OLED works on shared I2C GPIO6/GPIO7;
- BME280 coexists with the OLED in the precision environmental profile;
- DHT11 works on GPIO4 in the standard environmental profile;
- LD2410C frames are received on GPIO0 at 256000 baud while GPIO1 service TX remains disabled;
- MC-38 produces HIGH/open, LOW/closed, and HIGH again with one conductor disconnected;
- connector pin order and polarity were explicitly reviewed by the operator.

Accepted evidence is published under `docs/evidence/IHAP-50/`. This harness does **not** validate final PCB rail quality, source transfer, battery, charging, thermal behavior, enclosure, production reliability, or certification. Those remain downstream work.

## 2. Accepted reference pin map

| Function | ESP32-C3 pin | Rule |
|---|---:|---|
| LD2410C TX -> MCU RX | GPIO0 | UART1 RX, 256000 baud |
| LD2410C RX service line | GPIO1 | service-only physical reservation; disabled by default and disconnected for this gate |
| MC-38 door sense | GPIO3 | Accepted external pull network required |
| DHT11 data | GPIO4 | standard profile only |
| ADC engineering spare | GPIO5 | leave externally unconnected |
| I2C SDA | GPIO6 | OLED + optional BME280 |
| I2C SCL | GPIO7 | OLED + optional BME280 |
| Digital engineering spare | GPIO10 | leave externally unconnected |

Do not use GPIO2, GPIO8 or GPIO9. Keep GPIO20/GPIO21 free for recovery/UART0 when practical.

## 3. Common wiring

**Disconnect USB/power before changing wiring.** Use module pin labels, not wire colors.

### LD2410C

```text
LD2410C VCC -> ESP32-C3 5V
LD2410C GND -> common GND
LD2410C TX  -> GPIO0
LD2410C RX  -> DISCONNECTED
LD2410C OUT -> DISCONNECTED
```

GPIO1 is reserved by the Accepted interconnect contract for a controlled service TX path, but the IHAP-50 validation firmware intentionally does not configure a UART TX pin.

### OLED

```text
OLED GND -> common GND
OLED VCC -> 3.3V
OLED SCL -> GPIO7
OLED SDA -> GPIO6
```

The accepted owned display is expected at I2C address `0x3C`.

### MC-38

Validate the **Accepted IHAP-50 prototype network** rather than silently relying on an MCU internal pull-up:

```text
3.3V
 |
10k
 |
DOOR_SENSE ---- 1k ---- GPIO3
 |
MC-38
 |
GND
```

The optional 100 nF filter footprint is **DNP by default**. Its future population requires integrated noise/bounce evidence; approval of IHAP-50 does not assert that it is populated.

Expected states:

- magnet FAR / contact open -> `door_raw = 1`;
- magnet NEAR / contact closed -> `door_raw = 0`;
- one MC-38 conductor disconnected -> `door_raw = 1`.

The last condition demonstrates the accepted limitation that the simple MVP topology cannot distinguish a legitimate open contact from an interrupted wire.

## 4. Environmental profiles

The two accepted environmental profiles are alternatives. Do **not** mount DHT11 and BME280 together just to satisfy this test.

### Standard profile

Connect the owned DHT11 breakout:

```text
DHT11 +   -> 3.3V
DHT11 OUT -> GPIO4
DHT11 -   -> GND
```

Use the breakout's existing pull-up only if it is already present/known from the previously validated fixture. Do not add a second strong parallel pull-up blindly. The Accepted contract requires a board pull-up footprint targeting an effective ~5.1 kOhm; **final population remains IHAP-55 scope** after the effective module network is measured/identified.

The BME280 must be disconnected for this profile.

### Precision profile

Disconnect the DHT11 and connect the accepted BME280 profile:

```text
BME280 VIN -> 3.3V
BME280 GND -> common GND
BME280 SDA -> GPIO6
BME280 SCL -> GPIO7
```

OLED and BME280 share the same I2C bus. The accepted specimen is expected at `0x76` with chip ID `0x60`.

The I2C validation firmware disables MCU internal pull-ups. Pull-ups supplied by the selected modules/prototype network therefore remain part of the actual physical path under test. The Accepted IHAP-50 contract requires I2C pull-up footprints with 4.7 kOhm as the candidate value; **final population/effective resistance remains IHAP-55 `[UNVALIDATED]` scope**.

## 5. Prepare the branch

```bash
git fetch origin
git switch ihap-50-interconnect-prototype-assembly
git pull --ff-only
git status
git rev-parse HEAD
```

Record the exact HEAD SHA. The runner requires it explicitly and stores it in local evidence.

## 6. Host tests

From repository root:

```bash
cd tools/hardware-validation/ihap-50-interconnect
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r host/requirements.txt
python -m unittest discover -s host/tests -v
```

All evaluator tests must pass before any reproduction/regression acquisition.

## 7. Build and flash

Use the project ESP-IDF environment and the ESP32-C3 target:

```bash
cd firmware
rm -rf build sdkconfig sdkconfig.old
idf.py set-target esp32c3
idf.py build
idf.py -p /dev/ttyACM0 flash
cd ..
```

`firmware/sdkconfig.defaults` pins `CONFIG_IDF_TARGET="esp32c3"` and the USB Serial/JTAG console as a regression guard from SR-50-03. The generated flash command must target `--chip esp32c3`.

Do not run `idf.py monitor` while the Python runner owns the serial port. If your device path differs, use the actual `/dev/ttyACM*` path consistently.

## 8. STANDARD profile reproduction

Canonical accepted evidence: **`IHAP50-STANDARD-11` — PASS**. Do not overwrite or reuse that run ID.

For a future regression/reproduction run, wire the common devices + DHT11 and keep BME280 disconnected. Use a new unique run ID:

```bash
HEAD_SHA="$(git rev-parse HEAD)"
python host/ihap50_run.py \
  --port /dev/ttyACM0 \
  --profile standard \
  --run-id IHAP50-STANDARD-<NEW-ID> \
  --commit "$HEAD_SHA"
```

The runner:

1. requires connector/polarity confirmation;
2. asks for one controlled `RST`;
3. verifies the exact pin map and spare-pin checks;
4. requires GPIO1 service TX to be disabled;
5. asks whether the OLED visibly flashed full-on for about one second at boot;
6. clears pre-condition serial input and collects six fresh baseline samples;
7. guides MC-38 FAR, NEAR and disconnected-wire phases, clearing queued samples at every confirmed boundary;
8. displays sequence numbers and generates local `summary.json`, `summary.md`, and raw `serial.log`.

Restore the disconnected MC-38 conductor after the test.

## 9. PRECISION profile reproduction

Canonical accepted evidence: **`IHAP50-PRECISION-01` — PASS**. Do not overwrite or reuse that run ID.

Power off, disconnect DHT11, connect BME280 to the shared OLED I2C bus, then use a new unique run ID:

```bash
HEAD_SHA="$(git rev-parse HEAD)"
python host/ihap50_run.py \
  --port /dev/ttyACM0 \
  --profile precision \
  --run-id IHAP50-PRECISION-<NEW-ID> \
  --commit "$HEAD_SHA"
```

The precision profile does not repeat the MC-38 phases. Accepted STANDARD-11 already supplies that physical evidence.

## 10. Automatic PASS criteria

Common:

- exact boot pin map;
- GPIO5 ADC-spare pull test PASS;
- GPIO10 digital-spare pull test PASS;
- radar service TX not configured;
- requested and detected environmental profile must match or the runner aborts before sampling;
- OLED visual transfer command PASS plus operator visual confirmation;
- OLED communication success in >=80% of baseline samples;
- radar fresh in >=75% of baseline samples;
- at least one valid LD2410C frame;
- zero parsed invalid LD2410C frames in the run baseline.

Standard:

- BME280 absent;
- DHT11 valid in >=75% of baseline samples;
- MC-38 FAR = 1 for both fresh phase samples;
- MC-38 NEAR = 0 for both fresh phase samples;
- one conductor disconnected = 1 for both fresh phase samples;
- OLED and radar remain alive during each door phase.

Precision:

- BME280 present at `0x76`;
- BME280 chip ID `0x60` in every collected baseline sample;
- BME280 communication success in >=80% of baseline samples;
- DHT11 result is ignored because DHT11 is intentionally absent.

Any failed criterion returns process exit code `2`; PASS returns `0`.

## 11. Accepted evidence and local raw data

Accepted curated evidence:

```text
docs/evidence/IHAP-50/IHAP50-STANDARD-11-summary.md
docs/evidence/IHAP-50/IHAP50-STANDARD-11-summary.json
docs/evidence/IHAP-50/IHAP50-PRECISION-01-summary.md
docs/evidence/IHAP-50/IHAP50-PRECISION-01-summary.json
```

Future/local runs are written below:

```text
tools/hardware-validation/ihap-50-interconnect/runs/<RUN-ID>/
```

That directory is ignored by Git. Raw serial output stays local by default. Do not commit raw serial logs automatically.

## 12. Stop conditions

Stop and correct wiring rather than weakening the gate if any of these occur:

- brownout/reset loop;
- OLED not found at the expected accepted address;
- unexpected BME280 presence in the standard profile;
- BME280 missing/wrong identity in the precision profile;
- radar frames invalid or absent;
- GPIO5/GPIO10 spare check failure;
- door state unstable or opposite to the accepted semantics;
- visible heating, smell, damaged insulation, or uncertain polarity.

Do not turn a failed physical result into a documentation PASS. Preserve the failure and remediate the actual cause.

## 13. Scope boundary after acceptance

IHAP-50 acceptance freezes the logical/reference interconnect contract and the physically validated prototype behavior. It **does not** promote the separately Proposed IHAP-56 strengthening, and it does not validate the final PCB, exact connector manufacturer/SKU/footprint, effective final pull-up population, enclosure harness lengths, power/source-transfer/thermal behavior, certification, production reliability or commercial readiness. Those remain downstream gates.
