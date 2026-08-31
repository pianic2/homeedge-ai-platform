# IHAP-53 Validated Evidence Publication Guide

**Issue:** IHAP-53 — Local Display Decision — 0.96-inch OLED vs No Display  
**Purpose:** define exactly how a completed local validation run is promoted from ignored raw laboratory evidence into reviewed repository evidence.

## Source / publication boundary

Raw run data remains local under:

```text
tools/hardware-validation/ihap-53-local-display/runs/<RUN-ID>/
```

That directory is intentionally ignored by Git. Do **not** remove the ignore rule and do **not** use `git add -f` to publish the raw run.

Reviewed evidence for a validated run is published under:

```text
docs/evidence/IHAP-53/<RUN-ID>/
```

For the accepted physical run:

```text
docs/evidence/IHAP-53/IHAP53-DISPLAY-01/
```

## Publishable files for IHAP53-DISPLAY-01

Create this repository-visible structure:

```text
docs/evidence/IHAP-53/IHAP53-DISPLAY-01/
├── run-record.md
├── photo-front-text-card.png
├── photo-rear-marking.png
└── photo-wiring-annotated.png
```

### `run-record.md`

Use the completed reviewed run record derived from the local run. It must contain the physical PASS/FAIL classification, exact tested commit/toolchain, observed address, stability result, controlled reboot result, anomalies and claim boundary.

Do not publish workstation paths, usernames, credentials, SSIDs, MAC addresses, unique chip identifiers or other unnecessary host-specific data.

### Photographs

Only real photographs of the tested specimen may be evidence. Permitted transformations are non-semantic:

- crop;
- rotation/orientation normalization;
- standard PNG/JPEG conversion;
- light exposure/contrast/sharpness normalization that does not alter technical details;
- EXIF/metadata removal;
- explanatory arrows/labels on a supplemental wiring image, provided the underlying photograph remains real and the annotation does not invent or obscure evidence.

Do not use generatively reconstructed or AI-redrawn component images as validation evidence.

Required publication images for this run:

- `photo-front-text-card.png` — real tested display showing the readable `HOMEEDGE` / `IHAP53` card;
- `photo-rear-marking.png` — real rear PCB showing `GME12864-11-12-13 V3.22` and the I2C address-select markings;
- `photo-wiring-annotated.png` — supplemental real-photo wiring evidence documenting black = GND, red = 3.3 V, orange = SCL, yellow = SDA.

## Raw `serial.log`

The complete `serial.log` remains in the ignored local run by default. Do not copy the raw monitor stream into Git merely to make it visible.

The reviewed `run-record.md` records the evidence-derived facts needed for repository review, including:

- `0x3C` ACK and `0x3D` no-ACK;
- SSD1306 initialization-profile transfer PASS;
- visual transfer sequence PASS plus operator visual confirmation;
- heartbeat at/after 3600 seconds;
- highest accepted pre-reset `elapsed_s`;
- absence/presence of I2C errors, brownout and unexpected resets;
- controlled reboot/reinitialization result;
- non-invalidating host-monitor anomalies.

Retain the raw local log unchanged for audit/re-review.

## Copy workflow

From repository root, after reviewing the local evidence:

```bash
mkdir -p docs/evidence/IHAP-53/IHAP53-DISPLAY-01

cp tools/hardware-validation/ihap-53-local-display/runs/IHAP53-DISPLAY-01/run-record.md \
  docs/evidence/IHAP-53/IHAP53-DISPLAY-01/run-record.md
```

Copy the three sanitized image files into the same publication directory using the exact names above.

Then verify:

```bash
git status --short
```

Expected repository-visible additions are the reviewed `run-record.md` and the three sanitized PNG files under `docs/evidence/IHAP-53/IHAP53-DISPLAY-01/`. Files under `tools/hardware-validation/ihap-53-local-display/runs/` should remain ignored.

Before staging, verify that the published record and images contain no prohibited metadata or private host information.

## Staging

Stage only the reviewed publication package and related canonical documentation changes:

```bash
git add docs/evidence/IHAP-53/IHAP53-DISPLAY-01/
git add docs/evidence/IHAP-53/publication-guide.md
```

Do not stage `tools/hardware-validation/ihap-53-local-display/runs/`.

`IHAP53-DISPLAY-01` is physically validated PASS. Publication of PASS evidence does not itself accept ADR-0004; ADR status remains under explicit Project Owner authority after evidence review.
