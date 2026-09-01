# ADR-0003 — MVP Door State Sensor

**Status:** Accepted  
**Date:** 2026-07-16  
**Accepted:** 2026-09-01  
**Last evidence review:** 2026-09-01  
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
  status: Accepted
  approval_authority: project_owner
  approval_recorded: true
  approval_date: 2026-09-01
  source_of_truth: github_versioned_repository_documentation
  candidate_sensor_class: passive_wired_magnetic_reed_contact
  tested_owned_specimen: MC38-A
  reviewed_evidence_id: IHAP47-MC38-A-01
  owned_specimen_physical_gate: PASS
  project_owner_acceptance: accepted_2026-09-01
  observed_far_state: open_raw_1
  observed_near_state: closed_raw_0
  observed_reed_form: form_a_normally_open_relative_to_magnetic_actuation
  observed_cycle_gate: 20_complete_cycles_40_stable_movements_zero_mismatch
  observed_multiple_raw_transitions: 0_of_40_at_250us_sampling
  open_vs_disconnected_wire: electrically_indistinguishable
  final_pull_strategy_issue: IHAP-50
  quantitative_power_issue: IHAP-49
  final_mounting_issue: IHAP-51
  replacement_reproducibility: unvalidated
  unvalidated_claim_marker: "[UNVALIDATED]"

HIDDEN_ANTI_REGRESSION_RULES:
  - Keep one stable decision: passive wired reed-contact technology for MVP binary door-state telemetry.
  - Treat MC38-A evidence as owned-specimen evidence only; do not universalize the MC-38/DC-38 label.
  - Do not introduce window sensors, tamper detection, access control, alarm, antifurto or intrusion-detection behavior.
  - Do not define final GPIO, cable, connector, external pull resistor, protection or production debounce; those belong to IHAP-50.
  - Do not infer measured current or autonomy; those belong to IHAP-49.
  - Do not define final mounting gap, alignment margin, adhesive, bracket or enclosure; those belong to IHAP-51.
  - Preserve the Project Owner acceptance recorded on 2026-09-01 unless a later ADR supersedes this decision.
-->

---

## 1. Context

The HomeEdge MVP needs binary local door-state telemetry. The signal is telemetry only and must not be interpreted as identity, access authorization, intrusion evidence, alarm state, antifurto behavior, protection evidence or a safety-critical state.

ADR-0001 accepts ESP32-C3 as the MVP compute family. IHAP-47 therefore needs only a proportionate sensor technology that can supply deterministic binary electrical state to a 3.3 V digital input.

The owned candidate is sold under the generic `MC-38` / `DC-38` label. That label is not a controlled manufacturer part number and does not by itself establish reed form, activation distance, production lot or replacement equivalence.

### 1.1 Technology comparison

| Candidate | Power at sensor | Interface | Main benefit | Main limitation | MVP disposition |
|---|---:|---|---|---|---|
| Packaged wired magnetic reed contact | None | Two conductors + GPIO | Passive, simple, contactless, already owned | Generic commercial variants are not controlled | **Accepted** |
| Bare reed switch + selected magnet | None | Two conductors + GPIO | Controllable component choice | Requires custom protection/packaging | Deferred fallback |
| Digital Hall sensor | Active supply | Supply + ground + digital output | Semiconductor output, no reed contact | Adds powered electronics and integration complexity | Rejected for primary MVP |
| Mechanical microswitch | None | Two/three conductors + GPIO | Controlled industrial parts available | Requires mechanical actuation, force and travel | Rejected for primary MVP |
| Wireless door contact | Battery/radio | Wireless protocol | No signal cable | Adds battery, radio, pairing and lifecycle complexity | Rejected |
| Supervised loop / tamper circuit | Depends | Multi-threshold/fault model | Can distinguish some wiring faults | Expands architecture and security semantics | Rejected for MVP |

Representative technology references:

- [Espressif ESP32-C3 GPIO guide](https://docs.espressif.com/projects/esp-idf/en/stable/esp32c3/api-reference/peripherals/gpio.html)
- [Espressif ESP32-C3 Series Datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-c3_datasheet_en.pdf)
- [Standex Detect — Reed Switch Operational Characteristics](https://standexdetect.com/resources/reed-technology-academy/reed-switch-characteristics/reed-switch-operational-characteristics/)
- [Texas Instruments DRV5032 datasheet](https://www.ti.com/lit/ds/symlink/drv5032.pdf)
- [Omron D2F datasheet](https://omronfs.omron.com/en_US/ecb/products/pdf/en-d2f.pdf)

These references characterize technologies or controlled example parts; they do not characterize the generic owned MC-38 specimen.

### 1.2 Reviewed physical evidence

The lean guided protocol was executed on owned specimen `MC38-A` under evidence ID `IHAP47-MC38-A-01`.

Reviewed results:

| Observation | Result |
|---|---|
| Magnet FAR | raw `1`, electrical open |
| Magnet NEAR | raw `0`, electrical closed |
| Reed-form interpretation | Form A / normally open relative to magnetic actuation |
| Complete near/far cycles | `20/20` |
| Stable movements | `40/40` |
| Mismatches | `0` |
| Buffer overflows | `0` |
| Movements with >1 observed raw transition | `0/40` at `250 us` sampling |
| One conductor disconnected | raw `1` |
| GPIO6 to GND bench check | raw `0` |
| Temporary internal pull-up | adequate for this bench session |
| Physical decision gate | **PASS** |

The raw local session is preserved outside the repository. Only reviewed, sanitized decision evidence is committed.

No additional transition was observed in the 40 movements at the `250 us` harness sampling resolution. This is not an oscilloscope-grade proof that physical bounce cannot occur.

---

## 2. Decision

```text
Use passive, wired, two-conductor magnetic reed-contact technology
as the MVP door-state sensor class.

MC38-A passed the owned-specimen physical decision gate and is accepted
as the tested local MVP reference specimen.

Do not treat the generic MC-38/DC-38 commercial label as a controlled
replacement specification.
```

For the tested specimen and temporary bench topology:

- magnet FAR -> electrical open -> `HIGH` / raw `1`;
- magnet NEAR -> electrical closed -> `LOW` / raw `0`;
- one contact conductor connects to the ESP32-C3 input;
- the other contact conductor connects to ground;
- the input is biased high by a pull-up.

The failure-mode test confirms that an interrupted conductor and a legitimate open electrical contact both produce `HIGH`. Therefore the selected simple topology **does not provide wire supervision or fault distinction**.

The following remain outside this ADR:

- final GPIO;
- internal versus external production pull-up and resistor value;
- production polling/interrupt strategy and debounce;
- cable, connector and ESD/protection;
- installation gap, alignment margin, bracket, adhesive and enclosure;
- quantitative current/autonomy;
- tamper or supervised-loop behavior;
- controlled replacement SKU and cross-lot equivalence.

The Project Owner explicitly accepted this decision on 2026-09-01.

---

## 3. Alternatives and disposition

| Alternative | Outcome | Reason |
|---|---|---|
| Owned packaged MC38-A reed contact | **Accepted local tested reference** | Passive, deterministic in reviewed bench evidence, already owned, proportionate to binary telemetry |
| Controlled packaged reed contact with manufacturer P/N | Deferred fallback | Use if replacement reproducibility becomes necessary |
| Bare reed + separate magnet | Deferred | Adds packaging/protection work |
| Digital Hall sensor | Rejected primary | Active supply and additional design complexity without demonstrated MVP need |
| Mechanical microswitch | Rejected primary | Mechanical actuation and mounting/wear constraints |
| Wireless battery contact | Rejected | Adds radio, provisioning and battery lifecycle |
| Supervised loop | Rejected for MVP | Adds fault-state/security semantics and circuit complexity |

---

## 4. Consequences

### Positive

- passive sensor: no active sensor supply;
- two signal conductors and one digital input;
- simple, deterministic binary behavior demonstrated on the owned specimen;
- no new protocol or battery lifecycle;
- automated test procedure minimizes operator effort and preserves raw evidence;
- technology remains replaceable independently of the generic MC-38 label.

### Negative / limitations

- generic MC-38/DC-38 is not a controlled part number;
- open contact and interrupted conductor are electrically indistinguishable;
- short-to-ground / failed-closed conditions can appear as a closed circuit;
- replacement equivalence remains `[UNVALIDATED]`;
- production reliability is not established;
- final mounting geometry is not established;
- final integrated pull/cable/protection behavior is not established.

### Operational boundary

- `HIGH` and `LOW` are electrical states, not security conclusions;
- external behavior remains binary door-state telemetry;
- no sensor-fault/tamper state is introduced;
- the product must not silently claim alarm, antifurto, access-control or intrusion-detection capability.

---

## 5. Related risk

| Risk | Treatment in this ADR | Remaining exposure |
|---|---|---|
| [R-004 — Presence and Door State Misinterpretation](../risks/records/R-004-presence-door-state-misinterpretation.md) | Explicit telemetry-only semantics and prohibited security claims | Later software/stakeholder wording can still over-interpret binary state |

This ADR does not accept or close R-004.

---

## 6. Downstream handoff

| Topic | Owner |
|---|---|
| Final GPIO, pull network, cable/interface behavior, protection and production debounce | IHAP-50 |
| Quantitative closed-loop current / power impact | IHAP-49 |
| Mounting gap, alignment margin, attachment and enclosure integration | IHAP-51 |
| Controlled fallback/replacement SKU and BOM evidence | IHAP-17 / IHAP-43 |
| Production door-state acquisition | Future implementation task |
| Stable external event/schema semantics | Event-contract task / implementation |

Repeated gap/alignment sweeps are not an IHAP-47 acceptance gate. They belong to IHAP-51 when actual mounting geometry exists.

---

## 7. Evidence

| Evidence | Link |
|---|---|
| Reviewed run record | [`IHAP47-MC38-A-01/run-record.md`](../evidence/IHAP-47/IHAP47-MC38-A-01/run-record.md) |
| Reviewed machine summary | [`IHAP47-MC38-A-01/summary.json`](../evidence/IHAP-47/IHAP47-MC38-A-01/summary.json) |
| Evidence manifest | [`docs/evidence/IHAP-47/README.md`](../evidence/IHAP-47/README.md) |
| Lean automated protocol | [`test-protocol.md`](../evidence/IHAP-47/test-protocol.md) |
| Validation harness | [`tools/hardware-validation/ihap-47-door-state-sensor/`](../../tools/hardware-validation/ihap-47-door-state-sensor/) |
| Pull request | [PR #26](https://github.com/pianic2/homeedge-ai-platform/pull/26) |
| Related risk | [`R-004`](../risks/records/R-004-presence-door-state-misinterpretation.md) |

---

## 8. Review notes

```text
[x] One stable architectural decision.
[x] Physical decision evidence executed and reviewed.
[x] Tested specimen boundary explicit.
[x] Open-vs-disconnected-wire limitation experimentally demonstrated.
[x] Raw logs remain local; publication evidence sanitized.
[x] Final GPIO/pull/cable/debounce deferred to IHAP-50.
[x] Power deferred to IHAP-49.
[x] Mounting geometry deferred to IHAP-51.
[x] No production/security/alarm/tamper/access-control claim introduced.
[x] R-004 remains open and authoritative.
[x] Project Owner acceptance recorded on 2026-09-01.
```

ADR-0003 is Accepted. MC38-A is the tested local reference specimen; generic MC-38/DC-38 replacement equivalence remains `[UNVALIDATED]`.
