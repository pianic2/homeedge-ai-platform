# IHAP-46 — HLK-LD2410C V1.1 Physical Evidence

**Issue:** [IHAP-46](https://niccolopiazzi01.atlassian.net/browse/IHAP-46)  
**Evidence owner:** Project Owner  
**Received:** 2026-07-15  
**Repository purpose:** durable, human-readable physical evidence for one owned presence-sensor specimen

<!--
AI_AGENT_METADATA:
  document_type: hardware_evidence_manifest
  issue: IHAP-46
  evidence_scope: one_owned_hlk_ld2410c_v1_1_specimen
  source: project_owner_supplied_photographs
  original_files_committed: false
  published_files_sanitized: true
  transformations:
    - crop
    - jpeg_reencode
    - exif_removal
    - repository_svg_container
  privacy_review: passed_for_repository_publication
  unvalidated_claim_marker: "[UNVALIDATED]"

HIDDEN_ANTI_REGRESSION_RULES:
  - These photographs prove visible observations about one owned specimen only.
  - Do not infer seller identity, lot consistency, complete schematic, signal voltage, output logic level, or universal LD2410C equivalence.
  - Do not use the photographs as proof of UART operation, detection performance, power stability, production readiness, or MVP suitability.
-->

## Evidence files

| Evidence ID | File | View | SHA-256 |
|---|---|---|---|
| E-IHAP46-01 | [`ld2410c-v1-1-component-side.svg`](ld2410c-v1-1-component-side.svg) | Component/controller side | `8efd6555451c63895e2c14d84b5e235e0f7271b133a158f51525e7bce3618388` |
| E-IHAP46-02 | [`ld2410c-v1-1-antenna-side.svg`](ld2410c-v1-1-antenna-side.svg) | Antenna and pin-label side | `e24112a7f8fdfd471848eed560db8b1b7b6861b2104f9f73852ceceb12a47705` |

The SVG files are repository-safe containers for the sanitized JPEG raster payloads. They preserve the photographs without reconstructing or generating component detail.

## Published images

### E-IHAP46-01 — Component/controller side

![Component side of the owned HLK-LD2410C V1.1 specimen](ld2410c-v1-1-component-side.svg)

Visible observations:

- `HLK-LD2410C` silkscreen;
- `V1.1` PCB revision silkscreen;
- five-pin header;
- populated controller and support components;
- additional unpopulated circular pads on the PCB edge.

### E-IHAP46-02 — Antenna and pin-label side

![Antenna side of the owned HLK-LD2410C V1.1 specimen](ld2410c-v1-1-antenna-side.svg)

Visible observations:

- antenna structures;
- five soldered header positions;
- pin labels, left to right in the photographed orientation: `TX`, `RX`, `OUT`, `GND`, `VCC`;
- populated radio/controller package and support components.

## Provenance and transformations

The Project Owner supplied both photographs in the project conversation.

The source uploads used a `.heic` filename but contained JPEG image payloads. Repository copies were produced without generative alteration.

Applied transformations:

1. cropped unused surrounding background;
2. decoded and re-encoded the raster as JPEG;
3. removed EXIF metadata, including device or location metadata;
4. applied repository-friendly JPEG compression;
5. embedded the sanitized JPEG payload in a text-based SVG container so the repository connector could store and render the evidence.

No component, label, trace, pin, solder joint, antenna, package, or marking was added, removed, reconstructed, or enhanced.

The original uploads are not committed. The checksums above refer to the complete published SVG files.

## Claims supported

The images support claims about the visible layout and labels of one owned specimen:

- the board is visibly marked `HLK-LD2410C`;
- the board is visibly marked `V1.1`;
- the photographed specimen exposes five labelled connections;
- the visible pin order on the antenna side is `TX RX OUT GND VCC`;
- an antenna side and a component/controller side are physically present;
- the specimen can be uniquely referenced in IHAP-46 test metadata as `LD2410C-HLK-V1.1-OWNED-01`.

## Claims not supported

The images do not prove:

- exact seller, commercial SKU, listing, date code, or lot;
- electrical equivalence with other LD2410C boards;
- signal voltage or ESP32-C3 GPIO compatibility;
- UART baud rate, frame format, or successful communication;
- OUT pin logic level or timing;
- regulator behavior, current draw, rail stability, or autonomy;
- detection range, angle, stationary-presence performance, latency, or false-positive behavior;
- resistance to wall, corridor, door, curtain, fan, pet, or environmental interference;
- configuration persistence after reset;
- production, commercial, reliability, safety, security, alarm, or certification maturity.

Those claims remain `[UNVALIDATED]` unless supported by separate physical test evidence.
