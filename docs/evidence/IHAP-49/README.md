# IHAP-49 — Edge Power Subsystem Decision Evidence

**Status:** Accepted PR #34 decision package + **Proposed IHAP-56 remediation overlay** in PR #35

This directory contains the evidence package for IHAP-49. The accepted architecture uses regulated 5 V USB-C as the normal node supply and a rechargeable single-cell Li-ion path only as backup for blackout or cable/input interruption.

## Accepted Project Owner direction — 2026-09-07

- Normal operating source: regulated 5 V via USB-C.
- Battery role: backup only, for blackout or cable/input failure.
- Battery is not the normal continuous energy source.
- Multi-day standalone operation is not an MVP requirement.
- Selected reference cell: **LG INR18650-MJ1**, EAN/GTIN `8438493099829`, flat-top unprotected 18650 Li-ion.
- Final hardware direction: **one small, efficient, installable, modular custom core PCB**.
- Preferred first integrated power PMIC direction: **MPS MP2636GR-P** plus downstream regulated 5 V stage or reviewed equivalent topology.
- Existing 18650 holder remains the mechanical candidate; no replacement-holder purchase at this decision stage.
- Owned 4056E breakout is bench/control evidence only and is rejected as the final implementation.
- Redundant TPS61023/TPS2116/charger/boost/mux breakouts are not required solely to emulate the final custom PCB.

## Accepted electrical baseline

- USB-C normal input: 5 V, no PD requirement; correct Type-C sink termination and C-to-C 5 V operation required. V2 covers **both DUT plug orientations**.
- Reference source: 5 V with at least 1.5 A available/advertised; system-load-priority input limiting required.
- Product SYS: 5.0 V regulated, 4.75–5.25 V steady-state validation band, **>=0.5 A continuous across the accepted battery range and valid USB-input range**, >=1.0 A transient/headroom target.
- Battery CV target 4.2 V; nominal charge current approximately 1.0 A.
- NTC monitoring required.
- USB priority + automatic battery takeover; upstream USB backfeed prohibited.
- No-reset transfer remains the target and `[UNVALIDATED]`.
- Reverse insertion requires electrical blocking/protection or mechanical keying; procedure alone is not acceptable.
- Accepted quantitative ownership transfer covers ADR-0001/0002/0004/0005.

## Proposed IHAP-56 remediation overlay — pending explicit Project Owner approval

- RT-R012-01 source-side over-current interruption ahead of every service conductor claimed as protected; any segment before it remains explicit residual exposure until separately controlled/verified;
- mandatory NTC normal/hot/cold/open/short verification;
- manufacturer-derived thermal limits + justified MP2636 junction-temperature/derating method;
- worst-case ILIM <=1.50 A + V14;
- component-derived 3.3 V steady/transient criteria;
- bidirectional V7 with <=100 µs edges;
- high/mid/valid-low V8/V9 with loaded cutoff margin, quantified backfeed and zero-reset restoration criterion;
- numeric V10 cutoff/recovery;
- V13 installed/production-identical path verification;
- V15-A/V15-B with USB absent/present;
- ADR-0003/reed-current ownership extension.

RT-R012-01 and RT-R013-01 remain **Proposed**, not Approved/Implemented/Verified. ADR-0007 acceptance partially mitigates the associated risks at architecture-baseline level but does not approve later treatment detail or residual risk.

## Evidence / review routing

- `ihap-56-closure-matrix.md` — frozen Accepted-vs-Proposed review matrix.
- `validation-plan.md` — accepted baseline + Proposed verification overlay.
- `downstream-contracts.md` — accepted IHAP-55 obligations vs Proposed gates.
- `custom-pcb-power-contract.md` — detailed electrical boundary.
- `R-012` / `R-013` — canonical treatment dossiers.

The 2026-09-09 regression sweep reconciled **all 16 files changed by PR #35** against the matrix. **Author remediation is frozen pending the next independent review.**

IHAP-55 remains blocked by IHAP-56. IHAP-50 owns the connection matrix, IHAP-51 holder/enclosure serviceability, and IHAP-57 later treatment lifecycle/effectiveness after explicit approval and evidence.

## Planning / claim boundary

Planning backup runtime remains approximately 12–20 h with ~16 h central estimate under the current model, but autonomy remains `[UNVALIDATED]` until measured. Neither Accepted nor Proposed documentation establishes safety, certification, production readiness, validated no-reset transfer or measured autonomy.

PR #35 must not merge until its frozen latest-head independent review has no unresolved blocking finding. A clean review alone does not approve the Proposed treatment lifecycle.
