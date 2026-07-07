# Stakeholder Transparency and Atlassian Governance

**Issue:** IHAP-12 — S0-003 — Stakeholder Transparency and Atlassian Governance  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Document type:** Stakeholder transparency / governance documentation  
**Status:** Sprint 0 draft for review  
**Reading target:** less than 3 minutes for humans; hidden metadata supports AI agents and anti-regression checks.  
**Stakeholder Hub:** https://niccolopiazzi01.atlassian.net/wiki/spaces/IEHAP/overview  
**Source of truth:** This repository document defines the official stakeholder transparency rules until superseded by a reviewed change.

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
  human_readability_requirement: "max_3_minutes"
  confluence_landing_page: "https://niccolopiazzi01.atlassian.net/wiki/spaces/IEHAP/overview"
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
    - stakeholder_facing_landing_page
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
  - Confluence is a stakeholder landing page and navigation layer; it must not replace or duplicate the repository source of truth.
  - The only firmware node in the MVP remains firmware/room-env-node/.
  - firmware/room-env-node/ remains a generic room/door node.
  - The MVP includes temperature, humidity, local non-identifying presence detection, and door open/closed state.
  - Raw audio, person tracking, behavioral history, identity inference, window scope, 220V automation, and direct ESP32 Kafka publishing remain out of MVP.
  - The four service directories remain TARGET boundaries unless validated by later implementation evidence.
  - Stakeholder-facing pages must not weaken, expand, or silently reinterpret MVP boundaries.
  - Any unproven claim must be marked as [UNVALIDATED].
-->

---

## 1. Decision

HomeEdge AI Platform uses three surfaces with different roles:

| Surface | Role | What it is for |
|---|---|---|
| **GitHub repository** | Source of truth | Official documents, decisions, risks, policies, technical baselines, PR evidence |
| **Jira** | Tracking and review | Task state, sprint visibility, blockers, evidence links, project-owner review |
| **Confluence** | Stakeholder landing page | Fast human overview with links to Jira and GitHub |

Confluence helps a professor understand where to look. It does not replace the repository.

---

## 2. Stakeholder reading path

A professor or reviewer should be able to follow the project like this:

```text
Confluence Stakeholder Hub
  -> Jira board / Jira issue
  -> PR evidence
  -> repository source-of-truth document
```

The Confluence hub gives the first overview. Jira shows status and evidence. GitHub contains the durable truth.

Stakeholder hub:

```text
https://niccolopiazzi01.atlassian.net/wiki/spaces/IEHAP/overview
```

---

## 3. Minimum stakeholder view

A stakeholder must be able to see quickly:

- current project phase;
- active task/review state;
- completed work;
- work in review;
- blockers;
- open risks;
- key decisions;
- PR and document evidence;
- `[UNVALIDATED]` claims.

The page must be short. If a stakeholder needs depth, they should follow links to Jira or GitHub.

---

## 4. Evidence rule

Every relevant Jira task should link to the real evidence instead of copying it.

Minimum Jira evidence comment:

```text
Produced: what changed
Source of truth: repository file path
PR: GitHub pull request link
Validation: what was checked
Risks / [UNVALIDATED]: what is still not proven
Project owner action: review / approve / request changes
```

Jira is a navigation and review layer. It should not become a second documentation repository.

---

## 5. Redaction rule

Stakeholder-facing material must not expose:

- tokens, passwords, API keys;
- domestic IP addresses or private network details;
- private physical addresses;
- sensitive logs;
- personal data not needed for review;
- raw audio;
- private images/videos;
- person identification;
- individual tracking;
- behavioral history.

If sensitive information is useful for debugging, it must be redacted before being shared in Jira, Confluence, screenshots, or public repository documentation.

---

## 6. Claim rule

Unclear maturity must be marked down, not up.

Use these labels consistently:

| Label | Meaning |
|---|---|
| `DONE` | Completed and supported by evidence |
| `PLANNED` | Intended but not implemented |
| `IN REVIEW` | Produced, waiting for review |
| `STAKEHOLDER REVIEW` | Ready for stakeholder visibility |
| `RISK` | Known uncertainty or possible negative outcome |
| `DECISION` | Approved direction or constraint |
| `[UNVALIDATED]` | Not implemented, tested, reviewed, or proven |
| `OUT OF SCOPE` | Explicitly excluded |

Forbidden pattern:

```text
Production-ready / secure / safety-critical / commercially ready
```

Unless a later reviewed implementation and validation task proves it.

---

## 7. Protected MVP baseline

Stakeholder pages and reports must not change the MVP definition.

Inside MVP:

- temperature;
- humidity;
- local non-identifying presence;
- door open/closed state.

MVP firmware path:

```text
firmware/room-env-node/
```

The node is a generic room/door node.

Outside MVP:

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

Target service boundaries remain targets unless later implementation evidence proves otherwise:

```text
services/ingestion/
services/device-registry/
services/read-model/
services/ai-insight/
```

---

## 8. Practical rule

The operating rule for IHAP stakeholder transparency is simple:

```text
Confluence shows the map.
Jira shows the status.
GitHub contains the truth.
```

If they disagree, GitHub wins until the project owner approves a reviewed source-of-truth update.
