# IHAP-49 — Final Review Summary

## Decision ready for Project Owner acceptance

IHAP-49 now closes the **power architecture decision** rather than forcing a temporary breakout-stack implementation.

Proposed reference contract:

- normal source: **regulated 5 V USB-C**;
- battery role: **backup only** for blackout/cable-input interruption;
- selected cell: **LG INR18650-MJ1**, EAN/GTIN `8438493099829`, flat-top unprotected 18650;
- final hardware direction: **one custom modular core PCB**;
- preferred first integrated PMIC: **MPS MP2636GR-P**;
- battery CV target: **4.2 V**;
- nominal charge-current target: **~1.0 A**;
- reference USB input: **5 V, >=1.5 A available/advertised**;
- SYS target: **5.0 V regulated, >=0.5 A continuous, >=1.0 A transient/headroom**;
- USB priority + automatic battery takeover;
- backfeed into upstream USB prohibited;
- **no-reset transfer is the reference target**;
- NTC battery-temperature monitoring required;
- unprotected cell means system-level protection is mandatory;
- multi-day battery-only operation is not an MVP requirement;
- planning autonomy remains ~12–20 h / ~16 h central and `[UNVALIDATED]`.

## Procurement direction

Purchase only hardware that persists in the final architecture or removes a specific blocker.

Current decision:

- LG MJ1 cells: **retain purchase**;
- existing holder: **retain**, no new holder purchase now;
- existing 4056E: bench/control evidence only;
- TPS61023 breakout: **do not purchase solely for final architecture**;
- TPS2116 breakout: **do not purchase solely for final architecture**;
- additional charger/boost/mux modules: **do not purchase without a specific blocker**.

## Why the 4056E gaps no longer block closure

The owned 4056E module was characterized enough to bound its use:

- `4056E` and `8205A` observed;
- protection controller exists but exact identity/thresholds remain unknown;
- legacy 5 V USB-A-to-C input sanity passed;
- tested C-to-C fast-charge input did not work;
- R3 in-circuit measurement was inconclusive.

The module is now **rejected as the final reference power implementation**, so unresolved RPROG/protection-controller details are inventory limitations, not blockers to the architecture decision.

## Implementation handoff

**IHAP-55 — Integrated Modular Edge PCB — Custom Mainboard Design and Prototype** owns:

- schematic/layout/DFM;
- MP2636 implementation or explicit reviewed supersession;
- 3.3 V regulator;
- USB-C input protection/CC implementation;
- NTC/reverse-polarity implementation;
- PCB fabrication/bring-up;
- charge current / thermal evidence;
- 5 V / 3.3 V rail measurements;
- USB-to-battery switchover/restoration;
- no-reset validation;
- measured backup runtime;
- final custom-board BOM and replication cost.

IHAP-50 owns the connection matrix. IHAP-51 owns enclosure, holder retention and serviceability.

## Review result by lane

- **Power Electronics:** PASS for architecture decision; implementation evidence handed to IHAP-55.
- **Battery Safety boundary:** PASS with residual physical validation explicit; no unsupported safety claim.
- **Hardware Compatibility:** PASS at contract level; final board must preserve accepted sensor domains.
- **Testing & Evidence:** PASS; planning arithmetic remains separated from measured runtime.
- **Security / Privacy:** PASS; no new sensing/data scope introduced.
- **Architecture Regression:** PASS; ESP32-C3, LD2410C, environmental profiles, reed and OLED decisions preserved.
- **Cost Governance:** PASS; redundant breakout purchases eliminated and board-level cost deferred to real BOM evidence.
- **Source of Truth:** PASS; ADR/evidence in GitHub, Jira workflow/handoff, Confluence not duplicated.

## Remaining gate

Only one IHAP-49 decision gate remains:

> **Project Owner explicit acceptance of ADR-0007 / PR #34.**

After acceptance, the PR can be merged and Jira IHAP-49 completed. Physical custom-board validation proceeds in IHAP-55 and may supersede ADR-0007 if evidence contradicts the contract.
