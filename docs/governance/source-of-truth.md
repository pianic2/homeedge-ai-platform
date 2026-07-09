# Source of Truth and DOC-REGRESSION Policy

**Issue:** IHAP-13 — S0-004 — Source of Truth and DOC-REGRESSION Policy  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Document type:** Documentation / Source of Truth governance  
**Status:** Sprint 0 draft for review  
**Source of truth:** This versioned GitHub document is the canonical policy for source-of-truth rules, document divergence handling, DOC-REGRESSION handling, canonical paths, and `[UNVALIDATED]` claim governance until superseded by a later reviewed change.

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
  commercial_ready_claims_allowed: false
  security_grade_claims_allowed: false
  unvalidated_claim_marker: "[UNVALIDATED]"
  canonical_policy_file: "docs/governance/source-of-truth.md"
  canonical_documentation_strategy: "docs/governance/documentation-strategy.md"
  canonical_docs_landing_page: "docs/README.md"
  canonical_templates_index: "docs/templates/README.md"
  canonical_risk_assessment_template: "docs/templates/risk-assessment.md"
  canonical_risk_index: "docs/risks/README.md"
  canonical_risk_model_baseline: "docs/risks/risk-model-baseline.md"
  canonical_risk_records_path: "docs/risks/records/"
  canonical_shift_left_governance_baseline: "docs/governance/shift-left-governance-baseline.md"
  canonical_scrum_governance_dor_dod: "docs/governance/scrum-governance-dor-dod.md"
  canonical_governance_lane_review_gate: "docs/governance/governance-lane-review-gate.md"
  canonical_team_working_rules: "docs/governance/team-working-rules.md"
  canonical_engineering_assistant_rules: "docs/governance/engineering-assistant-rules.md"
  canonical_adr_index: "docs/adr/README.md"
  canonical_adr_template: "docs/adr/template.md"
  canonical_product_vision: "docs/product/product-vision.md"
  canonical_stakeholder_transparency: "docs/governance/stakeholder-transparency.md"
  canonical_stakeholder_report_data_rules: "docs/governance/stakeholder-report-data-rules.md"
  commit_convention: "IHAP-XX: Commit message"
  stakeholder_report_authoritative_surface: "Confluence"
  confluence_stakeholder_hub: "https://niccolopiazzi01.atlassian.net/wiki/spaces/IEHAP/overview"
  repository_source_of_truth_for:
    - code
    - technical_documents
    - docs_landing_page
    - product_vision
    - adr
    - risk_model_baseline
    - risk_records
    - risk_assessment
    - templates
    - policies
    - technical_baselines
    - governance_rules
    - documentation_strategy
    - stakeholder_report_data_rules
    - scrum_governance_dor_dod
    - governance_lane_review_gate
    - team_working_rules
    - engineering_assistant_rules
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

HIDDEN_ANTI_REGRESSION_RULES:
  - GitHub remains the source of truth for technical documents, decisions, risks, policies, technical baselines, governance rules, templates, source code, and PR evidence.
  - docs/README.md is a documentation landing page only; it must not replace this source-of-truth policy or duplicate long-form canonical documents.
  - Jira remains authoritative for backlog, task state, workflow state, blockers, review state, and evidence links.
  - Confluence remains authoritative for stakeholder hub, stakeholder reports, stakeholder forms, and stakeholder navigation.
  - Confluence stakeholder reports may summarize project state but must not override GitHub source-of-truth technical documents.
  - Confluence must not duplicate long-form technical source-of-truth documents from GitHub.
  - If GitHub and Jira diverge on technical content, GitHub wins until a reviewed GitHub change updates the source of truth.
  - If GitHub and Confluence diverge on technical content, GitHub wins and Confluence must be realigned as a stakeholder-facing summary or link layer.
  - Any unproven claim must be marked as [UNVALIDATED].
  - The protected MVP boundary must not be silently expanded.
  - The four service directories are target service boundaries unless validated by later implementation evidence.
-->

---

## 1. Purpose

This document defines the operating rules for source of truth, document divergence, DOC-REGRESSION handling, canonical paths, and `[UNVALIDATED]` claims in HomeEdge AI Platform.

Core rule:

```text
GitHub contains the technical truth.
Jira tracks work and review state.
Confluence presents stakeholder navigation and stakeholder reports.
```

This document is governance-only. It does not introduce firmware, backend, mobile, infrastructure, cloud, Kafka runtime, AI runtime, production readiness, safety-critical guarantees, commercial readiness, or security-grade certification.

---

## 2. Scope

Included:

- source-of-truth ownership by domain;
- DOC-REGRESSION definition and severity;
- anti-divergence rules for GitHub, Jira, and Confluence;
- `[UNVALIDATED]` claim policy;
- canonical repository paths;
- merge/review blocking rules for documentation regressions;
- protected MVP boundaries inherited from Product Vision;
- Jira-linked commit convention;
- Docs Landing Page registration;
- Documentation Strategy registration;
- Templates index and Risk Assessment template registration;
- Risk Model Baseline registration;
- Scrum Governance, DoR and DoD registration;
- Governance Lane Review Gate registration;
- Team Working Rules registration;
- Engineering Assistant Rules registration;
- ADR index and template registration;
- Stakeholder Report Data Rules registration.

Excluded:

- firmware implementation;
- backend implementation;
- mobile implementation;
- runtime validation;
- cloud deployment;
- production-readiness claims;
- safety-critical claims;
- commercial readiness claims;
- security-grade claims;
- stakeholder report creation.

Stakeholder reports are intentionally kept on Confluence because Confluence supports stakeholder-facing pages and forms. They must remain summary/reporting artifacts and must not override GitHub technical source-of-truth documents.

---

## 3. Source of Truth Matrix

| Domain | Authoritative source | Secondary surface | Rule |
|---|---|---|---|
| Backlog | Jira | GitHub only as linked evidence | Jira owns backlog items, prioritization, workflow state, blockers, and review state. |
| Task status | Jira | Confluence summary only | Jira is authoritative for Backlog, Ready, In Progress, In Review, Stakeholder Review, Done, and blockers. |
| Code | GitHub | Jira PR links | GitHub is authoritative for source code, repository structure, commits, branches, and PR evidence. |
| Commits and branches | GitHub | Jira issue links | Jira-linked commits should start with the issue key, for example `IHAP-35: Register governance gate canonical path`. |
| Technical documents | GitHub | Confluence link/summary only | Technical documents must live in the repository. Confluence must not become a duplicate technical documentation repository. |
| Root semantic index | `README.md` | Jira/PR evidence links | Provides repository-level navigation and maturity warnings. It must not replace canonical policy documents. |
| Docs landing page | `docs/README.md` | Jira/PR evidence links | Provides navigable documentation index for `docs/`. It links canonical documents and must not redefine or duplicate them. |
| Source-of-truth policy | `docs/governance/source-of-truth.md` | Jira/PR evidence links | Defines source-of-truth hierarchy, DOC-REGRESSION, canonical paths, and `[UNVALIDATED]` policy. |
| Documentation Strategy | `docs/governance/documentation-strategy.md` | Jira/PR evidence links | Defines document families, when to create or update documents, anti-stale behavior, and documentation surface policy without replacing this source-of-truth policy. |
| Templates index | `docs/templates/README.md` | Jira/PR evidence links | Indexes reusable project templates and links existing canonical templates without duplicating them. |
| Risk Assessment template | `docs/templates/risk-assessment.md` | Jira/PR evidence links | Provides a minimal template for future risk assessments; concrete risk records are created only by explicit task need. |
| Risk documentation index | `docs/risks/README.md` | Jira/PR evidence links, Confluence summary | Routes risk documentation without accepting or duplicating risk decisions. |
| Risk Model Baseline | `docs/risks/risk-model-baseline.md` | Jira/PR evidence links, Confluence summary | Defines how risks are modeled, scored, linked, and reviewed. |
| Risk records | `docs/risks/records/` | Jira/PR evidence links, Confluence summary | Store concrete analyzed risks. They may propose treatment but do not accept, defer, or reject residual risk without Project Owner decision. |
| Shift Left governance baseline | `docs/governance/shift-left-governance-baseline.md` | Jira/PR evidence links | Defines the mandatory issue-level impact block and lightweight Shift Left review baseline. |
| Scrum governance, DoR and DoD | `docs/governance/scrum-governance-dor-dod.md` | Jira/PR evidence links | Defines lightweight Scrum governance, Definition of Ready, Definition of Done, Jira workflow movement, minimum evidence expectations, and Project Owner authority. |
| Governance Lane Review Gate | `docs/governance/governance-lane-review-gate.md` | Jira/PR evidence links | Defines when governance-lane tasks may advance toward review, stakeholder review, or Done. |
| Team Working Rules | `docs/governance/team-working-rules.md` | Jira/PR evidence links | Defines lightweight daily collaboration rules, evidence discipline, blocker handling, and advisory AI assistant usage boundaries. |
| Engineering Assistant Rules | `docs/governance/engineering-assistant-rules.md` | Jira/PR evidence links | Defines engineering assistant allowed actions, forbidden actions, operating flow, evidence expectations, and Project Owner authority boundaries. |
| AI review agents policy | `docs/governance/ai-review-agents-policy.md` | Jira/PR evidence links | Defines advisory review agents, severity model, outputs, and decision limits. |
| AI review agent playbook | `docs/governance/ai-review-agent-playbook.md` | Jira/PR evidence links | Defines reusable review-agent prompts and operating flow. |
| ADR index and template | `docs/adr/README.md`, `docs/adr/template.md` | Jira evidence link | Defines ADR index, naming convention, status model, template, and link policy. |
| Stakeholder transparency | `docs/governance/stakeholder-transparency.md` | Confluence summary/link | Defines stakeholder visibility and Atlassian governance behavior. |
| Stakeholder report data rules | `docs/governance/stakeholder-report-data-rules.md` | Confluence summary/link | Defines what stakeholder reports may show, link, redact, or block. |
| Product Vision | `docs/product/product-vision.md` | Jira/Confluence links | Product Vision, MVP boundaries, and current glossary live in GitHub until superseded by reviewed change. |
| Glossary | Current embedded glossary in `docs/product/product-vision.md` | Future `docs/glossary/project-glossary.md` candidate | Do not create a duplicate glossary until a later task explicitly extracts and links it. |
| ADR | GitHub `docs/adr/` | Jira evidence link | ADRs are versioned source-of-truth decisions. Jira may link them but must not replace them. |
| Risk Assessment | GitHub `docs/risks/` when introduced; template in `docs/templates/risk-assessment.md` | Jira evidence link, Confluence summary | Risk records are versioned in GitHub when introduced. Stakeholder summaries may link to them. |
| Stakeholder hub | Confluence | README/GitHub links back to hub | Confluence is authoritative for stakeholder navigation and landing-page experience. |
| Stakeholder reports | Confluence | Jira links/evidence, GitHub links to canonical docs | Stakeholder reports live on Confluence because pages/forms are better suited there. Reports must not override GitHub technical truth. |
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
- closes a task without the expected review/evidence trail;
- lets engineering assistants or review agents approve ADRs, close issues, declare Done, or transition Jira without explicit Project Owner instruction.

### 5.1 Examples

Regression:

```text
The MVP includes window sensors.
```

Correction:

```text
Window sensors are outside MVP unless changed by ADR.
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
| S0 — Blocking | Contradicts protected MVP, safety/security posture, approval authority, or source-of-truth hierarchy | Direct ESP32 Kafka in MVP; production-ready claim; 220V automation in MVP; AI agent declares Done | Block merge/review until fixed |
| S1 — High | Creates divergence between GitHub, Jira, and Confluence | Confluence duplicates technical docs and changes MVP wording | Block merge/review unless corrected or explicitly approved |
| S2 — Medium | Ambiguous maturity or missing `[UNVALIDATED]` marker | Target service described as implemented | Fix before approval |
| S3 — Low | Navigation, typo, broken link, unclear phrasing | Wrong path spelling; weak link label | Fix before or during review depending on impact |

### 5.3 Reporting format

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

A PR or review should not be approved while it contains unresolved S2 issues involving `[UNVALIDATED]`, MVP scope, target/runtime confusion, source-of-truth ambiguity, evidence, or approval authority.

### 5.5 Resolution flow

1. Identify the canonical source.
2. Correct the divergent document, ticket, page, comment, or PR.
3. Add or preserve `[UNVALIDATED]` when evidence is missing.
4. Update only links/summaries on Jira or Confluence when the GitHub source remains correct.
5. Update GitHub source of truth only through a reviewed repository change.
6. Link the fix as evidence.
7. Request review again.
8. Do not close the task without Project Owner approval.

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
- documentation strategy;
- documentation landing page;
- reusable project template inventory or canonical template paths;
- stakeholder report data rules;
- risk model baseline;
- risk records;
- risk assessments;
- `[UNVALIDATED]` policy;
- ADRs;
- canonical paths;
- Scrum governance, DoR and DoD;
- governance lane review gate;
- team working rules;
- engineering assistant rules;
- commit convention;
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

`[UNVALIDATED]` marks any claim that is not yet proven by implementation, tests, logs, reviewed PRs, runtime evidence, approved ADRs, Project Owner approval, or approved source-of-truth documentation.

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
- Project Owner approval recorded;
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
docs/README.md
```

```text
docs/product/product-vision.md
```

```text
docs/governance/stakeholder-transparency.md
docs/governance/stakeholder-report-data-rules.md
```

```text
docs/governance/source-of-truth.md
```

```text
docs/governance/documentation-strategy.md
```

```text
docs/templates/README.md
docs/templates/risk-assessment.md
```

```text
docs/risks/README.md
docs/risks/risk-model-baseline.md
docs/risks/records/
```

```text
docs/governance/shift-left-governance-baseline.md
```

```text
docs/governance/scrum-governance-dor-dod.md
```

```text
docs/governance/ai-review-agents-policy.md
```

```text
docs/governance/ai-review-agent-playbook.md
```

```text
docs/governance/governance-lane-review-gate.md
```

```text
docs/governance/team-working-rules.md
```

```text
docs/governance/engineering-assistant-rules.md
```

```text
docs/adr/README.md
docs/adr/template.md
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
docs/reviews/
docs/evidence/
docs/glossary/project-glossary.md
```

`docs/README.md` is the current documentation landing page. It is canonical only as a navigational index for `docs/`; it must not redefine source-of-truth policy, Documentation Strategy, Product Vision, ADR policy, template policy, risk model, or stakeholder reporting rules.

`docs/glossary/project-glossary.md` is a future candidate. It must not be created as a duplicate while the glossary remains embedded in the Product Vision or other existing governance sections.

`docs/risks/` is now a canonical risk documentation area. `docs/risks/risk-model-baseline.md` defines the risk modeling guide. `docs/risks/records/` stores concrete analyzed risk records. `docs/templates/risk-assessment.md` remains only a reusable template and does not accept any risk by itself.

---

## 9. AI Agent Semantic Routing

AI agents should use this routing order:

1. Start from `README.md` for the repository semantic map.
2. Read `docs/README.md` for documentation navigation under `docs/`.
3. Read `docs/governance/source-of-truth.md` for source-of-truth, anti-regression, canonical-path, and commit-convention rules.
4. Read `docs/governance/documentation-strategy.md` before creating, moving, splitting, merging, deprecating, or reorganizing repository documentation.
5. Read `docs/templates/README.md` before creating, using, moving, or changing reusable project templates.
6. Read `docs/risks/risk-model-baseline.md` before changing project risk taxonomy, scoring, residual risk treatment, risk evidence, or stakeholder risk visibility.
7. Read `docs/risks/README.md` and `docs/risks/records/` before changing concrete risk records.
8. Read `docs/governance/shift-left-governance-baseline.md` for the mandatory issue-level Shift Left impact block.
9. Read `docs/governance/scrum-governance-dor-dod.md` before evaluating Definition of Ready, Definition of Done, Jira workflow movement, or minimum evidence expectations.
10. Read `docs/governance/ai-review-agents-policy.md` for advisory review-agent roles, severity model, and decision limits.
11. Read `docs/governance/ai-review-agent-playbook.md` for concrete review-agent prompts and review-output format.
12. Read `docs/governance/governance-lane-review-gate.md` before evaluating governance-lane movement toward Review, Stakeholder Review, or Done.
13. Read `docs/governance/team-working-rules.md` before changing daily collaboration rules, blocker handling, evidence discipline, working agreements, or AI assistant usage boundaries.
14. Read `docs/governance/engineering-assistant-rules.md` before using or changing engineering assistant operating boundaries, allowed actions, forbidden actions, or assistant evidence rules.
15. Read `docs/adr/README.md` before adding or changing ADRs, ADR naming, ADR status, or ADR link policy.
16. Read `docs/adr/template.md` before drafting a new ADR.
17. Read `docs/product/product-vision.md` for Product Vision, MVP boundaries, and current glossary.
18. Read `docs/governance/stakeholder-transparency.md` for stakeholder visibility and Atlassian governance rules.
19. Read `docs/governance/stakeholder-report-data-rules.md` before changing what stakeholder reports may show, link, redact, or block.
20. Use Jira for task state, workflow, review state, blockers, and evidence links.
21. Use Confluence for stakeholder hub, stakeholder reports, stakeholder forms, and navigation.

AI agents must not infer implementation maturity from directory names alone. Empty or placeholder paths are not runtime proof.

---

## 10. Commit Convention

Jira-linked commits should start with the Jira issue key.

Format:

```text
IHAP-XX: Commit message
```

Examples:

```text
IHAP-14: Add Shift Left governance baseline
IHAP-14: Register Shift Left canonical path
IHAP-35: Register governance gate canonical path
```

Do not place the Jira issue key at the end of the commit message.

This is a repository governance convention. It must not be duplicated inside individual task-level governance documents unless a later reviewed source-of-truth change says otherwise.

---

## 11. Acceptance Criteria

This policy satisfies IHAP-13 and remains aligned with IHAP-16, IHAP-22, IHAP-23, IHAP-24, IHAP-25, IHAP-29, IHAP-30, IHAP-31, IHAP-33, and IHAP-35 when:

- source-of-truth responsibility is defined for backlog, task state, code, documents, Docs Landing Page, Product Vision, ADRs, Risk Model Baseline, Risk Records, Risk Assessments, Templates, stakeholder hub, stakeholder reports, stakeholder report data rules, PR evidence, runtime evidence, Documentation Strategy, Scrum Governance DoR/DoD, Governance Lane Review Gate, Team Working Rules, Engineering Assistant Rules, ADR index/template, and `[UNVALIDATED]` claims;
- DOC-REGRESSION is defined with examples and severity levels;
- reporting, blocking, and resolution flow are defined;
- GitHub/Jira/Confluence anti-divergence rules are explicit;
- `[UNVALIDATED]` usage and removal rules are documented;
- canonical repository paths are listed, including `docs/README.md`, `docs/governance/documentation-strategy.md`, `docs/templates/README.md`, `docs/templates/risk-assessment.md`, `docs/risks/README.md`, `docs/risks/risk-model-baseline.md`, `docs/risks/records/`, `docs/governance/scrum-governance-dor-dod.md`, `docs/governance/governance-lane-review-gate.md`, `docs/governance/team-working-rules.md`, `docs/governance/engineering-assistant-rules.md`, `docs/governance/stakeholder-report-data-rules.md`, `docs/adr/README.md`, and `docs/adr/template.md`;
- stakeholder reports are explicitly assigned to Confluence;
- no firmware, backend, mobile, runtime, production-ready, security-grade, commercial-ready, or safety-critical claim is introduced;
- Project Owner approval remains required before task completion.

---

## 12. Practical Rule

```text
Confluence reports and orients.
Jira tracks and links evidence.
GitHub defines the technical truth.
```

If they disagree on technical content, GitHub wins until a reviewed GitHub source-of-truth change says otherwise.
