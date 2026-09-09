# IHAP-49 — Execution Status

- Jira: **Completata**
- Original pull request: **#34 — merged 2026-09-07** (`fb5188a615bc9a1b55bbea65863e64a4ad22f548`)
- ADR: **ADR-0007 — Accepted baseline 2026-09-07**
- Post-acceptance IHAP-56 amendment/treatments: **Proposed; not yet Project Owner approved**
- Post-merge remediation: **IHAP-56 / PR #35 — in review before merge**
- IHAP-55 custom PCB execution: **blocked until IHAP-56 gate is resolved**
- R-012 / R-013 treatments: **RT-R012-01 / RT-R013-01 Proposed**; physical effectiveness `[UNVALIDATED]`

## Accepted baseline preserved

- regulated 5 V USB-C normal source;
- LG INR18650-MJ1 backup only;
- custom modular core PCB direction;
- MP2636GR-P first direction + downstream regulated 5 V stage/reviewed equivalent;
- 5 V SYS 4.75–5.25 V, >=0.5 A continuous **across accepted battery and valid USB-input ranges**, >=1.0 A headroom target;
- USB priority / automatic takeover / prohibited backfeed / no-reset target `[UNVALIDATED]`;
- reverse insertion prevented electrically or mechanically, procedure alone insufficient;
- accepted quantitative ownership transfer from ADR-0001/0002/0004/0005.

## Proposed IHAP-56 overlay

- source-side over-current interruption with explicit uncovered-segment handling;
- NTC normal/hot/cold/open/short verification;
- numeric thermal criteria + justified MP2636 junction estimate/derating;
- ILIM <=1.50 A + V14;
- component-derived 3.3 V criteria;
- bidirectional <=100 µs V7;
- high/mid/valid-low V8/V9 with loaded cutoff margin, quantified backfeed and zero-reset restoration criterion;
- numeric V10;
- V13 installed/production-identical path;
- V15-A/V15-B with USB absent/present;
- ADR-0003 ownership extension.

## Review gate

The 2026-09-09 global closure sweep reconciled all **16 changed PR files** against `ihap-56-closure-matrix.md` and addressed the eight latest P1/P2 findings together. **Author remediation is frozen now.** No additional document changes should occur before the next independent review unless needed to fix a newly reported finding or state/tooling inconsistency.

PR #35 remains blocked until prior threads are traceably resolved and a fresh latest-head Codex/review-agent pass reports no unresolved blocking finding. A clean technical review does not itself approve the Proposed treatments; lifecycle changes still require explicit Project Owner approval.
