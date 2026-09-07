# IHAP-49 — Power Risk Assessment Summary

**Status:** architecture-level summary only; canonical living treatment dossiers are R-012 and R-013

This file is a compact IHAP-49 evidence summary. It is **not** the canonical treatment dossier. The canonical Risk Records are:

- [R-012 — Unprotected 1S Li-ion Battery Fault and Cell-Side Protection](../../risks/records/R-012-unprotected-li-ion-battery-fault.md), treatment `RT-R012-01`;
- [R-013 — Edge Power Rail and Source-Transfer Integrity](../../risks/records/R-013-edge-power-rail-transfer-integrity.md), treatment `RT-R013-01`.

Both treatments are approved at architecture level but remain **not Implemented / not Verified** until IHAP-55 physical evidence exists. Residual-risk decision remains Pending Project Owner.

| Exposure | Severity | Canonical risk | Accepted control / requirement | Primary validation evidence / state |
|---|---|---|---|---|
| Normal 5 V source loss | High | R-013 | LG MJ1 backup retained; automatic USB-priority transfer required | **V8 + V9** `[UNVALIDATED]` |
| Backfeed into USB source/cable | High | R-013 | Backfeed prohibited; source path must isolate upstream USB | **V8 + V9** `[UNVALIDATED]` |
| Battery over-charge | High | R-012 | 4.2 V CV; ~1 A nominal charge target; system-load priority | **V4** `[UNVALIDATED]` |
| NTC hot/cold or sensor open/short | High | R-012 | Battery-temperature monitoring mandatory; fault behavior must fail bounded | **V4 mandatory NTC simulation** `[UNVALIDATED]` |
| Battery over-discharge | High | R-012 | System-level cutoff/recovery required; no intentional operation below accepted cell boundary | **V10** `[UNVALIDATED]` |
| BAT-side short / battery over-current | High | R-012 | **Cell-side over-current interruption mandatory** upstream of PMIC-output protection coverage | schematic/BOM + **V13** `[UNVALIDATED]` |
| Reverse cell insertion | High | R-012 | Electrical reverse blocking/protection or physical keying required; procedure alone prohibited | **V1 + V3** implementation check `[UNVALIDATED]` |
| Wi-Fi / load transient brownout | High | R-013 | >=0.5 A continuous and >=1.0 A transient/headroom product-SYS envelope | **V7 mandatory load-step** `[UNVALIDATED]` |
| USB-C incompatibility | High | R-013 | Correct Type-C sink CC termination; C-to-C 5 V support required | **V2** `[UNVALIDATED]` |
| Excess battery / PMIC / regulator temperature | High | R-012 + R-013 | switch-mode power path, NTC gating, bounded charge target, continuous-load thermal observation | **V4 + V6** `[UNVALIDATED]` |
| Product 5 V not regulated in USB mode | High | R-013 | MP2636 pass-through treated as intermediate only; downstream 5 V regulation or reviewed equivalent required | **V2 + V5 + V6** `[UNVALIDATED]` |
| Holder fit / contact stress | Medium | R-012 | Existing holder retained provisionally; physical fit/retention bounded | **V3** `[UNVALIDATED]` |
| Unsupported autonomy expectation | Medium | R-013 | Battery role backup-only; arithmetic separated from measured runtime | **V12** `[UNVALIDATED]` |
| Cost creep from stacked breakouts | Medium | decision/cost governance | Custom PCB selected; redundant TPS61023/TPS2116/charger breakout purchases rejected | IHAP-55 final BOM `[UNVALIDATED]` |
| Custom PCB implementation failure | High | R-012 + R-013 | staged bring-up, ERC/DRC/DFM, test points and mandatory validation sequence | IHAP-55 implementation evidence `[UNVALIDATED]` |
| Event corruption/duplication after reset | Medium | R-013 + downstream runtime scope | no-reset transfer is target; any reset must be explicitly logged and handed to runtime validation | **V7 + V8 + V9** plus downstream runtime evidence |
| Sensor-placement regression from PCB integration | Medium | R-011 where environmental placement is affected | placement-sensitive sensors remain modular/off-board and enclosure work remains IHAP-51 | IHAP-55/IHAP-51 `[UNVALIDATED]` |

## Cell-side protection clarification

The selected LG MJ1 is **unprotected**. MP2636 boost/SYS current limiting or SYS short-circuit protection cannot be used as the sole control for a short on holder leads or the BAT net **upstream** of that output protection.

Therefore the final board must contain a suitably located cell-side interruption element — fuse, electronic protection switch or reviewed equivalent — whose threshold/time is justified against legitimate charge/discharge/transient current and conductor/trace ampacity. Verification is mandatory under V13. The actual Li-ion cell must not be intentionally hard-shorted merely to prove this control.

## Owned 4056E module risk disposition

The owned `4056E + 8205A` module remains useful evidence but is **not the final reference architecture**. Its unresolved protection-controller identity, exact RPROG and lack of demonstrated USB-C-to-USB-C operation therefore do not define the final product protection contract; they are reasons not to reuse that module as the reference implementation.

## Traceability rule

- R-012 and R-013 are canonical for treatment rationale, lifecycle, evidence and effectiveness review.
- ADR-0007 contains the inverse risk/treatment links and declares its effect/remaining exposure.
- IHAP-55 implements and verifies the controls.
- IHAP-57 coordinates later Risk Record effectiveness updates.
- This summary must not be used to mark a risk `Verified`, `Accepted` or `Closed`.

## Safety language boundary

The selected architecture is an MVP engineering decision. None of the controls above authorizes claims such as `safe`, `certified`, `fire-safe`, `compliant`, `production-ready`, `commercial-ready` or equivalent. Physical evidence remains `[UNVALIDATED]` where indicated.
