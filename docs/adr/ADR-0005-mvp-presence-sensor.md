# ADR-0005 — MVP Presence Sensor

**Status:** Proposed
**Date:** 2026-09-01
**Project:** [ITS] [EDGE] HomeEdge AI Platform
**Jira:** [IHAP-46](https://niccolopiazzi01.atlassian.net/browse/IHAP-46)
**PR:** [#25](https://github.com/pianic2/homeedge-ai-platform/pull/25)
**Supersedes:** None
**Superseded by:** None

<!--
AI_AGENT_METADATA:
  document_type: architecture_decision_record
  decision_scope: mvp_local_non_identifying_presence_sensor
  issue: IHAP-46
  parent_issue: IHAP-43
  status: Proposed
  approval_authority: project_owner
  approval_recorded: false
  source_of_truth: github_versioned_repository_documentation
  proposed_technology: hlk_ld2410c_class_24ghz_presence_radar
  tested_owned_specimen: LD2410C-HLK-V1.1-OWNED-01
  tested_interface: receive_only_uart_256000_baud
  product_output: presence_detected_boolean_only
  quantitative_power_issue: IHAP-49
  final_interconnect_issue: IHAP-50
  final_mounting_issue: IHAP-51
  definitive_bom_issue: IHAP-17
  residual_physical_gate: completed
  unvalidated_claim_marker: "[UNVALIDATED]"

HIDDEN_ANTI_REGRESSION_RULES:
  - Keep one decision: the presence-sensing technology for the reference MVP.
  - Do not mark this ADR Accepted without explicit Project Owner approval.
  - Keep the product/event boundary at presence_detected boolean only.
  - Treat detailed radar fields as local laboratory diagnostics only.
  - Do not authorize coordinates, trajectory, identity, person count, behavioral history, persistent raw radar, occupancy guarantees, alarm, antifurto, intrusion detection, safety or protection claims.
  - Do not convert one tested HLK-LD2410C V1.1 specimen into universal seller, lot or replacement equivalence.
  - Keep quantitative power in IHAP-49, final pinout/interconnect in IHAP-50, mounting/enclosure in IHAP-51 and definitive BOM propagation in IHAP-17.
-->

---

## 1. Context

The Product Vision includes a current room-level presence state for the generic
room/door node. The state is local and non-identifying. It is telemetry, not an
occupancy guarantee, identity signal, individual history, alarm or protection
function.

IHAP-46 compares only three proportionate choices:

1. the owned HLK-LD2410C V1.1 presence-radar specimen;
2. a conventional PIR motion-sensor class;
3. no presence sensor.

Hi-Link describes LD2410C as a 24 GHz indoor presence module intended to detect
moving and stationary/micro-moving human targets. The family exposes GPIO and
UART outputs and configurable range/sensitivity/unmanned-delay behavior:

- https://www.hlktech.net/index.php?id=1184
- https://www.hlktech.net/index.php?id=1154

Panasonic describes PIR operation as detecting changes in incident infrared
energy and documents that field of view can be constrained by mounting, masks
or optical apertures:

- https://na.industrial.panasonic.com/blog/pir-motion-sensors-technology-low-power-or-line-power-applications-and-lens-options
- https://api.pim.na.industrial.panasonic.com/file_stream/main/fileversion/244673

These sources characterize the technology families. They do not validate the
owned specimen or a generic low-cost PIR board.

### 1.1 Reviewed physical evidence

The owned specimen is visibly marked `HLK-LD2410C` and `V1.1`. A receive-only
laboratory path was tested with LD2410C TX connected to ESP32-C3 GPIO5 at
256000 baud. LD2410C RX and OUT remained disconnected.

Reviewed evidence establishes for the owned specimen and tested setups:

- `EMPTY-02`: 300.007 s, 3,001 samples, presence ratio 0.000, zero invalid radar frames;
- strict `ENTER-02`: 6,535 valid UART samples, zero invalid radar frames and ten valid clear preconditions;
- strict `ENTER-02`: all ten repetitions eventually reported presence, with presence ratios from 0.917 to 0.993;
- strict `ENTER-02`: 7/10 repetitions met the original 2,000 ms operational-onset threshold.
- `STILL-02`: 300.008 s with 3,000/3,000 presence samples and zero invalid radar frames;
- corrected `EXIT-04`: eventual release in both clean repetitions, but both failed the original 10,000 ms operational release gate at 18,506 ms and 18,754 ms from `START NOW`;
- `ADJ-CLOSED-01`: zero presence in 1,200 samples over 120.009 s on the tested external corridor path;
- `ADJ-OPEN-01`: zero presence in 1,200 samples over 120.010 s on the same path, with the door open about 30 degrees and the threshold never crossed.

The operational onset includes operator reaction and travel. It is not isolated
radar-processing latency. Three threshold failures remain recorded as failures.

The exit measurement includes normal operator travel and door closing. The
operator estimated that at about 5–7 seconds; no machine marker exists at door
closure, so the estimate is not subtracted. The two clean failures characterize
an operational release limitation rather than isolated radar-processing delay.

The adjacent-space results are limited to the stated path, placement, door
conditions and owned specimen. They do not establish universal immunity through
walls or doorways. The lean physical gate is complete; no further physical run
is required for this decision.

### 1.2 Capability and data boundary

The decision distinguishes three layers:

| Layer | Allowed use |
|---|---|
| Hardware capability | The module may internally calculate richer target and distance data. |
| Local validation/configuration | UART telemetry may be captured temporarily in a controlled local evidence run; configuration access may be used only by a future reviewed implementation. |
| Product/event boundary | At most `presence_detected: true \| false`, or an equivalent current local state. |

Coordinates, trajectories, identity, person count, behavioral profiles,
persistent raw radar and individual room history are not authorized. Bluetooth
is not an MVP requirement and is not authorized as an unattended product
control surface by this ADR.

---

## 2. Decision

```text
Proposed decision:

Select one HLK-LD2410C-class 24 GHz presence-radar module as the reference
MVP technology for local, non-identifying room presence, subject only to
explicit Project Owner acceptance of this Proposed ADR.

Authorize only a current boolean presence state across the product/event
boundary. Keep detailed radar telemetry local to controlled diagnostics.
```

The owned `HLK-LD2410C V1.1` is the tested local reference specimen. It is not
a controlled universal replacement SKU.

The tested integration path is receive-only UART. Final firmware may retain
UART only when justified by configuration, diagnostics and pin budget; final
GPIO/UART wiring remains IHAP-50. GPIO OUT is not a blocking decision test when
the reviewed UART path is sufficient. Quantitative current, rail and autonomy
remain IHAP-49.

This proposed decision does not accept itself. The physical decision evidence
is complete and specialist review records no blocker or major finding.
Acceptance remains pending only at the Project Owner decision gate.

---

## 3. Alternatives Considered

| Criterion | LD2410C | Conventional PIR | No presence sensor |
|---|---|---|---|
| Moving presence | Demonstrated on the owned specimen, with recorded onset limitations | Technology is intended for motion/change detection; no identified owned specimen was qualified | Not available |
| Stationary presence | Demonstrated for 300 seconds on the owned specimen | Weak fit for a current-presence state because the sensing principle depends on infrared change | Not available |
| Adjacent-space behavior | No detection on the tested 120-second corridor path with the door closed or open about 30 degrees; other placements remain `[UNVALIDATED]` | Optical field of view can be constrained; exact module/lens behavior remains `[UNVALIDATED]` | No false presence because no signal exists |
| Complexity | 5 V module supply plus UART/GPIO choices and configuration surface | Typically simpler digital motion output | Lowest |
| Power | Qualitatively higher and continuously active; quantitative evidence belongs to IHAP-49 | Qualitatively lower for common low-power PIR classes; exact candidate not costed/tested | Zero |
| ESP32-C3 integration | Receive-only UART physically demonstrated; final pinout pending IHAP-50 | Simple GPIO direction, but no physical comparison specimen | None |
| Privacy | Hardware exposes richer local diagnostics; product boundary restricts output to boolean | Naturally coarse motion output; still creates timestamp/inference risk if retained | No presence telemetry |
| Cost evidence | EUR 4.39 acquired unit cost; dated official listing USD 4.98; replacement equivalence `[UNVALIDATED]` | Exact candidate cost `[UNVALIDATED]` | Zero |
| Replacement | Manufacturer family is listed; PCB/seller/lot equivalence remains `[UNVALIDATED]` | Broad technology availability, but no controlled candidate profile is selected | Not applicable |
| Testability | Structured UART supports automated acquisition and limitation analysis | GPIO is simple but provides less diagnostic evidence | No sensing behavior to test |
| Product fit | Best fit: stationary presence is demonstrated and the boolean-only boundary is defined; onset/release limitations are explicit | Suitable for motion-trigger use, not sufficient for the intended current-presence state | Conflicts with the current Product Vision presence capability |

No additional sensor technology is introduced because none changes the current
decision with proportionate evidence.

---

## 4. Consequences

### Positive

- preserves the intended distinction between moving and substantially stationary presence;
- keeps all authorized product output coarse and non-identifying;
- uses an already-owned, identified and partially qualified specimen;
- supports automated local evidence capture;
- avoids adding an unqualified PIR solely to create a physical comparison;
- preserves replacement at the technology/profile level rather than relying only on a seller label.

### Negative / limitations

- continuously active radar is qualitatively more complex and power-demanding than a PIR;
- richer UART diagnostics increase privacy and logging exposure if boundaries are not enforced;
- adjacent-space detections may require placement and sensitivity constraints;
- 3/10 strict entry repetitions exceeded the original 2,000 ms operational threshold;
- both clean corrected exit repetitions exceeded the original 10,000 ms operational release threshold;
- adjacent-space evidence covers only the tested path and does not guarantee immunity in other layouts;
- one tested specimen does not prove seller, lot or population-wide equivalence;
- exact replacement availability, landed price and revision continuity can change;
- no occupancy, safety, alarm, antifurto, intrusion-detection or protection guarantee is created.

### Neutral / operational

- the Product Vision already authorizes only local non-identifying presence;
- raw run telemetry remains local and only reviewed aggregates are published;
- final pin assignment, power budget and enclosure are downstream decisions;
- production firmware and stable event-schema enforcement are separate implementation work.

---

## 5. Related Risks and Treatments

| Risk | Effect | Remaining exposure |
|---|---|---|
| [R-002 — Event Payload Leakage](../risks/records/R-002-event-payload-leakage.md) | Boolean-only product boundary minimizes payload | Runtime schema, logging, transport and retention remain `[UNVALIDATED]` |
| [R-003 — Technical Metadata Inference](../risks/records/R-003-technical-metadata-inference.md) | Blocks detailed domestic geometry and raw radar from stakeholder evidence | Timestamp/room-state correlation remains a future implementation risk |
| [R-004 — Presence and Door State Misinterpretation](../risks/records/R-004-presence-door-state-misinterpretation.md) | Explicitly rejects tracking, occupancy guarantee, alarm and protection interpretations | Stakeholder wording and runtime enforcement remain active controls |
| [R-007 — AI Inference and Profiling](../risks/records/R-007-ai-inference-profiling.md) | Blocks identity, routine profiling and behavioral-history use | Future AI work requires a separate reviewed scope |

This ADR does not accept, close or resolve any Risk Record. Residual-risk
authority remains with the Project Owner.

---

## 6. Follow-up Work

| Item | Tracking |
|---|---|
| Quantify voltage/current/rail/autonomy impact | IHAP-49 |
| Freeze UART/GPIO path, pins, connectors and protection | IHAP-50 |
| Define placement, range constraint, mounting and enclosure | IHAP-51 |
| Propagate accepted reference quantity and cost | IHAP-17 / IHAP-43 after acceptance |
| Implement boolean-only production semantics | Future firmware/event-contract implementation task |

---

## 7. Evidence Links

| Evidence | Link |
|---|---|
| Jira issue and Project Owner gate | [IHAP-46](https://niccolopiazzi01.atlassian.net/browse/IHAP-46) |
| Pull request | [PR #25](https://github.com/pianic2/homeedge-ai-platform/pull/25) |
| Physical evidence index | [IHAP-46 evidence](../evidence/IHAP-46/README.md) |
| Reviewed runs | [Reviewed run checkpoint](../evidence/IHAP-46/reviewed-runs.md) |
| Machine-readable checkpoint | [Existing run summary](../evidence/IHAP-46/existing-run-summary.json) |
| Acquisition/replacement evidence | [Replacement sourcing](../evidence/IHAP-46/replacement-sourcing.md) |
| Validation harness | [IHAP-46 harness](../../tools/hardware-validation/ihap-46-presence-sensor/README.md) |
| Product boundary | [Product Vision](../product/product-vision.md) |

---

## 8. Review Notes

```text
[x] One stable decision only.
[x] LD2410C is compared with PIR and no sensor.
[x] Hardware capability, local diagnostics and product/event output are separated.
[x] Detailed radar persistence, tracking, identity, person count and behavioral history are rejected.
[x] Power, wiring, mounting and BOM ownership remain in their existing tasks.
[x] Existing physical failures and limitations are preserved without threshold rewriting.
[x] No alarm, antifurto, intrusion-detection, safety, occupancy-guarantee or protection claim is introduced.
[x] Residual stationary, release and adjacent-space physical gate reviewed.
[x] Final specialist review records BLOCKER 0 / MAJOR 0.
[ ] Explicit Project Owner acceptance or rejection recorded.
```
