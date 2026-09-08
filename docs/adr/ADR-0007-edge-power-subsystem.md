# ADR-0007 — Edge Power Subsystem

**Status:** Accepted  
**Date:** 2026-09-05  
**Updated:** 2026-09-08 — IHAP-56 post-merge remediation  
**Accepted:** 2026-09-07  
**Amendment status:** **Proposed** — IHAP-56 remediation controls added after PR #34 are not yet Project Owner approved  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Jira:** [IHAP-49](https://niccolopiazzi01.atlassian.net/browse/IHAP-49)  
**PR:** [#34](https://github.com/pianic2/homeedge-ai-platform/pull/34)  
**Post-merge remediation:** [IHAP-56](https://niccolopiazzi01.atlassian.net/browse/IHAP-56) / [PR #35](https://github.com/pianic2/homeedge-ai-platform/pull/35)  
**Implementation follow-up:** [IHAP-55](https://niccolopiazzi01.atlassian.net/browse/IHAP-55)  
**Supersedes:** accepted follow-up ownership only from ADR-0001, ADR-0002, ADR-0004 and ADR-0005 where quantitative final-node power measurements were assigned to IHAP-49; extension to ADR-0003 is Proposed by IHAP-56  
**Superseded by:** None

<!--
AI_AGENT_METADATA:
  document_type: architecture_decision_record
  issue: IHAP-49
  remediation_issue: IHAP-56
  status: Accepted
  amendment_status: Proposed
  approval_authority: project_owner
  source_of_truth: github_versioned_repository_documentation
  jira_role: workflow_state_and_evidence_links
  confluence_role: stakeholder_navigation_only
  related_risk_model: docs/risks/risk-model-baseline.md
  related_risks:
    - docs/risks/records/R-012-unprotected-li-ion-battery-fault.md
    - docs/risks/records/R-013-edge-power-rail-transfer-integrity.md
  unvalidated_claim_marker: "[UNVALIDATED]"
  task_scope: edge_power_subsystem_decision
  implementation_task: IHAP-55
  runtime_changes_allowed: false
  firmware_changes_allowed: false

HIDDEN_ANTI_REGRESSION_RULES:
  - The 2026-09-07 PR #34 baseline remains Accepted.
  - Normal source remains regulated 5 V USB-C.
  - Rechargeable 1S Li-ion remains backup only, not primary multi-day supply.
  - Selected cell remains LG INR18650-MJ1 unless explicitly superseded.
  - Final reference implementation converges to a custom core PCB, not stacked charger/boost/mux breakouts.
  - MP2636 is the preferred charger/power-path/battery-boost PMIC candidate, not evidence by itself of a regulated 5.0 V USB-powered SYS rail.
  - The accepted final board direction includes post-regulation or an equivalent reviewed topology that keeps the product SYS rail regulated in both USB and battery modes.
  - Accepted quantitative power ownership transfer covers ADR-0001, ADR-0002, ADR-0004 and ADR-0005; ADR-0003 extension remains Proposed until approved.
  - Reverse-cell procedure alone is not an acceptable control in the accepted baseline.
  - Cell-side over-current interruption, mandatory NTC fault-state verification, numeric thermal/low-voltage criteria, V13/V14/V15, bidirectional <=100 us V7, high/mid/low V8/V9 and the ADR-0003 ownership extension are IHAP-56 Proposed amendments until explicit Project Owner approval.
  - RT-R012-01 and RT-R013-01 remain Proposed until explicit Project Owner treatment approval evidence exists.
  - ADR acceptance does not approve later treatment lifecycle, accept residual risk, or close R-012/R-013.
  - Do not infer validated autonomy from capacity arithmetic.
  - Do not claim safe, certified, fire-safe, compliant, production-ready or installable from prototype evidence.
-->

---

## 1. Context

The reference edge node combines an ESP32-C3 compute profile, HLK-LD2410C-class presence radar, one environmental-sensor profile, a passive reed-contact input and the accepted local OLED display.

The LD2410C requires a 5 V domain and is a material always-on load. IHAP-49 planning evidence places the current reference node near a central estimate of roughly **0.625 W at the 5 V load domain**, with uncertainty dominated by ESP32-C3/Wi-Fi duty cycle, the development-board implementation and OLED usage. This is a planning estimate, not a measured final-board value.

A 3.5 Ah-class 1S Li-ion cell is therefore an hours-scale backup source, not a multi-day primary supply. The Project Owner decided that the MVP should use wired USB-C power normally and retain a rechargeable battery only to bridge blackout, cable disconnection or normal-input failure.

During IHAP-49, the Project Owner further clarified the final hardware direction: the product should converge to a **small, efficient, easily installable, modular and scalable custom PCB**, rather than permanently stacking development boards and breakout modules.

---

## 2. Accepted Decision — PR #34 baseline

```text
Normal source:
    regulated 5 V via USB-C

Backup source:
    one rechargeable 1S Li-ion 18650, backup only

Selected reference cell:
    LG INR18650-MJ1
    EAN/GTIN 8438493099829
    flat-top, unprotected, 3.6 V nominal, 3.5 Ah class

Final reference implementation direction:
    one custom core PCB integrating USB-C input, 1S charging,
    battery/system power-path management, battery backup conversion,
    a regulated 5.0 V product SYS rail, required protections
    and the downstream 3.3 V rail.

External sensors remain modular where placement/serviceability requires it.
```

This baseline was explicitly **Accepted by the Project Owner on 2026-09-07** through ADR-0007 / PR #34. IHAP-56 may document proposed remediation detail, but that later detail must not be rewritten as part of the 2026-09-07 acceptance unless the Project Owner explicitly approves the amendment/treatment scope.

### 2.1 Power-domain contract

The accepted target topology is:

```text
USB-C 5 V normal input
        |
        v
Type-C sink termination + input protection
        |
        v
MP2636-class 1S charger / system power path / battery boost
        |                         |
        |                         +----> LG INR18650-MJ1
        |                                  in serviceable holder
        v
intermediate SYS / pass-through-or-boost node
        |
        v
5 V post-regulation stage
(buck-boost or reviewed equivalent able to regulate across
both the USB pass-through and battery-boost intermediate range)
        |
        v
regulated 5.0 V product SYS bus
        |
        +----> LD2410C external module
        |
        +----> regulated 3.3 V rail
                    |
                    +----> ESP32-C3 core
                    +----> OLED interface
                    +----> DHT11/BME280 profile interface
                    +----> reed input network
```

The post-regulation requirement is accepted. MPS documents an **IN-to-SYS pass-through path when input power is present** and programmable SYS voltage in battery boost mode. Therefore MP2636 alone must not be treated as evidence that the USB-powered SYS node is regulated to exactly 5.0 V. IHAP-55 must either implement the downstream regulation stage or explicitly supersede the MP2636 topology with another reviewed design that satisfies the same product-bus contract.

### 2.2 Selected cell

The accepted reference cell model is **LG INR18650-MJ1**, EAN/GTIN `8438493099829`.

Selection evidence records:

- 18650 flat-top, unprotected Li-ion;
- 3.6 V nominal;
- 3500 mAh typical / 3400 mAh minimum in the selected seller evidence;
- 10 A seller-listed discharge capability;
- approximately 18.2 mm × 65 mm seller-listed dimensions;
- selected seller: NKON;
- Project Owner order decision: 10 cells, EUR 19.90 subtotal + EUR 6.33 shipping = EUR 26.23 planned landed total.

Selection policy is **cost-first after minimum compatibility, provenance and evidence gates are met**.

The cell is unprotected, therefore protection is a **system responsibility**. The accepted baseline does not imply that cell-level protection exists.

### 2.3 Integrated PMIC direction

The accepted preferred first charger / power-path / battery-boost PMIC candidate is **Monolithic Power Systems MP2636GR-P**.

It covers switch-mode 1S charging, system-load-priority power-path management, programmable input-current/input-voltage regulation, selectable 4.2 V battery setting, programmable charge current, NTC input, reverse battery boost, boost current limiting, pass-through OCP/OVP, boost short/OVP controls and battery-current monitoring.

**Accepted implementation caveat:** MP2636's programmable SYS voltage applies in battery boost mode; with valid input present it uses an IN-to-SYS pass-through path. The preferred first implementation is therefore **MP2636 plus a downstream 5 V regulation stage, or a reviewed equivalent topology**.

### 2.4 USB-C input contract

- 5 V only; USB Power Delivery is not required for MVP.
- Correct USB-C sink CC termination is mandatory.
- The custom board must support USB-C-to-USB-C 5 V sources.
- Reference source profile: **5 V with at least 1.5 A available/advertised**.
- Input-current limiting must prioritize the system load and prevent deliberate overdraw of the reference source profile.

### 2.5 Charging contract

- Battery CV target: **4.2 V**.
- Reference nominal charge-current target: **approximately 1.0 A**.
- The system load has priority over battery charging when input power is constrained.
- **Charging while the node operates is permitted on the integrated power-path implementation**, subject to downstream validation.
- Charging while operating remains **prohibited for the owned stand-alone 4056E breakout path** because it is not a validated load-sharing controller.
- Battery-temperature monitoring via NTC or an explicitly reviewed equivalent control is mandatory on the custom board.

### 2.6 Product SYS and load-headroom contract

Accepted product 5 V SYS target:

- nominal: **5.0 V regulated**;
- steady-state validation band: **4.75–5.25 V**, unless a downstream selected component requires a tighter limit;
- minimum design capability: **>=0.5 A continuous**;
- transient/headroom target: **>=1.0 A** without reset or uncontrolled rail collapse.

These figures are design-capability requirements, not expected continuous node consumption.

### 2.7 Source transfer contract

- USB-C is the priority source.
- Loss of valid USB input must automatically transfer the node to battery-backed 5 V operation.
- Backfeed into the external USB source/cable is prohibited.
- **No-reset transfer is the reference target behavior** and remains `[UNVALIDATED]` until fabricated-board evidence exists.
- Restoration of normal power must be deterministic and must not create reset loops or source oscillation.

### 2.8 Low-voltage, polarity and serviceability contract

- The design must not intentionally operate the cell below the accepted manufacturer discharge boundary.
- A higher graceful low-battery warning/shutdown threshold is preferred where practical.
- The current holder is retained as the mechanical candidate; no replacement holder purchase is required at this decision stage.
- Because the holder is not mechanically keyed, **procedure alone is not an acceptable reverse-polarity control**.
- The final implementation must provide either electrical reverse-battery blocking/protection or a mechanically keyed interface/enclosure that physically prevents reverse insertion. Polarity labels and service instructions are supplementary only.
- Actual MJ1 fit/contact pressure remains physical evidence for IHAP-55/IHAP-51 after cell receipt.

### 2.9 Owned 4056E module disposition

The owned charger/protection board is **not selected as the final custom-PCB power implementation**. Recorded C0/C1 evidence remains historical/bench evidence only; unresolved controller identity and exact RPROG are not final-architecture characteristics.

### 2.10 Proposed IHAP-56 amendment package — NOT YET ACCEPTED

The following remediation additions were created after PR #34 and are **Proposed** until explicit Project Owner approval. They must not be consumed by IHAP-55 as accepted ADR requirements merely because this file's baseline status is `Accepted`:

- `RT-R012-01`: explicit cell-side over-current interruption covering holder/BAT-net faults upstream of PMIC SYS limiting;
- mandatory NTC normal/hot/cold/open/short functional verification;
- manufacturer-derived numeric thermal PASS/FAIL limits and pre-test thermal table;
- first-reference numeric low-voltage cutoff/recovery/hysteresis policy;
- worst-case input-current-limit <=1.50 A plus combined node+charging V14 verification;
- bidirectional baseline↔1 A V7 with <=100 µs current-edge requirement;
- high/mid/low battery V8/V9 transfer/restoration coverage, including explicit zero-reset restoration criterion for no-reset effectiveness verification;
- installed-path V13 cell-side over-current verification and V15 bounded electrical reverse-blocking verification;
- extension of quantitative ownership transfer to **ADR-0003 / reed current**.

These additions may be reviewed and strengthened inside PR #35 while Proposed. Approval of ADR-0007 / PR #34 does not approve them retroactively.

---

## 3. Alternatives Considered

| Alternative | Outcome | Reason |
|---|---|---|
| Regulated 5 V USB-C only | Rejected as complete subsystem; retained as normal source | Does not satisfy blackout/cable-fault backup requirement. |
| Rechargeable 1S battery as primary source | Rejected | Current node load makes a single 18650 hours-scale rather than multi-day. |
| 5 V USB-C normal + 1S backup | **Selected** | Matches the actual continuity requirement. |
| Protected 18650 | Rejected for reference direction | Higher cost/length and duplicates system-level protection. |
| LG INR18650-MJ1 unprotected | **Selected cell** | Meets capacity/current requirement with favorable landed cost and identifiable provenance. |
| Owned 4056E + separate boost + mux breakouts | Rejected as final implementation | Useful for bench characterization but increases board stacking, wiring, cost and failure points. |
| TPS61023 + TPS2116 modular path | Rejected as final implementation | Technically viable but redundant once custom PCB integration is the declared target. |
| MP2636 + downstream 5 V regulation on custom PCB | **Selected first implementation direction** | Retains integrated charger/PPM/battery boost/NTC while explicitly regulating the product 5 V bus in both USB and battery modes. |
| Alternative PMIC/topology satisfying the same accepted baseline | Allowed only by explicit IHAP-55 review/supersession | Prevents lock-in if layout or physical evidence reveals a better implementation. |
| ETA9740 integrated custom-board path | Cost-down alternative | Lower IC price but weaker fit to first-reference evidence requirements. |
| LiPo pouch | Rejected | No product requirement justifies the different mechanical profile. |
| Replaceable primary cells | Rejected | Poor fit for always-on 5 V radar/Wi-Fi node. |

---

## 4. Consequences

### Positive

- Stable regulated 5 V product power contract regardless of normal or backup source.
- Backup requirement is bounded to blackout/cable-fault continuity rather than multi-day operation.
- Final hardware eliminates redundant breakout boards, connectors and loose wiring.
- Custom PCB direction improves compactness, installability and modular sensor interfaces.
- MP2636 still consolidates charging, power-path and battery boost while the accepted post-regulator closes the normal-input SYS regulation gap.

### Negative / Trade-offs

- A custom PCB introduces schematic, layout, DFM, fabrication and bring-up work.
- Maintaining a regulated 5 V product bus requires an additional on-board regulation function beyond MP2636's input pass-through behavior.
- Battery-related electrical and thermal behavior depends on the integrated design and must be physically validated.
- No-reset transfer, thermal behavior, charge current and measured runtime remain implementation evidence.
- The unprotected MJ1 requires system-level controls; the additional cell-side interruption and detailed verification scheme proposed by IHAP-56 are not yet accepted amendments.

### Claim boundary

This ADR does not establish certification, fire safety, production readiness, commercial readiness or universal reliability. Physical implementation claims remain `[UNVALIDATED]` until downstream evidence exists.

---

## 5. Related Risks and Treatments

ADR-0007 affects two canonical power risks. The table below distinguishes the **allowed effect of the accepted baseline** from the later Proposed treatment detail.

| Risk | Treatment | ADR effect | Remaining exposure |
|---|---|---|---|
| [R-012 — Unprotected 1S Li-ion Battery Fault and Cell-Side Protection](../risks/records/R-012-unprotected-li-ion-battery-fault.md) | `RT-R012-01` — **Proposed** | **Partially mitigates** through the accepted backup-only, system-responsibility protection and reverse-polarity-prevention baseline | Cell-side interruption, NTC fault-state, numeric low-voltage/thermal detail, implementation and effectiveness remain Proposed / `[UNVALIDATED]` |
| [R-013 — Edge Power Rail and Source-Transfer Integrity](../risks/records/R-013-edge-power-rail-transfer-integrity.md) | `RT-R013-01` — **Proposed** | **Partially mitigates** through the accepted regulated product SYS, post-regulation/equivalent, USB priority, anti-backfeed and headroom/source-transfer baseline | Detailed source-limit, dynamic, high/mid/low restoration and effectiveness evidence remain Proposed / `[UNVALIDATED]` |

The Risk Records contain the inverse ADR links. Accepted ADR status does not make either treatment `Approved`, `In Progress`, `Implemented` or `Verified`, and does not accept residual risk.

---

## 6. Follow-up Work

### Accepted baseline follow-up

| Item | Tracking |
|---|---|
| Freeze MP2636 implementation or explicitly reviewed superseding topology | IHAP-55 |
| Select and justify downstream regulated 5 V stage and 3.3 V regulator | IHAP-55 |
| Implement accepted reverse-insertion prevention | IHAP-55 / IHAP-51 for physical keying if used |
| Execute PCB ERC/DRC/DFM, fabrication and staged bring-up | IHAP-55 |
| Execute accepted 0.5 A continuous and 1.0 A headroom validation | IHAP-55 |
| Execute accepted USB loss/restoration/backfeed validation | IHAP-55 |
| Execute final-node quantitative power measurements transferred from ADR-0001/0002/0004/0005 | IHAP-55 |
| Measure backup endurance before any measured autonomy claim | IHAP-55 |
| Freeze final signal/connector matrix consumed by PCB | IHAP-50 |
| Verify enclosure, battery retention/service access and sensor placement | IHAP-51 |
| Reconcile final assembled-board BOM/replication cost | IHAP-17 after IHAP-55 evidence |

### Proposed IHAP-56 follow-up — blocked pending approval

| Item | Tracking |
|---|---|
| Obtain explicit Project Owner decision for RT-R012-01 / RT-R013-01 and the amendment package | IHAP-56 / IHAP-57 |
| Cell-side over-current interruption + installed-path V13 | Proposed — IHAP-55 after approval |
| Mandatory NTC normal/hot/cold/open/short verification | Proposed — IHAP-55 after approval |
| Numeric thermal and low-voltage criteria; V14/V15; strengthened V7/V8/V9 | Proposed — IHAP-55 after approval |
| Extend quantitative ownership to ADR-0003/reed current | Proposed — requires explicit approval/accepted reassignment |
| Update treatment lifecycle/effectiveness from decision + implementation/verification evidence | IHAP-57 after approval/evidence |

### 6.1 Accepted ownership transfer and Proposed ADR-0003 correction

The accepted PR #34 baseline transfers quantitative final-node power work from **ADR-0001, ADR-0002, ADR-0004 and ADR-0005** to IHAP-55. Those obligations are not waived.

IHAP-56 identifies a completeness gap for **ADR-0003** reed/pull-network current. Extending ADR-0007's ownership-transfer claim to ADR-0003 is a **Proposed amendment**, not part of the 2026-09-07 acceptance record. Until explicitly approved or reassigned by another accepted decision, ADR-0003's original ownership semantics remain authoritative.

The results of IHAP-55 may supersede ADR-0007 if physical evidence shows the accepted implementation direction cannot satisfy the baseline contract.

---

## 7. Evidence Links

| Evidence | Link |
|---|---|
| Jira decision issue | [IHAP-49](https://niccolopiazzi01.atlassian.net/browse/IHAP-49) |
| Jira remediation issue | [IHAP-56](https://niccolopiazzi01.atlassian.net/browse/IHAP-56) |
| Project Owner decision record | `docs/evidence/IHAP-49/decision-record.md` |
| Custom-PCB power contract | `docs/evidence/IHAP-49/custom-pcb-power-contract.md` |
| Owned hardware evidence | `docs/evidence/IHAP-49/owned-hardware-evidence.md` |
| Charger characterization run | `docs/evidence/IHAP-49/IHAP49-CHARGER-C0-C1-01/run-record.md` |
| Power tree | `docs/evidence/IHAP-49/power-tree.md` |
| Planning power/autonomy budget | `docs/evidence/IHAP-49/power-budget.md` |
| Alternatives | `docs/evidence/IHAP-49/alternatives.md` |
| Validation handoff | `docs/evidence/IHAP-49/validation-plan.md` |
| Risk assessment summary | `docs/evidence/IHAP-49/risk-assessment.md` |
| Related Risk Record R-012 | `docs/risks/records/R-012-unprotected-li-ion-battery-fault.md` |
| Related treatment | `RT-R012-01` — Proposed |
| Related Risk Record R-013 | `docs/risks/records/R-013-edge-power-rail-transfer-integrity.md` |
| Related treatment | `RT-R013-01` — Proposed |
| Original acceptance PR | [PR #34](https://github.com/pianic2/homeedge-ai-platform/pull/34) |
| Post-merge remediation PR | [PR #35](https://github.com/pianic2/homeedge-ai-platform/pull/35) |

---

## 8. Review Notes

```text
[x] Accepted PR #34 baseline and Proposed IHAP-56 amendment scope are explicitly separated.
[x] No later treatment/amendment detail is represented as retroactively accepted.
[x] R-012/R-013 inverse links declare the allowed effect `Partially mitigates` for the accepted baseline.
[x] RT-R012-01 / RT-R013-01 remain Proposed pending explicit Project Owner approval.
[x] ADR-0003 ownership extension is Proposed, not silently added to the accepted supersession claim.
[x] [UNVALIDATED] is preserved on unproven implementation/effectiveness/autonomy claims.
[x] No safety/certification/production-readiness claim is introduced.
[ ] Independent PR #35 review must complete on the final head with no unresolved blocking finding before merge.
```
