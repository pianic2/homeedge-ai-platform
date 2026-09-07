# IHAP-49 — Custom PCB Power Contract

**Status:** Accepted architecture contract — Project Owner approval 2026-09-07; post-merge remediation tracked by IHAP-56  
**Implementation owner:** IHAP-55 — Integrated Modular Edge PCB — Custom Mainboard Design and Prototype

## Purpose

Freeze the electrical and product requirements that IHAP-49 owns without forcing the reference MVP to permanently use stacked breakout modules.

The final reference direction is a **single custom core PCB**. IHAP-49 defines the accepted power contract; IHAP-55 implements, lays out, fabricates and physically validates that contract. R-012/R-013 are the canonical risk-treatment dossiers.

## Frozen product-level decision

- Normal node power: **regulated 5 V via USB-C**.
- Backup: **one rechargeable 1S Li-ion 18650** used only for blackout / cable-input interruption.
- Selected reference cell: **LG INR18650-MJ1**, EAN/GTIN `8438493099829`, flat-top unprotected 18650, 3.6 V nominal, 3.5 Ah class.
- Multi-day battery-only operation is not an MVP requirement.
- Planning backup runtime remains approximately **12–20 h**, central estimate ~16 h, and is `[UNVALIDATED]` until measured on the fabricated implementation.
- Cost is the first differentiator after minimum compatibility, provenance and evidence gates are met.

## Final-board topology requirement

The accepted **5.0 V regulated product bus** must not depend on the MP2636 input pass-through path being exactly 5.0 V. MPS documents an IN-to-SYS pass-through path when input power is present and a programmable SYS voltage in battery boost mode. The final PCB therefore requires an explicit regulation stage or equivalent topology after the charger/power-path stage so both USB-powered and battery-powered operation satisfy the same 5 V product-bus contract.

The unprotected cell also requires a protection boundary **before PMIC-output protection can be relied upon**: BAT-side over-current interruption is mandatory, and reverse insertion must be electrically blocked or physically impossible through keying.

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

The final design must not require separate TP4056/4056E, boost and power-mux **breakout boards**. Additional ICs/passives on the single custom PCB are allowed when required to satisfy the frozen electrical contract.

## Reference integrated PMIC direction

**Preferred charger / power-path / battery-boost PMIC candidate for IHAP-55:** `MP2636GR-P` (Monolithic Power Systems).

It provides the coupled functions that the breakout stack otherwise needs:

- 1S Li-ion / Li-polymer switch-mode charging;
- system power-path management with system-load priority;
- programmable input-current limit and input-voltage regulation;
- selectable 4.2 V battery charge voltage;
- programmable charge current;
- NTC battery-temperature input;
- reverse boost from the battery to a programmable intermediate SYS voltage;
- programmable boost output-current limit;
- pass-through over-current / over-voltage controls;
- boost short-circuit and over-voltage controls;
- battery-current monitor output.

**Important implementation constraint:** the MP2636 alone is **not evidence of a regulated 5.0 V SYS rail while USB input is present**. IHAP-55 must therefore either:

1. use MP2636 with a downstream 5 V regulation stage capable of both buck and boost behavior across the complete intermediate range; or
2. explicitly supersede the MP2636 topology with another reviewed implementation that independently satisfies the same 5.0 V product-bus contract.

The exact intermediate boost setpoint, downstream-regulator SKU and efficiency trade-off are IHAP-55 schematic/BOM decisions. The **product output target remains 5.0 V regulated**.

`ETA9740` remains a future cost-down candidate, not the first-reference choice, until equal evidence demonstrates no regression of this contract.

## Electrical contract

### USB-C input

- 5 V only; USB Power Delivery is **not required** for MVP.
- Type-C sink implementation must include correct CC termination (`Rd`, normally 5.1 kΩ on CC1 and CC2 unless the selected front end requires otherwise).
- The final board must work from USB-C-to-USB-C 5 V sources that advertise sufficient current.
- Reference source profile: **5 V, at least 1.5 A available/advertised**.
- Input-current limit must be configured so the node + charging load cannot intentionally exceed the reference input profile.

### Charging and battery-temperature control

- Cell CV target: **4.2 V**.
- Reference charge-current target: **~1.0 A nominal**, subject to final calculation and physical validation in IHAP-55.
- The system-load path has priority over battery charging when input power is constrained.
- Charging while the node operates is permitted only on the integrated power-path implementation; it remains prohibited for the owned 4056E breakout as a stand-alone charger path.
- Battery NTC monitoring is mandatory unless a reviewed equivalent gives equal or stronger bounded control.
- The final NTC implementation must be functionally verified for **normal, hot, cold, open and short** conditions.
- Hot/cold out-of-window conditions and NTC open/short faults must inhibit charging or be intercepted by an explicitly reviewed equivalent fail-bounded control.
- Recovery to the valid NTC state must be deterministic and must not create charge oscillation.

### Cell-side over-current protection

Because the reference MJ1 is unprotected:

- a **cell-side over-current interruption element** is mandatory;
- it must be located so a short/over-current on holder leads or the BAT net downstream of the cell is covered **before** reliance on PMIC SYS/boost output limiting;
- acceptable architectures include a fuse, resettable/electronic protection switch, or reviewed equivalent;
- the exact threshold/time must be justified from legitimate worst-case charge/discharge/transient current and conductor/trace ampacity;
- PMIC SYS/boost current limiting alone is **not sufficient** for a BAT-side fault upstream of that limiting stage;
- verification must use a bounded current-limited fixture or equivalent method; do not intentionally hard-short the actual Li-ion cell.

### 5 V product SYS bus

- Nominal target: **5.0 V regulated**.
- Steady-state acceptance band for IHAP-55 validation: **4.75–5.25 V** unless a downstream component requires a tighter limit.
- Must power LD2410C and the downstream 3.3 V regulator.
- Minimum design capability: **>=0.5 A continuous** at the product 5 V SYS bus across the accepted battery operating range and valid USB input range.
- Transient/headroom target: **>=1.0 A** without reset or uncontrolled rail collapse.
- Current capability is a design envelope, not an assertion that the node continuously draws this current.

### 3.3 V domain

- The custom PCB must provide a regulated 3.3 V rail compatible with the accepted ESP32-C3 compute profile and 3.3 V peripherals.
- The rail design must cover the Espressif supply-current requirement plus OLED/environmental/reed-interface margin.
- The final design must not silently reuse the unknown regulator capability of the current SuperMini-compatible development board.

### Battery low-voltage behavior

- The design must not intentionally operate the MJ1 below its accepted minimum-discharge boundary.
- A graceful low-battery warning/shutdown threshold above the hard protection boundary is preferred where practical.
- Exact cutoff and recovery values are implementation/test evidence in IHAP-55.

### Source transfer

- Normal USB power has priority.
- Loss of valid USB input must transfer the system to battery-backed 5 V operation automatically.
- Backfeed into the USB source/cable is prohibited.
- **No-reset transfer is the target behavior** and remains `[UNVALIDATED]` until tested on the fabricated board.
- Normal-source restoration must be deterministic and must not create reset loops or repeated source oscillation.

### Reverse polarity / serviceability

- The selected cell is unprotected; power-system protection is a system responsibility.
- The existing holder is retained as the mechanical candidate, but it is not mechanically keyed against reverse insertion.
- **Procedure alone is not an acceptable reverse-polarity control.** The final implementation must provide either:
  - electrical reverse-battery blocking/protection; or
  - a mechanically keyed battery interface/enclosure that physically prevents reversed insertion.
- Service procedure and polarity markings are supplementary controls only.
- Actual LG MJ1 holder fit/contact pressure remains an IHAP-55/IHAP-51 validation item after the cells arrive.

## Owned 4056E module disposition

The owned USB-C charger/protection module is **not selected as the final custom-PCB power architecture**. Its recorded C0/C1 evidence remains historical/bench evidence only. Unresolved protection-controller identity and exact RPROG value must not be promoted into assumed final-board characteristics.

## Procurement rule

Until IHAP-55 schematic/BOM review requires exact parts:

- purchase the selected LG MJ1 cells because they remain part of the final architecture;
- do **not** buy TPS61023, TPS2116, additional charger modules or other redundant breakouts solely to emulate functions integrated on the custom PCB;
- existing modules may be used as bench references;
- any new breakout purchase requires a specific validation blocker and Project Owner approval.

## Accepted follow-up ownership supersession

ADR-0007 **does not cancel** quantitative power evidence required by earlier accepted hardware ADRs. It supersedes only their original task-owner assignment from `IHAP-49` to `IHAP-55` for measurements requiring the final custom implementation.

The following obligations remain mandatory and move to IHAP-55:

- ADR-0001: quantitative rail/regulator/current/peak/autonomy validation for the final ESP32-C3 implementation;
- ADR-0002: environmental-profile quantitative current contribution in the integrated node;
- ADR-0003: final reed/pull-network quantitative closed-loop current contribution;
- ADR-0004: display current measurement and resulting sleep/power policy;
- ADR-0005: LD2410C quantitative current/rail contribution and autonomy impact;
- integrated 5 V / 3.3 V rail, current and brownout evidence for the complete custom node.

This is an **ownership transfer, not a waiver**. IHAP-55 cannot declare the custom board validated until these measurements are captured.

## Canonical risk / treatment links

- `docs/risks/records/R-012-unprotected-li-ion-battery-fault.md` — `RT-R012-01`, battery/cell-side protection and NTC/polarity/cutoff evidence;
- `docs/risks/records/R-013-edge-power-rail-transfer-integrity.md` — `RT-R013-01`, regulated rail/backfeed/transfer/load-headroom evidence.

Neither risk is accepted or closed by ADR-0007. Effectiveness remains Pending Evidence until IHAP-55 tests and IHAP-57 updates the records.

## Handoff / closure boundary

IHAP-49 remains the completed architecture-decision task. IHAP-55 owns schematic/layout/fabrication and the mandatory implementation tests; IHAP-51 owns enclosure/serviceability; IHAP-57 tracks treatment effectiveness. Material contradictory evidence must reopen/supersede ADR-0007 rather than silently weaken the accepted contract.
