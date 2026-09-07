# IHAP-49 — Project Owner Decision Record

**Initial power-source decision:** 2026-09-05  
**Cell-selection update:** 2026-09-07  
**Custom-PCB / procurement update:** 2026-09-07

## 1. Power role decision

The reference MVP edge node will use **regulated 5 V via USB-C as the normal operating supply**.

A rechargeable 1S Li-ion battery remains part of the MVP only as **backup power** for:

- mains/input blackout affecting the USB-C source;
- cable disconnection or cable/input fault;
- continuity of the node when the normal 5 V source is unavailable.

The battery is not the primary continuous energy source and is not selected to provide multi-day standalone operation.

## 2. Cell decision

The Project Owner selected **LG INR18650-MJ1** as the reference cell model for procurement and downstream physical validation.

Selected identity / order basis:

- model: `INR18650-MJ1`;
- EAN / GTIN: `8438493099829`;
- format: 18650 flat-top, unprotected Li-ion;
- nominal voltage: 3.6 V;
- 3.5 Ah class;
- seller: NKON;
- planned quantity: 10 cells;
- product subtotal: EUR 19.90;
- planned shipping: EUR 6.33;
- planned landed total: **EUR 26.23**;
- planned landed average: **EUR 2.623/cell**.

Cost policy is explicit: **cost is the first differentiator after minimum compatibility, provenance and evidence thresholds are met**.

The existing 18650 holder remains the mechanical reference candidate. No replacement holder purchase is authorized at this stage. Actual MJ1 fit/contact pressure remains `[UNVALIDATED]` until the cells arrive and is handed to IHAP-55/IHAP-51 physical validation.

## 3. Custom-board decision

The Project Owner explicitly set the final hardware objective as a **small, efficient, easily installable, modular and scalable custom PCB**, rather than a permanent stack of development boards and breakout modules.

Consequences:

1. IHAP-49 freezes the power architecture and electrical contract.
2. A dedicated custom-board implementation task, **IHAP-55 — Integrated Modular Edge PCB — Custom Mainboard Design and Prototype**, implements and validates the final PCB.
3. Do **not** buy TPS61023, TPS2116 or additional charger/power breakouts solely to emulate functions that the final PCB will integrate.
4. Existing 4056E modules and holder remain useful as bench/control evidence.
5. Battery cells are not redundant procurement because the selected 18650 remains part of the final architecture.

## 4. Integrated PMIC direction

For the first custom-board revision, the Proposed reference implementation direction is **Monolithic Power Systems MP2636GR-P**.

It is preferred because it integrates the coupled functions required by the final power contract:

- 1S switch-mode charging;
- system power-path management;
- system-load priority;
- input-current limiting/input-voltage regulation;
- selectable 4.2 V charge voltage;
- programmable charge current;
- NTC battery-temperature monitoring;
- reverse battery-to-SYS boost with programmable output;
- programmable boost current limit;
- pass-through and boost protection features.

`ETA9740` remains a future cost-down candidate, not the first-reference choice.

## 5. Electrical contract decisions

- USB-C normal input: **5 V**, no PD requirement for MVP.
- USB-C-to-USB-C support is required on the final PCB through correct Type-C sink termination.
- Reference source profile: **5 V / at least 1.5 A available or advertised**.
- Battery CV target: **4.2 V**.
- Nominal charge-current target: **~1.0 A**, exact schematic value owned by IHAP-55.
- Charging while the node operates is permitted only on the integrated power-path implementation and must be validated downstream.
- 5 V SYS target: **5.0 V regulated**, >=0.5 A continuous design capability and >=1.0 A transient/headroom target.
- USB has priority over battery.
- Automatic transfer to backup is required; no-reset transfer is the target and remains `[UNVALIDATED]` until the custom board is tested.
- Backfeed into the USB source is prohibited.
- The unprotected MJ1 requires system-level protection.
- Battery NTC monitoring is mandatory unless an explicitly reviewed equivalent control supersedes it.

## 6. Owned 4056E disposition

The owned charger/protection module is **not the final reference implementation**.

Recorded evidence remains useful:

- `4056E` charger marking observed;
- `8205A` dual MOSFET observed;
- separate protection-controller IC observed, exact identity/thresholds `[UNVALIDATED]`;
- legacy USB-A-to-USB-C 5 V input sanity passed at VIN 4.95 V;
- unloaded `B+/B-` / `OUT+/OUT-` approximately 4.19 / 4.18 V;
- tested USB-C-to-USB-C fast-charge source did not provide usable input to the module;
- in-circuit R3 measurement was inconclusive.

Because this module is rejected as the final implementation, its unresolved exact protection-controller identity and RPROG value are not blockers to the architecture decision.

## 7. Validation boundary

Planning calculations indicate roughly **12–20 h** of backup runtime for a 3.5 Ah-class cell, with ~16 h as the central estimate. This remains `[UNVALIDATED]`.

IHAP-55 owns fabricated-board validation of:

- charging current/termination/temperature;
- 5 V and 3.3 V rail behavior;
- source switchover/restoration;
- brownout/reset behavior;
- low-voltage behavior;
- measured backup runtime;
- final board-level BOM and replication cost.

IHAP-51 owns final holder retention, battery accessibility and enclosure/serviceability constraints.

## Project Owner review gate

This record authorizes completion of the IHAP-49 decision package and downstream handoff. It does **not** by itself authorize ADR acceptance, PR merge or final Jira completion. Those remain gated on explicit Project Owner acceptance of the updated ADR-0007 / PR #34.
