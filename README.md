# HomeEdge AI Platform

**Educational edge-first smart home platform built around an ESP32-C3 MVP node, target backend service boundaries, mobile monitoring direction, and source-of-truth governance.**

HomeEdge is a portfolio and ITS project focused on building a smart home platform in a controlled, reviewable, and anti-regression way.

At Sprint 0, the repository prioritizes explicit boundaries over premature runtime claims. Directories may describe target architecture, not necessarily implemented production services.

<!--
AI_AGENT_METADATA:
  project: "[ITS] [EDGE] HomeEdge AI Platform"
  jira_project_key: "IHAP"
  repository: "pianic2/homeedge-ai-platform"
  document_role: "root_semantic_index"
  source_of_truth_policy: "docs/governance/source-of-truth.md"
  shift_left_governance_baseline: "docs/governance/shift-left-governance-baseline.md"
  ai_review_agents_policy: "docs/governance/ai-review-agents-policy.md"
  product_vision: "docs/product/product-vision.md"
  stakeholder_transparency: "docs/governance/stakeholder-transparency.md"
  current_glossary_location: "docs/product/product-vision.md"
  standalone_glossary_status: "future_candidate_not_created_by_ihap_13"
  stakeholder_hub: "https://niccolopiazzi01.atlassian.net/wiki/spaces/IEHAP/overview"
  stakeholder_reports_authoritative_surface: "Confluence"
  source_of_truth_roles:
    github: "technical truth, code, versioned docs, decisions, risks, policies, baselines, PR evidence"
    jira: "backlog, workflow state, task status, review state, blockers, evidence links"
    confluence: "stakeholder hub, stakeholder reports, stakeholder forms, navigation"
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
  target_service_boundaries_unvalidated:
    - services/ingestion/
    - services/device-registry/
    - services/read-model/
    - services/ai-insight/
  unvalidated_claim_marker: "[UNVALIDATED]"

AI_AGENT_ROUTING:
  - Start here for repository semantic navigation.
  - Read docs/governance/source-of-truth.md before modifying docs, governance, Jira evidence, Confluence summaries, canonical paths, or commit convention.
  - Read docs/governance/shift-left-governance-baseline.md before planning issue-level impact blocks, review readiness, or Jira evidence.
  - Read docs/governance/ai-review-agents-policy.md before running advisory review-agent checks, classifying findings, or producing review summaries.
  - Read docs/product/product-vision.md before changing MVP scope, product language, glossary terms, firmware boundaries, service boundary wording, or stakeholder claims.
  - Read docs/governance/stakeholder-transparency.md before changing stakeholder visibility, Atlassian governance, Jira evidence comments, or Confluence hub/report behavior.
  - Do not infer runtime maturity from folder names.
  - Preserve [UNVALIDATED] on all unproven claims.
  - Do not introduce production-ready, safety-critical, commercial-ready, or security-grade claims without reviewed evidence.
-->

---

## Semantic Index

| Need | Canonical path / surface | Rule |
|---|---|---|
| Source-of-truth rules | `docs/governance/source-of-truth.md` | Defines GitHub/Jira/Confluence roles, DOC-REGRESSION, anti-divergence, canonical paths, commit convention, and `[UNVALIDATED]` policy. |
| Shift Left governance baseline | `docs/governance/shift-left-governance-baseline.md` | Defines the mandatory issue-level impact block for security, privacy, cost, compliance, testing, documentation, and stakeholder visibility. |
| AI review agents policy | `docs/governance/ai-review-agents-policy.md` | Defines Sprint 0 advisory review agents, severity model, review output template, and non-decision-making limits. |
| Product Vision and MVP boundary | `docs/product/product-vision.md` | Canonical source for Product Vision, MVP inclusions/exclusions, and current glossary. |
| Stakeholder transparency | `docs/governance/stakeholder-transparency.md` | Defines stakeholder visibility, Jira evidence behavior, and Confluence hub usage. |
| Stakeholder hub and reports | Confluence | Confluence is authoritative for stakeholder-facing hub, reports, forms, and navigation. |
| Backlog and task state | Jira | Jira is authoritative for backlog, workflow state, task status, blockers, review state, and evidence links. |
| Code and PR evidence | GitHub | GitHub is authoritative for code, repository structure, commits, branches, PRs, and versioned technical documentation. |

Operating rule:

```text
Confluence reports and orients.
Jira tracks and links evidence.
GitHub defines the technical truth.
```

If GitHub and Jira/Confluence diverge on technical content, GitHub wins until a reviewed GitHub source-of-truth change updates the project truth.

---

## Purpose

The project is designed to demonstrate a complete engineering path:

- embedded firmware for ESP32-C3 devices;
- smart home sensor integration;
- structured event collection direction;
- backend API/service-boundary design `[UNVALIDATED]`;
- mobile-first monitoring direction `[UNVALIDATED]`;
- reproducible setup;
- technical documentation and governance.

---

## Sprint 0 Repository Skeleton

This repository starts with a deliberately small and explicit skeleton. The goal is to make project boundaries visible before runtime implementation expands.

```text
homeedge-ai-platform/
├── apps/
│   └── mobile/
├── docs/
│   ├── adr/
│   ├── architecture/
│   ├── governance/
│   └── product/
├── firmware/
│   └── room-env-node/
├── infrastructure/
├── schemas/
├── scripts/
├── services/
│   ├── ingestion/
│   ├── device-registry/
│   ├── read-model/
│   └── ai-insight/
└── tools/
```

### MVP boundary

The only firmware node in the MVP skeleton is:

```text
firmware/room-env-node/
```

This node is a generic room/door node.

Inside MVP:

- temperature;
- humidity;
- local non-identifying presence detection;
- door open/closed state.

Outside MVP:

- raw audio collection;
- person tracking;
- behavioral history;
- person identification;
- window sensor scope;
- 220V automation;
- direct ESP32 Kafka publishing;
- commercial claims;
- safety-critical claims;
- production/security-grade certification claims.

### Backend target topology

The backend target is represented as four service boundaries:

```text
services/ingestion/
services/device-registry/
services/read-model/
services/ai-insight/
```

These directories are **target service boundaries** `[UNVALIDATED]`, not proof that production-ready services already exist.

---

## Architecture Direction

```text
Edge Nodes -> Backend Services -> Mobile Dashboard -> AI-ready Insights
```

- **Edge Nodes:** collect room-level signals within the MVP boundary.
- **Backend Services:** target boundaries for receiving, validating, and exposing data `[UNVALIDATED]`.
- **Mobile Dashboard:** target direction for room state, latest telemetry, and device health visibility `[UNVALIDATED]`.
- **AI-ready Insights:** future target direction based on validated data `[UNVALIDATED]`.

---

## Stack Direction

| Area | Stack / direction |
|---|---|
| Firmware | ESP32-C3, ESP-IDF, C |
| Backend | Java, Spring Boot, REST APIs `[UNVALIDATED]` |
| Mobile | TypeScript, React Native, Expo `[UNVALIDATED]` |
| DevOps | Docker, GitHub Actions, Linux `[UNVALIDATED]` |
| Docs | Source-of-truth governance, Shift Left governance, AI review agents policy, Product Vision, ADRs, Risk Assessments, stakeholder transparency |

---

## Current Status

This repository is in Sprint 0. The current focus is repository structure, product/governance documentation, source-of-truth rules, anti-regression policy, Shift Left governance baseline, AI review-agent policy, and explicit MVP boundaries.

Nothing in this repository should be interpreted as production-ready, security-grade, safety-critical, or commercially ready unless a later reviewed source-of-truth document and implementation evidence prove it.

---

## Why It Matters

HomeEdge is intended to be the main technical portfolio project: it combines embedded systems, backend architecture, mobile development, DevOps basics, stakeholder transparency, and project governance in one coherent platform.