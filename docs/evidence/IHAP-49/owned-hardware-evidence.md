# IHAP-49 — Owned Hardware Evidence

**Status:** bounded physical evidence; owned modules retained as bench/control inventory

## Owned 18650 holder

Observed characteristics:

- single-cell cylindrical holder marked for `18650` use;
- spring contact on one end;
- red/black wire leads;
- no keyed mechanism observed that would physically prevent reverse insertion.

User measurements:

- maximum useful length with spring fully compressed: approximately **70 mm**;
- maximum cell diameter/width: approximately **18 mm**.

Project Owner disposition — 2026-09-07:

- do **not** procure a replacement holder at this decision stage;
- retain this owned holder as the reference mechanical candidate;
- holder body is reported as slightly elastic/compliant;
- selected LG INR18650-MJ1 seller listing gives approximately **18.2 mm diameter × 65 mm height**;
- expected fit via slight elastic deformation is a hypothesis only and remains `[UNVALIDATED]` until receipt.

Downstream acceptance conditions:

- insertion must not require excessive force;
- wrapper must not be cut, pinched or abraded;
- contacts must maintain reliable pressure without visible cell damage;
- removal must remain controlled;
- **procedure or polarity labeling alone is not an acceptable reverse-insertion control**;
- ordinary installation/service must include either:
  - electrical reverse-battery blocking/protection; or
  - a mechanically keyed holder/interface/enclosure that physically prevents reversed insertion;
- because the selected MJ1 is unprotected, the final design must also include **cell-side over-current interruption** positioned so holder-lead/BAT-net faults upstream of PMIC SYS protection are covered.

Final fit/retention evidence belongs to IHAP-55 / IHAP-51. Electrical cell-side protection belongs to IHAP-55 and is tracked canonically by `docs/risks/records/R-012-unprotected-li-ion-battery-fault.md`.

## Owned USB-C charger/protection board

Observed markings/topology:

- USB-C input connector;
- charger IC marked `4056E`;
- battery pads `B+` / `B-`;
- output pads `OUT+` / `OUT-`;
- dual MOSFET marked `8205A`;
- separate six-pin protection-controller IC; exact identity/marking not reliably readable.

Supported statement:

> The tested specimen is a 4056E-family single-cell charger board with a discrete downstream protection stage including an 8205A dual MOSFET and a separate protection-controller IC.

Executed C0/C1 evidence:

- in-circuit R3 readings: approximately 0.814 kΩ and 0.345 kΩ with probes reversed on the 2 kΩ range;
- result: **inconclusive**, so no RPROG or charge-current value was inferred;
- legacy 5 V / 1.55 A USB-A-to-USB-C source: VIN **4.95 V**;
- unloaded `B+/B-`: approximately **4.19 V**;
- unloaded `OUT+/OUT-`: approximately **4.18 V**;
- tested USB-C-to-USB-C fast-charge source did not produce usable board input in the tested configuration.

Unsupported statements remain:

- original TP4056 identity;
- exact protection-controller identity/thresholds;
- exact programmed charge current;
- validated charge termination with LG MJ1;
- simultaneous load/charge power-path behavior;
- seamless UPS behavior;
- safety/certification/production suitability.

## Final disposition

The owned `4056E + 8205A` breakout is **REJECTED as the final reference power implementation** because the product direction requires a custom integrated core PCB and this board does not establish the required system power-path / regulated-product-SYS / USB-C-to-USB-C behavior.

It remains useful as:

- historical procurement evidence;
- component-characterization evidence;
- optional bench/control hardware.

Its unresolved exact RPROG and protection-controller thresholds are therefore **not IHAP-49 architecture-acceptance blockers** and must not be reused as assumed final-board protection values.

## Selected cell relation

The selected reference cell is **LG INR18650-MJ1**, EAN/GTIN `8438493099829`, flat-top unprotected 18650 Li-ion. Because it is unprotected, the final custom PCB must provide the required system-level charging, low-voltage, cell-side over-current, thermal and polarity controls defined by ADR-0007 and R-012.

## Evidence handling

The photographs and measurements were supplied directly by the Project Owner during IHAP-49. This file records only observed/measured facts and explicit owner decisions; it does not infer hidden specifications from visually similar marketplace modules.
