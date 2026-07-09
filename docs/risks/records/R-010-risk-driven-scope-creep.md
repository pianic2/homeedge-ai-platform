# R-010 — Risk-Driven Scope Creep

**Status:** Draft  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Jira:** IHAP-16  
**Owner decision:** Pending Project Owner  
**Decision state:** Pending Project Owner  
**Risk type:** Documentation / Compliance  
**Source of truth:** This GitHub risk record until superseded by a later reviewed change.

<!--
AI_AGENT_METADATA:
  risk_id: R-010
  canonical_path: docs/risks/records/R-010-risk-driven-scope-creep.md
  risk_model: docs/risks/risk-model-baseline.md
  product_boundary: docs/product/product-vision.md
  documentation_strategy: docs/governance/documentation-strategy.md
  risk_acceptance_authority: project_owner
  runtime_changes_allowed: false
  adr_created: false
  unvalidated_claim_marker: "[UNVALIDATED]"
-->

---

## 1. Risk Statement

There is a risk that risk treatment is used to introduce features outside the MVP because documenting mitigation can look like approving new implementation scope.

---

## 2. Source Trigger

The project uses risk governance early. That is correct, but risk documents can accidentally become a backlog expansion mechanism if mitigation proposals are written as implementation commitments.

---

## 3. Affected Assets and Trust Boundary

| Area | Detail |
|---|---|
| Asset | Risk records, Product Vision, Jira backlog, stakeholder summaries, future implementation tasks. |
| Trust boundary | Risk analysis -> scope decision -> implementation work. |
| Data involved | Scope labels, mitigation wording, decision state, evidence links. |
| Stakeholder surface | Stakeholders may read proposed mitigation as approved roadmap. |

---

## 4. Scoring

| Field | Value | Rationale |
|---|---|---|
| Likelihood | Medium | Mitigation language naturally points to future work unless carefully bounded. |
| Impact | High | Silent scope expansion can undermine MVP discipline and source-of-truth consistency. |
| Residual risk | High | Risk persists for every future risk record and governance task. |
| Treatment proposal | Reject silent expansion | Mitigation may propose future work, but scope changes require Project Owner decision and reviewed source-of-truth update. |
| Decision state | Pending Project Owner | No residual risk decision has been made. |

---

## 5. Existing Controls

- Product Vision protects MVP / FUTURE / OUT OF MVP boundaries.
- Documentation Strategy requires new documents only when they reduce confusion and do not duplicate truth.
- Source-of-truth policy blocks silent MVP expansion.
- Risk Model Baseline requires `Pending Project Owner` unless decision evidence exists.

---

## 6. Evidence Gap

Missing or future evidence:

- explicit Jira task for each future mitigation;
- Project Owner decision for any scope expansion;
- reviewed source-of-truth change when MVP/FUTURE/OUT OF MVP changes;
- stakeholder wording that separates proposal from approved work.

---

## 7. Mitigation Proposal

Risk records should use precise treatment language:

- “Mitigate later” means possible future work, not current scope.
- “Defer” means not active now.
- “Reject” means keep out of MVP/current scope.
- “Candidate accept” means candidate for Project Owner review, not accepted.

Any new implementation must be introduced through its own Jira task and reviewed evidence.

---

## 8. Stakeholder Visibility

| Item | Rule |
|---|---|
| Risk treatment proposal | Show allowed if marked as proposal. |
| Scope expansion | Link to explicit Project Owner decision. |
| Future mitigation | Show as FUTURE / `[UNVALIDATED]`. |
| Implied implementation commitment | Blocked. |

Stakeholder-safe wording:

```text
Risk treatment proposals do not expand MVP scope. New implementation requires a separate task, reviewed evidence, and Project Owner decision.
```
