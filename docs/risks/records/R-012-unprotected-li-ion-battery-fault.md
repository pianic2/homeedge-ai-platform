# Risk Assessment — Unprotected 1S Li-ion Battery Fault and Cell-Side Protection

**Risk ID:** R-012  
**Risk status:** Under Treatment  
**Current assessment date:** 2026-09-07  
**Last reviewed:** 2026-09-07  
**Next review:** IHAP-55 schematic review, received-cell qualification, or material battery/protection topology change  
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
  unvalidated_claim_marker: "[UNVALIDATED]"

HIDDEN_ANTI_REGRESSION_RULES:
  - The selected LG INR18650-MJ1 is unprotected; do not imply cell-level protection exists.
  - PMIC SYS/boost current limiting must not be treated as protection for a short on the holder leads or BAT net upstream of the PMIC.
  - Procedure-only reverse-polarity mitigation is prohibited.
  - Cell-side over-current interruption, charging limits, NTC behavior, low-voltage behavior and polarity controls remain [UNVALIDATED] until IHAP-55 evidence exists.
  - Do not describe the subsystem as safe, certified, fire-safe, production-ready or compliant.
-->

---

## 1. Risk Statement

```text
There is a risk that the unprotected 1S Li-ion cell, holder wiring or custom PCB is electrically or thermally overstressed because reverse insertion, a BAT-side short/over-current condition, incorrect charging, excessive discharge or temperature-control failure can occur outside the protection coverage of the downstream SYS rail.
```

---

## 2. Source Trigger and Scope

**Source trigger:** ADR-0007 selects an **unprotected LG INR18650-MJ1** in a currently unkeyed serviceable holder. The preferred MP2636-class architecture provides charger/power-path/boost controls, but output/SYS limiting alone cannot interrupt every fault path on the holder leads or BAT net upstream of the PMIC. Physical implementation is not yet fabricated.

**In scope:**

- 18650 holder and battery connector polarity;
- holder leads and BAT net before the charger/power-path PMIC;
- cell-side over-current / short interruption;
- reverse-cell insertion;
- charge-voltage/current control;
- NTC hot/cold and sensor-fault behavior;
- low-voltage cutoff/recovery;
- cell/holder fit and service access insofar as they affect electrical risk.

**Out of scope:**

- battery certification or regulatory approval;
- destructive abuse testing of an actual cell;
- multi-cell packs;
- production qualification;
- enclosure aesthetics unrelated to polarity/retention.

---

## 3. Affected Assets and Trust Boundary

| Area | Detail |
|---|---|
| Assets | LG MJ1 cell, holder leads, BAT net, charger/power-path PMIC, PCB, enclosure/service interface |
| Trust boundary | User/service interaction with the removable cell and the electrical boundary between cell/holder and PCB |
| Category | Technical / Compliance-Claims |
| Stakeholder surface | Hardware replication, installation/service instructions, battery/autonomy and maturity claims |

---

## 4. Current Assessment

| Field | Value | Rationale |
|---|---|---|
| Likelihood | Medium | The holder is not keyed and the final protection implementation does not yet exist |
| Impact | High | Reverse insertion, uncontrolled BAT-side current or charging faults can damage hardware/cell and invalidate subsystem operation |
| Residual risk | Pending Evidence | Treatment is approved architecturally but not implemented or verified |
| Evidence gap | `[UNVALIDATED]` | No fabricated custom board, cell-side protection verification, NTC fault simulation or received-cell fit test |
| Decision state | Pending Project Owner | ADR acceptance is not residual-risk acceptance |

---

## 5. Existing Controls

| Control | Evidence | Coverage | Limitation |
|---|---|---|---|
| Backup-only battery role | ADR-0007 | Reduces duty/expectation | Does not prevent electrical faults |
| 4.2 V CV and ~1 A charge targets | ADR-0007 / IHAP-49 contract | Bounds intended charging | Implementation `[UNVALIDATED]` |
| NTC monitoring requirement | ADR-0007 | Requires temperature gating | Fault thresholds/function `[UNVALIDATED]` |
| Reverse-insertion prevention requirement | ADR-0007 | Procedure-only control explicitly rejected | Electrical/mechanical implementation `[UNVALIDATED]` |
| Owned holder dimensions and unkeyed condition recorded | `docs/evidence/IHAP-49/owned-hardware-evidence.md` | Makes mechanical risk visible | Received-cell fit remains `[UNVALIDATED]` |

Planned controls belong to the treatment below and must not be represented as already implemented.

---

## 6. Risk Treatment Summary

| Treatment ID | Title | Strategy | Lifecycle status | Jira | ADR | Last review |
|---|---|---|---|---|---|---|
| RT-R012-01 | Implement and verify system-level 1S cell protection | Mitigate | Approved | IHAP-55 implementation; IHAP-57 effectiveness tracking | ADR-0007 | 2026-09-07 |

`Approved` is supported by the Project Owner acceptance of ADR-0007 and the subsequent instruction to resolve all review findings. It does **not** mean Implemented or Verified.

---

## 7. Risk Treatments

### RT-R012-01 — Implement and verify system-level 1S cell protection

**Strategy:** Mitigate  
**Lifecycle status:** Approved  
**Treatment owner:** IHAP-55 power/PCB workstream; IHAP-51 for mechanical keying/serviceability where used  
**Jira coordination:** IHAP-55 / IHAP-57  
**Related ADRs:** ADR-0007  
**Introduced:** 2026-09-07  
**Last reviewed:** 2026-09-07  
**Next review trigger:** IHAP-55 schematic freeze or first fabricated-board bring-up

#### Rationale

The chosen cell is unprotected. The final product therefore needs protection at the **system boundary**, including fault paths that exist before the PMIC SYS output. In particular, PMIC boost/SYS current limiting cannot by itself protect a short on holder leads or the BAT net upstream of that limiting stage.

#### Mandatory controls / actions

- place a **cell-side over-current interruption element** (fuse, resettable/electronic protection switch, or reviewed equivalent) so the holder leads/BAT net downstream of the cell are covered before an upstream-of-PMIC short can draw uncontrolled current;
- size the interruption threshold/time from the final worst-case normal charge/discharge/transient envelope, conductor/trace ampacity and selected component characteristics; the exact rating is an IHAP-55 schematic/BOM decision;
- do **not** rely solely on MP2636 SYS/boost current limiting to cover BAT-side faults;
- provide electrical reverse-battery blocking/protection **or** a mechanically keyed interface/enclosure that physically prevents reverse insertion; labels/procedure are supplementary only;
- implement 4.2 V charge-voltage selection and ~1 A nominal charge target within the final source/thermal budget;
- implement NTC temperature gating so both out-of-range temperature equivalents and NTC open/short faults inhibit charging or are intercepted by an equivalent fail-bounded control;
- implement low-voltage cutoff/recovery that does not intentionally discharge the MJ1 below the accepted manufacturer boundary;
- verify holder fit/retention without wrapper damage or excessive insertion force.

#### Scope coverage

| Cause / consequence | Coverage | Remaining exposure |
|---|---|---|
| BAT-side short / excessive cell current | Direct | Exact interruption rating and behavior remain `[UNVALIDATED]` until schematic and bench verification |
| Reverse insertion | Direct | Depends on final electrical blocker or mechanical keying implementation |
| Charging over-voltage/current | Direct | Depends on PMIC configuration and physical test evidence |
| NTC hot/cold or sensor fault | Direct | Final network thresholds and recovery behavior remain `[UNVALIDATED]` |
| Over-discharge | Direct | Exact cutoff/recovery values remain `[UNVALIDATED]` |
| Cell internal defect / abuse outside intended use | Partial | Not eliminated by this architecture; certification/abuse qualification remains outside MVP claims |

#### Source and Evidence Register

| ID | Source | Source type | Supports | Version / applicability | Verification | Checked on | Limitations |
|---|---|---|---|---|---|---|---|
| SRC-01 | `docs/adr/ADR-0007-edge-power-subsystem.md` | Project decision | Unprotected cell selection and mandatory system-level protection | Accepted 2026-09-07 | Verified | 2026-09-07 | Architecture only |
| SRC-02 | `docs/evidence/IHAP-49/owned-hardware-evidence.md` | Internal evidence | Unkeyed holder and owned charger observations | Owned specimens | Verified | 2026-09-07 | Does not prove final PCB protection |
| SRC-03 | MPS MP2636 datasheet registered in `docs/evidence/IHAP-49/source-register.md` | Manufacturer | PMIC charger/power-path/boost and TS behavior | MP2636 Rev.1.02 | Verified for architecture review | 2026-09-07 | Does not cover arbitrary holder/BAT-net short paths by itself |
| SRC-04 | LG INR18650-MJ1 manufacturer/seller sources registered in IHAP-49 | Manufacturer/seller | Cell envelope and selected model | 1S MJ1 reference | Partially Verified pending received lot | 2026-09-07 | Received specimen not yet inspected |

#### Implementation and Verification Evidence

| Evidence ID | Evidence | Evidence class | Expected result | Actual result | Status |
|---|---|---|---|---|---|
| EV-01 | IHAP-55 schematic/BOM review | Implementation | Cell-side interruption element is upstream of relevant BAT fault paths; rating rationale recorded; reverse-polarity and NTC/cutoff controls present | Not executed | `[UNVALIDATED]` |
| EV-02 | IHAP-55 NTC hot/cold/open/short simulation | Verification | Charging is inhibited for all defined out-of-window/fault states and recovers deterministically when a valid NTC equivalent is restored | Not executed | `[UNVALIDATED]` |
| EV-03 | IHAP-55 controlled cell-side over-current verification | Verification | Protection interrupts at/within the frozen threshold/time without using an intentional hard short across the actual MJ1 cell | Not executed | `[UNVALIDATED]` |
| EV-04 | Received MJ1 / holder qualification | Verification | Correct identity/condition and non-destructive fit/retention | Not executed | `[UNVALIDATED]` |
| EV-05 | Charge / low-voltage / recovery run | Verification | Charge/CV/current and cutoff/recovery match frozen design limits | Not executed | `[UNVALIDATED]` |

For EV-03, use a current-limited bench source, protected test fixture, sacrificial protection sample or equivalent bounded method. **Do not intentionally hard-short the actual Li-ion cell.**

#### Treatment Effectiveness Review

**Review date:** Pending  
**Evidence reviewed:** EV-01 through EV-05 pending  
**Effectiveness:** Pending Evidence  
**Likelihood after treatment:** Pending Evidence  
**Impact after treatment:** Pending Evidence  
**Residual risk:** Pending Evidence  
**Project Owner decision required:** Yes

---

## 8. Traceability

| Relationship | Link | Effect / Rule |
|---|---|---|
| Accepted ADR | `docs/adr/ADR-0007-edge-power-subsystem.md` | Partially mitigates by mandating the treatment; does not verify effectiveness |
| Implementation task | IHAP-55 | Schematic, PCB and physical tests |
| Effectiveness tracking | IHAP-57 | Updates this dossier after implementation/verification evidence |
| Remediation task | IHAP-56 | Creates canonical risk/treatment traceability from post-merge review |
| Validation contract | `docs/evidence/IHAP-49/validation-plan.md` | Defines non-destructive verification requirements |

---

## 9. Stakeholder Visibility

Risk summary and treatment state may be shown in stakeholder summaries. Technical details should link to GitHub. Do not claim the battery subsystem is safe/certified/production-ready; implementation and effectiveness remain `[UNVALIDATED]`.

---

## 10. Assessment History

| Date | Change | Treatment | Evidence | Decision |
|---|---|---|---|---|
| 2026-09-07 | Canonical risk created from IHAP-49 post-merge review; cell-side over-current and reverse/NTC requirements made explicit | RT-R012-01 Approved | ADR-0007 + IHAP-49 evidence; physical evidence pending | Residual-risk decision Pending |

---

## 11. Review Notes

```text
[x] Risk statement, assets, boundary and source trigger are explicit.
[x] Existing controls are separated from planned treatment.
[x] RT-R012-01 has stable identity, strategy, lifecycle and Jira coordination.
[x] Cell-side over-current coverage does not rely on SYS output limiting.
[x] Procedure-only reverse-polarity control is prohibited.
[x] NTC functional/fault verification is mandatory.
[x] Implementation and verification evidence remain separate.
[x] Missing proof preserves [UNVALIDATED].
[x] ADR inverse link is required and provided by IHAP-56 remediation.
[x] No residual-risk acceptance or safety/certification claim is made.
```
