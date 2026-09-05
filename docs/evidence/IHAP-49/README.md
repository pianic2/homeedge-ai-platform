# IHAP-49 — Edge Power Subsystem Decision Evidence

**Status:** Planning evidence — Project Owner review pending

This directory contains the evidence package for IHAP-49. The decision under review is to use regulated 5 V USB-C as the normal node supply and retain a rechargeable single-cell battery subsystem only as backup for blackout or cable/input interruption.

No battery, charger, holder, converter, autonomy, safety, certification, compliance, production-readiness or installation claim is accepted by this evidence package unless explicitly supported by a completed validation record.

## Current Project Owner direction

- Normal operating source: regulated 5 V via USB-C.
- Battery role: backup only, for blackout or cable/input failure.
- Battery is not the normal continuous energy source.
- Multi-day standalone operation is not an MVP requirement.
- Rechargeable battery architecture remains in scope and must be validated as one coupled subsystem.
- USB power meter is not currently required; ordinary multimeter measurements plus brownout/reset evidence are the minimum planned instrumentation, with higher-bandwidth instrumentation required only if transient failures cannot otherwise be bounded.

## Evidence captured before execution

- Owned holder is marked for 18650 use and has red/black leads. User-measured maximum useful cell length with spring fully compressed: approximately 70 mm. User-measured maximum cell diameter/width: approximately 18 mm. This dimensional envelope is not accepted as compatible with a specific reference cell yet.
- Owned USB-C charger board exposes `B+`, `B-`, `OUT+`, and `OUT-` terminals.
- Macro evidence shows a charger IC marked `4056E`, a dual MOSFET marked `8205A`, and a separate six-pin protection-controller device whose exact identity is not yet verified.
- The owned charger board therefore has a discrete downstream protection stage in addition to the charger function, but the exact protection-controller identity and trip thresholds remain `[UNVALIDATED]`.

## Decision evidence still required

1. Select and document the exact backup cell SKU, chemistry, capacity, provenance and protected/unprotected policy.
2. Select a mechanically compatible holder; the owned 18 mm maximum-width holder is not accepted as the reference holder until compatibility with the selected cell is physically demonstrated.
3. Select the 1S-to-regulated-5 V conversion topology/component and demonstrate sufficient steady-state and transient headroom.
4. Resolve normal-source/backup-source switchover and backfeed isolation. A charger board with `B/OUT` terminals is not by itself evidence of seamless system power-path management.
5. Freeze the rule for whether charging while the node is operating is permitted. Until demonstrated with an explicit power-path design, it remains prohibited.
6. Measure integrated node input current and rail voltages under representative operation and check for resets/brownout.
7. Validate backup transfer/recovery and an actual discharge run before making an autonomy claim.
8. Record whole-subsystem replication cost after exact components are selected.

## Planning power estimate

The planning estimate is intentionally not a validation result. For the accepted reference node profile, a working central estimate is approximately 0.625 W of 5 V load power, dominated by the always-on LD2410C presence radar. With an assumed 90% boost efficiency, this corresponds to about 0.694 W from a 1S battery path. A nominal 3.5 Ah, 3.6 V cell therefore has about 12.6 Wh nominal energy; using a conservative 90% planning-use factor yields approximately 11.34 Wh and about 16.3 h estimated backup runtime at the central load assumption.

Planning range before physical measurement: approximately 12–20 h for a 3.5 Ah-class cell depending on actual ESP32-C3/Wi-Fi duty cycle, OLED content, converter efficiency, cell usable energy and cutoff behavior.

**Autonomy remains `[UNVALIDATED]`.** Capacity arithmetic does not satisfy the acceptance criterion for measured autonomy.

## Required physical validation sequence

- polarity and continuity inspection with power removed;
- charger-board identity and terminal mapping verification;
- cell/holder fit and polarity control;
- normal 5 V USB-C operation with the complete reference load;
- 5 V and 3.3 V rail measurement under representative load;
- integrated steady-state current measurement;
- brownout/reset logging during Wi-Fi activity, radar operation and display activity;
- battery-path regulation check across representative cell voltage range;
- normal-source interruption and backup takeover behavior;
- restoration of normal source and recovery behavior;
- charging behavior with the operating-load rule enforced;
- protection/failure cases that can be exercised without bypassing component ratings;
- controlled backup-runtime discharge run after the exact cell and power path are frozen.

## Claim boundary

Until those tests are complete, the subsystem must not be described as safe, certified, fire-safe, compliant, production-ready, fault-tolerant, seamless-UPS capable, or validated for a stated number of hours. The current artifacts define a Proposed architecture and the evidence still needed to accept it.
