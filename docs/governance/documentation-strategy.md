# Documentation Strategy

**Issue:** IHAP-29 — S0-020 — Documentation Strategy  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Document type:** Governance / Documentation Strategy  
**Status:** Sprint 0 draft for review  
**Reading target:** less than 3 minutes for humans; hidden metadata supports AI routing and anti-regression checks.  
**Source of truth:** This versioned GitHub document defines the documentation strategy for HomeEdge AI Platform until superseded by a later reviewed change.

<!--
AI_AGENT_METADATA:
  issue: IHAP-29
  document_type: documentation_strategy
  canonical_path: docs/governance/documentation-strategy.md
  source_of_truth: github_versioned_repository_documentation
  source_of_truth_policy: docs/governance/source-of-truth.md
  shift_left_governance_baseline: docs/governance/shift-left-governance-baseline.md
  scrum_governance_dor_dod: docs/governance/scrum-governance-dor-dod.md
  governance_lane_review_gate: docs/governance/governance-lane-review-gate.md
  stakeholder_transparency: docs/governance/stakeholder-transparency.md
  ai_review_agents_policy: docs/governance/ai-review-agents-policy.md
  ai_review_agent_playbook: docs/governance/ai-review-agent-playbook.md
  product_vision: docs/product/product-vision.md
  adr_index: docs/adr/README.md
  adr_template: docs/adr/template.md
  task_scope: documentation_governance_only
  runtime_changes_allowed: false
  firmware_changes_allowed: false
  backend_changes_allowed: false
  mobile_changes_allowed: false
  cloud_changes_allowed: false
  ci_runtime_enforcement_allowed: false
  production_ready_claims_allowed: false
  safety_critical_claims_allowed: false
  commercial_ready_claims_allowed: false
  certification_claims_allowed: false
  security_grade_claims_allowed: false
  unvalidated_claim_marker: "[UNVALIDATED]"

HIDDEN_ANTI_REGRESSION_RULES:
  - GitHub remains the technical source of truth for versioned technical documentation, code, decisions, risks, policies, governance baselines, ADRs, and PR evidence.
  - Jira remains authoritative for backlog, task state, workflow state, blockers, review state, and evidence links.
  - Confluence remains authoritative for stakeholder hub, stakeholder reports, stakeholder forms, and stakeholder navigation.
  - Confluence must summarize and link; it must not duplicate long-form GitHub technical documentation.
  - Do not create documents only to increase the file count.
  - Do not duplicate rules already defined by canonical documents; link them instead.
  - README.md and docs/governance/source-of-truth.md must be updated when canonical documentation paths are added, moved, renamed, or deprecated.
  - Preserve [UNVALIDATED] on every unproven claim.
  - Do not expand MVP scope silently.
  - Do not introduce firmware, backend, mobile, cloud, runtime, production-ready, safety-critical, commercial-ready, certification, or security-grade claims.
-->

---

## 1. Rule

```text
GitHub defines technical truth.
Jira tracks work and evidence.
Confluence orients stakeholders.
Documents stay minimal, linked, and current.
```

This strategy defines how HomeEdge documentation should grow without creating parallel truths, stale files, or unreadable governance documents.

---

## 2. Document Families

| Family | Canonical surface | Use for |
|---|---|---|
| Root index | `README.md` | Repository overview, semantic navigation, canonical links, maturity warnings. |
| Governance | `docs/governance/` | Source-of-truth rules, workflow rules, review gates, assistant rules, documentation strategy. |
| Product | `docs/product/` | Product Vision, MVP boundaries, glossary, scope language. |
| ADRs | `docs/adr/` | Architecture decisions that need durable traceability. |
| Architecture | `docs/architecture/` | Architecture notes only when they reduce ambiguity and do not duplicate Product Vision or ADRs. |
| Risk assessments | future `docs/risks/` | Risk records only when a task explicitly introduces or reviews risk. |
| Reviews / evidence | future `docs/reviews/` or `docs/evidence/` | Durable evidence only when Jira/PR links are not enough. |
| Stakeholder reports | Confluence | Short stakeholder-facing progress, risks, forms, and navigation. |

Future folders must not be created just because they are listed here. Create them only when a task needs them and the Project Owner approves the scope.

---

## 3. When to Create a New Document

Create a new document only when all of these are true:

```text
[ ] The topic has durable value beyond one Jira comment or PR description.
[ ] The topic would make an existing document too large or unclear.
[ ] The document has one clear responsibility.
[ ] The canonical path is obvious.
[ ] The document can be linked from README.md or another canonical document.
[ ] The document will not duplicate an existing rule, ADR, policy, or Product Vision section.
```

Do not create a document when a Jira evidence comment, PR description, Confluence stakeholder summary, or link to an existing canonical file is enough.

---

## 4. When to Update an Existing Document

Update the existing canonical document when changing:

| Change | Update |
|---|---|
| Project source-of-truth roles, DOC-REGRESSION, canonical paths, commit convention, `[UNVALIDATED]` policy | `docs/governance/source-of-truth.md` |
| Repository semantic navigation or visible canonical links | `README.md` |
| Product Vision, MVP boundary, glossary, target/runtime language | `docs/product/product-vision.md` |
| Jira workflow, Definition of Ready, Definition of Done, evidence expectations | `docs/governance/scrum-governance-dor-dod.md` |
| Governance-lane movement checks | `docs/governance/governance-lane-review-gate.md` |
| Stakeholder visibility, Confluence report behavior, redaction rules | `docs/governance/stakeholder-transparency.md` |
| ADR naming, status, link policy, or template | `docs/adr/README.md` or `docs/adr/template.md` |

If the change is only task status, blocker state, review state, or an evidence link, update Jira instead of changing GitHub docs.

---

## 5. GitHub / Jira / Confluence Policy

| Surface | Responsible for | Must not become |
|---|---|---|
| GitHub | Technical truth, versioned docs, code, ADRs, risks, policies, PR evidence | Workflow-state authority |
| Jira | Backlog, task state, review state, blockers, evidence links | Long-form technical documentation |
| Confluence | Stakeholder hub, stakeholder reports, forms, navigation | Competing technical source of truth |

Confluence may explain and link. It must not copy long-form GitHub technical documents as official technical truth.

---

## 6. Anti-Stale Policy

A document is stale when it contradicts the current canonical source, points to obsolete paths, weakens `[UNVALIDATED]`, or hides changed scope behind outdated summaries.

Use this rule:

```text
Change the source where the truth lives.
Update indexes when paths change.
Update summaries when stakeholder navigation changes.
Do not copy long-form technical truth across tools.
```

Minimum maintenance rules:

```text
[ ] Add or move a canonical document -> update README.md.
[ ] Add or move a canonical source-of-truth path -> update docs/governance/source-of-truth.md.
[ ] Change technical truth -> update GitHub through review.
[ ] Change task state or blocker/evidence links -> update Jira.
[ ] Change stakeholder summary/report/navigation -> update Confluence.
[ ] Reference an unproven claim -> preserve [UNVALIDATED].
[ ] Find duplicated or divergent technical text outside GitHub -> replace it with a short summary and link.
```

---

## 7. Human Readability and AI Routing

Visible documentation should be short, practical, and link-based.

Use visible text for:

- the rule;
- the decision;
- the scope;
- the owner surface;
- the checklist;
- the link to deeper canonical material.

Use hidden metadata only for:

- AI routing;
- canonical path discovery;
- anti-regression constraints;
- forbidden claim reminders;
- tool/surface responsibility hints.

Do not hide project decisions only in metadata. If a human needs the decision, it must be visible.

---

## 8. Review Checklist

Before moving this documentation strategy toward review, check:

```text
[ ] GitHub remains the technical source of truth.
[ ] Jira remains the backlog, state, blocker, review, and evidence-link surface.
[ ] Confluence remains stakeholder hub, report, form, and navigation surface.
[ ] README.md links this document when it becomes canonical.
[ ] docs/governance/source-of-truth.md registers this canonical path.
[ ] No existing canonical rule is duplicated as a competing policy.
[ ] No new document family is created without a concrete task need.
[ ] [UNVALIDATED] is preserved on unproven claims.
[ ] MVP boundary is not expanded.
[ ] No runtime, production-ready, safety-critical, commercial-ready, certification, or security-grade claim is introduced.
```

---

## 9. Related Documents

This strategy must stay aligned with:

- `README.md`;
- `docs/governance/source-of-truth.md`;
- `docs/governance/shift-left-governance-baseline.md`;
- `docs/governance/scrum-governance-dor-dod.md`;
- `docs/governance/governance-lane-review-gate.md`;
- `docs/governance/stakeholder-transparency.md`;
- `docs/governance/ai-review-agents-policy.md`;
- `docs/governance/ai-review-agent-playbook.md`;
- `docs/product/product-vision.md`;
- `docs/adr/README.md`;
- `docs/adr/template.md`.

If this document conflicts with `docs/governance/source-of-truth.md`, the source-of-truth policy wins until a reviewed GitHub change resolves the conflict.

---

## 10. Practical Rule

```text
Create documents when they reduce future confusion.
Do not create documents when they create another place to maintain the same truth.
```
