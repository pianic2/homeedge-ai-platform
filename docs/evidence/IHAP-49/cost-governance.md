# IHAP-49 — Cost Governance Notes

**Status:** decision-level cost baseline frozen; final assembled-board replication cost deferred to IHAP-55

## Cost-first rule

For IHAP-49, **cost is the first differentiator among options that already meet minimum compatibility, provenance and evidence thresholds**.

This rule does not authorize anonymous/reclaimed/ambiguous batteries or components whose missing controls would shift cost/risk elsewhere in the system.

## Selected battery procurement basis

Reference cell: **LG INR18650-MJ1**  
EAN / GTIN: `8438493099829`  
Selected seller: NKON

Project Owner order-decision values:

| Item | Amount |
|---|---:|
| 10 × cells product subtotal | EUR 19.90 |
| Shipping | EUR 6.33 |
| Planned landed order total | **EUR 26.23** |
| Product price per cell | EUR 1.99 |
| Planned landed average | **EUR 2.623/cell** |

Purchase completion is recorded only after explicit Project Owner confirmation.

Accounting after purchase must distinguish:

- cash-out procurement total;
- one installed cell per reference node unless the design changes;
- remaining cells as shared inventory;
- landed acquisition cost per conforming cell;
- final replication cost under the accepted procurement assumptions.

## Owned inventory disposition

The project already owns:

- `4056E` USB-C charger/protection breakout boards;
- single-cell 18650 holders with leads.

The holder remains the mechanical candidate and creates **no new holder purchase** at this stage. Actual fit remains physical downstream evidence.

The 4056E board is retained as bench/control inventory but is **rejected as the final custom-PCB power implementation**.

## Breakout procurement decision

The Project Owner explicitly chose a custom integrated mainboard as the final hardware direction.

Therefore do **not** purchase, solely for final-architecture emulation:

- TPS61023 boost modules;
- TPS2116 power-mux modules;
- additional TP4056/4056E chargers;
- other duplicated charger/boost/mux breakouts.

A breakout may be purchased later only if a specific validation blocker cannot be removed through the custom-PCB design path and the Project Owner approves the spend.

This prevents approximately the entire modular `charger + boost + mux` cash-out from becoming throw-away prototype inventory.

## Integrated PMIC cost direction

Preferred first custom-board PMIC: **MPS MP2636GR-P**.

Current dated distribution evidence used for planning:

- MPS status: Active;
- Mouser Europe snapshot: approximately **EUR 3.67 at qty 1**, **EUR 2.78 at qty 10**, **EUR 2.55 at qty 25** before board-level assembly/PCB economics.

Future cost-down candidate: **ETA9740**.

Current LCSC snapshot shows approximately **USD 0.26 at qty 5**, materially cheaper than MP2636. It is not selected for revision 1 because the first board prioritizes the stronger fit to NTC monitoring and separated input/SYS power-path controls. A later revision may revisit it once measured requirements are known.

## Board-level cost target

IHAP-49 does not invent a final PCB cost before schematic/BOM/fabrication evidence exists.

IHAP-55 must compare:

1. custom-board power BOM;
2. PCB/fabrication/assembly allocation;
3. battery + holder allocation;
4. connector/protection/passive allocation;
5. breakout-stack prototype equivalent;
6. complete node BOM impact.

The target is that the custom board should reduce **total** cost/footprint/interconnect complexity, not merely reduce one IC price.

## IHAP-17 boundary

IHAP-17 may consume the accepted IHAP-49 architecture after Project Owner approval, but the **definitive assembled power-board replication total** remains pending IHAP-55 implementation evidence. Historical owned inventory must remain distinct from replication pricing.
