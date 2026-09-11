# IHAP-49 — Execution Status

**Lifecycle reconciled:** 2026-09-11 during IHAP-55 startup review.

- Jira IHAP-49: **Completata**; PR #34 merged 2026-09-07 at `fb5188a615bc9a1b55bbea65863e64a4ad22f548`.
- ADR-0007: **Accepted baseline 2026-09-07**.
- IHAP-56: **Completata**.
- PR #35: **merged 2026-09-10** at `629ff78965a20481cf68954d6bcb8ac865fc27c2`.
- IHAP-56 amendment + RT-R012-01 / RT-R013-01: **Proposed; not Project Owner approved**.
- IHAP-55: **In corso** from 2026-09-11 under explicit Project Owner authorization; branch `ihap-55-integrated-modular-edge-pcb`.

## Accepted baseline preserved

Regulated 5 V USB-C normal source; LG MJ1 backup only; custom core PCB; MP2636 first direction plus downstream 5 V regulation/reviewed equivalent; 5 V SYS 4.75–5.25 V; >=0.5 A continuous **across accepted battery and valid USB-input ranges**; >=1 A headroom; USB priority/takeover/backfeed prohibition; no-reset target `[UNVALIDATED]`; electrical/mechanical reverse-insertion prevention; quantitative ownership transfer from ADR-0001/0002/0004/0005.

## Proposed remediation overlay remains Proposed

Source-side over-current/upstream-segment treatment; NTC fault-state tests; numeric thermal + Tj method; ILIM/V14; 3.3 V dynamic criteria; bidirectional V7; high/mid/valid-low V8/V9 with cutoff margin, quantified backfeed and zero-reset restoration criterion; numeric V10; V13 installed path; V15 USB absent/present; ADR-0003 transfer extension.

None of these later controls inherits approval from PR #34, PR #35 merge, IHAP-56 closure or IHAP-55 execution start.

## Post-merge reconciliation rule

The pre-merge review-gate wording captured in the IHAP-49 evidence package was historically correct before PR #35 merged. Any residual sentence in that package saying `PR #35 remains blocked`, `PR #35 must not merge`, `IHAP-56 is still in review`, or `IHAP-55 remains blocked by IHAP-56` is a stale workflow snapshot and is superseded for lifecycle/workflow interpretation by:

1. the actual merged PR #35 state;
2. Jira IHAP-56 = Completata;
3. Jira IHAP-55 = In corso; and
4. `docs/evidence/IHAP-49/ihap-56-post-merge-reconciliation.md`.

This supersession changes **workflow/lifecycle state only**. It does not change the Accepted-vs-Proposed technical boundary.