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
  canonical_source_of_truth_policy: "docs/governance/source-of-truth.md"
  canonical_shift_left_baseline: "docs/governance/shift-left-governance-baseline.md"
  canonical_ai_review_agents_policy: "docs/governance/ai-review-agents-policy.md"
  canonical_ai_review_agent_playbook: "docs/governance/ai-review-agent-playbook.md"
  canonical_governance_lane_review_gate: "docs/governance/governance-lane-review-gate.md"
  canonical_stakeholder_transparency: "docs/governance/stakeholder-transparency.md"
  canonical_product_vision: "docs/product/product-vision.md"

HIDDEN_ANTI_REGRESSION_RULES:
  - This document defines lightweight Scrum operating rules; it does not replace source-of-truth, Shift Left, AI review-agent, stakeholder transparency, or governance-lane gate policies.
  - GitHub remains the technical source of truth for technical documents, decisions, risks, policies, baselines, governance rules, source code, and PR evidence.
  - Jira remains authoritative for backlog, task state, workflow state, review state, blockers, and evidence links.
  - Confluence remains authoritative for stakeholder hub, stakeholder reports, stakeholder forms, and stakeholder navigation.
  - Project Owner decides Ready, Done, and final workflow movements.
  - AI review agents are advisory only and must follow docs/governance/ai-review-agents-policy.md.
  - Any unproven claim must keep [UNVALIDATED].
  - The protected MVP boundary must not be silently expanded.
  - Target service boundaries must not be described as implemented runtime without traceable evidence.
-->

---

## 1. Purpose

This document defines the lightweight Scrum governance baseline for HomeEdge AI Platform.

It defines:

- Definition of Ready;
- Definition of Done;
- Jira workflow movement rules;
- minimum evidence expectations;
- Project Owner decision authority;
- alignment with the existing governance documents.

Core rule:

```text
Project Owner decides Ready and Done.
Jira tracks state and evidence.
GitHub defines technical truth.
Confluence reports and orients stakeholders.
AI review agents report findings only.
```

This document is governance-only. It does not introduce firmware, backend, mobile, cloud, runtime automation, CI enforcement, production readiness, safety-critical guarantees, commercial readiness, or security-grade certification.

---

## 2. Scope

Included:

- lightweight Scrum governance for Sprint 0 and Sprint 1;
- Definition of Ready;
- Definition of Done;
- Jira state movement rules;
- issue-level evidence expectations;
- documentation-only task evidence;
- implementation task evidence;
- governance-lane task evidence;
- stakeholder visibility expectations;
- Project Owner authority;
- `[UNVALIDATED]` claim preservation;
- DOC-REGRESSION awareness.

Excluded:

- enterprise-heavy Scrum governance;
- automated approval of Ready or Done;
- CI/runtime enforcement of gates;
- firmware, backend, mobile, or cloud implementation;
- production-readiness, safety-critical, commercial-readiness, certification, or security-grade claims;
- duplicating technical source-of-truth documents into Jira or Confluence.

---

## 3. Relationship With Other Governance Documents

This document coordinates existing governance rules. It does not replace them.

GitHub/Jira/Confluence authority is defined by `docs/governance/source-of-truth.md`; this document only applies those boundaries to Scrum readiness, workflow movement, evidence, and completion.

| Area | Canonical document | Scrum governance usage |
|---|---|---|
| Source-of-truth hierarchy, DOC-REGRESSION, canonical paths, `[UNVALIDATED]` policy | `docs/governance/source-of-truth.md` | Used to decide where evidence and technical truth must live. |
| Shift Left Impact block | `docs/governance/shift-left-governance-baseline.md` | Required before an issue can be considered Ready or reviewable. |
| AI review-agent authority and severity model | `docs/governance/ai-review-agents-policy.md` | Used to keep review agents advisory and non-decision-making. |
| Concrete AI review prompts | `docs/governance/ai-review-agent-playbook.md` | Used when a controlled review pass is needed. |
| Governance-lane movement checks | `docs/governance/governance-lane-review-gate.md` | Used before governance-lane movement toward Review, Stakeholder Review, or Done. |
| Stakeholder visibility and Confluence role | `docs/governance/stakeholder-transparency.md` | Used when a task affects stakeholder-facing visibility. |
| MVP boundary and glossary | `docs/product/product-vision.md` | Used to prevent silent MVP expansion or maturity overclaiming. |

If this document conflicts with `docs/governance/source-of-truth.md`, the source-of-truth policy wins until a reviewed GitHub change resolves the conflict.

---

## 4. Scrum Operating Model

HomeEdge uses a lightweight issue-driven Scrum model.

The goal is to keep work:

- small;
- reviewable;
- evidence-backed;
- linked to Jira;
- versioned in GitHub when technical truth changes;
- understandable for ITS stakeholders through Confluence navigation and reports.

This project does not use Scrum ceremony overhead as a substitute for evidence.

A task is complete only when its acceptance criteria, evidence, review state, and Project Owner decision support completion.

---

## 5. Jira Workflow States

The expected Jira workflow states are:

```text
Backlog
Pronto
In Progress
In Review
Stakeholder Review
Done
```

The exact Jira status names may remain localized, but the governance meaning must stay stable.

---

## 6. State Rules

### 6.1 Backlog

The task exists but is not ready for execution.

A task may stay in Backlog when:

```text
[ ] Goal is missing or unclear.
[ ] Scope is missing or too broad.
[ ] Non-scope is missing where scope risk exists.
[ ] Acceptance criteria are missing or not verifiable.
[ ] Evidence expectation is missing.
[ ] Dependencies or blockers are unclear.
[ ] Shift Left Impact block is missing, incomplete, reordered, or unjustified.
[ ] Source-of-truth surface is unclear.
[ ] The task risks silent MVP expansion.
[ ] The task contains unproven claims without [UNVALIDATED].
```

### 6.2 Pronto

The task is ready for execution, but not yet being worked.

A task may be moved to Pronto only when the Definition of Ready is satisfied and the Project Owner accepts readiness.

Minimum entry criteria:

```text
[ ] Goal is clear.
[ ] Scope is explicit.
[ ] Non-scope is explicit where needed.
[ ] Acceptance criteria are verifiable.
[ ] Evidence expectation is stated.
[ ] Owner, assignee, or explicit owner note exists.
[ ] Dependencies and blockers are noted when relevant.
[ ] Mandatory Shift Left Impact block is present and ordered.
[ ] Required source-of-truth surfaces are named.
[ ] No silent MVP expansion is introduced.
[ ] No unproven claim appears without [UNVALIDATED].
[ ] Project Owner remains the final authority for readiness.
```

AI review agents may report readiness findings, but they must not declare the issue Ready.

### 6.3 In Progress

The task is actively being worked.

A task may move to In Progress when:

```text
[ ] The task is in Pronto or Project Owner explicitly authorizes starting it.
[ ] The working branch, document path, or implementation surface is clear when applicable.
[ ] Scope has not expanded beyond the Jira issue.
[ ] The expected evidence path remains clear.
```

During In Progress:

```text
[ ] Keep changes inside the task scope.
[ ] Do not silently expand MVP boundaries.
[ ] Preserve [UNVALIDATED] on unproven claims.
[ ] Keep technical truth in GitHub.
[ ] Use Jira for blockers, comments, state, and evidence links.
[ ] Use Confluence only when stakeholder-facing summary/report/navigation is explicitly required.
```

### 6.4 In Review

The work has a reviewable evidence package.

A task may move toward In Review when:

```text
[ ] A branch, PR, diff, document, or evidence package exists.
[ ] Changed technical truth is in GitHub.
[ ] Jira can link to the reviewable evidence.
[ ] Acceptance criteria can be checked against evidence.
[ ] Shift Left Impact remains present, ordered, and justified.
[ ] No known S0/S1 DOC-REGRESSION remains unresolved.
[ ] No unsupported production-ready, safety-critical, commercial-ready, certification, or security-grade claim is introduced.
```

For governance-lane tasks, `docs/governance/governance-lane-review-gate.md` must also be used before movement toward review.

Review means the work is inspectable. It does not mean approval.

### 6.5 Stakeholder Review

The work is stable enough to be visible to stakeholders, but it is not necessarily Done.

A task may move toward Stakeholder Review when:

```text
[ ] Reviewable evidence is stable and linked from Jira.
[ ] No unresolved BLOCKER finding remains.
[ ] No unresolved MAJOR finding affects source-of-truth, MVP scope, evidence, claim maturity, stakeholder correctness, or approval authority.
[ ] Stakeholder-facing impact is clear.
[ ] Confluence, if used, summarizes and links instead of duplicating technical truth.
[ ] [UNVALIDATED] markers are preserved where claims remain unproven.
[ ] Project Owner action is explicitly requested or recorded.
```

Stakeholder Review means ready for stakeholder visibility, not final approval and not Done.

### 6.6 Done

The task is completed with evidence and Project Owner approval.

A task may move toward Done only when the Definition of Done is satisfied.

Minimum entry criteria:

```text
[ ] Project Owner explicitly approves the completion decision.
[ ] Jira contains final evidence links.
[ ] Acceptance criteria are satisfied or explicitly deferred/rejected by Project Owner decision.
[ ] Relevant GitHub source-of-truth documents are updated when technical truth changed.
[ ] No unresolved blocker remains.
[ ] No unresolved BLOCKER finding remains.
[ ] No unresolved MAJOR finding affects source-of-truth, MVP scope, evidence, claim maturity, stakeholder correctness, or approval authority.
[ ] No unresolved S0/S1 DOC-REGRESSION remains.
[ ] No source-of-truth divergence remains unresolved.
[ ] No unproven claim lacks [UNVALIDATED].
[ ] No production-ready, safety-critical, commercial-ready, certification, or security-grade claim is introduced without traceable evidence.
```

AI review agents must not declare Done.

---

## 7. Definition of Ready

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
[ ] Source-of-truth surfaces are identified.
[ ] Mandatory Shift Left Impact block is present.
[ ] Shift Left dimensions are in the required order.
[ ] Every N/A in the Shift Left block has an explicit rationale.
[ ] Required review perspectives are identifiable when relevant.
[ ] No silent MVP expansion is introduced.
[ ] No unproven claim appears without [UNVALIDATED].
[ ] Project Owner accepts the task as ready.
```

The mandatory Shift Left Impact block must use the standard dimension order:

```text
Security
Privacy
Cost
Compliance
Testing
Documentation
Stakeholder Visibility
```

---

## 8. Definition of Done

A task is Done only when the project can prove what changed, where the source of truth lives, and who approved completion.

Minimum Definition of Done:

```text
[ ] Acceptance criteria are satisfied or explicitly deferred/rejected.
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

## 9. Minimum Evidence Rules

Evidence must be proportional to the task.

### 9.1 Documentation-only task

```text
[ ] GitHub file path.
[ ] Branch or PR link.
[ ] Reviewable diff.
[ ] Jira evidence comment.
[ ] Explicit statement that no runtime behavior changed.
```

### 9.2 Governance task

```text
[ ] Canonical GitHub governance document created or updated.
[ ] README semantic index updated when a canonical document is added or moved.
[ ] source-of-truth.md updated when canonical paths or source-of-truth rules change.
[ ] Jira evidence link.
[ ] Governance Lane Review Gate used when moving toward Review, Stakeholder Review, or Done.
```

### 9.3 Implementation task

Implementation claims require implementation evidence.

Possible evidence:

```text
[ ] PR link.
[ ] Commit link.
[ ] Test output.
[ ] Build output.
[ ] Runtime logs.
[ ] Screenshots where appropriate.
[ ] Manual verification notes.
[ ] Updated documentation.
[ ] Explicit [UNVALIDATED] marker where runtime proof is missing.
```

Target architecture claims without implementation evidence must remain `[UNVALIDATED]`.

### 9.4 Stakeholder-facing task

```text
[ ] Confluence page or report link when stakeholder content changed.
[ ] Jira evidence link.
[ ] GitHub source-of-truth link for technical claims.
[ ] Confirmation that Confluence summarizes and links instead of redefining technical truth.
[ ] [UNVALIDATED] markers preserved where needed.
```

---

## 10. Jira Evidence Comment Template

Use this template when a task produces reviewable evidence:

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

## 11. Acceptance Criteria Handling

Acceptance criteria must be treated explicitly.

Allowed final states for each acceptance criterion:

```text
Satisfied
Deferred by Project Owner
Rejected by Project Owner
Not applicable with rationale
```

Not allowed:

```text
Implicitly ignored
Assumed complete
Covered by vague review
Moved to Done without evidence
```

If an acceptance criterion is deferred or rejected, Jira must record the decision and the reason.

---

## 12. Blockers

A task must not move toward Done while a blocker is unresolved.

Blocking examples:

```text
[ ] Missing evidence for completed claim.
[ ] Source-of-truth divergence.
[ ] Silent MVP expansion.
[ ] Unproven claim without [UNVALIDATED].
[ ] Unresolved S0/S1 DOC-REGRESSION.
[ ] Review-blocking S2 DOC-REGRESSION.
[ ] Unsupported production-ready, safety-critical, commercial-ready, certification, or security-grade claim.
[ ] Project Owner approval missing for Ready or Done.
[ ] AI review agent declared approval or Done.
```

---

## 13. DOC-REGRESSION Handling

A DOC-REGRESSION is blocking when it contradicts protected project truth, weakens claim control, creates parallel source-of-truth surfaces, or enables premature Done.

Before moving a task toward Review, Stakeholder Review, or Done, check:

```text
[ ] No source-of-truth hierarchy was weakened.
[ ] No long-form technical document was moved into Confluence.
[ ] No Jira description replaced canonical GitHub documentation.
[ ] No [UNVALIDATED] marker was removed without evidence.
[ ] No target service boundary was described as implemented runtime.
[ ] No protected MVP boundary was silently expanded.
[ ] No AI agent was treated as final approver.
```

If a DOC-REGRESSION exists, use the severity and handling rules in `docs/governance/source-of-truth.md`.

---

## 14. AI Review Agent Limits

AI review-agent authority, severity levels, allowed output, and forbidden approval language are defined in `docs/governance/ai-review-agents-policy.md`.

For operational prompts and reusable review flows, use `docs/governance/ai-review-agent-playbook.md`.

In this Scrum baseline the only local rule is:

```text
AI review agents report findings.
Project Owner decides Ready, Done, and final Jira transitions.
```

---

## 15. Project Owner Authority

The Project Owner is the final authority for:

```text
[ ] Ready decisions.
[ ] Done decisions.
[ ] Final Jira transitions.
[ ] Acceptance criteria deferral or rejection.
[ ] Scope changes.
[ ] MVP boundary changes.
[ ] ADR approval.
[ ] Risk acceptance.
[ ] Stakeholder-facing final approval when needed.
```

Advisory review output can support a Project Owner decision, but it cannot replace it.

---

## 16. Forbidden Claims

Do not introduce these claims unless a later reviewed implementation and validation task proves them with traceable evidence:

```text
Production-ready
Security-grade
Safety-critical
Commercially ready
Certified access control
Alarm-grade intrusion detection
Production-grade security certification
Direct ESP32 Kafka producer in MVP
Person tracking in MVP
Raw audio collection in MVP
```

If a claim is directional, planned, target-only, or not yet proven, mark it `[UNVALIDATED]`.

---

## 17. Practical Checklists

### 17.1 Before marking a task Ready

```text
[ ] Goal clear.
[ ] Scope explicit.
[ ] Non-scope explicit where needed.
[ ] Acceptance criteria verifiable.
[ ] Evidence expectation clear.
[ ] Owner/assignee or owner note present.
[ ] Dependencies/blockers noted.
[ ] Shift Left Impact block present and ordered.
[ ] Source-of-truth surfaces named.
[ ] [UNVALIDATED] preserved on unproven claims.
[ ] No silent MVP expansion.
[ ] Project Owner readiness decision recorded or explicitly requested.
```

### 17.2 Before requesting review

```text
[ ] Branch, PR, diff, document, or evidence package exists.
[ ] Changed technical truth is in GitHub.
[ ] Jira can link to evidence.
[ ] README updated if a canonical document was added or moved.
[ ] source-of-truth.md updated if canonical paths or source-of-truth rules changed.
[ ] No unresolved BLOCKER finding exists.
[ ] No S0/S1 DOC-REGRESSION remains.
[ ] [UNVALIDATED] markers are preserved.
```

### 17.3 Before moving to Stakeholder Review

```text
[ ] Reviewable evidence is stable.
[ ] Jira links evidence.
[ ] No unresolved BLOCKER remains.
[ ] No unresolved MAJOR affects source-of-truth, MVP scope, evidence, claim maturity, stakeholder correctness, or approval authority.
[ ] Stakeholder content is short, readable, and link-based if applicable.
[ ] Confluence does not duplicate technical truth.
[ ] Project Owner action is recorded or requested.
```

### 17.4 Before moving to Done

```text
[ ] Project Owner explicitly approves completion.
[ ] Jira contains final evidence links.
[ ] Acceptance criteria are satisfied or explicitly deferred/rejected.
[ ] Relevant source-of-truth documents are updated.
[ ] No unresolved blocker remains.
[ ] No unresolved BLOCKER remains.
[ ] No blocking MAJOR remains.
[ ] No unresolved S0/S1 DOC-REGRESSION remains.
[ ] No source-of-truth divergence remains.
[ ] No unproven claim lacks [UNVALIDATED].
[ ] No forbidden maturity claim is introduced without traceable evidence.
```

---

## 18. Acceptance Criteria

This document satisfies IHAP-23 when:

```text
[ ] DoR is defined with concrete minimum fields.
[ ] DoD is defined with concrete minimum evidence and review requirements.
[ ] Jira workflow states are mapped to entry and exit criteria.
[ ] Project Owner authority for Ready and Done is explicit.
[ ] Mandatory Shift Left Impact block is required for every Jira task.
[ ] Source-of-truth boundaries for GitHub, Jira, and Confluence are preserved by reference to docs/governance/source-of-truth.md.
[ ] DOC-REGRESSION blocking rule is included for governance reviews.
[ ] AI review agents are explicitly advisory and non-decision-making by reference to docs/governance/ai-review-agents-policy.md.
[ ] Evidence expectations are defined for documentation-only, governance, implementation, and stakeholder-facing tasks.
[ ] Stakeholder Review is clearly separated from Done.
[ ] No firmware, backend, mobile, cloud, runtime, CI enforcement, production-ready, safety-critical, commercial-ready, or security-grade claim is introduced.
```

---

## 19. Related Documents

This baseline must stay aligned with:

```text
README.md
docs/governance/source-of-truth.md
docs/governance/shift-left-governance-baseline.md
docs/governance/ai-review-agents-policy.md
docs/governance/ai-review-agent-playbook.md
docs/governance/governance-lane-review-gate.md
docs/governance/stakeholder-transparency.md
docs/product/product-vision.md
```

If this document conflicts with `docs/governance/source-of-truth.md`, the source-of-truth policy wins until a reviewed GitHub change resolves the conflict.

---

## 20. Practical Rule

```text
Ready means the task can start without guessing.
Review means the work is inspectable.
Stakeholder Review means the work is visible to stakeholders.
Done means evidence exists and the Project Owner approved completion.
```