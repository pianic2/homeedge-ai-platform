# Risk Documentation

**Issue:** IHAP-16 — S0-007 — Risk Model Baseline  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Document type:** Risk documentation index  
**Status:** Sprint 0 draft for review  
**Reading target:** less than 2 minutes for humans.  
**Source of truth:** This index routes risk documentation under `docs/risks/`. It links canonical risk documents and concrete risk records; it does not accept risk or replace Project Owner decisions.

<!--
AI_AGENT_METADATA:
  issue: IHAP-16
  document_type: risk_documentation_index
  canonical_path: docs/risks/README.md
  source_of_truth: github_versioned_repository_documentation
  source_of_truth_policy: docs/governance/source-of-truth.md
  risk_model_baseline: docs/risks/risk-model-baseline.md
  risk_records_path: docs/risks/records/
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
  - This file is an index, not a risk acceptance record.
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

- the project risk modeling guide;
- concrete risk records;
- links from Jira evidence and Confluence stakeholder summaries.

Do not use it to accept risk automatically.

---

## 2. Current Documents

| Need | Use | Rule |
|---|---|---|
| Risk modeling guide | `risk-model-baseline.md` | Defines how risks are modeled, scored, linked, and reviewed. |
| Concrete risk records | `records/` | Stores analyzed risks. Every record remains `Pending Project Owner` unless explicit decision evidence exists. |
| Future risk assessment template | `../templates/risk-assessment.md` | Template only. Use only when an explicit future task requires a separate assessment. |

---

## 3. Current Risk Records

| ID | Record | Primary category | Decision state |
|---|---|---|---|
| R-001 | `records/R-001-device-identity-spoofing.md` | Security / Technical | Pending Project Owner |
| R-002 | `records/R-002-event-payload-leakage.md` | Security / Privacy | Pending Project Owner |
| R-003 | `records/R-003-technical-metadata-inference.md` | Privacy / Stakeholder Visibility | Pending Project Owner |
| R-004 | `records/R-004-presence-door-state-misinterpretation.md` | Privacy / Compliance / Claims | Pending Project Owner |
| R-005 | `records/R-005-target-boundary-overclaim.md` | Compliance / Documentation | Pending Project Owner |
| R-006 | `records/R-006-source-of-truth-drift.md` | Documentation / Stakeholder Visibility | Pending Project Owner |
| R-007 | `records/R-007-ai-inference-profiling.md` | AI / Privacy | Pending Project Owner |
| R-008 | `records/R-008-cost-abuse.md` | Cost / Technical | Pending Project Owner |
| R-009 | `records/R-009-stakeholder-maturity-misread.md` | Stakeholder Visibility / Claims | Pending Project Owner |
| R-010 | `records/R-010-risk-driven-scope-creep.md` | Documentation / Compliance | Pending Project Owner |

These records expose and analyze risk. They do not approve residual risk.

---

## 4. Surface Rules

```text
GitHub defines risk truth.
Jira tracks risk work and evidence.
Confluence summarizes and links for stakeholders.
Project Owner decides risk acceptance.
```

Confluence must not duplicate long-form risk documentation. If stakeholder visibility is needed, use a short summary and link back to GitHub/Jira evidence.

---

## 5. Practical Rule

```text
The README is the index.
The baseline is the guide.
The records carry the analysis.
```
