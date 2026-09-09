# IHAP-56 — Closure / Regression Matrix

**Purpose:** one canonical review matrix for PR #35. It separates the 2026-09-07 Project Owner-approved ADR-0007 / PR #34 baseline from post-merge IHAP-56 treatment and validation proposals. No Proposed row may be represented as Accepted until explicit Project Owner approval exists.

## Decision-state invariants

| Requirement / control | State | Canonical owner / source | Downstream consumer | Validation / evidence | Approval boundary |
|---|---|---|---|---|---|
| 5 V USB-C normal source | **Accepted** | ADR-0007 / PR #34 | IHAP-55 | V2 | PO approval 2026-09-07 |
| LG INR18650-MJ1 1S backup only | **Accepted** | ADR-0007 / PR #34 | IHAP-55 / IHAP-51 | V3/V5/V12 | PO approval 2026-09-07 |
| Custom modular core PCB | **Accepted** | ADR-0007 / PR #34 | IHAP-55 | schematic/layout/fabrication evidence | PO approval 2026-09-07 |
| MP2636 first direction + downstream regulated 5 V stage or reviewed equivalent | **Accepted** | ADR-0007 / PR #34 | IHAP-55 | V2/V5/V6 | PO approval 2026-09-07 |
| 5.0 V product SYS, 4.75–5.25 V steady state | **Accepted** | ADR-0007 / PR #34 | IHAP-55 | V2/V5/V6 | PO approval 2026-09-07 |
| >=0.5 A continuous capability across the accepted battery range and valid USB-input range | **Accepted** | ADR-0007 / PR #34 | IHAP-55 | V6 at relevant range endpoints | PO approval 2026-09-07 |
| >=1.0 A transient/headroom target | **Accepted** | ADR-0007 / PR #34 | IHAP-55 | V7 baseline step-up evidence | PO approval 2026-09-07 |
| USB priority, automatic backup takeover, prohibited backfeed | **Accepted** | ADR-0007 / PR #34 | IHAP-55 | V8/V9 baseline | PO approval 2026-09-07 |
| No-reset transfer | **Accepted target, UNVALIDATED** | ADR-0007 / PR #34 | IHAP-55 | V8 baseline; physical evidence required | PO approval 2026-09-07 |
| Deterministic restoration / no reset loops or source oscillation | **Accepted** | ADR-0007 / PR #34 | IHAP-55 | V9 baseline | PO approval 2026-09-07 |
| Reverse insertion: electrical blocking/protection or physical keying; procedure alone insufficient | **Accepted** | ADR-0007 / PR #34 | IHAP-55 / IHAP-51 | V1/V3 baseline | PO approval 2026-09-07 |
| NTC monitoring on custom board | **Accepted** | ADR-0007 / PR #34 | IHAP-55 | V4 baseline | PO approval 2026-09-07 |
| Quantitative ownership transfer from ADR-0001/0002/0004/0005 to IHAP-55 | **Accepted** | ADR-0007 / PR #34 | IHAP-55 | V11 baseline | PO approval 2026-09-07 |
| Cell-side over-current interruption ahead of all in-scope service wiring, or explicit separately controlled upstream exposure | **Proposed** | R-012 / RT-R012-01 | IHAP-55 | Proposed V13 + upstream-segment verification | Requires explicit PO treatment/amendment approval |
| NTC normal/hot/cold/open/short functional criteria | **Proposed** | R-012 / RT-R012-01 | IHAP-55 | Proposed V4 strengthening | Requires explicit PO treatment/amendment approval |
| Numeric thermal acceptance / justified junction-temperature method | **Proposed** | R-012 + R-013 treatments | IHAP-55 | Proposed thermal overlay | Requires explicit PO treatment/amendment approval |
| Numeric low-voltage cutoff/recovery/hysteresis | **Proposed** | R-012 / RT-R012-01 | IHAP-55 | Proposed V10 | Requires explicit PO treatment/amendment approval |
| Worst-case ILIM <=1.50 A + combined node/charging system-priority test | **Proposed** | R-013 / RT-R013-01 | IHAP-55 | Proposed V14 | Requires explicit PO treatment/amendment approval |
| Bidirectional <=100 us 1 A load step | **Proposed strengthening** | R-013 / RT-R013-01 | IHAP-55 | Proposed V7 strengthening | Requires explicit PO treatment/amendment approval |
| High/mid/low V8/V9 coverage + zero restoration-reset criterion | **Proposed strengthening** | R-013 / RT-R013-01 | IHAP-55 | Proposed V8/V9 strengthening | Requires explicit PO treatment/amendment approval |
| Quantified backfeed thresholds and two-condition upstream-port test | **Proposed strengthening** | R-013 / RT-R013-01 | IHAP-55 | Proposed V8/V9 | Requires explicit PO treatment/amendment approval |
| Electrical reverse blocking under reversed battery with USB absent **and present** | **Proposed strengthening** | R-012 / RT-R012-01 | IHAP-55 | Proposed V15-A/V15-B | Requires explicit PO treatment/amendment approval |
| 3.3 V component-derived rail limits in steady/transient/source-transfer tests | **Proposed strengthening** | R-013 / RT-R013-01 | IHAP-55 | Proposed V2/V5/V7/V8/V9 overlay | Requires explicit PO treatment/amendment approval |
| ADR-0003/reed-current ownership transfer extension | **Proposed** | IHAP-56 | IHAP-55 | Proposed V11 extension | Requires explicit PO approval or another accepted downstream assignment |

## Review invariants

1. `Accepted` means only the durable 2026-09-07 ADR-0007 / PR #34 decision evidence.
2. `Proposed` treatments and validation strengthening may be reviewed in PR #35 but do not inherit ADR status.
3. Risk Records use only the category vocabulary from `docs/risks/risk-model-baseline.md`.
4. Every ADR↔Risk relationship uses one allowed effect and has an inverse link.
5. V13 cannot claim protection for wiring located upstream of the interruption element.
6. No thermal PASS may use package/case temperature as a direct substitute for junction temperature without a documented conversion/derating method.
7. No `no backfeed` PASS is qualitative: Proposed strengthening defines measurable connector current/voltage limits.
8. 3.3 V validation uses the intersection of populated-component supply limits; ESP32-C3 3.0–3.6 V is the initial outer bound, with tighter downstream limits taking precedence.
9. USB-C-to-USB-C functional validation exercises both DUT plug orientations.
10. No merge until latest-head independent review has no unresolved blocking finding.

## Current review finding closure targets

| Finding | Required closure |
|---|---|
| Upstream holder faults | Proposed protection must be source-side of all in-scope wiring; otherwise upstream segment is explicitly uncovered and needs a separate control/verification before treatment can be approved/verified. |
| Reverse insertion while USB present | Proposed V15 split into USB-absent and USB-present bounded simulator cases. |
| MP2636 junction limit | Proposed thermal method requires a justified junction estimate or conservative case/board derating derived from datasheet thermal parameters, loss, layout and ambient. |
| 0.5 A accepted range | Restore accepted range qualifiers and exercise relevant battery/USB endpoints in V6. |
| Low transfer point vs cutoff | Proposed low V8/V9 point must maintain explicit margin above maximum cutoff under load; 2.80±0.05 V is retired. |
| Backfeed criterion | Proposed V8/V9 defines USB VBUS and upstream-current limits in disconnected and attached-unpowered-source conditions. |
| 3.3 V rail | Proposed overlay defines component-derived steady/transient limits in all relevant power tests. |
| USB-C orientations | Accepted V2 functionally tests C-to-C operation with both DUT plug orientations. |

This matrix is a review aid and decision-state router. It does not itself approve any Proposed treatment, control or residual risk.
