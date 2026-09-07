# Risk Assessment — Edge Power Rail and Source-Transfer Integrity

**Risk ID:** R-013  
**Risk status:** Under Treatment  
**Current assessment date:** 2026-09-07  
**Last reviewed:** 2026-09-07  
**Next review:** IHAP-55 schematic freeze, first power bring-up, or material PMIC/regulator/source-transfer change  
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
  unvalidated_claim_marker: "[UNVALIDATED]"

HIDDEN_ANTI_REGRESSION_RULES:
  - MP2636 input pass-through must not be mislabeled as a regulated 5.0 V product rail.
  - Product 5 V regulation, backfeed blocking, load-step response and source transfer remain [UNVALIDATED] until IHAP-55 evidence exists.
  - No-reset transfer is a target, not an achieved property.
  - Do not treat average-current arithmetic as proof of transient headroom.
-->

---

## 1. Risk Statement

```text
There is a risk that the edge node resets, loses sensing continuity, backfeeds the external source, oscillates between sources or operates outside its accepted voltage domain because the USB pass-through, battery boost, post-regulation and source-transfer stages may not maintain a stable regulated product rail across steady-state and transient conditions.
```

---

## 2. Source Trigger and Scope

**Source trigger:** ADR-0007 requires one regulated 5 V product bus from both normal USB-C power and 1S backup. Review of the preferred MP2636 direction established that valid USB input is passed to SYS rather than regulated to the programmable battery-boost setpoint, so a downstream regulator or equivalent topology is required. Physical behavior is not yet measured.

**In scope:**

- USB-C sink/input behavior;
- MP2636-class pass-through / boost intermediate node;
- downstream 5 V product regulation;
- 3.3 V rail fed from the product bus;
- normal-source priority and battery takeover/restoration;
- upstream USB backfeed prevention;
- 0.5 A continuous capability and 1.0 A transient/headroom response;
- ESP32-C3 reset/brownout behavior attributable to power delivery;
- quantitative final-node current/rail work transferred from earlier ADRs.

**Out of scope:**

- application-level event recovery implementation beyond recording power-induced resets;
- universal operation from arbitrary USB-C/PD profiles;
- certification/production reliability claims;
- multi-day battery-only autonomy.

---

## 3. Affected Assets and Trust Boundary

| Area | Detail |
|---|---|
| Assets | 5 V product SYS, 3.3 V rail, ESP32-C3, LD2410C, OLED/environmental/reed interfaces, upstream USB source |
| Trust boundary | External 5 V USB-C source ↔ power-path/charger ↔ battery ↔ post-regulator ↔ node load |
| Category | Technical / Data-integrity consequence |
| Stakeholder surface | Continuity/autonomy claims, node availability and reproducibility |

---

## 4. Current Assessment

| Field | Value | Rationale |
|---|---|---|
| Likelihood | Medium | The topology is accepted but the custom PCB and dynamic response are not yet implemented |
| Impact | High | Rail collapse/backfeed/reset can interrupt the reference sensing node and invalidate continuity claims |
| Residual risk | Pending Evidence | Treatment requirements exist but effectiveness is unverified |
| Evidence gap | `[UNVALIDATED]` | No fabricated-board load-step, transfer/restoration, backfeed, rail or final-node current evidence |
| Decision state | Pending Project Owner | ADR acceptance is not residual-risk acceptance |

---

## 5. Existing Controls

| Control | Evidence | Coverage | Limitation |
|---|---|---|---|
| Regulated 5.0 V product-bus contract | ADR-0007 | Prevents accepting pass-through as final rail | Physical regulation `[UNVALIDATED]` |
| MP2636 pass-through caveat + downstream regulation requirement | ADR-0007 / custom PCB power contract | Addresses identified normal-input regulation gap | Exact regulator/topology `[UNVALIDATED]` |
| USB-priority automatic takeover and no-backfeed requirements | ADR-0007 | Defines expected source behavior | Transfer/isolation `[UNVALIDATED]` |
| >=0.5 A continuous / >=1.0 A headroom envelope | ADR-0007 | Defines sizing target | Capability `[UNVALIDATED]` |
| Mandatory 1 A instrumented load-step contract | IHAP-49 validation plan | Requires dynamic proof rather than average-current inference | Test not yet executed |

---

## 6. Risk Treatment Summary

| Treatment ID | Title | Strategy | Lifecycle status | Jira | ADR | Last review |
|---|---|---|---|---|---|---|
| RT-R013-01 | Implement and verify regulated dual-source product power | Mitigate | Approved | IHAP-55 implementation; IHAP-57 effectiveness tracking | ADR-0007 | 2026-09-07 |

`Approved` is supported by the accepted ADR-0007 requirements and the Project Owner remediation instruction. It does not mean Implemented or Verified.

---

## 7. Risk Treatments

### RT-R013-01 — Implement and verify regulated dual-source product power

**Strategy:** Mitigate  
**Lifecycle status:** Approved  
**Treatment owner:** IHAP-55 custom PCB/power workstream  
**Jira coordination:** IHAP-55 / IHAP-57  
**Related ADRs:** ADR-0007  
**Introduced:** 2026-09-07  
**Last reviewed:** 2026-09-07  
**Next review trigger:** schematic freeze or first fabricated-board power validation

#### Mandatory controls / actions

- preserve a **regulated 5.0 V product SYS** independent of whether the intermediate node is USB pass-through or battery boost;
- when MP2636 is used, add a downstream regulator capable of maintaining the frozen product-bus band across the complete intermediate range, or explicitly review and supersede the topology with an equivalent design;
- implement correct USB-C 5 V sink termination and input protection for C-to-C operation;
- prevent prohibited backfeed toward the external USB source;
- implement deterministic USB-priority transfer to battery and restoration without source oscillation;
- size the product 5 V stage for >=0.5 A continuous capability and >=1.0 A transient/headroom;
- provide product-SYS, intermediate-SYS and 3.3 V test points;
- execute mandatory instrumented 1 A load-step testing in normal-source and representative battery conditions;
- execute source-loss/restoration waveform capture and reset/brownout logging;
- execute final-node quantitative rail/current characterization transferred from ADR-0001/0002/0003/0004/0005;
- execute controlled endurance testing before any measured autonomy claim.

#### Scope coverage

| Cause / consequence | Coverage | Remaining exposure |
|---|---|---|
| USB pass-through below/above desired product rail | Direct | Depends on post-regulator/topology physical evidence |
| Battery boost / low-cell regulation | Direct | Depends on converter efficiency/current capability and layout |
| 1 A transient rail excursion / brownout | Direct | Mandatory waveform test pending |
| USB↔battery transfer/reset | Direct | No-reset target pending physical test |
| Upstream backfeed | Direct | Schematic and transfer verification pending |
| Final-node actual power | Direct | Quantitative V11 characterization pending |
| Runtime event recovery after a power reset | Partial | Hardware review records reset evidence; software recovery remains downstream scope |

#### Source and Evidence Register

| ID | Source | Source type | Supports | Version / applicability | Verification | Checked on | Limitations |
|---|---|---|---|---|---|---|---|
| SRC-01 | `docs/adr/ADR-0007-edge-power-subsystem.md` | Project decision | Product rail/source-transfer contract | Accepted 2026-09-07 | Verified | 2026-09-07 | Architecture only |
| SRC-02 | MPS MP2636 datasheet registered in `docs/evidence/IHAP-49/source-register.md` | Manufacturer | IN-to-SYS pass-through and boost/charger behavior | MP2636 Rev.1.02 | Verified for architecture review | 2026-09-07 | Final PCB dynamics/layout not covered |
| SRC-03 | `docs/evidence/IHAP-49/validation-plan.md` | Project validation contract | Continuous/load-step/transfer/current tests | IHAP-49 accepted handoff | Verified | 2026-09-07 | Execution pending IHAP-55 |
| SRC-04 | ADR-0001/0002/0003/0004/0005 | Project decisions | Accepted node loads and quantitative follow-up obligations | Current accepted ADRs | Verified | 2026-09-07 | Final custom-board measurements pending |

#### Implementation and Verification Evidence

| Evidence ID | Evidence | Evidence class | Expected result | Actual result | Status |
|---|---|---|---|---|---|
| EV-01 | IHAP-55 schematic/ERC/DRC/BOM review | Implementation | Post-regulation/equivalent, anti-backfeed, test points and current envelope are implemented | Not executed | `[UNVALIDATED]` |
| EV-02 | V2/V5/V6 regulated rail tests | Verification | Product 5 V remains within frozen steady-state limits in normal and battery conditions | Not executed | `[UNVALIDATED]` |
| EV-03 | V7 1 A load-step waveform | Verification | Meets frozen transient/reset/recovery criteria | Not executed | `[UNVALIDATED]` |
| EV-04 | V8/V9 source transfer/restoration | Verification | No backfeed/source oscillation; no-reset target evaluated | Not executed | `[UNVALIDATED]` |
| EV-05 | V11 final-node quantitative characterization | Verification | Required rail/current/load contributions recorded | Not executed | `[UNVALIDATED]` |
| EV-06 | V12 endurance | Verification | Measured backup duration for tested board/cell/configuration | Not executed | `[UNVALIDATED]` |

#### Treatment Effectiveness Review

**Review date:** Pending  
**Evidence reviewed:** EV-01 through EV-06 pending  
**Effectiveness:** Pending Evidence  
**Likelihood after treatment:** Pending Evidence  
**Impact after treatment:** Pending Evidence  
**Residual risk:** Pending Evidence  
**Project Owner decision required:** Yes

---

## 8. Traceability

| Relationship | Link | Effect / Rule |
|---|---|---|
| Accepted ADR | `docs/adr/ADR-0007-edge-power-subsystem.md` | Partially mitigates by defining the treatment; does not prove effectiveness |
| Implementation task | IHAP-55 | Custom PCB implementation and physical validation |
| Effectiveness tracking | IHAP-57 | Updates lifecycle/effectiveness after evidence |
| Remediation task | IHAP-56 | Creates canonical risk/treatment traceability and removes stale contracts |
| Validation contract | `docs/evidence/IHAP-49/validation-plan.md` | Defines mandatory tests |

---

## 9. Stakeholder Visibility

Stakeholder summaries may state that wired 5 V operation with battery backup is the accepted architecture and that physical rail/transfer effectiveness remains `[UNVALIDATED]`. Do not claim fault tolerance, seamless UPS, validated autonomy or production reliability before verification evidence.

---

## 10. Assessment History

| Date | Change | Treatment | Evidence | Decision |
|---|---|---|---|---|
| 2026-09-07 | Canonical risk created from IHAP-49 post-merge review; post-regulation/load-step/source-transfer controls made traceable | RT-R013-01 Approved | ADR-0007 + manufacturer source; physical evidence pending | Residual-risk decision Pending |

---

## 11. Review Notes

```text
[x] Risk statement, source trigger, assets and trust boundary are explicit.
[x] Existing controls are separated from planned treatment.
[x] RT-R013-01 has stable identity, strategy, lifecycle and Jira coordination.
[x] MP2636 pass-through is not mislabeled as regulated product SYS.
[x] Load-step and source-transfer evidence are mandatory, not inferred.
[x] Quantitative prior-ADR obligations include ADR-0003 and are transferred, not waived.
[x] Implementation and verification evidence remain separate.
[x] Missing proof preserves [UNVALIDATED].
[x] ADR inverse link is required and provided by IHAP-56 remediation.
[x] No residual-risk acceptance or reliability/safety claim is made.
```
