# IHAP-49 — Owned Hardware Evidence

**Status:** visual/user-measured evidence; component qualification incomplete

## Owned 18650 holder

Observed characteristics:

- single-cell cylindrical holder marked for `18650` use;
- spring contact on one end;
- red/black wire leads;
- no keyed mechanism observed that would physically prevent reverse insertion.

User measurements:

- maximum useful length with spring fully compressed: approximately **70 mm**;
- maximum cell diameter/width: approximately **18 mm**.

Decision boundary:

- the owned holder remains inventory evidence only;
- it is **not accepted as the reference holder** until the exact selected cell is shown to fit without excessive interference or abnormal contact compression;
- the approximately 18 mm measured maximum width is especially restrictive relative to many branded 18650 cells whose manufacturer maximum diameter can exceed nominal 18.0 mm;
- reverse-insertion risk must be addressed by electrical protection and/or enclosure/access constraints.

## Owned USB-C charger/protection board

Observed board markings and topology:

- USB-C input connector;
- charger IC marking visibly consistent with `4056E`;
- battery pads labeled `B+` and `B-`;
- load/output pads labeled `OUT+` and `OUT-`;
- dual MOSFET marking visibly `8205A`;
- separate six-pin IC adjacent to the 8205A stage; exact marking/identity not reliably readable from current photographic evidence.

Supported statement:

> The tested specimen is a 4056E-family single-cell charger board with a discrete downstream protection stage including an 8205A dual MOSFET and a separate protection-controller IC.

Unsupported statements at this stage:

- that the charger IC is an original TP4056 rather than a compatible 4056E-family device;
- exact protection-controller identity;
- exact over-charge, over-discharge, over-current or short-circuit thresholds;
- suitability for simultaneous system load and charging;
- seamless normal-source/battery-source power-path behavior;
- safety certification or production suitability.

These remain `[UNVALIDATED]` until supported by exact component identification and/or physical tests.

## Evidence handling

The photographs were supplied directly by the Project Owner during IHAP-49 planning. This markdown file records only what can be read or measured from those specimens; it does not infer hidden component specifications from visually similar marketplace modules.
