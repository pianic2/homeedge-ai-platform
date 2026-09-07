# IHAP-49 — Custom PCB Power Contract

**Status:** Proposed architecture contract for Project Owner review  
**Implementation owner:** IHAP-55 — Integrated Modular Edge PCB — Custom Mainboard Design and Prototype

## Purpose

Freeze the electrical and product requirements that IHAP-49 owns without forcing the reference MVP to permanently use stacked breakout modules.

The final reference direction is a **single custom core PCB**. IHAP-49 defines the power contract; IHAP-55 implements, lays out, fabricates and physically validates that contract.

## Frozen product-level decision

- Normal node power: **regulated 5 V via USB-C**.
- Backup: **one rechargeable 1S Li-ion 18650** used only for blackout / cable-input interruption.
- Selected reference cell: **LG INR18650-MJ1**, EAN/GTIN `8438493099829`, flat-top unprotected 18650, 3.6 V nominal, 3.5 Ah class.
- Multi-day battery-only operation is not an MVP requirement.
- Planning backup runtime remains approximately **12–20 h**, central estimate ~16 h, and is `[UNVALIDATED]` until measured on the fabricated implementation.
- Cost is the first differentiator after minimum compatibility, provenance and evidence gates are met.

## Final-board topology requirement

```text
USB-C 5 V input
      |
      v
input protection / Type-C sink termination
      |
      v
integrated 1S charger + system power path + battery-to-SYS boost
      |                         |
      |                         +----> LG INR18650-MJ1 via serviceable holder
      |
      v
regulated 5 V SYS bus
      |
      +----> LD2410C external module
      |
      +----> 3.3 V regulator --> ESP32-C3 core + OLED / ENV / reed interface domain
```

The final design must not require separate TP4056/4056E, boost and power-mux breakout boards.

## Reference integrated PMIC direction

**Preferred implementation candidate for IHAP-55:** `MP2636GR-P` (Monolithic Power Systems).

The selection is based on one IC providing the coupled functions that the breakout stack otherwise needs:

- 1S Li-ion / Li-polymer switch-mode charging;
- system power-path management with system-load priority;
- programmable input-current limit and input-voltage regulation;
- selectable 4.2 V battery charge voltage;
- programmable charge current;
- NTC battery-temperature input;
- reverse boost from the battery to a programmable SYS voltage;
- programmable boost output-current limit;
- pass-through over-current / over-voltage controls;
- boost short-circuit and over-voltage controls;
- battery-current monitor output;
- active/currently orderable manufacturer part.

The MP2636 datasheet permits SYS in boost mode to be programmed from 4.2 V to 6 V; **5.0 V is the reference target**.

This is an **architecture/component selection**, not a claim that the future PCB is already electrically validated. Schematic values, layout, thermal behavior, switchover logic and fabricated-board behavior remain IHAP-55 evidence.

## Cost-down alternative retained

`ETA9740` remains a **future cost-down candidate**, not the reference choice for the first custom-board revision.

It is materially cheaper and integrates bidirectional charging/boost with automatic mode switching, but the current evidence provides weaker control/monitoring for this project's battery-temperature and separated input/SYS requirements. The reference first revision therefore prioritizes a cleaner system-power-path boundary and NTC support over the lowest PMIC sticker price.

A later board revision may supersede MP2636 after equal validation evidence demonstrates lower total BOM cost without regressing the power contract.

## Electrical contract

### USB-C input

- 5 V only; USB Power Delivery is **not required** for MVP.
- Type-C sink implementation must include correct CC termination (`Rd`, normally 5.1 kΩ on CC1 and CC2 unless the chosen USB-C front end requires otherwise).
- The final board must work from USB-C-to-USB-C 5 V sources that advertise sufficient source current; it must not rely on the legacy USB-A-to-USB-C behavior observed on the owned 4056E module.
- Reference source profile: **5 V, at least 1.5 A available/advertised**.
- Input-current limit must be configured so the node + charging load cannot intentionally exceed the reference input profile.

### Charging

- Cell CV target: **4.2 V**.
- Reference charge-current target: **~1.0 A nominal**, subject to final resistor calculation and physical validation in IHAP-55.
- 1.0 A is intentionally below the selected MJ1 standard-charge envelope and leaves input-power/thermal margin for the always-on node load.
- The system-load path has priority over battery charging when input power is constrained.
- **Charging while the node operates is permitted only on the integrated power-path implementation.** It remains prohibited for the owned 4056E breakout when used as a stand-alone charger path.
- Battery NTC monitoring is mandatory on the custom-board implementation unless a later reviewed design provides an equivalent or stronger bounded control.

### 5 V SYS bus

- Nominal target: **5.0 V regulated**.
- Must power LD2410C and the downstream 3.3 V regulator.
- Minimum design capability: **>=0.5 A continuous** at the 5 V SYS bus across the accepted battery operating range.
- Transient/headroom target: **>=1.0 A** without reset or uncontrolled rail collapse.
- Current capability is a design envelope, not an assertion that the node continuously draws this current.

### 3.3 V domain

- The custom PCB must provide a regulated 3.3 V rail compatible with the accepted ESP32-C3 compute profile and 3.3 V peripherals.
- The rail design must cover the Espressif chip supply-current requirement plus OLED/environmental/reed-interface margin; the exact regulator and final current rating belong to IHAP-55 schematic/BOM review.
- The final design must not silently reuse the unknown regulator capability of the current SuperMini-compatible development board.

### Battery low-voltage behavior

- The design must not intentionally operate the MJ1 below its accepted cell minimum-discharge boundary.
- A graceful low-battery warning/shutdown threshold above the hard protection boundary is preferred and should be implemented if it does not materially increase cost/complexity.
- Exact cutoff and recovery values are implementation/test evidence in IHAP-55.

### Source transfer

- Normal USB power has priority.
- Loss of valid USB input must transfer the system to battery-backed 5 V operation automatically.
- Prohibited backfeed into the USB source/cable is not allowed.
- **No-reset transfer is the target behavior** for the reference node and must be physically validated on the fabricated board; until then it remains `[UNVALIDATED]`.
- Normal-source restoration must be deterministic and must not create reset loops or repeated source oscillation.

### Reverse polarity / serviceability

- The selected cell is unprotected; power-system protection is therefore mandatory.
- The existing holder is retained as the mechanical candidate and costs no new procurement, but it is not mechanically keyed against reverse insertion.
- The final implementation must mitigate reversed-cell insertion electrically and/or make reverse insertion inaccessible through the enclosure/service procedure.
- Actual LG MJ1 holder fit/contact pressure remains an IHAP-55/IHAP-51 physical validation item after the cells arrive.

## Owned 4056E module disposition

The owned USB-C charger/protection module is **not selected as the final custom-PCB power architecture**.

Existing evidence remains useful as a prototype/control record:

- charger IC visibly marked `4056E`;
- `8205A` dual MOSFET observed;
- separate protection-controller device observed but exact identity/thresholds not verified;
- legacy USB-A-to-USB-C 5 V input sanity passed at VIN 4.95 V;
- unloaded B/OUT were approximately 4.19/4.18 V;
- tested USB-C-to-USB-C fast-charge source did not provide usable input to this module;
- in-circuit R3 measurement was polarity-dependent and therefore inconclusive.

Because this module is not the final reference implementation, unresolved protection-controller identity and exact RPROG value are **not blockers for accepting the IHAP-49 architecture decision**. They remain documented limitations of owned inventory.

## Procurement rule

Until IHAP-55 schematic/BOM review requires exact parts:

- purchase the selected LG MJ1 cells because they remain part of the final architecture;
- do **not** buy TPS61023, TPS2116, additional charger modules or other redundant breakouts solely to emulate functions that will be integrated on the custom PCB;
- existing modules may be used as bench references;
- any new breakout purchase requires a specific validation blocker and Project Owner approval.

## Handoff / closure boundary

IHAP-49 is complete when the Project Owner accepts this power contract and ADR-0007.

The following are intentionally **not IHAP-49 closure blockers** and move to IHAP-55 / IHAP-51 as implementation evidence:

- schematic component values and PCB layout;
- exact NTC, inductor, sense resistor and regulator SKU selection;
- fabricated-board rail measurements;
- charge-current and thermal validation on the integrated PMIC;
- automatic USB-to-battery transfer validation;
- measured backup runtime;
- final holder fit and enclosure serviceability;
- final assembled-board replication cost.

Those results may refine or supersede ADR-0007 if physical evidence proves the selected implementation cannot satisfy this contract.
