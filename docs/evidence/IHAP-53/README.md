# IHAP-53 Local Display Evidence

**Issue:** IHAP-53 — Local Display Decision — 0.96-inch OLED vs No Display  
**Status:** pre-validation; owned specimen not yet qualified  
**Purpose:** record the smallest reproducible evidence required to qualify the owned 0.96-inch OLED candidate without turning IHAP-53 into a firmware project

## 1. Claim classification

### Physical observations

For the owned specimen:

- blue 0.96-inch-class OLED appearance;
- four pins labelled `GND`, `VCC`, `SCL`, `SDA`;
- PCB marking `GME12864-11-12-13 V3.22`;
- address-selection marking `0x3C` / `0x3D`.

These observations apply to one specimen only.

### Primary-source family evidence

GoldenMorning documents the `GME12864-11/12/13` module family as:

- 0.96 inch;
- 128×64;
- monochrome OLED;
- four-pin I2C;
- SSD1306 controller;
- `GME12864-12` as the blue variant;
- 3.3–5 V module supply range.

Source: <https://goldenmorninglcd.com/oled-display-module/0.96-inch-128x64-ssd1306-gme12864-11/>

Solomon Systech documents SSD1306 as a 128×64 monochrome OLED controller with I2C support and an internal charge pump.

Source: <https://www.solomon-systech.com/en/product/SSD1306>

The owned specimen is **consistent with** the GoldenMorning `-12` family description, but seller provenance, exact PCB-revision correspondence, onboard pull-ups/regulator implementation and electrical behavior remain `[UNVALIDATED]` until the protocol below passes.

## 2. Validation subject

| Field | Value |
|---|---|
| Evidence ID | `IHAP53-DISPLAY-OWNED-01` |
| Observed marking | `GME12864-11-12-13 V3.22` |
| Observed color | Blue |
| Candidate family | `GME12864-12` — conditional |
| Candidate controller | SSD1306 — conditional |
| Expected interface | I2C |
| Expected address | `0x3C` reference; `0x3D` accepted if physically configured |
| Validation supply | ESP32-C3 `3.3V` only |
| Status before run | `[UNVALIDATED]` |

## 3. Wiring for the validation harness

This is validation wiring, **not** the final IHAP-50 pinout.

| OLED pin | ESP32-C3 |
|---|---|
| `GND` | `GND` |
| `VCC` | `3.3V` |
| `SDA` | GPIO5 |
| `SCL` | GPIO6 |

Rules:

1. Disconnect USB power before changing wiring.
2. Use 3.3 V for this qualification; do not test 5 V as part of IHAP-53.
3. Use one common ground.
4. Do not use GPIO2.
5. Do not add an external level shifter.
6. Do not add or change I2C pull-ups unless the preflight cannot communicate; if wiring must change, record it and restart the run.

## 4. Build and flash

Prerequisites:

- ESP-IDF with ESP32-C3 support;
- the ESP32-C3 board accepted by ADR-0001;
- USB data cable connected directly to the PC.

Commands:

```bash
cd tools/hardware-validation/ihap-53-local-display/firmware
idf.py set-target esp32c3
idf.py build
idf.py -p /dev/ttyACM0 flash monitor
```

Use the actual serial port if it differs from `/dev/ttyACM0`.

The harness is validation tooling only. It does not implement the final HomeEdge display firmware or freeze product GPIO assignments.

## 5. Short functional gate

The harness must complete these stages in order:

1. I2C probe finds exactly one candidate display at `0x3C` or `0x3D`.
2. SSD1306 candidate initialization succeeds.
3. full-screen ON test is visibly correct;
4. full-screen OFF test is visibly correct;
5. checkerboard test is visibly stable and covers the complete display area;
6. the static `HOMEEDGE` / `IHAP53` text card is readable and correctly oriented;
7. stability mode starts and emits serial heartbeat records.

Reject the run if:

- neither `0x3C` nor `0x3D` acknowledges;
- both candidate addresses unexpectedly acknowledge without an explained second device;
- initialization or framebuffer transfer returns an I2C error;
- visible output is shifted, cropped, mirrored unexpectedly, corrupted or blank;
- the ESP32-C3 repeatedly resets or reports brownout;
- the display becomes unstable during the run.

A failed SSD1306 test does **not** prove the module is defective. It means the candidate controller/profile has not been validated and must be investigated before ADR acceptance.

## 6. One-hour stability gate

After the short gate passes:

1. leave the same wiring unchanged;
2. leave the harness running for **60 minutes**;
3. do not power-cycle or reconnect the display;
4. verify that a heartbeat continues approximately every 5 seconds;
5. verify that the on-screen stability marker continues changing;
6. reject the run for any I2C transfer error, unexpected reset, brownout, frozen/corrupted display or manual rewiring.

This is a functional stability check, not lifetime/endurance certification.

## 7. Reboot / reinitialization gate

After the one-hour gate:

1. press `RST` once;
2. do not change wiring;
3. confirm the harness probes the same address again;
4. confirm the initialization and visual test sequence repeats successfully;
5. confirm stability mode starts again.

## 8. Evidence to return

Keep the evidence compact. Provide:

- the complete serial log from boot through the short functional gate;
- the final serial section showing at least the last stability heartbeat before the 60-minute mark;
- the serial section after the single reboot;
- one front photograph while the text card is displayed;
- one rear photograph showing PCB marking and pin labels.

Before repository publication, photographs must be cropped to the component, converted to a standard image format when needed and stripped of EXIF metadata. Do not publish workstation paths, network credentials, SSIDs, MAC addresses or unique chip identifiers.

## 9. Acceptance record template

```text
Run ID: IHAP53-DISPLAY-01
Subject: IHAP53-DISPLAY-OWNED-01
Supply: 3.3 V
Observed address: 0x__
Short gate: PASS / FAIL
60-minute stability: PASS / FAIL
Reboot/re-init: PASS / FAIL
Brownout/reset observed: YES / NO
Visible corruption observed: YES / NO
Controller conclusion: SSD1306 validated / not validated
Notes:
```

## 10. What a PASS supports

A complete PASS supports only these owned-specimen claims:

- the specimen communicates on the observed I2C address under the tested wiring;
- the SSD1306 command/data profile used by the harness is functionally compatible;
- 128×64 full-area rendering and simple text output work;
- repeated updates remain functional for the one-hour run;
- the display reinitializes after one controlled ESP32-C3 reset;
- the tested specimen operates from the 3.3 V validation supply.

It does not prove:

- universal compatibility of every `GME12864-11/12/13` board;
- seller or lot reproducibility;
- final product wiring;
- final pull-up values;
- current consumption or autonomy;
- enclosure visibility or mechanical durability;
- production, safety, security or certification maturity.

Quantitative power remains IHAP-49; final interconnect remains IHAP-50; enclosure remains IHAP-51.
