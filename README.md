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
  scrum_governance_dor_dod: "docs/governance/scrum-governance-dor-dod.md"
  ai_review_agents_policy: "docs/governance/ai-review-agents-policy.md"
  ai_review_agent_playbook: "docs/governance/ai-review-agent-playbook.md"
  governance_lane_review_gate: "docs/governance/governance-lane-review-gate.md"
  team_working_rules: "docs/governance/team-working-rules.md"
  engineering_assistant_rules: "docs/governance/engineering-assistant-rules.md"
  documentation_strategy: "docs/governance/documentation-strategy.md"
  cost_governance_and_bom_policy: "docs/governance/cost-governance-and-bom-policy.md"
  docs_landing_page: "docs/README.md"
  templates_index: "docs/templates/README.md"
  risk_assessment_template: "docs/templates/risk-assessment.md"
  risk_index: "docs/risks/README.md"
  risk_model_baseline: "docs/risks/risk-model-baseline.md"
  risk_records_path: "docs/risks/records/"
  adr_index: "docs/adr/README.md"
  adr_template: "docs/adr/template.md"
  product_vision: "docs/product/product-vision.md"
  stakeholder_transparency: "docs/governance/stakeholder-transparency.md"
  stakeholder_report_data_rules: "docs/governance/stakeholder-report-data-rules.md"
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
  - Read docs/README.md for documentation navigation under docs/.
  - Read docs/governance/source-of-truth.md before modifying docs, governance, Jira evidence, Confluence summaries, canonical paths, or commit convention.
  - Read docs/governance/documentation-strategy.md before creating, moving, splitting, merging, deprecating, or reorganizing repository documentation.
  - Read docs/governance/cost-governance-and-bom-policy.md before changing hardware BOM records, price snapshots, shipping treatment, replication-cost claims, paid-tool boundaries, or central-node cost requirements.
  - Read docs/templates/README.md before creating, using, moving, or changing reusable project templates.
  - Read docs/risks/risk-model-baseline.md before changing project risk taxonomy, scoring, residual risk treatment, risk evidence, or stakeholder risk visibility.
  - Read docs/risks/README.md and docs/risks/records/ before changing concrete risk records.
  - Read docs/governance/shift-left-governance-baseline.md before planning issue-level impact blocks, review readiness, or Jira evidence.
  - Read docs/governance/scrum-governance-dor-dod.md before evaluating Definition of Ready, Definition of Done, Jira workflow movement, or minimum evidence expectations.
  - Read docs/governance/ai-review-agents-policy.md before understanding review-agent roles, severity model, and decision limits.
  - Read docs/governance/ai-review-agent-playbook.md before running concrete review-agent prompts or producing review summaries.
  - Read docs/governance/governance-lane-review-gate.md before moving governance-lane tasks toward review, stakeholder review, or Done.
  - Read docs/governance/team-working-rules.md before changing daily collaboration rules, blocker handling, evidence discipline, working agreements, or AI assistant usage boundaries.
  - Read docs/governance/engineering-assistant-rules.md before using or changing engineering assistant operating boundaries, allowed actions, forbidden actions, or assistant evidence rules.
  - Read docs/adr/README.md before adding or changing ADRs, ADR naming, ADR status, or ADR link policy.
  - Read docs/adr/template.md before drafting a new ADR.
  - Read docs/product/product-vision.md before changing MVP scope, product language, glossary terms, firmware boundaries, service boundary wording, or stakeholder claims.
  - Read docs/governance/stakeholder-transparency.md before changing stakeholder visibility, Atlassian governance, Jira evidence comments, or Confluence hub/report behavior.
  - Read docs/governance/stakeholder-report-data-rules.md before changing what stakeholder reports may show, link, redact, or block.
  - Do not infer runtime maturity from folder names.
  - Preserve [UNVALIDATED] on all unproven claims.
  - Do not introduce production-ready, safety-critical, commercial-ready, or security-grade claims without reviewed evidence.
-->

---

## Semantic Index

| Need | Canonical path / surface | Rule |
|---|---|---|
| Source-of-truth rules | `docs/governance/source-of-truth.md` | Defines GitHub/Jira/Confluence roles, DOC-REGRESSION, anti-divergence, canonical paths, commit convention, and `[UNVALIDATED]` policy. |
| Documentation strategy | `docs/governance/documentation-strategy.md` | Defines document families, when to create or update docs, anti-stale behavior, and documentation surface policy without duplicating source-of-truth rules. |
| Cost governance and BOM policy | `docs/governance/cost-governance-and-bom-policy.md` | Defines dated hardware-price snapshots, complete edge/central/shared cost separation, shipping treatment, replication-cost rules, and paid-tool boundaries without executing purchases. |
| Docs landing page | `docs/README.md` | Provides navigable documentation index for `docs/` without replacing canonical documents or duplicating long-form rules. |
| Project templates | `docs/templates/README.md` | Indexes reusable project templates and links canonical templates without duplicating their source documents. |
| Risk documentation | `docs/risks/README.md` | Indexes the risk modeling guide and concrete risk records. |
| Risk model baseline | `docs/risks/risk-model-baseline.md` | Defines how project risks are modeled, scored, linked, and reviewed. |
| Shift Left governance baseline | `docs/governance/shift-left-governance-baseline.md` | Defines the mandatory issue-level impact block for security, privacy, cost, compliance, testing, documentation, and stakeholder visibility. |
| Scrum governance, DoR and DoD | `docs/governance/scrum-governance-dor-dod.md` | Defines lightweight Scrum governance, Definition of Ready, Definition of Done, Jira workflow movement, minimum evidence expectations, and Project Owner authority. |
| AI review agents policy | `docs/governance/ai-review-agents-policy.md` | Defines Sprint 0 advisory review agents, severity model, review output template, and non-decision-making limits. |
| AI review agent playbook | `docs/governance/ai-review-agent-playbook.md` | Provides concrete copy-paste prompts and the operating flow for using review agents in Jira, GitHub, PR, and stakeholder reviews. |
| Governance lane review gate | `docs/governance/governance-lane-review-gate.md` | Defines when governance-lane tasks may advance toward review, stakeholder review, or Done without source-of-truth divergence, missing evidence, unsupported claims, or premature AI/Project Owner authority violations. |
| Team working rules | `docs/governance/team-working-rules.md` | Defines lightweight daily operating rules, collaboration boundaries, blocker handling, evidence discipline, and AI assistant usage boundaries. |
| Engineering assistant rules | `docs/governance/engineering-assistant-rules.md` | Defines engineering assistant allowed actions, forbidden actions, operating flow, evidence expectations, and Project Owner authority boundaries. |
| ADR index and template | `docs/adr/README.md`, `docs/adr/template.md` | Defines ADR index, naming convention, status model, template, and link policy. |
| Product Vision and MVP boundary | `docs/product/product-vision.md` | Canonical source for Product Vision, MVP inclusions/exclusions, and current glossary. |
| Stakeholder transparency | `docs/governance/stakeholder-transparency.md` | Defines stakeholder visibility, Jira evidence behavior, and Confluence hub usage. |
| Stakeholder report data rules | `docs/governance/stakeholder-report-data-rules.md` | Defines what stakeholder reports may show, link, redact, or block. |
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
│   ├── README.md
│   ├── adr/
│   ├── architecture/
│   ├── governance/
│   ├── product/
│   ├── risks/
│   └── templates/
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
| Docs | Source-of-truth governance, Documentation Strategy, Cost Governance and BOM Policy, Project Templates, Risk Model Baseline, Risk Records, Shift Left governance, Scrum governance DoR/DoD, AI review agents policy, AI review agent playbook, Governance Lane Review Gate, Team Working Rules, Engineering Assistant Rules, ADR index/template, Product Vision, Risk Assessments, stakeholder transparency, stakeholder report data rules |

---

## Current Status

This repository is in Sprint 0. The current focus is repository structure, product/governance documentation, source-of-truth rules, anti-regression policy, Documentation Strategy, Cost Governance and BOM Policy, Project Templates, Risk Model Baseline, Risk Records, Shift Left governance baseline, Scrum governance DoR/DoD, AI review-agent policy/playbook, Governance Lane Review Gate, Team Working Rules, Engineering Assistant Rules, ADR index/template, stakeholder report data rules, and explicit MVP boundaries.

Nothing in this repository should be interpreted as production-ready, security-grade, safety-critical, or commercially ready unless a later reviewed source-of-truth document and implementation evidence prove it.

---

## Why It Matters

HomeEdge is intended to be the main technical portfolio project: it combines embedded systems, backend architecture, mobile development, DevOps basics, stakeholder transparency, and project governance in one coherent platform.