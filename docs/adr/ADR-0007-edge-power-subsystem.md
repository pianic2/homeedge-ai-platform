# ADR-0007 — Edge Power Subsystem

**Status:** Proposed  
**Date:** 2026-09-05  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Jira:** [IHAP-49](https://niccolopiazzi01.atlassian.net/browse/IHAP-49)  
**PR:** [#34](https://github.com/pianic2/homeedge-ai-platform/pull/34)  
**Supersedes:** None  
**Superseded by:** None

<!--
AI_AGENT_METADATA:
  document_type: architecture_decision_record
  issue: IHAP-49
  status: Proposed
  approval_authority: project_owner
  source_of_truth: github_versioned_repository_documentation
  jira_role: workflow_state_and_evidence_links
  confluence_role: stakeholder_navigation_only
  unvalidated_claim_marker: "[UNVALIDATED]"
  task_scope: edge_power_subsystem_decision
  runtime_changes_allowed: false
  firmware_changes_allowed: false

HIDDEN_ANTI_REGRESSION_RULES:
  - Keep one stable architectural decision: normal regulated 5 V USB-C supply with rechargeable single-cell battery backup only.
  - Do not convert planning current or capacity arithmetic into a validated autonomy claim.
  - Do not accept the selected cell, holder, charger/protection thresholds, converter or source-selection implementation without traceable physical evidence where required.
  - Do not infer seamless UPS/load-sharing behavior from a generic 4056-family charger board.
  - Do not claim safe, certified, fire-safe, compliant, production-ready or installable from prototype evidence.
  - IHAP-50 owns final interconnect implementation; IHAP-51 owns final enclosure/mounting implementation.
  - IHAP-17 receives definitive BOM lines only after Project Owner acceptance.
-->

---

## 1. Context

The reference MVP edge node combines an ESP32-C3 board, HLK-LD2410C-class presence radar, one accepted environmental-sensor profile, a passive reed-contact input and the accepted local OLED display.

The presence radar requires a 5 V domain and is an always-on material load. Planning evidence for IHAP-49 places the complete node near an engineering central estimate of roughly 0.625 W at the 5 V load domain, with significant uncertainty from ESP32-C3/Wi-Fi duty cycle, the owned SuperMini-compatible board and the OLED. The estimate is not a measurement.

A single 3.5 Ah-class 1S Li-ion cell is therefore an hours-scale source for this node rather than a multi-day primary supply. The Project Owner has decided that autonomous multi-day battery operation is not an MVP requirement. The node shall normally be powered from regulated 5 V over USB-C, while a rechargeable battery remains in scope only as continuity backup for blackout or cable/input interruption.

The owned hardware includes:

- a USB-C charger/protection board with charger IC visibly marked `4056E`, an `8205A` dual MOSFET and a separate six-pin protection-controller device whose exact identity/thresholds remain `[UNVALIDATED]`;
- an 18650 holder measured by the Project Owner at approximately 70 mm maximum useful length with the spring fully compressed and approximately 18 mm maximum cell width/diameter. The holder body is reported by the Project Owner as slightly compliant and is retained as the reference-holder candidate, but actual fit/contact pressure with the selected cell remains `[UNVALIDATED]` until the cell arrives.

The selected cell candidate is **LG INR18650-MJ1**, EAN/GTIN `8438493099829`, 18650 flat-top unprotected Li-ion, selected on a cost-first basis after meeting the minimum provenance, electrical-envelope and reproducibility threshold. Seller evidence lists 3.6 V nominal, 3500 mAh typical, 3400 mAh minimum, 10 A discharge capability and approximately 18.2 mm × 65 mm dimensions. Procurement/received-specimen evidence and physical integration remain pending.

The power subsystem is safety-sensitive. Component ownership or low purchase price does not prove electrical compatibility, adequate protection, acceptable thermal behavior or valid runtime.

---

## 2. Decision

```text
We will power the reference MVP edge node normally from a regulated 5 V USB-C source.

We will retain a rechargeable single-cell Li-ion battery subsystem only as backup
for blackout or normal-input/cable interruption.

The backup cell selected for procurement and validation is LG INR18650-MJ1,
EAN/GTIN 8438493099829, flat-top unprotected 18650 Li-ion.

The backup path will feed the same regulated 5 V node domain through an explicit
conversion and source-selection/isolation design. The battery is not the primary
continuous source and multi-day standalone operation is not an MVP requirement.
```

This section becomes authoritative only when the ADR status is `Accepted` by the Project Owner.

### 2.1 Power-domain contract

The Proposed domain structure is:

```text
regulated 5 V USB-C normal source
              |
              +--------------------------+
              |                          |
              |                    source selection /
              |                    isolation stage
              |                          |
              |                          v
              |                  regulated 5 V node bus
              |                     |            |
              |                     v            v
              |                  LD2410C     ESP32-C3 board
              |                                  |
              |                                  v
              |                            onboard 3.3 V
              |                           /      |       \
              |                    DHT11/BME280 OLED  reed network
              |
              +--> 4056E-family charger/protection --> LG INR18650-MJ1
                                      |
                                      v
                               protected output
                                      |
                                      v
                           1S -> regulated 5 V converter
                                      |
                                      +----> source selection /
                                             isolation stage
```

The exact source-selection/isolation topology remains `[UNVALIDATED]` and must prevent prohibited backfeed between the normal source and battery path.

### 2.2 Battery role and selected cell

The backup battery exists for continuity through blackout or cable/input interruption. It is not intended to make the node a multi-day off-grid device.

The selected cell candidate for procurement/validation is **LG INR18650-MJ1**:

- EAN/GTIN `8438493099829`;
- 18650 flat-top, unprotected Li-ion;
- seller-listed 3.6 V nominal;
- seller-listed 3500 mAh typical / 3400 mAh minimum;
- seller-listed 10 A discharge capability;
- seller-listed approximately 18.2 mm diameter × 65 mm height.

Selection is cost-first: once minimum compatibility, provenance and evidence thresholds are satisfied, lower total procurement/replication cost is preferred over stronger documentation that does not materially improve the node requirement.

A 3.5 Ah-class 1S cell has a current planning estimate of approximately 12–20 h backup runtime, with roughly 16 h as a central arithmetic estimate under the current load model. **Backup autonomy remains `[UNVALIDATED]` until a controlled discharge run is completed with the frozen implementation.**

### 2.3 Charging and power-path rule

The owned 4056E-family board is a charger/protection candidate, not evidence of a complete system load-sharing/UPS controller.

Until an explicit power-path implementation is selected and validated:

- charging while the node is operating from the battery path is **prohibited**;
- seamless no-reset switchover is **not assumed**;
- whether source loss may cause one controlled reboot or must preserve uninterrupted operation remains a validation/implementation decision inside IHAP-49.

### 2.4 Exact component acceptance remains open

The ADR has selected the **LG INR18650-MJ1** cell model for procurement and validation, but physical acceptance of the received specimen remains pending.

The ADR does **not** yet accept:

- the received cell specimen/lot as conforming before markings/condition are checked;
- the owned holder/cell fit as physically validated;
- an exact 1S-to-5 V converter;
- an exact source-selection/isolation circuit;
- the exact protection-controller identity or trip thresholds on the owned 4056E board;
- a definitive normal-source PSU/cable SKU;
- a validated backup runtime.

Those details must be closed with evidence inside the same IHAP-49 branch and PR before this ADR can be accepted.

---

## 3. Alternatives Considered

| Alternative | Outcome | Reason |
|---|---|---|
| Regulated 5 V USB-C only | Rejected as complete subsystem; retained as normal source | Lowest complexity but does not satisfy the Project Owner requirement for blackout/cable-fault backup. |
| Rechargeable 1S battery as primary source | Rejected | Current load model makes a single 18650 an hours-scale source; multi-day standalone operation is not an MVP requirement. |
| Normal 5 V USB-C + rechargeable 1S backup | **Selected architecture class, Proposed** | Matches the actual continuity requirement while keeping the stable node domain at regulated 5 V. |
| Protected 18650 + charger/regulator | Rejected for current reference direction | Duplicated cell-level protection adds cost/length without a demonstrated need if the system-level protection stage is qualified. |
| LG INR18650-MJ1 unprotected + verified charger/protection + regulator | **Selected implementation direction for procurement/validation** | Meets the required capacity/current envelope at lower cost than higher-priced branded alternatives while retaining identifiable model/provenance. Physical and protection validation remain mandatory. |
| Other branded 3.4–3.5 Ah unprotected 18650 cells | Acceptable alternatives, not selected | Samsung/LG/Molicel/EVE-class alternatives can meet the electrical requirement, but the selected MJ1 had the preferred cost/value balance for the current order. |
| Unprotected cell + separate additional BMS/protection | Not preferred | Adds components and interfaces without a demonstrated need if the owned charger/protection stage can be qualified. |
| LiPo pouch | Rejected for current reference direction | Does not remove charging/protection/regulation/power-path constraints and adds a different mechanical handling profile without a current product requirement. |
| Replaceable primary cells | Rejected | Poor fit for an always-on 5 V radar/Wi-Fi node and does not simplify the required regulated 5 V domain. |

---

## 4. Consequences

### Positive

- Normal operation uses a simple, externally regulated 5 V USB-C source.
- The node can retain a bounded local continuity capability for blackout or cable/input interruption.
- The accepted 5 V LD2410C domain does not change between normal and backup operation.
- Battery capacity can be sized for backup duration rather than multi-day primary autonomy.
- Cost remains the first differentiator after minimum technical/provenance thresholds are met.
- A USB power meter is not required as a prerequisite; ordinary multimeter measurements plus reset/brownout evidence are sufficient for the initial validation plan, with escalation to higher-bandwidth instrumentation only if transient behavior cannot otherwise be bounded.

### Negative / Trade-offs

- Battery backup still introduces cell, holder, charging, protection, conversion, source-selection, reverse-polarity, backfeed and enclosure constraints.
- The backup path requires conversion from a 1S Li-ion voltage range to regulated 5 V.
- The source-transition behavior must be deliberately designed and tested.
- The selected LG MJ1 is an unprotected cell, so system-level protection is mandatory and must be validated.
- The owned holder fit is still a physical hypothesis until the selected cell arrives.
- The exact protection behavior of the owned generic charger/protection board is not yet known.
- Battery autonomy must be physically measured; capacity arithmetic alone is insufficient.

### Neutral / Operational

- DHT11 remains the standard-indoor profile and BME280 the precision/extended profile; they are not summed as simultaneous reference loads.
- The passive reed-contact decision is unchanged.
- The accepted OLED remains part of the reference node.
- Audio remains excluded from the reference MVP.
- IHAP-50 owns final interconnect implementation.
- IHAP-51 owns enclosure/mounting implementation.
- IHAP-17 receives definitive power BOM lines only after Project Owner acceptance of IHAP-49.

---

## 5. Related Risks and Treatments

No existing canonical Risk Record was found that should be silently repurposed as the battery/power treatment dossier during this execution pass. IHAP-49 therefore records its current technical risks in `docs/evidence/IHAP-49/risk-assessment.md` and does not claim that an existing project risk is resolved.

| Risk | Treatment | Effect | Remaining exposure |
|---|---|---|---|
| Normal-source loss / node reset | IHAP-49 source-selection and recovery validation | Partially mitigates | Transfer/reboot behavior `[UNVALIDATED]` |
| Battery over-charge / over-discharge / over-current | Charger/protection qualification + selected unprotected-cell policy | Partially mitigates | Protection-controller identity/thresholds `[UNVALIDATED]` |
| Reverse cell insertion | Electrical and/or IHAP-51 mechanical mitigation | Leaves unresolved pending design | Mitigation not frozen |
| Backfeed between sources | Explicit isolation/source-selection design | Leaves unresolved pending design | Topology not frozen |
| Brownout from load/transients | Current/rail measurements + reset logging + headroom | Partially mitigates | Integrated transient peak `[UNVALIDATED]` |
| Unsupported autonomy expectation | Backup-only product boundary + controlled discharge test | Avoids false claim | Measured runtime `[UNVALIDATED]` |
| Holder mechanical interference/contact stress | Non-destructive fit/contact inspection of received MJ1 | Leaves unresolved pending test | Physical fit `[UNVALIDATED]` |

---

## 6. Follow-up Work

| Item | Tracking |
|---|---|
| Confirm procurement and inspect received LG INR18650-MJ1 cell markings/condition | IHAP-49, same branch/PR |
| Validate selected MJ1 fit/contact pressure in the owned holder | IHAP-49, same branch/PR |
| Select 1S-to-regulated-5 V converter | IHAP-49, same branch/PR |
| Select source-selection/isolation implementation | IHAP-49, same branch/PR |
| Verify charger current configuration and protection behavior | IHAP-49, same branch/PR |
| Measure integrated normal-source current and rails | IHAP-49 validation evidence |
| Test source interruption and restoration | IHAP-49 validation evidence |
| Run controlled backup-endurance test | IHAP-49 validation evidence |
| Freeze final physical interconnect | IHAP-50 |
| Freeze battery accessibility/mounting/enclosure constraints | IHAP-51 |
| Propagate definitive BOM lines after acceptance | IHAP-17 |
| Reconcile parent hardware baseline after acceptance | IHAP-43 |

---

## 7. Evidence Links

| Evidence | Link |
|---|---|
| Jira issue | [IHAP-49](https://niccolopiazzi01.atlassian.net/browse/IHAP-49) |
| Pull request | [PR #34](https://github.com/pianic2/homeedge-ai-platform/pull/34) |
| Project Owner decision record | `docs/evidence/IHAP-49/decision-record.md` |
| Owned hardware evidence | `docs/evidence/IHAP-49/owned-hardware-evidence.md` |
| Power tree | `docs/evidence/IHAP-49/power-tree.md` |
| Planning power/autonomy budget | `docs/evidence/IHAP-49/power-budget.md` |
| Alternatives | `docs/evidence/IHAP-49/alternatives.md` |
| Validation plan | `docs/evidence/IHAP-49/validation-plan.md` |
| Preliminary risk assessment | `docs/evidence/IHAP-49/risk-assessment.md` |
| Cost governance | `docs/evidence/IHAP-49/cost-governance.md` |
| Downstream contracts | `docs/evidence/IHAP-49/downstream-contracts.md` |
| Review checklist | `docs/evidence/IHAP-49/review-checklist.md` |
| Related ADRs | ADR-0001, ADR-0002, ADR-0003, ADR-0004, ADR-0005 |

Primary manufacturer/seller sources used for planning are registered in `docs/evidence/IHAP-49/source-register.md`.

---

## 8. Review Notes

```text
[x] One stable architectural decision only.
[x] ADR necessity is explicit; coupled power architecture needs traceability.
[x] Current power/battery risks and remaining exposure are explicit.
[x] The ADR is not treated as risk acceptance or closure evidence.
[x] Source-of-truth boundaries are preserved.
[x] MVP boundary is explicit: normal wired 5 V + backup battery only.
[x] LG INR18650-MJ1 selected for procurement/validation on a cost-first basis.
[x] [UNVALIDATED] is preserved on unproven claims.
[x] No production-ready, commercial-ready, security-grade, certified, safety-critical,
    fire-safe, alarm-grade, antifurto, access-control, intrusion-detection or protection
    claim is introduced.
[ ] Received cell provenance/condition and holder fit validated.
[ ] Converter/source-selection implementation validated.
[ ] Integrated normal-source and backup-path validation complete.
[ ] Backup autonomy measured.
[ ] Complete replication cost frozen.
[ ] Project Owner acceptance recorded before status becomes Accepted.
```
