# IHAP-53 Local Display Evidence and Physical Validation Runbook

**Issue:** IHAP-53 — Local Display Decision — 0.96-inch OLED vs No Display  
**Status:** physical validation PASS; ADR-0004 remains `Proposed` pending explicit Project Owner acceptance  
**Human entrypoint:** this file  
**Validation harness:** `tools/hardware-validation/ihap-53-local-display/`  
**Raw evidence location:** `tools/hardware-validation/ihap-53-local-display/runs/<RUN-ID>/` — local only, do not commit raw runs  
**Published evidence:** `docs/evidence/IHAP-53/IHAP53-DISPLAY-01/`  
**Purpose:** qualify the owned 0.96-inch OLED candidate with a reproducible procedure without turning IHAP-53 into a final firmware implementation task.

> Do not rely on chat history for execution. If an instruction needed to execute or interpret IHAP-53 is missing from this file or from a file linked by this file, stop the run and correct the repository documentation on the existing IHAP-53 branch/PR before continuing.

## Validated result — IHAP53-DISPLAY-01

The controlled physical run completed with **PASS**.

Validated for the tested owned specimen only:

- observed I2C address: `0x3C`;
- `0x3D` did not acknowledge;
- SSD1306 command/data profile used by the harness: functionally compatible;
- 128×64 full-area rendering and text card: visually correct by operator observation;
- stability: heartbeat reached `elapsed_s=3622`, beyond the required 3600 seconds;
- no invalidating I2C failure, brownout, unexpected reset, frozen display or visible corruption during the one-hour gate;
- controlled reboot/reinitialization: PASS;
- tested supply: ESP32-C3 `3.3V`.

Published review evidence:

- [`IHAP53-DISPLAY-01/run-record.md`](IHAP53-DISPLAY-01/run-record.md)
- [`IHAP53-DISPLAY-01/photo-front-text-card.png`](IHAP53-DISPLAY-01/photo-front-text-card.png)
- [`IHAP53-DISPLAY-01/photo-rear-marking.png`](IHAP53-DISPLAY-01/photo-rear-marking.png)
- [`IHAP53-DISPLAY-01/photo-wiring-annotated.png`](IHAP53-DISPLAY-01/photo-wiring-annotated.png)

The PASS does **not** independently identify the physical controller die, seller/lot provenance, onboard regulator or pull-up implementation, quantitative current consumption, final product wiring, enclosure suitability or universal compatibility of similarly marked modules.

---

## 1. What you need

### Hardware

- the ESP32-C3 board accepted by ADR-0001;
- the owned blue 0.96-inch-class OLED marked `GME12864-11-12-13 V3.22`;
- four female/female or otherwise appropriate jumper wires;
- one USB **data** cable suitable for the ESP32-C3 board;
- a PC capable of building/flashing ESP-IDF firmware;
- stable PC USB power for the validation run;
- a camera/phone for the two required evidence photographs.

No multimeter, external power supply, logic analyzer, external level shifter, external I2C pull-up or 5 V display test is required by IHAP-53.

### Software

Reference toolchain for this run:

- Git;
- **ESP-IDF v6.0.1** with ESP32-C3 support;
- a terminal capable of saving the monitor output to a file.

Official ESP-IDF v6.0.1 ESP32-C3 setup documentation:

<https://docs.espressif.com/projects/esp-idf/en/v6.0.1/esp32c3/get-started/index.html>

Before testing, run:

```bash
idf.py --version
```

Expected reference version:

```text
ESP-IDF v6.0.1
```

If another ESP-IDF version is used, record it as a deviation in `run-record.md`. Do not silently treat a different version as the reference environment.

---

## 2. Claim classification

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

The owned specimen is **consistent with** the GoldenMorning `-12` family description. Physical validation demonstrates compatibility with the SSD1306 command/data profile used by the harness, but does not independently prove exact controller die identity, seller provenance, exact PCB-revision correspondence, onboard pull-up/regulator implementation or electrical characteristics beyond the tested 3.3 V functional behavior.

---

## 3. Validation subject

| Field | Value |
|---|---|
| Evidence ID | `IHAP53-DISPLAY-OWNED-01` |
| Observed marking | `GME12864-11-12-13 V3.22` |
| Observed color | Blue |
| Candidate family | `GME12864-12` — consistent with family evidence; exact provenance `[UNVALIDATED]` |
| Controller profile | SSD1306 command/data profile — functionally validated for tested specimen; exact die identity `[UNVALIDATED]` |
| Interface | I2C — validated for tested specimen |
| Observed address | `0x3C` |
| Validation supply | ESP32-C3 `3.3V` — functional PASS for tested specimen |
| Status before run | `[UNVALIDATED]` |
| Status after run | `PASS` within documented claim boundary |

---

## 4. Check out the exact IHAP-53 work

Use the existing task branch and PR. Do not create another IHAP-53 branch or PR.

If the repository is not present locally:

```bash
git clone https://github.com/pianic2/homeedge-ai-platform.git
cd homeedge-ai-platform
git fetch origin pull/31/head:ihap-53-local-display-decision
git switch ihap-53-local-display-decision
```

If the repository already exists locally:

```bash
cd homeedge-ai-platform
git fetch origin
git switch ihap-53-local-display-decision
git pull --ff-only origin ihap-53-local-display-decision
```

Before the run, execute:

```bash
git status
git rev-parse HEAD
```

Requirements:

- branch must be `ihap-53-local-display-decision`;
- working tree must contain no unintended local modifications;
- record the exact `git rev-parse HEAD` value in the run record.

Do not hard-code an old commit SHA into the procedure: the branch may legitimately advance with review/documentation corrections before the physical run. The exact run commit belongs in the evidence.

---

## 5. Create the local evidence run

The first controlled run ID is:

```text
IHAP53-DISPLAY-01
```

From repository root:

```bash
mkdir -p tools/hardware-validation/ihap-53-local-display/runs/IHAP53-DISPLAY-01
cp tools/hardware-validation/ihap-53-local-display/run-record-template.md \
  tools/hardware-validation/ihap-53-local-display/runs/IHAP53-DISPLAY-01/run-record.md
```

All raw evidence for this attempt stays together in:

```text
tools/hardware-validation/ihap-53-local-display/runs/IHAP53-DISPLAY-01/
```

Expected local structure after completion:

```text
IHAP53-DISPLAY-01/
├── run-record.md
├── serial.log
├── photo-front-text-card.jpg
└── photo-rear-marking.jpg
```

If the run becomes invalid for any reason, **do not overwrite or delete it**. Preserve it and use the next progressive run ID, for example `IHAP53-DISPLAY-02`.

Raw runs are laboratory evidence and are not committed by default.

---

## 6. Wiring for the validation harness

This is validation wiring, **not** the final IHAP-50 pinout.

Disconnect USB power before changing wiring.

| OLED pin | ESP32-C3 |
|---|---|
| `GND` | `GND` |
| `VCC` | `3.3V` |
| `SDA` | GPIO5 |
| `SCL` | GPIO6 |

Rules:

1. Confirm the labels on the physical OLED before connecting each wire.
2. Use **3.3 V only** for IHAP-53 qualification.
3. Use one common ground.
4. Do not use GPIO2.
5. Do not add an external level shifter.
6. Do not add or change I2C pull-ups unless the preflight cannot communicate.
7. If wiring changes after the run starts, invalidate that attempt, record the reason and start a new run ID.
8. Take the required rear photograph after wiring identification is clear enough to show the PCB marking and pin labels.

Before applying USB power, compare the physical wiring against the table a second time.

---

## 7. Build and flash

From repository root, activate the ESP-IDF v6.0.1 environment according to the official Espressif documentation, then run:

```bash
cd tools/hardware-validation/ihap-53-local-display/firmware
idf.py --version
idf.py set-target esp32c3
idf.py build
```

Identify the ESP32-C3 serial port on the host. On Linux it commonly appears under `/dev/ttyACM*` or `/dev/ttyUSB*`; do not assume the example path is correct.

Then flash using the actual port:

```bash
idf.py -p /dev/ttyACM0 flash
```

Replace `/dev/ttyACM0` when the actual port differs.

Record in `run-record.md`:

- ESP-IDF version;
- Git commit SHA;
- serial port;
- build result;
- flash result;
- any deviation.

Do not start the controlled run if build or flash fails.

---

## 8. Capture the complete serial evidence

The serial stream must be saved, not only observed on screen.

From the firmware directory, on Linux/macOS:

```bash
idf.py -p /dev/ttyACM0 monitor 2>&1 | tee ../runs/IHAP53-DISPLAY-01/serial.log
```

Replace the port and run ID when necessary.

The terminal should now both display and save the complete monitor output.

Do not truncate `serial.log` between the short functional gate and the 60-minute stability gate. The same log must also contain the controlled reboot/reinitialization sequence.

If the monitor/capture command fails, treat the attempt as an evidence-capture failure and correct the procedure before continuing.

---

## 9. Short functional gate

The harness must complete these stages in order:

1. I2C probe finds exactly one candidate display at `0x3C` or `0x3D`.
2. SSD1306 candidate initialization succeeds.
3. full-screen ON test is visibly correct;
4. full-screen OFF test is visibly correct;
5. checkerboard test is visibly stable and covers the complete display area;
6. the static `HOMEEDGE` / `IHAP53` text card is readable, complete and correctly oriented;
7. stability mode starts and heartbeat records begin.

The firmware emits structured records such as:

```text
{"event":"probe",...}
{"event":"gate",...}
{"event":"visual",...}
{"event":"heartbeat",...}
```

`PASS_TRANSFER` means the I2C transfer returned successfully. **Visual correctness remains an operator observation** and must be recorded separately in `run-record.md`.

Reject the run if:

- neither `0x3C` nor `0x3D` acknowledges;
- both candidate addresses unexpectedly acknowledge without an explained second device;
- initialization or framebuffer transfer returns an I2C error;
- visible output is shifted, cropped, mirrored unexpectedly, corrupted or blank;
- the ESP32-C3 repeatedly resets or reports brownout;
- the display becomes unstable during the run.

A failed SSD1306-profile test does **not** prove the module is defective. It means the candidate profile has not been validated and must be investigated before ADR acceptance.

When the static text card is visible and correct, save:

```text
runs/<RUN-ID>/photo-front-text-card.jpg
```

The image must clearly show the complete active display area and readable `HOMEEDGE` / `IHAP53` text.

---

## 10. One-hour stability gate

Only continue when the short functional gate is valid.

1. Leave the same wiring unchanged.
2. Leave the same monitor/log capture running.
3. Run continuously for at least **60 minutes** from the emitted `stability` start event.
4. Do not power-cycle or reconnect the display.
5. Verify that a heartbeat continues approximately every 5 seconds.
6. Verify that the on-screen stability marker continues changing.
7. Reject the run for any I2C transfer error, unexpected reset, brownout, frozen/corrupted display or manual rewiring.

The harness currently runs continuously and does not stop automatically at 60 minutes. The acceptance point is demonstrated by a valid heartbeat with `elapsed_s >= 3600` and no invalidating event since the stability start.

This is a functional stability check, not lifetime/endurance certification.

Record the observed stability outcome in `run-record.md`.

---

## 11. Reboot / reinitialization gate

After a valid heartbeat at or beyond 3600 seconds:

1. Keep the serial monitor and `tee` capture running.
2. Press the ESP32-C3 `RST` button **once**.
3. Do not change wiring.
4. Confirm the harness emits a new boot sequence.
5. Confirm it probes the same display address again.
6. Confirm SSD1306-profile initialization succeeds again.
7. Confirm the full visual sequence is correct again.
8. Confirm stability mode starts again.

Do not perform repeated resets unless a new diagnostic run is explicitly required.

After the reinitialization sequence has been captured successfully, stop the monitor normally (`Ctrl+]` in the ESP-IDF monitor; if the active monitor shows a different quit key, use the key printed by that monitor).

Record the reboot/re-init outcome in `run-record.md`.

---

## 12. Required evidence before review

The local run directory must contain:

### `run-record.md`

Must identify:

- run ID;
- subject/evidence ID;
- Git branch and exact commit SHA;
- ESP-IDF version;
- host serial port;
- validation supply;
- observed I2C address;
- build and flash result;
- short functional gate result;
- visual observations for full-on/full-off/checkerboard/text card;
- 60-minute stability result;
- highest observed `elapsed_s` before reboot;
- reboot/reinitialization result;
- brownout/unexpected reset observation;
- visible corruption observation;
- controller/profile compatibility conclusion;
- deviations/anomalies/notes.

### `serial.log`

Must contain one continuous evidence stream covering:

- initial boot;
- probe;
- SSD1306-profile initialization;
- complete short visual sequence;
- stability start;
- heartbeat at or beyond 3600 seconds;
- the single controlled reset;
- successful post-reset probe/init/visual sequence and restart of stability mode.

### `photo-front-text-card.jpg`

Must show the complete display while the `HOMEEDGE` / `IHAP53` text card is visible.

### `photo-rear-marking.jpg`

Must show enough of the rear/PCB side to identify the specimen marking and address-select markings.

Before any photograph is committed to the repository it must be cropped to the component, converted to a standard image format when needed and stripped of EXIF metadata. Do not publish workstation paths, network credentials, SSIDs, MAC addresses or unique chip identifiers.

Published sanitized evidence may use PNG names defined by `publication-guide.md`.

---

## 13. Acceptance record

Use the repository template:

`tools/hardware-validation/ihap-53-local-display/run-record-template.md`

Do not use an acceptance record copied from chat.

The physical test does not itself change ADR status. `IHAP53-DISPLAY-01` is a complete PASS and creates evidence for Project Owner review; **ADR-0004 remains `Proposed` until the Project Owner explicitly accepts the decision**.

---

## 14. What a PASS supports

A complete PASS supports only these owned-specimen claims:

- the specimen communicates on the observed I2C address under the tested wiring;
- the SSD1306 command/data profile used by the harness is functionally compatible;
- 128×64 full-area rendering and simple text output work;
- repeated updates remain functional for the one-hour run;
- the display reinitializes after one controlled ESP32-C3 reset;
- the tested specimen operates from the 3.3 V validation supply.

It does not prove:

- exact physical controller die identity;
- universal compatibility of every `GME12864-11/12/13` board;
- seller or lot reproducibility;
- final product wiring;
- final pull-up values;
- current consumption or autonomy;
- enclosure visibility or mechanical durability;
- production, safety, security or certification maturity.

Quantitative power remains IHAP-49; final interconnect remains IHAP-50; enclosure remains IHAP-51.

---

## 15. Stop conditions and correction rule

Stop and correct the existing IHAP-53 repository documentation/harness before proceeding when any of these is true:

- a required step is ambiguous;
- the physical board labels do not match the documented wiring assumptions;
- the expected command does not work in the reference environment;
- required evidence cannot be captured exactly as documented;
- the firmware behavior differs from this runbook;
- a test result cannot be classified without relying on chat history;
- a change to wiring, firmware, toolchain or acceptance criteria is required.

Corrections remain on branch `ihap-53-local-display-decision` and PR #31. Preserve invalid attempts under their original run IDs.
