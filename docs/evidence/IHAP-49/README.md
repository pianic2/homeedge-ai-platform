# IHAP-49 — Edge Power Subsystem Decision Evidence

**Status:** Accepted decision package — implementation validation handed to IHAP-55; post-merge remediation tracked by IHAP-56 / PR #35

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

## Frozen electrical / protection contract

- USB-C normal input: 5 V, no PD requirement; correct Type-C sink termination and C-to-C 5 V operation required.
- Reference source: 5 V with at least 1.5 A available/advertised; board ILIM worst-case including tolerance must be <=1.50 A.
- MP2636 pass-through is an intermediate node only; **post-regulation or reviewed equivalent** must create the regulated product 5 V SYS in both USB and battery modes.
- Battery CV target: 4.2 V; nominal charge current approximately 1.0 A.
- NTC monitoring is mandatory and normal/hot/cold/open/short behavior must be functionally verified.
- Unprotected MJ1 requires **cell-side over-current interruption** covering holder/BAT faults upstream of PMIC-output limiting.
- Reverse insertion requires electrical blocking/protection or mechanical keying; procedure alone is not a control. Electrical blocking requires bounded simulator verification.
- Product SYS: 5.0 V regulated, >=0.5 A continuous, >=1.0 A transient/headroom.
- Load-step evidence must exercise both baseline->1 A and 1 A->baseline with <=100 µs reference current edges and waveform/reset criteria.
- USB priority + automatic battery takeover/restoration must be verified at representative high/mid/low battery voltages.
- Backfeed into upstream USB is prohibited.
- Low-voltage first-reference policy: cutoff 2.70 V ±0.05 V, no deliberate operation below 2.50 V, recovery at >=3.00 V ±0.05 V or valid USB.
- Thermal validation uses manufacturer-derived limits; MJ1 charge 0–45 °C, discharge -20–60 °C, MP2636 Tj <=125 °C during accepted operation. Final regulator/inductor/protection limits must be frozen before V4/V6.
- No-reset transfer is the reference target and remains `[UNVALIDATED]` pending IHAP-55 physical evidence.

## Evidence captured

- Owned holder is marked for 18650 use and has red/black leads. User-measured maximum useful cell length with spring fully compressed: approximately 70 mm; user-measured maximum cell diameter/width: approximately 18 mm. Physical fit remains `[UNVALIDATED]` until cell receipt and downstream validation.
- Owned charger board exposes `B+`, `B-`, `OUT+`, and `OUT-`; `4056E` and `8205A` markings were observed, while the separate protection-controller identity remains `[UNVALIDATED]`.
- `IHAP49-CHARGER-C0-C1-01/run-record.md` records C0/C1: in-circuit R3 measurement inconclusive; legacy 5 V / 1.55 A USB-A-to-C source produced VIN 4.95 V and unloaded B/OUT about 4.19/4.18 V; tested C-to-C fast-charge source did not produce usable charger-board input.

## Implementation / validation handoff

IHAP-55 owns the fabricated-board implementation and all mandatory physical evidence defined by `validation-plan.md`, including:

- MP2636 implementation or explicitly reviewed supersession plus regulated 5 V post-stage;
- USB-C CC/ESD/input current limiting;
- cell-side over-current and reverse-polarity implementation;
- NTC network and fault simulation;
- charging/current-limit/system-priority verification;
- numeric thermal acceptance table;
- 5 V / 3.3 V rail and bidirectional 1 A load-step capture;
- high/mid/low battery source transfer/restoration;
- numeric low-voltage cutoff/recovery;
- quantitative measurements transferred from ADR-0001/0002/**0003**/0004/0005;
- measured backup runtime and final board-level BOM/replication cost.

Canonical risk dossiers are **R-012** and **R-013**. Their treatments are **Proposed**, not Approved/Implemented/Verified, until explicit Project Owner treatment approval and downstream evidence exist. Residual risk remains Pending Evidence.

IHAP-51 owns holder retention, battery accessibility and enclosure/serviceability. IHAP-50 owns the final connection matrix.

## Planning autonomy boundary

Planning calculations indicate approximately 12–20 h for a 3.5 Ah-class cell, with roughly 16 h as a central estimate under the current load model. **Autonomy remains `[UNVALIDATED]` until measured on the fabricated custom implementation.**

## Runbooks / plans

- `validation-plan.md` — mandatory implementation-validation contract consumed by IHAP-55.
- `downstream-contracts.md` — downstream ownership and requirements.
- `custom-pcb-power-contract.md` — accepted electrical contract.
- `charger-characterization-runbook.md` — staged runbook for the owned 4056E board.
- `IHAP49-CHARGER-C0-C1-01/run-record.md` — executed C0/C1 evidence.

## Approval boundary

On **2026-09-07**, the Project Owner explicitly approved **ADR-0007 and PR #34**. That approval covers the architectural decision; it does **not** by itself approve the later R-012/R-013 treatment lifecycle states or establish safety, certification, production readiness, validated no-reset transfer or measured autonomy.
