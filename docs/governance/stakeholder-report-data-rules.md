# Stakeholder Report Data Rules

**Issue:** IHAP-30 — S0-021 — Stakeholder Report Data Rules  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Document type:** Governance / Stakeholder report data policy  
**Status:** Sprint 0 draft for review  
**Reading target:** less than 3 minutes for humans.  
**Source of truth:** This GitHub document defines what stakeholder reports may show, link, redact, or block until superseded by a later reviewed change.

<!--
AI_AGENT_METADATA:
  issue: IHAP-30
  related_issues:
    - IHAP-18
  document_type: stakeholder_report_data_rules
  canonical_path: docs/governance/stakeholder-report-data-rules.md
  source_of_truth: github_versioned_repository_documentation
  source_of_truth_policy: docs/governance/source-of-truth.md
  stakeholder_transparency: docs/governance/stakeholder-transparency.md
  product_vision: docs/product/product-vision.md
  task_scope: documentation_governance_only
  runtime_changes_allowed: false
  firmware_changes_allowed: false
  backend_changes_allowed: false
  mobile_changes_allowed: false
  cloud_changes_allowed: false
  stakeholder_report_creation_allowed: false
  production_ready_claims_allowed: false
  safety_critical_claims_allowed: false
  commercial_ready_claims_allowed: false
  certification_claims_allowed: false
  security_grade_claims_allowed: false
  alarm_grade_claims_allowed: false
  antifurto_claims_allowed: false
  certified_access_control_claims_allowed: false
  certified_intrusion_detection_claims_allowed: false
  protection_claims_allowed: false
  ai_runtime_validation_claims_allowed_without_evidence: false
  risk_acceptance_allowed: false
  autonomous_decision_authority: false
  unvalidated_claim_marker: "[UNVALIDATED]"

HIDDEN_ANTI_REGRESSION_RULES:
  - GitHub remains the source of truth for technical documents, decisions, risks, policies, governance rules, and PR evidence.
  - Jira remains authoritative for backlog, task state, workflow state, blockers, review state, and evidence links.
  - Confluence remains authoritative for stakeholder hub, stakeholder reports, forms, and navigation.
  - Stakeholder reports summarize and link; they must not duplicate long-form GitHub technical documents.
  - Preserve [UNVALIDATED] on unproven claims across stakeholder-facing surfaces.
  - Do not expose secrets, private domestic data, raw audio, identity data, individual tracking, behavioral history, or sensitive logs.
  - Do not expand MVP scope or present target service boundaries as runtime proof.
  - Do not let stakeholder reports upgrade target, future, or planned scope into implemented runtime.
  - Door state and presence state must remain telemetry/local state, not antifurto, access control, intrusion detection, safety-critical monitoring, or protection guarantees.
  - AI insight must remain target/future [UNVALIDATED] unless implementation and runtime evidence exist.
  - Review agents are advisory; Project Owner decisions remain required.
-->

---

## 1. Rule

```text
Report status.
Link evidence.
Redact sensitive data.
Keep unproven claims marked [UNVALIDATED].
Do not turn stakeholder reports into technical source of truth.
```

This document adds data rules for stakeholder reports. For surface ownership, use `docs/governance/source-of-truth.md`; for stakeholder flow, use `docs/governance/stakeholder-transparency.md`.

---

## 2. Data Categories

| Category | May appear in stakeholder reports? | Rule |
|---|---:|---|
| Task key, title, phase, workflow state | Yes | Use Jira as the state source. |
| Short progress summary | Yes | Keep it human-readable and link evidence. |
| Blocker or risk summary | Yes | Summarize impact; link Jira or GitHub evidence. |
| PR, branch, commit, document links | Yes | Prefer links over copied technical content. |
| Technical document body | Link only | GitHub remains the canonical document surface. |
| ADR or risk record body | Link only | Do not duplicate long-form decision or risk content in Confluence. |
| PR diff, logs, screenshots, test output | Link or redact | Share only if useful and safe; redact sensitive details first. |
| Device IDs, network details, local addresses | Redact or omit | Include only if required for review and non-sensitive. |
| Tokens, passwords, API keys, private addresses | Blocked | Never publish in stakeholder reports. |
| Raw audio, private images/videos | Blocked | Outside stakeholder report data scope. |
| Person identification, individual tracking, behavioral history | Blocked | Must not be introduced through reporting. |
| Backend, mobile, cloud, schema, storage, ingestion, registry, read-model, or AI runtime claims | Only with evidence or `[UNVALIDATED]` | Reports must not present target boundaries as implemented runtime. |
| Production-ready, commercial-ready, security-certified, security-grade, safety-critical, alarm-grade, antifurto, certified access control, certified intrusion detection, or protection claims | Blocked | Do not claim that the system protects people, goods, or environments. Future reconsideration requires reviewed evidence and Project Owner decision. |

---

## 3. Claim Handling

Use the weakest accurate maturity label. A stakeholder report must not upgrade project maturity beyond GitHub source-of-truth evidence.

| Situation | Required wording |
|---|---|
| Evidence exists and is linked | State the completed fact and link evidence. |
| Work is planned but not implemented | `PLANNED` or `[UNVALIDATED]`. |
| Work is in review | `IN REVIEW`; do not imply acceptance. |
| Ready for stakeholder visibility | `STAKEHOLDER REVIEW`; do not imply Done. |
| Target architecture or future capability | `TARGET`, `FUTURE`, or `[UNVALIDATED]`. |
| Backend, mobile, cloud, event schema, storage, ingestion, device registry, read model, or AI insight without runtime proof | Keep `[UNVALIDATED]`. |
| Door state or presence state | Describe as local telemetry/state only. Do not describe as protection, antifurto, access control, intrusion detection, or safety evidence. |
| AI insight without implementation and runtime evidence | Describe as target/future `[UNVALIDATED]`; do not imply runtime validation. |
| Commercial, production, security-grade, safety-critical, certification, alarm-grade, or antifurto wording | Block in current stakeholder reports. |
| Missing proof | Keep `[UNVALIDATED]`. |

Forbidden shortcut:

```text
Looks done, probably secure, production-ready, certified, reliable, antifurto, or AI-validated.
```

Correct shortcut:

```text
Evidence linked, or [UNVALIDATED].
```

---

## 4. MVP-Sensitive Reporting

Stakeholder reports must not reinterpret product scope.

Use these canonical references instead of repeating their full content:

| Need | Use |
|---|---|
| MVP boundary and glossary | `docs/product/product-vision.md` |
| Source-of-truth and DOC-REGRESSION | `docs/governance/source-of-truth.md` |
| Stakeholder visibility behavior | `docs/governance/stakeholder-transparency.md` |
| Workflow and evidence expectations | `docs/governance/scrum-governance-dor-dod.md` |

When a report mentions presence, door state, backend services, AI insight, Kafka, security, safety, production maturity, commercial maturity, or certification, it must either link evidence or preserve `[UNVALIDATED]`.

Reports must not imply that HomeEdge is an antifurto, alarm system, certified access-control system, certified intrusion-detection system, safety-critical system, or system that protects people, goods, or environments.

---

## 5. Report Checklist

Before publishing or updating a stakeholder report, check:

```text
[ ] The report is short and link-based.
[ ] Jira is used for task state and workflow state.
[ ] GitHub is linked for technical truth and evidence.
[ ] No long-form GitHub document is copied into Confluence.
[ ] Sensitive data is omitted or redacted.
[ ] [UNVALIDATED] is preserved where evidence is missing.
[ ] MVP scope is not expanded or reworded loosely.
[ ] No forbidden maturity claim is introduced.
[ ] No antifurto, alarm-grade, certified access-control, certified intrusion-detection, or protection claim is introduced.
[ ] Backend, mobile, cloud, schema, storage, ingestion, registry, read model, and AI claims are not presented as implemented without evidence.
[ ] AI insight is not presented as runtime validated without evidence.
[ ] Review-agent output is presented as advisory only.
[ ] Project Owner authority is not replaced by the report.
```

---

## 6. Practical Rule

```text
A stakeholder report is a map, not the territory.
```

If a report needs technical depth, link the GitHub source. If it needs state, link Jira. If it contains uncertainty, show it clearly.
