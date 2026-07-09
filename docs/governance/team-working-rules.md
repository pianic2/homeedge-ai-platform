# Team Working Rules

**Issue:** IHAP-24 — S0-015 — Team Working Rules  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Document type:** Governance / Working agreement  
**Status:** Sprint 0 draft for review  
**Source of truth:** This versioned GitHub document defines the lightweight team working rules for daily collaboration, evidence discipline, blocker handling, and AI assistant usage boundaries until superseded by a later reviewed change.

<!--
AI_AGENT_METADATA:
  issue: IHAP-24
  document_type: team_working_rules
  source_of_truth: github_versioned_repository_documentation
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
  security_grade_claims_allowed: false
  unvalidated_claim_marker: "[UNVALIDATED]"
  canonical_references:
    root_semantic_index: "README.md"
    source_of_truth: "docs/governance/source-of-truth.md"
    shift_left_governance_baseline: "docs/governance/shift-left-governance-baseline.md"
    scrum_governance_dor_dod: "docs/governance/scrum-governance-dor-dod.md"
    ai_review_agents_policy: "docs/governance/ai-review-agents-policy.md"
    ai_review_agent_playbook: "docs/governance/ai-review-agent-playbook.md"
    governance_lane_review_gate: "docs/governance/governance-lane-review-gate.md"
    stakeholder_transparency: "docs/governance/stakeholder-transparency.md"
    product_vision: "docs/product/product-vision.md"

HIDDEN_ANTI_REGRESSION_RULES:
  - This document is a lightweight working agreement, not a replacement for canonical governance documents.
  - GitHub remains the technical source of truth.
  - Jira remains authoritative for backlog, task state, workflow state, review state, blockers, and evidence links.
  - Confluence remains authoritative for stakeholder hub, stakeholder reports, stakeholder forms, and stakeholder navigation.
  - Project Owner remains the final authority for Ready, Done, final Jira transitions, ADR approval, risk acceptance, and scope changes.
  - AI assistants and review agents are advisory only.
  - AI assistants and review agents must not approve ADRs, close issues, declare Done, or transition Jira issues without explicit Project Owner instruction.
  - Preserve [UNVALIDATED] on unproven claims.
  - Do not introduce firmware, backend, mobile, cloud, runtime, CI enforcement, production-ready, safety-critical, commercial-ready, certification, or security-grade claims.
  - Do not duplicate long-form GitHub technical documentation into Jira or Confluence.
-->

---

## 1. Purpose

This document defines the daily working rules for HomeEdge AI Platform.

It keeps the team workflow small, traceable, reviewable, and evidence-linked.

Core rule:

```text
Work stays small.
Evidence stays linked.
Technical truth stays in GitHub.
Workflow state stays in Jira.
Stakeholder reporting stays in Confluence.
Project Owner decides Ready and Done.
AI supports review but does not approve.
```

This document is governance-only. It does not introduce firmware, backend, mobile, cloud, runtime automation, CI enforcement, production readiness, safety-critical guarantees, commercial readiness, or security-grade certification.

---

## 2. Operating Principles

| Principle | Rule |
|---|---|
| One task, one scope | Work only on the active Jira issue. New scope becomes a separate task or explicit Project Owner decision. |
| Small changes first | Prefer short, reviewable changes over large process documents. |
| Evidence before movement | Do not move work forward without linkable evidence. |
| Review is not approval | Reviews may find issues or no blocking findings. They do not equal Done. |
| Explicit blockers | Blockers must name the problem, impact, affected source, and expected next action. |
| No silent maturity upgrade | Unproven capability, runtime, AI, reliability, security, production, safety, or commercial claims stay `[UNVALIDATED]`. |

---

## 3. Surface Rules

| Surface | Use it for | Do not use it for |
|---|---|---|
| GitHub | Technical truth, source code, versioned documents, policies, ADRs, risks, PR evidence | Task workflow state as the primary authority |
| Jira | Backlog, task state, workflow state, blockers, review state, evidence links | Long-form technical documentation |
| Confluence | Stakeholder hub, stakeholder reports, forms, and navigation | Competing technical source of truth |

Practical rule:

```text
Confluence reports and orients.
Jira tracks and links evidence.
GitHub defines the technical truth.
```

If GitHub and Jira or Confluence disagree on technical content, use `docs/governance/source-of-truth.md`.

---

## 4. Daily Working Rules

1. Start from the Jira issue.
2. Read the canonical GitHub documents named by the issue.
3. Keep changes inside the approved scope.
4. Use a task branch when repository files change.
5. Keep commits Jira-linked.
6. Prefer links and short summaries over copied technical content.
7. Record blockers immediately in Jira when they affect scope, evidence, review, or completion.
8. Do not treat directories, placeholders, drafts, or target boundaries as runtime proof.

---

## 5. Review and Evidence Rules

Every completed or reviewable governance change needs linkable evidence.

Minimum evidence pattern:

```text
Produced: what changed
Source of truth: GitHub file path or repository evidence
PR / Branch / Commit: link
Validation: what was checked
Risks / [UNVALIDATED]: what remains unproven or not applicable
Project Owner action: review / approve / request changes / authorize transition
```

Use `docs/governance/scrum-governance-dor-dod.md` for the full Definition of Ready, Definition of Done, workflow movement, and evidence expectations.

Use `docs/governance/governance-lane-review-gate.md` before moving governance-lane work toward Review, Stakeholder Review, or Done.

---

## 6. Blocker and Risk Handling

A blocker must be explicit enough to act on.

Use this lightweight format:

```text
Blocker:
Impact:
Affected source:
Expected action:
Owner decision needed: yes / no
```

Block movement when the issue contains:

- source-of-truth divergence;
- missing evidence for a completed claim;
- silent MVP expansion;
- unproven claim without `[UNVALIDATED]`;
- unsupported production-ready, safety-critical, commercial-ready, certification, or security-grade claim;
- AI assistant or review agent acting as approver;
- missing Project Owner approval for Ready or Done.

Use `docs/governance/source-of-truth.md` for DOC-REGRESSION severity and resolution flow.

---

## 7. AI Assistant and Review Agent Rules

AI assistants and review agents may:

- propose plans;
- draft documents;
- compare sources;
- identify regressions;
- classify findings;
- recommend corrections;
- produce review summaries.

AI assistants and review agents must not:

- approve ADRs;
- approve architecture changes;
- declare Ready;
- declare Done;
- close issues;
- transition Jira issues without explicit Project Owner instruction;
- remove `[UNVALIDATED]` without traceable evidence;
- introduce production-ready, safety-critical, commercial-ready, certification, or security-grade claims.

Allowed final wording:

```text
No blocking findings detected by this review pass. Project Owner review is still required.
```

Forbidden final wording:

```text
Approved.
Done.
Ready authorized.
ADR accepted.
Production-ready.
Security-grade.
```

Use `docs/governance/ai-review-agents-policy.md` and `docs/governance/ai-review-agent-playbook.md` for the full review-agent model and prompts.

---

## 8. What This Document Does Not Define

This document does not redefine:

- source-of-truth hierarchy;
- DOC-REGRESSION severity;
- Shift Left impact block;
- Definition of Ready;
- Definition of Done;
- governance-lane gates;
- AI review-agent prompts;
- stakeholder report structure;
- Product Vision;
- MVP boundaries;
- architecture implementation;
- runtime behavior.

Use the canonical documents listed in the README semantic index for those rules.

---

## 9. Acceptance Criteria

This document satisfies IHAP-24 when:

```text
[ ] Lightweight team working rules are documented.
[ ] GitHub/Jira/Confluence roles are preserved by reference.
[ ] Project Owner authority for Ready, Done, final transitions, ADR approval, risk acceptance, and scope changes is explicit.
[ ] AI assistants and review agents remain advisory only.
[ ] Evidence-linking expectations are stated without duplicating long-form canonical policies.
[ ] Blocker and risk handling is documented.
[ ] [UNVALIDATED] policy is preserved for unproven claims.
[ ] No firmware, backend, mobile, cloud, runtime, CI enforcement, production-ready, safety-critical, commercial-ready, certification, or security-grade claim is introduced.
```

---

## 10. Practical Rule

```text
Keep work small.
Keep evidence linked.
Keep claims bounded.
Keep agents advisory.
Keep Project Owner decisions explicit.
```
