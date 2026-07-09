# Documentation

**Issue:** IHAP-33 — S0-023 — Docs Landing Page  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Document type:** Documentation landing page  
**Status:** Sprint 0 draft for review  
**Reading target:** less than 2 minutes for humans.  
**Source of truth:** This versioned GitHub document is the canonical landing page for documentation under `docs/` until superseded by a later reviewed change.

<!--
AI_AGENT_METADATA:
  issue: IHAP-33
  document_type: docs_landing_page
  canonical_path: docs/README.md
  source_of_truth: github_versioned_repository_documentation
  source_of_truth_policy: docs/governance/source-of-truth.md
  documentation_strategy: docs/governance/documentation-strategy.md
  root_semantic_index: README.md
  task_scope: documentation_navigation_only
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

HIDDEN_ANTI_REGRESSION_RULES:
  - This page is a navigational index only.
  - This page must not replace README.md as the repository semantic index.
  - This page must not replace docs/governance/source-of-truth.md as the source-of-truth policy.
  - This page must not duplicate long-form governance, product, ADR, template, or stakeholder report content.
  - GitHub remains the technical source of truth.
  - Jira remains authoritative for backlog, task state, workflow state, blockers, review state, and evidence links.
  - Confluence remains authoritative for stakeholder hub, stakeholder reports, stakeholder forms, and stakeholder navigation.
  - Future candidate paths listed here are not validated or created by this page.
  - Preserve [UNVALIDATED] on unproven claims.
  - Do not expand the MVP boundary silently.
-->

---

## 1. Start Here

| Need | Go to | Status |
|---|---|---|
| Repository overview | `../README.md` | Existing canonical repository index |
| Source-of-truth rules | `governance/source-of-truth.md` | Existing canonical policy |
| Documentation strategy | `governance/documentation-strategy.md` | Existing canonical strategy |
| Product Vision and MVP boundary | `product/product-vision.md` | Existing canonical product document |
| ADR index and template | `adr/README.md`, `adr/template.md` | Existing canonical ADR documents |
| Project templates | `templates/README.md` | Existing canonical template index |

This page links documentation sources. It does not redefine them.

---

## 2. Documentation Areas

| Area | Path | What belongs here |
|---|---|---|
| Governance | `governance/` | Source-of-truth rules, workflow rules, review gates, assistant rules, documentation strategy. |
| Product | `product/` | Product Vision, MVP boundaries, scope language, and current glossary. |
| ADRs | `adr/` | Architecture decisions and ADR template. |
| Templates | `templates/` | Reusable project templates and template inventory. |
| Architecture | `architecture/` | Architecture notes only when they reduce ambiguity and do not duplicate Product Vision or ADRs. |
| Risks | future `risks/` | Candidate area for risk records only when a task explicitly introduces or reviews risk. |
| Reviews / Evidence | future `reviews/` or `evidence/` | Candidate area for durable evidence only when Jira or PR links are not enough. |
| Glossary | future `glossary/project-glossary.md` | Candidate file only if the current glossary is later extracted from Product Vision by reviewed task. |

Future paths are not created, validated, or accepted just because they are listed here.

---

## 3. Current Canonical Documents

### Governance

- `governance/source-of-truth.md`
- `governance/documentation-strategy.md`
- `governance/shift-left-governance-baseline.md`
- `governance/scrum-governance-dor-dod.md`
- `governance/governance-lane-review-gate.md`
- `governance/ai-review-agents-policy.md`
- `governance/ai-review-agent-playbook.md`
- `governance/stakeholder-transparency.md`
- `governance/team-working-rules.md`
- `governance/engineering-assistant-rules.md`

### Product

- `product/product-vision.md`

### ADR

- `adr/README.md`
- `adr/template.md`

### Templates

- `templates/README.md`
- `templates/risk-assessment.md`

---

## 4. Non-Duplication Rule

```text
Link canonical sources.
Do not copy their rules here.
```

This page must not duplicate:

- source-of-truth policy;
- Documentation Strategy;
- MVP boundary;
- ADR naming, status, or approval rules;
- Shift Left, review-agent, governance-gate, or evidence templates;
- stakeholder reports;
- runtime, production-ready, safety-critical, commercial-ready, certification, or security-grade claims.

---

## 5. Stakeholder Navigation

Use the surfaces this way:

```text
GitHub defines technical truth.
Jira tracks work state and evidence.
Confluence orients stakeholders through hub, reports, forms, and navigation.
```

Confluence may summarize and link. It must not duplicate long-form GitHub technical documentation.

---

## 6. Practical Rule

```text
Use README.md for repository-level navigation.
Use docs/README.md for documentation navigation.
Use canonical documents for actual project truth.
```
