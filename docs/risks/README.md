# Risk Documentation

**Issue:** IHAP-16 — S0-007 — Risk Model Baseline  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Document type:** Risk documentation index  
**Status:** Sprint 0 draft for review  
**Reading target:** less than 2 minutes for humans.  
**Source of truth:** This index routes risk documentation under `docs/risks/`. It links canonical risk documents; it does not accept risk or replace Project Owner decisions.

<!--
AI_AGENT_METADATA:
  issue: IHAP-16
  document_type: risk_documentation_index
  canonical_path: docs/risks/README.md
  source_of_truth: github_versioned_repository_documentation
  source_of_truth_policy: docs/governance/source-of-truth.md
  risk_model_baseline: docs/risks/risk-model-baseline.md
  risk_assessment_template: docs/templates/risk-assessment.md
  task_scope: documentation_governance_only
  runtime_changes_allowed: false
  firmware_changes_allowed: false
  backend_changes_allowed: false
  mobile_changes_allowed: false
  cloud_changes_allowed: false
  schema_changes_allowed: false
  production_ready_claims_allowed: false
  commercial_ready_claims_allowed: false
  safety_critical_claims_allowed: false
  security_grade_claims_allowed: false
  certification_claims_allowed: false
  alarm_grade_claims_allowed: false
  antifurto_claims_allowed: false
  protection_claims_allowed: false
  risk_acceptance_authority: project_owner
  autonomous_decision_authority: false
  unvalidated_claim_marker: "[UNVALIDATED]"

HIDDEN_ANTI_REGRESSION_RULES:
  - This file is an index, not a risk register and not a risk acceptance record.
  - GitHub remains the source of truth for risk documentation.
  - Jira tracks risk work state, blockers, review state, and evidence links.
  - Confluence may summarize and link risk posture for stakeholders but must not duplicate long-form risk documentation.
  - Risk acceptance, deferral, or rejection requires Project Owner decision.
  - Review agents may identify findings and recommendations only.
  - Preserve [UNVALIDATED] on unproven implementation, runtime, security, privacy, AI, reliability, cost, or stakeholder-facing claims.
  - Do not expand MVP scope silently.
-->

---

## 1. Purpose

This folder contains versioned risk documentation for HomeEdge AI Platform.

Use it for:

- the project risk model baseline;
- future risk records only when explicitly required by a Jira task and Project Owner-approved scope;
- links from Jira evidence and Confluence stakeholder summaries.

Do not use it to accept risk automatically.

---

## 2. Current Documents

| Need | Use | Rule |
|---|---|---|
| Project risk model | `risk-model-baseline.md` | Defines risk categories, scoring, residual risk, treatment, evidence, ownership, and stakeholder visibility boundaries. |
| Future risk assessment template | `../templates/risk-assessment.md` | Template only. Use only when an explicit future task requires a concrete risk assessment. |

---

## 3. Surface Rules

```text
GitHub defines risk truth.
Jira tracks risk work and evidence.
Confluence summarizes and links for stakeholders.
Project Owner decides risk acceptance.
```

Confluence must not duplicate long-form risk documentation. If stakeholder visibility is needed, use a short summary and link back to GitHub/Jira evidence.

---

## 4. Practical Rule

```text
Expose risk clearly.
Do not use risk documentation to smuggle scope into the MVP.
```
