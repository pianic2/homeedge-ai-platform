# R-002 — Event Payload Leakage

**Status:** Draft  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Jira:** IHAP-16  
**Owner decision:** Pending Project Owner  
**Decision state:** Pending Project Owner  
**Risk type:** Security / Privacy  
**Source of truth:** This GitHub risk record until superseded by a later reviewed change.

<!--
AI_AGENT_METADATA:
  risk_id: R-002
  canonical_path: docs/risks/records/R-002-event-payload-leakage.md
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

There is a risk that event payloads expose sensitive domestic or operational details because transport, logging, retention, and stakeholder reporting behavior are not yet implemented and tested.

---

## 2. Source Trigger

The MVP direction includes HTTP/JSON event flow from the room/door node toward ingestion. The event shape contains room telemetry and technical metadata, but schema, transport, log handling, and storage are still `[UNVALIDATED]`.

---

## 3. Affected Assets and Trust Boundary

| Area | Detail |
|---|---|
| Asset | Event payload, HTTP/JSON path, ingestion target, logs, stakeholder reports. |
| Trust boundary | Device -> network -> ingestion -> logs/reports. |
| Data involved | Temperature, humidity, presence state, door state, timestamp, device id, room id, firmware version. |
| Stakeholder surface | Summary allowed; raw payloads/logs should be linked only when safe and redacted. |

---

## 4. Scoring

| Field | Value | Rationale |
|---|---|---|
| Likelihood | Medium | Payload and logging behavior are not yet proven; leakage commonly happens through debug output and reports. |
| Impact | High | Door/presence state and metadata can reveal domestic patterns if exposed or correlated. |
| Residual risk | Medium | Current documentation defines boundaries but no runtime redaction/enforcement exists. |
| Treatment proposal | Mitigate | Minimize payload, redact logs/reports, and keep sensitive data out of stakeholder surfaces. |
| Decision state | Pending Project Owner | No residual risk decision has been made. |

---

## 5. Existing Controls

- Raw audio, identity, individual tracking, and behavioral history are OUT OF MVP.
- Stakeholder report data rules block secrets, private addresses, raw audio, identity data, and behavioral history.
- `[UNVALIDATED]` prevents unproven transport/storage claims.

---

## 6. Evidence Gap

Missing evidence:

- implemented event schema;
- transport behavior and logs;
- ingestion validation output;
- redaction checks for logs/screenshots/reports;
- proof that raw sensitive payloads are not copied into Confluence.

---

## 7. Mitigation Proposal

Future implementation and docs should require:

- minimal payload fields;
- no raw audio or identity fields;
- redacted examples in docs and stakeholder reports;
- private network metadata omitted from reports;
- logs reviewed before being shared.

No runtime security claim is made by this mitigation proposal.

---

## 8. Stakeholder Visibility

| Item | Rule |
|---|---|
| Risk summary | Show allowed. |
| Raw payload examples | Link/redact only. |
| Sensitive logs | Redact or block. |
| Transport security claim | `[UNVALIDATED]` until evidence exists. |

Stakeholder-safe wording:

```text
Event payload leakage is tracked as a privacy/security risk. Payload, logging, and redaction behavior remain [UNVALIDATED] until implemented and reviewed.
```
