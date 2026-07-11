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
  related_risk_model: docs/risks/risk-model-baseline.md
  unvalidated_claim_marker: "[UNVALIDATED]"

HIDDEN_ANTI_REGRESSION_RULES:
  - Keep one stable architectural decision per ADR.
  - Do not create an ADR automatically for every risk or treatment.
  - When an ADR affects documented risks, declare linked risks, treatments, and effects.
  - The Risk Record remains the canonical treatment dossier and must contain the inverse link.
  - An ADR never closes or accepts a risk by itself.
  - Do not mark an ADR Accepted, Rejected, or Superseded without Project Owner approval.
  - Preserve [UNVALIDATED] on unproven claims.
-->

---

## 1. Context

Describe the problem, constraint, or architectural pressure that requires a stable decision.

Keep this factual. Mark unproven claims with `[UNVALIDATED]`.

---

## 2. Decision

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

## 5. Related Risks and Treatments

Complete this section when the ADR affects documented risks. Use `None` when it does not.

| Risk | Treatment | Effect | Remaining exposure |
|---|---|---|---|
| R-XXX / None | RT-RXXX-XX / None | Mitigates / Partially mitigates / Transfers / Avoids / Introduces / Leaves unresolved / Supersedes | ... |

Rules:

- link every referenced Risk Record;
- declare the effect separately for each risk;
- update the linked Risk Record with the inverse ADR link;
- do not state that the risk is resolved without verification evidence and Risk Record effectiveness review;
- do not use this section as a substitute for the full treatment rationale, evidence, or residual-risk decision.

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
| Related Risk Records | <path or none> |
| Related treatments | RT-RXXX-XX / none |
| Related ADRs | <path or none> |

---

## 8. Review Notes

```text
[ ] One stable architectural decision only.
[ ] ADR necessity is explicit; no ADR was created automatically from a risk.
[ ] Related risks and treatments are listed when relevant.
[ ] Effect and remaining exposure are explicit for every linked risk.
[ ] Linked Risk Records contain inverse links.
[ ] The ADR is not treated as risk acceptance or closure evidence.
[ ] Source-of-truth boundaries are preserved.
[ ] MVP boundary is not silently expanded.
[ ] [UNVALIDATED] is preserved on unproven claims.
[ ] No production-ready, commercial-ready, security-grade, certified, safety-critical, alarm-grade, antifurto, access-control, intrusion-detection, or protection claim is introduced.
[ ] Project Owner decision is recorded before status becomes Accepted, Rejected, or Superseded.
```
