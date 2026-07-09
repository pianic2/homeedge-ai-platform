# Governance Lane Review Gate

**Issue:** IHAP-35 — S0-026 — Governance Lane Review Gate  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Document type:** Governance / Review Gate  
**Status:** Sprint 0 draft for review  
**Source of truth:** This versioned GitHub document is the canonical Governance Lane Review Gate for Sprint 0 governance-lane task movement until superseded by a later reviewed change.

<!--
AI_AGENT_METADATA:
  issue: IHAP-35
  document_type: governance_lane_review_gate
  source_of_truth: github_versioned_repository_documentation
  task_scope: documentation_governance_only
  runtime_changes_allowed: false
  firmware_changes_allowed: false
  backend_changes_allowed: false
  mobile_changes_allowed: false
  cloud_changes_allowed: false
  autonomous_decision_authority: false
  issue_transition_allowed_without_project_owner_instruction: false
  issue_closure_allowed: false
  adr_approval_allowed: false
  production_ready_claims_allowed: false
  safety_critical_claims_allowed: false
  commercial_ready_claims_allowed: false
  security_grade_claims_allowed: false
  unvalidated_claim_marker: "[UNVALIDATED]"
  canonical_source_of_truth_policy: "docs/governance/source-of-truth.md"
  canonical_shift_left_baseline: "docs/governance/shift-left-governance-baseline.md"
  canonical_scrum_governance_dor_dod: "docs/governance/scrum-governance-dor-dod.md"
  canonical_ai_review_agents_policy: "docs/governance/ai-review-agents-policy.md"
  canonical_ai_review_agent_playbook: "docs/governance/ai-review-agent-playbook.md"
  canonical_stakeholder_transparency: "docs/governance/stakeholder-transparency.md"
  canonical_product_vision: "docs/product/product-vision.md"
  covered_issues:
    - IHAP-23
    - IHAP-24
    - IHAP-25
    - IHAP-34
    - IHAP-35

HIDDEN_ANTI_REGRESSION_RULES:
  - This gate coordinates existing governance policies; it does not replace them.
  - docs/governance/scrum-governance-dor-dod.md defines lightweight Scrum governance, Definition of Ready, Definition of Done, Jira workflow movement, and minimum evidence expectations.
  - GitHub remains the technical source of truth for technical documents, decisions, risks, policies, baselines, governance rules, source code, and PR evidence.
  - Jira remains authoritative for backlog, task state, workflow state, review state, blockers, and evidence links.
  - Confluence remains authoritative for stakeholder hub, stakeholder reports, stakeholder forms, and stakeholder navigation.
  - Confluence must not duplicate this gate as long-form technical documentation.
  - Review agents may detect, classify, recommend, and report findings, but they cannot approve ADRs, close issues, declare Done, or transition Jira issues without explicit Project Owner instruction.
  - Any unproven claim must keep [UNVALIDATED].
  - The protected MVP boundary must not be silently expanded.
  - Target service boundaries must not be described as implemented runtime without traceable evidence.
-->

---

## 1. Purpose

This document defines the Governance Lane Review Gate for Sprint 0 governance work.

The gate decides what must be checked before a governance-lane task or document can move toward:

- Ready;
- Review;
- Stakeholder Review;
- Done.

The gate is intentionally lightweight. It exists to prevent governance work from advancing while it contains missing evidence, source-of-truth divergence, unsupported claims, DOC-REGRESSION, or premature workflow authority.

Core rule:

```text
Review agents report findings.
Project Owner decides transitions.
GitHub defines technical truth.
Jira tracks evidence and state.
Confluence reports and orients.
```

This document is governance-only. It does not introduce firmware, backend, mobile, cloud, runtime automation, CI enforcement, production readiness, safety-critical guarantees, commercial readiness, or security-grade certification.

---

## 2. Scope

Included:

- governance-lane task movement checks;
- Ready, Review, Stakeholder Review, and Done gate criteria;
- required reviewer mapping;
- source-of-truth consistency checks;
- DOC-REGRESSION blocking rules;
- evidence expectations;
- `[UNVALIDATED]` claim preservation;
- Confluence non-duplication rules;
- Project Owner decision boundary.

Excluded:

- runtime implementation;
- firmware implementation;
- backend implementation;
- mobile implementation;
- cloud deployment;
- CI enforcement of gates;
- technical review gates for schemas, firmware behavior, backend contracts, or architecture implementation;
- replacing Project Owner approval;
- duplicating GitHub governance documentation into Jira or Confluence.

---

## 3. Covered Governance Lane Issues

This gate applies to the Sprint 0 governance-lane issues listed below:

| Issue | Title | Gate relevance |
|---|---|---|
| IHAP-23 | Scrum Governance, DoR and DoD | Defines lightweight Scrum governance, task readiness, completion rules, Jira workflow movement, and minimum evidence expectations through `docs/governance/scrum-governance-dor-dod.md`. |
| IHAP-24 | Team Working Rules | Defines collaboration and operating rules. |
| IHAP-25 | Engineering Assistant Rules | Defines assistant/tool usage boundaries. |
| IHAP-34 | Configure Review Agents | Defines advisory review agents and severity model. |
| IHAP-35 | Governance Lane Review Gate | Defines this gate. |

The gate may be reused by later governance tasks when explicitly referenced by Jira or a later reviewed source-of-truth change.

---

## 4. Source-of-Truth Boundary

| Surface | Authority | Gate rule |
|---|---|---|
| GitHub | Technical truth, code, versioned technical documents, decisions, risks, policies, governance baselines, PR evidence | Technical governance rules must live here. |
| Jira | Backlog, workflow state, task status, review state, blockers, evidence links | Jira tracks state and links evidence; it must not become a duplicate technical documentation repository. |
| Confluence | Stakeholder hub, stakeholder reports, stakeholder forms, stakeholder navigation | Confluence summarizes and links; it must not redefine technical truth. |

If GitHub and Jira or Confluence disagree on technical content, GitHub wins until a reviewed GitHub source-of-truth change updates the project truth.

---

## 5. Required Reviewers

Governance-lane movement toward Review, Stakeholder Review, or Done requires at least these advisory review perspectives:

| Reviewer | Required checks | Blocks when |
|---|---|---|
| Source of Truth Guardian | GitHub/Jira/Confluence roles, canonical paths, DOC-REGRESSION, `[UNVALIDATED]` preservation, technical truth location | Technical truth is moved out of GitHub, duplicated incorrectly, contradicted, or silently weakened. |
| Testing & Evidence Reviewer | Acceptance criteria, PR/diff evidence, Jira evidence links, review output, missing proof, premature Done risk | Evidence is missing for a completed claim, review movement, or Done movement. |
| Stakeholder Clarity Reviewer | Confluence summary behavior, stakeholder readability, link-based navigation, claim clarity, redaction | Stakeholder material contradicts GitHub, duplicates technical docs, hides serious uncertainty, or weakens `[UNVALIDATED]`. |

These reviewers are advisory. They can identify blocking findings, but they cannot approve, close, declare Done, or transition Jira issues.

---

## 6. Gate Levels

### 6.1 Ready Gate

A governance-lane task may be considered ready for work only when:

```text
[ ] Scope is explicit.
[ ] Acceptance criteria are verifiable.
[ ] Required source-of-truth surfaces are named.
[ ] The mandatory Shift Left Impact block is present and ordered.
[ ] Required review perspectives are identifiable.
[ ] No MVP boundary is silently expanded.
[ ] No unproven claim appears without [UNVALIDATED].
[ ] Project Owner remains the final authority for readiness decisions.
```

For the full Definition of Ready baseline, use `docs/governance/scrum-governance-dor-dod.md`.

A task is not ready when it has unclear scope, missing acceptance criteria, missing Shift Left impact, unsupported claims, or source-of-truth ambiguity.

### 6.2 Review Gate

A governance-lane task may move toward technical review only when:

```text
[ ] A branch, PR, diff, or reviewable evidence package exists.
[ ] Changed source-of-truth files are in GitHub.
[ ] README semantic links are updated when canonical documents are added or moved.
[ ] docs/governance/source-of-truth.md is updated when canonical paths or source-of-truth rules change.
[ ] Jira can link to the reviewable evidence.
[ ] Confluence is not used as a competing technical source of truth.
[ ] No unresolved BLOCKER finding exists.
```

Review may still surface MAJOR/MINOR/NOTE findings. Unresolved BLOCKER findings stop movement.

### 6.3 Stakeholder Review Gate

A governance-lane task may move toward Stakeholder Review only when:

```text
[ ] Reviewable evidence is stable and linked from Jira.
[ ] No unresolved BLOCKER finding remains.
[ ] No unresolved MAJOR finding affects source-of-truth, MVP scope, evidence, claim maturity, stakeholder correctness, or approval authority.
[ ] Stakeholder-facing content, if any, is short, readable, and link-based.
[ ] Confluence does not duplicate long-form GitHub technical documentation.
[ ] [UNVALIDATED] markers are preserved where claims remain unproven.
[ ] Project Owner action is explicitly requested or recorded.
```

Stakeholder Review means the work is ready for stakeholder visibility. It does not mean Done.

### 6.4 Done Gate

A governance-lane task may move toward Done only when:

```text
[ ] Project Owner explicitly approves the completion decision.
[ ] Jira contains final evidence links.
[ ] Acceptance criteria are satisfied or explicitly deferred by Project Owner decision.
[ ] No unresolved BLOCKER finding remains.
[ ] No unresolved MAJOR finding affects source-of-truth, MVP scope, evidence, claim maturity, stakeholder correctness, or approval authority.
[ ] No source-of-truth divergence remains unresolved.
[ ] No unproven claim lacks [UNVALIDATED].
[ ] No production-ready, safety-critical, commercial-ready, certification, or security-grade claim is introduced without traceable evidence.
```

For the full Definition of Done baseline, use `docs/governance/scrum-governance-dor-dod.md`.

Review agents must not declare Done. They may only state that no blocking findings were detected by their review pass.

---

## 7. Blocking Conditions

Movement toward Review, Stakeholder Review, or Done must be blocked when one or more of these conditions exists:

- unresolved `BLOCKER` finding;
- unresolved `MAJOR` finding affecting source-of-truth, MVP scope, evidence, claim maturity, stakeholder correctness, or approval authority;
- unresolved S0 or S1 DOC-REGRESSION;
- review-blocking S2 DOC-REGRESSION involving `[UNVALIDATED]`, MVP scope, target/runtime confusion, or source-of-truth ambiguity;
- missing Jira evidence link for a completed governance or implementation claim;
- unproven claim without `[UNVALIDATED]`;
- removal of `[UNVALIDATED]` without traceable evidence;
- GitHub technical truth moved into Jira or Confluence as a competing source;
- Confluence duplicates long-form technical documentation instead of linking and summarizing;
- silent MVP expansion;
- target service boundaries presented as implemented runtime without evidence;
- production-ready, safety-critical, commercial-ready, certification, or security-grade claim without evidence;
- Project Owner approval missing for Ready or Done decision.

---

## 8. Severity Model

| Severity | Blocking | Meaning | DOC-REGRESSION mapping |
|---|---|---|---|
| `BLOCKER` | Yes | Contradicts protected source-of-truth, silently expands MVP, removes `[UNVALIDATED]` without evidence, or creates premature Done risk. | S0 DOC-REGRESSION |
| `MAJOR` | Usually yes | Creates serious ambiguity, divergence, misleading maturity, missing evidence, or stakeholder confusion. | S1 or review-blocking S2 DOC-REGRESSION |
| `MINOR` | No by default | Correctable issue that does not invalidate the gate by itself. | Non-blocking S2 or S3 DOC-REGRESSION |
| `NOTE` | No | Suggestion or observation with no blocking impact. | Non-regression observation |

A MAJOR finding becomes blocking when it affects source-of-truth hierarchy, MVP scope, evidence, claim maturity, stakeholder correctness, or approval authority.

---

## 9. Gate Checklist

Use this checklist before requesting movement beyond the current state:

```text
[ ] The task scope is still the scope approved in Jira.
[ ] The mandatory Shift Left Impact block is present and justified.
[ ] All changed technical truth is in GitHub.
[ ] Jira is used only for state, blockers, comments, and evidence links.
[ ] Confluence is used only for stakeholder hub, reports, forms, summaries, and navigation.
[ ] Technical long-form documentation is not duplicated into Confluence.
[ ] README semantic links are updated when canonical documents are added or moved.
[ ] source-of-truth.md canonical paths are updated when canonical documents are added or moved.
[ ] No unresolved DOC-REGRESSION remains.
[ ] No unproven claim appears without [UNVALIDATED].
[ ] No [UNVALIDATED] marker was removed without traceable evidence.
[ ] MVP scope was not silently expanded.
[ ] Target architecture is not described as implemented runtime without evidence.
[ ] Forbidden maturity claims are absent unless backed by traceable evidence.
[ ] Required reviewer findings are linked or summarized as evidence.
[ ] Project Owner action is explicit for Ready or Done movement.
```

---

## 10. Gate Output Template

Use this output in Jira comments, PR reviews, or review summaries:

```text
GOVERNANCE LANE REVIEW GATE

Issue:
Requested movement: Ready / Review / Stakeholder Review / Done
Scope reviewed:
Sources checked:
Reviewers applied:

Gate findings:
- BLOCKER:
- MAJOR:
- MINOR:
- NOTE:

DOC-REGRESSION status: none / unresolved / fixed
[UNVALIDATED] claims preserved: yes / no / not applicable
Source-of-truth boundaries preserved: yes / no
Evidence links present: yes / no
Confluence used only as stakeholder/link layer: yes / no / not applicable
Project Owner decision required: yes / no

Gate result:
No blocking findings detected by this review pass / Blocked pending fixes
```

Allowed final phrasing:

```text
No blocking findings detected by this review pass.
```

Forbidden final phrasing:

```text
Approved.
Done.
Ready authorized.
ADR accepted.
Production-ready.
Security-grade.
```

---

## 11. Confluence Rule

Confluence may contain a short stakeholder explanation or report that links to this GitHub document.

Confluence must not contain a full duplicate of this gate as a competing technical source of truth.

Correct Confluence usage:

```text
Short stakeholder summary -> Jira issue -> GitHub PR/document evidence
```

Incorrect Confluence usage:

```text
Full copied gate policy treated as official technical documentation
```

If Confluence and GitHub diverge on this gate, GitHub wins until a reviewed GitHub source-of-truth change updates the project truth.

---

## 12. Acceptance Criteria

This document satisfies IHAP-35 when:

- the Governance Lane Review Gate exists as a canonical GitHub document;
- covered governance-lane issues are explicitly listed;
- Ready, Review, Stakeholder Review, and Done gate levels are defined;
- required reviewers are mapped to concrete checks and blocking conditions;
- `BLOCKER`, `MAJOR`, `MINOR`, and `NOTE` severities are defined and mapped to DOC-REGRESSION severity;
- gate output template is defined;
- Done is blocked when evidence is missing, documents diverge, claims are unsupported, or Project Owner approval is missing;
- GitHub/Jira/Confluence source-of-truth boundaries are preserved;
- `[UNVALIDATED]` markers are preserved unless traceable evidence exists;
- Confluence remains stakeholder explanation and link layer only;
- README semantic index links this document;
- `docs/governance/source-of-truth.md` registers this canonical path;
- `docs/governance/scrum-governance-dor-dod.md` remains the canonical baseline for Scrum governance, DoR, DoD, Jira workflow movement, and minimum evidence expectations;
- no firmware, backend, mobile, cloud, runtime, production-ready, safety-critical, commercial-ready, or security-grade claim is introduced.

---

## 13. Related Documents

This gate must stay aligned with:

- `README.md`;
- `docs/governance/source-of-truth.md`;
- `docs/governance/shift-left-governance-baseline.md`;
- `docs/governance/scrum-governance-dor-dod.md`;
- `docs/governance/ai-review-agents-policy.md`;
- `docs/governance/ai-review-agent-playbook.md`;
- `docs/governance/stakeholder-transparency.md`;
- `docs/product/product-vision.md`.

If this gate conflicts with `docs/governance/source-of-truth.md`, the source-of-truth policy wins until a reviewed GitHub change resolves the conflict.

---

## 14. Practical Rule

```text
Governance gates do not approve work.
They expose whether movement would be safe for Project Owner review.
```
