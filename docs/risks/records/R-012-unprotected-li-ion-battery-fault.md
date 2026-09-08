# Risk Assessment — Unprotected 1S Li-ion Battery Fault and Cell-Side Protection

**Risk ID:** R-012  
**Risk status:** Newly Identified  
**Current assessment date:** 2026-09-08  
**Last reviewed:** 2026-09-08  
**Next review:** explicit Project Owner treatment decision, IHAP-55 schematic review, received-cell qualification, or material battery/protection topology change  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Jira:** IHAP-49 / IHAP-55 / IHAP-57  
**Related remediation:** IHAP-56  
**Related ADR:** `docs/adr/ADR-0007-edge-power-subsystem.md`  
**Owner decision:** Pending

<!--
AI_AGENT_METADATA:
  document_type: risk_record
  source_of_truth: github_versioned_repository_documentation
  jira_role: operational_coordination_only
  confluence_role: stakeholder_summary_and_navigation_only
  risk_acceptance_authority: project_owner
  related_adr: docs/adr/ADR-0007-edge-power-subsystem.md
  primary_treatment: RT-R012-01
  treatment_lifecycle: Proposed
  unvalidated_claim_marker: "[UNVALIDATED]"

HIDDEN_ANTI_REGRESSION_RULES:
  - The selected LG INR18650-MJ1 is unprotected; do not imply cell-level protection exists.
  - PMIC SYS/boost current limiting must not be treated as protection for a short on holder leads or BAT net upstream of the PMIC.
  - Procedure-only reverse-polarity mitigation is prohibited.
  - Electrical reverse blocking requires bounded functional verification; mechanical keying must physically prevent ordinary reverse insertion.
  - Cell-side over-current interruption, charging limits, NTC behavior, low-voltage behavior, thermal behavior and polarity controls remain [UNVALIDATED] until IHAP-55 evidence exists.
  - RT-R012-01 remains Proposed until explicit Project Owner treatment approval evidence exists.
  - Do not describe the subsystem as safe, certified, fire-safe, production-ready or compliant.
-->

---

## 1. Risk Statement

```text
There is a risk that the unprotected 1S Li-ion cell, holder wiring or custom PCB is electrically or thermally overstressed because reverse insertion, a BAT-side short/over-current condition, incorrect charging, excessive discharge or temperature-control failure can occur outside the protection coverage of the downstream SYS rail.
```

---

## 2. Source Trigger and Scope

**Source trigger:** ADR-0007 selects an **unprotected LG INR18650-MJ1** in a currently unkeyed serviceable holder. The preferred MP2636-class architecture provides charger/power-path/boost controls, but output/SYS limiting alone cannot interrupt every fault path on holder leads or BAT net upstream of the PMIC. Physical implementation is not yet fabricated.

**In scope:** holder/BAT wiring, cell-side over-current interruption, reverse insertion, charge voltage/current, NTC hot/cold/open/short behavior, low-voltage cutoff/recovery, thermal operating boundaries, holder fit and service interaction.

**Out of scope:** battery certification/regulatory approval, destructive abuse testing of an actual cell, multi-cell packs, production qualification, unrelated enclosure aesthetics.

---

## 3. Affected Assets and Trust Boundary

| Area | Detail |
|---|---|
| Assets | LG MJ1 cell, holder leads, BAT net, charger/power-path PMIC, PCB, enclosure/service interface |
| Trust boundary | User/service interaction with removable cell and electrical boundary between cell/holder and PCB |
| Category | Technical / Compliance-Claims |
| Stakeholder surface | Hardware replication, installation/service instructions, battery/autonomy and maturity claims |

---

## 4. Current Assessment

| Field | Value | Rationale |
|---|---|---|
| Likelihood | Medium | Holder is not keyed and final protection implementation does not yet exist |
| Impact | High | Reverse insertion, uncontrolled BAT-side current, thermal or charging faults can damage hardware/cell and invalidate subsystem operation |
| Residual risk | Pending Evidence | A proposed treatment exists but is not approved, implemented or verified |
| Evidence gap | `[UNVALIDATED]` | No fabricated board, cell-side protection verification, NTC fault simulation, reverse-blocking functional test, thermal run or received-cell fit test |
| Decision state | Pending Project Owner | ADR acceptance is not treatment approval or residual-risk acceptance |

---

## 5. Existing Controls

| Control | Evidence | Coverage | Limitation |
|---|---|---|---|
| Backup-only battery role | ADR-0007 | Reduces duty/expectation | Does not prevent electrical faults |
| 4.2 V CV and ~1 A charge targets | ADR-0007 / IHAP-49 contract | Bounds intended charging | Implementation `[UNVALIDATED]` |
| NTC monitoring requirement | ADR-0007 | Requires temperature gating | Fault thresholds/function `[UNVALIDATED]` |
| Reverse-insertion prevention requirement | ADR-0007 | Procedure-only control explicitly rejected | Electrical/mechanical implementation `[UNVALIDATED]` |
| Owned holder dimensions and unkeyed condition recorded | `docs/evidence/IHAP-49/owned-hardware-evidence.md` | Makes mechanical risk visible | Received-cell fit remains `[UNVALIDATED]` |

Planned controls below are not existing controls.

---

## 6. Risk Treatment Summary

| Treatment ID | Title | Strategy | Lifecycle status | Jira | ADR | Last review |
|---|---|---|---|---|---|---|
| RT-R012-01 | Implement and verify system-level 1S cell protection | Mitigate | **Proposed** | IHAP-55 implementation; IHAP-57 effectiveness tracking | ADR-0007 | 2026-09-08 |

`Proposed` is mandatory here because no durable Project Owner decision explicitly approves this treatment scope yet. ADR-0007 acceptance predates the treatment record and must not be reused as implicit approval evidence.

---

## 7. Risk Treatments

### RT-R012-01 — Implement and verify system-level 1S cell protection

**Strategy:** Mitigate  
**Lifecycle status:** Proposed  
**Treatment owner:** IHAP-55 power/PCB workstream; IHAP-51 for mechanical keying/serviceability where used  
**Jira coordination:** IHAP-55 / IHAP-57  
**Related ADRs:** ADR-0007  
**Introduced:** 2026-09-07  
**Last reviewed:** 2026-09-08  
**Next review trigger:** explicit Project Owner treatment decision or IHAP-55 schematic freeze

#### Rationale

The selected cell is unprotected. The final product needs system-boundary controls including fault paths before the PMIC SYS output. PMIC boost/SYS current limiting cannot by itself protect a short on holder leads or BAT net upstream of that stage.

#### Proposed mandatory controls / actions

- place a **cell-side over-current interruption element** so relevant holder/BAT-net faults are covered before uncontrolled current can bypass PMIC SYS limiting;
- size its threshold/time from legitimate charge/discharge/transient current, conductor/trace ampacity and component characteristics;
- provide electrical reverse-battery blocking/protection **or** mechanical keying that physically prevents reverse insertion; procedure/labels are supplementary only;
- if electrical blocking is used, execute V15 with a 4.20 V current-limited battery simulator and explicit leakage/rail criteria;
- implement 4.2 V charge-voltage selection and ~1 A nominal charge target inside the source/thermal budget;
- implement NTC gating with normal/hot/cold/open/short functional verification;
- enforce MJ1 charge operation at **0–45 °C** and discharge operation at **-20–60 °C**;
- implement the first-reference low-voltage policy: cutoff **2.70 V ±0.05 V**, no deliberate operation below **2.50 V**, recovery **>=3.00 V ±0.05 V** or valid USB, with no cutoff/restart oscillation;
- verify holder fit/retention without wrapper damage or excessive insertion force.

#### Scope coverage

| Cause / consequence | Coverage | Remaining exposure |
|---|---|---|
| BAT-side short / excessive cell current | Direct | Interruption rating/behavior `[UNVALIDATED]` until schematic and V13 |
| Reverse insertion | Direct | Electrical blocker or mechanical keying `[UNVALIDATED]`; electrical path needs V15 |
| Charging over-voltage/current | Direct | PMIC configuration and V4/V14 pending |
| NTC hot/cold/open/short | Direct | Network thresholds and recovery `[UNVALIDATED]` |
| Thermal overstress | Direct | Final component thermal table and V4/V6 evidence pending |
| Over-discharge / oscillatory recovery | Direct | Numeric V10 evidence pending |
| Cell internal defect / abuse outside intended use | Partial | Not eliminated; certification/abuse qualification outside MVP claims |

#### Source and Evidence Register

| ID | Source | Source type | Supports | Version / applicability | Verification | Checked on | Limitations |
|---|---|---|---|---|---|---|---|
| SRC-01 | `docs/adr/ADR-0007-edge-power-subsystem.md` | Project decision | Unprotected cell selection and system-level protection requirement | Accepted 2026-09-07 | Verified | 2026-09-08 | Does not approve treatment lifecycle |
| SRC-02 | `docs/evidence/IHAP-49/owned-hardware-evidence.md` | Internal evidence | Unkeyed holder / owned hardware observations | Owned specimens | Verified | 2026-09-08 | Does not prove final PCB protection |
| SRC-03 | MPS MP2636 datasheet in source register | Manufacturer | PMIC charger/power-path/boost/TS behavior | Rev.1.02 | Verified | 2026-09-08 | Does not cover arbitrary upstream BAT faults |
| SRC-04 | LG INR18650-MJ1 product specification in source register | Manufacturer | 4.2 V max charge, 2.5 V discharge end, 0–45 °C charge, -20–60 °C discharge | MJ1 Rev.1 source | Verified for model | 2026-09-08 | Received lot still pending inspection |

#### Implementation and Verification Evidence

| Evidence ID | Evidence | Evidence class | Expected result | Actual result | Status |
|---|---|---|---|---|---|
| EV-01 | IHAP-55 schematic/BOM review | Implementation | Cell-side interruption, reverse control, NTC, low-voltage and thermal limits present | Not executed | `[UNVALIDATED]` |
| EV-02 | V4 NTC/charging/thermal + V14 source-limit run | Verification | Charge/NTC/source-priority behavior meets frozen limits | Not executed | `[UNVALIDATED]` |
| EV-03 | V13 controlled cell-side over-current verification | Verification | Protection interrupts/limits within frozen threshold/time without hard-shorting actual MJ1 | Not executed | `[UNVALIDATED]` |
| EV-04 | Received MJ1 / holder qualification | Verification | Correct identity/condition and non-destructive fit/retention | Not executed | `[UNVALIDATED]` |
| EV-05 | V10 low-voltage / recovery run | Verification | 2.70 V cutoff, >=3.00 V recovery, no deliberate <2.50 V discharge or oscillation | Not executed | `[UNVALIDATED]` |
| EV-06 | V15 reverse-polarity functional test when electrical blocking is used | Verification | Reversed 4.20 V simulator causes <=1 mA steady current, product rails <=0.3 V, no damage | Not executed / N/A if mechanical-only keying | `[UNVALIDATED]` |

For EV-03/EV-06 use bounded current-limited fixtures. **Do not intentionally hard-short or reverse-connect the actual Li-ion cell.**

#### Treatment Effectiveness Review

**Review date:** Pending  
**Evidence reviewed:** Pending  
**Effectiveness:** Pending Evidence  
**Likelihood after treatment:** Pending Evidence  
**Impact after treatment:** Pending Evidence  
**Residual risk:** Pending Evidence  
**Project Owner decision required:** Yes

---

## 8. Traceability

| Relationship | Link | Effect / Rule |
|---|---|---|
| Accepted ADR | `docs/adr/ADR-0007-edge-power-subsystem.md` | Defines architectural constraints; does not approve/verify RT-R012-01 |
| Implementation task | IHAP-55 | Schematic, PCB and physical tests |
| Effectiveness tracking | IHAP-57 | Treatment lifecycle/effectiveness after evidence |
| Remediation task | IHAP-56 | Creates canonical risk/treatment traceability |
| Validation contract | `docs/evidence/IHAP-49/validation-plan.md` | V4/V10/V13/V14/V15 and thermal criteria |

---

## 9. Stakeholder Visibility

Risk summary and treatment state may be shown in stakeholder summaries. Technical details should link to GitHub. Do not claim the battery subsystem is safe/certified/production-ready; treatment is Proposed and effectiveness remains `[UNVALIDATED]`.

---

## 10. Assessment History

| Date | Change | Treatment | Evidence | Decision |
|---|---|---|---|---|
| 2026-09-07 | Canonical risk created from IHAP-49 post-merge review | RT-R012-01 initially drafted | ADR-0007 + IHAP-49 evidence | Pending |
| 2026-09-08 | Lifecycle corrected per risk model; reverse, thermal and numeric low-voltage verification strengthened | RT-R012-01 **Proposed** | Review finding remediation; implementation pending | Pending Project Owner |

---

## 11. Review Notes

```text
[x] Risk statement, assets, boundary and source trigger are explicit.
[x] Existing controls are separated from proposed treatment.
[x] RT-R012-01 has stable identity and Jira coordination.
[x] Lifecycle is Proposed until explicit approval evidence exists.
[x] Cell-side over-current does not rely on SYS output limiting.
[x] Procedure-only reverse-polarity control is prohibited and electrical blocking has a functional test.
[x] NTC, thermal and numeric low-voltage verification are mandatory.
[x] Missing proof preserves [UNVALIDATED].
[x] No residual-risk acceptance or safety/certification claim is made.
```
