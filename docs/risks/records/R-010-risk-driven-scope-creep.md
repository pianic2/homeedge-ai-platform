# R-010 — Risk-Driven Scope Creep

**Risk ID:** R-010  
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
  risk_id: R-010
  document_type: living_risk_record
  runtime_changes_allowed: false
  orphan_status: not_orphan
-->

## 1. Risk Statement

There is a risk that treatment of an in-MVP risk is interpreted as approval to add new features or capabilities outside the current MVP.

## 2. Source Trigger and Scope

Risk analysis naturally proposes controls, but proposals are not implementation commitments or scope decisions.

In scope: risk records, Product Vision, Jira backlog, future tasks and stakeholder summaries.  
Out of scope: approving or implementing FUTURE/OUT OF MVP capability through this record.

## 3. Current Assessment

| Field | Value | Rationale |
|---|---|---|
| Category | Documentation / Compliance | Scope-governance risk |
| Likelihood | Medium | Treatment language naturally suggests future work |
| Impact | High | Silent expansion undermines MVP discipline |
| Residual risk | High | Every new treatment can reintroduce pressure |
| Decision state | Pending Project Owner | No residual-risk decision is inferred |

## 4. Existing Controls

| Control | Evidence | Coverage | Limitation |
|---|---|---|---|
| MVP/FUTURE/OUT OF MVP boundaries | `docs/product/product-vision.md` | Full as scope policy | Requires review on each proposal |
| Project Owner approval authority | `docs/governance/scrum-governance-dor-dod.md` | Full as workflow governance | Does not automatically prevent backlog expansion |

## 5. Risk Treatment

### RT-R010-01 — Avoid implicit scope expansion through risk treatment

**Strategy:** Avoid  
**Lifecycle status:** Proposed  
**Treatment owner:** Project Owner / governance review  
**Jira coordination:** Not required — governance gate  
**Related ADRs:** None  
**Next review trigger:** A treatment proposes runtime work, a new Jira task, an ADR or a change to MVP/FUTURE/OUT OF MVP.

Planned actions:

- mark treatments as proposals until approved;
- require a separate Jira task for implementation;
- require Project Owner approval for scope changes;
- update canonical MVP boundaries before implementing newly admitted capability;
- show future treatments as `FUTURE` or `[UNVALIDATED]`.

**Remaining exposure:** Pressure to add attractive controls remains and must be reassessed when new work is proposed.

### Source and Evidence Register

| ID | Source | Verification | Checked on | Limitations |
|---|---|---|---|---|
| SRC-01 | `docs/product/product-vision.md` | Verified | 2026-07-12 | Requires explicit change governance |
| SRC-02 | `docs/governance/scrum-governance-dor-dod.md` | Verified | 2026-07-12 | Workflow governance only |

### Evidence and Effectiveness

| Evidence | Expected result | Actual result | Status |
|---|---|---|---|
| EV-01 | No treatment is implemented as scope without a separate approved task | Future reviews pending | `[UNVALIDATED]` |

**Effectiveness:** Pending Evidence  
**Project Owner decision required:** Yes

## 6. Traceability

| Relationship | Link | Rule |
|---|---|---|
| Jira review task | IHAP-40 | Record migration only |
| Jira treatment task | Not required | Scope gate is sufficient |
| Related ADR | None | A future ADR cannot expand MVP by itself |

## 7. Stakeholder Visibility

```text
Risk treatment proposals do not expand MVP scope. New implementation requires a separate task, reviewed evidence and Project Owner decision.
```

## 8. Assessment History

| Date | Change | Treatment | Decision |
|---|---|---|---|
| 2026-07-12 | Legacy Reject proposal reclassified under IHAP-39 | RT-R010-01 Avoid / Proposed | Pending |

## 9. Review Notes

```text
[x] Treatment starts as Proposed.
[x] Avoid replaces the obsolete Reject treatment label.
[x] No implementation commitment is created.
[x] Orphan check passed through a governance treatment.
[x] MVP boundaries remain unchanged.
```