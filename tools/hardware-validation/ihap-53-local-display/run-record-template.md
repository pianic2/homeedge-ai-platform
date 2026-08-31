# IHAP-53 Local Display Run Record

Do not overwrite a completed or invalidated run. Copy this template to `runs/<RUN-ID>/run-record.md` before starting the physical validation.

## Run identity

- Run ID:
- Evidence subject: `IHAP53-DISPLAY-OWNED-01`
- Date/time started:
- Operator:
- Git branch: `ihap-53-local-display-decision`
- Git commit SHA:
- ESP-IDF version:
- Host OS:
- Serial port:

## Hardware

- ESP32-C3 board:
- OLED observed marking: `GME12864-11-12-13 V3.22`
- OLED observed color: Blue
- Supply: `3.3 V`
- SDA: `GPIO5`
- SCL: `GPIO6`
- Wiring checked against canonical runbook before USB power: YES / NO
- Wiring deviation: NONE / describe

## Build and flash

- `idf.py set-target esp32c3`: PASS / FAIL
- `idf.py build`: PASS / FAIL
- flash: PASS / FAIL
- Notes:

## Probe and initialization

- `0x3C` ACK: YES / NO
- `0x3D` ACK: YES / NO
- Observed display address:
- Exactly one candidate address found: YES / NO
- SSD1306 initialization transfer: PASS / FAIL

## Short functional gate — visual observations

`PASS_TRANSFER` in the serial log is not sufficient by itself. Record what was actually visible.

- Full-screen ON: PASS / FAIL
  - complete active area illuminated: YES / NO
  - corruption/shift/crop observed: YES / NO
- Full-screen OFF: PASS / FAIL
  - complete active area off: YES / NO
  - residual/corrupt output observed: YES / NO
- Checkerboard: PASS / FAIL
  - complete active area covered: YES / NO
  - stable and correctly oriented: YES / NO
- Text card: PASS / FAIL
  - `HOMEEDGE` readable: YES / NO
  - `IHAP53` readable: YES / NO
  - border complete: YES / NO
  - orientation correct: YES / NO
- Stability mode started: YES / NO
- Short functional gate: PASS / FAIL

## 60-minute stability gate

- Stability start observed in serial log: YES / NO
- Highest valid `elapsed_s` before controlled reboot:
- Heartbeat at or beyond `elapsed_s >= 3600`: YES / NO
- Heartbeat cadence remained approximately 5 s: YES / NO
- Stability marker continued changing: YES / NO
- I2C transfer error observed: YES / NO
- Unexpected reset observed: YES / NO
- Brownout observed: YES / NO
- Frozen display observed: YES / NO
- Visible corruption observed: YES / NO
- Wiring changed during gate: YES / NO
- 60-minute stability gate: PASS / FAIL

## Controlled reboot / reinitialization gate

- One intentional ESP32-C3 reset performed after stability gate: YES / NO
- New boot sequence captured in same `serial.log`: YES / NO
- Same display address rediscovered: YES / NO
- SSD1306 initialization succeeded again: YES / NO
- Full visual sequence succeeded again: YES / NO
- Stability mode restarted: YES / NO
- Reboot/re-init gate: PASS / FAIL

## Evidence files

- `serial.log`: PRESENT / MISSING
- `photo-front-text-card.jpg`: PRESENT / MISSING
- `photo-rear-marking.jpg`: PRESENT / MISSING

## Final run classification

- Short gate: PASS / FAIL
- 60-minute stability: PASS / FAIL
- Reboot/re-init: PASS / FAIL
- Brownout/unexpected reset observed: YES / NO
- Visible corruption observed: YES / NO
- Controller conclusion: `SSD1306 validated` / `not validated`
- Overall physical validation: PASS / FAIL / INVALID

## Deviations, anomalies and notes

- Deviations from canonical runbook:
- Anomalies:
- Invalidating event, if any:
- Additional notes:

## Claim boundary

A PASS supports only the claims listed in `docs/evidence/IHAP-53/README.md`. It does not itself accept ADR-0003, finalize the product pinout, quantify display current/autonomy, approve enclosure mechanics, finalize BOM, or establish production/certification maturity.