# IHAP-49 — Power Risk Assessment Summary

**Status:** architecture-level summary only; canonical living treatment dossiers are R-012 and R-013

This file is a compact IHAP-49 evidence summary. It is **not** the canonical treatment dossier. Canonical Risk Records:

- [R-012 — Unprotected 1S Li-ion Battery Fault and Cell-Side Protection](../../risks/records/R-012-unprotected-li-ion-battery-fault.md), treatment `RT-R012-01`;
- [R-013 — Edge Power Rail and Source-Transfer Integrity](../../risks/records/R-013-edge-power-rail-transfer-integrity.md), treatment `RT-R013-01`.

Both treatments are **Proposed**, not Approved/Implemented/Verified. Residual-risk decision remains Pending Project Owner.

| Exposure | Severity | Canonical risk | Required control / requirement | Primary validation evidence / state |
|---|---|---|---|---|
| Normal 5 V source loss | High | R-013 | LG MJ1 backup; automatic USB-priority transfer | **V8 + V9 high/mid/low** `[UNVALIDATED]` |
| Backfeed into USB source/cable | High | R-013 | Backfeed prohibited | **V8 + V9** `[UNVALIDATED]` |
| USB source overload while charging + running | High | R-013 | worst-case ILIM <=1.50 A; system-load priority | **V14** `[UNVALIDATED]` |
| Battery over-charge | High | R-012 | 4.20 ±0.05 V maximum-charge envelope; ~1 A nominal target | **V4** `[UNVALIDATED]` |
| NTC hot/cold/open/short | High | R-012 | fail-bounded NTC behavior mandatory | **V4** `[UNVALIDATED]` |
| Battery over-discharge / restart oscillation | High | R-012 | cutoff 2.70 ±0.05 V; no deliberate <2.50 V; recovery >=3.00 ±0.05 V or USB | **V10** `[UNVALIDATED]` |
| BAT-side short / over-current | High | R-012 | cell-side interruption upstream of PMIC-output protection | **V13** `[UNVALIDATED]` |
| Reverse cell insertion | High | R-012 | electrical block/protection or physical keying; procedure prohibited | **V1 + V3 + V15 when electrical blocking is used** `[UNVALIDATED]` |
| Wi-Fi / load transient brownout or release overshoot | High | R-013 | >=1 A headroom; both load edges <=100 µs reference transition | **V7 bidirectional** `[UNVALIDATED]` |
| USB-C incompatibility | High | R-013 | correct Type-C sink CC termination / C-to-C 5 V | **V2** `[UNVALIDATED]` |
| Thermal overstress | High | R-012 + R-013 | MJ1 charge 0–45 °C, discharge -20–60 °C; MP2636 Tj <=125 °C; final component-specific table mandatory | **V4 + V5 + V6 + V7 + V8 + V9** `[UNVALIDATED]` |
| Product 5 V not regulated in USB mode | High | R-013 | MP2636 pass-through intermediate only; post-regulation required | **V2 + V5 + V6** `[UNVALIDATED]` |
| Holder fit / contact stress | Medium | R-012 | physical fit/retention bounded | **V3** `[UNVALIDATED]` |
| Unsupported autonomy expectation | Medium | R-013 | backup-only role; runtime requires endurance evidence | **V12** `[UNVALIDATED]` |
| Cost creep from stacked breakouts | Medium | decision/cost governance | custom PCB selected; redundant breakout purchases rejected | IHAP-55 final BOM `[UNVALIDATED]` |
| Custom PCB implementation failure | High | R-012 + R-013 | staged bring-up/ERC/DRC/DFM/test points and mandatory validation | IHAP-55 evidence `[UNVALIDATED]` |
| Event corruption/duplication after reset | Medium | R-013 + downstream runtime | no-reset target; any reset explicitly recorded | V7/V8/V9 + downstream runtime evidence |
| Sensor-placement regression | Medium | R-011 where applicable | placement-sensitive sensors remain modular/off-board | IHAP-55/IHAP-51 `[UNVALIDATED]` |

## Thermal boundary

Manufacturer-derived values already frozen in `validation-plan.md`:

- LG MJ1 charging: **0–45 °C**;
- LG MJ1 discharge: **-20–60 °C**;
- MP2636 recommended operating junction: **<=125 °C**; thermal shutdown around 150 °C is protective behavior and is FAIL for normal validation.

The final post-regulator, 3.3 V regulator, inductor and protection-element limits must be entered numerically before V4/V6 can pass. Maintaining output voltage while exceeding a registered temperature limit is **not** a PASS.

## Cell-side / reverse boundary

The selected LG MJ1 is unprotected. PMIC SYS/boost limiting is insufficient for upstream holder/BAT faults. V13 verifies the cell-side interruption using a bounded fixture. If electrical reverse blocking is selected, V15 uses a 4.20 V / 10 mA current-limited simulator and requires <=1 mA reversed steady current and product rails <=0.3 V. The actual cell is not reverse-connected or hard-shorted for these tests.

## Traceability rule

- R-012 and R-013 are canonical for treatment rationale/lifecycle/effectiveness.
- ADR-0007 contains inverse risk/treatment links but does not approve the later treatment lifecycle states.
- IHAP-55 implements and verifies after treatment approval; IHAP-57 coordinates lifecycle/effectiveness updates.
- This summary must not mark a risk/treatment `Approved`, `Implemented`, `Verified`, `Accepted` or `Closed` without the required evidence/decision.

## Claim boundary

None of the controls authorizes `safe`, `certified`, `fire-safe`, `compliant`, `production-ready` or equivalent claims. Physical evidence remains `[UNVALIDATED]` where indicated.
