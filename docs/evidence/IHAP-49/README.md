# IHAP-49 — Edge Power Subsystem Decision Evidence

**Status:** Accepted PR #34 decision package + **Proposed IHAP-56 remediation overlay** in PR #35

This directory contains the evidence package for IHAP-49. The accepted architecture uses regulated 5 V USB-C as the normal node supply and a rechargeable single-cell Li-ion path only as backup for blackout or cable/input interruption.

## Accepted Project Owner direction — 2026-09-07

- Normal operating source: regulated 5 V via USB-C.
- Battery role: backup only, for blackout or cable/input failure.
- Battery is not the normal continuous energy source.
- Multi-day standalone operation is not an MVP requirement.
- Selected reference cell: **LG INR18650-MJ1**, EAN/GTIN `8438493099829`, flat-top unprotected 18650 Li-ion.
- Cost is the first differentiator after minimum compatibility/provenance/evidence thresholds are met.
- Final hardware direction: **one small, efficient, installable, modular custom core PCB**.
- Preferred first integrated power PMIC direction: **MPS MP2636GR-P**.
- MP2636 USB-mode pass-through requires a downstream regulated 5 V stage or reviewed equivalent topology.
- Existing 18650 holder remains the mechanical candidate; no replacement-holder purchase now.
- Owned 4056E breakout is retained only as bench/control evidence and is rejected as the final implementation.
- Do not buy redundant TPS61023/TPS2116/charger/boost/mux breakouts solely to emulate the final custom PCB.

## Accepted electrical baseline

- USB-C normal input: 5 V, no PD requirement; correct Type-C sink termination and C-to-C 5 V operation required. Functional V2 evidence covers **both DUT plug orientations**.
- Reference source: 5 V with at least 1.5 A available/advertised; system-load-priority input limiting required.
- Product SYS: 5.0 V regulated, 4.75–5.25 V steady-state validation band, **>=0.5 A continuous across the accepted battery range and valid USB-input range**, >=1.0 A transient/headroom target.
- Battery CV target 4.2 V; nominal charge current approximately 1.0 A.
- NTC monitoring required.
- USB priority + automatic battery takeover; upstream USB backfeed prohibited.
- No-reset transfer remains the target and `[UNVALIDATED]`.
- Reverse insertion requires electrical blocking/protection or mechanical keying; procedure alone is not acceptable.
- Accepted quantitative ownership transfer covers ADR-0001/0002/0004/0005.

## Proposed IHAP-56 remediation overlay — pending explicit Project Owner approval

The following items were introduced after PR #34 and are **Proposed**, not part of the 2026-09-07 acceptance record:

- RT-R012-01 source-side over-current interruption ahead of every service conductor claimed as protected; any segment before the element remains explicit residual exposure until separately controlled/verified;
- mandatory NTC normal/hot/cold/open/short verification;
- manufacturer-derived numeric thermal PASS/FAIL limits plus a justified MP2636 junction-temperature/derating method;
- worst-case ILIM <=1.50 A plus V14 combined node+charging verification;
- component-derived 3.3 V steady/transient PASS criteria;
- bidirectional V7 with <=100 µs current edges;
- V8/V9 high/mid/**valid-low** transfer/restoration, low-point margin above cutoff, quantified backfeed and zero restoration-attributable reset for proposed no-reset effectiveness verification;
- V10 cutoff 2.70±0.05 V, no deliberate <2.50 V operation, restart >=3.00±0.05 V or valid USB;
- V13 actual/production-identical source-side protection-path verification;
- bounded V15-A/V15-B reverse-blocking simulator tests with USB absent and present when electrical protection is used;
- extension of quantitative ownership transfer to **ADR-0003 / reed current**.

RT-R012-01 and RT-R013-01 remain **Proposed**, not Approved/Implemented/Verified. ADR-0007 acceptance partially mitigates the associated risks at the accepted architecture-baseline level but does not approve the later treatment detail or accept residual risk.

## Evidence captured

- Owned holder is marked for 18650 use and has red/black leads. User-measured maximum useful cell length with spring fully compressed: approximately 70 mm; user-measured maximum cell diameter/width: approximately 18 mm. Physical fit remains `[UNVALIDATED]` until cell receipt and downstream validation.
- Owned charger board exposes `B+`, `B-`, `OUT+`, and `OUT-`; `4056E` and `8205A` markings were observed, while the separate protection-controller identity remains `[UNVALIDATED]`.
- `IHAP49-CHARGER-C0-C1-01/run-record.md` records C0/C1: in-circuit R3 measurement inconclusive; legacy 5 V / 1.55 A USB-A-to-C source produced VIN 4.95 V and unloaded B/OUT about 4.19/4.18 V; tested C-to-C fast-charge source did not produce usable charger-board input.

## Implementation / validation handoff

- `ihap-56-closure-matrix.md` — canonical review matrix for Accepted-vs-Proposed state across PR #35.
- `validation-plan.md` — accepted PR #34 test baseline plus Proposed IHAP-56 strengthening.
- `downstream-contracts.md` — accepted IHAP-55 obligations vs Proposed treatment gates.
- `custom-pcb-power-contract.md` — same approval boundary and detailed power contract.
- IHAP-55 remains blocked by IHAP-56 until the remediation/approval gate is resolved.
- IHAP-51 owns holder retention, battery accessibility and enclosure/serviceability.
- IHAP-50 owns the final connection matrix.
- IHAP-57 coordinates later treatment lifecycle/effectiveness only after explicit treatment approval and implementation/verification evidence.

## Planning autonomy boundary

Planning calculations indicate approximately 12–20 h for a 3.5 Ah-class cell, with roughly 16 h as a central estimate under the current load model. **Autonomy remains `[UNVALIDATED]` until measured on the fabricated custom implementation.**

## Approval boundary

On **2026-09-07**, the Project Owner explicitly approved **ADR-0007 and PR #34**. That approval covers the architectural baseline only. The later IHAP-56 treatment/validation amendments remain Proposed until an explicit Project Owner decision records approval. Neither layer establishes safety, certification, production readiness, validated no-reset transfer or measured autonomy.
