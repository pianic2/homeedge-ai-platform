# Source of Truth and DOC-REGRESSION Policy

**Issue:** IHAP-13 — S0-004 — Source of Truth and DOC-REGRESSION Policy  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Document type:** Documentation / Source of Truth governance  
**Status:** Sprint 0 draft for review  
**Source of truth:** This versioned GitHub document is the canonical policy for source-of-truth rules, document divergence handling, DOC-REGRESSION handling, and `[UNVALIDATED]` claim governance until superseded by a later reviewed change.

<!--
AI_AGENT_METADATA:
  issue: IHAP-13
  document_type: source_of_truth_governance
  source_of_truth: github_versioned_repository_documentation
  task_scope: documentation_governance_only
  runtime_changes_allowed: false
  firmware_changes_allowed: false
  backend_changes_allowed: false
  mobile_changes_allowed: false
  production_ready_claims_allowed: false
  safety_critical_claims_allowed: false
  security_grade_claims_allowed: false
  unvalidated_claim_marker: "[UNVALIDATED]"
  canonical_policy_file: "docs/governance/source-of-truth.md"
  canonical_product_vision: "docs/product/product-vision.md"
  canonical_stakeholder_transparency: "docs/governance/stakeholder-transparency.md"
  standalone_glossary_status: "future_candidate_not_created_by_ihap_13"
  current_glossary_location: "docs/product/product-vision.md"
  stakeholder_report_authoritative_surface: "Confluence"
  confluence_stakeholder_hub: "https://niccolopiazzi01.atlassian.net/wiki/spaces/IEHAP/overview"
  repository_source_of_truth_for:
    - code
    - technical_documents
    - product_vision
    - adr
    - risk_assessment
    - policies
    - technical_baselines
    - governance_rules
    - pr_evidence
    - runtime_evidence_when_committed_or_linked
  jira_authoritative_for:
    - backlog
    - task_status
    - workflow_state
    - review_state
    - blockers
    - evidence_links
  confluence_authoritative_for:
    - stakeholder_hub
    - stakeholder_reports
    - stakeholder_forms
    - stakeholder_navigation
  mvp_firmware_node: "firmware/room-env-node/"
  mvp_node_semantics: "generic_room_door_node"
  mvp_includes:
    - temperature_collection
    - humidity_collection
    - local_non_identifying_presence_detection
    - door_open_closed_state
  mvp_excludes:
    - raw_audio_collection
    - individual_presence_tracking
    - behavioral_history_tracking
    - person_identification
    - window_sensor_scope
    - 220v_automation
    - esp32_direct_kafka_producer
    - commercial_claims
    - safety_critical_claims
    - production_security_grade_certification
  target_service_boundaries:
    - services/ingestion/
    - services/device-registry/
    - services/read-model/
    - services/ai-insight/

HIDDEN_ANTI_REGRESSION_RULES:
  - GitHub remains the source of truth for technical documents, decisions, risks, policies, technical baselines, governance rules, source code, and PR evidence.
  - Jira remains authoritative for backlog, task state, workflow state, review state, blockers, and evidence links.
  - Confluence remains authoritative for stakeholder hub, stakeholder reports, stakeholder forms, and stakeholder navigation.
  - Confluence stakeholder reports may summarize project state but must not override GitHub source-of-truth technical documents.
  - Confluence must not duplicate long-form technical source-of-truth documents from GitHub.
  - If GitHub and Jira diverge on technical content, GitHub wins until a reviewed GitHub change updates the source of truth.
  - If GitHub and Confluence diverge on technical content, GitHub wins and Confluence must be realigned as a stakeholder-facing summary or link layer.
  - The only firmware node in the MVP remains firmware/room-env-node/.
  - firmware/room-env-node/ remains a generic room/door node.
  - The MVP includes temperature, humidity, local non-identifying presence detection, and door open/closed state.
  - Raw audio, person tracking, behavioral history, identity inference, window scope, 220V automation, direct ESP32 Kafka publishing, commercial claims, safety-critical claims, and production/security-grade certification claims remain out of MVP.
  - The four services directories are target service boundaries unless validated by later implementation evidence.
  - Any unproven claim must be marked as [UNVALIDATED].
-->

---

## 1. Purpose

This document defines the operating rules for source of truth, document divergence, DOC-REGRESSION handling, and `[UNVALIDATED]` claims in HomeEdge AI Platform.

The goal is to prevent the project from developing parallel truths across GitHub, Jira, and Confluence.

Core rule:

```text
GitHub contains the technical truth.
Jira tracks work and review state.
Confluence presents stakeholder navigation and stakeholder reports.
```

This document is governance-only. It does not introduce firmware, backend, mobile, infrastructure, cloud, Kafka runtime, AI runtime, production readiness, safety-critical guarantees, or security-grade certification.

---

## 2. Scope

Included:

- source-of-truth ownership by domain;
- DOC-REGRESSION definition and severity;
- anti-divergence rules for GitHub, Jira, and Confluence;
- `[UNVALIDATED]` claim policy;
- initial canonical repository paths;
- merge/review blocking rules for documentation regressions;
- protected MVP boundaries inherited from the Product Vision.

Excluded:

- historical passive documentation;
- firmware implementation;
- backend implementation;
- mobile implementation;
- runtime validation;
- cloud deployment;
- production-readiness claims;
- safety-critical claims;
- security-grade claims;
- stakeholder report creation.

Stakeholder reports are intentionally kept on Confluence because Confluence supports stakeholder-facing pages and forms. They must remain summary/reporting artifacts and must not override GitHub technical source-of-truth documents.

---

## 3. Source of Truth Matrix

| Domain | Authoritative source | Secondary surface | Rule |
|---|---|---|---|
| Backlog | Jira | GitHub only as linked evidence | Jira owns backlog items, prioritization, workflow state, blockers, and review state. |
| Task status | Jira | Confluence summary only | Jira is authoritative for status such as Backlog, Ready, In Progress, In Review, Stakeholder Review, and Done. |
| Code | GitHub | Jira PR links | GitHub is authoritative for source code, repository structure, commits, branches, and PR evidence. |
| Technical documents | GitHub | Confluence link/summary only | Technical documents must live in the repository. Confluence must not become a duplicate technical documentation repository. |
| Product Vision | `docs/product/product-vision.md` | Jira/Confluence links | Product Vision, MVP boundaries, and current glossary live in GitHub until superseded by reviewed change. |
| Glossary | Current embedded glossary in `docs/product/product-vision.md` | Future `docs/glossary/project-glossary.md` candidate | Do not create a duplicate glossary until a later task explicitly extracts and links it. |
| ADR | GitHub `docs/adr/` | Jira evidence link | ADRs are versioned source-of-truth decisions. Jira may link them but must not replace them. |
| Risk Assessment | GitHub `docs/risks/` | Jira evidence link, Confluence summary | Risk records are versioned in GitHub when introduced. Stakeholder summaries may link to them. |
| Stakeholder hub | Confluence | README/GitHub links back to hub | Confluence is authoritative for stakeholder navigation and landing-page experience. |
| Stakeholder reports | Confluence | Jira links/evidence, GitHub links to canonical docs | Stakeholder reports live on Confluence because pages/forms are better suited there. Reports must not override GitHub technical truth. |
| Sprint review | GitHub for durable review docs; Jira for task state; Confluence for stakeholder report | PR links and Jira evidence | Sprint review evidence must be linkable and must not duplicate technical truth inconsistently. |
| PR evidence | GitHub | Jira evidence link | PRs are the primary evidence of repository changes. |
| Runtime evidence | GitHub when committed as logs/reports or linked from Jira | Jira evidence link | Runtime claims require evidence. Missing evidence means the claim remains `[UNVALIDATED]`. |
| `[UNVALIDATED]` claims | GitHub policy and source documents | Jira/Confluence must preserve marker | Any unproven claim must keep `[UNVALIDATED]` across all surfaces. |

---

## 4. Protected MVP Baseline

The MVP is protected by `docs/product/product-vision.md`.

The only firmware node in the MVP is:

```text
firmware/room-env-node/
```

The MVP node is a generic room/door node.

Inside MVP:

- temperature;
- humidity;
- local non-identifying presence;
- door open/closed state.

Outside MVP:

- person tracking;
- behavioral history;
- person identification;
- raw audio;
- window sensors;
- 220V automation;
- direct ESP32 Kafka publishing;
- commercial claims;
- safety-critical claims;
- production/security-grade certification claims.

The following service boundaries are target directories and must not be presented as production-ready runtime services unless later implementation evidence proves it:

```text
services/ingestion/
services/device-registry/
services/read-model/
services/ai-insight/
```

---

## 5. DOC-REGRESSION Policy

A DOC-REGRESSION is any documentation, ticket, page, comment, PR, or stakeholder report change that weakens, contradicts, duplicates incorrectly, or silently expands the canonical project truth.

A DOC-REGRESSION occurs when a change:

- contradicts GitHub source-of-truth documentation;
- expands MVP scope without reviewed approval;
- removes `[UNVALIDATED]` without evidence;
- declares target architecture as implemented runtime;
- declares production-ready, safety-critical, commercial-ready, or security-grade status without validation;
- moves technical source of truth from GitHub into Jira or Confluence;
- duplicates long-form technical documents in Confluence and creates divergence risk;
- changes canonical paths without updating semantic links;
- closes a task without the expected review/evidence trail.

### 5.1 Examples

Regression:

```text
The MVP includes window sensors.
```

Correction:

```text
Window sensors are outside MVP unless a later reviewed ADR changes this boundary.
```

Regression:

```text
The ESP32 publishes directly to Kafka.
```

Correction:

```text
Direct ESP32 Kafka publishing is outside MVP. Backend-side event streaming remains future scope `[UNVALIDATED]` until implemented and reviewed.
```

Regression:

```text
Confluence contains the official technical documentation.
```

Correction:

```text
Confluence contains stakeholder navigation and stakeholder reports. GitHub contains official technical documentation.
```

Regression:

```text
The AI insight service detects anomalies reliably.
```

Correction:

```text
The AI insight service boundary is a target direction `[UNVALIDATED]` until implementation and runtime evidence exist.
```

### 5.2 Severity

| Severity | Meaning | Examples | Required action |
|---|---|---|---|
| S0 — Blocking | Contradicts protected MVP, safety/security posture, or source-of-truth hierarchy | Direct ESP32 Kafka in MVP; production-ready claim; 220V automation in MVP | Block merge/review until fixed |
| S1 — High | Creates divergence between GitHub, Jira, and Confluence | Confluence duplicates technical docs and changes MVP wording | Block merge/review unless corrected or explicitly approved |
| S2 — Medium | Ambiguous maturity or missing `[UNVALIDATED]` marker | Target service described as implemented | Fix before approval |
| S3 — Low | Navigation, typo, broken link, unclear phrasing | Wrong path spelling; weak link label | Fix before or during review depending on impact |

### 5.3 Reporting format

Use this format in PR reviews, Jira comments, or review notes:

```text
DOC-REGRESSION

Severity: S0/S1/S2/S3
Location:
Canonical source violated:
Problem:
Expected correction:
Evidence:
```

### 5.4 Merge and review gate

A PR or review must not be approved while it contains unresolved S0 or S1 DOC-REGRESSION issues.

A PR or review should not be approved while it contains unresolved S2 issues involving `[UNVALIDATED]`, MVP scope, target/runtime confusion, or source-of-truth ambiguity.

### 5.5 Resolution flow

1. Identify the canonical source.
2. Correct the divergent document, ticket, page, comment, or PR.
3. Add or preserve `[UNVALIDATED]` when evidence is missing.
4. Update only links/summaries on Jira or Confluence when the GitHub source remains correct.
5. Update GitHub source of truth only through a reviewed repository change.
6. Link the fix as evidence.
7. Request review again.
8. Do not close the task without project owner approval.

---

## 6. Anti-Divergence Rule

### 6.1 GitHub vs Jira

If GitHub and Jira disagree on technical content, GitHub wins until a reviewed GitHub change updates the source of truth.

Jira remains authoritative for:

- backlog item existence;
- task state;
- workflow state;
- blockers;
- review status;
- evidence links.

Jira must not become a second technical documentation repository.

### 6.2 GitHub vs Confluence

If GitHub and Confluence disagree on technical content, GitHub wins until a reviewed GitHub change updates the source of truth.

Confluence remains authoritative for:

- stakeholder hub;
- stakeholder reports;
- stakeholder forms;
- stakeholder-facing navigation.

Confluence stakeholder reports may summarize progress and collect feedback through forms, but they must link to GitHub for technical truth and must preserve `[UNVALIDATED]` markers when referencing unproven claims.

### 6.3 When to update GitHub

Update GitHub when changing:

- Product Vision;
- MVP boundary;
- architecture baseline;
- source-of-truth rules;
- DOC-REGRESSION policy;
- `[UNVALIDATED]` policy;
- ADRs;
- risk assessments;
- canonical paths;
- source code;
- runtime evidence committed as project evidence.

### 6.4 When to update Jira or Confluence only

Update Jira or Confluence only when changing:

- task state;
- stakeholder report text;
- stakeholder forms;
- review comments;
- evidence links;
- PR links;
- navigation links;
- short summaries that do not change technical truth.

Never resolve a divergence by copying long-form GitHub technical documentation into Confluence. Fix the link, fix the summary, or update the GitHub source of truth through review.

---

## 7. `[UNVALIDATED]` Policy

`[UNVALIDATED]` marks any claim that is not yet proven by implementation, tests, logs, reviewed PRs, runtime evidence, or approved source-of-truth documentation.

Use `[UNVALIDATED]` for:

- target architecture not implemented yet;
- service boundaries without runtime evidence;
- firmware capabilities not tested yet;
- backend integrations not implemented yet;
- AI insight claims without validation;
- performance claims without measurement;
- reliability claims without evidence;
- security claims without specific validation;
- stakeholder-facing claims that could be interpreted as already proven.

Correct examples:

```text
The AI insight boundary is a target direction `[UNVALIDATED]`.
```

```text
Backend-side event streaming may be introduced later `[UNVALIDATED]`.
```

```text
Runtime reliability has not been measured yet `[UNVALIDATED]`.
```

Remove `[UNVALIDATED]` only when there is traceable evidence such as:

- implementation merged through PR;
- tests or logs committed or linked;
- runtime evidence reviewed;
- ADR approved;
- project owner approval recorded;
- source-of-truth document updated through review.

Forbidden unqualified claims:

```text
Production-ready
Security-grade
Safety-critical
Commercially ready
Certified access control
Alarm-grade intrusion detection
Direct ESP32 Kafka producer in MVP
Person tracking in MVP
Raw audio collection in MVP
```

---

## 8. Canonical Paths

Current canonical paths:

```text
README.md
```

```text
docs/product/product-vision.md
```

```text
docs/governance/stakeholder-transparency.md
```

```text
docs/governance/source-of-truth.md
```

Current MVP firmware path:

```text
firmware/room-env-node/
```

Target service boundary paths:

```text
services/ingestion/
services/device-registry/
services/read-model/
services/ai-insight/
```

Future candidate paths:

```text
docs/adr/
docs/risks/
docs/reviews/
docs/evidence/
docs/glossary/project-glossary.md
```

`docs/glossary/project-glossary.md` is a future candidate. It must not be created as a duplicate while the glossary remains embedded in the Product Vision or other existing governance sections.

---

## 9. AI Agent Semantic Routing

AI agents should use this routing order:

1. Start from `README.md` for the semantic map.
2. Read `docs/governance/source-of-truth.md` for source-of-truth and anti-regression rules.
3. Read `docs/product/product-vision.md` for Product Vision, MVP boundaries, and current glossary.
4. Read `docs/governance/stakeholder-transparency.md` for stakeholder visibility and Atlassian governance rules.
5. Use Jira for task state, workflow, review state, blockers, and evidence links.
6. Use Confluence for stakeholder hub, stakeholder reports, stakeholder forms, and navigation.

AI agents must not infer implementation maturity from directory names alone. Empty or placeholder paths are not runtime proof.

---

## 10. Acceptance Criteria

This policy satisfies IHAP-13 when:

- source-of-truth responsibility is defined for backlog, task state, code, documents, Product Vision, ADRs, Risk Assessments, stakeholder hub, stakeholder reports, sprint review, PR evidence, runtime evidence, and `[UNVALIDATED]` claims;
- DOC-REGRESSION is defined with examples and severity levels;
- reporting, blocking, and resolution flow are defined;
- GitHub/Jira/Confluence anti-divergence rules are explicit;
- `[UNVALIDATED]` usage and removal rules are documented;
- initial canonical repository paths are listed;
- stakeholder reports are explicitly assigned to Confluence;
- no firmware, backend, mobile, runtime, production-ready, security-grade, or safety-critical claim is introduced;
- project owner approval remains required before task completion.

---

## 11. Practical Rule

```text
Confluence reports and orients.
Jira tracks and links evidence.
GitHub defines the technical truth.
```

If they disagree on technical content, GitHub wins until a reviewed GitHub source-of-truth change says otherwise.
