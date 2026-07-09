# R-009 — Stakeholder Maturity Misread

**Status:** Draft  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Jira:** IHAP-16  
**Owner decision:** Pending Project Owner  
**Decision state:** Pending Project Owner  
**Risk type:** Stakeholder Visibility / Claims  
**Source of truth:** This GitHub risk record until superseded by a later reviewed change.

<!--
AI_AGENT_METADATA:
  risk_id: R-009
  canonical_path: docs/risks/records/R-009-stakeholder-maturity-misread.md
  risk_model: docs/risks/risk-model-baseline.md
  stakeholder_transparency: docs/governance/stakeholder-transparency.md
  stakeholder_report_rules: docs/governance/stakeholder-report-data-rules.md
  risk_acceptance_authority: project_owner
  runtime_changes_allowed: false
  adr_created: false
  unvalidated_claim_marker: "[UNVALIDATED]"
-->

---

## 1. Risk Statement

There is a risk that stakeholders interpret Sprint 0 documentation as production-ready, commercial-ready, security-grade, safety-critical, alarm-grade, antifurto, certified, or protective system maturity because summaries can compress technical nuance too much.

---

## 2. Source Trigger

The project intentionally exposes progress through Jira and Confluence for stakeholder visibility. This is useful, but short summaries can accidentally upgrade target, planned, draft, or `[UNVALIDATED]` claims into perceived completed capability.

---

## 3. Affected Assets and Trust Boundary

| Area | Detail |
|---|---|
| Asset | Confluence stakeholder hub, reports, Jira comments, PR summaries, README claims. |
| Trust boundary | Technical evidence -> stakeholder-readable summary. |
| Data involved | Status labels, maturity wording, risk summaries, evidence links. |
| Stakeholder surface | Directly affected. |

---

## 4. Scoring

| Field | Value | Rationale |
|---|---|---|
| Likelihood | Medium | Stakeholders read summaries first, not full GitHub documents. |
| Impact | High | Misread maturity weakens claim governance and can misrepresent project state. |
| Residual risk | High | Risk persists whenever reports or demos are created. |
| Treatment proposal | Mitigate | Use weakest accurate labels and preserve `[UNVALIDATED]` across stakeholder surfaces. |
| Decision state | Pending Project Owner | No residual risk decision has been made. |

---

## 5. Existing Controls

- Stakeholder transparency defines GitHub/Jira/Confluence roles.
- Stakeholder report data rules define allowed, linked, redacted, and blocked content.
- Claim boundaries block forbidden production, commercial, security-grade, safety, alarm, antifurto, access-control, intrusion-detection, and protection wording.

---

## 6. Evidence Gap

Missing or future evidence:

- every Confluence report review after each merge;
- explicit `[UNVALIDATED]` preservation in reports;
- link checks from report to PR/Jira/GitHub;
- reviewer confirmation that stakeholder wording remains safe.

---

## 7. Mitigation Proposal

Every stakeholder surface should:

- use `TARGET`, `FUTURE`, `IN REVIEW`, `STAKEHOLDER REVIEW`, `OUT OF SCOPE`, or `[UNVALIDATED]` precisely;
- avoid “done” unless evidence supports it and Project Owner approves;
- link GitHub/Jira instead of copying long technical content;
- block maturity and protection claims.

---

## 8. Stakeholder Visibility

| Item | Rule |
|---|---|
| Risk summary | Show allowed. |
| Claim maturity | Must use weakest accurate label. |
| Technical depth | Link only. |
| Forbidden maturity/protection wording | Blocked. |

Stakeholder-safe wording:

```text
The project is in Sprint 0 / review state. Target or future capabilities remain [UNVALIDATED] until linked implementation and runtime evidence exists.
```
