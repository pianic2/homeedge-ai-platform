# R-008 — Cost Abuse and Operational Overhead

**Status:** Draft  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Jira:** IHAP-16  
**Owner decision:** Pending Project Owner  
**Decision state:** Pending Project Owner  
**Risk type:** Cost / Technical  
**Source of truth:** This GitHub risk record until superseded by a later reviewed change.

<!--
AI_AGENT_METADATA:
  risk_id: R-008
  canonical_path: docs/risks/records/R-008-cost-abuse.md
  risk_model: docs/risks/risk-model-baseline.md
  risk_acceptance_authority: project_owner
  runtime_changes_allowed: false
  adr_created: false
  unvalidated_claim_marker: "[UNVALIDATED]"
-->

---

## 1. Risk Statement

There is a risk that event volume, logs, cloud services, tooling, maintenance load, or future AI providers create uncontrolled cost because runtime volume and deployment behavior are not yet measured.

---

## 2. Source Trigger

The project targets edge-to-backend telemetry, future cloud/deployment direction, and future AI insight. These areas can create cost even in small projects when logging, data retention, provider usage, or event frequency are not bounded.

---

## 3. Affected Assets and Trust Boundary

| Area | Detail |
|---|---|
| Asset | Event flow, logs, ingestion target, read model target, cloud target, future AI target. |
| Trust boundary | Local prototype -> hosted/runtime infrastructure. |
| Data involved | Event count, log volume, retained telemetry, AI/provider input. |
| Stakeholder surface | Cost risk can be summarized; raw billing/provider details should be linked or redacted as needed. |

---

## 4. Scoring

| Field | Value | Rationale |
|---|---|---|
| Likelihood | Medium | Cloud, logs, and AI are future targets; cost can grow silently if not bounded. |
| Impact | Medium | Cost overruns can block continuation or force scope reduction. |
| Residual risk | Pending evidence | No runtime cost measurement or event volume evidence exists yet. |
| Treatment proposal | Defer / Mitigate | Defer detailed estimates to cost governance and add limits during implementation. |
| Decision state | Pending Project Owner | No residual risk decision has been made. |

---

## 5. Existing Controls

- Current IHAP-16 changes are documentation-only.
- Runtime, cloud, and AI provider usage remain `[UNVALIDATED]`.
- IHAP-17 is expected to cover cost governance and BOM policy separately.

---

## 6. Evidence Gap

Missing evidence:

- event frequency estimates;
- log retention settings;
- cloud deployment plan;
- AI provider usage estimate;
- budget guardrail or kill-switch;
- cost dashboard or measurement.

---

## 7. Mitigation Proposal

Future work should:

- define event-rate assumptions;
- cap logs and retention;
- avoid paid providers until explicitly approved;
- keep AI cost `[UNVALIDATED]` until measured;
- link cost estimates from the cost governance document when available.

---

## 8. Stakeholder Visibility

| Item | Rule |
|---|---|
| Cost risk summary | Show allowed. |
| Budget estimate | Show only when sourced. |
| Provider billing details | Link/redact as needed. |
| Economic claim | `[UNVALIDATED]` until evidence exists. |

Stakeholder-safe wording:

```text
Cost exposure is tracked as a risk. Runtime cost, event volume, cloud usage, and AI provider cost remain [UNVALIDATED] until measured or estimated through reviewed evidence.
```
