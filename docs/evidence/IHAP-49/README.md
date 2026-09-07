# IHAP-49 — Edge Power Subsystem Decision Evidence

**Status:** Execution evidence — Project Owner review ongoing

This directory contains the evidence package for IHAP-49. The decision under review is to use regulated 5 V USB-C as the normal node supply and retain a rechargeable single-cell battery subsystem only as backup for blackout or cable/input interruption.

No battery, charger, holder, converter, autonomy, safety, certification, compliance, production-readiness or installation claim is accepted by this evidence package unless explicitly supported by a completed validation record.

## Current Project Owner direction

- Normal operating source: regulated 5 V via USB-C.
- Battery role: backup only, for blackout or cable/input failure.
- Battery is not the normal continuous energy source.
- Multi-day standalone operation is not an MVP requirement.
- Selected cell candidate for procurement/validation: **LG INR18650-MJ1**, EAN/GTIN `8438493099829`, flat-top unprotected 18650 Li-ion.
- Cost is the first differentiator after minimum compatibility/provenance/evidence thresholds are met.
- Owned 18650 holder remains the reference-holder candidate; no replacement holder purchase is planned. Actual MJ1 fit/contact pressure remains `[UNVALIDATED]` until receipt.
- USB power meter is not currently required; ordinary multimeter measurements plus brownout/reset evidence are the minimum planned instrumentation, with higher-bandwidth instrumentation required only if transient failures cannot otherwise be bounded.

## Current procurement decision

Planned NKON order:

- 10 × LG INR18650-MJ1;
- product subtotal: EUR 19.90;
- shipping: EUR 6.33;
- planned landed total: **EUR 26.23**;
- landed average: **EUR 2.623/cell**.

Purchase completion is not recorded until the Project Owner explicitly confirms the completed order.

## Evidence captured

- Owned holder is marked for 18650 use and has red/black leads. User-measured maximum useful cell length with spring fully compressed: approximately 70 mm. User-measured maximum cell diameter/width: approximately 18 mm. Project Owner reports slight plastic compliance; seller-listed MJ1 diameter is approximately 18.2 mm. Physical fit remains `[UNVALIDATED]`.
- Owned USB-C charger board exposes `B+`, `B-`, `OUT+`, and `OUT-` terminals.
- Macro evidence shows a charger IC marked `4056E`, a dual MOSFET marked `8205A`, and a separate six-pin protection-controller device whose exact identity is not yet verified.
- The owned charger board therefore has a discrete downstream protection stage in addition to the charger function, but the exact protection-controller identity and trip thresholds remain `[UNVALIDATED]`.
- `IHAP49-CHARGER-C0-C1-01/run-record.md` records the first executed charger characterization: in-circuit R3 resistance was polarity-dependent and therefore inconclusive; the board accepted a legacy 5 V / 1.55 A USB-A-to-USB-C source at 4.95 V input, with unloaded B/OUT readings of approximately 4.19/4.18 V. A tested USB-C-to-USB-C fast-charge source did not produce usable board input voltage and is not accepted as compatible with this charger module.

## Remaining decision / validation work

1. Confirm completed cell procurement and inspect received cell markings/condition.
2. Validate LG MJ1 fit/contact pressure in the owned holder.
3. Complete charger/protection validation with the received cell: actual charge current, terminal voltage, termination behavior and thermal observations.
4. Select the 1S-to-regulated-5 V conversion topology/component and demonstrate sufficient steady-state and transient headroom.
5. Resolve normal-source/backup-source switchover and backfeed isolation. A charger board with `B/OUT` terminals is not by itself evidence of seamless system power-path management.
6. Freeze the rule for whether charging while the node is operating is permitted. Until demonstrated with an explicit power-path design, it remains prohibited.
7. Measure integrated node input current and rail voltages under representative operation and check for resets/brownout.
8. Validate backup transfer/recovery and an actual discharge run before making an autonomy claim.
9. Record whole-subsystem replication cost after exact components are selected.

## Planning power estimate

The planning estimate is intentionally not a validation result. For the accepted reference node profile, a working central estimate is approximately 0.625 W of 5 V load power, dominated by the always-on LD2410C presence radar. With an assumed 90% boost efficiency, this corresponds to about 0.694 W from a 1S battery path. A nominal 3.5 Ah, 3.6 V cell therefore has about 12.6 Wh nominal energy; using a conservative 90% planning-use factor yields approximately 11.34 Wh and about 16.3 h estimated backup runtime at the central load assumption.

Planning range before physical measurement: approximately 12–20 h for a 3.5 Ah-class cell depending on actual ESP32-C3/Wi-Fi duty cycle, OLED content, converter efficiency, cell usable energy and cutoff behavior.

**Autonomy remains `[UNVALIDATED]`.** Capacity arithmetic does not satisfy the acceptance criterion for measured autonomy.

## Runbooks / plans

- `validation-plan.md` — overall IHAP-49 physical-validation plan.
- `charger-characterization-runbook.md` — staged runbook for the owned 4056E charger/protection board.
- `IHAP49-CHARGER-C0-C1-01/run-record.md` — executed C0/C1 evidence: R3 in-circuit HOLD/inconclusive; legacy 5 V charger-input sanity PASS; USB-C-to-USB-C compatibility not demonstrated.

## Required physical validation sequence

- charger-board unpowered characterization;
- received-cell identity/condition and cell/holder fit;
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
