# Risk Model Baseline

**Issue:** IHAP-16 — S0-007 — Risk Model Baseline  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Document type:** Risk governance / modeling guide  
**Status:** Sprint 0 draft for review  
**Reading target:** less than 3 minutes for humans; hidden metadata supports AI routing and anti-regression checks.  
**Source of truth:** This versioned GitHub document defines how project risks are modeled until superseded by a later reviewed change.

<!--
AI_AGENT_METADATA:
  issue: IHAP-16
  document_type: risk_model_baseline
  canonical_path: docs/risks/risk-model-baseline.md
  source_of_truth: github_versioned_repository_documentation
  risk_index: docs/risks/README.md
  risk_records_path: docs/risks/records/
  source_of_truth_policy: docs/governance/source-of-truth.md
  shift_left_governance_baseline: docs/governance/shift-left-governance-baseline.md
  stakeholder_report_data_rules: docs/governance/stakeholder-report-data-rules.md
  product_vision: docs/product/product-vision.md
  risk_assessment_template: docs/templates/risk-assessment.md
  task_scope: documentation_governance_only
  runtime_changes_allowed: false
  firmware_changes_allowed: false
  backend_changes_allowed: false
  mobile_changes_allowed: false
  cloud_changes_allowed: false
  schema_changes_allowed: false
  autonomous_decision_authority: false
  risk_acceptance_authority: project_owner
  ai_review_agents_decision_authority: false
  unvalidated_claim_marker: "[UNVALIDATED]"

HIDDEN_ANTI_REGRESSION_RULES:
  - This baseline is a guide for defining risks, not a risk register.
  - Concrete risk records live under docs/risks/records/ and must remain linked from docs/risks/README.md.
  - Risk records may propose treatment but must not accept, defer, or reject residual risk without Project Owner decision.
  - Do not duplicate the Shift Left impact block or the risk assessment template.
  - No ADR is introduced by this document.
  - Preserve [UNVALIDATED] on unproven runtime, security, privacy, AI, reliability, cost, or stakeholder-facing claims.
  - Presence and door state remain telemetry/local state only; they are not antifurto, alarm-grade, access-control, intrusion-detection, safety-critical, or protection evidence.
-->

---

## 1. Rule

```text
Model risk consistently.
Record concrete risks separately.
Link evidence.
Project Owner decides acceptance.
```

This file is the guide. The index is `docs/risks/README.md`. Concrete risk records live under `docs/risks/records/`.

---

## 2. What a Risk Record Must Contain

Each concrete risk record must include:

| Field | Required rule |
|---|---|
| Risk statement | One clear sentence: “There is a risk that ... because ...”. |
| Source trigger | Why the risk exists in the current project scope. |
| Affected assets | Device, event payload, metadata, target service, stakeholder surface, or governance surface. |
| Trust boundary | The boundary where the risk can materialize. |
| Category | Technical, Security, Privacy, Compliance / Claims, Cost, Documentation, Stakeholder Visibility, or AI / Inference. |
| Likelihood | Low / Medium / High. |
| Impact | Low / Medium / High. |
| Residual risk | Low / Medium / High / Pending evidence. |
| Treatment proposal | Mitigate / Defer / Reject / Candidate accept. This is not approved until Project Owner decision. |
| Evidence gap | What is still missing. Missing proof keeps related claims `[UNVALIDATED]`. |
| Stakeholder visibility | Show, link, redact, or block. |
| Decision state | `Pending Project Owner` unless explicit Project Owner evidence says otherwise. |

---

## 3. Categories

| Category | Use for |
|---|---|
| Technical | Firmware behavior, event payloads, target services, runtime maturity. |
| Security | Spoofing, tampering, replay, exposed secrets, unsafe trust boundaries. |
| Privacy | Presence state, door state, metadata inference, retention, domestic context leakage. |
| Compliance / Claims | Misleading production, commercial, safety, security, certification, alarm, antifurto, access-control, intrusion-detection, or protection wording. |
| Cost | Hardware, cloud, logs, tooling, event volume, future AI/provider costs. |
| Documentation | Stale docs, duplicate truth, source-of-truth drift, missing evidence links. |
| Stakeholder Visibility | Misunderstanding, overexposure, missing redaction, missing `[UNVALIDATED]`. |
| AI / Inference | Future insight ambiguity, profiling, false interpretation, unvalidated AI claims. |

---

## 4. Scoring

| Field | Values | Meaning |
|---|---|---|
| Likelihood | Low / Medium / High | Probability under current scope and evidence. |
| Impact | Low / Medium / High | Expected damage to project, privacy, security, cost, compliance, evidence, or stakeholder clarity. |
| Residual risk | Low / Medium / High / Pending evidence | Risk remaining after current controls or proposed treatment. |
| Treatment proposal | Mitigate / Defer / Reject / Candidate accept | Proposed action only. Project Owner decision is still required. |
| Decision state | Pending Project Owner / Accepted / Deferred / Rejected | Final state requires explicit Project Owner evidence. |

`Candidate accept` means candidate for Project Owner review. It does not accept the risk.

---

## 5. Source Boundaries

Risk records must preserve these boundaries:

- MVP scope lives in `docs/product/product-vision.md`.
- Task-level impact checks live in `docs/governance/shift-left-governance-baseline.md`.
- Stakeholder report rules live in `docs/governance/stakeholder-report-data-rules.md`.
- The reusable risk template lives in `docs/templates/risk-assessment.md`.
- Concrete risk records live under `docs/risks/records/`.

Risk documentation must not introduce runtime behavior, expand MVP scope, approve ADRs, or weaken claim boundaries.

---

## 6. Review Checklist

Before adding or changing a risk record:

```text
[ ] The risk is tied to a concrete source trigger.
[ ] The risk has affected assets and trust boundary.
[ ] Likelihood, impact, residual risk, and treatment proposal are explicit.
[ ] Decision state is Pending Project Owner unless explicit evidence says otherwise.
[ ] Missing proof keeps [UNVALIDATED].
[ ] Stakeholder visibility is show/link/redact/block.
[ ] No runtime, firmware, backend, mobile, cloud, schema, or ADR is introduced.
[ ] No forbidden production, commercial, security-grade, safety-critical, alarm, antifurto, certification, access-control, intrusion-detection, or protection claim is introduced.
```

---

## 7. Practical Rule

```text
The baseline defines the model.
The risk record carries the analysis.
The Project Owner carries the decision.
```
