# Scrum Governance, Definition of Ready and Definition of Done

**Issue:** IHAP-23 — S0-014 — Scrum Governance, DoR and DoD  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Document type:** Governance / Scrum baseline  
**Status:** Sprint 0 draft for review  
**Source of truth:** This versioned GitHub document is the canonical Scrum governance baseline for Definition of Ready, Definition of Done, Jira workflow movement, and minimum evidence expectations until superseded by a later reviewed change.

<!--
AI_AGENT_METADATA:
  issue: IHAP-23
  document_type: scrum_governance_dor_dod
  source_of_truth: github_versioned_repository_documentation
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
  security_grade_claims_allowed: false
  autonomous_decision_authority: false
  issue_transition_allowed_without_project_owner_instruction: false
  issue_closure_allowed_without_project_owner_instruction: false
  unvalidated_claim_marker: "[UNVALIDATED]"
  source_of_truth_boundaries: "docs/governance/source-of-truth.md"
  shift_left_impact_block: "docs/governance/shift-left-governance-baseline.md"
  ai_review_agent_authority: "docs/governance/ai-review-agents-policy.md"
  ai_review_agent_prompts: "docs/governance/ai-review-agent-playbook.md"
  governance_lane_movement_gate: "docs/governance/governance-lane-review-gate.md"
  stakeholder_visibility_rules: "docs/governance/stakeholder-transparency.md"
  mvp_boundary: "docs/product/product-vision.md"
  agent_routing:
    - Use this document only for Scrum readiness, workflow movement, evidence expectations, and completion criteria.
    - Use source-of-truth.md for GitHub/Jira/Confluence authority, DOC-REGRESSION severity, canonical paths, commit convention, and [UNVALIDATED] policy.
    - Use shift-left-governance-baseline.md for the mandatory impact block and impact dimensions.
    - Use ai-review-agents-policy.md and ai-review-agent-playbook.md for review-agent authority, severity labels, output language, and prompts.
    - Use governance-lane-review-gate.md before moving governance-lane work toward Review, Stakeholder Review, or Done.
    - Use stakeholder-transparency.md for stakeholder-facing summaries, Confluence behavior, and Jira evidence comment expectations.
    - Use product-vision.md for MVP scope and forbidden product/implementation claims.
  anti_regression_rules:
    - This document must not duplicate long-form rules from the canonical documents listed above.
    - GitHub remains technical source of truth; Jira tracks state/evidence; Confluence reports and orients.
    - Project Owner decides Ready, Done, and final workflow transitions.
    - AI review agents report findings only.
    - Preserve [UNVALIDATED] on unproven claims.
    - Do not introduce production-ready, safety-critical, commercial-ready, certification, or security-grade claims.
-->

---

## 1. Purpose

This document defines the lightweight Scrum baseline used by HomeEdge AI Platform to decide when work is ready, reviewable, stakeholder-visible, and done.

It covers only:

- Definition of Ready;
- Definition of Done;
- Jira workflow movement meaning;
- minimum evidence expectations;
- Project Owner authority for Ready and Done.

Core rule:

```text
Ready means work can start without guessing.
Review means work is inspectable.
Stakeholder Review means work is visible to stakeholders.
Done means evidence exists and the Project Owner approved completion.
```

This document is governance-only. It does not introduce firmware, backend, mobile, cloud, runtime automation, CI enforcement, production readiness, safety-critical guarantees, commercial readiness, or security-grade certification.

---

## 2. Scope and Canonical References

This document coordinates existing governance rules. It does not replace them.

| Need | Use |
|---|---|
| Source-of-truth boundaries, DOC-REGRESSION severity, canonical paths, `[UNVALIDATED]` policy | `docs/governance/source-of-truth.md` |
| Mandatory Shift Left Impact block | `docs/governance/shift-left-governance-baseline.md` |
| AI review-agent limits and review language | `docs/governance/ai-review-agents-policy.md` |
| AI review-agent prompts and operating flow | `docs/governance/ai-review-agent-playbook.md` |
| Governance-lane movement checks | `docs/governance/governance-lane-review-gate.md` |
| Stakeholder visibility and Confluence behavior | `docs/governance/stakeholder-transparency.md` |
| Product Vision and MVP boundary | `docs/product/product-vision.md` |

If this document conflicts with `docs/governance/source-of-truth.md`, the source-of-truth policy wins until a reviewed GitHub change resolves the conflict.

---

## 3. Jira Workflow Meaning

| State | Meaning | Exit requirement |
|---|---|---|
| Backlog | Candidate work, not yet ready. | Project Owner refinement or prioritization. |
| Pronto | Ready for execution. | Work starts or Project Owner changes priority. |
| In Progress | Work is actively being changed. | Reviewable evidence exists. |
| In Review | Work is inspectable. | Blocking findings are fixed or explicitly handled by Project Owner. |
| Stakeholder Review | Work is stable enough for stakeholder visibility. | Project Owner accepts as Done or requests changes. |
| Done | Work is complete. | No further workflow movement expected. |

Review and Stakeholder Review are not approval states. Done requires Project Owner approval.

---

## 4. Definition of Ready

A task is Ready only when it has enough structure to start without guessing.

Minimum Definition of Ready:

```text
[ ] Issue type is clear.
[ ] Goal is clear.
[ ] Scope is explicit.
[ ] Non-scope is explicit where relevant.
[ ] Acceptance criteria are concrete and verifiable.
[ ] Evidence expectation is stated.
[ ] Owner, assignee, or explicit owner note exists.
[ ] Dependencies and blockers are noted or explicitly marked not applicable.
[ ] Source-of-truth surfaces are identified when technical truth changes.
[ ] Mandatory Shift Left Impact block is present and ordered.
[ ] Required review perspectives are identifiable when relevant.
[ ] No silent MVP expansion is introduced.
[ ] No unproven claim appears without [UNVALIDATED].
[ ] Project Owner accepts the task as ready.
```

The detailed Shift Left block format is defined in `docs/governance/shift-left-governance-baseline.md`.

---

## 5. Definition of Done

A task is Done only when the project can prove what changed, where the evidence lives, and who approved completion.

Minimum Definition of Done:

```text
[ ] Acceptance criteria are satisfied or explicitly deferred/rejected by Project Owner decision.
[ ] Evidence is linked from Jira.
[ ] GitHub PR, commit, diff, or document evidence exists when technical truth changed.
[ ] Relevant source-of-truth documents are updated when project truth changed.
[ ] Jira status, review state, blockers, and evidence links are coherent.
[ ] No unresolved blocker remains.
[ ] No unresolved BLOCKER finding remains.
[ ] No unresolved MAJOR finding affects source-of-truth, MVP scope, evidence, claim maturity, stakeholder correctness, or approval authority.
[ ] No unresolved S0/S1 DOC-REGRESSION remains.
[ ] [UNVALIDATED] is preserved on all unproven claims.
[ ] Forbidden maturity claims are absent unless backed by traceable evidence.
[ ] Stakeholder-facing impact is clear when applicable.
[ ] Project Owner approval is recorded.
```

Done must not be used for work that is only drafted, only reviewed by an advisory agent, or only visible to stakeholders.

---

## 6. Minimum Evidence by Task Type

| Task type | Minimum evidence |
|---|---|
| Documentation-only | GitHub file path, branch/PR link, reviewable diff, Jira evidence comment, explicit note that no runtime behavior changed. |
| Governance | Canonical GitHub document, README/source-of-truth updates when a canonical path changes, Jira evidence link, governance-lane gate when relevant. |
| Implementation | PR/commit link, tests/build/logs/manual verification as appropriate, updated docs, `[UNVALIDATED]` marker where runtime proof is missing. |
| Stakeholder-facing | Confluence page/report link when changed, Jira evidence link, GitHub source-of-truth link for technical claims, confirmation that Confluence summarizes and links only. |

Implementation claims require implementation evidence. Target architecture claims without implementation evidence must remain `[UNVALIDATED]`.

---

## 7. Jira Evidence Comment Template

```text
Produced:
- <what changed>

Source of truth:
- <GitHub file path or repository evidence>

PR / Branch / Commit:
- <link>

Validation:
- <what was checked>

Risks / [UNVALIDATED]:
- <what remains unproven or not applicable>

Project Owner action:
- review / approve / request changes / authorize transition
```

Jira evidence comments should link to evidence. They should not copy long-form GitHub technical documentation.

---

## 8. Blocking Rules

Movement toward Review, Stakeholder Review, or Done is blocked when one of these exists:

```text
[ ] Missing evidence for completed claim.
[ ] Source-of-truth divergence.
[ ] Silent MVP expansion.
[ ] Unproven claim without [UNVALIDATED].
[ ] Unresolved S0/S1 DOC-REGRESSION.
[ ] Review-blocking S2 DOC-REGRESSION.
[ ] Unsupported production-ready, safety-critical, commercial-ready, certification, or security-grade claim.
[ ] Project Owner approval missing for Ready or Done.
[ ] AI review agent declared approval, Ready, or Done.
```

Use `docs/governance/source-of-truth.md` for DOC-REGRESSION severity and resolution flow.

---

## 9. Project Owner Authority

The Project Owner is the final authority for Ready, Done, final Jira transitions, scope changes, acceptance-criteria deferral/rejection, ADR approval, risk acceptance, and stakeholder-facing final approval when needed.

AI review agents may support this decision with findings, but they cannot replace it. Their authority and output limits are defined in `docs/governance/ai-review-agents-policy.md`.

---

## 10. Acceptance Criteria

This document satisfies IHAP-23 when:

```text
[ ] DoR is defined with concrete minimum fields.
[ ] DoD is defined with concrete minimum evidence and review requirements.
[ ] Jira workflow states are mapped to entry and exit criteria.
[ ] Project Owner authority for Ready and Done is explicit.
[ ] Mandatory Shift Left Impact block is required for every Jira task by reference to docs/governance/shift-left-governance-baseline.md.
[ ] Source-of-truth boundaries for GitHub, Jira, and Confluence are preserved by reference to docs/governance/source-of-truth.md.
[ ] DOC-REGRESSION blocking rule is included by reference to docs/governance/source-of-truth.md.
[ ] AI review agents are advisory by reference to docs/governance/ai-review-agents-policy.md.
[ ] Evidence expectations are defined for documentation-only, governance, implementation, and stakeholder-facing tasks.
[ ] Stakeholder Review is clearly separated from Done.
[ ] No firmware, backend, mobile, cloud, runtime, CI enforcement, production-ready, safety-critical, commercial-ready, or security-grade claim is introduced.
```
