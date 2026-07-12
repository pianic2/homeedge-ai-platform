# Risk Documentation

**Issue:** IHAP-16 — S0-007 — Risk Model Baseline; extended by IHAP-39 and reviewed by IHAP-40  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Document type:** Risk documentation index  
**Status:** Sprint 0 draft for review  
**Reading target:** less than 2 minutes for humans.  
**Source of truth:** This index routes current MVP risk documentation under `docs/risks/`. It does not accept risk or replace Project Owner decisions.

<!--
AI_AGENT_METADATA:
  issue: IHAP-40
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
  - Keep only risks with a concrete current-MVP or current-governance exposure.
  - FUTURE or OUT OF MVP capability does not justify a standing canonical risk record.
  - Reassess removed risks only when the related capability is explicitly proposed for scope.
  - Risk and treatment truth lives in each GitHub Risk Record.
  - Jira coordinates work and links evidence.
  - Confluence summarizes and links only.
-->

---

## 1. Purpose

This folder contains the versioned risk and treatment documentation for the current HomeEdge AI Platform MVP and its active governance surfaces.

Use it for:

- the project risk and treatment model;
- concrete living Risk Records;
- traceability from risk to treatment, Jira, optional ADR and evidence;
- links from Jira and stakeholder summaries.

Do not keep speculative risks solely for capabilities classified as FUTURE or OUT OF MVP. Create or restore a risk record when that capability is explicitly proposed for scope.

---

## 2. Current Documents

| Need | Use | Rule |
|---|---|---|
| Risk and treatment model | `risk-model-baseline.md` | Defines lifecycle, source verification, traceability, orphan rules and decision boundaries |
| Concrete Risk Records | `records/` | Stores current MVP and current-governance risk dossiers |
| Risk Record template | `../templates/risk-assessment.md` | Use when an explicit task creates or revises a Risk Record |
| ADR relationship | `../adr/template.md` | Use only when a stable architectural decision is required |

---

## 3. Current Risk Records

| ID | Record | Primary category | Treatment state | Jira coordination | Decision state |
|---|---|---|---|---|---|
| R-001 | `records/R-001-device-identity-spoofing.md` | Security / Technical | RT-R001-01 Proposed | Future task 1 pending approval | Pending Project Owner |
| R-002 | `records/R-002-event-payload-leakage.md` | Security / Privacy | RT-R002-01 Proposed | Future task 2 pending approval | Pending Project Owner |
| R-003 | `records/R-003-technical-metadata-inference.md` | Privacy / Stakeholder Visibility | RT-R003-01 and RT-R003-02 Proposed | Policy review + future task 2 pending approval | Pending Project Owner |
| R-004 | `records/R-004-presence-door-state-misinterpretation.md` | Privacy / Compliance / Claims | RT-R004-01 Proposed | Existing policy/review | Pending Project Owner |
| R-005 | `records/R-005-target-boundary-overclaim.md` | Compliance / Documentation | RT-R005-01 Proposed | Existing policy/review | Pending Project Owner |
| R-006 | `records/R-006-source-of-truth-drift.md` | Documentation / Stakeholder Visibility | RT-R006-01 Proposed; Monitoring | Governance gate | Pending Project Owner |
| R-008 | `records/R-008-cost-abuse.md` | Cost / Technical | RT-R008-01 Proposed | IHAP-17 | Pending Project Owner |
| R-009 | `records/R-009-stakeholder-maturity-misread.md` | Stakeholder Visibility / Claims | RT-R009-01 Proposed | Existing policy/review | Pending Project Owner |
| R-010 | `records/R-010-risk-driven-scope-creep.md` | Documentation / Compliance | RT-R010-01 Proposed | Governance gate | Pending Project Owner |

All current records have a treatment or monitoring path and are not orphan under the IHAP-39 rule.

---

## 4. Removed Non-MVP Risk

`R-007 — AI Inference and Profiling` was removed by IHAP-40 because AI inference is classified as FUTURE / `[UNVALIDATED]` and no concrete AI function is currently proposed inside the MVP.

Reassessment trigger:

```text
Create or restore an AI risk record only when an explicit Jira task proposes an AI function, dataset, inference flow, evaluation boundary, or related MVP scope change.
```

Removal does not approve AI behavior and does not weaken the existing Product Vision or privacy boundaries. It prevents speculative governance and overengineering.

---

## 5. Approved Future Coordination Topology

Only two future operational treatment tasks are planned:

1. `RT-R001-01 — Device Identity and Ingestion Trust Controls`;
2. `RT-R002-01 / RT-R003-02 — Payload and Metadata Privacy Controls`.

They are not created automatically by IHAP-40. Project Owner approval remains required.

R-001, R-002 and R-003 record ADR status as `Candidate`; IHAP-40 creates no ADR.

---

## 6. Navigation Rule

```text
Risk Record -> Risk Treatment -> Jira coordination -> optional ADR -> evidence -> effectiveness review -> Project Owner decision
```

The index exposes status and routing only. It does not duplicate treatment rationale, source registers or evidence.

---

## 7. Surface Rules

```text
GitHub Risk Records define risk and treatment truth.
Jira coordinates work and links evidence.
ADRs document stable architectural decisions only when required.
Confluence summarizes and links for stakeholders.
Project Owner decides residual risk.
```

---

## 8. Practical Rule

```text
Keep risks aligned to current MVP exposure.
Remove speculative FUTURE-only risks.
Restore them only when concrete scope is proposed.
Treatments start as Proposed.
Evidence proves effectiveness.
The Project Owner decides.
```