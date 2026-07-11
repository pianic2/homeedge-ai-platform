# Project Templates

**Issue:** IHAP-31 — S0-022 — Templates; extended by IHAP-39 — S0-029 — Risk Treatment Workflow and Traceability  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Document type:** Templates index  
**Status:** Sprint 0 draft for review  
**Source of truth:** This versioned GitHub document is the canonical index for reusable project templates until superseded by a later reviewed change.

<!--
AI_AGENT_METADATA:
  issue: IHAP-39
  document_type: templates_index
  canonical_path: docs/templates/README.md
  source_of_truth: github_versioned_repository_documentation
  task_scope: documentation_governance_only
  risk_assessment_template: docs/templates/risk-assessment.md
  risk_model_baseline: docs/risks/risk-model-baseline.md
  adr_template: docs/adr/template.md
  unvalidated_claim_marker: "[UNVALIDATED]"

HIDDEN_ANTI_REGRESSION_RULES:
  - Use existing canonical templates first.
  - The Risk Assessment template produces living Risk Records under docs/risks/records/ only when explicitly approved.
  - Treatment details belong in Risk Records; Jira coordinates work only.
  - Do not duplicate ADR, Shift Left, evidence, review, governance gate, or stakeholder report templates here.
  - Preserve [UNVALIDATED] on unproven claims.
-->

---

## 1. Rule

```text
Use existing canonical templates first.
Create a new template only when it prevents repeated ambiguity and does not duplicate an existing canonical document.
```

This index makes templates easy to find without creating a second copy of rules already owned elsewhere.

---

## 2. Template Inventory

| Need | Use | Owner | Rule |
|---|---|---|---|
| ADR | `docs/adr/template.md` | ADR governance | Use only for stable architectural decisions; declare related risks and treatments when relevant. |
| Shift Left Impact | `docs/governance/shift-left-governance-baseline.md` | Shift Left governance | Copy from the canonical source. |
| Jira evidence comment | `docs/governance/scrum-governance-dor-dod.md` | Scrum governance | Link evidence; do not copy long-form docs into Jira. |
| Stakeholder evidence/report reference | `docs/governance/stakeholder-transparency.md` | Stakeholder transparency | Confluence summarizes and links. |
| AI review finding/summary | `docs/governance/ai-review-agents-policy.md`, `docs/governance/ai-review-agent-playbook.md` | AI review governance | Advisory only. |
| Governance lane gate output | `docs/governance/governance-lane-review-gate.md` | Governance gate | Gates expose findings; they do not approve work. |
| Living Risk Record and treatments | `docs/templates/risk-assessment.md` | Risk governance | Use only when an explicit task creates or reviews a risk. The resulting GitHub Risk Record is the canonical treatment dossier. |

---

## 3. Risk Record Template Rule

The Risk Assessment template supports records that evolve over time. It separates:

- current risk assessment;
- existing controls;
- stable `RT-*` treatments;
- source evidence;
- implementation evidence;
- verification evidence;
- effectiveness review;
- assessment history;
- Project Owner decision.

The template must be used together with `docs/risks/risk-model-baseline.md`.

Jira coordinates treatment tasks, blockers, workflow state, and evidence links. It must not replace the GitHub Risk Record.

---

## 4. When to Use a Template

Use a template when all are true:

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

## 5. When Not to Create a Template

Do not create a new template when:

```text
[ ] A Jira evidence comment is enough.
[ ] A PR description is enough.
[ ] A Confluence stakeholder summary or form is enough.
[ ] An existing canonical template already covers the need.
[ ] The template would create another place to maintain the same truth.
[ ] The template exists only to increase file count.
```

New template files require a reviewed GitHub change and Project Owner approval of scope.

---

## 6. Human Readability and AI Routing

Visible template documentation must stay practical and link-based.

Use visible text for purpose, usage rules, decision boundaries, and canonical links. Use hidden metadata only for routing and anti-regression reminders.

Do not hide project decisions only in metadata.

---

## 7. Related Documents

This index must stay aligned with:

- `docs/governance/source-of-truth.md`;
- `docs/governance/documentation-strategy.md`;
- `docs/risks/README.md`;
- `docs/risks/risk-model-baseline.md`;
- `docs/adr/README.md`;
- `docs/adr/template.md`;
- `docs/governance/shift-left-governance-baseline.md`;
- `docs/governance/scrum-governance-dor-dod.md`;
- `docs/governance/governance-lane-review-gate.md`;
- `docs/governance/ai-review-agents-policy.md`;
- `docs/governance/ai-review-agent-playbook.md`;
- `docs/governance/stakeholder-transparency.md`.

If this index conflicts with `docs/governance/source-of-truth.md`, the source-of-truth policy wins until a reviewed GitHub change resolves the conflict.

---

## 8. Practical Rule

```text
Templates reduce repeated ambiguity.
Risk Records preserve evolving treatment truth.
Templates must not create repeated truth.
```
