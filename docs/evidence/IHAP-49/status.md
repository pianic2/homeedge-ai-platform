# IHAP-49 — Execution Status

- Jira: **Completata**
- Original GitHub branch: `ihap-49-edge-power-subsystem-decision`
- Original pull request: **#34 — merged 2026-09-07**
- Merge commit on `main`: `fb5188a615bc9a1b55bbea65863e64a4ad22f548`
- ADR: **ADR-0007 — Accepted baseline 2026-09-07**
- ADR post-acceptance amendment: **IHAP-56 additions Proposed; not yet Project Owner approved**
- Post-merge remediation: **IHAP-56 / PR #35 — in review before merge**
- Project Owner decisions recorded in the accepted baseline:
  - normal regulated 5 V USB-C source;
  - LG INR18650-MJ1 1S backup only;
  - cost-first selection after minimum gates;
  - custom modular core PCB as final reference direction;
  - no redundant TPS61023/TPS2116 breakout procurement;
  - preferred first integrated PMIC direction: MP2636GR-P plus downstream regulated 5 V stage or reviewed equivalent topology;
  - reverse insertion prevented electrically or mechanically; procedure alone insufficient;
  - accepted quantitative power ownership transfer from ADR-0001/0002/0004/0005 to IHAP-55.
- Owned 4056E breakout: **bench/control evidence only; rejected as final implementation**
- Custom PCB implementation / physical validation: **IHAP-55, blocked until IHAP-56 gate is resolved**
- Canonical power-risk treatment/effectiveness tracking: **R-012/R-013 + IHAP-57; RT-R012-01/RT-R013-01 Proposed**
- Enclosure / holder serviceability validation: **IHAP-51**
- Backup autonomy: **`[UNVALIDATED]` until downstream endurance evidence**
- Definitive assembled-board replication cost: **deferred to IHAP-55 / IHAP-17 reconciliation**

## Post-merge remediation boundary

PR #34 is historical acceptance evidence and remains merged. IHAP-56 exists because later review found documentation/protection/traceability regressions that must be corrected without rewriting the accepted product direction or inheriting the earlier approval event.

### Accepted remediation of documentation/traceability defects

IHAP-56 must preserve and accurately propagate the already accepted PR #34 baseline, including explicit post-MP2636 regulated 5 V topology, reverse-insertion prevention, accepted source/rail/headroom/transfer constraints and accepted ADR-0001/0002/0004/0005 ownership transfer.

### Proposed treatment / validation additions awaiting explicit Project Owner decision

- cell-side over-current interruption for holder/BAT-net faults upstream of PMIC SYS limiting and installed-path V13 verification;
- mandatory NTC normal/hot/cold/open/short functional validation;
- manufacturer-derived numeric thermal PASS/FAIL limits;
- worst-case ILIM <=1.50 A + V14 combined source-limit/system-priority verification;
- bidirectional <=100 µs V7 strengthening;
- V8/V9 high/mid/low battery strengthening, including explicit restoration reset/brownout FAIL criterion for proposed no-reset effectiveness;
- numeric V10 low-voltage cutoff/recovery/hysteresis;
- V15 bounded electrical reverse-blocking test when applicable;
- ADR-0003/reed-current ownership transfer to IHAP-55.

These additions remain **Proposed** until explicitly approved. Physical custom-board behavior, no-reset transfer, treatment effectiveness, final current measurements and autonomy remain `[UNVALIDATED]`.

## Review gate

The Codex pass on `214eac063c` found 6 additional P1/P2 issues. PR #35 remains blocked until all six are remediated, their threads are resolved, and a **new review on the latest head** returns with no unresolved blocking finding. No merge or IHAP-55 unblock occurs before that gate.
