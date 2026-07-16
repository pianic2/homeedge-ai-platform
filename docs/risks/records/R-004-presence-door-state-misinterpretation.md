# R-004 — Presence and Door State Misinterpretation

**Status:** Draft  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Jira:** IHAP-16  
**Owner decision:** Pending Project Owner  
**Decision state:** Pending Project Owner  
**Risk type:** Privacy / Compliance / Claims  
**Source of truth:** This GitHub risk record until superseded by a later reviewed change.

<!--
AI_AGENT_METADATA:
  risk_id: R-004
  canonical_path: docs/risks/records/R-004-presence-door-state-misinterpretation.md
  risk_model: docs/risks/risk-model-baseline.md
  product_boundary: docs/product/product-vision.md
  stakeholder_report_rules: docs/governance/stakeholder-report-data-rules.md
  claim_boundaries_preserved: true
  risk_acceptance_authority: project_owner
  runtime_changes_allowed: false
  related_adrs:
    - docs/adr/ADR-0002-mvp-door-state-sensor.md
  adr_created: true
  adr_status: Proposed
  unvalidated_claim_marker: "[UNVALIDATED]"
-->

---

## 1. Risk Statement

There is a risk that local presence state or door open/closed telemetry is misinterpreted as person tracking, access control, intrusion detection, alarm-grade behavior, antifurto behavior, safety-critical monitoring, or protection evidence.

---

## 2. Source Trigger

The MVP includes local non-identifying presence state and door open/closed state. These are allowed only as telemetry/local state. They are not certified access control, intrusion detection, alarm-grade security, or safety-critical evidence.

---

## 3. Affected Assets and Trust Boundary

| Area | Detail |
|---|---|
| Asset | Presence state, door state, Product Vision wording, stakeholder reports, demos. |
| Trust boundary | Technical telemetry -> stakeholder interpretation. |
| Data involved | Boolean/state signals for presence and door open/closed. |
| Stakeholder surface | Summary allowed only with telemetry-safe wording. |

---

## 4. Scoring

| Field | Value | Rationale |
|---|---|---|
| Likelihood | High | Door and presence wording is easy to overread as security/safety functionality. |
| Impact | High | Misleading claim could violate project claim boundaries and create stakeholder confusion. |
| Residual risk | High | Risk remains until every stakeholder-facing surface consistently uses telemetry-safe wording. |
| Treatment proposal | Reject | Block alarm, antifurto, access-control, intrusion-detection, safety, and protection claims. |
| Decision state | Pending Project Owner | No residual risk acceptance exists. |

---

## 5. Existing Controls

- Product Vision defines presence as local, non-identifying room-level state.
- Product Vision defines door state as telemetry only.
- Stakeholder rules block production, safety, alarm, antifurto, certified access-control, certified intrusion-detection, and protection claims.

---

## 6. Evidence Gap

Missing evidence:

- final stakeholder wording review for every Confluence report;
- demo text review before publication;
- implementation evidence proving only allowed telemetry fields are emitted;
- tests preventing identity/tracking fields if schema is later introduced.

---

## 7. Mitigation Proposal

Mitigation is wording and scope control:

- always call door state “telemetry” or “state”; never “access control”;
- always call presence “local non-identifying room state”; never “person tracking”;
- block antifurto/alarm/protection phrasing;
- keep safety/security capability claims `[UNVALIDATED]` unless future reviewed evidence and Project Owner decision exist.

---

## 8. Stakeholder Visibility

| Item | Rule |
|---|---|
| Risk summary | Show allowed. |
| Door state | Show only as telemetry. |
| Presence state | Show only as local non-identifying room state. |
| Alarm / antifurto / protection claim | Blocked. |

Stakeholder-safe wording:

```text
The MVP can describe local presence and door state as telemetry only. It must not be described as tracking, alarm, antifurto, certified access control, intrusion detection, or protection.
```

---

## 9. Related Decisions

| ADR | Status | Effect on this risk | Remaining exposure |
|---|---|---|---|
| [ADR-0002 — MVP Door State Sensor](../../adr/ADR-0002-mvp-door-state-sensor.md) | Proposed | Preserves the telemetry-only boundary and explicitly rejects wire-supervision, tamper, access-control, alarm, antifurto, intrusion-detection and protection interpretations. | The risk remains active. Physical sensing evidence cannot prevent later wording, reporting or product-positioning misinterpretation. |

ADR-0002 does not accept, close or resolve R-004. Any residual-risk decision remains with the Project Owner and the Risk Record workflow.
