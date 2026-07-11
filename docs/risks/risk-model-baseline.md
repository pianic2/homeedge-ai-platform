# Risk Model Baseline

**Issue:** IHAP-16 — S0-007 — Risk Model Baseline; extended by IHAP-39 — S0-029 — Risk Treatment Workflow and Traceability  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Document type:** Risk governance / modeling guide  
**Status:** Sprint 0 draft for review  
**Reading target:** less than 5 minutes for humans; hidden metadata supports AI routing and anti-regression checks.  
**Source of truth:** This versioned GitHub document defines how project risks and treatments are modeled until superseded by a later reviewed change.

<!--
AI_AGENT_METADATA:
  issue: IHAP-39
  document_type: risk_model_baseline
  canonical_path: docs/risks/risk-model-baseline.md
  source_of_truth: github_versioned_repository_documentation
  risk_index: docs/risks/README.md
  risk_records_path: docs/risks/records/
  risk_assessment_template: docs/templates/risk-assessment.md
  adr_template: docs/adr/template.md
  jira_role: operational_coordination_only
  confluence_role: stakeholder_summary_and_navigation_only
  task_scope: documentation_governance_only
  runtime_changes_allowed: false
  autonomous_decision_authority: false
  risk_acceptance_authority: project_owner
  unvalidated_claim_marker: "[UNVALIDATED]"

HIDDEN_ANTI_REGRESSION_RULES:
  - The Risk Record is the canonical technical dossier for the risk and its treatments.
  - Jira coordinates treatment work, blockers, workflow state, and evidence links; it must not replace treatment truth.
  - ADRs are created only for stable architectural decisions and never automatically for every risk.
  - Confluence may summarize and link; it must not duplicate risk records or ADRs.
  - Implemented does not mean Verified.
  - No residual risk is accepted, deferred, or rejected without Project Owner decision evidence.
  - Preserve [UNVALIDATED] where implementation or effectiveness evidence is missing.
-->

---

## 1. Operating Rule

```text
The Risk Record is the canonical treatment dossier.
Jira coordinates treatment work.
ADRs record stable architectural decisions only when needed.
Evidence proves implementation and effectiveness.
The Project Owner alone decides residual-risk acceptance, deferral, or rejection.
```

This file defines the model. `docs/risks/README.md` is the index. Concrete records live under `docs/risks/records/`.

---

## 2. Required Risk Fields

Every concrete risk record must define:

| Field | Rule |
|---|---|
| Risk statement | One sentence: “There is a risk that ... because ...”. |
| Source trigger | Why the risk exists in the current project scope. |
| Affected assets | Device, payload, metadata, service, stakeholder, or governance surface. |
| Trust boundary | Where the risk can materialize. |
| Category | Technical, Security, Privacy, Compliance / Claims, Cost, Documentation, Stakeholder Visibility, or AI / Inference. |
| Current assessment | Likelihood, impact, residual risk, evidence gap, and decision state. |
| Existing controls | Only controls currently present and supported by evidence. |
| Treatments | One or more stable `RT-*` entries, monitoring, or explicit Project Owner decision. |
| Stakeholder visibility | Show, link, redact, or block. |
| Review history | Human-readable summary of material changes; Git preserves the full history. |

---

## 3. Risk and Decision States

| Field | Values |
|---|---|
| Risk status | Newly Identified / Under Treatment / Monitoring / Decision Pending / Closed |
| Likelihood | Low / Medium / High |
| Impact | Low / Medium / High |
| Residual risk | Low / Medium / High / Pending Evidence |
| Owner decision | Pending / Accepted / Deferred / Rejected |

Risk status and owner decision are separate. A risk may be `Under Treatment` while the owner decision remains `Pending`.

`Closed` requires traceable decision evidence and does not follow automatically from a closed Jira task.

---

## 4. Risk Treatment Model

A Risk Treatment is a versioned plan and evidence trail inside the Risk Record. It may coordinate one or more Jira tasks and may reference zero, one, or more ADRs.

### 4.1 Stable identifier

```text
RT-<RISK_ID>-<SEQUENCE>
```

Example: `RT-R001-01`.

The identifier remains stable when the treatment is revised. A materially different treatment receives a new sequence.

### 4.2 Strategy

Allowed strategies:

- Mitigate;
- Avoid;
- Transfer;
- Monitor;
- Candidate Accept.

`Candidate Accept` only prepares a decision request. It does not accept the risk.

### 4.3 Lifecycle

```text
Proposed -> Approved -> In Progress -> Implemented -> Verified
```

Alternative terminal or review states:

- Ineffective;
- Superseded;
- Withdrawn.

Rules:

- `Approved` requires explicit approval evidence for the treatment scope;
- `Implemented` requires implementation evidence;
- `Verified` requires verification evidence and an effectiveness review;
- `Implemented` never implies `Verified`;
- treatment lifecycle changes never accept, defer, or reject residual risk automatically.

### 4.4 Minimum treatment content

Each treatment must record:

- stable treatment ID and title;
- strategy and lifecycle status;
- rationale and scope coverage;
- uncovered exposure;
- operational owner or role;
- Jira coordination link when work is required;
- related ADRs or `None`;
- source register;
- implementation and verification evidence;
- effectiveness review;
- introduced date, last review, and next review trigger.

---

## 5. Source and Evidence Model

Sources justify why a treatment is appropriate. Evidence demonstrates what was implemented and whether it worked. They are not interchangeable.

### 5.1 Evidence classes

| Class | Purpose |
|---|---|
| Source evidence | Supports the treatment rationale or control design. |
| Implementation evidence | Shows that planned work exists or was performed. |
| Verification evidence | Shows observed behavior against an expected result. |
| Decision evidence | Records Project Owner acceptance, deferral, rejection, or treatment approval where required. |

### 5.2 Preferred source order

1. official standards and regulations;
2. official vendor or technology documentation;
3. institutional publications;
4. peer-reviewed research;
5. primary project documentation;
6. internal tests, logs, measurements, and reproductions;
7. secondary sources only as support.

Blogs, forums, promotional material, and AI-generated output must not be the sole primary basis for a material treatment decision.

### 5.3 Source verification states

- Verified;
- Partially Verified;
- Pending Verification;
- Obsolete;
- Rejected.

Every source must identify the claim it supports, version or applicability when relevant, checked date, and limitations. A generic homepage link is not sufficient evidence.

Missing implementation or effectiveness evidence preserves `[UNVALIDATED]`.

---

## 6. Many-to-Many Traceability

The model supports:

- one risk with multiple treatments;
- one treatment coordinating multiple Jira tasks;
- one treatment referencing multiple ADRs;
- one ADR affecting multiple risks or treatments.

Every relationship must be explicit in the Risk Record. When an ADR affects a documented risk, the ADR must declare the linked risk, linked treatment, and effect. The Risk Record must contain the inverse link.

Allowed ADR effects:

- mitigates;
- partially mitigates;
- transfers;
- avoids;
- introduces;
- leaves unresolved;
- supersedes a previous treatment decision.

An ADR never closes a risk by itself.

---

## 7. Orphan Risk and Anti-Orphan Rule

A newly recorded risk starts as:

```text
Newly Identified — Treatment Triage Required
```

It is not immediately orphaned while triage is active.

A risk is orphan when it is canonical but lacks an adequate treatment, monitoring, review, or decision path. Indicators include:

- no `RT-*` entry and no Project Owner decision;
- work is required but no Jira coordination link exists;
- Jira, ADR, PR, or evidence exists but is not linked from the Risk Record;
- a treatment is marked `Implemented` without implementation evidence;
- a treatment is marked `Verified` without verification evidence;
- sources are missing, obsolete, rejected, or unrelated to the supported claim;
- a review trigger occurred without reassessment;
- residual risk changed without a documented effectiveness review.

Anti-orphan requirement: every canonical risk must have at least one of:

- a proposed or active treatment;
- formal monitoring with a review trigger;
- a Project Owner decision;
- explicit deferral with a tracked follow-up.

No arbitrary day-based deadline is introduced by this baseline. The applicable governance gate determines when triage must be resolved.

---

## 8. Jira Risk Treatment Task

Jira coordinates the work; it does not replace the canonical treatment dossier.

Minimum task content:

- summary with treatment ID;
- Risk Record link;
- treatment goal, scope, and non-scope;
- current treatment lifecycle state;
- expected source, implementation, and verification evidence;
- related ADR or ADR candidate status;
- Project Owner decision requirement;
- completion condition requiring the Risk Record to be updated.

Closing a Jira task does not automatically mean the treatment is verified, effective, or accepted.

---

## 9. Stakeholder Proposal Flow

```text
Stakeholder proposal
-> Jira or Confluence intake
-> technical triage and duplicate check
-> source review
-> GitHub Risk Record proposal
-> PR review
-> canonical creation, merge, or rejection
```

A stakeholder proposal does not automatically:

- create a canonical risk;
- create a treatment task;
- create an ADR;
- change residual risk;
- change MVP scope.

Confluence may show proposal state and links only. Technical truth becomes canonical only through reviewed GitHub change.

---

## 10. Review and History

Every material treatment review records:

- review date;
- evidence reviewed;
- effectiveness: Effective / Partially Effective / Ineffective / Pending Evidence;
- likelihood and impact after treatment;
- residual risk;
- remaining exposure;
- whether Project Owner decision is required.

The Risk Record contains a short assessment history. Git history remains the full revision history.

Review triggers may include:

- implementation completion;
- failed or changed test results;
- incident or new threat information;
- architecture or dependency change;
- source becoming obsolete;
- scheduled review date;
- stakeholder evidence that changes the risk statement.

---

## 11. Review Checklist

```text
[ ] Risk statement, source trigger, assets, and trust boundary are explicit.
[ ] Existing controls are separated from planned treatments.
[ ] Every treatment has a stable RT-* ID, strategy, status, coverage, and remaining exposure.
[ ] Sources identify the supported claim, verification state, date, and applicability.
[ ] Implementation and verification evidence are separate.
[ ] Implemented is not treated as Verified.
[ ] Missing proof preserves [UNVALIDATED].
[ ] Jira coordinates work but does not replace treatment truth.
[ ] ADRs are linked only when a stable architectural decision is relevant.
[ ] Risk, treatment, Jira, ADR, and evidence links are bidirectional where applicable.
[ ] Orphan indicators and review triggers are checked.
[ ] Project Owner decision evidence exists before Accepted, Deferred, Rejected, or Closed.
[ ] No runtime, firmware, backend, mobile, cloud, schema, or security enforcement is introduced by the record.
[ ] No forbidden production, commercial, security-grade, safety-critical, alarm, antifurto, certification, access-control, intrusion-detection, or protection claim is introduced.
```

---

## 12. Practical Rule

```text
The baseline defines the model.
The Risk Record carries the living treatment dossier.
Jira coordinates work.
Evidence carries proof.
The Project Owner carries the residual-risk decision.
```
