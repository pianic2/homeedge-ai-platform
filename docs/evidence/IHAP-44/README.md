# IHAP-44 — ESP32-C3 SuperMini Physical Evidence

**Issue:** [IHAP-44](https://niccolopiazzi01.atlassian.net/browse/IHAP-44)  
**Decision document:** [`ADR-0001`](../../adr/ADR-0001-mvp-edge-compute-platform.md)  
**Evidence owner:** Project Owner  
**Received:** 2026-07-14  
**Repository purpose:** durable, human-readable physical evidence for one owned board specimen

<!--
AI_AGENT_METADATA:
  document_type: hardware_evidence_manifest
  issue: IHAP-44
  evidence_scope: one_owned_esp32_c3_supermini_compatible_specimen
  source: project_owner_supplied_photographs
  original_files_committed: false
  published_files_sanitized: true
  transformations:
    - crop
    - jpeg_conversion
    - resize
    - compression
    - exif_removal
  privacy_review: passed_for_repository_publication
  unvalidated_claim_marker: "[UNVALIDATED]"

HIDDEN_ANTI_REGRESSION_RULES:
  - These photographs prove observations about one owned specimen only.
  - Do not infer seller identity, lot consistency, schematic, regulator capacity or universal SuperMini equivalence.
  - Do not use the photographs as proof of runtime stability, current draw, 5 V tolerance or production readiness.
-->

## Evidence Files

| Evidence ID | File | View | SHA-256 |
|---|---|---|---|
| E-IHAP44-01 | [`esp32-c3-supermini-front.jpg`](esp32-c3-supermini-front.jpg) | Front/component side | `4236504134822a114149616858adf3e04b5524d340237aa1056aca28f8a1c8ab` |
| E-IHAP44-02 | [`esp32-c3-supermini-back.jpg`](esp32-c3-supermini-back.jpg) | Rear/pin-label side | `2dc9b89c9455b118a9154c75615f19cc5b2769708f2ebdb20ceb06c5f1d84998` |

## Published Images

### E-IHAP44-01 — Front

![Front view of the ESP32-C3 SuperMini-compatible specimen](esp32-c3-supermini-front.jpg)

Visible observations:

- USB-C connector;
- `BOOT` and `RST` buttons;
- ESP32-C3 package;
- 40 MHz crystal;
- PCB antenna area;
- supply and GPIO edge labels visible in part.

### E-IHAP44-02 — Rear

![Rear view of the ESP32-C3 SuperMini-compatible specimen](esp32-c3-supermini-back.jpg)

Visible observations:

- `ESP32 C3 Super Mini` label;
- supply labels `5V`, `G`, `3.3`;
- GPIO labels `0`–`10`, `20` and `21`;
- through-hole/castellated connection layout.

## Provenance and Transformations

The Project Owner supplied the photographs in the project conversation. Repository copies were produced without generative alteration.

Applied transformations:

1. cropped unused surrounding background;
2. converted the source image payload to JPEG;
3. resized to a repository-friendly resolution;
4. applied JPEG compression;
5. removed EXIF metadata, including any location/device metadata.

No component, label, trace, pin, solder joint or marking was added, removed or reconstructed.

The original source files are not committed. The checksums above refer to the complete sanitized JPEG repository files.

## Claims Supported

The images support claims about the visible layout and labels of one specimen:

- the board is labelled `ESP32 C3 Super Mini`;
- the specimen has USB-C, BOOT and RST;
- the listed supply and GPIO labels are physically exposed;
- the photographed PCB is consistent with the specimen described in ADR-0001.

## Claims Not Supported

The images do not prove:

- exact seller, commercial SKU, listing or lot;
- equivalence of other boards marketed as SuperMini;
- complete schematic or regulator identity/capacity;
- GPIO electrical safety or 5 V tolerance;
- runtime stability, Wi-Fi behavior or brownout immunity;
- measured current, power or autonomy;
- current market availability or replacement price;
- production, commercial, reliability, safety, security or certification maturity.

Those claims remain `[UNVALIDATED]` unless supported by separate evidence.
