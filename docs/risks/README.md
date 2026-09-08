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
-->

---

## 1. Purpose

This folder contains versioned risk documentation for HomeEdge AI Platform. Risk/treatment truth lives in each Risk Record; Jira coordinates work; Confluence may summarize/link only; the Project Owner decides treatment approval and residual risk where required.

---

## 2. Current Documents

| Need | Use | Rule |
|---|---|---|
| Risk and treatment model | `risk-model-baseline.md` | Defines lifecycle, source verification, traceability, orphan rules and decision boundaries. |
| Concrete Risk Records | `records/` | Canonical living dossiers. |
| Risk Record template | `../templates/risk-assessment.md` | Use for explicit risk work. |
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
| R-012 | `records/R-012-unprotected-li-ion-battery-fault.md` | Technical | **RT-R012-01 Proposed** | Pending Project Owner |
| R-013 | `records/R-013-edge-power-rail-transfer-integrity.md` | Technical | **RT-R013-01 Proposed** | Pending Project Owner |

R-012 and R-013 were introduced by IHAP-56 after post-merge review of ADR-0007. Their canonical Category fields use only the vocabulary defined by `risk-model-baseline.md`; compliance/claim or data-integrity consequences are recorded in each dossier's rationale/stakeholder surface instead of inventing category values. Their treatment rationale is documented, but lifecycle remains **Proposed** because ADR-0007/PR #34 acceptance predates those treatment records and is not valid approval evidence for them. IHAP-55 is the intended implementation/verification owner after applicable approval; IHAP-57 coordinates later lifecycle/effectiveness updates after an explicit treatment decision and physical evidence.

---

## 4. Navigation Rule

```text
Risk Record -> Risk Treatment -> Jira coordination -> optional ADR -> evidence -> effectiveness review -> Project Owner decision
```

---

## 5. Surface Rules

```text
GitHub Risk Records define risk and treatment truth.
Jira coordinates work and links evidence.
ADRs document stable architectural decisions when required.
Confluence summarizes and links for stakeholders.
Project Owner decides treatment approval and residual risk.
```

Preserve `[UNVALIDATED]` where evidence is missing.

---

## 6. Orphan Review

A record requires review when it lacks a treatment, monitoring, explicit decision, current source verification, required Jira coordination, or current effectiveness review.

R-011 is not orphaned because RT-R011-01 is Proposed with coordination and review trigger.

R-012 and R-013 are not orphaned: each has a **Proposed** treatment, IHAP-55/IHAP-57 coordination, inverse ADR-0007 links with an allowed ADR effect, and explicit pending-evidence state. Proposed treatment status does not imply approval, implementation, verification or risk acceptance.

---

## 7. Practical Rule

```text
The README is the index.
The baseline is the model.
The records carry the living analysis and treatments.
Jira coordinates.
The Project Owner decides.
```
