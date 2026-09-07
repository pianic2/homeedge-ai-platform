# IHAP-49 — Review and Acceptance Summary

## Decision accepted by Project Owner

IHAP-49 closes the **power architecture decision** rather than forcing a temporary breakout-stack implementation.

Accepted reference contract:

- normal source: **regulated 5 V USB-C**;
- battery role: **backup only** for blackout/cable-input interruption;
- selected cell: **LG INR18650-MJ1**, EAN/GTIN `8438493099829`, flat-top unprotected 18650;
- final hardware direction: **one custom modular core PCB**;
- preferred first charger/power-path/battery-boost PMIC candidate: **MPS MP2636GR-P**;
- explicit downstream regulated 5 V stage or reviewed equivalent topology required;
- battery CV target: **4.2 V**;
- nominal charge-current target: **~1.0 A**;
- reference USB input: **5 V, >=1.5 A available/advertised**;
- product SYS target: **5.0 V regulated, >=0.5 A continuous, >=1.0 A transient/headroom**;
- USB priority + automatic battery takeover;
- backfeed into upstream USB prohibited;
- **no-reset transfer is the reference target** and remains `[UNVALIDATED]`;
- NTC battery-temperature monitoring and mandatory fault-state validation required;
- unprotected cell means system-level protection including cell-side over-current interruption is mandatory;
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

## Why the 4056E gaps no longer block the architectural decision

The owned 4056E module was characterized enough to bound its use:

- `4056E` and `8205A` observed;
- protection controller exists but exact identity/thresholds remain unknown;
- legacy 5 V USB-A-to-C input sanity passed;
- tested C-to-C fast-charge input did not work;
- R3 in-circuit measurement was inconclusive.

The module is **rejected as the final reference power implementation**, so unresolved RPROG/protection-controller details are inventory limitations, not blockers to the architecture decision.

## Implementation handoff

**IHAP-55 — Integrated Modular Edge PCB — Custom Mainboard Design and Prototype** owns:

- schematic/layout/DFM;
- MP2636 implementation or explicit reviewed supersession;
- downstream regulated 5 V stage;
- 3.3 V regulator;
- cell-side over-current interruption and rating rationale;
- USB-C input protection/CC implementation;
- NTC and reverse-polarity implementation;
- PCB fabrication/bring-up;
- mandatory NTC hot/cold/open/short functional verification;
- charge current / thermal evidence;
- 5 V / 3.3 V rail measurements;
- mandatory 0.5 A continuous and 1 A instrumented load-step tests;
- USB-to-battery switchover/restoration and backfeed checks;
- no-reset validation;
- quantitative load characterization transferred from ADR-0001/0002/0003/0004/0005;
- measured backup runtime;
- final custom-board BOM and replication cost.

IHAP-50 owns the connection matrix. IHAP-51 owns enclosure, holder retention and serviceability. IHAP-57 coordinates later R-012/R-013 treatment-effectiveness updates.

## Review provenance

The previous version of this document used generic lane-wide `PASS` declarations. Those declarations were **author-written summaries, not independent review evidence**, and are removed by IHAP-56.

Traceable review evidence currently consists of:

| Review artifact | Reviewer / authority | Target | Sources / observed evidence | Outcome |
|---|---|---|---|---|
| PR #34 review submission and inline findings | `chatgpt-codex-connector[bot]` advisory reviewer | PR #34 / pre-merge IHAP-49 branch | ADR-0007, validation plan, source register, owned-hardware evidence and related governance | Produced material P1/P2 findings; original findings were remediated before merge, then a later review pass exposed additional post-merge findings |
| Project Owner approval | Project Owner | ADR-0007 and PR #34 | Accepted decision/evidence package after requested remediation | Authorized ADR acceptance, PR merge and Jira completion; this is decision authority, not proof of downstream physical effectiveness |
| Post-merge remediation review | PR #35 review agents | IHAP-56 branch / PR #35 | Entire remediation diff plus canonical ADR/risk/governance sources | **Pending before merge**; PR #35 must not merge until no blocking findings remain |

## Author self-check by lane — not independent PASS evidence

The following is an **author checklist only**. It identifies the intended review lenses for PR #35 and must not be used to satisfy an independent review gate by itself.

| Lane | Author check before external review |
|---|---|
| Power Electronics | MP2636 pass-through is separated from regulated product SYS; post-regulator is explicit; cell-side protection is not confused with SYS limiting |
| Battery / Li-ion boundary | Unprotected-cell exposure is explicit; reverse insertion, NTC faults, over-current and low-voltage behavior remain treatment/verification items |
| Hardware Compatibility | 5 V / 3.3 V domains and modular sensor boundaries remain aligned with accepted hardware ADRs |
| Testing & Evidence | 0.5 A, 1 A waveform, NTC fault, transfer/backfeed, quantitative load and endurance tests are mandatory and `[UNVALIDATED]` until executed |
| Security / Privacy | No new sensing or data collection scope is introduced by the power remediation |
| Architecture Regression | Accepted product direction is preserved; remediation tightens constraints without silently redesigning the node |
| Cost Governance | Redundant breakout procurement remains rejected; final board-level cost is deferred to real IHAP-55 BOM evidence |
| Source of Truth / ADR Conformance | ADR-0007 links canonical R-012/R-013 treatments; Risk Records contain inverse links; Jira remains workflow/coordination only |

Independent PR #35 reviewers must report reviewer identity, target ref/commit, sources checked, observed evidence and finding severity/provenance in accordance with `docs/governance/ai-review-agents-policy.md`.

## Project Owner outcome and current gate

On **2026-09-07**, the Project Owner explicitly approved **ADR-0007 and PR #34**. PR #34 subsequently merged and Jira IHAP-49 moved to Completata.

IHAP-56 does not revoke that product decision. It corrects post-merge documentation/protection/risk-traceability findings. **PR #35 remains blocked from merge until the independent review pass reports no unresolved blocking findings.** Physical custom-board validation remains downstream and may supersede ADR-0007 only if evidence contradicts the accepted contract.
