# IHAP-48 — Audio Hardware Disposition — GY-MAX4466

**Status:** Project Owner decision recorded — remove from reference MVP  
**Date:** 2026-08-31  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Jira:** IHAP-48 — Audio Hardware Disposition — GY-MAX4466  
**Parent:** IHAP-43 — MVP Hardware Component Decision Baseline  
**Document type:** Hardware disposition / ADR-not-required decision record  
**Source of truth:** This versioned GitHub record is the canonical technical disposition for the GY-MAX4466 relative to the reference MVP until superseded by a later reviewed decision.

<!--
AI_AGENT_METADATA:
  issue: IHAP-48
  parent_issue: IHAP-43
  document_type: hardware_disposition_record
  decision_scope: gy_max4466_reference_mvp_disposition
  project_owner_decision_date: 2026-08-31
  owned_inventory: true
  reference_mvp_physical_presence: false
  electrically_connected: false
  powered: false
  firmware_accessible: false
  mvp_audio_capability_authorized: false
  future_audio_experimentation: separate_approval_required
  adr_required: false
  runtime_changes_allowed: false
  firmware_changes_allowed: false
  unvalidated_claim_marker: "[UNVALIDATED]"

HIDDEN_ANTI_REGRESSION_RULES:
  - The GY-MAX4466 is not part of the reference MVP physical node.
  - Ownership does not justify physical inclusion.
  - Do not reserve ADC/GPIO, power, wiring, enclosure volume, aperture or firmware surface for audio in the MVP.
  - Raw audio collection, transmission, persistence, voice recognition, identity, individual tracking, behavioral history and routine profiling remain outside MVP.
  - FUTURE audio-derived work is not authorized by this record and requires a separate reviewed task and Product Owner approval.
  - Do not infer the exact purchased module pinout, supply implementation, current draw, microphone type, gain network or seller/lot characteristics without evidence.
  - No production-ready, commercial-ready, security-grade, alarm-grade, antifurto, access-control, safety-critical or certification claim is introduced.
-->

---

## 1. Context

HomeEdge uses one generic room/door reference node for the MVP. The current Product Vision includes temperature, humidity, local non-identifying presence, door open/closed telemetry and the accepted local status display. Raw audio collection is explicitly outside the MVP boundary.

The Project Owner owns GY-MAX4466 microphone-preamplifier modules, but ownership is inventory evidence only. It is not an architectural reason to include an audio-capable component in the reference node.

Analog Devices documents the MAX4466 IC family as a microphone-preamplifier component. That primary source is sufficient to establish that the inventory is audio-capable at the IC-family level. It does not prove the exact electrical implementation, pinout, microphone, gain network, supply arrangement, seller SKU or lot characteristics of the owned GY-MAX4466 module.

Primary source:

- Analog Devices MAX4466 product page: https://www.analog.com/en/products/max4466.html
- MAX4465–MAX4469 datasheet: https://www.analog.com/media/en/technical-documentation/data-sheets/MAX4465-MAX4469.pdf

No quantitative module-level electrical claim is required for the selected disposition.

---

## 2. Alternatives Considered

| Alternative | Physical presence | Electrical connection | Powered | Firmware access | MVP authorization | Disposition |
|---|---:|---:|---:|---:|---:|---|
| A. Remove from reference MVP; retain as FUTURE inventory | No | No | No | No | No | **Selected** |
| B. Install physically but leave electrically disconnected | Yes | No | No | No | No | Rejected |
| C. Install and power but block software access | Yes | Yes | Yes | No by policy | No | Rejected |
| D. Local derived audio signals | Future decision | Future decision | Future decision | Future decision | Not approved here | FUTURE only |

### 2.1 Alternative A — selected

Removing the module from the reference node satisfies hardware least privilege and removes an unnecessary privacy-sensitive capability from the physical architecture.

It avoids creating requirements for:

- ADC/GPIO allocation;
- power budgeting;
- audio wiring and connectors;
- enclosure volume or microphone aperture;
- audio firmware drivers or sampling surfaces;
- proof that an installed microphone is not being used;
- stakeholder explanation for a microphone with no approved MVP function.

### 2.2 Alternative B — rejected

A physically installed but electrically disconnected microphone provides no MVP function while retaining physical BOM, assembly, enclosure and stakeholder-trust costs. It also creates a latent reconnection path that would require stronger non-use evidence.

### 2.3 Alternative C — rejected

A powered microphone with software access blocked creates a larger latent capability and power/misuse surface without any approved MVP value. Software policy alone is not a proportionate control when the hardware itself is unnecessary.

### 2.4 Alternative D — FUTURE only

Local derived audio signals are a genuinely considered future direction, but they are not part of the MVP and are not authorized by IHAP-48.

Any future experiment must start from a separate approved task and must define, before implementation:

- exact product value;
- allowed signal semantics;
- whether the derived output is reversible or can expose speech/content;
- local processing and data-minimization boundaries;
- retention and transport rules;
- Security & Privacy review;
- architecture significance and ADR necessity;
- hardware/electrical validation;
- stakeholder-safe wording and evidence.

The existence of this FUTURE direction does not reserve hardware resources in the MVP.

---

## 3. Project Owner Decision

On 2026-08-31 the Project Owner decided:

```text
Remove the GY-MAX4466 completely from the reference MVP node.
Retain the owned modules as FUTURE inventory only.
Audio is a genuinely considered future addition, but it is not part of the MVP.
```

The resulting state is:

| Property | Approved state |
|---|---|
| Component owned | Yes |
| Present in reference MVP node | **No** |
| Electrically connected in reference MVP | **No** |
| Powered in reference MVP | **No** |
| Accessible from MVP firmware | **No** |
| Raw audio capability authorized | **No** |
| Derived audio capability authorized | **No — separate future approval required** |
| Future inventory status | **FUTURE** |

---

## 4. ADR Necessity

**ADR NOT REQUIRED.**

Rationale:

- the decision does not add a new runtime or physical capability to the MVP;
- the module is removed rather than retained as an architecture dependency;
- the decision preserves the existing Product Vision privacy boundary;
- no GPIO, ADC, power, interconnect, enclosure or firmware contract is reserved for audio;
- a later audio capability would require a new explicit decision and may independently require an ADR;
- creating an ADR for the removal would add document weight without recording a stable new architecture dependency.

If a later proposal physically installs, connects, powers or reserves runtime capability for an audio module, ADR necessity must be reevaluated from the then-current architecture and ADR index.

---

## 5. Security, Privacy and Stakeholder Boundary

The selected disposition minimizes latent collection capability in the reference node.

The MVP continues to prohibit:

- raw audio collection;
- raw audio transmission or persistence;
- speech or voice recognition;
- person identification;
- individual tracking;
- behavioral history;
- routine profiling.

The module must not appear in stakeholder material as an installed MVP sensor. It may be described only as owned FUTURE inventory or as a possible later experiment requiring separate approval.

---

## 6. Hardware, Cost and Testing Consequences

### Hardware compatibility

For the reference MVP, audio contributes:

```text
ADC/GPIO reservation = 0
power-budget load = 0
audio wiring = 0
audio connector allocation = 0
microphone aperture/mounting requirement = 0
firmware audio surface = 0
```

No exact module current, pinout or gain characteristic is needed to support these zero-allocation consequences because the module is absent from the reference configuration.

### Cost governance

Already-owned modules remain historical acquisition/inventory evidence. They must not be counted as required reference-node replication cost.

The provisional IHAP-17 classification `EDGE_INSTALLED_DISABLED` must be replaced downstream with a FUTURE / inventory-only classification and reference MVP quantity `0` after this accepted disposition is propagated by IHAP-17.

### Testing and evidence

No audio functional test is required to validate removal from the MVP.

PASS evidence is instead structural:

- Product Vision keeps raw audio outside MVP;
- this disposition records physical absence and zero resource allocation;
- no runtime audio implementation is introduced;
- downstream tasks receive zero-allocation handoffs;
- final reference BOM excludes the module.

A photograph of an owned specimen may be added later as inventory evidence, but it is not a blocker for this removal decision and must not be used to infer undocumented module characteristics.

---

## 7. Downstream Handoff

| Consumer | Required handoff |
|---|---|
| IHAP-43 | Record GY-MAX4466 as removed from reference MVP; FUTURE inventory; ADR not required |
| IHAP-49 | Exclude microphone/audio load from reference MVP power budget |
| IHAP-50 | Allocate no ADC/GPIO, connector, wire or passive to audio |
| IHAP-51 | Require no microphone aperture, mounting or internal volume for audio |
| IHAP-17 | Replace provisional `EDGE_INSTALLED_DISABLED` classification with FUTURE / inventory-only; reference MVP quantity `0` |
| Future firmware | No audio driver, sampling, storage or transport requirement is created by IHAP-48 |

These handoffs do not modify the owner tasks themselves. Each downstream task remains responsible for integrating the accepted input in its own branch/PR.

---

## 8. Review Gate

IHAP-48 is ready for completion when the following review perspectives find no `BLOCKER` or `MAJOR` issue:

- Security & Privacy Review;
- Stakeholder Clarity Review;
- Hardware Compatibility Review;
- Architecture Regression Review;
- Testing & Evidence Review;
- Cost Governance Review;
- Source of Truth Review.

PASS criteria:

```text
owned_inventory              = YES
reference_physical_presence  = NO
electrical_connection        = NO
powered                      = NO
firmware_access              = NO
mvp_audio_capability         = NO
future_audio                 = separate approval required
ADR_required                 = NO
```

No Product Vision change is required because raw audio is already outside MVP and FUTURE audio remains outside the current product boundary.
