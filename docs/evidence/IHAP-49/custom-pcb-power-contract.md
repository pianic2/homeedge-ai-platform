# IHAP-49 — Custom PCB Power Contract

**Status:** Accepted architecture contract — Project Owner approval 2026-09-07; post-merge remediation tracked by IHAP-56  
**Implementation owner:** IHAP-55 — Integrated Modular Edge PCB — Custom Mainboard Design and Prototype

## Purpose

Freeze the electrical and product requirements that IHAP-49 owns without forcing the reference MVP to permanently use stacked breakout modules.

The final reference direction is a **single custom core PCB**. IHAP-49 defines the accepted power contract; IHAP-55 implements, lays out, fabricates and physically validates it. R-012/R-013 are the canonical risk-treatment dossiers and their treatment lifecycle remains **Proposed** until explicit Project Owner treatment approval exists.

## Frozen product-level decision

- Normal node power: **regulated 5 V via USB-C**.
- Backup: **one rechargeable 1S Li-ion 18650** used only for blackout / cable-input interruption.
- Selected reference cell: **LG INR18650-MJ1**, EAN/GTIN `8438493099829`, flat-top unprotected 18650, 3.6 V nominal, 3.5 Ah class.
- Multi-day battery-only operation is not an MVP requirement.
- Planning backup runtime remains approximately **12–20 h**, central estimate ~16 h, and is `[UNVALIDATED]` until measured on the fabricated implementation.
- Cost is the first differentiator after minimum compatibility, provenance and evidence gates are met.

## Final-board topology requirement

The accepted **5.0 V regulated product bus** must not depend on the MP2636 input pass-through path being exactly 5.0 V. MPS documents an IN-to-SYS pass-through path when input power is present and a programmable SYS voltage in battery boost mode. The final PCB therefore requires an explicit regulation stage or equivalent topology after the charger/power-path stage so both USB-powered and battery-powered operation satisfy the same 5 V product-bus contract.

The unprotected cell also requires a protection boundary before PMIC-output protection can be relied upon: BAT-side over-current interruption is mandatory, and reverse insertion must be electrically blocked or physically impossible through keying.

```text
USB-C 5 V input
      |
      v
input protection / Type-C sink termination
      |
      v
MP2636-class 1S charger + system power path + battery boost
      |                         ^
      |                         |
      |                 cell-side protection boundary
      |                 - over-current interruption
      |                 - reverse block OR physical keying
      |                         ^
      |                         |
      |                 serviceable 18650 holder
      |                         ^
      |                         |
      |                 LG INR18650-MJ1
      v
intermediate SYS / pass-through-or-boost node
      |
      v
5 V post-regulation stage
(buck-boost or reviewed equivalent capable of regulating across
both the USB pass-through and battery-boost intermediate range)
      |
      v
regulated 5.0 V product SYS bus
      |
      +----> LD2410C external module
      |
      +----> 3.3 V regulator --> ESP32-C3 core + OLED / ENV / reed interface domain
```

The final design must not require separate TP4056/4056E, boost and power-mux **breakout boards**. Additional ICs/passives on the single custom PCB are allowed when required to satisfy the frozen contract.

## Reference integrated PMIC direction

**Preferred charger / power-path / battery-boost PMIC candidate for IHAP-55:** `MP2636GR-P` (Monolithic Power Systems).

It provides 1S switch-mode charging, system-load-priority power-path management, programmable input-current/input-voltage regulation, selectable 4.2 V battery charge voltage, programmable charge current, NTC input, reverse battery boost, boost current limiting, pass-through OCP/OVP, boost short/OVP controls and battery-current monitoring.

**Important implementation constraint:** MP2636 alone is **not evidence of regulated 5.0 V SYS while USB input is present**. IHAP-55 must either use MP2636 plus a downstream 5 V regulation stage that covers the complete intermediate range or explicitly supersede the topology with another reviewed implementation satisfying the same product-bus contract.

`ETA9740` remains a future cost-down candidate only.

## Electrical contract

### USB-C input and source-current limit

- 5 V only; USB Power Delivery is **not required** for MVP.
- Correct Type-C sink CC termination is mandatory (`Rd`, normally 5.1 kΩ on CC1/CC2 unless the selected front end requires otherwise).
- USB-C-to-USB-C 5 V operation is mandatory for the final PCB.
- Reference source profile: **5 V, at least 1.5 A available/advertised**.
- Input-current limit must be configured so its **worst-case maximum including tolerance is <=1.50 A**.
- IHAP-55 must execute the combined node-load + charging **V14** test and prove charge current yields to system load before product SYS leaves 4.75–5.25 V.

### Charging and battery-temperature control

- Cell CV target: **4.2 V**; validation maximum-charge envelope **4.20 ±0.05 V**.
- Reference charge-current target: **~1.0 A nominal**.
- System-load path has priority over battery charging when input power is constrained.
- Charging while the node operates is permitted only on the integrated power-path implementation; it remains prohibited for the owned 4056E breakout as a stand-alone path.
- Battery NTC monitoring is mandatory unless a reviewed equivalent provides equal/stronger bounded control.
- Functional verification is mandatory for **normal, hot, cold, open and short** NTC conditions; out-of-range and fault states must inhibit charging or be intercepted by an explicitly reviewed fail-bounded equivalent.
- Recovery must be deterministic without charge oscillation.

### Thermal contract

Manufacturer-derived numeric limits govern PASS/FAIL, not mere qualitative temperature observation.

Already frozen:

- LG MJ1 charging operating temperature: **0–45 °C**;
- LG MJ1 discharge operating temperature: **-20–60 °C**;
- MP2636 recommended operating junction temperature: **-40 to +125 °C**;
- MP2636 thermal shutdown around **150 °C** is protective behavior and entering it is a validation FAIL.

Before V4/V6, IHAP-55 must register numeric manufacturer operating/rated limits for the selected post-regulator, 3.3 V regulator, inductor and protection components and define how measured board/case temperature maps to the applicable junction/hotspot limit. A rail-stable run that exceeds a registered temperature limit is FAIL.

### Cell-side over-current protection

Because the reference MJ1 is unprotected:

- a **cell-side over-current interruption element** is mandatory;
- it must cover holder-lead/BAT-net faults before reliance on PMIC SYS/boost output limiting;
- fuse, resettable/electronic protection switch or reviewed equivalent are acceptable;
- exact threshold/time must be justified from legitimate charge/discharge/transient current and conductor/trace ampacity;
- PMIC SYS/boost limiting alone is insufficient;
- V13 uses a bounded current-limited fixture; the real Li-ion cell is not intentionally hard-shorted.

### 5 V product SYS bus and dynamic headroom

- Nominal target: **5.0 V regulated**.
- Steady-state band: **4.75–5.25 V**, unless a downstream component requires tighter limits.
- Minimum capability: **>=0.5 A continuous** across accepted battery and valid USB input ranges.
- Transient/headroom target: **>=1.0 A** without reset/uncontrolled rail collapse.
- V7 must exercise **baseline->1.0 A and 1.0 A->baseline** with measured 10–90% current-transition time **<=100 µs** on each edge unless final load evidence requires a faster reference.
- Generic transient limits: product SYS must not fall below **4.5 V** or rise above **5.5 V** and must return to 4.75–5.25 V within **2 ms**, unless selected loads require tighter limits.

### 3.3 V domain

- Provide a regulated 3.3 V rail compatible with the accepted ESP32-C3 compute profile and 3.3 V peripherals.
- Cover Espressif current requirements plus OLED/environmental/reed-interface margin.
- Do not silently inherit the unknown regulator capability of the SuperMini-compatible development board.

### Battery low-voltage behavior

The first-reference numeric policy is:

- battery-backed cutoff: **2.70 V ±0.05 V** at BATT under the frozen validation load/measurement condition;
- deliberate sustained operation below the MJ1 manufacturer discharge-end voltage **2.50 V** is prohibited;
- restart after low-voltage cutoff requires **BATT >=3.00 V ±0.05 V** or valid USB input;
- no cutoff/restart oscillation is allowed between the thresholds;
- a change to these values requires explicit reviewed justification against the MJ1 specification and converter requirements.

### Source transfer

- Normal USB power has priority.
- Loss of valid USB must transfer automatically to battery-backed regulated 5 V.
- Backfeed into USB is prohibited.
- No-reset transfer remains the target and `[UNVALIDATED]` until tested.
- V8/V9 must verify transfer/restoration at representative **high 4.10±0.10 V, mid 3.60±0.10 V and low 2.80±0.05 V** battery conditions, with relevant node loads.
- Restoration must be deterministic without reset loops/source oscillation.

### Reverse polarity / serviceability

- The selected cell is unprotected; system protection is a product responsibility.
- Existing holder remains a mechanical candidate but is not keyed against reverse insertion.
- Procedure alone is not acceptable.
- Final implementation must provide either electrical reverse-battery blocking/protection or mechanical keying that physically prevents reversed insertion.
- If electrical blocking is used, **V15 is mandatory**: use a 4.20 V battery simulator with 10 mA current limit, require <=1 mA steady reversed-source current, product 5 V/3.3 V rails <=0.3 V, no damage/heating, and normal recovery after correct polarity.
- The real Li-ion cell must not be intentionally reverse-connected.
- Actual MJ1 holder fit/contact pressure remains IHAP-55/IHAP-51 evidence.

## Owned 4056E module disposition

The owned USB-C charger/protection module is **not selected as the final custom-PCB power architecture**. Its C0/C1 evidence remains historical/bench evidence only. Unresolved controller identity/RPROG must not become assumed final-board characteristics.

## Procurement rule

Until IHAP-55 schematic/BOM review requires exact parts:

- purchase the selected LG MJ1 cells because they persist in the architecture;
- do **not** buy TPS61023, TPS2116, additional charger modules or redundant breakouts solely to emulate integrated functions;
- existing modules may be used as bench references;
- any new breakout purchase requires a specific validation blocker and Project Owner approval.

## Accepted follow-up ownership supersession

ADR-0007 does **not cancel** quantitative power evidence from earlier accepted hardware ADRs. It supersedes only task ownership from IHAP-49 to IHAP-55 for measurements requiring the final custom implementation.

Mandatory obligations transferred to IHAP-55:

- ADR-0001: quantitative rail/regulator/current/peak/autonomy validation for final ESP32-C3 implementation;
- ADR-0002: environmental-profile current contribution;
- ADR-0003: final reed/pull-network closed-loop current contribution;
- ADR-0004: display current and resulting sleep/power policy;
- ADR-0005: LD2410C current/rail/autonomy contribution;
- integrated 5 V / 3.3 V rail, current and brownout evidence.

This is an ownership transfer, not a waiver.

## Canonical risk / treatment links

- `docs/risks/records/R-012-unprotected-li-ion-battery-fault.md` — `RT-R012-01` **Proposed**;
- `docs/risks/records/R-013-edge-power-rail-transfer-integrity.md` — `RT-R013-01` **Proposed**.

ADR-0007 acceptance does not approve these later treatment lifecycle states and does not accept/close either risk. IHAP-55 implementation/effectiveness remains `[UNVALIDATED]`; IHAP-57 coordinates subsequent lifecycle/effectiveness updates after explicit treatment approval.

## Handoff / closure boundary

`validation-plan.md` is the mandatory physical test contract and `downstream-contracts.md` is the primary downstream ownership surface. IHAP-49 remains the completed architecture-decision task. IHAP-55 owns schematic/layout/fabrication and mandatory implementation tests; IHAP-51 owns enclosure/serviceability; IHAP-57 tracks treatment lifecycle/effectiveness. Contradictory evidence must reopen/supersede ADR-0007 rather than silently weaken the accepted contract.
