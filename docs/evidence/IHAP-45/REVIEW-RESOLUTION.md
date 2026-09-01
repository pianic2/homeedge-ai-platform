# IHAP-45 Review Resolution

**Date:** 2026-07-16  
**Scope:** resolution of pre-PR review findings  
**Decision authority:** Project Owner

## Resolved findings

| Severity | Finding | Resolution |
|---|---|---|
| BLOCKER | IHAP-45 commits were accidentally present on `main`, preventing a meaningful PR | the complete state was preserved on a backup/recovery branch and `main` was restored to the pre-IHAP-45 commit before opening the PR |
| MAJOR | generated ESP-IDF `sdkconfig` and `sdkconfig.old` polluted the diff | both files were removed; the harness `.gitignore` now excludes them; `sdkconfig.defaults` remains the intentional source |
| MAJOR | the stable sensor decision was not recorded in an ADR | ADR-0002 records DHT11 as the standard indoor profile, BME280 as the precision / extended-environment profile and DHT22 as not selected |
| MAJOR | placement and enclosure bias lacked a canonical Risk Record | R-011 and proposed treatment RT-R011-01 were added with inverse ADR traceability and IHAP-50/IHAP-51 coordination |
| MINOR | BME280 was described only as a fallback | terminology now distinguishes its primary specialized profile from its secondary procurement-fallback role |

## Remaining boundaries

- absolute accuracy remains `[UNVALIDATED]` because no independent reference instrument was used;
- R-011 remains active and RT-R011-01 remains `Proposed`;
- pressure remains outside the MVP measurement contract;
- raw serial and per-sample telemetry remain local-only;
- Jira and Confluence were not modified during this correction tranche.
