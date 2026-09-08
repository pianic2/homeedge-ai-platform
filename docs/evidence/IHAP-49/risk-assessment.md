# IHAP-49 — Power Risk Assessment Summary

**Status:** architecture-level summary only; canonical living treatment dossiers are R-012 and R-013

This file is a compact IHAP-49 evidence summary. It is **not** the canonical treatment dossier. Canonical Risk Records:

- [R-012 — Unprotected 1S Li-ion Battery Fault and Cell-Side Protection](../../risks/records/R-012-unprotected-li-ion-battery-fault.md), treatment `RT-R012-01`;
- [R-013 — Edge Power Rail and Source-Transfer Integrity](../../risks/records/R-013-edge-power-rail-transfer-integrity.md), treatment `RT-R013-01`.

Both treatments are **Proposed**, not Approved/Implemented/Verified. Residual-risk decision remains Pending Project Owner.

## Accepted baseline versus Proposed remediation

ADR-0007 / PR #34 was accepted on 2026-09-07. The accepted baseline already partially mitigates R-012/R-013 through backup-only use, system-responsibility protection, reverse-insertion prevention, regulated product SYS, post-regulation/equivalent, USB priority, anti-backfeed, headroom and source-transfer targets.

IHAP-56 later introduced tighter controls/tests. The rows below mark those additions **Proposed** so they are not mistaken for retroactively accepted requirements.

| Exposure | Severity | Canonical risk | Control / requirement | Validation evidence / approval state |
|---|---|---|---|---|
| Normal 5 V source loss | High | R-013 | Accepted automatic USB-priority transfer; **Proposed** high/mid/low strengthening | Accepted V8/V9 baseline; strengthened V8/V9 `[UNVALIDATED]` / Proposed |
| Backfeed into USB source/cable | High | R-013 | Accepted: backfeed prohibited | V8/V9 `[UNVALIDATED]` |
| USB source overload while charging + running | High | R-013 | Accepted source-profile/system-priority intent; **Proposed** worst-case ILIM <=1.50 A + V14 | V14 `[UNVALIDATED]` / Proposed |
| Battery over-charge | High | R-012 | Accepted 4.2 V CV / ~1 A target; **Proposed** 4.20 ±0.05 V numeric PASS envelope | V4 `[UNVALIDATED]`; numeric strengthening Proposed |
| NTC hot/cold/open/short | High | R-012 | Accepted NTC monitoring; **Proposed** mandatory fail-bounded fault-state verification | strengthened V4 `[UNVALIDATED]` / Proposed |
| Battery over-discharge / restart oscillation | High | R-012 | Accepted do-not-operate-below-cell-boundary intent; **Proposed** 2.70/3.00 V numeric policy | strengthened V10 `[UNVALIDATED]` / Proposed |
| BAT-side short / over-current | High | R-012 | **Proposed** cell-side interruption upstream of PMIC-output limiting | V13 installed-path test `[UNVALIDATED]` / Proposed |
| Reverse cell insertion | High | R-012 | Accepted electrical block/protection or physical keying; **Proposed** V15 electrical functional criteria | V1+V3 accepted; V15 `[UNVALIDATED]` / Proposed |
| Wi-Fi / load transient brownout or release overshoot | High | R-013 | Accepted >=1 A headroom; **Proposed** bidirectional <=100 µs strengthening | accepted V7 baseline; strengthened V7 `[UNVALIDATED]` / Proposed |
| USB-C incompatibility | High | R-013 | Accepted Type-C sink/C-to-C 5 V contract | V2 `[UNVALIDATED]` |
| Thermal overstress | High | R-012 + R-013 | Accepted physical thermal validation intent; **Proposed** manufacturer-derived numeric table/limits | strengthened thermal evidence `[UNVALIDATED]` / Proposed |
| Product 5 V not regulated in USB mode | High | R-013 | Accepted MP2636 pass-through caveat + post-regulation | V2+V5+V6 `[UNVALIDATED]` |
| Holder fit / contact stress | Medium | R-012 | Physical fit/retention bounded | V3 `[UNVALIDATED]` |
| Unsupported autonomy expectation | Medium | R-013 | Accepted backup-only role; runtime requires endurance evidence | V12 `[UNVALIDATED]` |
| Cost creep from stacked breakouts | Medium | decision/cost governance | Accepted custom PCB direction; redundant breakout purchases rejected | IHAP-55 final BOM `[UNVALIDATED]` |
| Event corruption/duplication after reset | Medium | R-013 + downstream runtime | Accepted no-reset target; **Proposed** V9 zero restoration-reset effectiveness criterion | accepted logging + strengthened V9 Proposed |
| Sensor-placement regression | Medium | R-011 where applicable | Accepted placement-sensitive sensors remain modular/off-board | IHAP-55/IHAP-51 `[UNVALIDATED]` |

## Proposed thermal boundary

IHAP-56 proposes explicit manufacturer-derived PASS/FAIL use of:

- LG MJ1 charging **0–45 °C**;
- LG MJ1 discharge **-20–60 °C**;
- MP2636 recommended operating junction **<=125 °C**; thermal shutdown around 150 °C would fail a treatment validation run;
- exact numeric limits for final post-regulator, 3.3 V regulator, inductor and protection element before thermal treatment evidence passes.

These are source-supported engineering limits but their promotion into the IHAP-56 treatment acceptance contract remains **Proposed** pending Project Owner approval.

## Proposed cell-side / reverse strengthening

The selected MJ1 is unprotected. RT-R012-01 proposes cell-side over-current interruption because PMIC SYS/boost limiting cannot cover every upstream holder/BAT fault. Proposed V13 must test the installed fabricated path (or a production-identical assembled PCB path), not merely a loose sacrificial protection device. Proposed V15 bounds electrical reverse-blocking verification with a current-limited simulator. The actual cell is never intentionally reverse-connected or hard-shorted.

## Traceability rule

- R-012 and R-013 are canonical for treatment rationale/lifecycle/effectiveness.
- Both canonical Category fields use the defined value **Technical**; compliance/claim or data-integrity effects are consequences, not invented category names.
- ADR-0007 inverse links declare the allowed effect **Partially mitigates** for the accepted baseline.
- ADR-0007 acceptance does not approve later RT-R012-01/RT-R013-01 details.
- IHAP-55 implements the applicable scope only after the decision boundary is resolved; IHAP-57 coordinates lifecycle/effectiveness after approval and evidence.
- This summary must not mark a risk/treatment `Approved`, `Implemented`, `Verified`, `Accepted` or `Closed` without the required evidence/decision.

## Claim boundary

None of the controls authorizes `safe`, `certified`, `fire-safe`, `compliant`, `production-ready` or equivalent claims. Physical evidence remains `[UNVALIDATED]` where indicated.
