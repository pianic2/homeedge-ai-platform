# IHAP-49 — Edge Power Subsystem Decision Evidence

**Status:** Accepted decision package — implementation validation handed to IHAP-55

This directory contains the evidence package for IHAP-49. The accepted architecture uses regulated 5 V USB-C as the normal node supply and a rechargeable single-cell Li-ion path only as backup for blackout or cable/input interruption.

## Accepted Project Owner direction

- Normal operating source: regulated 5 V via USB-C.
- Battery role: backup only, for blackout or cable/input failure.
- Battery is not the normal continuous energy source.
- Multi-day standalone operation is not an MVP requirement.
- Selected reference cell: **LG INR18650-MJ1**, EAN/GTIN `8438493099829`, flat-top unprotected 18650 Li-ion.
- Cost is the first differentiator after minimum compatibility/provenance/evidence thresholds are met.
- Final hardware direction: **one small, efficient, installable, modular custom core PCB**.
- Preferred first integrated power PMIC direction: **MPS MP2636GR-P**.
- Existing 18650 holder remains the mechanical candidate; no replacement-holder purchase now.
- Owned 4056E breakout is retained only as bench/control evidence and is rejected as the final implementation.
- Do not buy TPS61023, TPS2116 or additional charger/boost/mux breakouts solely to emulate the final custom PCB.

## Frozen electrical contract

- USB-C normal input: 5 V, no PD requirement.
- Correct Type-C sink termination required; USB-C-to-USB-C 5 V operation is required on the final PCB.
- Reference source: 5 V with at least 1.5 A available/advertised.
- Battery CV target: 4.2 V.
- Nominal charge-current target: approximately 1.0 A.
- NTC battery-temperature monitoring required.
- 5 V SYS target: 5.0 V regulated, >=0.5 A continuous design capability, >=1.0 A transient/headroom target.
- USB priority + automatic battery takeover.
- Backfeed into upstream USB prohibited.
- No-reset transfer is the reference target and remains `[UNVALIDATED]` pending IHAP-55 physical evidence.

## Evidence captured

- Owned holder is marked for 18650 use and has red/black leads. User-measured maximum useful cell length with spring fully compressed: approximately 70 mm; user-measured maximum cell diameter/width: approximately 18 mm. Seller-listed MJ1 diameter is approximately 18.2 mm. Physical fit remains `[UNVALIDATED]` until cell receipt and downstream physical validation.
- Owned USB-C charger board exposes `B+`, `B-`, `OUT+`, and `OUT-` terminals.
- Macro evidence shows a charger IC marked `4056E`, a dual MOSFET marked `8205A`, and a separate six-pin protection-controller device whose exact identity remains `[UNVALIDATED]`.
- `IHAP49-CHARGER-C0-C1-01/run-record.md` records the executed charger characterization: in-circuit R3 resistance was polarity-dependent and therefore inconclusive; the board accepted a legacy 5 V / 1.55 A USB-A-to-USB-C source at 4.95 V input, with unloaded B/OUT readings of approximately 4.19/4.18 V. A tested USB-C-to-USB-C fast-charge source did not produce usable board input voltage.

## Implementation / validation handoff

IHAP-55 owns the fabricated-board validation of:

- final MP2636 implementation or explicitly reviewed supersession;
- USB-C input/CC/ESD implementation;
- 3.3 V regulator;
- NTC and reverse-polarity implementation;
- charging current/termination/temperature;
- 5 V and 3.3 V rail behavior;
- source switchover/restoration;
- brownout/reset behavior;
- no-reset transfer validation;
- low-voltage behavior;
- measured backup runtime;
- final board-level BOM and replication cost.

IHAP-51 owns holder retention, battery accessibility and enclosure/serviceability. IHAP-50 owns the final connection matrix.

## Planning autonomy boundary

Planning calculations indicate approximately 12–20 h for a 3.5 Ah-class cell, with roughly 16 h as a central estimate under the current load model. **Autonomy remains `[UNVALIDATED]` until measured on the fabricated custom implementation.**

## Runbooks / plans

- `validation-plan.md` — implementation-validation handoff plan.
- `charger-characterization-runbook.md` — staged runbook for the owned 4056E charger/protection board.
- `IHAP49-CHARGER-C0-C1-01/run-record.md` — executed C0/C1 evidence.
- `custom-pcb-power-contract.md` — accepted electrical contract consumed by IHAP-55.

## Approval

On **2026-09-07**, the Project Owner explicitly approved **ADR-0007 and PR #34**.

This acceptance authorizes the architectural decision and PR merge. It does not establish safety certification, fire safety, production readiness, commercial readiness, validated no-reset transfer or measured backup autonomy.
