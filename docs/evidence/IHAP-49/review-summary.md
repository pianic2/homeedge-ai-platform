# IHAP-49 — Proposed Review Summary

## Proposed subsystem decision

Use regulated **5 V USB-C as the normal operating source** for the reference MVP edge node and retain a **rechargeable single-cell battery path only as backup** for blackout or cable/input interruption.

This resolves the previous primary-source question: battery operation is required in the MVP only as continuity/backup capability, not as the normal source and not as a multi-day off-grid requirement.

## What is decided now

- normal source class: regulated 5 V USB-C;
- backup battery remains in scope;
- battery role is backup only;
- selected cell candidate for procurement/validation: **LG INR18650-MJ1**, EAN/GTIN `8438493099829`, flat-top unprotected 18650 Li-ion;
- cell selection policy: cost-first after minimum compatibility/provenance/evidence thresholds are met;
- planned order decision: 10 cells, EUR 19.90 subtotal + EUR 6.33 shipping = EUR 26.23 landed total; purchase completion still pending Project Owner confirmation;
- owned 18650 holder retained as reference-holder candidate with no new holder purchase; actual MJ1 fit/contact pressure remains `[UNVALIDATED]` until receipt;
- node load remains one regulated 5 V domain feeding LD2410C and ESP32-C3 board input, with accepted 3.3 V peripherals downstream;
- backup path requires 1S-to-regulated-5 V conversion;
- source switchover/isolation and backfeed behavior must be explicit;
- charger module alone is not treated as a complete UPS/power-path solution;
- charging while operating from the battery path remains prohibited until an explicit load-sharing/power-path implementation is selected and validated;
- autonomy arithmetic is planning evidence only and remains `[UNVALIDATED]` until a controlled discharge run.

## What remains open before acceptance

- confirm completed procurement and inspect received MJ1 markings/condition;
- validate MJ1 mechanical fit/contact pressure in the owned holder;
- select exact 1S-to-5 V converter;
- select exact source-selection/isolation implementation;
- verify charger current configuration and protection-controller identity/thresholds;
- freeze normal source/cable reference profile;
- complete integrated current/rail/brownout measurements;
- validate backup transfer/restoration behavior;
- measure backup runtime;
- freeze complete replication cost.

## Recommendation

Continue IHAP-49 in the current branch/PR. Cell model selection is closed for procurement/validation; the next immediately actionable bench step, while the cells are in procurement, is **unpowered characterization of the owned 4056E charger/protection board**, starting with the charge-current programming resistor and terminal mapping. Then close the 1S-to-5 V converter and source-selection implementation in the same PR. Do not create a second remediation branch or PR. Keep the ADR Proposed until explicit Project Owner acceptance.
