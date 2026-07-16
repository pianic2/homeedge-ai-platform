# R-005 — Target Boundary Overclaim

**Risk ID:** R-005  
**Risk status:** Under Treatment  
**Current assessment date:** 2026-07-12  
**Last reviewed:** 2026-07-12  
**Next review:** Event-driven  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Jira:** IHAP-40  
**Owner decision:** Pending

<!--
AI_AGENT_METADATA:
  issue: IHAP-40
  risk_id: R-005
  document_type: living_risk_record
  runtime_changes_allowed: false
  orphan_status: not_orphan
-->

## 1. Risk Statement

There is a risk that current target backend, mobile, cloud, schema or AI boundaries are presented as implemented MVP runtime without traceable evidence.

## 2. Source Trigger and Scope

The repository contains target directories and architecture direction that are not runtime proof.

In scope: maturity wording for current repository and stakeholder surfaces.  
Out of scope: implementing target services or admitting FUTURE capabilities into the MVP.

## 3. Current Assessment

| Field | Value | Rationale |
|---|---|---|
| Category | Compliance / Documentation | Evidence and maturity risk |
| Likelihood | High | Directory names and diagrams are easily mistaken for implementation |
| Impact | High | Overclaiming weakens trust and source-of-truth correctness |
| Residual risk | High | Runtime evidence is absent for target boundaries |
| Decision state | Pending Project Owner | No residual-risk decision is inferred |

## 4. Existing Controls

| Control | Evidence | Coverage | Limitation |
|---|---|---|---|
| TARGET and `[UNVALIDATED]` policy | `docs/governance/source-of-truth.md` | Full as documentation governance | Requires consistent application |
| Stakeholder claim boundaries | `docs/governance/stakeholder-report-data-rules.md` | Full for reports | Cannot prove runtime implementation |

## 5. Risk Treatment

### RT-R005-01 — Enforce evidence-backed maturity labels

**Strategy:** Mitigate  
**Lifecycle status:** Proposed  
**Treatment owner:** Governance / documentation review  
**Jira coordination:** Not required — existing policy and review  
**Related ADRs:** None  
**Next review trigger:** Any technical or stakeholder surface describes backend, mobile, cloud, schema or AI capability.

Planned actions:

- use `TARGET` for architecture direction;
- use `FUTURE` for deferred capability;
- preserve `[UNVALIDATED]` until implementation and test evidence exists;
- never treat directories or diagrams as runtime proof.

**Remaining exposure:** Reviewers may miss an overclaim; runtime status remains evidence-dependent.

### Source and Evidence Register

| ID | Source | Verification | Checked on | Limitations |
|---|---|---|---|---|
| SRC-01 | `docs/governance/source-of-truth.md` | Verified | 2026-07-12 | Governance evidence only |
| SRC-02 | `docs/governance/stakeholder-report-data-rules.md` | Verified | 2026-07-12 | Applies to stakeholder material |

### Evidence and Effectiveness

| Evidence | Expected result | Actual result | Status |
|---|---|---|---|
| EV-01 | Every unproven capability uses the weakest accurate maturity label | Not executed for future surfaces | `[UNVALIDATED]` |

**Effectiveness:** Pending Evidence  
**Project Owner decision required:** Yes

## 6. Traceability

| Relationship | Link | Rule |
|---|---|---|
| Jira review task | IHAP-40 | Record migration only |
| Jira treatment task | Not required | Existing governance is sufficient |
| Related ADR | None | No architectural decision is introduced |

## 7. Stakeholder Visibility

```text
Backend, mobile, cloud, schema and AI areas are target or future boundaries unless linked implementation and runtime evidence prove otherwise.
```

## 8. Assessment History

| Date | Change | Treatment | Decision |
|---|---|---|---|
| 2026-07-12 | Migrated to IHAP-39 treatment model | RT-R005-01 Proposed | Pending |

## 9. Review Notes

```text
[x] Treatment starts as Proposed.
[x] Policy controls are not presented as runtime evidence.
[x] No task or ADR is required.
[x] Orphan check passed through a governance treatment.
[x] No target boundary was admitted into the MVP.
```