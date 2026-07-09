# Risk Assessment — <Short Title>

**Status:** Draft / In Review / Accepted / Deferred / Rejected  
**Date:** YYYY-MM-DD  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Jira:** IHAP-XX  
**PR:** <link when available>  
**Owner decision:** Pending / Accepted / Deferred / Rejected

<!--
AI_AGENT_METADATA:
  issue: IHAP-31
  document_type: risk_assessment_template
  canonical_path: docs/templates/risk-assessment.md
  source_of_truth: github_versioned_repository_documentation
  template_output_target: future_docs_risks_records_only_when_explicitly_approved
  task_scope: documentation_governance_only
  runtime_changes_allowed: false
  firmware_changes_allowed: false
  backend_changes_allowed: false
  mobile_changes_allowed: false
  cloud_changes_allowed: false
  production_ready_claims_allowed: false
  safety_critical_claims_allowed: false
  commercial_ready_claims_allowed: false
  certification_claims_allowed: false
  security_grade_claims_allowed: false
  risk_acceptance_authority: project_owner
  unvalidated_claim_marker: "[UNVALIDATED]"

HIDDEN_ANTI_REGRESSION_RULES:
  - This file is a template, not an actual risk record.
  - Do not create docs/risks/ or a concrete risk assessment unless a later task explicitly requires it.
  - Risk acceptance, rejection, deferral, or mitigation approval requires Project Owner decision.
  - GitHub stores versioned risk records when introduced.
  - Jira tracks risk work state and evidence links.
  - Confluence may summarize and link risk posture for stakeholders but must not duplicate long-form technical risk records.
  - Preserve [UNVALIDATED] on unproven claims.
  - Do not expand MVP scope silently.
  - Do not introduce production-ready, safety-critical, commercial-ready, certification, or security-grade claims.
-->

---

## 1. Scope

Describe the risk being assessed.

```text
This assessment covers ...
```

Out of scope:

```text
This assessment does not introduce firmware, backend, mobile, cloud, runtime, production, safety-critical, commercial, certification, or security-grade claims.
```

---

## 2. Risk Statement

State the risk in one clear sentence.

```text
There is a risk that ... because ...
```

Keep unproven claims marked with `[UNVALIDATED]`.

---

## 3. Impact

Use the same dimensions and order as the Shift Left Impact block.

| Dimension | Impact | Rationale |
|---|---:|---|
| Security | N/A / Low / Medium / High |  |
| Privacy | N/A / Low / Medium / High |  |
| Cost | N/A / Low / Medium / High |  |
| Compliance | N/A / Low / Medium / High |  |
| Testing | N/A / Low / Medium / High |  |
| Documentation | N/A / Low / Medium / High |  |
| Stakeholder Visibility | N/A / Low / Medium / High |  |

Every `N/A` requires an explicit rationale.

---

## 4. Mitigation / Decision Options

| Option | Meaning | Follow-up |
|---|---|---|
| Accept | Project Owner accepts the residual risk. | Link decision evidence. |
| Mitigate | Reduce the risk before proceeding. | Track mitigation task or PR. |
| Defer | Move the risk decision to future work. | Link future Jira issue when available. |
| Reject | Keep the risky scope out of the project or MVP. | Link rejection rationale. |

This section does not approve the decision by itself. Project Owner decision is required before the status is treated as accepted, deferred, or rejected.

---

## 5. Evidence

| Evidence | Link |
|---|---|
| Jira issue | IHAP-XX |
| Pull request | <link> |
| Related docs | <path> |
| Related ADRs | <path or none> |
| Runtime evidence | <link or `[UNVALIDATED]`> |

Missing evidence means the related claim remains `[UNVALIDATED]`.

---

## 6. Review Notes

```text
[ ] GitHub remains the source of truth for the risk record.
[ ] Jira links work state and evidence only.
[ ] Confluence summarizes and links only when stakeholder visibility is needed.
[ ] MVP boundary was not silently expanded.
[ ] [UNVALIDATED] is preserved where evidence is missing.
[ ] No production-ready, safety-critical, commercial-ready, certification, or security-grade claim was introduced.
[ ] Project Owner decision is recorded before status becomes Accepted, Deferred, or Rejected.
```

---

## 7. Practical Rule

```text
Assess risk to expose uncertainty.
Do not use risk assessment to smuggle scope into the MVP.
```
