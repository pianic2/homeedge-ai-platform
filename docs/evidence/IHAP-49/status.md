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
  - 5 V product SYS target 4.75–5.25 V with **>=0.5 A continuous across accepted battery and valid USB-input ranges** and >=1.0 A headroom target;
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

`ihap-56-closure-matrix.md` is now the cross-file regression router. Every material requirement is classified as Accepted or Proposed and mapped to its canonical owner, downstream consumer, validation/evidence and approval boundary.

### Accepted remediation of documentation/traceability defects

IHAP-56 must preserve and accurately propagate the already accepted PR #34 baseline, including explicit post-MP2636 regulated 5 V topology, reverse-insertion prevention, accepted 0.5 A battery/USB range capability, source/rail/headroom/transfer constraints and accepted ADR-0001/0002/0004/0005 ownership transfer.

### Proposed treatment / validation additions awaiting explicit Project Owner decision

- source-side over-current interruption ahead of every conductor claimed as protected; any segment before the element remains explicit residual exposure until separately controlled/verified;
- mandatory NTC normal/hot/cold/open/short functional validation;
- manufacturer-derived numeric thermal PASS/FAIL limits plus justified MP2636 junction-temperature/derating method;
- worst-case ILIM <=1.50 A + V14 combined source-limit/system-priority verification;
- component-derived 3.3 V steady/transient PASS criteria;
- bidirectional <=100 µs V7 strengthening;
- V8/V9 high/mid/valid-low battery strengthening, with low-point loaded margin above cutoff;
- quantified backfeed criteria for open and attached-unpowered upstream USB conditions;
- explicit restoration reset/brownout FAIL criterion for proposed no-reset effectiveness;
- numeric V10 low-voltage cutoff/recovery/hysteresis;
- V15-A/V15-B bounded electrical reverse-blocking tests with USB absent and present;
- ADR-0003/reed-current ownership transfer to IHAP-55.

These additions remain **Proposed** until explicitly approved. Physical custom-board behavior, no-reset transfer, treatment effectiveness, final current measurements and autonomy remain `[UNVALIDATED]`.

## Review gate

Codex review history on PR #35:

- pass on `fa2f3842c9`: 8 findings, remediated;
- pass on `214eac063c`: 6 findings, remediated;
- subsequent pass exposed **8 further P1/P2 boundary/verification findings**: upstream holder-fault coverage, reversed insertion with USB present, MP2636 junction verification method, accepted 0.5 A range regression, low transfer/cutoff overlap, qualitative backfeed criterion, missing 3.3 V PASS criteria and one-orientation-only USB-C validation.

The 2026-09-09 global closure sweep addresses all eight together across all **16 changed PR surfaces** and adds the closure/regression matrix instead of patching one review comment at a time.

**PR #35 remains blocked.** Required next gate: resolve all superseded/current review threads with traceable replies, run a fresh Codex/review-agent pass on the latest head, and merge only if that latest pass has no unresolved blocking finding. Even after a clean review, Proposed treatment/amendment lifecycle must not advance without explicit Project Owner approval. IHAP-55 remains blocked until the remediation/approval boundary is resolved.
