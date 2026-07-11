# Risk Assessment — <Short Title>

**Risk ID:** R-XXX  
**Risk status:** Newly Identified / Under Treatment / Monitoring / Decision Pending / Closed  
**Current assessment date:** YYYY-MM-DD  
**Last reviewed:** YYYY-MM-DD  
**Next review:** YYYY-MM-DD / Event-driven  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Jira:** IHAP-XX  
**PR:** <link when available>  
**Owner decision:** Pending / Accepted / Deferred / Rejected

<!--
AI_AGENT_METADATA:
  issue: IHAP-39
  document_type: risk_assessment_template
  canonical_path: docs/templates/risk-assessment.md
  source_of_truth: github_versioned_repository_documentation
  template_output_target: docs/risks/records/
  jira_role: operational_coordination_only
  confluence_role: stakeholder_summary_and_navigation_only
  task_scope: documentation_governance_only
  runtime_changes_allowed: false
  risk_acceptance_authority: project_owner
  unvalidated_claim_marker: "[UNVALIDATED]"

HIDDEN_ANTI_REGRESSION_RULES:
  - This file is a template, not an actual risk record.
  - Risk Records are living technical dossiers; Git preserves full history.
  - Treatment details belong in the Risk Record, not only in Jira.
  - Implemented does not mean Verified.
  - Risk acceptance, rejection, or deferral requires Project Owner decision evidence.
  - Preserve [UNVALIDATED] on unproven implementation or effectiveness claims.
-->

---

## 1. Risk Statement

```text
There is a risk that ... because ...
```

Keep unproven claims marked with `[UNVALIDATED]`.

---

## 2. Source Trigger and Scope

**Source trigger:** Describe the concrete project condition that exposes the risk.

**In scope:**

- ...

**Out of scope:**

- ...

This record does not introduce firmware, backend, mobile, cloud, runtime, security enforcement, or unsupported maturity claims.

---

## 3. Affected Assets and Trust Boundary

| Area | Detail |
|---|---|
| Assets | ... |
| Trust boundary | ... |
| Data involved | ... |
| Stakeholder surface | ... |

---

## 4. Current Assessment

| Field | Value | Rationale |
|---|---|---|
| Category | Technical / Security / Privacy / Compliance / Claims / Cost / Documentation / Stakeholder Visibility / AI | ... |
| Likelihood | Low / Medium / High | ... |
| Impact | Low / Medium / High | ... |
| Residual risk | Low / Medium / High / Pending Evidence | ... |
| Evidence gap | `[UNVALIDATED]` or linked evidence | ... |
| Decision state | Pending Project Owner / Accepted / Deferred / Rejected | ... |

---

## 5. Existing Controls

List only controls that currently exist and have evidence.

| Control | Evidence | Coverage | Limitation |
|---|---|---|---|
| ... | <link or `[UNVALIDATED]`> | Full / Partial | ... |

Planned actions belong in Risk Treatments, not here.

---

## 6. Risk Treatment Summary

| Treatment ID | Title | Strategy | Lifecycle status | Jira | ADR | Last review |
|---|---|---|---|---|---|---|
| RT-RXXX-01 | ... | Mitigate / Avoid / Transfer / Monitor / Candidate Accept | Proposed / Approved / In Progress / Implemented / Verified / Ineffective / Superseded / Withdrawn | IHAP-XX / Pending approval | None / ADR-XXX / Candidate | YYYY-MM-DD |

---

## 7. Risk Treatments

Repeat this subsection for every treatment.

### RT-RXXX-01 — <Treatment title>

**Strategy:** Mitigate / Avoid / Transfer / Monitor / Candidate Accept  
**Lifecycle status:** Proposed / Approved / In Progress / Implemented / Verified / Ineffective / Superseded / Withdrawn  
**Treatment owner:** <role or team>  
**Jira coordination:** IHAP-XX / Pending Project Owner approval / Not required  
**Related ADRs:** ADR-XXX / Candidate / None  
**Introduced:** YYYY-MM-DD  
**Last reviewed:** YYYY-MM-DD  
**Next review trigger:** <date, milestone, evidence, incident, dependency, or architecture change>

#### Rationale

Explain why this treatment is appropriate and which assumptions remain `[UNVALIDATED]`.

#### Planned Controls or Actions

- ...

These are planned actions until implementation evidence exists.

#### Scope Coverage

| Risk cause or consequence | Coverage | Rationale |
|---|---|---|
| ... | Full / Partial / None | ... |

#### Remaining Exposure

Describe what this treatment does not address.

#### Source and Evidence Register

| ID | Source | Source type | Supports | Version / applicability | Verification | Checked on | Limitations |
|---|---|---|---|---|---|---|---|
| SRC-01 | <title and link/path> | Standard / Official docs / Institution / Research / Project docs / Internal evidence / Secondary | <specific claim> | ... | Verified / Partially Verified / Pending Verification / Obsolete / Rejected | YYYY-MM-DD | ... |

A generic homepage link is not sufficient. Blog, forum, promotional, or AI-generated content must not be the sole primary support for a material treatment decision.

#### Implementation and Verification Evidence

| Evidence ID | Evidence | Evidence class | Expected result | Actual result | Status | Date |
|---|---|---|---|---|---|---|
| EV-01 | <PR, test, log, report, or review> | Implementation / Verification / Decision | ... | ... / Not executed | `[UNVALIDATED]` / Passed / Failed / Partial | YYYY-MM-DD |

`Implemented` requires implementation evidence. `Verified` requires verification evidence and an effectiveness review.

#### Treatment Effectiveness Review

**Review date:** YYYY-MM-DD  
**Evidence reviewed:** EV-XX  
**Effectiveness:** Effective / Partially Effective / Ineffective / Pending Evidence  
**Likelihood after treatment:** Low / Medium / High / Pending Evidence  
**Impact after treatment:** Low / Medium / High / Pending Evidence  
**Residual risk:** Low / Medium / High / Pending Evidence  
**Remaining exposure:** ...  
**Project Owner decision required:** Yes / No

This review does not accept, defer, or reject residual risk by itself.

---

## 8. Traceability

| Relationship | Link | Effect / Rule |
|---|---|---|
| Jira treatment task | IHAP-XX | Operational coordination only |
| Pull request | <link> | Implementation evidence only when relevant |
| Related ADR | `docs/adr/ADR-XXXX-*.md` / None | Mitigates / Partially mitigates / Transfers / Avoids / Introduces / Leaves unresolved / Supersedes |
| Related risks | R-XXX / None | State the shared boundary; do not merge distinct risk records |
| Related policy or test | <path/link> | ... |

Every applicable relationship must also be declared by the linked ADR or record when that artifact supports inverse links.

---

## 9. Stakeholder Visibility

| Item | Rule | Rationale |
|---|---|---|
| Risk summary | Show / Link / Redact / Block | ... |
| Treatment summary | Show / Link / Redact / Block | ... |
| Technical implementation | Show / Link / Redact / Block | ... |
| Secrets, private topology, personal or domestic data | Block / Redact | ... |
| Maturity claim | Keep `[UNVALIDATED]` where evidence is missing | ... |

Stakeholder-safe wording:

```text
...
```

Confluence may summarize and link only. It must not duplicate this dossier.

---

## 10. Assessment History

Record material changes only. Git preserves the full history.

| Date | Change | Treatment | Evidence | Decision |
|---|---|---|---|---|
| YYYY-MM-DD | Risk identified / treatment proposed / control implemented / effectiveness reviewed / source invalidated | RT-RXXX-01 / None | SRC-XX / EV-XX / None | Pending / linked Project Owner decision |

---

## 11. Review Notes

```text
[ ] GitHub remains the canonical risk and treatment dossier.
[ ] Jira coordinates work, status, blockers, and evidence links only.
[ ] Confluence summarizes and links only.
[ ] Existing controls are separated from planned actions.
[ ] Every treatment has a stable RT-* ID.
[ ] Sources identify the supported claim, verification state, date, and applicability.
[ ] Implementation evidence and verification evidence are separate.
[ ] Implemented is not treated as Verified.
[ ] [UNVALIDATED] is preserved where proof is missing.
[ ] Related Jira tasks and ADRs are linked in both directions when applicable.
[ ] Review triggers and orphan indicators were checked.
[ ] No ADR was created automatically.
[ ] No production-ready, commercial-ready, security-grade, certified, safety-critical, alarm-grade, antifurto, access-control, intrusion-detection, or protection claim was introduced.
[ ] Project Owner decision evidence exists before Accepted, Deferred, Rejected, or Closed.
```

---

## 12. Practical Rule

```text
Document the treatment in the Risk Record.
Coordinate the work in Jira.
Use ADRs only for stable architectural decisions.
Require evidence before effectiveness claims.
Leave residual-risk decisions to the Project Owner.
```
