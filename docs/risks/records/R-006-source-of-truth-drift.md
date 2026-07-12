# R-006 — Source-of-Truth Drift

**Risk ID:** R-006  
**Risk status:** Monitoring  
**Current assessment date:** 2026-07-12  
**Last reviewed:** 2026-07-12  
**Next review:** Event-driven  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Jira:** IHAP-40  
**Owner decision:** Pending

<!--
AI_AGENT_METADATA:
  issue: IHAP-40
  risk_id: R-006
  document_type: living_risk_record
  runtime_changes_allowed: false
  orphan_status: not_orphan
-->

## 1. Risk Statement

There is a risk that GitHub, Jira and Confluence diverge into parallel truths because each surface carries different project information.

## 2. Source Trigger and Scope

The project intentionally separates technical truth, workflow state and stakeholder summaries across three systems.

In scope: canonical documents, Jira evidence links, Confluence summaries and navigation.  
Out of scope: duplicating technical records in Jira or Confluence.

## 3. Current Assessment

| Field | Value | Rationale |
|---|---|---|
| Category | Documentation / Stakeholder Visibility | Cross-surface governance risk |
| Likelihood | Medium | Multiple surfaces are updated regularly |
| Impact | High | Divergence can mislead reviews and stakeholders |
| Residual risk | Medium | Existing policy reduces but cannot eliminate recurrence |
| Decision state | Pending Project Owner | No residual-risk decision is inferred |

## 4. Existing Controls

| Control | Evidence | Coverage | Limitation |
|---|---|---|---|
| Surface authority policy | `docs/governance/source-of-truth.md` | Full as governance | Does not automatically prevent stale links |
| Documentation strategy | `docs/governance/documentation-strategy.md` | Partial | Requires disciplined execution |
| Source of Truth Guardian | `docs/governance/ai-review-agents-policy.md` | Partial | Advisory review, not enforcement |

## 5. Risk Treatment

### RT-R006-01 — Monitor cross-surface source-of-truth alignment

**Strategy:** Monitor  
**Lifecycle status:** Proposed  
**Treatment owner:** Governance / documentation review  
**Jira coordination:** Not required — governance gate and issue evidence  
**Related ADRs:** None  
**Next review trigger:** A canonical document, Jira evidence link or Confluence stakeholder report changes.

Monitoring actions:

- keep technical truth in GitHub;
- use Jira for state, blockers and evidence links;
- use Confluence for summary and navigation only;
- run Source of Truth Guardian before stakeholder-facing movement;
- replace copied technical content with canonical links.

**Remaining exposure:** Drift can recur after any update across the three surfaces.

### Source and Evidence Register

| ID | Source | Verification | Checked on | Limitations |
|---|---|---|---|---|
| SRC-01 | `docs/governance/source-of-truth.md` | Verified | 2026-07-12 | Requires recurring application |
| SRC-02 | `docs/governance/documentation-strategy.md` | Verified | 2026-07-12 | Process evidence only |

### Evidence and Effectiveness

| Evidence | Expected result | Actual result | Status |
|---|---|---|---|
| EV-01 | Current links and summaries remain aligned after material changes | Future reviews pending | `[UNVALIDATED]` |

**Effectiveness:** Pending Evidence  
**Project Owner decision required:** Yes

## 6. Traceability

| Relationship | Link | Rule |
|---|---|---|
| Jira review task | IHAP-40 | Record migration only |
| Monitoring path | Governance lane review gate | Reassess on each trigger |
| Related ADR | None | No architectural decision required |

## 7. Stakeholder Visibility

```text
GitHub remains the technical source of truth. Jira tracks work and evidence. Confluence summarizes and links for stakeholder navigation.
```

## 8. Assessment History

| Date | Change | Treatment | Decision |
|---|---|---|---|
| 2026-07-12 | Converted to formal event-driven monitoring | RT-R006-01 Proposed | Pending |

## 9. Review Notes

```text
[x] Monitoring path and trigger are explicit.
[x] Treatment starts as Proposed.
[x] No duplicate technical truth was introduced.
[x] Orphan check passed through formal monitoring.
[x] Project Owner decision remains Pending.
```