# IHAP-50 — Integrated Interconnect Validation

**Issue:** IHAP-50 — Interconnect and Prototype Assembly Decision  
**Purpose:** lean physical gate for the proposed reference interconnect contract  
**Scope:** validation harness only; not product firmware, final PCB validation, or power-subsystem validation

## 1. What this gate proves

This harness checks the parts of IHAP-50 that cannot be closed by static review alone:

- the proposed ESP32-C3 pin allocation boots and remains recoverable;
- GPIO5 remains usable as the ADC-capable engineering spare and GPIO10 as a digital spare;
- OLED works on shared I2C GPIO6/GPIO7;
- BME280 can coexist with the OLED in the precision environmental profile;
- DHT11 works on GPIO4 in the standard environmental profile;
- LD2410C frames are received on GPIO0 at 256000 baud while GPIO1 service TX remains disabled;
- MC-38 produces HIGH/open, LOW/closed, and HIGH again with one conductor disconnected;
- connector pin order and polarity are explicitly reviewed by the operator.

It does **not** validate final PCB rail quality, source transfer, battery, charging, thermal behavior, enclosure, production reliability, or certification. Those remain downstream work.

## 2. Reference pin map under test

| Function | ESP32-C3 pin | Rule |
|---|---:|---|
| LD2410C TX -> MCU RX | GPIO0 | UART1 RX, 256000 baud |
| LD2410C RX service line | GPIO1 | **leave disconnected for this gate**; physical reservation only |
| MC-38 door sense | GPIO3 | external pull network required |
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

GPIO1 is reserved by the interconnect contract for a possible future controlled service TX path, but the IHAP-50 validation firmware intentionally does not configure a UART TX pin.

### OLED

```text
OLED GND -> common GND
OLED VCC -> 3.3V
OLED SCL -> GPIO7
OLED SDA -> GPIO6
```

The accepted owned display is expected at I2C address `0x3C`.

### MC-38

Validate the proposed external network rather than silently relying on an MCU internal pull-up:

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

The optional 100 nF filter footprint is **DNP** for this gate.

Expected states:

- magnet FAR / contact open -> `door_raw = 1`;
- magnet NEAR / contact closed -> `door_raw = 0`;
- one MC-38 conductor disconnected -> `door_raw = 1`.

The last condition intentionally demonstrates that the simple MVP topology cannot distinguish a legitimate open contact from an interrupted wire.

## 4. Environmental profiles

The two accepted environmental profiles are alternatives. Do **not** mount DHT11 and BME280 together just to satisfy this test.

### Standard profile

Connect the owned DHT11 breakout:

```text
DHT11 +   -> 3.3V
DHT11 OUT -> GPIO4
DHT11 -   -> GND
```

Use the breakout's existing pull-up only if it is already present/known from the previously validated fixture. Do not add a second strong parallel pull-up blindly. The reference PCB keeps a ~5.1 kOhm pull-up footprint and IHAP-55 must reconcile the effective network before population.

The BME280 must be disconnected for this run.

### Precision profile

Disconnect the DHT11 and connect the accepted BME280 profile:

```text
BME280 VIN -> 3.3V
BME280 GND -> common GND
BME280 SDA -> GPIO6
BME280 SCL -> GPIO7
```

OLED and BME280 share the same I2C bus. The accepted specimen is expected at `0x76` with chip ID `0x60`.

The I2C validation firmware disables MCU internal pull-ups. Pull-ups supplied by the selected modules/prototype network therefore remain part of the actual physical path under test. IHAP-55 must still reconcile exact effective pull-up resistance for the final PCB population.

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

All evaluator tests must pass before physical acquisition.

## 7. Build and flash

Use the project ESP-IDF environment and the ESP32-C3 target:

```bash
cd firmware
idf.py set-target esp32c3
idf.py build
idf.py -p /dev/ttyACM0 flash
cd ..
```

Do not run `idf.py monitor` while the Python runner owns the serial port.

If your device path differs, use the actual `/dev/ttyACM*` path consistently.

## 8. Run STANDARD

Wire the common devices + DHT11. Keep BME280 disconnected.

```bash
HEAD_SHA="$(git rev-parse HEAD)"
python host/ihap50_run.py \
  --port /dev/ttyACM0 \
  --profile standard \
  --run-id IHAP50-STANDARD-01 \
  --commit "$HEAD_SHA"
```

The runner will:

1. require connector/polarity confirmation;
2. ask for one controlled `RST`;
3. verify the exact pin map and spare-pin checks;
4. require GPIO1 service TX to be disabled;
5. ask whether the OLED visibly flashed full-on for about one second at boot;
6. collect six baseline samples (~30 s);
7. guide MC-38 FAR, NEAR and disconnected-wire phases, two samples each;
8. generate local `summary.json` and `summary.md` plus raw `serial.log`.

Restore the disconnected MC-38 conductor after the test.

## 9. Run PRECISION

Power off, disconnect DHT11, connect BME280 to the shared OLED I2C bus, then power/flash as needed and run:

```bash
HEAD_SHA="$(git rev-parse HEAD)"
python host/ihap50_run.py \
  --port /dev/ttyACM0 \
  --profile precision \
  --run-id IHAP50-PRECISION-01 \
  --commit "$HEAD_SHA"
```

The precision run does not repeat the MC-38 phases. It validates the alternative BME280 profile and OLED coexistence without duplicating physical work already covered by the standard run.

## 10. Automatic PASS criteria

Common:

- exact boot pin map;
- GPIO5 ADC-spare pull test PASS;
- GPIO10 digital-spare pull test PASS;
- radar service TX not configured;
- OLED visual transfer command PASS plus operator visual confirmation;
- OLED communication success in >=80% of baseline samples;
- radar fresh in >=75% of baseline samples;
- at least one valid LD2410C frame;
- zero parsed invalid LD2410C frames in the run baseline.

Standard:

- BME280 absent;
- DHT11 valid in >=75% of baseline samples;
- MC-38 FAR = 1 for both samples;
- MC-38 NEAR = 0 for both samples;
- one conductor disconnected = 1 for both samples;
- OLED and radar remain alive during each door phase.

Precision:

- BME280 present at `0x76`;
- BME280 chip ID `0x60` in every collected baseline sample;
- BME280 communication success in >=80% of baseline samples;
- DHT11 result is ignored because DHT11 is intentionally absent.

Any failed criterion returns process exit code `2`; PASS returns `0`.

## 11. Evidence handling

Runs are written below:

```text
tools/hardware-validation/ihap-50-interconnect/runs/<RUN-ID>/
```

That directory is ignored by Git. Raw serial output stays local by default.

After both runs, provide only the two `summary.json` / `summary.md` files for review unless a failure requires deeper raw-log inspection. Do not commit raw serial logs automatically.

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
