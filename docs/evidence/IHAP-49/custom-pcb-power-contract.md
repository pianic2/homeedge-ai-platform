# IHAP-49 — Custom PCB Power Contract

**Status:** Accepted PR #34 architecture contract + **Proposed IHAP-56 amendment overlay** pending explicit Project Owner approval  
**Implementation owner:** IHAP-55 — Integrated Modular Edge PCB — Custom Mainboard Design and Prototype

## Approval boundary

The Project Owner approved ADR-0007 / PR #34 on 2026-09-07. That accepted baseline remains authoritative. IHAP-56 later added R-012/R-013 treatment detail and tighter validation criteria. Those later additions remain **Proposed** until explicitly approved and must not be represented as retroactively accepted merely because they are documented in this contract.

## Accepted product-level decision

- Normal node power: **regulated 5 V via USB-C**.
- Backup: **one rechargeable 1S Li-ion 18650** used only for blackout / cable-input interruption.
- Selected reference cell: **LG INR18650-MJ1**, EAN/GTIN `8438493099829`, flat-top unprotected 18650, 3.6 V nominal, 3.5 Ah class.
- Multi-day battery-only operation is not an MVP requirement.
- Planning backup runtime remains approximately **12–20 h**, central estimate ~16 h, and is `[UNVALIDATED]` until measured.
- Cost is the first differentiator after minimum compatibility, provenance and evidence gates are met.
- Final reference direction: one custom core PCB rather than permanent stacked power breakouts.

## Accepted final-board topology

The accepted **5.0 V regulated product bus** must not depend on MP2636 input pass-through being exactly 5.0 V. MPS documents IN-to-SYS pass-through with valid input, so the accepted first direction is MP2636 plus a downstream 5 V regulation stage or a reviewed equivalent topology.

```text
USB-C 5 V input
      |
      v
Type-C sink termination + input protection
      |
      v
MP2636-class 1S charger + system power path + battery boost
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
      |
      v
regulated 5.0 V product SYS bus
      |
      +----> LD2410C
      |
      +----> 3.3 V regulator --> ESP32-C3 + OLED / ENV / reed interface domain
```

Accepted baseline reverse-polarity control requires either electrical blocking/protection or a mechanically keyed interface/enclosure that physically prevents reverse insertion; procedure/labels alone are insufficient.

## Accepted electrical contract

### USB-C input

- 5 V only; USB Power Delivery is not required.
- Correct Type-C sink CC termination is mandatory.
- USB-C-to-USB-C 5 V operation is required.
- Reference source profile: **5 V with at least 1.5 A available/advertised**.
- Input-current limiting must prioritize system load and prevent deliberate overdraw of the reference profile.

### Charging / battery-temperature baseline

- Cell CV target: **4.2 V**.
- Reference charge-current target: **~1.0 A nominal**.
- System load has priority over battery charging when input power is constrained.
- Charging while the node operates is permitted only on the integrated power-path implementation; it remains prohibited for the stand-alone owned 4056E path.
- Battery NTC monitoring or a reviewed equivalent is mandatory.

### 5 V product SYS and headroom

- Nominal target: **5.0 V regulated**.
- Steady-state validation band: **4.75–5.25 V**, unless a downstream component requires tighter limits.
- Minimum design capability: **>=0.5 A continuous**.
- Transient/headroom target: **>=1.0 A** without reset or uncontrolled rail collapse.

### 3.3 V domain

- Provide a regulated 3.3 V rail compatible with the accepted ESP32-C3 compute profile and 3.3 V peripherals.
- Do not silently inherit the unknown regulator capability of the development board.

### Source transfer

- USB-C is the priority source.
- Loss of valid USB must transfer automatically to battery-backed regulated 5 V.
- Backfeed into upstream USB is prohibited.
- No-reset transfer is the accepted target and remains `[UNVALIDATED]`.
- Restoration must be deterministic without reset loops/source oscillation.

### Low-voltage / serviceability baseline

- Do not intentionally operate the cell below the accepted manufacturer discharge boundary.
- A graceful higher low-battery shutdown threshold is preferred where practical.
- Existing holder remains a mechanical candidate and actual fit/contact pressure remains downstream evidence.
- Procedure alone is not an acceptable reverse-polarity control.

## Proposed IHAP-56 treatment / validation overlay — NOT YET ACCEPTED

The following additions are **Proposed** until explicit Project Owner approval:

### Proposed cell-side protection

- add a cell-side over-current interruption element covering holder/BAT-net faults upstream of PMIC SYS/boost limiting;
- size threshold/time from legitimate current envelope and conductor/trace ampacity;
- verify with V13 through the **installed fabricated battery-service path**, not merely a loose protection sample;
- use bounded current-limited fixtures; never intentionally hard-short the actual Li-ion cell.

### Proposed NTC / thermal strengthening

- make normal/hot/cold/open/short NTC functional verification mandatory;
- use manufacturer-derived numeric thermal limits as PASS/FAIL criteria;
- proposed model limits include MJ1 charge **0–45 °C**, discharge **-20–60 °C**, and MP2636 recommended Tj **<=125 °C** during accepted operation;
- register exact post-regulator/3.3 V regulator/inductor/protection limits before thermal treatment evidence can pass.

### Proposed source-current-limit / dynamic strengthening

- configure worst-case ILIM including tolerance to **<=1.50 A** and verify combined node+charging priority with V14;
- strengthen V7 to both baseline->1 A and 1 A->baseline with measured **<=100 µs** 10–90% current edges unless final measured load behavior requires faster;
- retain the accepted rail/reset/recovery limits on both edges.

### Proposed transfer / restoration strengthening

- execute V8/V9 at high **4.10±0.10 V**, mid **3.60±0.10 V**, low **2.80±0.05 V** battery conditions;
- for proposed no-reset effectiveness verification, **any restoration-attributable ESP32 reset/brownout is FAIL**, even if no reset loop occurs.

### Proposed low-voltage numeric policy

- cutoff **2.70 V ±0.05 V**;
- no deliberate sustained operation below **2.50 V**;
- restart at **>=3.00 V ±0.05 V** or valid USB;
- no cutoff/restart oscillation.

### Proposed electrical reverse-blocking verification

If electrical blocking is relied upon, V15 uses a 4.20 V / 10 mA current-limited simulator through the normal service interface and proposes <=1 mA steady reversed-source current, product rails <=0.3 V, no damage/heating and normal recovery. The actual Li-ion cell is never intentionally reverse-connected.

### Proposed ADR-0003 ownership correction

The accepted PR #34 ownership transfer covers ADR-0001, ADR-0002, ADR-0004 and ADR-0005. IHAP-56 proposes extending quantitative ownership to **ADR-0003 / reed pull-network current**. That extension is not accepted until explicitly approved or assigned by another accepted decision.

## Owned 4056E module disposition

The owned USB-C charger/protection module is **not selected as the final custom-PCB power architecture**. Its C0/C1 evidence remains historical/bench evidence only. Unresolved controller identity/RPROG must not become assumed final-board characteristics.

## Procurement rule

Until IHAP-55 schematic/BOM review requires exact parts:

- retain the selected LG MJ1 cell direction;
- do **not** buy TPS61023, TPS2116, additional charger modules or redundant breakouts solely to emulate integrated functions;
- existing modules may be used as bench references;
- any new breakout purchase requires a specific blocker and Project Owner approval.

## Canonical risk / treatment links

- `docs/risks/records/R-012-unprotected-li-ion-battery-fault.md` — `RT-R012-01` **Proposed**;
- `docs/risks/records/R-013-edge-power-rail-transfer-integrity.md` — `RT-R013-01` **Proposed**.

ADR-0007 acceptance partially mitigates both risks at the accepted architecture-baseline level; it does not approve later treatment details, verify effectiveness or accept residual risk.

## Handoff / closure boundary

`validation-plan.md` separates the accepted physical-test baseline from the Proposed IHAP-56 additions. `downstream-contracts.md` separates accepted IHAP-55 obligations from proposed treatment gates. IHAP-49 remains completed on the accepted PR #34 decision. IHAP-55 must not consume Proposed additions as mandatory until explicit approval exists, and remains blocked by IHAP-56 while that remediation gate is open.
