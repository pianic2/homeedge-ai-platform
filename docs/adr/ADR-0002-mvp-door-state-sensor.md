# ADR-0002 — MVP Door State Sensor

**Status:** Proposed  
**Date:** 2026-07-16  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Jira:** [IHAP-47](https://niccolopiazzi01.atlassian.net/browse/IHAP-47)  
**PR:** [#26](https://github.com/pianic2/homeedge-ai-platform/pull/26)  
**Supersedes:** None  
**Superseded by:** None

<!--
AI_AGENT_METADATA:
  document_type: architecture_decision_record
  decision_scope: mvp_door_state_sensor_technology
  issue: IHAP-47
  parent_issue: IHAP-43
  canonical_template: docs/adr/template.md
  status: Proposed
  approval_authority: project_owner
  approval_recorded: false
  source_of_truth: github_versioned_repository_documentation
  jira_role: workflow_state_blockers_and_evidence_links
  confluence_role: optional_stakeholder_summary_and_navigation_only
  candidate_sensor_class: passive_wired_magnetic_reed_contact
  owned_candidate: generic_mc38_or_dc38_contact
  owned_candidate_qualification: pending_physical_test
  exact_no_nc_behavior: unvalidated
  exact_activation_envelope: unvalidated
  exact_bounce_behavior: unvalidated
  final_pull_strategy_issue: IHAP-50
  quantitative_power_issue: IHAP-49
  final_mounting_issue: IHAP-51
  unvalidated_claim_marker: "[UNVALIDATED]"

HIDDEN_ANTI_REGRESSION_RULES:
  - Keep one stable decision in this ADR: the MVP door-state sensor technology class and its qualification boundary.
  - Do not treat the generic MC-38 or DC-38 commercial label as a controlled manufacturer part number.
  - Do not promote the owned specimen to definitive reference before the IHAP-47 physical protocol is completed.
  - Do not introduce window sensors, multiple-opening topology, tamper detection, access control, alarm, antifurto or intrusion-detection behavior.
  - Do not define the final GPIO, cable, connector, external pull resistor, protection circuit or assembly quantities; those belong to IHAP-50.
  - Do not infer measured current or autonomy; those belong to IHAP-49.
  - Do not define the final installation gap, adhesive, bracket or enclosure; those belong to IHAP-51.
  - Preserve [UNVALIDATED] for exact NO/NC behavior, activation distance, alignment tolerance, bounce, replacement reproducibility and current market cost until evidence exists.
-->

---

## 1. Context

The HomeEdge MVP contains one generic room/door node and may report the local room door as open or closed. The signal is telemetry only. It must not be interpreted as identity, access authorization, intrusion evidence, an alarm, antifurto behavior, protection evidence or a safety-critical state.

ADR-0001 accepts ESP32-C3 as the MVP compute family and requires at least one interrupt-capable 3.3 V digital input. It deliberately leaves the sensor, final pin mapping, power subsystem, interconnect and mounting decisions to their owning tasks.

IHAP-47 must choose a proportionate door-state technology for a single reference door. The owned candidate is sold under the generic `MC-38` or `DC-38` label. That commercial label does not identify a controlled manufacturer, part number, datasheet, reed form, activation distance or production lot.

Historical prototype artifacts supplied by the Project Owner establish limited feasibility for one earlier setup:

- one contact was connected between ESP32-C3 GPIO6 and ground;
- the ESP32-C3 internal pull-up was enabled;
- a closed electrical contact was interpreted as `LOW` and an open circuit as `HIGH`;
- firmware used three reads separated by approximately 1.2 ms and selected the majority level;
- serial telemetry showed both open and closed logical states during the historical session.

The raw historical firmware and serial log are not committed by this decision. They contain unrelated prototype behavior and raw execution data. The summary above is evidence of historical feasibility only. It does not prove the exact owned specimen type, bounce duration, activation envelope, cable tolerance, failure detection, reproducibility or reliability.

### 1.1 Technology comparison

| Candidate | Power at sensor | Interface | Main benefit | Main limitation | MVP disposition |
|---|---:|---|---|---|---|
| Packaged wired magnetic reed contact, including the owned MC-38 candidate | None | Two conductors and one GPIO | Passive, simple, contactless and already owned | Exact commercial variant and activation behavior are not controlled | Candidate |
| Bare reed switch plus selected magnet | None | Two conductors and one GPIO | The reed part and magnet can be controlled separately | Requires custom packaging and protection | Deferred fallback |
| Digital Hall-effect sensor | Active supply required | Supply, ground and digital output | No mechanical contact bounce and controlled semiconductor SKU | Adds powered electronics, decoupling and magnetic design with no demonstrated MVP need | Rejected for primary MVP use |
| Mechanical microswitch | None | Two or three conductors and one GPIO | Controlled industrial parts are available with NO/NC terminals | Requires physical actuation, force, travel and mounting tolerance | Rejected for primary MVP use |
| Wireless commercial door contact | Battery and radio | Radio protocol and pairing | Avoids signal cable | Adds battery lifecycle, protocol, provisioning and replacement complexity | Rejected for MVP |

Primary references used for the technology comparison:

- [Espressif ESP32-C3 GPIO programming guide](https://docs.espressif.com/projects/esp-idf/en/stable/esp32c3/api-reference/peripherals/gpio.html)
- [Espressif ESP32-C3 Series Datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-c3_datasheet_en.pdf)
- [Standex Detect — Reed Switch Operational Characteristics](https://standexdetect.com/resources/reed-technology-academy/reed-switch-characteristics/reed-switch-operational-characteristics/)
- [Standex Detect — Reed Sensor Activation Distances](https://standexdetect.com/resources/reed-technology-academy/reed-sensor-activation-distances/)
- [Texas Instruments DRV5032 datasheet](https://www.ti.com/lit/ds/symlink/drv5032.pdf)
- [Omron D2F datasheet](https://omronfs.omron.com/en_US/ecb/products/pdf/en-d2f.pdf)

These sources characterize representative technologies or controlled example parts. They do not characterize the exact owned MC-38 specimen.

### 1.2 Required physical evidence

The owned candidate cannot become the definitive reference until the reproducible IHAP-47 protocol records at least:

- specimen photographs and markings;
- magnet-near and magnet-far continuity behavior;
- inferred NO/NC behavior using unambiguous reed terminology;
- pull-in and drop-out distances;
- lateral and vertical alignment observations;
- raw transition and bounce evidence;
- repeated open/closed cycles;
- disconnected-wire and short-to-ground behavior;
- comparison of at least two owned specimens when available.

Until those results exist, exact specimen behavior remains `[UNVALIDATED]`.

---

## 2. Decision

```text
We will use a passive, wired, two-conductor magnetic reed-contact technology
as the proposed MVP door-state sensor class.

The owned MC-38 / DC-38 contact is the preferred qualification candidate,
but it is not the definitive reproducible reference until the IHAP-47
physical test protocol is completed and reviewed.
```

The proposed electrical semantics are:

- one contact conductor connects to an ESP32-C3 digital input;
- the other contact conductor connects to ground;
- the input is biased high by a pull-up;
- a closed electrical contact reads `LOW`;
- an open electrical circuit reads `HIGH`.

This topology is proposed because a disconnected conductor also produces the conservative `HIGH` electrical state rather than an apparent closed circuit. It does **not** provide wire supervision. The MVP cannot distinguish a physically open door from a detached magnet, misalignment, disconnected cable or contact that failed open.

The following implementation details are intentionally not accepted by this ADR:

- whether the owned specimen is technically Form A/NO or Form B/NC;
- the final physical mapping between magnet position and electrical state;
- the final GPIO number;
- internal versus external pull-up for the integrated node;
- the external pull resistance;
- polling period, interrupt use or final debounce interval;
- cable type, cable length, connector, ESD protection or assembly quantities;
- installation distance, bracket, adhesive, enclosure or final mounting geometry;
- tamper detection or supervised-loop behavior.

The default firmware direction is periodic sampling with software stable-state debounce. Interrupt-driven capture remains available when later power or wake requirements justify it. The test harness may sample much faster than production firmware solely to observe transitions; its timing is not the production decision.

The decision remains `Proposed`. The Project Owner must review physical evidence before accepting the exact MC-38 candidate or any replacement part.

---

## 3. Alternatives Considered

| Alternative | Outcome | Reason |
|---|---|---|
| Owned packaged MC-38 / DC-38 magnetic contact | Accepted as qualification candidate | Already owned, passive, historically connected to ESP32-C3 and proportionate to a binary door-state requirement. Exact variant and physical behavior remain `[UNVALIDATED]`. |
| Controlled packaged reed contact with manufacturer part number and declared gap | Deferred fallback | Preferred fallback if the generic owned contact cannot be qualified or reproduced. Selecting an exact procurement SKU requires current cost and availability evidence under IHAP-17. |
| Bare reed switch plus separately selected magnet | Deferred | Technically simple and controllable, but requires custom mechanical protection and packaging that the owned packaged contact may avoid. |
| Digital Hall-effect sensor such as TI DRV5032 class | Rejected as primary | Requires active supply, decoupling and variant-specific magnetic/output design. The absence of mechanical bounce does not currently justify the added integration complexity. |
| Mechanical microswitch such as Omron D2F class | Rejected as primary | Controlled ratings and NO/NC terminals are available, but the door must physically actuate the switch within force and travel tolerances. This adds mounting and wear constraints without a demonstrated MVP benefit. |
| Wireless battery contact | Rejected | Adds pairing, protocol, battery, radio reliability and replacement lifecycle beyond the single wired MVP node. |
| Supervised loop with end-of-line resistor or tamper circuit | Rejected for MVP | Would add fault-state modeling, analog or multi-threshold circuitry, wiring and security implications. The MVP is telemetry only and does not claim tamper detection. |

---

## 4. Consequences

### Positive

- Uses one digital GPIO and two signal conductors.
- Requires no active sensor supply.
- Avoids a new communication protocol or battery lifecycle.
- Supports non-contact door movement sensing.
- Keeps the sensor class replaceable independently of the generic MC-38 label.
- Reuses historical feasibility without misclassifying it as current validation.
- Provides an explicit path from raw physical evidence to a later Project Owner decision.

### Negative / Trade-offs

- The generic MC-38 label is not a controlled or reproducible part number.
- An open circuit is ambiguous: door open, magnet missing, misalignment, disconnected wire and failed-open contact can produce the same level.
- A short to ground or failed-closed contact can appear as a closed electrical circuit.
- Reed contacts can produce mechanical transition bounce.
- Activation distance depends on the reed, magnet, orientation, surrounding material and individual specimen.
- Internal pull-up behavior may be adequate on the bench but insufficient for the final cable and installation `[UNVALIDATED]`.
- The exact fallback part and current landed replacement cost remain `[UNVALIDATED]`.

### Neutral / Operational

- `HIGH` and `LOW` describe electrical states, not security conclusions.
- The external event remains binary door-state telemetry. A sensor-fault state is not introduced by this ADR.
- The firmware must maintain an internal uninitialized state until the first stable read rather than defaulting silently to `CLOSED`.
- Final pull, cable, connector, protection and GPIO choices belong to IHAP-50.
- Quantitative current and autonomy effects belong to IHAP-49.
- Final activation margin and physical mounting belong to IHAP-51.
- Window sensors and multi-opening wiring remain outside the current MVP.

---

## 5. Related Risks and Treatments

| Risk | Treatment | Effect | Remaining exposure |
|---|---|---|---|
| [R-004 — Presence and Door State Misinterpretation](../risks/records/R-004-presence-door-state-misinterpretation.md) | None | Partially mitigates through explicit telemetry-only semantics and rejected security claims | Stakeholders or later software may still over-interpret a binary state; wording and schema reviews remain required. |

This ADR does not accept, close or resolve R-004. The Risk Record remains authoritative for risk treatment and Project Owner decisions.

No new physical-sensor Risk Record is created automatically. A new record requires a separate scope decision if physical false-state exposure becomes a project-level risk rather than a documented component limitation.

---

## 6. Follow-up Work

| Item | Tracking |
|---|---|
| Execute specimen identification, NO/NC, gap, alignment, bounce, cycle and failure-mode protocol | IHAP-47 physical evidence handoff |
| Decide whether the owned MC-38 becomes the definitive reference or only a locally qualified candidate | IHAP-47 Project Owner decision |
| Select a controlled fallback SKU if generic replacement reproducibility is insufficient | IHAP-17 / IHAP-43 |
| Freeze GPIO, pull resistor, cable, connector and protection circuit | IHAP-50 |
| Include the closed-loop pull current and any active fallback in the power budget | IHAP-49 |
| Freeze mounting gap, alignment margin, attachment method and enclosure constraints | IHAP-51 |
| Implement production door-state acquisition after the hardware decision is accepted | Future implementation task |
| Review event semantics before a stable schema is declared | Event-contract task / future implementation |

---

## 7. Evidence Links

| Evidence | Link |
|---|---|
| Jira issue | [IHAP-47](https://niccolopiazzi01.atlassian.net/browse/IHAP-47) |
| Parent hardware baseline | [IHAP-43](https://niccolopiazzi01.atlassian.net/browse/IHAP-43) |
| Compute baseline | [ADR-0001](ADR-0001-mvp-edge-compute-platform.md) |
| Pull request | [PR #26](https://github.com/pianic2/homeedge-ai-platform/pull/26) |
| Evidence manifest | [`docs/evidence/IHAP-47/README.md`](../evidence/IHAP-47/README.md) |
| Reproducible physical protocol | [`docs/evidence/IHAP-47/test-protocol.md`](../evidence/IHAP-47/test-protocol.md) |
| Validation harness | [`tools/hardware-validation/ihap-47-door-state-sensor/`](../../tools/hardware-validation/ihap-47-door-state-sensor/) |
| Product boundary | [`docs/product/product-vision.md`](../product/product-vision.md) |
| Related Risk Record | [`R-004`](../risks/records/R-004-presence-door-state-misinterpretation.md) |
| Canonical ADR template | [`docs/adr/template.md`](template.md) |
| Related treatments | None |

---

## 8. Review Notes

```text
[x] One stable architectural decision only.
[x] ADR necessity is explicit; no ADR was created automatically from a risk.
[x] Related risks and treatments are listed when relevant.
[x] Effect and remaining exposure are explicit for every linked risk.
[x] Linked Risk Records contain inverse links.
[x] The ADR is not treated as risk acceptance or closure evidence.
[x] Source-of-truth boundaries are preserved.
[x] MVP boundary is not silently expanded.
[x] [UNVALIDATED] is preserved on unproven claims.
[x] No production-ready, commercial-ready, security-grade, certified, safety-critical, alarm-grade, antifurto, access-control, intrusion-detection, or protection claim is introduced.
[ ] Project Owner decision is recorded before status becomes Accepted, Rejected, or Superseded.
```

The inverse R-004 link is present. The final Project Owner status decision remains pending because the physical test has not yet been executed.
