# R-007 — AI Inference and Profiling

**Status:** Draft  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Jira:** IHAP-16  
**Owner decision:** Pending Project Owner  
**Decision state:** Pending Project Owner  
**Risk type:** AI / Privacy  
**Source of truth:** This GitHub risk record until superseded by a later reviewed change.

<!--
AI_AGENT_METADATA:
  risk_id: R-007
  canonical_path: docs/risks/records/R-007-ai-inference-profiling.md
  risk_model: docs/risks/risk-model-baseline.md
  product_boundary: docs/product/product-vision.md
  risk_acceptance_authority: project_owner
  runtime_changes_allowed: false
  adr_created: false
  unvalidated_claim_marker: "[UNVALIDATED]"
-->

---

## 1. Risk Statement

There is a risk that future AI insight turns room telemetry into behavioral profiling or unsupported interpretation because AI insight is currently a target/future boundary `[UNVALIDATED]`.

---

## 2. Source Trigger

The Product Vision includes an AI-ready insight direction, but AI runtime, evaluation, inference scope, and data minimization are not implemented or validated in Sprint 0.

---

## 3. Affected Assets and Trust Boundary

| Area | Detail |
|---|---|
| Asset | AI insight target, read model target, presence state, door state, timestamps, metadata. |
| Trust boundary | Telemetry/read model -> inferred meaning -> stakeholder or user interpretation. |
| Data involved | Room-level telemetry and technical metadata. |
| Stakeholder surface | AI claims are especially easy to overstate. |

---

## 4. Scoring

| Field | Value | Rationale |
|---|---|---|
| Likelihood | Medium | AI insight is explicitly a future direction, so the risk is likely to return later. |
| Impact | High | Profiling or false interpretation would violate privacy boundaries and stakeholder trust. |
| Residual risk | High | No AI runtime, dataset, evaluation, or guardrail evidence exists. |
| Treatment proposal | Defer | Keep AI insight target/future `[UNVALIDATED]` until a future reviewed task defines evidence and boundaries. |
| Decision state | Pending Project Owner | No residual risk decision has been made. |

---

## 5. Existing Controls

- Person identification, individual tracking, behavioral history, and routine profiling are OUT OF MVP.
- AI insight is marked as TARGET / FUTURE and `[UNVALIDATED]`.
- Stakeholder claim rules prevent runtime AI validation claims without evidence.

---

## 6. Evidence Gap

Missing evidence:

- AI task scope;
- input data minimization policy;
- evaluation method;
- false positive/negative handling;
- privacy review for inference;
- runtime evidence and stakeholder-safe wording.

---

## 7. Mitigation Proposal

Future AI work should require:

- explicit task scope before implementation;
- no identity, individual tracking, or routine profiling;
- documented input/output boundaries;
- evidence before claiming runtime validation;
- stakeholder wording that states target/future status clearly.

No ADR is introduced by this record.

---

## 8. Stakeholder Visibility

| Item | Rule |
|---|---|
| AI risk summary | Show allowed. |
| AI runtime claim | `[UNVALIDATED]` until evidence exists. |
| Behavioral profiling | Blocked for MVP. |
| Safety/security/automation claim | Blocked unless future evidence and Project Owner decision exist. |

Stakeholder-safe wording:

```text
AI insight is a future target [UNVALIDATED]. It must not be described as runtime validated or as behavioral profiling.
```
