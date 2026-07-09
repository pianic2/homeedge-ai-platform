# R-005 — Target Boundary Overclaim

**Status:** Draft  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Jira:** IHAP-16  
**Owner decision:** Pending Project Owner  
**Decision state:** Pending Project Owner  
**Risk type:** Compliance / Documentation  
**Source of truth:** This GitHub risk record until superseded by a later reviewed change.

<!--
AI_AGENT_METADATA:
  risk_id: R-005
  canonical_path: docs/risks/records/R-005-target-boundary-overclaim.md
  risk_model: docs/risks/risk-model-baseline.md
  product_boundary: docs/product/product-vision.md
  source_of_truth_policy: docs/governance/source-of-truth.md
  risk_acceptance_authority: project_owner
  runtime_changes_allowed: false
  adr_created: false
  unvalidated_claim_marker: "[UNVALIDATED]"
-->

---

## 1. Risk Statement

There is a risk that backend, mobile, cloud, schema, storage, ingestion, registry, read model, or AI target boundaries are presented as implemented runtime without traceable evidence.

---

## 2. Source Trigger

The repository contains target service boundaries for ingestion, device registry, read model, and AI insight. These paths are architectural direction, not proof of implemented services.

---

## 3. Affected Assets and Trust Boundary

| Area | Detail |
|---|---|
| Asset | `services/ingestion/`, `services/device-registry/`, `services/read-model/`, `services/ai-insight/`, mobile/cloud/schema wording. |
| Trust boundary | Repository structure -> implementation maturity claim. |
| Data involved | Not data-specific; maturity and evidence risk. |
| Stakeholder surface | High risk of misunderstanding if wording is loose. |

---

## 4. Scoring

| Field | Value | Rationale |
|---|---|---|
| Likelihood | High | Directory names and architecture diagrams are often mistaken for implemented services. |
| Impact | High | Overclaiming can invalidate stakeholder trust and source-of-truth correctness. |
| Residual risk | High | Runtime evidence is not yet present for target services. |
| Treatment proposal | Mitigate | Preserve TARGET and `[UNVALIDATED]` wording until implementation and test evidence exist. |
| Decision state | Pending Project Owner | No residual risk decision has been made. |

---

## 5. Existing Controls

- README and Product Vision define service directories as target boundaries.
- `[UNVALIDATED]` policy requires unproven runtime claims to remain marked.
- Stakeholder report data rules block target-to-runtime upgrades.

---

## 6. Evidence Gap

Missing evidence:

- service code implementing each boundary;
- tests/build logs;
- runtime logs or API responses;
- schema or event contract evidence;
- deployment or cloud evidence if later claimed.

---

## 7. Mitigation Proposal

Every document and stakeholder surface should use the weakest accurate label:

- `TARGET` for service boundaries;
- `FUTURE` for later capability;
- `[UNVALIDATED]` for unproven runtime behavior;
- `DONE` only with linked evidence.

No placeholder directory should be treated as runtime proof.

---

## 8. Stakeholder Visibility

| Item | Rule |
|---|---|
| Target architecture summary | Show allowed with TARGET / `[UNVALIDATED]`. |
| Runtime service claim | Evidence required. |
| Production-ready wording | Blocked. |
| AI insight runtime claim | `[UNVALIDATED]` until evidence exists. |

Stakeholder-safe wording:

```text
Backend, mobile, cloud, schema, and AI service areas are target boundaries unless implementation and runtime evidence prove otherwise.
```
