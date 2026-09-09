# IHAP-49 — Custom PCB Power Contract

**Status:** Accepted PR #34 architecture contract + **Proposed IHAP-56 amendment overlay** pending explicit Project Owner approval  
**Implementation owner:** IHAP-55 — Integrated Modular Edge PCB — Custom Mainboard Design and Prototype

## Approval boundary

The Project Owner approved ADR-0007 / PR #34 on 2026-09-07. That accepted baseline remains authoritative. IHAP-56 later added R-012/R-013 treatment detail and tighter validation criteria. Those later additions remain **Proposed** until explicitly approved and must not be represented as retroactively accepted merely because they are documented in this contract.

`ihap-56-closure-matrix.md` is the review router for Accepted-vs-Proposed state. It does not itself approve any Proposed control.

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
- Minimum design capability: **>=0.5 A continuous across the accepted battery range and valid USB-input range**.
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

- add a cell-side over-current interruption element **at the source side of all in-scope holder/service wiring**, so ordinary holder leads and connector conductors intended to be covered are downstream of the interruption element;
- if any conductor necessarily remains upstream of the interruption element, that segment is explicitly **not covered by V13** and must receive a separate reviewed control (mechanical insulation/routing/strain-relief or another source-side protective element) plus verification before RT-R012-01 can be approved/verified as covering holder wiring;
- size threshold/time from legitimate current envelope and conductor/trace ampacity;
- verify with V13 through the installed or production-identical fabricated battery-service path, not merely a loose protection sample;
- use bounded current-limited fixtures; never intentionally hard-short the actual Li-ion cell.

### Proposed NTC / thermal strengthening

- make normal/hot/cold/open/short NTC functional verification mandatory;
- use manufacturer-derived numeric thermal limits as PASS/FAIL criteria;
- proposed model limits include MJ1 charge **0–45 °C**, discharge **-20–60 °C**, and MP2636 recommended Tj **<=125 °C** during treatment validation;
- a package/case/board temperature reading is **not** a direct substitute for junction temperature;
- before a thermal PASS, IHAP-55 must document a manufacturer-supported or conservatively derived junction-temperature method using measured electrical loss/dissipation, datasheet thermal parameters applicable to the final PCB, ambient temperature, layout/copper conditions and measurement/model uncertainty; alternatively it may derive and freeze a conservative case/board-temperature ceiling that guarantees Tj remains within the registered limit;
- if no justified conversion/derating exists, the run cannot satisfy the proposed MP2636 thermal treatment criterion;
- register exact post-regulator/3.3 V regulator/inductor/protection limits before thermal treatment evidence can pass.

### Proposed source-current-limit / dynamic strengthening

- configure worst-case ILIM including tolerance to **<=1.50 A** and verify combined node+charging priority with V14;
- strengthen V7 to both baseline->1 A and 1 A->baseline with measured **<=100 µs** 10–90% current edges unless final measured load behavior requires faster;
- retain the accepted rail/reset/recovery limits on both edges.

### Proposed 3.3 V verification strengthening

- the final populated 3.3 V rail PASS band is the **intersection of the manufacturer supply ranges of every populated 3.3 V load**;
- until exact downstream parts are frozen, the ESP32-C3 **3.0–3.6 V** operating range is the initial outer bound; any tighter peripheral limit supersedes it;
- V2, V5, strengthened V7 and strengthened V8/V9 must measure the 3.3 V rail at the ESP32-C3 supply/test point and keep it inside the frozen component-derived band without reset/brownout attributable to the power event.

### Proposed transfer / restoration strengthening

- execute V8/V9 at high **4.10±0.10 V**, mid **3.60±0.10 V**, and a low condition nominally **2.90±0.05 V**;
- the low condition must also maintain **>=100 mV measured BATT headroom above the maximum permitted cutoff under the pre-transfer load** and the battery path must be enabled before USB removal; if load sag violates that margin, raise the simulator setpoint until the condition is valid and record the actual value;
- for proposed no-reset effectiveness verification, **any restoration-attributable ESP32 reset/brownout is FAIL**, even if no reset loop occurs.

### Proposed quantified backfeed verification

For strengthened V8/V9, test both:

1. upstream USB disconnected/open; and
2. a representative upstream source attached but unpowered, where that source can safely tolerate the test.

Proposed PASS criteria, unless the selected isolation component/source imposes tighter values:

- with the upstream port open, DUT USB VBUS remains **<=0.30 V** after settling while operating from battery;
- with an attached unpowered source, steady current driven from DUT toward the upstream source is **<=1.0 mA** after settling;
- no source oscillation or abnormal heating occurs;
- connector voltage/current, measurement point and settling interval are recorded.

### Proposed low-voltage numeric policy

- cutoff **2.70 V ±0.05 V**;
- no deliberate sustained operation below **2.50 V**;
- restart at **>=3.00 V ±0.05 V** or valid USB;
- no cutoff/restart oscillation.

### Proposed electrical reverse-blocking verification

If electrical blocking is relied upon, V15 has two bounded cases with the real Li-ion cell removed:

- **V15-A — USB absent:** reverse a 4.20 V battery simulator through the normal service interface with a 10 mA source limit; proposed PASS requires <=1 mA steady reverse-source current, product 5 V/3.3 V rails <=0.3 V, no damage/heating and normal recovery after correct polarity;
- **V15-B — USB present:** power the node from the accepted 5 V USB source and connect a **bidirectional/source-sink-capable** simulator reversed at the battery service interface, 4.20 V magnitude with source/sink current bounded to 10 mA. Proposed PASS requires absolute steady battery-port current attributable to the reversed connection **<=1 mA**, the protected internal BAT node to stay inside the frozen charger/PMIC battery-node envelope (maximum **4.25 V** for this proposed test), every reverse-protection device to remain below its frozen voltage/current rating including uncertainty, normal product rails from USB, and no abnormal heating/damage;
- the actual Li-ion cell is never intentionally reverse-connected.

If mechanical keying alone is selected, electrical reverse-drive is N/A and V1/V3 must prove ordinary reversed insertion is physically impossible.

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

`validation-plan.md` separates the accepted physical-test baseline from the Proposed IHAP-56 additions. `downstream-contracts.md` separates accepted IHAP-55 obligations from proposed treatment gates. `ihap-56-closure-matrix.md` is the cross-file regression router. IHAP-49 remains completed on the accepted PR #34 decision. IHAP-55 must not consume Proposed additions as mandatory until explicit approval exists, and remains blocked by IHAP-56 while that remediation gate is open.
