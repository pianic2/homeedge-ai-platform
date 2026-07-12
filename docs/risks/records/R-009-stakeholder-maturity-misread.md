# R-009 — Stakeholder Maturity Misread

**Risk ID:** R-009  
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
  risk_id: R-009
  document_type: living_risk_record
  runtime_changes_allowed: false
  orphan_status: not_orphan
-->

## 1. Risk Statement

There is a risk that stakeholders interpret Sprint 0 or target documentation as production-ready, commercial-ready, security-grade, safety-critical or otherwise completed capability.

## 2. Source Trigger and Scope

Stakeholders often consume short Jira and Confluence summaries before detailed technical evidence.

In scope: Confluence, Jira comments, README, PR summaries and demos.  
Out of scope: changing runtime maturity or admitting FUTURE capability into MVP.

## 3. Current Assessment

| Field | Value | Rationale |
|---|---|---|
| Category | Stakeholder Visibility / Claims | Interpretation of current project maturity |
| Likelihood | Medium | Summaries compress technical nuance |
| Impact | High | Misread maturity can misrepresent project state |
| Residual risk | High | Every new summary can reintroduce the risk |
| Decision state | Pending Project Owner | No residual-risk decision is inferred |

## 4. Existing Controls

| Control | Evidence | Coverage | Limitation |
|---|---|---|---|
| Stakeholder transparency policy | `docs/governance/stakeholder-transparency.md` | Full as policy | Requires repeated application |
| Report data and claim rules | `docs/governance/stakeholder-report-data-rules.md` | Full for reports | Summaries can still be written incorrectly |

## 5. Risk Treatment

### RT-R009-01 — Preserve the weakest accurate stakeholder maturity label

**Strategy:** Mitigate  
**Lifecycle status:** Proposed  
**Treatment owner:** Stakeholder / documentation review  
**Jira coordination:** Not required — existing policy and review  
**Related ADRs:** None  
**Next review trigger:** Any stakeholder report, demo, Jira evidence comment or public project summary is created.

Planned actions:

- use `TARGET`, `FUTURE`, `IN REVIEW`, `STAKEHOLDER REVIEW`, `OUT OF SCOPE` or `[UNVALIDATED]` precisely;
- avoid Done unless evidence and Project Owner approval exist;
- link technical evidence instead of copying it;
- block unsupported maturity and protection claims.

**Remaining exposure:** Stakeholder interpretation can still vary and requires recurring clarity review.

### Source and Evidence Register

| ID | Source | Verification | Checked on | Limitations |
|---|---|---|---|---|
| SRC-01 | `docs/governance/stakeholder-transparency.md` | Verified | 2026-07-12 | Requires recurring application |
| SRC-02 | `docs/governance/stakeholder-report-data-rules.md` | Verified | 2026-07-12 | Applies to stakeholder surfaces |

### Evidence and Effectiveness

| Evidence | Expected result | Actual result | Status |
|---|---|---|---|
| EV-01 | Every summary uses the weakest accurate label and links evidence | Future reviews pending | `[UNVALIDATED]` |

**Effectiveness:** Pending Evidence  
**Project Owner decision required:** Yes

## 6. Traceability

| Relationship | Link | Rule |
|---|---|---|
| Jira review task | IHAP-40 | Record migration only |
| Jira treatment task | Not required | Existing stakeholder governance is sufficient |
| Related ADR | None | No architectural decision required |

## 7. Stakeholder Visibility

```text
The project is in Sprint 0 and review states. Target or future capabilities remain [UNVALIDATED] until linked implementation and runtime evidence exists.
```

## 8. Assessment History

| Date | Change | Treatment | Decision |
|---|---|---|---|
| 2026-07-12 | Migrated to IHAP-39 treatment model | RT-R009-01 Proposed | Pending |

## 9. Review Notes

```text
[x] Treatment starts as Proposed.
[x] No new Jira task or ADR is required.
[x] Maturity labels remain evidence-bound.
[x] Orphan check passed through a governance treatment.
[x] Project Owner decision remains Pending.
```