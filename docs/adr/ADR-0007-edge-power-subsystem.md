# ADR-0007 — Edge Power Subsystem

**Status:** Accepted  
**Date:** 2026-09-05  
**Updated:** 2026-09-07  
**Accepted:** 2026-09-07  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Jira:** [IHAP-49](https://niccolopiazzi01.atlassian.net/browse/IHAP-49)  
**PR:** [#34](https://github.com/pianic2/homeedge-ai-platform/pull/34)  
**Implementation follow-up:** [IHAP-55](https://niccolopiazzi01.atlassian.net/browse/IHAP-55)  
**Supersedes:** None  
**Superseded by:** None

<!--
AI_AGENT_METADATA:
  document_type: architecture_decision_record
  issue: IHAP-49
  status: Accepted
  approval_authority: project_owner
  source_of_truth: github_versioned_repository_documentation
  jira_role: workflow_state_and_evidence_links
  confluence_role: stakeholder_navigation_only
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
  - Do not infer validated autonomy from capacity arithmetic.
  - Do not claim safe, certified, fire-safe, compliant, production-ready or installable from prototype evidence.
  - IHAP-55 owns custom-board schematic/layout/fabrication/bring-up.
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
    battery/system power-path management, battery-to-5 V backup conversion,
    required protections and the downstream 3.3 V rail.

External sensors remain modular where placement/serviceability requires it.
```

This ADR was explicitly **Accepted by the Project Owner on 2026-09-07**.

### 2.1 Power-domain contract

The target final topology is:

```text
USB-C 5 V normal input
        |
        v
Type-C sink termination + input protection
        |
        v
integrated 1S charger / system power path / battery boost
        |                         |
        |                         +----> LG INR18650-MJ1
        |                                  in serviceable holder
        v
regulated 5 V SYS bus
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

The preferred first custom-board implementation is **Monolithic Power Systems MP2636GR-P**.

It is selected because one active, orderable IC covers the coupled functions that otherwise require multiple breakout boards:

- switch-mode 1S charging;
- system power-path management and system-load priority;
- programmable input-current limit and input-voltage regulation;
- selectable 4.2 V battery-full setting;
- programmable charge current;
- NTC battery-temperature input;
- reverse boost from battery to a programmable SYS rail;
- programmable boost current limit;
- pass-through OCP/OVP;
- boost short-circuit/OVP controls;
- battery-current monitoring.

Its boost SYS voltage is programmable from 4.2 V to 6 V; the reference target is **5.0 V**.

**ETA9740** remains a cost-down alternative for a later revision. Its very low unit price and integrated bidirectional charger/boost are attractive, but the current evidence provides a weaker match to the first-revision requirements for separated input/SYS behavior and battery-temperature monitoring. It is not selected for the first reference PCB.

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

### 2.6 SYS and load-headroom contract

Reference 5 V SYS target:

- nominal: **5.0 V regulated**;
- minimum design capability: **>=0.5 A continuous** across the accepted battery range;
- transient/headroom target: **>=1.0 A** without reset or uncontrolled rail collapse.

These figures are **design-capability requirements**, not expected continuous node consumption.

The custom 3.3 V regulator must cover the accepted ESP32-C3 supply requirement plus the selected 3.3 V peripheral loads and must not silently inherit the unknown regulator capability of the current SuperMini-compatible development board.

### 2.7 Source transfer contract

- USB-C is the priority source.
- Loss of valid USB input must automatically transfer the node to battery-backed 5 V operation.
- Backfeed into the external USB source/cable is prohibited.
- **No-reset transfer is the reference target behavior** and remains `[UNVALIDATED]` until the fabricated custom board is tested.
- Restoration of normal power must be deterministic and must not create reset loops or source oscillation.

### 2.8 Low-voltage, polarity and serviceability contract

- The design must not intentionally operate the cell below the accepted manufacturer discharge boundary.
- A higher graceful low-battery warning/shutdown threshold is preferred where practical.
- The current holder is retained as the mechanical candidate; no replacement holder purchase is required at this decision stage.
- Because the holder is not mechanically keyed, reversed-cell insertion must be mitigated electrically and/or prevented by the final enclosure/service procedure.
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
| MP2636 integrated custom-board path | **Selected first implementation direction** | Integrates charger, PPM and boost with NTC and separated SYS behavior in one PMIC. |
| ETA9740 integrated custom-board path | Cost-down alternative | Much lower IC price but weaker fit to first-revision monitoring/power-path requirements. |
| LiPo pouch | Rejected | No product requirement justifies the different mechanical profile. |
| Replaceable primary cells | Rejected | Poor fit for always-on 5 V radar/Wi-Fi node. |

---

## 5. Consequences

### Positive

- Stable 5 V product power contract regardless of normal or backup source.
- Backup requirement is bounded to blackout/cable-fault continuity rather than multi-day operation.
- Final hardware can eliminate redundant breakout boards, connectors and wiring.
- Custom PCB direction improves compactness, installability and modular sensor interfaces.
- Integrated switch-mode charger/boost should improve efficiency relative to a linear charger + separate boost path.
- Cost-down remains possible through later PMIC/BOM substitution without changing the product power contract.

### Negative / Trade-offs

- A custom PCB introduces schematic, layout, DFM, fabrication and bring-up work.
- Battery safety-related behavior depends on the integrated design and must be physically validated.
- No-reset transfer, thermal behavior, charge current and measured runtime remain implementation evidence.
- The unprotected MJ1 requires system-level controls and disciplined enclosure/serviceability.

### Claim boundary

This ADR does not establish certification, fire safety, production readiness, commercial readiness or universal reliability. Physical implementation claims remain `[UNVALIDATED]` until IHAP-55 evidence exists.

---

## 6. Implementation / Validation Handoff

IHAP-49 owns **the decision and electrical contract**.

IHAP-55 owns:

- exact schematic resistor/inductor/capacitor values;
- final PMIC footprint/layout and thermal design;
- exact 3.3 V regulator selection;
- USB-C ESD/input-protection implementation;
- battery reverse-polarity implementation;
- NTC part/placement;
- PCB ERC/DRC and DFM;
- fabrication outputs;
- staged bring-up;
- charge-current/voltage/temperature validation;
- SYS rail/load/headroom measurements;
- no-reset switchover and restoration tests;
- measured backup endurance;
- assembled-board replication cost.

IHAP-50 owns the final signal/connector matrix consumed by the PCB. IHAP-51 owns enclosure, battery retention, service access and sensor placement. IHAP-17 consumes final board-level cost after downstream implementation evidence.

The results of IHAP-55 may supersede this ADR if physical evidence shows the selected implementation direction cannot satisfy the frozen contract.

---

## 7. Evidence Links

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
| Risk assessment | `docs/evidence/IHAP-49/risk-assessment.md` |
| Cost governance | `docs/evidence/IHAP-49/cost-governance.md` |
| Downstream contracts | `docs/evidence/IHAP-49/downstream-contracts.md` |
| Source register | `docs/evidence/IHAP-49/source-register.md` |

---

## 8. Review Gate

```text
[x] Battery role decided: backup only.
[x] Normal 5 V USB-C source decided.
[x] Exact reference cell selected.
[x] Cost-first selection rule recorded.
[x] Owned 4056E module physically characterized enough to bound its use and rejected as final implementation.
[x] Custom-PCB final direction recorded.
[x] Integrated charger / power-path / boost PMIC direction selected: MP2636GR-P.
[x] USB-C, charge, SYS-current, source-transfer and protection contracts defined.
[x] Validation and physical implementation explicitly handed to IHAP-55/IHAP-51.
[x] No redundant breakout procurement required for closure.
[x] Autonomy remains `[UNVALIDATED]` until measured downstream.
[x] Project Owner explicitly accepted ADR-0007 on 2026-09-07.
```
