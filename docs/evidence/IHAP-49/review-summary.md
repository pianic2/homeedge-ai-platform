# IHAP-49 — Proposed Review Summary

## Proposed subsystem decision

Use regulated **5 V USB-C as the normal operating source** for the reference MVP edge node and retain a **rechargeable single-cell battery path only as backup** for blackout or cable/input interruption.

This resolves the previous primary-source question: battery operation is required in the MVP only as continuity/backup capability, not as the normal source and not as a multi-day off-grid requirement.

## What is decided now

- normal source class: regulated 5 V USB-C;
- backup battery remains in scope;
- battery role is backup only;
- node load remains one regulated 5 V domain feeding LD2410C and ESP32-C3 board input, with accepted 3.3 V peripherals downstream;
- backup path requires 1S-to-regulated-5 V conversion;
- source switchover/isolation and backfeed behavior must be explicit;
- charger module alone is not treated as a complete UPS/power-path solution;
- charging while operating from the battery path remains prohibited until an explicit load-sharing/power-path implementation is selected and validated;
- autonomy arithmetic is planning evidence only and remains `[UNVALIDATED]` until a controlled discharge run.

## What remains open before acceptance

- exact cell SKU/provenance/protection policy;
- exact mechanically compatible holder;
- exact 1S-to-5 V converter;
- exact source-selection/isolation implementation;
- charger current configuration and protection-controller identity/thresholds;
- normal source/cable reference profile;
- integrated current/rail/brownout measurements;
- backup transfer/restoration behavior;
- measured backup runtime;
- complete replication cost.

## Recommendation

Continue IHAP-49 in the current branch/PR and close the exact component selection plus physical validation inside the same PR. Do not create a second remediation branch or PR. Keep the ADR Proposed until explicit Project Owner acceptance.
