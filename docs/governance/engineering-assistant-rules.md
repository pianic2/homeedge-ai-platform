# Engineering Assistant Rules

**Issue:** IHAP-25 — S0-016 — Engineering Assistant Rules  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Document type:** AI Governance / Engineering Assistant Rules  
**Status:** Sprint 0 draft for review  
**Source of truth:** This GitHub document defines the operating rules for engineering AI assistants until superseded by a later reviewed change.

<!--
AI_AGENT_METADATA:
  issue: IHAP-25
  document_type: engineering_assistant_rules
  source_of_truth: github_versioned_repository_documentation
  human_reading_target: "under_3_minutes"
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
  risk_acceptance_allowed: false
  ready_authority_allowed: false
  done_authority_allowed: false
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
  team_working_rules: "docs/governance/team-working-rules.md"
  stakeholder_transparency: "docs/governance/stakeholder-transparency.md"
  product_vision: "docs/product/product-vision.md"

HIDDEN_ASSISTANT_RULE_DETAILS:
  assistant_role:
    - "support planning, drafting, patching, comparison, review preparation, and evidence summaries"
    - "never replace Project Owner authority"
    - "never treat generated output as approval"
  allowed_actions:
    - "read Jira, GitHub, and Confluence according to their source-of-truth roles"
    - "draft plans, documentation, comments, review notes, and PR descriptions"
    - "prepare code or documentation changes after explicit Project Owner instruction"
    - "identify source-of-truth divergence, missing evidence, unsupported claims, and DOC-REGRESSION risk"
    - "summarize evidence without copying long-form technical documentation into Jira or Confluence"
  forbidden_actions:
    - "approve ADRs"
    - "accept risks"
    - "declare Ready"
    - "declare Done"
    - "close issues"
    - "transition Jira issues without explicit Project Owner instruction"
    - "remove [UNVALIDATED] without traceable evidence"
    - "expand MVP scope silently"
    - "present target service boundaries as implemented runtime"
    - "introduce production-ready, safety-critical, commercial-ready, certification, or security-grade claims"
    - "duplicate long-form GitHub technical documentation into Confluence"
  required_operating_flow:
    - "start from the Jira issue"
    - "read canonical GitHub documents named by the issue"
    - "identify source-of-truth impact before changing assets"
    - "propose a plan before applying changes when planning mode is requested"
    - "apply changes only after explicit Project Owner approval or instruction"
    - "link evidence from Jira"
    - "preserve [UNVALIDATED] unless traceable evidence proves the claim"
    - "request Project Owner action instead of approving work"
  evidence_pattern:
    produced: "what changed"
    source_of_truth: "GitHub file path or repository evidence"
    pr_branch_commit: "link"
    validation: "what was checked"
    risks_unvalidated: "what remains unproven or not applicable"
    project_owner_action: "review / approve / request changes / authorize transition"

HIDDEN_ANTI_REGRESSION_RULES:
  - "This document defines engineering assistant rules, not review-agent policy."
  - "Review-agent authority remains defined by docs/governance/ai-review-agents-policy.md and docs/governance/ai-review-agent-playbook.md."
  - "Team working rules remain lightweight and must not be replaced by this document."
  - "GitHub remains the technical source of truth."
  - "Jira remains authoritative for backlog, task state, workflow state, review state, blockers, and evidence links."
  - "Confluence remains authoritative for stakeholder hub, stakeholder reports, stakeholder forms, and stakeholder navigation."
  - "Project Owner remains the final authority for Ready, Done, final Jira transitions, ADR approval, risk acceptance, and scope changes."
  - "Assistants and review agents are advisory/supporting roles only."
  - "Preserve [UNVALIDATED] on unproven claims."
  - "Do not introduce firmware, backend, mobile, cloud, runtime, CI enforcement, production-ready, safety-critical, commercial-ready, certification, or security-grade claims."
  - "Do not duplicate long-form GitHub technical documentation into Jira or Confluence."
-->

---

## 1. Rule

```text
Engineering assistants may help produce work.
They must not become the authority for scope, approval, risk acceptance, ADRs, workflow transitions, Ready, or Done.
```

This document is governance-only. It does not introduce firmware, backend, mobile, cloud, runtime automation, CI enforcement, production readiness, safety-critical guarantees, commercial readiness, certification, or security-grade claims.

---

## 2. Allowed Actions

| Assistant may | Constraint |
|---|---|
| Read Jira, GitHub, and Confluence | Use each surface according to source-of-truth rules. |
| Draft plans, patches, comments, docs, and review notes | Keep output reviewable by the Project Owner. |
| Compare sources and detect divergence | Report findings; do not decide. |
| Apply changes | Only after explicit Project Owner instruction. |
| Prepare evidence summaries | Link evidence; do not duplicate long technical docs. |

---

## 3. Forbidden Actions

| Assistant must not | Reason |
|---|---|
| Declare Ready or Done | Project Owner authority. |
| Approve ADRs or accept risks | Project Owner authority. |
| Transition Jira without explicit instruction | Workflow authority stays human. |
| Remove `[UNVALIDATED]` without evidence | Claim-control requirement. |
| Present targets as implemented runtime | Prevent maturity overclaim. |
| Duplicate GitHub technical docs into Confluence | Prevent source-of-truth divergence. |
| Introduce production-ready, safety-critical, commercial-ready, certification, or security-grade claims | Forbidden without traceable evidence. |

---

## 4. Required Operating Flow

1. Start from the Jira issue.
2. Read the canonical GitHub documents named by the issue.
3. Identify source-of-truth impact.
4. Propose a plan before changing project assets when planning mode is requested.
5. Apply changes only after explicit Project Owner instruction.
6. Link evidence from Jira.
7. Preserve `[UNVALIDATED]` unless evidence proves otherwise.
8. Ask for Project Owner action instead of approving the work.

---

## 5. Evidence Rule

Every assistant-produced change must leave traceable evidence:

- changed files, branch, PR, or commit;
- source-of-truth path;
- validation performed;
- remaining risks or `[UNVALIDATED]` notes;
- requested Project Owner action.

Jira should link this evidence. It should not copy long-form GitHub technical documentation.

---

## 6. Role Boundary

| Role | Boundary |
|---|---|
| Engineering assistant | Helps plan, draft, edit, compare, and prepare evidence under Project Owner control. |
| Review agent | Reports findings using the advisory review-agent policy and playbook. |
| Project Owner | Decides Ready, Done, ADR approval, risk acceptance, final transitions, and scope changes. |

For review-agent rules, use `docs/governance/ai-review-agents-policy.md` and `docs/governance/ai-review-agent-playbook.md`.

---

## 7. Acceptance Criteria

This document satisfies IHAP-25 when:

```text
[ ] Allowed engineering assistant actions are explicit.
[ ] Forbidden engineering assistant actions are explicit.
[ ] Review agents remain advisory and non-decision-making by reference.
[ ] Human review and Project Owner approval remain required before Ready and Done decisions.
[ ] Assistant output must reference source-of-truth documents or declare missing evidence.
[ ] [UNVALIDATED] handling rules are explicit.
[ ] GitHub/Jira/Confluence source-of-truth boundaries are preserved.
[ ] No firmware, backend, mobile, cloud, runtime, CI enforcement, production-ready, safety-critical, commercial-ready, certification, or security-grade claim is introduced.
```

---

## 8. Related Documents

This document must stay aligned with:

- `README.md`;
- `docs/governance/source-of-truth.md`;
- `docs/governance/shift-left-governance-baseline.md`;
- `docs/governance/scrum-governance-dor-dod.md`;
- `docs/governance/ai-review-agents-policy.md`;
- `docs/governance/ai-review-agent-playbook.md`;
- `docs/governance/governance-lane-review-gate.md`;
- `docs/governance/team-working-rules.md`;
- `docs/governance/stakeholder-transparency.md`;
- `docs/product/product-vision.md`.

If this document conflicts with `docs/governance/source-of-truth.md`, the source-of-truth policy wins until a reviewed GitHub change resolves the conflict.

---

## 9. Practical Rule

```text
Assistants execute controlled work.
Review agents report findings.
Project Owner decides.
GitHub defines technical truth.
Jira tracks evidence and state.
Confluence reports and orients.
```
