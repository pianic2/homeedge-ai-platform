# Project Templates

**Issue:** IHAP-31 — S0-022 — Templates  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Document type:** Templates index  
**Status:** Sprint 0 draft for review  
**Source of truth:** This versioned GitHub document is the canonical index for reusable project templates until superseded by a later reviewed change.

<!--
AI_AGENT_METADATA:
  issue: IHAP-31
  document_type: templates_index
  canonical_path: docs/templates/README.md
  source_of_truth: github_versioned_repository_documentation
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
  unvalidated_claim_marker: "[UNVALIDATED]"

CANONICAL_TEMPLATE_OWNERS:
  adr_template: docs/adr/template.md
  shift_left_impact_template: docs/governance/shift-left-governance-baseline.md
  jira_evidence_comment_template: docs/governance/scrum-governance-dor-dod.md
  stakeholder_evidence_rule: docs/governance/stakeholder-transparency.md
  ai_review_output_templates:
    - docs/governance/ai-review-agents-policy.md
    - docs/governance/ai-review-agent-playbook.md
  governance_lane_gate_output_template: docs/governance/governance-lane-review-gate.md
  risk_assessment_template: docs/templates/risk-assessment.md

HIDDEN_ANTI_REGRESSION_RULES:
  - Use existing canonical templates first.
  - Do not duplicate ADR, Shift Left, Jira evidence, AI review, governance gate, or stakeholder report templates here.
  - GitHub remains the technical source of truth.
  - Jira remains authoritative for backlog, workflow state, review state, blockers, and evidence links.
  - Confluence remains authoritative for stakeholder hub, stakeholder reports, stakeholder forms, and navigation.
  - Confluence must not duplicate long-form GitHub technical documentation.
  - Do not create templates only to increase file count.
  - Preserve [UNVALIDATED] on unproven claims.
  - Do not expand the MVP boundary silently.
  - Do not introduce runtime, production-ready, safety-critical, commercial-ready, certification, or security-grade claims.
-->

---

## 1. Rule

```text
Use existing canonical templates first.
Create a new template only when it prevents repeated ambiguity and does not duplicate an existing canonical document.
```

This index exists to make templates easy to find without creating a second copy of rules already owned by other source-of-truth documents.

---

## 2. Template Inventory

| Need | Use | Owner | Rule |
|---|---|---|---|
| ADR | `docs/adr/template.md` | ADR governance | Do not duplicate here. |
| Shift Left Impact | `docs/governance/shift-left-governance-baseline.md` | Shift Left governance | Copy from the canonical source. |
| Jira evidence comment | `docs/governance/scrum-governance-dor-dod.md` | Scrum governance | Link evidence; do not copy long-form docs into Jira. |
| Stakeholder evidence/report reference | `docs/governance/stakeholder-transparency.md` | Stakeholder transparency | Confluence summarizes and links. |
| AI review finding/summary | `docs/governance/ai-review-agents-policy.md`, `docs/governance/ai-review-agent-playbook.md` | AI review governance | Advisory only. |
| Governance lane gate output | `docs/governance/governance-lane-review-gate.md` | Governance gate | Gates expose findings; they do not approve work. |
| Risk assessment | `docs/templates/risk-assessment.md` | Templates index | Use only when a task introduces or reviews risk. |

---

## 3. When to Use a Template

Use a template when all of these are true:

```text
[ ] The content will be reused across multiple tasks.
[ ] The template reduces ambiguity or regression risk.
[ ] The owner surface is clear.
[ ] The output can be linked from Jira as evidence.
[ ] The template does not duplicate an existing canonical rule.
[ ] The result remains readable for humans.
```

Use the smallest existing canonical template that fits.

---

## 4. When Not to Create a Template

Do not create a new template when:

```text
[ ] A Jira evidence comment is enough.
[ ] A PR description is enough.
[ ] A Confluence stakeholder summary or form is enough.
[ ] An existing canonical template already covers the need.
[ ] The template would duplicate ADR, Shift Left, evidence, review, gate, or stakeholder rules.
[ ] The template would create another place to maintain the same truth.
[ ] The template exists only to increase file count.
```

New template files require a reviewed GitHub change and Project Owner approval of the scope.

---

## 5. Human Readability and AI Routing

Visible template documentation must stay short, practical, and link-based.

Use visible text for:

- the template purpose;
- when to use it;
- when not to use it;
- the owner surface;
- links to canonical sources.

Use hidden metadata only for:

- AI routing;
- canonical path discovery;
- anti-regression reminders;
- forbidden claim reminders.

Do not hide project decisions only in metadata. If a human needs the decision, it must be visible.

---

## 6. Related Documents

This index must stay aligned with:

- `README.md`;
- `docs/governance/source-of-truth.md`;
- `docs/governance/documentation-strategy.md`;
- `docs/governance/shift-left-governance-baseline.md`;
- `docs/governance/scrum-governance-dor-dod.md`;
- `docs/governance/governance-lane-review-gate.md`;
- `docs/governance/ai-review-agents-policy.md`;
- `docs/governance/ai-review-agent-playbook.md`;
- `docs/governance/stakeholder-transparency.md`;
- `docs/adr/README.md`;
- `docs/adr/template.md`.

If this index conflicts with `docs/governance/source-of-truth.md`, the source-of-truth policy wins until a reviewed GitHub change resolves the conflict.

---

## 7. Practical Rule

```text
Templates reduce repeated ambiguity.
They must not create repeated truth.
```
