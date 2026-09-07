# IHAP-49 — Power Risk Assessment

**Status:** architecture-level risks bounded; implementation residuals delegated to IHAP-55 / IHAP-51

| Risk | Severity | Architectural control / decision | Residual owner / state |
|---|---|---|---|
| Normal 5 V source loss | High | LG MJ1 backup retained; automatic transfer required | IHAP-55 transfer test `[UNVALIDATED]` |
| Backfeed into USB source/cable | High | Separated input/SYS power-path required; backfeed prohibited | IHAP-55 schematic + V6/V7 |
| Battery over-charge | High | 4.2 V CV integrated charger; ~1 A charge target; NTC mandatory | IHAP-55 V4 `[UNVALIDATED]` |
| Battery over-discharge | High | System-level cutoff/recovery required; no intentional operation below cell boundary | IHAP-55 V8 `[UNVALIDATED]` |
| Battery over-current / SYS short | High | Integrated PMIC current limiting / SCP required | IHAP-55 schematic + safe bench validation |
| Reverse cell insertion | High | Risk explicit; holder unkeyed; electrical and/or mechanical prevention mandatory | IHAP-55 / IHAP-51 `[UNVALIDATED]` |
| Wi-Fi / load transient brownout | High | >=0.5 A continuous and >=1.0 A transient SYS design envelope; reset logging required | IHAP-55 V5/V6 |
| USB-C incompatibility | High | Correct Type-C sink CC termination required; final board must support C-to-C 5 V | IHAP-55 V2 |
| Excess battery / PMIC temperature | High | Switch-mode architecture + NTC + conservative ~1 A charge target | IHAP-55 V4 thermal evidence |
| Holder fit / contact stress | Medium | Existing holder retained provisionally; no new purchase | IHAP-55/IHAP-51 physical fit `[UNVALIDATED]` |
| Unsupported autonomy expectation | Medium | Battery role backup-only; arithmetic kept separate from measured runtime | IHAP-55 V9 `[UNVALIDATED]` |
| Cost creep from stacked breakouts | Medium | Custom PCB selected; redundant TPS61023/TPS2116/charger purchases rejected | Controlled; IHAP-55 BOM review |
| Custom PCB implementation failure | High | First revision must use staged bring-up, ERC/DRC/DFM and test points | IHAP-55 |
| Event corruption/duplication after reset | Medium | No-reset transfer is reference target; any reset behavior must be visible to runtime validation | IHAP-55 + downstream runtime evidence |
| Sensor-placement regression from PCB integration | Medium | LD2410C, OLED, ENV sensor and MC-38 remain modular/off-board as required | IHAP-55/IHAP-51 |

## Owned 4056E module risk disposition

The owned `4056E + 8205A` module remains useful evidence but is **not the final reference architecture**. Its unresolved protection-controller identity, exact RPROG and lack of demonstrated USB-C-to-USB-C operation therefore no longer block IHAP-49 acceptance; they are reasons not to use that board as the final integrated reference.

## Safety language boundary

The selected architecture is a prototype/MVP engineering decision. None of the controls above authorizes claims such as `safe`, `certified`, `fire-safe`, `compliant`, `production-ready`, `commercial-ready` or equivalent. Physical board evidence remains required in IHAP-55.
