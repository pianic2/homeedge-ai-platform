# IHAP-48 Evidence — Audio Hardware Disposition

**Issue:** IHAP-48 — Audio Hardware Disposition — GY-MAX4466  
**Decision date:** 2026-08-31  
**Decision:** remove from reference MVP; retain as FUTURE inventory  
**Runtime test required:** No

---

## Evidence purpose

This evidence package supports a hardware-disposition decision, not an audio-performance qualification.

The selected reference MVP state is:

```text
physical presence = no
electrical connection = no
powered = no
firmware access = no
MVP audio capability = no
future audio work = separate approval required
```

Because the component is removed from the reference configuration, no microphone gain, current, waveform, ADC quality, sensitivity, noise, pinout or module-level supply characteristic is required to validate the decision.

---

## Canonical evidence

| Evidence | Purpose |
|---|---|
| [`docs/architecture/ihap-48-audio-hardware-disposition.md`](../../architecture/ihap-48-audio-hardware-disposition.md) | Canonical disposition and ADR-not-required rationale |
| [`docs/product/product-vision.md`](../../product/product-vision.md) | Protected MVP and privacy boundary; raw audio remains outside MVP |
| [`docs/adr/ADR-0001-mvp-edge-compute-platform.md`](../../adr/ADR-0001-mvp-edge-compute-platform.md) | ESP32-C3 reference profile and no audio authorization |
| [`docs/adr/ADR-0004-local-status-display.md`](../../adr/ADR-0004-local-status-display.md) | Current accepted local-display hardware dependency and downstream resource ownership |
| [`docs/risks/records/R-002-event-payload-leakage.md`](../../risks/records/R-002-event-payload-leakage.md) | Existing privacy control excluding raw audio from payload scope |
| [`docs/risks/records/R-007-ai-inference-profiling.md`](../../risks/records/R-007-ai-inference-profiling.md) | Existing future-inference/profiling boundary |
| Jira IHAP-48 | Project Owner decision, workflow and completion evidence |
| Jira IHAP-43 | Final hardware decision matrix consumer |
| IHAP-17 cost/BOM work | Provisional installed-disabled classification to be replaced downstream |

Primary IC-family documentation:

- Analog Devices MAX4466 product page: https://www.analog.com/en/products/max4466.html
- Analog Devices MAX4465–MAX4469 datasheet: https://www.analog.com/media/en/technical-documentation/data-sheets/MAX4465-MAX4469.pdf

These sources establish that MAX4466 is intended for microphone-preamplifier use. They do not establish the exact implementation of the owned GY-MAX4466 module.

---

## Claim boundary

Supported:

- the Project Owner owns GY-MAX4466 inventory;
- the reference MVP does not physically include that inventory;
- no audio-specific electrical, firmware, enclosure or BOM requirement is reserved;
- a future audio-derived direction is genuinely considered but remains outside MVP and requires separate approval;
- an ADR is not required for the selected removal disposition.

Not supported / not claimed:

- exact owned-module pinout;
- exact supply/current behavior;
- microphone capsule identity;
- onboard gain-network values;
- seller/lot reproducibility;
- audio capture quality;
- speech recognition or derived-signal feasibility;
- privacy acceptability of any future derived signal;
- production, commercial, alarm, safety, security or certification maturity.

---

## PASS gate

```text
[PASS] Product Vision raw-audio boundary preserved
[PASS] Reference physical presence = NO
[PASS] Electrical connection = NO
[PASS] Power allocation = NO
[PASS] ADC/GPIO reservation = NO
[PASS] Firmware audio surface = NO
[PASS] Audio enclosure/aperture requirement = NO
[PASS] Future audio direction explicitly separated from MVP
[PASS] ADR-not-required rationale documented
[PASS] No audio runtime implementation introduced
```

A specimen photograph may be added later as inventory-identification evidence, but it is not required to prove removal from the reference MVP.
