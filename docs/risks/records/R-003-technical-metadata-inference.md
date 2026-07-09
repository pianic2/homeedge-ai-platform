# R-003 — Technical Metadata Inference

**Status:** Draft  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Jira:** IHAP-16  
**Owner decision:** Pending Project Owner  
**Decision state:** Pending Project Owner  
**Risk type:** Privacy / Stakeholder Visibility  
**Source of truth:** This GitHub risk record until superseded by a later reviewed change.

<!--
AI_AGENT_METADATA:
  risk_id: R-003
  canonical_path: docs/risks/records/R-003-technical-metadata-inference.md
  risk_model: docs/risks/risk-model-baseline.md
  product_boundary: docs/product/product-vision.md
  stakeholder_report_rules: docs/governance/stakeholder-report-data-rules.md
  risk_acceptance_authority: project_owner
  runtime_changes_allowed: false
  adr_created: false
  unvalidated_claim_marker: "[UNVALIDATED]"
-->

---

## 1. Risk Statement

There is a risk that technical metadata enables domestic inference because timestamps, device ids, room ids, firmware versions, and network details can reveal patterns when retained, correlated, logged, or exposed.

---

## 2. Source Trigger

The Product Vision allows minimal event direction fields such as timestamp, device id, room id, and firmware version, while IP/network metadata is out of stakeholder view. These fields are useful for engineering evidence but can become privacy-sensitive in combination.

---

## 3. Affected Assets and Trust Boundary

| Area | Detail |
|---|---|
| Asset | Timestamp, device id, room id, firmware version, IP/network metadata. |
| Trust boundary | Runtime telemetry -> logs/storage -> stakeholder reports. |
| Data involved | Technical metadata and domestic context labels. |
| Stakeholder surface | Generic labels only; private topology redacted or omitted. |

---

## 4. Scoring

| Field | Value | Rationale |
|---|---|---|
| Likelihood | Medium | Metadata is likely to be present in events, logs, screenshots, or debugging evidence. |
| Impact | Medium | Metadata may expose domestic layout, activity timing, or device topology. |
| Residual risk | Medium | Current docs define redaction intent, but runtime retention/redaction is not implemented. |
| Treatment proposal | Mitigate | Redact private topology, aggregate where possible, and keep stakeholder views generic. |
| Decision state | Pending Project Owner | No residual risk decision has been made. |

---

## 5. Existing Controls

- Product data boundary marks IP/network metadata as out of stakeholder view.
- Stakeholder report rules require redaction or omission of device/network details when sensitive.
- Raw identity and behavioral data are OUT OF MVP.

---

## 6. Evidence Gap

Missing evidence:

- actual event schema and metadata fields;
- runtime retention behavior;
- log redaction behavior;
- stakeholder report examples after redaction;
- rule for generic room labels versus private domestic labels.

---

## 7. Mitigation Proposal

Future implementation and documentation should:

- use generic room labels in examples;
- avoid private addresses and precise domestic topology;
- omit IP/network metadata from stakeholder material;
- avoid publishing raw logs without redaction review;
- keep metadata retention `[UNVALIDATED]` until implemented and reviewed.

---

## 8. Stakeholder Visibility

| Item | Rule |
|---|---|
| Generic metadata risk summary | Show allowed. |
| Room labels | Generic only. |
| IP/network/private topology | Redact or omit. |
| Retention or correlation claim | `[UNVALIDATED]` until evidence exists. |

Stakeholder-safe wording:

```text
Technical metadata is useful for evidence but may expose domestic context. Private topology and network details are redacted or omitted from stakeholder material.
```
