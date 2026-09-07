# IHAP-49 — Project Owner Decision Record

**Decision date:** 2026-09-05  
**Cell-selection update:** 2026-09-07

## Decision

The reference MVP edge node will use **regulated 5 V via USB-C as the normal operating supply**.

A rechargeable battery subsystem remains part of the MVP only as **backup power** for:

- mains/input blackout affecting the USB-C source;
- cable disconnection or cable/input fault;
- short-duration continuity of the node when the normal 5 V source is unavailable.

The battery is therefore not the reference node's primary continuous power source and is not selected to provide multi-day standalone operation.

## Cell selection decision

The Project Owner selects **LG INR18650-MJ1** as the reference **cell candidate for procurement and physical validation**.

Selected listing / identity:

- manufacturer/brand: LG;
- model: `INR18650-MJ1`;
- EAN / GTIN: `8438493099829`;
- format: 18650, flat-top, unprotected Li-ion;
- nominal voltage: 3.6 V;
- typical capacity: 3500 mAh;
- minimum capacity in the selected seller listing: 3400 mAh;
- seller-listed maximum discharge current: 10 A;
- seller-listed dimensions: approximately 18.2 mm diameter × 65 mm height;
- selected seller: NKON;
- planned quantity: 10 cells;
- unit product price used for the order decision: EUR 1.99;
- planned product subtotal: EUR 19.90;
- planned shipping: EUR 6.33;
- planned landed order total: **EUR 26.23**;
- landed average across the 10-cell order: **EUR 2.623/cell**.

The cost-first selection rule is explicit: among cells that meet the minimum provenance, electrical-envelope and reproducibility threshold, total cost is the primary differentiator. Molicel M35A is therefore not preferred merely for stronger documentation when the LG MJ1 provides an adequate technical envelope at lower cost.

The selected cell is **not yet physically accepted**. Procurement completion, actual received markings/condition, holder fit, charger/protection behavior and integrated backup validation remain pending. The planned purchase must not be recorded as completed until the Project Owner confirms the order.

The already-owned holder remains the reference-holder candidate. The Project Owner states that its plastic body has enough compliance that the approximately 0.2 mm nominal interference between the user-measured ~18 mm opening and the seller-listed ~18.2 mm cell diameter is expected to be recovered by elastic deformation. This is a design assumption only; actual fit/contact pressure must be verified non-destructively when the selected cell arrives.

## Consequences

1. The normal-source design is centered on a regulated 5 V USB-C input.
2. The backup path must ultimately provide a regulated 5 V domain compatible with the accepted node loads.
3. The subsystem must resolve source switchover, isolation and backfeed behavior; the charger module alone is not treated as a complete UPS/power-path solution.
4. Backup capacity is sized against a blackout/cable-fault continuity objective rather than a multi-day off-grid objective.
5. Planning calculations indicate a 3.5 Ah-class 1S Li-ion cell is plausibly in the ~12–20 h backup range, with ~16 h as a central estimate, but autonomy remains `[UNVALIDATED]` until measured on the frozen implementation.
6. USB power-meter purchase is not required at this stage. A multimeter plus brownout/reset logging is the minimum validation instrumentation; unexplained transient behavior must escalate to appropriate higher-bandwidth measurement rather than be inferred from a slow USB meter.
7. The exact cell model is selected for procurement/validation; holder fit, converter and source-selection/power-path implementation remain open validation/implementation decisions inside IHAP-49.
8. No safety, certification, fire-safety, production-readiness or compliance claim is implied by retaining a backup battery.

## Project Owner review gate

This decision authorizes execution/documentation of IHAP-49 but does not authorize merge, ADR acceptance, Jira completion or definitive IHAP-17 BOM propagation. Those remain gated on Project Owner review of the Proposed implementation and evidence.
