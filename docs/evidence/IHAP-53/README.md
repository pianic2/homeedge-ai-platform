# IHAP-53 Local Display Evidence and Physical Validation Runbook

**Issue:** IHAP-53 — Local Display Decision — 0.96-inch OLED vs No Display  
**ADR:** [`ADR-0004 — Local Status Display`](../../adr/ADR-0004-local-status-display.md)  
**Status:** physical validation **PASS**; ADR-0004 **Accepted** by the Project Owner on 2026-08-31  
**Human entrypoint:** this file  
**Validation harness:** `tools/hardware-validation/ihap-53-local-display/`  
**Raw evidence location:** `tools/hardware-validation/ihap-53-local-display/runs/<RUN-ID>/` — local only, do not commit raw runs  
**Published evidence:** `docs/evidence/IHAP-53/IHAP53-DISPLAY-01/`  
**Purpose:** document and reproduce qualification of the owned 0.96-inch OLED without turning IHAP-53 into final room-node firmware implementation.

> Do not rely on chat history for execution. If an instruction needed to execute or interpret IHAP-53 is missing from this file or a file linked by it, stop the run and correct the repository documentation on the existing IHAP-53 branch/PR before continuing.

---

## Validated result — IHAP53-DISPLAY-01

The controlled physical run completed with **PASS**.

Validated for the tested owned specimen only:

- observed I2C address: `0x3C`;
- `0x3D` did not acknowledge;
- SSD1306 command/data profile used by the harness: functionally compatible;
- 128×64 full-area rendering and `HOMEEDGE / IHAP53` text card: visually correct by operator observation;
- stability heartbeat reached `elapsed_s=3622`, beyond the required 3600 seconds;
- no invalidating I2C failure, brownout, unexpected reset, frozen display or visible corruption during the one-hour gate;
- controlled reboot/reinitialization: PASS;
- tested supply: ESP32-C3 `3.3V`;
- moving stability marker: confirmed by the operator.

Published reviewed evidence:

- [`IHAP53-DISPLAY-01/run-record.md`](IHAP53-DISPLAY-01/run-record.md)
- [`IHAP53-DISPLAY-01/photo-front-text-card.png`](IHAP53-DISPLAY-01/photo-front-text-card.png)
- [`IHAP53-DISPLAY-01/photo-rear-marking.png`](IHAP53-DISPLAY-01/photo-rear-marking.png)
- [`IHAP53-DISPLAY-01/photo-wiring-annotated.png`](IHAP53-DISPLAY-01/photo-wiring-annotated.png)
- [`final-review-summary.md`](final-review-summary.md)

The PASS does **not** independently identify the physical controller die, seller/lot provenance, onboard regulator or pull-up implementation, quantitative current consumption, final product wiring, enclosure suitability or universal compatibility of similarly marked modules.

ADR-0004 acceptance makes the **local status display profile** an MVP architectural requirement. It does not convert the validation harness into final firmware or close IHAP-49, IHAP-50, IHAP-51 or IHAP-17 follow-up work.

---

## 1. Required hardware and software

### Hardware

- ESP32-C3 board accepted by ADR-0001;
- owned blue OLED marked `GME12864-11-12-13 V3.22`;
- four suitable jumper wires;
- USB data cable;
- PC capable of building/flashing ESP-IDF;
- stable PC USB power;
- camera/phone for evidence photographs.

Not required by IHAP-53: multimeter, external PSU, logic analyzer, external level shifter, external I2C pull-ups or a 5 V display test.

### Software

Reference toolchain:

- Git;
- **ESP-IDF v6.0.1** with ESP32-C3 support;
- terminal capable of persisting monitor output.

Official ESP-IDF v6.0.1 ESP32-C3 setup documentation:

<https://docs.espressif.com/projects/esp-idf/en/v6.0.1/esp32c3/get-started/index.html>

Before testing:

```bash
idf.py --version
```

Reference result:

```text
ESP-IDF v6.0.1
```

A different version must be recorded as a deviation.

---

## 2. Claim classification

Physical observations for the owned specimen:

- blue 0.96-inch-class OLED appearance;
- pins labelled `GND`, `VCC`, `SCL`, `SDA`;
- PCB marking `GME12864-11-12-13 V3.22`;
- address-selection marking `0x3C` / `0x3D`.

Primary family evidence:

- GoldenMorning documents the `GME12864-11/12/13` family as 0.96-inch, 128×64, monochrome OLED, four-pin I2C, SSD1306, with `GME12864-12` as blue and a 3.3–5 V module supply range: <https://goldenmorninglcd.com/oled-display-module/0.96-inch-128x64-ssd1306-gme12864-11/>.
- Solomon Systech documents SSD1306 as a 128×64 monochrome OLED controller with I2C support: <https://www.solomon-systech.com/en/product/SSD1306>.

The owned specimen is consistent with that family evidence. The physical run validates **functional SSD1306 command/profile compatibility**, not independent physical-controller identification.

| Field | Value |
|---|---|
| Evidence ID | `IHAP53-DISPLAY-OWNED-01` |
| Observed marking | `GME12864-11-12-13 V3.22` |
| Observed color | Blue |
| Family correspondence | `GME12864-12` consistent; exact provenance `[UNVALIDATED]` |
| Controller profile | SSD1306 command/data profile functionally validated; exact die identity `[UNVALIDATED]` |
| Interface | I2C — validated for tested specimen |
| Observed address | `0x3C` |
| Validation supply | ESP32-C3 `3.3V` — functional PASS |
| Physical result | PASS within documented claim boundary |
| Architectural decision | ADR-0004 Accepted 2026-08-31 |

---

## 3. Check out the exact IHAP-53 work

Use the existing branch and PR only.

If the repository is absent:

```bash
git clone https://github.com/pianic2/homeedge-ai-platform.git
cd homeedge-ai-platform
git fetch origin pull/31/head:ihap-53-local-display-decision
git switch ihap-53-local-display-decision
```

If already present:

```bash
cd homeedge-ai-platform
git fetch origin
git switch ihap-53-local-display-decision
git pull --ff-only origin ihap-53-local-display-decision
```

Then:

```bash
git status
git rev-parse HEAD
```

Record the exact run SHA. Do not substitute a later documentation-only SHA for the firmware SHA actually tested.

---

## 4. Create an immutable local evidence run

First controlled run ID:

```text
IHAP53-DISPLAY-01
```

From repository root:

```bash
mkdir -p tools/hardware-validation/ihap-53-local-display/runs/IHAP53-DISPLAY-01
cp tools/hardware-validation/ihap-53-local-display/run-record-template.md \
  tools/hardware-validation/ihap-53-local-display/runs/IHAP53-DISPLAY-01/run-record.md
```

Raw run directory:

```text
IHAP53-DISPLAY-01/
├── run-record.md
├── serial.log
├── photo-front-text-card.jpg
└── photo-rear-marking.jpg
```

Raw runs are local laboratory evidence and ignored by Git. Never overwrite an invalid/completed attempt; use a new progressive run ID.

Published sanitized evidence follows [`publication-guide.md`](publication-guide.md).

---

## 5. Validation wiring

This is **test-fixture wiring**, not the final IHAP-50 pinout.

Disconnect USB power before wiring changes.

| OLED pin | ESP32-C3 |
|---|---|
| `GND` | `GND` |
| `VCC` | `3.3V` |
| `SDA` | GPIO5 |
| `SCL` | GPIO6 |

Observed jumper colors for `IHAP53-DISPLAY-01`:

- black = GND;
- red = 3.3 V;
- orange = SCL;
- yellow = SDA.

Rules:

1. Verify physical OLED labels before connecting.
2. Use 3.3 V only for this qualification profile.
3. Use common ground.
4. Do not use GPIO2.
5. Do not add an external level shifter.
6. Do not change pull-ups unless a new diagnostic run explicitly requires it.
7. Any wiring change after run start invalidates that attempt.

---

## 6. Build and flash

From repository root, after activating ESP-IDF v6.0.1:

```bash
cd tools/hardware-validation/ihap-53-local-display/firmware
idf.py --version
idf.py set-target esp32c3
idf.py build
```

Identify the actual serial port, then flash, for example:

```bash
idf.py -p /dev/ttyACM0 flash
```

Record ESP-IDF version, exact Git SHA, port, build result, flash result and deviations in `run-record.md`.

Do not start the controlled run if build or flash fails.

---

## 7. Persist the complete serial evidence

From the firmware directory on Linux/macOS:

```bash
idf.py -p /dev/ttyACM0 monitor 2>&1 | tee ../runs/IHAP53-DISPLAY-01/serial.log
```

Use the real port and run ID. Keep one continuous log from initial boot through the one-hour gate and controlled reboot/reinitialization.

If capture fails, treat it as an evidence-capture failure and correct the procedure before continuing.

---

## 8. Short functional gate

Required order:

1. exactly one candidate address responds at `0x3C` or `0x3D`;
2. SSD1306-profile initialization succeeds;
3. full-screen ON is visibly correct;
4. full-screen OFF is visibly correct;
5. checkerboard is stable, correctly oriented and covers the full area;
6. `HOMEEDGE / IHAP53` text card is complete and readable;
7. stability mode begins and heartbeats appear.

`PASS_TRANSFER` proves a successful transfer only. Visual correctness remains an operator observation and must be recorded.

Reject for no candidate address, unexpected dual candidate response, I2C error, shifted/cropped/mirrored/corrupt/blank output, unexpected reset/brownout or display instability.

---

## 9. One-hour stability gate

Only continue after the short gate passes.

- Keep wiring and power unchanged.
- Keep the same monitor/log capture active.
- Run continuously at least 60 minutes from the stability start event.
- Verify heartbeat approximately every 5 seconds.
- Verify the moving marker continues changing.
- Reject for I2C error, unexpected reset, brownout, freeze/corruption or rewiring.

Acceptance requires a valid heartbeat with:

```text
elapsed_s >= 3600
```

For `IHAP53-DISPLAY-01`, the highest accepted pre-reset heartbeat was `elapsed_s=3622`.

This is a functional stability test, not lifetime/endurance certification.

---

## 10. Controlled reboot / reinitialization gate

After `elapsed_s >= 3600`:

1. keep monitor and capture active;
2. press ESP32-C3 `RST` exactly once;
3. do not change wiring;
4. confirm a new boot sequence;
5. confirm the same display address;
6. confirm SSD1306-profile initialization succeeds;
7. confirm the complete visual sequence again;
8. confirm stability mode restarts.

Stop the monitor normally after the evidence is captured.

---

## 11. Required evidence and publication

Local raw evidence must include:

- `run-record.md`;
- continuous `serial.log`;
- front text-card photograph;
- rear/PCB marking photograph.

The run record must identify run ID, tested SHA, toolchain, port, supply, address, build/flash, visual observations, 60-minute result, highest `elapsed_s`, reboot/re-init result, reset/brownout/corruption observations, SSD1306-profile compatibility conclusion and anomalies/deviations.

Before repository publication, photographs must be real photographs with only non-semantic transformations such as crop, orientation normalization, standard-format conversion, mild exposure/contrast/sharpness normalization and metadata removal. Generatively reconstructed images are not validation evidence.

Canonical published files for this accepted run:

```text
docs/evidence/IHAP-53/IHAP53-DISPLAY-01/
├── run-record.md
├── photo-front-text-card.png
├── photo-rear-marking.png
└── photo-wiring-annotated.png
```

Raw `serial.log` remains local by policy and retained for audit/re-review.

---

## 12. Acceptance record

Physical PASS and architectural acceptance are separate gates.

- Physical validation `IHAP53-DISPLAY-01`: **PASS**.
- Final specialist review: **PASS**, no BLOCKER/MAJOR remaining.
- Project Owner decision: **ADR-0004 Accepted on 2026-08-31**.

Acceptance is persisted in the ADR, ADR index, PR/Jira closure records and Product Vision update. The physical run did not accept itself.

---

## 13. What the accepted evidence supports

Supported for the tested specimen:

- I2C communication at the observed address under tested wiring;
- functional compatibility with the SSD1306 command/data profile used by the harness;
- 128×64 full-area rendering and simple text output;
- repeated updates for the one-hour run;
- reinitialization after one controlled ESP32-C3 reset;
- functional operation from the tested 3.3 V supply.

Not proven by IHAP-53:

- exact physical controller die identity;
- universal compatibility of every `GME12864-11/12/13` board;
- seller/lot reproducibility;
- final product pinout or pull-up values;
- quantitative current consumption or autonomy;
- enclosure visibility/mechanical durability;
- production, security, safety or certification maturity.

Quantitative power remains IHAP-49; final interconnect remains IHAP-50; enclosure remains IHAP-51; definitive BOM propagation remains IHAP-17.

---

## 14. Stop and correction rule for future reruns

Stop and correct the existing repository documentation/harness before proceeding if:

- a required step is ambiguous;
- physical labels do not match assumptions;
- a reference command does not work;
- required evidence cannot be captured as documented;
- firmware behavior differs from this runbook;
- a result cannot be classified without chat history;
- wiring, firmware, toolchain or acceptance criteria must change.

Preserve invalid attempts under their original run IDs. Do not create a replacement IHAP-53 branch or PR for corrections to this historical validation package.
