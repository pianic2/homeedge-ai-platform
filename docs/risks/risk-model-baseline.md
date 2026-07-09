# Risk Model Baseline

**Issue:** IHAP-16 — S0-007 — Risk Model Baseline  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Document type:** Risk governance / baseline  
**Status:** Sprint 0 draft for review  
**Reading target:** less than 4 minutes for humans; hidden metadata supports AI routing and anti-regression checks.  
**Source of truth:** This versioned GitHub document defines the initial project risk model until superseded by a later reviewed change.

<!--
AI_AGENT_METADATA:
  issue: IHAP-16
  document_type: risk_model_baseline
  canonical_path: docs/risks/risk-model-baseline.md
  source_of_truth: github_versioned_repository_documentation
  source_of_truth_policy: docs/governance/source-of-truth.md
  documentation_strategy: docs/governance/documentation-strategy.md
  shift_left_governance_baseline: docs/governance/shift-left-governance-baseline.md
  stakeholder_transparency: docs/governance/stakeholder-transparency.md
  stakeholder_report_data_rules: docs/governance/stakeholder-report-data-rules.md
  product_vision: docs/product/product-vision.md
  risk_index: docs/risks/README.md
  risk_assessment_template: docs/templates/risk-assessment.md
  task_scope: documentation_governance_only
  runtime_changes_allowed: false
  firmware_changes_allowed: false
  backend_changes_allowed: false
  mobile_changes_allowed: false
  cloud_changes_allowed: false
  schema_changes_allowed: false
  production_ready_claims_allowed: false
  commercial_ready_claims_allowed: false
  safety_critical_claims_allowed: false
  security_grade_claims_allowed: false
  certification_claims_allowed: false
  alarm_grade_claims_allowed: false
  antifurto_claims_allowed: false
  certified_access_control_claims_allowed: false
  certified_intrusion_detection_claims_allowed: false
  protection_claims_allowed: false
  autonomous_decision_authority: false
  risk_acceptance_authority: project_owner
  ai_review_agents_decision_authority: false
  unvalidated_claim_marker: "[UNVALIDATED]"

HIDDEN_ANTI_REGRESSION_RULES:
  - This baseline defines a model; it does not accept, defer, reject, or mitigate a specific residual risk by itself.
  - Project Owner decision is required before any risk is treated as accepted, deferred, or rejected.
  - AI review agents may detect findings, classify severity, and recommend corrections only.
  - This file must not duplicate the Shift Left task impact block; link docs/governance/shift-left-governance-baseline.md instead.
  - This file must not duplicate the risk assessment template; link docs/templates/risk-assessment.md instead.
  - The MVP boundary remains docs/product/product-vision.md.
  - Target service boundaries remain target only and [UNVALIDATED] until implementation and runtime evidence exist.
  - Presence and door state are telemetry/local state only; they are not antifurto, alarm-grade, access-control, intrusion-detection, safety-critical, or protection evidence.
  - Do not introduce firmware, backend, mobile, cloud, schema, runtime, production, commercial, safety-critical, certification, or security-grade claims.
-->

---

## 1. Rule

```text
Expose risk early.
Score it consistently.
Treat it explicitly.
Link evidence.
Project Owner decides acceptance.
```

This baseline makes project risks visible without creating an enterprise approval process.

It does not approve risk, expand MVP scope, or validate runtime behavior.

---

## 2. Scope

Included:

- project risk categories;
- likelihood, impact, residual risk, treatment, and decision state;
- owner/responsibility boundaries;
- required evidence;
- stakeholder visibility rules;
- relationship with MVP, FUTURE, OUT OF MVP, TARGET, and `[UNVALIDATED]`;
- baseline risks for device, network path, event payload, target services, AI target, documentation, cost, and stakeholder visibility.

Excluded:

- firmware changes;
- backend changes;
- mobile changes;
- cloud changes;
- schema changes;
- runtime implementation;
- risk acceptance by this document;
- production-ready, commercial-ready, safety-critical, security-grade, certification, alarm-grade, antifurto, access-control, intrusion-detection, or protection claims.

---

## 3. Risk Categories

| Category | Covers |
|---|---|
| Technical | Device behavior, firmware maturity, event payloads, target service boundaries, and data flow maturity. |
| Security | Spoofing, tampering, unauthorized event submission, replay, exposed secrets, and unsafe trust boundaries. |
| Privacy | Presence state, door state, metadata inference, retention, correlation, and domestic context leakage. |
| Compliance / Claims | Misleading maturity, security, safety, commercial, certification, alarm, antifurto, access-control, intrusion-detection, or protection wording. |
| Cost | Hardware, cloud, logs, tooling, maintenance load, event volume, and future AI/provider cost. |
| Documentation | Source-of-truth drift, stale files, duplicated truth, missing links, and weak evidence traceability. |
| Stakeholder Visibility | Overexposure, unclear status, weak redaction, missing `[UNVALIDATED]`, and misunderstanding of project maturity. |
| AI / Inference | Future insight ambiguity, profiling risk, false interpretation, and unvalidated AI capability claims. |

---

## 4. Risk Scoring

Use the same impact dimensions as the Shift Left baseline, but do not duplicate the task-level Shift Left block here.

For task-level impact checks, use `docs/governance/shift-left-governance-baseline.md`.

| Field | Values | Rule |
|---|---|---|
| Likelihood | Low / Medium / High | Probability that the risk materializes under current scope and evidence. |
| Impact | Low / Medium / High | Expected project, technical, privacy, security, compliance, cost, or stakeholder effect. |
| Residual risk | Low / Medium / High / Pending evidence | Risk remaining after current mitigation or current deferral. |
| Treatment | Mitigate / Defer / Reject / Candidate accept | Proposed handling. It is not approved until the Project Owner decides. |
| Decision state | Pending Project Owner / Accepted / Deferred / Rejected | Final state requires explicit Project Owner decision evidence. |

`Candidate accept` means “candidate for Project Owner review”. It does not accept the risk.

---

## 5. Assets and Trust Boundaries

| Asset / boundary | Current maturity | Risk relevance |
|---|---|---|
| ESP32 room/door node | MVP device direction; runtime evidence required per implementation task | Physical access, spoofing, firmware reliability, and telemetry integrity. |
| Firmware event generation | `[UNVALIDATED]` until implemented and tested | Malformed payloads, missing validation, incorrect states, or misleading evidence. |
| HTTP/JSON event path | MVP target until implemented and verified | Leakage, replay, spoofing, transport weakness, and missing ingestion validation. |
| Ingestion service boundary | TARGET `[UNVALIDATED]` | Event validation, abuse control, cost exposure, and target/runtime confusion. |
| Device registry boundary | TARGET `[UNVALIDATED]` | Device identity, known-device state, lifecycle ambiguity, and spoofing control. |
| Read model boundary | TARGET `[UNVALIDATED]` | Stale state, misleading dashboard data, and unclear evidence freshness. |
| AI insight boundary | TARGET / FUTURE `[UNVALIDATED]` | Inference, profiling, false interpretation, and unsupported AI maturity claims. |
| GitHub | Technical source of truth | Risk model, docs, code, policies, technical baselines, and PR evidence. |
| Jira | Tracking and evidence links | Workflow state, blockers, review state, and risk work evidence. |
| Confluence | Stakeholder hub and reports | Short stakeholder summary, navigation, and redacted visibility only. |

Target service boundaries do not prove implemented runtime services.

---

## 6. Baseline Risks

| ID | Risk | Category | Residual risk | Treatment |
|---|---|---|---:|---|
| R-001 | A fake or unknown device is treated as trusted. | Security / Technical | Pending evidence | Mitigate later through reviewed device identity and registry design `[UNVALIDATED]`. |
| R-002 | Event payloads leak sensitive details through transport, logs, or reports. | Security / Privacy | Medium | Mitigate with minimization, redaction, and evidence review. |
| R-003 | Metadata such as timestamp, device id, room id, firmware version, or network details enables domestic inference. | Privacy / Stakeholder Visibility | Medium | Redact, omit, aggregate, or link only when needed. |
| R-004 | Presence or door state is misunderstood as person tracking, access control, intrusion detection, or protection. | Privacy / Compliance / Claims | High | Reject that wording. Keep telemetry-only language. |
| R-005 | Backend, mobile, cloud, event schema, storage, ingestion, registry, read model, or AI target is presented as implemented without evidence. | Compliance / Documentation | High | Preserve TARGET and `[UNVALIDATED]` until evidence exists. |
| R-006 | GitHub, Jira, and Confluence drift into parallel truths. | Documentation / Stakeholder Visibility | Medium | Keep GitHub canonical, Jira evidence-linked, and Confluence summary/link-only. |
| R-007 | Future AI insight becomes behavioral profiling or unsupported inference. | AI / Privacy | High | Defer; require future reviewed task and evidence before runtime or stakeholder claim. |
| R-008 | Event volume, logs, cloud services, tooling, or AI providers create uncontrolled cost. | Cost / Technical | Pending evidence | Defer to cost governance and future implementation estimates. |
| R-009 | Stakeholders read Sprint 0 documentation as production, commercial, security-grade, safety-critical, alarm-grade, or antifurto posture. | Stakeholder Visibility / Claims | High | Block forbidden claim wording and use weakest accurate maturity label. |
| R-010 | Risk documentation is used to introduce features outside MVP. | Documentation / Compliance | High | Reject silent scope expansion; require reviewed Project Owner decision for scope changes. |

This table is a baseline. It is not a complete risk register and does not accept residual risk.

---

## 7. Evidence Required

| Claim type | Evidence required |
|---|---|
| Runtime implemented | PR, code, tests, logs, screenshots, or other runtime evidence. |
| Firmware behavior | Firmware diff, build/test/manual evidence, and clear scope link. |
| Event/schema stability | Versioned schema or fixture plus tests/review evidence. |
| Security or privacy mitigation | Documented control plus implementation or review evidence. |
| Cost posture | Estimate, measurement, budget rule, or explicit `[UNVALIDATED]` marker. |
| Stakeholder claim | GitHub source, Jira/PR evidence, safe Confluence summary, and preserved `[UNVALIDATED]` where needed. |
| Missing proof | Keep `[UNVALIDATED]`. |

Evidence can reduce uncertainty. It does not remove Project Owner authority.

---

## 8. Responsibility Model

| Role / surface | Responsibility | Cannot do |
|---|---|---|
| Project Owner | Accept, defer, or reject residual risk; approve scope changes; decide final risk posture. | Skip evidence or override source-of-truth rules silently. |
| Task owner | Document risk, propose mitigation, link evidence, and preserve `[UNVALIDATED]`. | Accept residual risk independently. |
| AI review agents | Detect findings, classify severity, recommend correction, and report evidence gaps. | Approve risks, close issues, declare Done, or authorize Jira transitions. |
| Stakeholders | Review clarity, visibility, and navigability. | Replace technical risk decision authority. |
| GitHub | Store technical risk truth and versioned documents. | Become workflow state authority. |
| Jira | Track state, blockers, review state, and evidence links. | Become long-form technical risk documentation. |
| Confluence | Summarize risk posture and link evidence for stakeholders. | Duplicate long-form GitHub risk documents or redefine technical truth. |

---

## 9. MVP / FUTURE / OUT OF MVP / `[UNVALIDATED]`

Risk handling must preserve the current product boundary:

| Scope marker | Risk rule |
|---|---|
| MVP | Risks may be documented and mitigated only within the approved MVP boundary. |
| TARGET | Target service boundaries remain `[UNVALIDATED]` until implemented and evidenced. |
| FUTURE | Future capability requires future task scope, evidence, and Project Owner decision before being treated as active work. |
| OUT OF MVP | Risk treatment cannot smuggle the item into MVP. Reject or defer. |
| `[UNVALIDATED]` | Required when implementation, runtime, security, privacy, cost, reliability, AI, or stakeholder evidence is missing. |

Presence state is local and non-identifying. Door state is telemetry only. Neither is protection, access control, intrusion detection, antifurto, alarm-grade, or safety-critical evidence.

---

## 10. Stakeholder Visibility

Stakeholder-facing material may show:

- short risk summary;
- impact in plain language;
- current treatment proposal;
- decision state;
- Jira and GitHub evidence links;
- `[UNVALIDATED]` where proof is missing.

Stakeholder-facing material must redact or omit:

- tokens, passwords, API keys;
- private domestic addresses;
- private network details;
- sensitive logs;
- precise local topology when not needed;
- raw audio, private images/videos, identity data, individual tracking, behavioral history, or routine profiling.

Stakeholder-facing material must block:

- production-ready claims;
- commercial-ready claims;
- security-certified or security-grade claims;
- safety-critical claims;
- alarm-grade claims;
- antifurto claims;
- certified access-control claims;
- certified intrusion-detection claims;
- claims that the system protects people, goods, or environments.

Use `docs/governance/stakeholder-report-data-rules.md` for detailed stakeholder report rules.

---

## 11. Review Checklist

Before moving IHAP-16 or future risk-model changes toward review, check:

```text
[ ] The change is documentation/governance only.
[ ] No runtime, firmware, backend, mobile, cloud, or schema behavior changed.
[ ] Risk acceptance remains Project Owner-only.
[ ] AI review agents report findings only.
[ ] MVP, FUTURE, OUT OF MVP, TARGET, and [UNVALIDATED] boundaries are preserved.
[ ] Target service boundaries are not presented as implemented runtime.
[ ] No forbidden maturity, safety, security, alarm, antifurto, certification, access-control, intrusion-detection, or protection claim was introduced.
[ ] Confluence, if updated, summarizes and links only.
[ ] Jira links evidence and does not duplicate long-form risk documentation.
```

---

## 12. Practical Rule

```text
Assess risk to expose uncertainty.
Treat risk to reduce uncertainty.
Do not use risk treatment to approve scope silently.
```
