# Risk Assessment — Unprotected 1S Li-ion Battery Fault and Cell-Side Protection

**Risk ID:** R-012  
**Risk status:** Newly Identified  
**Current assessment date:** 2026-09-09  
**Last reviewed:** 2026-09-09  
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
  - RT-R012-01 may claim holder/service-wiring over-current coverage only for conductors physically downstream of the interruption element.
  - Any conductor between the cell contact and interruption element is residual exposure until separately controlled and verified.
  - Procedure-only reverse-polarity mitigation is prohibited.
  - Electrical reverse blocking requires bounded functional verification with USB absent and with normal USB present; mechanical keying must physically prevent ordinary reverse insertion.
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

**In scope:** cell contact/holder/BAT wiring, source-side over-current interruption, any conductor upstream of the interruption element, reverse insertion, charge voltage/current, NTC hot/cold/open/short behavior, low-voltage cutoff/recovery, thermal operating boundaries, holder fit and service interaction.

**Out of scope:** battery certification/regulatory approval, destructive abuse testing of an actual cell, multi-cell packs, production qualification, unrelated enclosure aesthetics.

---

## 3. Affected Assets and Trust Boundary

| Area | Detail |
|---|---|
| Assets | LG MJ1 cell, holder contacts/leads, BAT net, charger/power-path PMIC, PCB, enclosure/service interface |
| Trust boundary | User/service interaction with removable cell and electrical boundary between cell/holder and PCB |
| Category | Technical |
| Stakeholder surface | Compliance / Claims consequences: hardware replication, installation/service instructions, battery/autonomy and maturity claims |

---

## 4. Current Assessment

| Field | Value | Rationale |
|---|---|---|
| Likelihood | Medium | Holder is not keyed and final protection implementation does not yet exist |
| Impact | High | Reverse insertion, uncontrolled BAT-side current, thermal or charging faults can damage hardware/cell and invalidate subsystem operation |
| Residual risk | Pending Evidence | A proposed treatment exists but is not approved, implemented or verified |
| Evidence gap | `[UNVALIDATED]` | No fabricated board, source-side protection verification, upstream-segment control evidence, NTC fault simulation, reverse-blocking functional test, thermal run or received-cell fit test |
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
| RT-R012-01 | Implement and verify system-level 1S cell protection | Mitigate | **Proposed** | IHAP-55 implementation; IHAP-57 effectiveness tracking | ADR-0007 | 2026-09-09 |

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
**Last reviewed:** 2026-09-09  
**Next review trigger:** explicit Project Owner treatment decision or IHAP-55 schematic freeze

#### Rationale

The selected cell is unprotected. The final product needs system-boundary controls including fault paths before the PMIC SYS output. PMIC boost/SYS current limiting cannot by itself protect a short on holder leads or BAT net upstream of that stage. A protection element located only on the PCB after ordinary holder wiring also cannot claim to protect a short that occurs **before** that element. The accepted ADR establishes the battery role and system-level protection direction; the more specific source-side interruption, upstream-segment, fault-state and numeric verification details below are the **Proposed** RT-R012-01 treatment and are not approved merely because ADR-0007 is Accepted.

#### Proposed mandatory controls / actions

- place a **source-side over-current interruption element ahead of every holder/service conductor that RT-R012-01 claims to protect**, preferably at or immediately adjacent to the cell/holder positive contact;
- if any conductor necessarily remains between cell contact and interruption element, explicitly record that segment as uncovered by V13 and either move/add protection ahead of it or provide a separate reviewed mechanical/electrical control and verification before claiming treatment coverage for that segment;
- size interruption threshold/time from legitimate charge/discharge/transient current, conductor/trace ampacity and component characteristics;
- provide electrical reverse-battery blocking/protection **or** mechanical keying that physically prevents reverse insertion; procedure/labels are supplementary only;
- if electrical blocking is used, execute V15-A with USB absent **and V15-B with normal USB present**, both using bounded source/sink-capable battery-simulator fixtures and explicit current/voltage criteria;
- implement 4.2 V charge-voltage selection and ~1 A nominal charge target inside the source/thermal budget;
- implement NTC gating with normal/hot/cold/open/short functional verification;
- enforce MJ1 charge operation at **0–45 °C** and discharge operation at **-20–60 °C** if this proposed treatment is approved;
- implement the first-reference low-voltage policy: cutoff **2.70 V ±0.05 V**, no deliberate operation below **2.50 V**, recovery **>=3.00 V ±0.05 V** or valid USB, with no cutoff/restart oscillation;
- verify holder fit/retention without wrapper damage or excessive insertion force.

#### Scope coverage

| Cause / consequence | Coverage | Remaining exposure |
|---|---|---|
| BAT-side short / excessive cell current downstream of source-side interruption | Direct | Interruption rating/behavior `[UNVALIDATED]` until schematic and V13 |
| Conductor between cell contact and interruption element | Conditional / residual | **Not covered by V13**; must be eliminated from the claimed protected segment or separately controlled/verified before treatment effectiveness can be Verified |
| Reverse insertion with USB absent | Direct | Electrical blocker or mechanical keying `[UNVALIDATED]`; electrical path needs V15-A |
| Reverse insertion while USB remains present | Direct | Charger-originated current into reversed interface remains `[UNVALIDATED]`; electrical path needs V15-B |
| Charging over-voltage/current | Direct | PMIC configuration and V4/V14 pending |
| NTC hot/cold/open/short | Direct | Network thresholds and recovery `[UNVALIDATED]` |
| Thermal overstress | Direct | Final component thermal/junction method and powered evidence pending |
| Over-discharge / oscillatory recovery | Direct | Numeric V10 evidence pending |
| Cell internal defect / abuse outside intended use | Partial | Not eliminated; certification/abuse qualification outside MVP claims |

#### Source and Evidence Register

| ID | Source | Source type | Supports | Version / applicability | Verification | Checked on | Limitations |
|---|---|---|---|---|---|---|---|
| SRC-01 | `docs/adr/ADR-0007-edge-power-subsystem.md` | Project decision | Unprotected cell selection, backup role, system-responsibility protection and reverse-polarity direction | Accepted 2026-09-07 | Verified | 2026-09-09 | Does not approve the later RT-R012-01 details or lifecycle |
| SRC-02 | `docs/evidence/IHAP-49/owned-hardware-evidence.md` | Internal evidence | Unkeyed holder / owned hardware observations | Owned specimens | Verified | 2026-09-09 | Does not prove final PCB/source-side protection |
| SRC-03 | MPS MP2636 datasheet in source register | Manufacturer | PMIC charger/power-path/boost/TS behavior | Rev.1.02 | Verified | 2026-09-09 | Does not cover arbitrary upstream BAT faults |
| SRC-04 | LG INR18650-MJ1 product specification in source register | Manufacturer | 4.2 V max charge, 2.5 V discharge end, 0–45 °C charge, -20–60 °C discharge | MJ1 Rev.1 source | Verified for model | 2026-09-09 | Received lot still pending inspection |

#### Implementation and Verification Evidence

| Evidence ID | Evidence | Evidence class | Expected result | Actual result | Status |
|---|---|---|---|---|---|
| EV-01 | IHAP-55 schematic/BOM review | Implementation | Source-side interruption coverage boundary, residual upstream segment (if any), reverse control, NTC, low-voltage and thermal limits are explicit | Not executed | `[UNVALIDATED]` |
| EV-02 | V4 NTC/charging/thermal + V14 source-limit run | Verification | Charge/NTC/source-priority behavior meets the approved/frozen treatment limits | Not executed | `[UNVALIDATED]` |
| EV-03 | V13 source-side over-current verification | Verification | Every conductor claimed as protected is downstream of and exercised through the actual/production-identical interruption path; any upstream segment has separate evidence | Not executed | `[UNVALIDATED]` |
| EV-04 | Received MJ1 / holder qualification | Verification | Correct identity/condition and non-destructive fit/retention | Not executed | `[UNVALIDATED]` |
| EV-05 | V10 low-voltage / recovery run | Verification | 2.70 V cutoff, >=3.00 V recovery, no deliberate <2.50 V discharge or oscillation | Not executed | `[UNVALIDATED]` |
| EV-06 | V15-A/V15-B reverse-polarity functional tests when electrical blocking is used | Verification | USB-absent and USB-present reversed-interface cases stay within frozen current/voltage/device-stress criteria with no damage | Not executed / N/A if mechanical-only keying | `[UNVALIDATED]` |

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
| Accepted ADR | `docs/adr/ADR-0007-edge-power-subsystem.md` | **Partially mitigates** — the accepted baseline establishes backup-only use, system-responsibility protection and reverse-polarity prevention direction. This allowed ADR effect does **not** approve, implement or verify the later RT-R012-01 treatment details. |
| Implementation task | IHAP-55 | Schematic, PCB and physical tests after the applicable treatment/amendment scope is explicitly approved |
| Effectiveness tracking | IHAP-57 | Treatment lifecycle/effectiveness after approval and evidence |
| Remediation task | IHAP-56 | Creates canonical risk/treatment traceability and proposed remediation detail |
| Validation contract | `docs/evidence/IHAP-49/validation-plan.md` | Accepted baseline plus explicitly marked Proposed IHAP-56 test additions; source-side V13 and USB-absent/present V15 detail are not treatment approval by themselves |
| Closure matrix | `docs/evidence/IHAP-49/ihap-56-closure-matrix.md` | Cross-file Accepted/Proposed state and review invariants |

---

## 9. Stakeholder Visibility

Risk summary and treatment state may be shown in stakeholder summaries. Technical details should link to GitHub. Do not claim the battery subsystem is safe/certified/production-ready; treatment is Proposed and effectiveness remains `[UNVALIDATED]`.

---

## 10. Assessment History

| Date | Change | Treatment | Evidence | Decision |
|---|---|---|---|---|
| 2026-09-07 | Canonical risk created from IHAP-49 post-merge review | RT-R012-01 initially drafted | ADR-0007 + IHAP-49 evidence | Pending |
| 2026-09-08 | Lifecycle corrected per risk model; reverse, thermal and numeric low-voltage verification strengthened; canonical category/inverse ADR effect corrected | RT-R012-01 **Proposed** | Review finding remediation; implementation pending | Pending Project Owner |
| 2026-09-09 | Upstream-holder coverage boundary and USB-present reverse-insertion case made explicit | RT-R012-01 **Proposed** | Latest Codex finding remediation | Pending Project Owner |

---

## 11. Review Notes

```text
[x] Risk statement, assets, boundary and source trigger are explicit.
[x] Category uses the canonical risk-model vocabulary; claim consequences remain in stakeholder/rationale text.
[x] Existing controls are separated from proposed treatment.
[x] RT-R012-01 has stable identity and Jira coordination.
[x] Lifecycle is Proposed until explicit approval evidence exists.
[x] V13 cannot overclaim protection for conductors located before the interruption element.
[x] Electrical reverse blocking includes bounded USB-absent and USB-present functional cases.
[x] NTC, thermal and numeric low-voltage verification remain Proposed treatment detail until approved.
[x] Inverse ADR relationship declares the allowed effect `Partially mitigates` without implying treatment approval.
[x] Missing proof preserves [UNVALIDATED].
[x] No residual-risk acceptance or safety/certification claim is made.
```
