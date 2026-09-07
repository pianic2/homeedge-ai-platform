# IHAP-49 — Cost Governance Notes

**Status:** cell selected for procurement/validation; subsystem replication total still incomplete

## Cost-first selection rule

For IHAP-49, **cost is the first differentiator among options that already meet the minimum compatibility, provenance and evidence threshold**. Stronger documentation alone does not justify a higher-cost component when it does not materially improve the reference-node requirement.

The rule does not authorize anonymous/reclaimed/ambiguous cells merely because their sticker price is lower.

## Owned inventory evidence

The project already owns:

- USB-C 4056E-family charger/protection boards;
- single-cell 18650 holders with leads.

Historical ownership does not make either component automatically acceptable for the reference implementation.

The owned holder is retained as the **reference-holder candidate**. User measurements are approximately 70 mm useful length with the spring fully compressed and approximately 18 mm maximum opening. The Project Owner reports that the plastic body is slightly elastic and expects it to accommodate the selected cell's seller-listed approximately 18.2 mm diameter. **No new holder purchase is planned.** Physical fit/contact pressure remains `[UNVALIDATED]` until the cell arrives.

The owned charger/protection board remains a **candidate** because the exact protection-controller identity and quantitative trip thresholds are not yet verified.

## Selected cell procurement candidate

**LG INR18650-MJ1**  
EAN / GTIN: `8438493099829`  
Seller: NKON  
Planned quantity: **10**

Order-decision values supplied/confirmed by the Project Owner:

| Item | Amount |
|---|---:|
| 10 × cell product subtotal | EUR 19.90 |
| Shipping | EUR 6.33 |
| Planned landed order total | **EUR 26.23** |
| Product price per cell | EUR 1.99 |
| Landed average per cell across this order | **EUR 2.623** |

The order is **not recorded as completed yet**. Procurement completion must be recorded only after explicit Project Owner confirmation.

### Cost accounting boundary

Do not charge all 10 cells to one reference node.

After purchase/receipt, cost surfaces should distinguish:

- **cash-out procurement:** actual order total paid;
- **reference-node installed quantity:** 1 cell per node unless the final design changes;
- **remaining cells:** shared/project inventory;
- **landed unit acquisition cost:** total landed order / received conforming quantity;
- **replication cost:** the cost to reproduce the accepted subsystem under the stated procurement assumptions, not an arbitrary allocation of unused inventory.

## Replication-cost rule

The final power-subsystem replication cost must include every required component needed to reproduce the accepted architecture, including as applicable:

- regulated 5 V USB-C source/cable if part of the reference kit;
- exact backup cell;
- compatible holder;
- charger/protection board;
- DC/DC converter;
- source-selection/isolation components;
- switch;
- fuse/protection/polarity components;
- connectors and wiring attributable to the power subsystem.

A low individual part price must not be used to characterize the subsystem as inexpensive before this complete cost is known.

## Current disposition

Cell model selection is closed for procurement/validation, while procurement receipt/conformance and all remaining power-path components are still open. Definitive IHAP-17 BOM propagation and final replication totals remain deferred until the complete implementation is validated and Project Owner acceptance is obtained.
