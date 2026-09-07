# IHAP-49 — Power Architecture Alternatives

**Status:** Proposed comparison supporting ADR-0007 review

## Architecture-level alternatives

| Alternative | Disposition | Rationale |
|---|---|---|
| Regulated 5 V USB-C only | Rejected as complete subsystem; retained as normal source | Lowest complexity, but does not satisfy blackout/cable-input backup requirement. |
| Rechargeable 1S battery as primary source | Rejected | Current load model makes one 18650 an hours-scale source; multi-day standalone operation is not an MVP requirement. |
| Normal 5 V USB-C + rechargeable 1S backup | **Selected architecture** | Matches the actual continuity requirement while preserving one 5 V product domain. |
| Protected 18650 | Rejected for reference direction | Adds cost and mechanical length while duplicating protection intended at system level. |
| LG INR18650-MJ1 unprotected | **Selected cell** | Meets the capacity/current envelope with favorable landed cost and identifiable model/provenance. |
| LiPo pouch | Rejected | Does not remove charging/protection/power-path work and adds a different mechanical profile without a current product need. |
| Replaceable primary cells | Rejected | Poor fit for always-on radar/Wi-Fi and repeated-consumable use. |

## Power implementation alternatives

| Implementation | Cost / integration | Technical fit | Disposition |
|---|---|---|---|
| Owned `4056E` charger/protection + separate boost + source mux | Low sunk cost, high wiring/module count | Charger evidence exists, but no complete power path; exact protection controller unknown; tested C-to-C input not supported | **Rejected as final implementation; retained as bench evidence** |
| TPS61023 boost + TPS2116 mux + charger module | Moderate module cost, three-board stack | Technically viable and testable, but duplicates functions that the declared custom PCB should integrate | **Rejected as final reference; do not purchase solely for emulation** |
| MT3608-class boost + discrete ORing/mux | Low sticker price | More trimming, poorer disconnect/backfeed behavior and more discrete failure paths | Rejected |
| **MP2636GR-P integrated charger/PPM/boost** | Higher IC cost, much lower module/interconnect count | Separate VIN/SYS behavior, programmable 4.2 V charging, current limits, NTC, programmable 5 V SYS boost, protection features | **Selected first custom-board implementation direction** |
| ETA9740 integrated bidirectional charger/boost | Very low IC cost | Strong cost-down potential and automatic mode switching, but weaker match to first-revision NTC / separated input-SYS control requirements | **Future cost-down candidate** |

## Why MP2636 wins the first revision

The project is cost-first **after minimum technical/evidence gates**. Cost-first therefore does not mean choosing the cheapest IC when doing so adds board-level controls or weakens the evidence/validation boundary.

MP2636 is preferred for revision 1 because it collapses the charger, power-path manager and battery boost into one controlled PMIC while retaining:

- 4.2 V selectable cell charging;
- programmable ~1 A reference charge current;
- NTC battery-temperature monitoring;
- system-load priority;
- programmable 5 V SYS output in boost mode;
- programmable boost current limit;
- separated USB input and SYS domains;
- protection/monitoring hooks useful during bring-up.

ETA9740 remains explicitly retained for a later cost-down review once the first board establishes measured load, thermal and switchover requirements.

## Procurement consequence

The project should **not buy TPS61023/TPS2116 or additional charger breakouts** merely to reproduce functions that the custom PCB will integrate. The selected LG MJ1 cells remain a valid purchase because the battery itself persists in the final architecture.
