# Stakeholder Transparency and Atlassian Governance

**Issue:** IHAP-12 — S0-003 — Stakeholder Transparency and Atlassian Governance  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Document type:** Stakeholder transparency / governance documentation  
**Status:** Sprint 0 draft for review  
**Source of truth:** This versioned repository document is the source of truth for stakeholder transparency rules, Atlassian governance responsibilities, decision/risk traceability, redaction policy, and stakeholder reporting conventions until superseded by a later reviewed change.

<!--
AI_AGENT_METADATA:
  issue: IHAP-12
  document_type: stakeholder_transparency_governance
  source_of_truth: github_versioned_repository_documentation
  task_scope: documentation_governance_only
  runtime_changes_allowed: false
  firmware_changes_allowed: false
  backend_changes_allowed: false
  mobile_changes_allowed: false
  production_ready_claims_allowed: false
  unvalidated_claim_marker: "[UNVALIDATED]"
  repository_source_of_truth_for:
    - documents
    - decisions
    - risks
    - policies
    - technical_baselines
    - governance_rules
  jira_role:
    - tracking
    - workflow_state
    - review_state
    - evidence_links
    - blockers
    - stakeholder_navigation
  confluence_role:
    - optional_stakeholder_facing_hub
    - summary_navigation_layer
    - not_source_of_truth
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
    - production_grade_security_certification
    - commercial_claims
    - safety_critical_claims
  target_service_boundaries:
    - services/ingestion/
    - services/device-registry/
    - services/read-model/
    - services/ai-insight/

HIDDEN_ANTI_REGRESSION_RULES:
  - The repository remains the source of truth for documentation, decisions, risks, policies, and technical baselines.
  - Jira must not duplicate source-of-truth documents; it must expose state, evidence links, review status, blockers, and stakeholder navigation.
  - Confluence may be used only as a stakeholder-facing hub or summary layer; it must not replace or duplicate the repository source of truth.
  - The only firmware node in the MVP remains firmware/room-env-node/.
  - firmware/room-env-node/ remains a generic room/door node.
  - The MVP includes temperature, humidity, local non-identifying presence detection, and door open/closed state.
  - Raw audio, person tracking, behavioral history, identity inference, window scope, 220V automation, and direct ESP32 Kafka publishing remain out of MVP.
  - The four service directories remain TARGET boundaries unless validated by later implementation evidence.
  - Stakeholder-facing reports must not weaken, expand, or silently reinterpret MVP boundaries.
  - Any unproven claim must be marked as [UNVALIDATED].
-->

---

## 1. Purpose

This document defines how HomeEdge AI Platform gives ITS professors, reviewers, and project stakeholders a fast, clear, and evidence-backed view of project progress.

The goal is not to create bureaucracy. The goal is to make the project observable in a few clicks:

- what is being built;
- what has been completed;
- what is in review;
- what requires stakeholder attention;
- what is blocked;
- which risks and decisions exist;
- where the source-of-truth evidence lives;
- which claims are validated and which remain `[UNVALIDATED]`.

This document is limited to stakeholder transparency, Jira/Atlassian governance, reporting conventions, redaction rules, and anti-duplication rules. It does not introduce firmware, backend, mobile, infrastructure, runtime services, Kafka integration, AI implementation, production deployment, or security-grade certification.

---

## 2. Governance Principle: Repository as Source of Truth

The repository is the official source of truth for the project.

The repository owns:

- product documentation;
- governance documentation;
- decision records;
- risk records;
- technical baselines;
- anti-regression rules;
- versioned evidence documents;
- Sprint 0 source-of-truth documents;
- reviewed changes through pull requests.

Jira and Confluence may expose, summarize, or link to this information, but they must not replace it.

Rule:

```text
If it defines the project, it belongs in the repository.
```

If Jira, Confluence, or a stakeholder report disagrees with the reviewed repository documentation, the repository version wins unless the project owner explicitly approves a new source-of-truth change.

---

## 3. Stakeholder Navigation Model

Stakeholders must be able to understand the project quickly without manually searching through every file, branch, task, or pull request.

The intended navigation path is:

```text
Jira board
  -> Jira issue
  -> evidence links
  -> GitHub PR
  -> repository source-of-truth document
  -> optional Confluence stakeholder hub or report
```

A stakeholder should be able to identify within a few clicks:

- the current project phase;
- the active sprint or preparation phase;
- the state of relevant Jira tasks;
- completed work;
- work in review;
- work in stakeholder review;
- open blockers;
- open risks;
- key decisions;
- source-of-truth documents;
- pull requests supporting delivered work;
- `[UNVALIDATED]` claims and validation gaps.

The stakeholder-facing layer must optimize for clarity, not volume.

---

## 4. Tool Responsibilities

### 4.1 GitHub Repository

GitHub is the technical and governance source of truth.

It must contain:

- versioned project documentation;
- product vision and MVP boundaries;
- governance policies;
- decision and risk records when introduced by dedicated tasks;
- reviewed pull requests;
- source-of-truth markdown files;
- technical baselines;
- anti-regression rules.

GitHub must not be used to claim completion of work that has no Jira tracking or project-owner review path.

### 4.2 Jira

Jira is the project tracking and stakeholder navigation layer.

Jira must expose:

- issue status;
- sprint visibility;
- review state;
- stakeholder review state;
- blockers;
- concise evidence summaries;
- links to GitHub PRs;
- links to repository source-of-truth documents;
- project-owner action requests.

Jira must not duplicate full repository documents, decision records, risk registers, or technical policies.

Rule:

```text
Jira tells where the truth is and what state it is in. Jira is not the source of truth itself.
```

### 4.3 Confluence

Confluence may be used as an optional stakeholder-facing hub.

Acceptable Confluence content:

- project landing page;
- stakeholder navigation index;
- short sprint summaries;
- links to Jira board;
- links to GitHub repository;
- links to repository documents;
- links to PR evidence;
- links to stakeholder reports.

Confluence must not contain duplicated source-of-truth technical documentation, duplicated risk registers, duplicated decisions, or stronger claims than the repository.

Rule:

```text
Confluence is a map, not the territory.
```

---

## 5. Minimum Stakeholder View

A stakeholder-facing view is sufficient only if it lets a professor or reviewer understand the current state quickly.

The minimum stakeholder view must include:

| Area | Required information |
|---|---|
| Project status | Current phase, active sprint/preparation state, high-level health |
| Completed work | Completed issues with evidence links |
| In review | Issues requiring technical/project-owner review |
| Stakeholder review | Issues ready for stakeholder visibility or feedback |
| Blockers | What is blocked, why, impact, requested decision |
| Risks | Open risk summary and source-of-truth link |
| Decisions | Decision summary and source-of-truth link |
| Evidence | PRs, repository files, reviewed documents |
| `[UNVALIDATED]` | Claims or assumptions not yet proven |
| Next actions | Clear owner-facing next steps |

The view must be concise enough to read quickly, but complete enough to avoid hiding risk, uncertainty, or review gaps.

---

## 6. Jira Evidence Policy

Every Jira issue that produces a repository artifact, pull request, decision, risk, or stakeholder-facing output should receive an evidence comment.

Recommended Jira evidence format:

```md
IHAP-XX evidence summary

Status:
- <Planning / In Progress / In Review / Stakeholder Review / Done>

Produced:
- <short output summary>

Source of truth:
- Repository document: <path>
- Pull request: <link>

Stakeholder summary:
- <1-3 bullets understandable without reading the full repository>

Risks / blockers:
- <none / list>

Validation:
- <what has been reviewed>
- <what remains [UNVALIDATED]>

Project owner action:
- <review / approve / request changes / move to stakeholder review>
```

Jira comments must summarize and link. They must not paste full source-of-truth documents.

---

## 7. Stakeholder Report Policy

Stakeholder reports are summaries, not source-of-truth documents.

A stakeholder report should help a professor or reviewer understand the project state without reading every Jira issue or GitHub diff.

Minimum stakeholder report template:

```md
# Stakeholder Report — <Sprint / Date>

## Executive Snapshot
- Current phase:
- Current sprint:
- Overall status:
- Main completed outputs:
- Main risks:
- Decisions needed:

## Completed Since Last Report
- IHAP-XX — summary — evidence link

## In Review
- IHAP-XX — summary — PR/repository link

## Stakeholder Review
- IHAP-XX — what stakeholder should check

## Open Risks
- Risk:
- Impact:
- Source of truth:

## Decisions
- Decision:
- Source of truth:

## [UNVALIDATED] Items
- Claim:
- Why unvalidated:
- Next validation action:

## Links
- Jira board:
- Repository:
- Product Vision:
- Current sprint evidence:
```

A report may live in the repository or be linked from Confluence. If copied into Confluence for readability, it must link back to the repository source or PR evidence.

---

## 8. Redaction Policy

Stakeholder-facing material must not expose private, sensitive, or security-relevant data.

Forbidden or redacted information includes:

- API keys;
- tokens;
- passwords;
- private IP addresses;
- domestic network details;
- private physical addresses;
- raw logs containing secrets or personal data;
- personal data not needed for review;
- raw audio;
- private images or videos;
- person identification;
- individual tracking data;
- behavioral history;
- detailed security-sensitive implementation data not needed for stakeholder review.

If sensitive information is required for debugging, it must be redacted before being shared in Jira, Confluence, stakeholder reports, screenshots, or public repository documentation.

---

## 9. Claim Classification Policy

Every important project statement should be understandable as one of the following classes.

| Class | Meaning |
|---|---|
| `DONE` | Completed and supported by evidence/review |
| `PLANNED` | Intended future work, not completed |
| `IN REVIEW` | Produced, waiting for technical/project-owner review |
| `STAKEHOLDER REVIEW` | Stable enough for stakeholder visibility or feedback |
| `RISK` | Known uncertainty or possible negative outcome |
| `DECISION` | Approved project direction or constraint |
| `[UNVALIDATED]` | Not implemented, not tested, not approved, or not proven |
| `OUT OF SCOPE` | Explicitly excluded from current scope or MVP |

Examples:

```text
DONE: IHAP-11 defined the MVP boundaries in docs/product/product-vision.md.
```

```text
PLANNED: The service directories are target boundaries for future implementation.
```

```text
[UNVALIDATED]: The stakeholder report format has not yet been validated by professors.
```

```text
OUT OF SCOPE: Direct ESP32 Kafka publishing is outside the MVP.
```

Unclear maturity must always be marked down, not up.

---

## 10. Decision and Risk Traceability

Decisions and risks must be traceable to repository source-of-truth artifacts when introduced by project tasks.

Jira may summarize decisions and risks for quick navigation, but the durable record must be versioned in the repository.

A decision or risk reference should include:

- short title;
- linked Jira issue;
- repository source-of-truth file;
- current status;
- owner or reviewer expectation;
- impact on scope, MVP, architecture, security, privacy, cost, or stakeholder visibility.

If a decision or risk has not yet been recorded in the repository, it must be treated as `[UNVALIDATED]` or pending until documented and reviewed.

---

## 11. Anti-Duplication Rules

To avoid governance noise and inconsistency:

1. Do not copy full repository documents into Jira.
2. Do not copy full repository documents into Confluence.
3. Jira must link to repository paths and pull requests.
4. Confluence must link to repository paths, Jira board, and stakeholder reports.
5. Decisions and risks must be versioned in the repository.
6. Jira may summarize decisions and risks, but must point to the source-of-truth file.
7. Stakeholder reports must summarize and link, not duplicate.
8. If Jira/Confluence and the repository disagree, the repository wins unless a new reviewed change updates the source of truth.

This prevents the project from becoming bureaucratic while keeping it reviewable.

---

## 12. Anti-Regression Rules

Stakeholder-facing summaries must not weaken, expand, or silently reinterpret the approved Sprint 0 baseline.

Protected baseline from IHAP-10/IHAP-11:

### MVP firmware path

```text
firmware/room-env-node/
```

### MVP node semantics

The MVP node is a generic room/door node.

### Inside MVP

- temperature;
- humidity;
- local non-identifying presence detection;
- door open/closed state.

### Outside MVP

- person tracking;
- behavioral history;
- person identification;
- raw audio;
- windows;
- 220V automation;
- direct ESP32 Kafka publishing;
- commercial claims;
- safety-critical claims;
- production/security-grade certification claims.

### Target service boundaries

The following directories are target service boundaries, not proof of implemented production services:

```text
services/ingestion/
services/device-registry/
services/read-model/
services/ai-insight/
```

Any stakeholder report, Jira comment, Confluence page, or future governance document that contradicts this baseline must be treated as a regression risk until reviewed and explicitly approved by the project owner.

---

## 13. Review and Approval Flow

Recommended flow for documentation/governance tasks:

```text
Ready
  -> In Progress
  -> Pull Request opened
  -> In Review
  -> Project owner review
  -> Stakeholder Review when appropriate
  -> Done only after explicit approval
```

A merged pull request does not automatically mean the Jira issue is complete unless the project owner has approved that rule for the task.

For stakeholder-facing outputs, the review must check:

- repository source-of-truth alignment;
- no duplicate source-of-truth content in Jira/Confluence;
- no sensitive information exposure;
- no unvalidated production, security, commercial, or safety-critical claims;
- no regression against IHAP-10/IHAP-11 MVP boundaries;
- clear links from Jira to repository evidence;
- sufficient readability for professors/reviewers.

---

## 14. Out of Scope

This document does not implement or validate:

- firmware changes;
- backend services;
- mobile application features;
- runtime telemetry;
- Kafka integration;
- AI inference;
- CI/CD;
- security certification;
- production deployment;
- safety-critical behavior;
- commercial readiness.

Any claim in those areas must remain `[UNVALIDATED]` unless supported by a later reviewed implementation task and source-of-truth evidence.
