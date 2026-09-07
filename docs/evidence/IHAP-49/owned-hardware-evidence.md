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

Project Owner disposition update — 2026-09-07:

- do **not** procure a replacement holder;
- retain this owned holder as the reference-holder candidate;
- the holder body is reported as slightly elastic/compliant;
- the selected LG INR18650-MJ1 seller listing gives approximately **18.2 mm diameter × 65 mm height**, so the current mechanical hypothesis is that the ~0.2 mm nominal interference can be accommodated by elastic deformation of the holder body;
- this hypothesis is **not yet physical evidence** and must be checked non-destructively when the selected cell arrives.

Acceptance boundary:

- actual insertion must not require excessive force;
- the cell wrapper must not be cut, pinched or abraded by the holder;
- contacts must maintain reliable pressure without visibly deforming/damaging the cell;
- removal must remain controlled;
- reverse-insertion risk must still be addressed by electrical protection and/or enclosure/access constraints.

Holder fit/contact pressure remains `[UNVALIDATED]` until the received LG MJ1 specimen is tested.

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

## Selected cell relation

The selected procurement/validation candidate is **LG INR18650-MJ1**, EAN/GTIN `8438493099829`, flat-top unprotected 18650 Li-ion. Because the cell is unprotected, continued use of this cell in the reference subsystem depends on successful qualification of system-level charge/discharge protection and failure behavior.

## Evidence handling

The photographs were supplied directly by the Project Owner during IHAP-49 planning. This markdown file records only what can be read or measured from those specimens; it does not infer hidden component specifications from visually similar marketplace modules.
