# R-006 — Source-of-Truth Drift

**Status:** Draft  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Jira:** IHAP-16  
**Owner decision:** Pending Project Owner  
**Decision state:** Pending Project Owner  
**Risk type:** Documentation / Stakeholder Visibility  
**Source of truth:** This GitHub risk record until superseded by a later reviewed change.

<!--
AI_AGENT_METADATA:
  risk_id: R-006
  canonical_path: docs/risks/records/R-006-source-of-truth-drift.md
  risk_model: docs/risks/risk-model-baseline.md
  source_of_truth_policy: docs/governance/source-of-truth.md
  documentation_strategy: docs/governance/documentation-strategy.md
  risk_acceptance_authority: project_owner
  runtime_changes_allowed: false
  adr_created: false
  unvalidated_claim_marker: "[UNVALIDATED]"
-->

---

## 1. Risk Statement

There is a risk that GitHub, Jira, and Confluence drift into parallel truths because each surface contains project information but only some surfaces are authoritative for technical content.

---

## 2. Source Trigger

The project intentionally uses GitHub for technical truth, Jira for work state/evidence, and Confluence for stakeholder reports/navigation. This split is useful, but it creates divergence risk if technical content is copied instead of linked.

---

## 3. Affected Assets and Trust Boundary

| Area | Detail |
|---|---|
| Asset | GitHub docs, Jira issue descriptions/comments, Confluence stakeholder hub/reports. |
| Trust boundary | Technical truth -> tracking summary -> stakeholder summary. |
| Data involved | Scope, risk posture, maturity labels, evidence links, status summaries. |
| Stakeholder surface | High: stakeholders mainly read summaries first. |

---

## 4. Scoring

| Field | Value | Rationale |
|---|---|---|
| Likelihood | Medium | Multiple surfaces are used regularly and can become stale. |
| Impact | High | Divergence can mislead review, invalidate evidence, or weaken claim boundaries. |
| Residual risk | Medium | Existing policy reduces the risk, but every future update must keep links aligned. |
| Treatment proposal | Mitigate | Keep GitHub canonical, Jira evidence-linked, and Confluence summary/link-only. |
| Decision state | Pending Project Owner | No residual risk decision has been made. |

---

## 5. Existing Controls

- `source-of-truth.md` defines surface authority.
- `documentation-strategy.md` defines when to create/update docs.
- Stakeholder reports must summarize and link, not duplicate long-form technical docs.
- Review agents are configured to detect source-of-truth divergence.

---

## 6. Evidence Gap

Missing or future evidence:

- continued link correctness after every PR;
- stakeholder reports aligned after merges;
- Jira comments pointing to current PR/document paths;
- review output for each governance movement.

---

## 7. Mitigation Proposal

Operational mitigation:

- update GitHub when technical truth changes;
- update Jira only for state/evidence links;
- update Confluence only for stakeholder summary/navigation;
- replace copied technical content with links;
- run Source of Truth Guardian before movement toward Stakeholder Review or Done.

---

## 8. Stakeholder Visibility

| Item | Rule |
|---|---|
| Risk summary | Show allowed. |
| Canonical technical docs | Link only. |
| Divergent copied text | Replace with link or update GitHub. |
| Status | Jira remains authoritative. |

Stakeholder-safe wording:

```text
GitHub remains the technical source of truth. Jira tracks work and evidence. Confluence summarizes and links for stakeholder navigation.
```
