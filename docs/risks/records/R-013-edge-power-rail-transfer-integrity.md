# Risk Assessment — Edge Power Rail and Source-Transfer Integrity

**Risk ID:** R-013  
**Risk status:** Newly Identified  
**Current assessment date:** 2026-09-08  
**Last reviewed:** 2026-09-08  
**Next review:** explicit Project Owner treatment decision, IHAP-55 schematic freeze, first power bring-up, or material PMIC/regulator/source-transfer change  
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
  primary_treatment: RT-R013-01
  treatment_lifecycle: Proposed
  unvalidated_claim_marker: "[UNVALIDATED]"

HIDDEN_ANTI_REGRESSION_RULES:
  - MP2636 input pass-through must not be mislabeled as a regulated 5.0 V product rail.
  - Product 5 V regulation, source-current limiting, backfeed blocking, load-step response and source transfer remain [UNVALIDATED] until IHAP-55 evidence exists.
  - No-reset transfer is a target, not an achieved property.
  - Mandatory load-step evidence covers both load edges with a frozen slew/rise-fall requirement when that proposed amendment is approved.
  - Transfer/restoration evidence must cover high/mid/low accepted battery conditions when that proposed amendment is approved.
  - RT-R013-01 remains Proposed until explicit Project Owner treatment approval evidence exists.
-->

---

## 1. Risk Statement

```text
There is a risk that the edge node resets, loses sensing continuity, backfeeds or overloads the external source, oscillates between sources or operates outside its accepted voltage domain because USB input limiting, pass-through, battery boost, post-regulation and source-transfer stages may not maintain a stable regulated product rail across steady-state and transient conditions.
```

---

## 2. Source Trigger and Scope

**Source trigger:** ADR-0007 requires one regulated 5 V product bus from both normal USB-C power and 1S backup. Review established that MP2636 valid input is passed to SYS rather than regulated to the programmable battery-boost setpoint, so a downstream regulator or equivalent topology is required. Physical behavior is not yet measured.

**In scope:** USB-C sink/input behavior and current limiting; intermediate pass-through/boost; downstream 5 V and 3.3 V regulation; USB-priority takeover/restoration; backfeed; 0.5 A continuous and 1.0 A dynamic response; thermal interaction with power delivery; ESP32 reset/brownout; final-node quantitative power work transferred by the accepted ADR baseline from ADR-0001/0002/0004/0005, with ADR-0003 transfer proposed by IHAP-56 pending Project Owner approval.

**Out of scope:** application-level event recovery beyond recording power-induced resets; arbitrary USB-C/PD profiles; certification/production reliability; multi-day battery-only autonomy.

---

## 3. Affected Assets and Trust Boundary

| Area | Detail |
|---|---|
| Assets | 5 V product SYS, 3.3 V rail, ESP32-C3, LD2410C, OLED/environmental/reed interfaces, upstream USB source |
| Trust boundary | External 5 V USB-C source ↔ charger/power path ↔ battery ↔ post-regulator ↔ node load |
| Category | Technical |
| Stakeholder surface | Data-integrity consequence: sensing continuity, node availability, autonomy claims and reproducibility |

---

## 4. Current Assessment

| Field | Value | Rationale |
|---|---|---|
| Likelihood | Medium | Topology is accepted but custom PCB and dynamic response are not implemented |
| Impact | High | Rail collapse/backfeed/source overload/reset can interrupt sensing and invalidate continuity claims |
| Residual risk | Pending Evidence | Proposed treatment is not approved, implemented or verified |
| Evidence gap | `[UNVALIDATED]` | No fabricated-board source-limit, bidirectional load-step, transfer/restoration, backfeed, thermal or final-node current evidence |
| Decision state | Pending Project Owner | ADR acceptance is not treatment approval or residual-risk acceptance |

---

## 5. Existing Controls

| Control | Evidence | Coverage | Limitation |
|---|---|---|---|
| Regulated 5.0 V product-bus contract | ADR-0007 | Prevents accepting pass-through as final rail | Physical regulation `[UNVALIDATED]` |
| MP2636 caveat + downstream regulation requirement | ADR-0007 / custom PCB power contract | Addresses normal-input regulation gap | Exact regulator/topology `[UNVALIDATED]` |
| USB-priority/no-backfeed requirements | ADR-0007 | Defines expected source behavior | Transfer/isolation `[UNVALIDATED]` |
| >=0.5 A continuous / >=1.0 A headroom envelope | ADR-0007 | Defines sizing target | Capability `[UNVALIDATED]` |

The detailed V7/V8/V9/V14 acceptance conditions added by IHAP-56 are **Proposed treatment/validation detail**, not existing controls and not accepted merely because ADR-0007 is Accepted.

---

## 6. Risk Treatment Summary

| Treatment ID | Title | Strategy | Lifecycle status | Jira | ADR | Last review |
|---|---|---|---|---|---|---|
| RT-R013-01 | Implement and verify regulated dual-source product power | Mitigate | **Proposed** | IHAP-55 implementation; IHAP-57 effectiveness tracking | ADR-0007 | 2026-09-08 |

`Proposed` is required because there is not yet durable Project Owner evidence explicitly approving this later treatment scope. Accepted ADR-0007 requirements support the rationale but do not substitute for treatment approval.

---

## 7. Risk Treatments

### RT-R013-01 — Implement and verify regulated dual-source product power

**Strategy:** Mitigate  
**Lifecycle status:** Proposed  
**Treatment owner:** IHAP-55 custom PCB/power workstream  
**Jira coordination:** IHAP-55 / IHAP-57  
**Related ADRs:** ADR-0007  
**Introduced:** 2026-09-07  
**Last reviewed:** 2026-09-08  
**Next review trigger:** explicit Project Owner treatment decision or schematic freeze

#### Rationale

The accepted ADR baseline already requires a regulated 5.0 V product bus, USB-priority backup transfer, prohibited backfeed, a post-MP2636 regulation stage or reviewed equivalent, and a >=0.5 A continuous / >=1.0 A headroom design envelope. Those architectural constraints do not prove that the fabricated implementation actually maintains the rail under combined charging, fast load transitions, source loss/restoration or low-battery conditions. RT-R013-01 therefore proposes a single verification treatment that couples source-current limiting, dynamic rail capture, transfer/restoration and final-node current evidence so effectiveness can be measured against the accepted architecture. The tighter numeric test conditions added by IHAP-56 remain **Proposed** until explicit Project Owner approval and must not be treated as accepted architecture amendments before that decision.

#### Proposed mandatory controls / actions

- preserve a **regulated 5.0 V product SYS** regardless of intermediate USB pass-through or battery boost;
- with MP2636, add a downstream regulator covering the complete intermediate range or explicitly supersede the topology through review;
- implement correct USB-C 5 V sink termination/input protection;
- freeze input-current limiting so worst-case configured maximum including tolerance is **<=1.50 A** for the reference source;
- verify combined node-load + charging behavior using V14, proving charge current yields to system load before SYS collapse;
- prevent prohibited backfeed toward the external USB source;
- implement deterministic USB-priority transfer/restoration without source oscillation;
- verify transfer and restoration at **high 4.10±0.10 V, mid 3.60±0.10 V and low 2.80±0.05 V** battery conditions;
- require **zero restoration-attributable ESP32 reset/brownout** in V9 at every required battery/load condition if the no-reset target is to be verified;
- size product 5 V stage for >=0.5 A continuous and >=1.0 A transient/headroom;
- execute V7 in both directions, baseline->1 A and 1 A->baseline, with **10–90% current transition <=100 µs** or a faster final measured load-derived requirement;
- enforce rail/reset/transient and manufacturer-derived thermal PASS criteria;
- provide product-SYS, intermediate-SYS and 3.3 V test points;
- execute final-node quantitative characterization for the accepted transferred obligations from ADR-0001/0002/0004/0005; include ADR-0003/reed current only after the proposed ownership-transfer amendment is explicitly approved or otherwise assigned by an accepted downstream decision;
- execute endurance before any measured autonomy claim.

#### Scope coverage

| Cause / consequence | Coverage | Remaining exposure |
|---|---|---|
| USB pass-through below/above desired product rail | Direct | Post-regulator physical evidence pending |
| USB source overload / incorrect ILIM | Direct | V14 pending |
| Battery boost / low-cell regulation | Direct | Converter/layout evidence pending |
| 1 A load-apply droop / load-release overshoot | Direct | Bidirectional <=100 µs V7 pending |
| USB↔battery transfer/reset | Direct | V8/V9 high/mid/low pending; any restoration reset fails the proposed no-reset verification target |
| Upstream backfeed | Direct | Schematic + V8/V9 pending |
| Thermal overstress | Direct | Final thermal table and powered evidence pending |
| Final-node actual power | Direct | V11 pending |
| Runtime event recovery after power reset | Partial | Software recovery remains downstream scope |

#### Source and Evidence Register

| ID | Source | Source type | Supports | Version / applicability | Verification | Checked on | Limitations |
|---|---|---|---|---|---|---|---|
| SRC-01 | `docs/adr/ADR-0007-edge-power-subsystem.md` | Project decision | Accepted product rail/source-transfer architecture baseline | Accepted 2026-09-07 | Verified | 2026-09-08 | Does not approve RT-R013-01 or the later numeric validation amendments |
| SRC-02 | MPS MP2636 datasheet in source register | Manufacturer | IN-to-SYS pass-through, operating Tj, boost/charger behavior | Rev.1.02 | Verified | 2026-09-08 | Final PCB dynamics/layout not covered |
| SRC-03 | `docs/evidence/IHAP-49/validation-plan.md` | Project validation plan | Accepted baseline tests plus explicitly marked Proposed IHAP-56 extensions | IHAP-49 handoff / IHAP-56 remediation | Verified as documentation | 2026-09-08 | Execution pending; proposed extensions are not treatment approval |
| SRC-04 | ADR-0001/0002/0004/0005; ADR-0003 separately proposed for transfer | Project decisions | Accepted node-load obligations and proposed reed-current ownership correction | Current accepted ADRs + IHAP-56 proposal | Verified | 2026-09-08 | Final custom-board measurements pending; ADR-0003 transfer not yet approved as an ADR-0007 amendment |

#### Implementation and Verification Evidence

| Evidence ID | Evidence | Evidence class | Expected result | Actual result | Status |
|---|---|---|---|---|---|
| EV-01 | IHAP-55 schematic/ERC/DRC/BOM review | Implementation | Post-regulation/equivalent, anti-backfeed, ILIM, test points, thermal table and current envelope implemented for the approved scope | Not executed | `[UNVALIDATED]` |
| EV-02 | V2/V5/V6 regulated rail/thermal tests | Verification | Product 5 V and thermal limits hold in normal/battery operation | Not executed | `[UNVALIDATED]` |
| EV-03 | V7 bidirectional 1 A load-step | Verification | Both edges meet the approved current-transition requirement and frozen transient/reset/recovery criteria | Not executed | `[UNVALIDATED]` |
| EV-04 | V8/V9 source transfer/restoration | Verification | High/mid/low battery conditions meet no-backfeed/no-oscillation and, for no-reset verification, **zero transfer/restoration-attributable reset or brownout** | Not executed | `[UNVALIDATED]` |
| EV-05 | V14 combined source-current-limit/system-priority | Verification | Input remains <=1.50 A / frozen ILIM and charge current yields before SYS collapse | Not executed | `[UNVALIDATED]` |
| EV-06 | V11 final-node quantitative characterization | Verification | Required accepted rail/current/load contributions recorded; any proposed ADR-0003/reed-current transfer is included only after approval/assignment | Not executed | `[UNVALIDATED]` |
| EV-07 | V12 endurance | Verification | Measured backup duration for tested board/cell/configuration | Not executed | `[UNVALIDATED]` |

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
| Accepted ADR | `docs/adr/ADR-0007-edge-power-subsystem.md` | **Partially mitigates** — the accepted baseline requires regulated product SYS, post-regulation/equivalent, USB priority, anti-backfeed and source-transfer/headroom targets. This allowed ADR effect does **not** approve, implement or verify the later RT-R013-01 treatment details. |
| Implementation task | IHAP-55 | Custom PCB implementation and physical validation after the applicable treatment/amendment scope is explicitly approved |
| Effectiveness tracking | IHAP-57 | Treatment lifecycle/effectiveness after approval and evidence |
| Remediation task | IHAP-56 | Creates canonical risk/treatment traceability and proposed remediation detail |
| Validation contract | `docs/evidence/IHAP-49/validation-plan.md` | Accepted baseline plus explicitly marked Proposed IHAP-56 test additions; proposed V7/V8/V9/V14 detail does not self-approve treatment |

---

## 9. Stakeholder Visibility

Stakeholder summaries may state the accepted wired-5-V + battery-backup architecture and that physical rail/transfer effectiveness remains `[UNVALIDATED]`. Do not claim fault tolerance, seamless UPS, validated autonomy or production reliability before evidence.

---

## 10. Assessment History

| Date | Change | Treatment | Evidence | Decision |
|---|---|---|---|---|
| 2026-09-07 | Canonical risk created from IHAP-49 post-merge review | RT-R013-01 initially drafted | ADR-0007 + manufacturer source | Pending |
| 2026-09-08 | Lifecycle corrected; combined ILIM test, high/mid/low transfer and bidirectional slew-controlled load-step added; rationale/category/inverse ADR effect and restoration no-reset criterion corrected | RT-R013-01 **Proposed** | Review finding remediation; implementation pending | Pending Project Owner |

---

## 11. Review Notes

```text
[x] Risk statement, source trigger, assets and trust boundary are explicit.
[x] Category uses the canonical risk-model vocabulary; data-integrity consequences remain in stakeholder/rationale text.
[x] Existing controls are separated from proposed treatment detail.
[x] RT-R013-01 has a treatment-specific rationale and remains Proposed until explicit approval evidence exists.
[x] MP2636 pass-through is not mislabeled as regulated product SYS.
[x] Source-limit/system-priority evidence is explicit in the proposed treatment.
[x] Load-step covers both edges with numeric transition-time criteria in the proposed amendment.
[x] Transfer/restoration covers high/mid/low battery conditions and restoration-attributable reset/brownout is an explicit failure for the no-reset target.
[x] Accepted quantitative ownership transfer remains ADR-0001/0002/0004/0005; ADR-0003 extension is Proposed until approved.
[x] Inverse ADR relationship declares the allowed effect `Partially mitigates` without implying treatment approval.
[x] Missing proof preserves [UNVALIDATED].
[x] No residual-risk acceptance or reliability/safety claim is made.
```
