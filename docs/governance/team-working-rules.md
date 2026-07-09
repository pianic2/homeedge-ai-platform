# Team Working Rules

**Issue:** IHAP-24 — S0-015 — Team Working Rules  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Document type:** Governance / Working agreement  
**Status:** Sprint 0 draft for review  
**Source of truth:** This GitHub document defines the lightweight working rules for the project team until superseded by a later reviewed change.

<!--
AI_AGENT_METADATA:
  issue: IHAP-24
  document_type: team_working_rules
  source_of_truth: github_versioned_repository_documentation
  human_reading_target: "under_2_minutes"
  task_scope: documentation_governance_only
  runtime_changes_allowed: false
  firmware_changes_allowed: false
  backend_changes_allowed: false
  mobile_changes_allowed: false
  cloud_changes_allowed: false
  ci_runtime_enforcement_allowed: false
  autonomous_decision_authority: false
  issue_transition_allowed_without_project_owner_instruction: false
  issue_closure_allowed_without_project_owner_instruction: false
  adr_approval_allowed: false
  production_ready_claims_allowed: false
  safety_critical_claims_allowed: false
  commercial_ready_claims_allowed: false
  certification_claims_allowed: false
  security_grade_claims_allowed: false
  unvalidated_claim_marker: "[UNVALIDATED]"

CANONICAL_REFERENCES:
  root_semantic_index: "README.md"
  source_of_truth: "docs/governance/source-of-truth.md"
  shift_left_governance_baseline: "docs/governance/shift-left-governance-baseline.md"
  scrum_governance_dor_dod: "docs/governance/scrum-governance-dor-dod.md"
  ai_review_agents_policy: "docs/governance/ai-review-agents-policy.md"
  ai_review_agent_playbook: "docs/governance/ai-review-agent-playbook.md"
  governance_lane_review_gate: "docs/governance/governance-lane-review-gate.md"
  engineering_assistant_rules: "docs/governance/engineering-assistant-rules.md"
  stakeholder_transparency: "docs/governance/stakeholder-transparency.md"
  product_vision: "docs/product/product-vision.md"

HIDDEN_WORKING_RULE_DETAILS:
  surface_rules:
    github:
      role: "technical truth, source code, versioned documents, policies, ADRs, risks, PR evidence"
      not_for: "primary workflow state authority"
    jira:
      role: "backlog, task state, workflow state, blockers, review state, evidence links"
      not_for: "long-form technical documentation"
    confluence:
      role: "stakeholder hub, stakeholder reports, stakeholder forms, navigation"
      not_for: "competing technical source of truth"
  daily_working_rules:
    - "Start from the Jira issue."
    - "Read the canonical GitHub documents named by the issue."
    - "Keep changes inside approved scope."
    - "Use a task branch when repository files change."
    - "Keep commits Jira-linked."
    - "Prefer links and short summaries over copied technical content."
    - "Record blockers immediately when they affect scope, evidence, review, or completion."
    - "Do not treat directories, placeholders, drafts, or target boundaries as runtime proof."
  evidence_pattern:
    produced: "what changed"
    source_of_truth: "GitHub file path or repository evidence"
    pr_branch_commit: "link"
    validation: "what was checked"
    risks_unvalidated: "what remains unproven or not applicable"
    project_owner_action: "review / approve / request changes / authorize transition"
  blocker_pattern:
    blocker: "problem"
    impact: "effect on scope/evidence/review/completion"
    affected_source: "canonical source or Jira issue"
    expected_action: "fix, defer, reject, or Project Owner decision"
    owner_decision_needed: "yes / no"
  block_movement_when:
    - "source-of-truth divergence exists"
    - "evidence is missing for a completed claim"
    - "MVP scope is silently expanded"
    - "unproven claim lacks [UNVALIDATED]"
    - "unsupported production-ready, safety-critical, commercial-ready, certification, or security-grade claim appears"
    - "AI assistant or review agent acts as approver"
    - "Project Owner approval is missing for Ready or Done"
  ai_assistants_may:
    - "propose plans"
    - "draft documents"
    - "compare sources"
    - "identify regressions"
    - "classify findings"
    - "recommend corrections"
    - "produce review summaries"
  ai_assistants_must_not:
    - "approve ADRs"
    - "approve architecture changes"
    - "declare Ready"
    - "declare Done"
    - "close issues"
    - "transition Jira issues without explicit Project Owner instruction"
    - "remove [UNVALIDATED] without traceable evidence"
    - "introduce production-ready, safety-critical, commercial-ready, certification, or security-grade claims"
  allowed_ai_final_wording: "No blocking findings detected by this review pass. Project Owner review is still required."
  forbidden_ai_final_wording:
    - "Approved."
    - "Done."
    - "Ready authorized."
    - "ADR accepted."
    - "Production-ready."
    - "Security-grade."

HIDDEN_ANTI_REGRESSION_RULES:
  - "This document is a lightweight working agreement, not a replacement for canonical governance documents."
  - "GitHub remains the technical source of truth."
  - "Jira remains authoritative for backlog, task state, workflow state, review state, blockers, and evidence links."
  - "Confluence remains authoritative for stakeholder hub, stakeholder reports, stakeholder forms, and stakeholder navigation."
  - "Project Owner remains the final authority for Ready, Done, final Jira transitions, ADR approval, risk acceptance, and scope changes."
  - "AI assistants and review agents are advisory only."
  - "Preserve [UNVALIDATED] on unproven claims."
  - "Do not introduce firmware, backend, mobile, cloud, runtime, CI enforcement, production-ready, safety-critical, commercial-ready, certification, or security-grade claims."
  - "Do not duplicate long-form GitHub technical documentation into Jira or Confluence."
-->

---

## 1. Rule

```text
Work stays small.
Evidence stays linked.
GitHub defines technical truth.
Jira tracks workflow and evidence.
Confluence reports and orients stakeholders.
Project Owner decides Ready and Done.
AI supports review but does not approve.
```

---

## 2. How We Work

| Rule | Meaning |
|---|---|
| One task, one scope | Do not expand a Jira issue silently. New scope becomes a new task or an explicit Project Owner decision. |
| Evidence before movement | Work can move forward only when the evidence can be linked from Jira. |
| Review is not approval | Review can report findings. Done requires Project Owner approval. |
| Claims stay bounded | Unproven claims keep `[UNVALIDATED]`. Forbidden maturity claims stay out. |
| Confluence stays readable | Stakeholder pages summarize and link; they do not duplicate GitHub technical docs. |

---

## 3. Canonical References

| Need | Use |
|---|---|
| Source of truth, DOC-REGRESSION, `[UNVALIDATED]`, commit convention | `docs/governance/source-of-truth.md` |
| Shift Left impact block | `docs/governance/shift-left-governance-baseline.md` |
| Ready, Done, workflow movement, evidence expectations | `docs/governance/scrum-governance-dor-dod.md` |
| AI review-agent limits and prompts | `docs/governance/ai-review-agents-policy.md`, `docs/governance/ai-review-agent-playbook.md` |
| Engineering assistant operating rules | `docs/governance/engineering-assistant-rules.md` |
| Governance-lane movement | `docs/governance/governance-lane-review-gate.md` |
| Stakeholder visibility and Confluence behavior | `docs/governance/stakeholder-transparency.md` |
| Product Vision and MVP boundary | `docs/product/product-vision.md` |

---

## 4. Practical Rule

```text
Keep work small.
Keep evidence linked.
Keep claims bounded.
Keep agents advisory.
Keep Project Owner decisions explicit.
```
