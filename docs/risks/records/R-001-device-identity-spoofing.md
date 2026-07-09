# R-001 — Device Identity Spoofing

**Status:** Draft  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Jira:** IHAP-16  
**Owner decision:** Pending Project Owner  
**Decision state:** Pending Project Owner  
**Risk type:** Security / Technical  
**Source of truth:** This GitHub risk record until superseded by a later reviewed change.

<!--
AI_AGENT_METADATA:
  risk_id: R-001
  canonical_path: docs/risks/records/R-001-device-identity-spoofing.md
  risk_model: docs/risks/risk-model-baseline.md
  product_boundary: docs/product/product-vision.md
  risk_acceptance_authority: project_owner
  runtime_changes_allowed: false
  adr_created: false
  unvalidated_claim_marker: "[UNVALIDATED]"
-->

---

## 1. Risk Statement

There is a risk that a fake, cloned, or unknown device is treated as trusted because device identity and registry behavior are target boundaries `[UNVALIDATED]` until implemented and tested.

---

## 2. Source Trigger

The MVP has an ESP32-class room/door node and target service boundaries for ingestion and device registry. The device registry is not yet runtime-proven.

This risk is not theoretical noise: every edge-to-backend system eventually needs to decide whether an incoming device should be trusted.

---

## 3. Affected Assets and Trust Boundary

| Area | Detail |
|---|---|
| Asset | ESP32 room/door node, device id, event payload, ingestion target, device registry target. |
| Trust boundary | Device -> network -> ingestion -> registry/read model. |
| Data involved | Device id, room id, firmware version, timestamp, telemetry fields. |
| Stakeholder surface | Risk summary may be shown; implementation detail should be linked, not copied. |

---

## 4. Scoring

| Field | Value | Rationale |
|---|---|---|
| Likelihood | Medium | No runtime identity control exists yet; current service boundaries are target only. |
| Impact | High | Fake device data can corrupt telemetry, read models, stakeholder evidence, and future automation assumptions. |
| Residual risk | Pending evidence | No implemented registry/auth evidence exists yet. |
| Treatment proposal | Mitigate | Future implementation should define known-device registration, request validation, and rejected-device handling. |
| Decision state | Pending Project Owner | No acceptance, deferral, or rejection has been approved. |

---

## 5. Existing Controls

- MVP boundary limits scope to one generic room/door node.
- Target services remain `[UNVALIDATED]` instead of being claimed as implemented.
- Stakeholder reports must not overstate security maturity.

---

## 6. Evidence Gap

Missing evidence:

- device registration model;
- accepted/rejected device behavior;
- ingestion validation logic;
- tests or logs proving unknown-device rejection;
- documented error handling.

Until evidence exists, device identity security remains `[UNVALIDATED]`.

---

## 7. Mitigation Proposal

Future implementation should define:

- stable device identifier format;
- known-device registry boundary;
- request validation at ingestion;
- behavior for unknown, disabled, or malformed device identity;
- audit/log evidence without exposing private domestic details.

No ADR is introduced by this record.

---

## 8. Stakeholder Visibility

| Item | Rule |
|---|---|
| Risk summary | Show allowed. |
| Device identity design | Link only when implemented. |
| Secrets, tokens, private topology | Blocked. |
| Security maturity claim | Keep `[UNVALIDATED]`; no security-grade wording. |

Stakeholder-safe wording:

```text
Device identity is a known risk area and remains [UNVALIDATED] until the registry and ingestion behavior are implemented and tested.
```
