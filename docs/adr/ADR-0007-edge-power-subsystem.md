# ADR-0007 — Edge Power Subsystem

**Status:** Accepted  
**Date:** 2026-09-05  
**Updated:** 2026-09-07 — IHAP-56 post-merge remediation  
**Accepted:** 2026-09-07  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Jira:** [IHAP-49](https://niccolopiazzi01.atlassian.net/browse/IHAP-49)  
**PR:** [#34](https://github.com/pianic2/homeedge-ai-platform/pull/34)  
**Post-merge remediation:** [IHAP-56](https://niccolopiazzi01.atlassian.net/browse/IHAP-56) / [PR #35](https://github.com/pianic2/homeedge-ai-platform/pull/35)  
**Implementation follow-up:** [IHAP-55](https://niccolopiazzi01.atlassian.net/browse/IHAP-55)  
**Supersedes:** follow-up ownership only from ADR-0001, ADR-0002, ADR-0003, ADR-0004 and ADR-0005 where quantitative final-node power measurements were assigned to IHAP-49  
**Superseded by:** None

<!--
AI_AGENT_METADATA:
  document_type: architecture_decision_record
  issue: IHAP-49
  remediation_issue: IHAP-56
  status: Accepted
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
  - Normal source remains regulated 5 V USB-C.
  - Rechargeable 1S Li-ion remains backup only, not primary multi-day supply.
  - Selected cell remains LG INR18650-MJ1 unless explicitly superseded.
  - Final reference implementation converges to a custom core PCB, not stacked charger/boost/mux breakouts.
  - MP2636 is the preferred charger/power-path/battery-boost PMIC candidate, not evidence by itself of a regulated 5.0 V USB-powered SYS rail.
  - The final board must include post-regulation or an equivalent reviewed topology that keeps the product SYS rail regulated in both USB and battery modes.
  - Quantitative power measurements transferred from prior ADRs remain mandatory in IHAP-55; they are not waived.
  - The unprotected cell requires a cell-side over-current interruption element covering holder/BAT-net faults upstream of PMIC SYS limiting.
  - Reverse-cell procedure alone is not an acceptable control.
  - NTC functional and fault-state verification is mandatory downstream.
  - ADR acceptance does not accept or close R-012 or R-013 residual risk.
  - Do not infer validated autonomy from capacity arithmetic.
  - Do not claim safe, certified, fire-safe, compliant, production-ready or installable from prototype evidence.
  - IHAP-55 owns custom-board schematic/layout/fabrication/bring-up and transferred quantitative power validation.
  - IHAP-50 owns the canonical connection/interface matrix consumed by the PCB.
  - IHAP-51 owns final enclosure/mounting/serviceability.
  - IHAP-17 receives definitive board-level BOM/replication cost only after downstream implementation evidence.
-->

---

## 1. Context

The reference edge node combines an ESP32-C3 compute profile, HLK-LD2410C-class presence radar, one environmental-sensor profile, a passive reed-contact input and the accepted local OLED display.

The LD2410C requires a 5 V domain and is a material always-on load. IHAP-49 planning evidence places the current reference node near a central estimate of roughly **0.625 W at the 5 V load domain**, with uncertainty dominated by ESP32-C3/Wi-Fi duty cycle, the development-board implementation and OLED usage. This is a planning estimate, not a measured final-board value.

A 3.5 Ah-class 1S Li-ion cell is therefore an hours-scale backup source, not a multi-day primary supply. The Project Owner decided that the MVP should use wired USB-C power normally and retain a rechargeable battery only to bridge blackout, cable disconnection or normal-input failure.

During IHAP-49, the Project Owner further clarified the final hardware direction: the product should converge to a **small, efficient, easily installable, modular and scalable custom PCB**, rather than permanently stacking development boards and breakout modules.

---

## 2. Decision

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

This ADR was explicitly **Accepted by the Project Owner on 2026-09-07**. IHAP-56 is a post-merge remediation of traceability and implementation constraints; it does not redesign the accepted product direction.

### 2.1 Power-domain contract

The target final topology is:

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

The post-regulation requirement is intentional. MPS documents an **IN-to-SYS pass-through path when input power is present** and programmable SYS voltage in battery boost mode. Therefore MP2636 alone must not be treated as evidence that the USB-powered SYS node is regulated to exactly 5.0 V. IHAP-55 must either implement the downstream regulation stage or explicitly supersede the MP2636 topology with another reviewed design that satisfies the same product-bus contract.

Final physical implementation is owned by IHAP-55 and must preserve the module boundaries established by the accepted sensor decisions.

### 2.2 Selected cell

The reference cell model is **LG INR18650-MJ1**, EAN/GTIN `8438493099829`.

Current selection evidence records:

- 18650 flat-top, unprotected Li-ion;
- 3.6 V nominal;
- 3500 mAh typical / 3400 mAh minimum in the selected seller evidence;
- 10 A seller-listed discharge capability;
- approximately 18.2 mm × 65 mm seller-listed dimensions;
- selected seller: NKON;
- Project Owner order decision: 10 cells, EUR 19.90 subtotal + EUR 6.33 shipping = EUR 26.23 planned landed total.

Selection policy is **cost-first after minimum compatibility, provenance and evidence gates are met**.

The cell is unprotected, therefore protection is a **system responsibility**. The final PCB must not depend on the cell itself providing over-charge, over-discharge, over-current or reverse-insertion protection.

### 2.3 Integrated PMIC direction

The preferred first charger / power-path / battery-boost PMIC candidate is **Monolithic Power Systems MP2636GR-P**.

It is selected because one active, orderable IC covers the coupled functions that otherwise require multiple breakout boards:

- switch-mode 1S charging;
- system power-path management and system-load priority;
- programmable input-current limit and input-voltage regulation;
- selectable 4.2 V battery-full setting;
- programmable charge current;
- NTC battery-temperature input;
- reverse boost from battery to a programmable intermediate SYS rail;
- programmable boost current limit;
- pass-through OCP/OVP;
- boost short-circuit/OVP controls;
- battery-current monitoring.

**Implementation caveat:** MP2636's programmable SYS voltage applies in battery boost mode; with valid input present it uses an IN-to-SYS pass-through path. The preferred first implementation is therefore **MP2636 plus a downstream 5 V regulation stage, or a reviewed equivalent topology**. The exact post-regulator SKU is intentionally left to IHAP-55 schematic/BOM review.

**ETA9740** remains a cost-down alternative for a later revision. Its very low unit price and integrated bidirectional charger/boost are attractive, but the current evidence provides a weaker match to the first-revision requirements for battery-temperature monitoring and a cleanly bounded first implementation. It is not selected for the first reference PCB.

### 2.4 USB-C input contract

- 5 V only; USB Power Delivery is not required for MVP.
- Correct USB-C sink CC termination is mandatory.
- The custom board must support USB-C-to-USB-C 5 V sources and must not rely on the legacy USB-A-to-USB-C behavior required by the owned 4056E module.
- Reference source profile: **5 V with at least 1.5 A available/advertised**.
- Input-current limiting must prioritize the system load and prevent deliberate overdraw of the reference source profile.

### 2.5 Charging contract

- Battery CV target: **4.2 V**.
- Reference nominal charge-current target: **approximately 1.0 A**, with exact component values frozen by IHAP-55 schematic review.
- The system load has priority over battery charging when input power is constrained.
- **Charging while the node operates is permitted on the integrated power-path implementation**, subject to IHAP-55 validation.
- Charging while operating remains **prohibited for the owned stand-alone 4056E breakout path** because it is not a validated load-sharing controller.
- Battery-temperature monitoring via NTC or an explicitly reviewed equivalent control is mandatory on the custom board.
- IHAP-55 must functionally verify normal, hot-equivalent, cold-equivalent, NTC-open and NTC-short states with explicit charge-inhibit and deterministic-recovery criteria.

### 2.6 Product SYS and load-headroom contract

Reference product 5 V SYS target:

- nominal: **5.0 V regulated**;
- steady-state validation band: **4.75–5.25 V**, unless a downstream selected component requires a tighter limit;
- minimum design capability: **>=0.5 A continuous** across the accepted battery range and valid USB input range;
- transient/headroom target: **>=1.0 A** without reset or uncontrolled rail collapse.

These figures are **design-capability requirements**, not expected continuous node consumption.

The custom 3.3 V regulator must cover the accepted ESP32-C3 supply requirement plus the selected 3.3 V peripheral loads and must not silently inherit the unknown regulator capability of the current SuperMini-compatible development board.

### 2.7 Source transfer contract

- USB-C is the priority source.
- Loss of valid USB input must automatically transfer the node to battery-backed 5 V operation.
- Backfeed into the external USB source/cable is prohibited.
- **No-reset transfer is the reference target behavior** and remains `[UNVALIDATED]` until the fabricated custom board is tested.
- Restoration of normal power must be deterministic and must not create reset loops or source oscillation.

### 2.8 Low-voltage, over-current, polarity and serviceability contract

- The design must not intentionally operate the cell below the accepted manufacturer discharge boundary.
- A higher graceful low-battery warning/shutdown threshold is preferred where practical.
- Because the selected MJ1 is unprotected, the final design must include a **cell-side over-current interruption element** located so holder-lead/BAT-net faults upstream of PMIC SYS/boost limiting are covered. A fuse, resettable/electronic protection switch or reviewed equivalent is acceptable; exact threshold/time and component choice belong to IHAP-55 schematic/BOM review.
- PMIC SYS/boost current limiting alone is not sufficient evidence of protection for faults upstream of that limiting stage.
- The current holder is retained as the mechanical candidate; no replacement holder purchase is required at this decision stage.
- Because the holder is not mechanically keyed, **procedure alone is not an acceptable reverse-polarity control**.
- The final implementation must provide either electrical reverse-battery blocking/protection or a mechanically keyed interface/enclosure that physically prevents reverse insertion. Polarity labels and service instructions are supplementary only.
- Actual MJ1 fit/contact pressure remains physical evidence for IHAP-55/IHAP-51 after cell receipt.

---

## 3. Owned 4056E Module Disposition

The owned charger/protection board is **not selected as the final custom-PCB power implementation**.

Physical evidence remains useful:

- charger IC marking `4056E` observed;
- `8205A` dual MOSFET observed;
- separate six-pin protection controller observed, exact identity/thresholds `[UNVALIDATED]`;
- legacy 5 V / 1.55 A USB-A-to-USB-C source produced VIN 4.95 V;
- unloaded B/OUT readings approximately 4.19/4.18 V;
- tested USB-C-to-USB-C fast-charge source did not produce usable module input;
- in-circuit R3 measurements were polarity-dependent and therefore inconclusive.

Because this module is **rejected as the final reference implementation**, its unresolved protection-controller identity and exact charge-current programming are no longer blockers to accepting the architectural decision. They remain limitations of owned inventory.

---

## 4. Alternatives Considered

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
| Alternative PMIC/topology satisfying the same contract | Allowed only by explicit IHAP-55 review/supersession | Prevents lock-in if layout or physical evidence reveals a better implementation. |
| ETA9740 integrated custom-board path | Cost-down alternative | Much lower IC price but weaker fit to first-revision monitoring/power-path requirements. |
| LiPo pouch | Rejected | No product requirement justifies the different mechanical profile. |
| Replaceable primary cells | Rejected | Poor fit for always-on 5 V radar/Wi-Fi node. |

---

## 5. Consequences

### Positive

- Stable regulated 5 V product power contract regardless of normal or backup source.
- Backup requirement is bounded to blackout/cable-fault continuity rather than multi-day operation.
- Final hardware eliminates redundant breakout boards, connectors and loose wiring.
- Custom PCB direction improves compactness, installability and modular sensor interfaces.
- MP2636 still consolidates charging, power-path and battery boost while the post-regulator closes the normal-input SYS regulation gap identified in review.
- Cost-down remains possible through later PMIC/BOM substitution without changing the product power contract.

### Negative / Trade-offs

- A custom PCB introduces schematic, layout, DFM, fabrication and bring-up work.
- Maintaining a regulated 5 V product bus requires an additional on-board regulation function beyond MP2636's input pass-through behavior.
- Battery-related electrical and thermal behavior depends on the integrated design and must be physically validated.
- No-reset transfer, thermal behavior, charge current and measured runtime remain implementation evidence.
- The unprotected MJ1 requires cell-side protection, charging/temperature controls and disciplined enclosure/serviceability.

### Claim boundary

This ADR does not establish certification, fire safety, production readiness, commercial readiness or universal reliability. Physical implementation claims remain `[UNVALIDATED]` until IHAP-55 evidence exists.

---

## 6. Related Risks and Treatments

ADR-0007 affects two canonical power risks. The ADR defines required treatments but **does not close, accept, defer or verify either risk**.

| Risk | Treatment | Effect | Remaining exposure |
|---|---|---|---|
| [R-012 — Unprotected 1S Li-ion Battery Fault and Cell-Side Protection](../risks/records/R-012-unprotected-li-ion-battery-fault.md) | `RT-R012-01` — Implement and verify system-level 1S cell protection | **Partially mitigates** by mandating cell-side over-current interruption, bounded charging/NTC behavior and reverse-insertion prevention | Implementation/effectiveness remain `[UNVALIDATED]`; residual risk is Pending Evidence and requires later Project Owner decision |
| [R-013 — Edge Power Rail and Source-Transfer Integrity](../risks/records/R-013-edge-power-rail-transfer-integrity.md) | `RT-R013-01` — Implement and verify regulated dual-source product power | **Partially mitigates** by requiring post-regulated 5 V SYS, anti-backfeed, deterministic transfer and instrumented headroom validation | Regulator dynamics, source transfer, no-reset behavior and final-node current remain `[UNVALIDATED]`; residual risk is Pending Evidence |

Inverse links and the full treatment dossiers live in the Risk Records. IHAP-55 implements and verifies the treatments; IHAP-57 coordinates the subsequent effectiveness updates. Accepted ADR status must not be interpreted as treatment `Implemented`, `Verified` or residual-risk acceptance.

---

## 7. Implementation / Validation Handoff

IHAP-49 owns **the decision and electrical contract**.

IHAP-55 owns:

- exact schematic resistor/inductor/capacitor values;
- final PMIC footprint/layout and thermal design;
- exact 5 V post-regulator topology/SKU;
- exact 3.3 V regulator selection;
- USB-C ESD/input-protection implementation;
- cell-side over-current interruption implementation and rating rationale;
- battery reverse-polarity implementation;
- NTC part/placement and mandatory fault-state functional validation;
- PCB ERC/DRC and DFM;
- fabrication outputs;
- staged bring-up;
- charge-current/voltage/temperature validation;
- SYS rail/load/headroom measurements including mandatory 1 A load-step evidence;
- no-reset switchover and restoration tests;
- measured backup endurance;
- assembled-board replication cost.

### 7.1 Explicit ownership transfer from prior accepted ADRs

Earlier accepted hardware ADRs assigned quantitative final-node power work to IHAP-49. ADR-0007 explicitly **supersedes only that follow-up task ownership** and transfers the still-mandatory measurements to IHAP-55 because the Project Owner selected a custom-board final implementation.

The obligations are not waived:

- **ADR-0001:** quantitative rail, regulator, board current/peak and autonomy-related validation for the final ESP32-C3 implementation;
- **ADR-0002:** quantitative environmental-profile current contribution in the integrated node;
- **ADR-0003:** quantitative reed/pull-network closed-loop current and product-power impact;
- **ADR-0004:** display current measurement and resulting sleep/power policy;
- **ADR-0005:** LD2410C quantitative current/rail contribution and autonomy impact;
- integrated complete-node rail/current/brownout evidence.

IHAP-55 cannot close custom-board validation without these measurements.

IHAP-50 owns the final signal/connector matrix consumed by the PCB. IHAP-51 owns enclosure, battery retention, service access and sensor placement. IHAP-17 consumes final board-level cost after downstream implementation evidence.

The results of IHAP-55 may supersede this ADR if physical evidence shows the selected implementation direction cannot satisfy the frozen contract.

---

## 8. Evidence Links

| Evidence | Link |
|---|---|
| Project Owner decision record | `docs/evidence/IHAP-49/decision-record.md` |
| Custom-PCB power contract | `docs/evidence/IHAP-49/custom-pcb-power-contract.md` |
| Owned hardware evidence | `docs/evidence/IHAP-49/owned-hardware-evidence.md` |
| Charger characterization run | `docs/evidence/IHAP-49/IHAP49-CHARGER-C0-C1-01/run-record.md` |
| Power tree | `docs/evidence/IHAP-49/power-tree.md` |
| Planning power/autonomy budget | `docs/evidence/IHAP-49/power-budget.md` |
| Alternatives | `docs/evidence/IHAP-49/alternatives.md` |
| Validation handoff | `docs/evidence/IHAP-49/validation-plan.md` |
| Risk assessment summary | `docs/evidence/IHAP-49/risk-assessment.md` |
| Canonical battery risk | `docs/risks/records/R-012-unprotected-li-ion-battery-fault.md` |
| Canonical rail/transfer risk | `docs/risks/records/R-013-edge-power-rail-transfer-integrity.md` |
| Cost governance | `docs/evidence/IHAP-49/cost-governance.md` |
| Downstream contracts | `docs/evidence/IHAP-49/downstream-contracts.md` |
| Source register | `docs/evidence/IHAP-49/source-register.md` |
| Original acceptance PR | `https://github.com/pianic2/homeedge-ai-platform/pull/34` |
| Post-merge remediation PR | `https://github.com/pianic2/homeedge-ai-platform/pull/35` |

---

## 9. Review Gate

```text
[x] Battery role decided: backup only.
[x] Normal 5 V USB-C source decided.
[x] Exact reference cell selected.
[x] Cost-first selection rule recorded.
[x] Owned 4056E module physically characterized enough to bound its use and rejected as final implementation.
[x] Custom-PCB final direction recorded.
[x] MP2636 retained as preferred charger/power-path/battery-boost PMIC candidate.
[x] USB-powered SYS pass-through limitation remediated by mandatory downstream 5 V regulation or reviewed equivalent topology.
[x] USB-C, charge, product-SYS-current, source-transfer and protection contracts defined.
[x] Cell-side over-current interruption is mandatory for BAT-side faults upstream of PMIC SYS limiting.
[x] Reverse-polarity control strengthened: procedure alone prohibited.
[x] NTC functional/fault-state validation is mandatory downstream.
[x] Canonical R-012/R-013 treatments and inverse ADR links are recorded without claiming risk acceptance.
[x] Prior ADR quantitative power obligations, including ADR-0003, explicitly transfer to IHAP-55 rather than being waived.
[x] Mandatory 1 A load-step validation handed to IHAP-55.
[x] No redundant breakout procurement required for closure.
[x] Autonomy remains `[UNVALIDATED]` until measured downstream.
[x] Project Owner explicitly accepted ADR-0007 on 2026-09-07.
```
