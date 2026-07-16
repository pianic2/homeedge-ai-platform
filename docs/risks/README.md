# Risk Documentation

**Issue:** IHAP-16 — S0-007 — Risk Model Baseline; extended by IHAP-39 — S0-029 — Risk Treatment Workflow and Traceability  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Document type:** Risk documentation index  
**Status:** Sprint 0 draft for review  
**Reading target:** less than 2 minutes for humans.  
**Source of truth:** This index routes risk documentation under `docs/risks/`. It does not accept risk or replace Project Owner decisions.

<!--
AI_AGENT_METADATA:
  issue: IHAP-39
  document_type: risk_documentation_index
  canonical_path: docs/risks/README.md
  risk_model_baseline: docs/risks/risk-model-baseline.md
  risk_records_path: docs/risks/records/
  risk_assessment_template: docs/templates/risk-assessment.md
  jira_role: operational_coordination_only
  confluence_role: stakeholder_summary_and_navigation_only
  risk_acceptance_authority: project_owner
  unvalidated_claim_marker: "[UNVALIDATED]"

HIDDEN_ANTI_REGRESSION_RULES:
  - This file is an index, not a treatment dossier or risk acceptance record.
  - Risk and treatment truth lives in each GitHub Risk Record.
  - Jira tracks treatment work, blockers, workflow state, and evidence links.
  - Confluence may summarize and link but must not duplicate technical records.
  - Preserve [UNVALIDATED] on unproven implementation or effectiveness claims.
-->

---

## 1. Purpose

This folder contains versioned risk documentation for HomeEdge AI Platform.

Use it for:

- the project risk and treatment model;
- concrete living Risk Records;
- traceability from risk to treatment, Jira, ADR, and evidence;
- links from Jira evidence and Confluence stakeholder summaries.

Do not use this index to accept risk automatically.

---

## 2. Current Documents

| Need | Use | Rule |
|---|---|---|
| Risk and treatment model | `risk-model-baseline.md` | Defines lifecycle, source verification, traceability, orphan rules, and decision boundaries. |
| Concrete Risk Records | `records/` | Each record is the canonical living dossier for the risk and its treatments. |
| Risk Record template | `../templates/risk-assessment.md` | Use when an explicit task creates or revises a Risk Record. |
| ADR relationship | `../adr/template.md` | Use only when a stable architectural decision is required. |

---

## 3. Current Risk Records

| ID | Record | Primary category | Treatment state | Decision state |
|---|---|---|---|---|
| R-001 | `records/R-001-device-identity-spoofing.md` | Security / Technical | To be reviewed by IHAP-40 | Pending Project Owner |
| R-002 | `records/R-002-event-payload-leakage.md` | Security / Privacy | To be reviewed by IHAP-40 | Pending Project Owner |
| R-003 | `records/R-003-technical-metadata-inference.md` | Privacy / Stakeholder Visibility | To be reviewed by IHAP-40 | Pending Project Owner |
| R-004 | `records/R-004-presence-door-state-misinterpretation.md` | Privacy / Compliance / Claims | To be reviewed by IHAP-40 | Pending Project Owner |
| R-005 | `records/R-005-target-boundary-overclaim.md` | Compliance / Documentation | To be reviewed by IHAP-40 | Pending Project Owner |
| R-006 | `records/R-006-source-of-truth-drift.md` | Documentation / Stakeholder Visibility | To be reviewed by IHAP-40 | Pending Project Owner |
| R-007 | `records/R-007-ai-inference-profiling.md` | AI / Privacy | To be reviewed by IHAP-40 | Pending Project Owner |
| R-008 | `records/R-008-cost-abuse.md` | Cost / Technical | To be reviewed by IHAP-40 | Pending Project Owner |
| R-009 | `records/R-009-stakeholder-maturity-misread.md` | Stakeholder Visibility / Claims | To be reviewed by IHAP-40 | Pending Project Owner |
| R-010 | `records/R-010-risk-driven-scope-creep.md` | Documentation / Compliance | To be reviewed by IHAP-40 | Pending Project Owner |
| R-011 | `records/R-011-environmental-sensor-placement-bias.md` | Technical / Claims | RT-R011-01 Proposed | Pending Project Owner |

IHAP-39 defines the model only. IHAP-40 owns the earlier record migration and review. R-011 was introduced by IHAP-45 from concrete environmental-sensor evidence and has its own proposed treatment and event-driven review trigger.

---

## 4. Navigation Rule

```text
Risk Record -> Risk Treatment -> Jira coordination -> optional ADR -> evidence -> effectiveness review -> Project Owner decision
```

The index may expose status and routing. It must not duplicate treatment rationale, source registers, evidence, or decision reasoning from the Risk Record.

---

## 5. Surface Rules

```text
GitHub Risk Records define risk and treatment truth.
Jira coordinates work and links evidence.
ADRs document stable architectural decisions when required.
Confluence summarizes and links for stakeholders.
Project Owner decides residual risk.
```

Confluence must not duplicate long-form risk or treatment documentation. Stakeholder summaries must preserve `[UNVALIDATED]` where evidence is missing.

---

## 6. Orphan Review

A record requires review when it lacks a treatment, monitoring, explicit decision, current source verification, required Jira coordination, or current effectiveness review.

Do not mark a newly identified risk orphan while treatment triage is active. Apply the full rule from `risk-model-baseline.md`.

R-011 is not orphaned: RT-R011-01 is Proposed, IHAP-51/IHAP-50 provide coordination, ADR-0002 contains the inverse link and the next review is event-driven.

---

## 7. Practical Rule

```text
The README is the index.
The baseline is the model.
The records carry the living analysis and treatments.
Jira coordinates.
The Project Owner decides.
```
