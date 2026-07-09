# Documentation

**Issue:** IHAP-33 — S0-023 — Docs Landing Page  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Document type:** Documentation landing page  
**Status:** Sprint 0 draft for review  
**Reading target:** less than 2 minutes for humans.  
**Source of truth:** This page is the canonical navigation entry point for documentation under `docs/`. It links canonical documents; it does not replace them.

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

  canonical_documents:
    governance:
      - docs/governance/source-of-truth.md
      - docs/governance/documentation-strategy.md
      - docs/governance/shift-left-governance-baseline.md
      - docs/governance/scrum-governance-dor-dod.md
      - docs/governance/governance-lane-review-gate.md
      - docs/governance/ai-review-agents-policy.md
      - docs/governance/ai-review-agent-playbook.md
      - docs/governance/stakeholder-transparency.md
      - docs/governance/stakeholder-report-data-rules.md
      - docs/governance/team-working-rules.md
      - docs/governance/engineering-assistant-rules.md
    product:
      - docs/product/product-vision.md
    risks:
      - docs/risks/README.md
      - docs/risks/risk-model-baseline.md
    adr:
      - docs/adr/README.md
      - docs/adr/template.md
    templates:
      - docs/templates/README.md
      - docs/templates/risk-assessment.md

  future_candidate_paths:
    - docs/reviews/
    - docs/evidence/
    - docs/glossary/project-glossary.md

HIDDEN_ANTI_REGRESSION_RULES:
  - This page is a navigational index only.
  - This page must not replace README.md as the repository semantic index.
  - This page must not replace docs/governance/source-of-truth.md as the source-of-truth policy.
  - This page must not duplicate long-form governance, product, risk, ADR, template, or stakeholder report content.
  - Future candidate paths listed here are not validated or created by this page.
  - Preserve [UNVALIDATED] on unproven claims.
  - Do not expand the MVP boundary silently.
-->

---

## 1. Start Here

| Need | Go to |
|---|---|
| Repository overview | `../README.md` |
| Source-of-truth rules | `governance/source-of-truth.md` |
| Documentation strategy | `governance/documentation-strategy.md` |
| Product Vision / MVP boundary | `product/product-vision.md` |
| Risk model baseline | `risks/risk-model-baseline.md` |
| ADR index | `adr/README.md` |
| Templates | `templates/README.md` |
| Stakeholder report data rules | `governance/stakeholder-report-data-rules.md` |

---

## 2. Documentation Map

| Area | Path | Status |
|---|---|---|
| Governance | `governance/` | Existing documentation family |
| Product | `product/` | Existing documentation family |
| Risks | `risks/` | Risk model baseline and future explicitly approved risk records |
| ADRs | `adr/` | Existing documentation family |
| Templates | `templates/` | Existing documentation family |
| Architecture | `architecture/` | Existing area; use only when needed |
| Reviews / Evidence | future `reviews/` or `evidence/` | Candidate only |
| Glossary | future `glossary/project-glossary.md` | Candidate only; current glossary stays in `product/product-vision.md` |

Future paths are not created, validated, or accepted just because they are listed here.

---

## 3. Rule

```text
README.md routes the repository.
docs/README.md routes documentation.
Canonical documents define the truth.
```

For source-of-truth ownership, stakeholder surfaces, `[UNVALIDATED]`, MVP boundaries, and DOC-REGRESSION rules, use `governance/source-of-truth.md`.
