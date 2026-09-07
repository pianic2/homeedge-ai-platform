# IHAP-49 — Edge Power Subsystem Decision Evidence

**Status:** architecture decision package ready for Project Owner acceptance

This directory contains the canonical evidence supporting ADR-0007.

## Final Proposed decision

- Normal operating source: **regulated 5 V via USB-C**.
- Battery role: **backup only** for blackout / cable-input interruption.
- Selected cell: **LG INR18650-MJ1**, EAN/GTIN `8438493099829`, flat-top unprotected 18650 Li-ion.
- Final hardware direction: **small, efficient, installable, modular custom core PCB**, not a permanent breakout stack.
- Preferred first integrated power PMIC: **MPS MP2636GR-P**.
- USB-C input: 5 V only, correct Type-C sink termination, reference source >=1.5 A available/advertised.
- Charge target: 4.2 V CV, ~1.0 A nominal.
- 5 V SYS target: >=0.5 A continuous and >=1.0 A transient/headroom capability.
- Battery-temperature monitoring required.
- USB priority; automatic battery takeover required; no-reset transfer is the target.
- Backfeed into upstream USB is prohibited.
- Multi-day battery-only operation is not an MVP requirement.
- Backup estimate remains ~12–20 h / ~16 h central and `[UNVALIDATED]` until IHAP-55 measures it.

## Procurement direction

Selected/planned NKON cell order:

- 10 × LG INR18650-MJ1;
- product subtotal EUR 19.90;
- shipping EUR 6.33;
- planned landed total **EUR 26.23**;
- planned landed average **EUR 2.623/cell**.

Purchase completion is recorded only after explicit Project Owner confirmation.

No new power breakout is required solely to emulate the final custom board:

- TPS61023: do not purchase for final-architecture emulation;
- TPS2116: do not purchase for final-architecture emulation;
- extra 4056E/TP4056 boards: do not purchase without a specific blocker;
- existing holder remains the mechanical candidate;
- existing charger modules remain bench/control inventory.

## Evidence captured in IHAP-49

- voltage/current-domain and autonomy planning budget;
- exact cell selection/procurement rationale;
- holder measurements and reverse-insertion limitation;
- owned charger board visual evidence (`4056E`, `8205A`, separate protection controller);
- C0 R3 in-circuit measurement correctly recorded as inconclusive;
- C1 legacy 5 V input sanity: VIN 4.95 V; unloaded B/OUT ~4.19/4.18 V;
- tested USB-C-to-USB-C fast-charge input limitation on the owned breakout;
- wired-only / battery / cell / PMIC / breakout alternatives;
- custom-PCB power contract;
- risk assessment;
- cost governance;
- downstream handoff;
- physical validation plan for IHAP-55.

## Key documents

- `../../adr/ADR-0007-edge-power-subsystem.md` — Proposed subsystem ADR.
- `decision-record.md` — Project Owner decisions accumulated during execution.
- `custom-pcb-power-contract.md` — frozen electrical contract consumed by IHAP-55.
- `power-tree.md` — final Proposed power-domain structure.
- `power-budget.md` — planning load/autonomy model.
- `alternatives.md` — architecture / PMIC / breakout comparisons.
- `owned-hardware-evidence.md` — visual/user-measured evidence for existing components.
- `charger-characterization-runbook.md` — staged owned-module characterization method.
- `IHAP49-CHARGER-C0-C1-01/run-record.md` — executed charger evidence.
- `validation-plan.md` — custom-board validation handoff to IHAP-55.
- `risk-assessment.md` — residual risk ownership.
- `cost-governance.md` — procurement and cost-down boundaries.
- `downstream-contracts.md` — IHAP-50/55/51/17/43 handoffs.
- `source-register.md` — canonical/manufacturer/supplier source register.
- `review-checklist.md` — final review gate.
- `review-summary.md` — concise acceptance summary.

## Closure boundary

IHAP-49 is a **hardware architecture decision task**, not the custom-PCB fabrication task.

It is ready for acceptance when the Project Owner approves ADR-0007 and this evidence package. Physical implementation evidence moves to:

- **IHAP-55** — custom board schematic, PCB, bring-up, charging, rails, transfer, runtime and final BOM;
- **IHAP-51** — battery retention/serviceability/enclosure and sensor placement.

If those downstream tests contradict ADR-0007, the architecture must be explicitly superseded/reopened rather than silently weakened.

## Claim boundary

Nothing in this package establishes `safe`, `certified`, `fire-safe`, `compliant`, `production-ready`, `commercial-ready` or measured-runtime status. Those claims require specific downstream evidence and, where relevant, formal certification outside this MVP task.
