# IHAP-49 — Project Owner Decision Record

**Decision date:** 2026-09-05

## Decision

The reference MVP edge node will use **regulated 5 V via USB-C as the normal operating supply**.

A rechargeable battery subsystem remains part of the MVP only as **backup power** for:

- mains/input blackout affecting the USB-C source;
- cable disconnection or cable/input fault;
- short-duration continuity of the node when the normal 5 V source is unavailable.

The battery is therefore not the reference node's primary continuous power source and is not selected to provide multi-day standalone operation.

## Consequences

1. The normal-source design is centered on a regulated 5 V USB-C input.
2. The backup path must ultimately provide a regulated 5 V domain compatible with the accepted node loads.
3. The subsystem must resolve source switchover, isolation and backfeed behavior; the charger module alone is not treated as a complete UPS/power-path solution.
4. Backup capacity is sized against a blackout/cable-fault continuity objective rather than a multi-day off-grid objective.
5. Planning calculations indicate a 3.5 Ah-class 1S Li-ion cell is plausibly in the ~12–20 h backup range, with ~16 h as a central estimate, but autonomy remains `[UNVALIDATED]` until measured on the frozen implementation.
6. USB power-meter purchase is not required at this stage. A multimeter plus brownout/reset logging is the minimum validation instrumentation; unexplained transient behavior must escalate to appropriate higher-bandwidth measurement rather than be inferred from a slow USB meter.
7. Exact cell, holder, converter and source-selection/power-path components remain open implementation decisions inside IHAP-49 until evidence is complete.
8. No safety, certification, fire-safety, production-readiness or compliance claim is implied by retaining a backup battery.

## Project Owner review gate

This decision authorizes execution/documentation of IHAP-49 but does not authorize merge, ADR acceptance, Jira completion or definitive IHAP-17 BOM propagation. Those remain gated on Project Owner review of the Proposed implementation and evidence.
