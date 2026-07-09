# ADR-XXXX — Decision Title

**Status:** Proposed  
**Date:** YYYY-MM-DD  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Jira:** IHAP-XX  
**PR:** <link when available>  
**Supersedes:** None / ADR-XXXX  
**Superseded by:** None / ADR-XXXX

<!--
AI_AGENT_METADATA:
  document_type: architecture_decision_record
  status_allowed_values:
    - Proposed
    - Accepted
    - Superseded
    - Rejected
  approval_authority: project_owner
  source_of_truth: github_versioned_repository_documentation
  jira_role: evidence_links_only
  confluence_role: stakeholder_navigation_only
  unvalidated_claim_marker: "[UNVALIDATED]"
  forbidden_claims:
    - production_ready
    - safety_critical
    - commercial_ready
    - security_grade

HIDDEN_ANTI_REGRESSION_RULES:
  - Keep one decision per ADR.
  - Do not mark an ADR Accepted, Rejected, or Superseded without Project Owner approval.
  - Do not expand MVP scope silently.
  - Preserve [UNVALIDATED] on unproven claims.
  - Do not treat target architecture as implemented runtime without evidence.
  - Do not introduce production-ready, safety-critical, commercial-ready, certification, or security-grade claims.
-->

---

## 1. Context

Describe the problem, constraint, or architectural pressure that requires a decision.

Keep this factual. Mark unproven claims with `[UNVALIDATED]`.

---

## 2. Decision

State the decision clearly.

```text
We will ...
```

This section becomes authoritative only when the ADR status is `Accepted` by the Project Owner.

---

## 3. Alternatives Considered

| Alternative | Outcome | Reason |
|---|---|---|
| Option A | Accepted / Rejected / Deferred | ... |
| Option B | Accepted / Rejected / Deferred | ... |

---

## 4. Consequences

### Positive

- ...

### Negative / Trade-offs

- ...

### Neutral / Operational

- ...

---

## 5. Risks

| Risk | Impact | Mitigation / Follow-up |
|---|---|---|
| ... | Low / Medium / High | ... |

---

## 6. Follow-up Work

| Item | Tracking |
|---|---|
| ... | Jira issue / future task / none |

---

## 7. Evidence Links

| Evidence | Link |
|---|---|
| Jira issue | IHAP-XX |
| Pull request | <link> |
| Related docs | <path> |
| Related ADRs | <path> |

---

## 8. Review Notes

```text
[ ] Source-of-truth boundaries preserved.
[ ] MVP boundary not silently expanded.
[ ] [UNVALIDATED] preserved on unproven claims.
[ ] No production-ready, safety-critical, commercial-ready, or security-grade claim introduced.
[ ] Project Owner decision recorded before status becomes Accepted, Rejected, or Superseded.
```
