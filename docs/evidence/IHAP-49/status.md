# IHAP-49 — Execution Status

- Jira: **Completata**
- Original GitHub branch: `ihap-49-edge-power-subsystem-decision`
- Original pull request: **#34 — merged 2026-09-07**
- Merge commit on `main`: `fb5188a615bc9a1b55bbea65863e64a4ad22f548`
- ADR: **ADR-0007 — Accepted 2026-09-07**
- Post-merge remediation: **IHAP-56 / PR #35 — in review before merge**
- Project Owner decisions recorded:
  - normal regulated 5 V USB-C source;
  - LG INR18650-MJ1 1S backup only;
  - cost-first selection after minimum gates;
  - custom modular core PCB as final reference direction;
  - no redundant TPS61023/TPS2116 breakout procurement;
  - preferred first integrated PMIC direction: MP2636GR-P plus downstream regulated 5 V stage or reviewed equivalent topology.
- Owned 4056E breakout: **bench/control evidence only; rejected as final implementation**
- Custom PCB implementation / physical validation: **IHAP-55**
- Canonical power-risk effectiveness tracking: **IHAP-57**
- Enclosure / holder serviceability validation: **IHAP-51**
- Backup autonomy: **`[UNVALIDATED]` until IHAP-55 endurance run**
- Definitive assembled-board replication cost: **deferred to IHAP-55 / IHAP-17 reconciliation**

## Post-merge remediation boundary

PR #34 is historical acceptance evidence and remains merged. IHAP-56 exists because later review found documentation/protection/traceability regressions that must be corrected without rewriting the accepted product direction.

IHAP-56 requires:

- explicit post-MP2636 regulated 5 V stage in every power-tree/contract surface;
- cell-side over-current interruption for holder/BAT-net faults upstream of PMIC SYS limiting;
- electrical or physically keyed reverse-insertion prevention; procedure alone is insufficient;
- mandatory NTC hot/cold/open/short functional validation;
- canonical R-012/R-013 risk/treatment traceability;
- quantitative power ownership transfer from ADR-0001/0002/0003/0004/0005 to IHAP-55;
- removal of unsupported generic review PASS claims;
- clean post-remediation review before merge.

Physical custom-board behavior, no-reset transfer, treatment effectiveness, final current measurements and autonomy remain `[UNVALIDATED]` until IHAP-55/IHAP-57 evidence exists.
