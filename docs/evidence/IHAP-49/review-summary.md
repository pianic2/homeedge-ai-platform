# IHAP-49 — Review and Acceptance Summary

## Accepted Project Owner decision — PR #34 baseline

IHAP-49 closed the **power architecture decision** rather than forcing a temporary breakout-stack implementation.

Accepted on 2026-09-07:

- normal source: **regulated 5 V USB-C**;
- battery role: **backup only** for blackout/cable-input interruption;
- selected cell: **LG INR18650-MJ1**, EAN/GTIN `8438493099829`, flat-top unprotected 18650;
- final hardware direction: **one custom modular core PCB**;
- preferred first charger/power-path/battery-boost PMIC candidate: **MPS MP2636GR-P**;
- explicit downstream regulated 5 V stage or reviewed equivalent topology required;
- battery CV target: **4.2 V**;
- nominal charge-current target: **~1.0 A**;
- reference USB input: **5 V, >=1.5 A available/advertised**;
- product SYS target: **5.0 V regulated, >=0.5 A continuous across the accepted battery range and valid USB-input range, >=1.0 A transient/headroom**;
- USB priority + automatic battery takeover;
- backfeed into upstream USB prohibited;
- **no-reset transfer is the reference target** and remains `[UNVALIDATED]`;
- NTC battery-temperature monitoring required;
- reverse insertion must be prevented electrically or mechanically; procedure/labels alone are insufficient;
- accepted quantitative power ownership transfer covers ADR-0001/0002/0004/0005;
- multi-day battery-only operation is not an MVP requirement;
- planning autonomy remains ~12–20 h / ~16 h central and `[UNVALIDATED]`.

## Proposed IHAP-56 remediation amendment — not yet Project Owner approved

Post-merge review identified additional controls and verification detail. These are **Proposed**, not part of the 2026-09-07 acceptance record:

- RT-R012-01 source-side over-current interruption ahead of every holder/service conductor claimed as protected, with explicit residual-segment handling when any conductor precedes the interruption element;
- mandatory NTC normal/hot/cold/open/short functional verification;
- manufacturer-derived numeric thermal PASS/FAIL limits plus a justified MP2636 junction-temperature/derating method;
- worst-case ILIM <=1.50 A plus V14 combined node+charging source-limit/system-priority verification;
- component-derived 3.3 V steady/transient PASS criteria;
- bidirectional V7 baseline↔1 A with <=100 µs current edges;
- V8/V9 high/mid/valid-low battery transfer/restoration, including loaded margin above cutoff, quantified backfeed and explicit zero restoration-attributable reset/brownout for proposed no-reset effectiveness verification;
- numeric V10 cutoff/recovery/hysteresis policy;
- V13 verification through every actual/production-identical conductor claimed as source-side protected;
- V15-A/V15-B electrical reverse-blocking tests with USB absent and USB present when electrical blocking is used;
- proposed extension of quantitative ownership transfer to ADR-0003 / reed-current work.

RT-R012-01 and RT-R013-01 remain **Proposed**. ADR-0007 acceptance does not approve those later treatment details or accept residual risk.

## Closure / regression matrix

`docs/evidence/IHAP-49/ihap-56-closure-matrix.md` is the review matrix for PR #35. For each material requirement it records:

`requirement → Accepted/Proposed state → canonical source/owner → downstream consumer → validation/evidence → approval boundary`.

The 2026-09-09 closure sweep reconciles **all 16 changed PR files** against this matrix before the next external review. This is specifically intended to prevent another incremental patch loop where a local finding is fixed but a dependent contract/risk/validation surface drifts.

## Procurement direction

- LG MJ1 cells: retain the selected direction;
- existing holder: retain, no replacement purchase at the decision stage;
- existing 4056E: bench/control evidence only;
- TPS61023/TPS2116/additional charger/boost/mux breakouts: do not purchase solely to emulate the final custom PCB without a specific blocker and Project Owner approval.

## Why the 4056E gaps no longer block the architectural decision

The owned 4056E module was characterized enough to bound its use: `4056E` and `8205A` were observed, the protection-controller identity remains unknown, legacy USB-A-to-C input sanity passed, tested C-to-C input did not work, and R3 in-circuit measurement was inconclusive. The module is rejected as the final reference implementation, so unresolved RPROG/protection-controller details are inventory limitations rather than architecture-decision blockers.

## Downstream handoff boundary

### Accepted IHAP-55 baseline

IHAP-55 owns schematic/layout/DFM, MP2636 implementation or reviewed supersession, downstream regulated 5 V stage, 3.3 V regulator, USB-C input/CC implementation, NTC implementation, accepted reverse-polarity control, PCB fabrication/bring-up, accepted 0.5 A endpoint-range / 1 A headroom tests, USB loss/restoration/backfeed checks, quantitative power work transferred from ADR-0001/0002/0004/0005, measured backup runtime and final custom-board BOM/cost.

### Proposed additions after approval only

Source-side over-current implementation/V13, upstream residual-segment control, mandatory NTC fault-state verification, numeric thermal/junction/low-voltage criteria, 3.3 V dynamic criteria, quantified backfeed, V14/V15, strengthened bidirectional V7, high/mid/valid-low V8/V9 and ADR-0003 ownership transfer are the IHAP-56 **Proposed** overlay. IHAP-55 must not consume them as accepted gates until the Project Owner approves the amendment/treatment scope.

IHAP-50 owns the connection matrix. IHAP-51 owns enclosure, holder retention and serviceability. IHAP-57 coordinates R-012/R-013 lifecycle/effectiveness only after explicit treatment approval and downstream evidence.

## Review provenance

Traceable review evidence:

| Review artifact | Reviewer / authority | Target | Outcome |
|---|---|---|---|
| PR #34 review | `chatgpt-codex-connector[bot]` advisory reviewer | original IHAP-49 branch / PR #34 | Material findings remediated before the accepted merge; later post-merge review exposed additional gaps |
| Project Owner approval | Project Owner | ADR-0007 / PR #34 | Authorized 2026-09-07 baseline acceptance, merge and IHAP-49 completion; not downstream physical evidence and not later treatment approval |
| PR #35 Codex pass 1 | `chatgpt-codex-connector[bot]` | pre-remediation PR #35 head `fa2f3842c9` | 8 P1/P2 findings; remediated |
| PR #35 Codex pass 2 | `chatgpt-codex-connector[bot]` | commit `214eac063c` | 6 P1/P2 findings; remediated |
| PR #35 Codex pass 3 | `chatgpt-codex-connector[bot]` | later IHAP-56 head | 8 further P1/P2 findings: upstream holder fault coverage, reversed insertion with USB present, junction-temperature method, accepted 0.5 A range regression, low-transfer/cutoff overlap, qualitative backfeed, missing 3.3 V criteria, and one-orientation-only USB-C validation |
| Global closure sweep | author remediation pass | all 16 PR #35 changed surfaces + canonical risk model | Accepted/Proposed matrix created; all 8 pass-3 findings and dependent surfaces remediated together before rerunning review |
| Final latest-head review | PR #35 review agent | latest head after closure sweep | **Pending**; PR #35 must not merge until no unresolved blocking finding remains |

## Author self-check by lane — not independent PASS evidence

| Lane | Author check before external review |
|---|---|
| Power Electronics | accepted MP2636/post-regulator and 0.5 A range architecture is distinct from Proposed source-side/validation additions |
| Battery / Li-ion boundary | unprotected-cell exposure is explicit; V13 never overclaims a segment before the interruption element; V15 covers USB absent/present when electrical blocking is proposed |
| Hardware Compatibility | 5 V / 3.3 V domains and modular sensor boundaries remain aligned with accepted hardware ADRs; V2 covers both DUT Type-C orientations |
| Testing & Evidence | accepted V1–V12 baseline is distinguished from Proposed strengthening; low transfer has cutoff margin; backfeed and 3.3 V criteria are measurable |
| Thermal Evidence | proposed MP2636 Tj criterion requires a justified junction estimate/derived case ceiling rather than package-temperature substitution |
| Security / Privacy | no new sensing or data collection scope is introduced |
| Architecture Regression | PR #34 accepted product direction is preserved; post-acceptance amendments do not inherit earlier approval |
| Cost Governance | redundant breakout procurement remains rejected; final cost requires real IHAP-55 evidence |
| Source of Truth / ADR Conformance | R-012/R-013 use canonical categories and inverse `Partially mitigates` effects; treatment states remain Proposed; closure matrix routes state consistently |

## Project Owner outcome and current gate

On **2026-09-07**, the Project Owner explicitly approved **ADR-0007 and PR #34**. PR #34 merged and Jira IHAP-49 moved to Completata.

IHAP-56 does not revoke that product decision. It remediates post-merge documentation/protection/risk-traceability findings while preserving the approval boundary. **PR #35 remains blocked from merge and IHAP-55 remains blocked from execution until the newest-head independent review reports no unresolved blocking findings and the Proposed treatment/amendment decision boundary is explicitly resolved.**
