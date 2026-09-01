# IHAP-53 Local Display Run Record

Do not overwrite a completed or invalidated run. This record documents the completed physical validation run `IHAP53-DISPLAY-01`.

## Run identity

- Run ID: `IHAP53-DISPLAY-01`
- Evidence subject: `IHAP53-DISPLAY-OWNED-01`
- Date/time started: `2026-08-31` — exact wall-clock start time not recorded in the supplied evidence
- Operator: Project Owner / physical test operator
- Git branch: `ihap-53-local-display-decision`
- Git commit SHA: `2dc4b1d53f8069ca1fa7fb840c9edacf0f102085`
- ESP-IDF version: `v6.0.1`
- Host OS: Linux
- Serial port: `/dev/ttyACM0`

## Hardware

- ESP32-C3 board: ESP32-C3 board accepted by ADR-0001; boot log reports chip revision `v0.4`
- OLED observed marking: `GME12864-11-12-13 V3.22`
- OLED observed color: Blue
- Supply: `3.3 V`
- SDA: `GPIO5`
- SCL: `GPIO6`
- Wiring checked against canonical runbook before USB power: YES
- Wiring deviation: NONE
- Observed jumper-wire mapping:
  - black -> `GND`
  - red -> `3.3V`
  - orange -> `SCL`
  - yellow -> `SDA`

## Build and flash

- `idf.py set-target esp32c3`: PASS
- `idf.py build`: PASS
- flash: PASS
- Notes:
  - The executed application identifies itself as `ihap53_local_display_harness`.
  - Boot log reports application version `2dc4b1d` and ESP-IDF `v6.0.1`.
  - The bootloader reports a detected 4096 KiB flash device while the binary image header is configured for 2048 KiB. ESP-IDF explicitly continues using the 2048 KiB image-header size. This warning did not affect the IHAP-53 display validation and is not treated as an invalidating event.

## Probe and initialization

- `0x3C` ACK: YES
- `0x3D` ACK: NO
- Observed display address: `0x3C`
- Exactly one candidate address found: YES
- SSD1306 initialization-profile transfer: PASS

## Short functional gate — visual observations

`PASS_TRANSFER` in the serial log is not sufficient by itself. The serial evidence is combined with the operator's direct visual observations.

- Full-screen ON: PASS
  - complete active area illuminated: YES
  - corruption/shift/crop observed: NO
- Full-screen OFF: PASS
  - complete active area off: YES
  - residual/corrupt output observed: NO
- Checkerboard: PASS
  - complete active area covered: YES
  - stable and correctly oriented: YES
- Text card: PASS
  - `HOMEEDGE` readable: YES
  - `IHAP53` readable: YES
  - border complete: YES
  - orientation correct: YES
- Stability mode started: YES
- Short functional gate: PASS

Operator observation: the test screen remained correctly rendered and readable. The moving stability pixel/marker functioned correctly.

## 60-minute stability gate

- Stability start observed in serial log: YES
- Highest valid `elapsed_s` before controlled reboot: `3622`
- Heartbeat at or beyond `elapsed_s >= 3600`: YES
- Heartbeat cadence remained approximately 5 s: YES
- Stability marker continued changing: YES
- I2C transfer error observed: NO
- Unexpected reset observed: NO
- Brownout observed: NO
- Frozen display observed: NO
- Visible corruption observed: NO
- Wiring changed during gate: NO
- 60-minute stability gate: PASS

Evidence review notes:

- The first stability sequence starts after the short functional gate and reaches heartbeat cycle `709` at `elapsed_s=3622`, all reported with `result="PASS"`.
- No firmware `FAIL`, I2C transfer error, brownout indication or unplanned boot sequence is present before the controlled reboot.
- The operator confirms that the display stayed functional for the full interval and that the moving stability marker continued operating.

## Controlled reboot / reinitialization gate

- One intentional ESP32-C3 reset performed after stability gate: YES
- New boot sequence captured in same `serial.log`: YES
- Same display address rediscovered: YES
- SSD1306 initialization-profile transfer succeeded again: YES
- Full visual sequence succeeded again: YES
- Stability mode restarted: YES
- Reboot/re-init gate: PASS

Post-reset evidence:

- display rediscovered at `0x3C`;
- `0x3D` remained non-responsive;
- SSD1306 initialization-profile transfer returned `PASS`;
- full-on, full-off, checkerboard and text-card transfers all returned `PASS_TRANSFER`;
- short functional gate returned `PASS_TRANSFER`;
- stability mode restarted and produced successful heartbeat records;
- the operator confirms that the expected test text remained visible and correct after reboot.

## Evidence files

Raw/local evidence:

- `serial.log`: PRESENT — retained in the ignored local run and not committed by default.

Published repository evidence:

- `photo-front-text-card.png`: PRESENT
- `photo-rear-marking.png`: PRESENT
- `photo-wiring-annotated.png`: PRESENT
- `run-record.md`: PRESENT

The required publication package is complete for the reviewed run.

## Final run classification

- Short gate: PASS
- 60-minute stability: PASS
- Reboot/re-init: PASS
- Brownout/unexpected reset observed: NO
- Visible corruption observed: NO
- Controller conclusion: `SSD1306 command/profile compatibility validated for the tested specimen; exact physical controller identity not independently proven`
- Overall physical validation: **PASS**

## Deviations, anomalies and notes

- Deviations from canonical runbook: NONE affecting the physical validation.
- Anomalies:
  - ESP-IDF boot warning: physical flash detected as 4096 KiB while the firmware image header uses 2048 KiB. Non-blocking for IHAP-53.
  - After the required reboot/reinitialization gate had already completed successfully, `idf_monitor` emitted host-side serial write-timeout warnings and later a read/no-data disconnect/thread exception. The required post-reset boot, address probe, SSD1306 initialization-profile transfer, visual sequence, stability restart and subsequent PASS heartbeats had already been captured. No I2C `FAIL`, brownout, display corruption or second boot sequence accompanies this host-monitor anomaly.
- Invalidating event, if any: NONE.
- Additional notes:
  - The operator visually confirmed correct display behavior throughout the one-hour run.
  - The moving stability pixel/marker operated correctly.
  - The display remained readable and correctly initialized after the intentional reboot.
  - The test validates the owned specimen under the documented 3.3 V wiring only.
  - The publication package includes the required rear PCB photograph and annotated wiring photograph.

## Independent evidence review

The supplied `serial.log`, published photographs and operator observations support a **PASS** classification for the physical validation:

1. exactly one I2C candidate responded (`0x3C`);
2. the SSD1306 initialization command/profile used by the harness succeeded;
3. all four visual transfers passed and visual correctness was confirmed by the operator;
4. the first stability run exceeded the 3600-second threshold and reached `3622 s`;
5. all recorded first-run heartbeats report `PASS`;
6. no brownout, I2C failure or unexpected reboot is evidenced during the one-hour gate;
7. the intentional reboot was followed by successful rediscovery at the same address, reinitialization, full visual-sequence execution and restart of stability mode;
8. the operator independently observed correct screen content and the moving stability marker.

The later host-monitor disconnect occurs after the required reboot/reinitialization evidence was already collected and is classified as a non-invalidating capture/monitor anomaly, not as evidence of display failure.

The run does not independently prove the physical controller die identity, seller/lot provenance, universal module compatibility, quantitative current consumption, final bus wiring or enclosure suitability.

## Claim boundary

A PASS supports only the claims listed in `docs/evidence/IHAP-53/README.md`. It does not itself accept ADR-0004, finalize the product pinout, quantify display current/autonomy, approve enclosure mechanics, finalize BOM, or establish production/certification maturity.
