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
  related_issues:
    - IHAP-18
  document_type: stakeholder_transparency_governance
  source_of_truth: github_versioned_repository_documentation
  task_scope: documentation_governance_only
  runtime_changes_allowed: false
  firmware_changes_allowed: false
  backend_changes_allowed: false
  mobile_changes_allowed: false
  production_ready_claims_allowed: false
  commercial_ready_claims_allowed: false
  safety_critical_claims_allowed: false
  alarm_grade_claims_allowed: false
  security_grade_claims_allowed: false
  certification_claims_allowed: false
  antifurto_claims_allowed: false
  protection_claims_allowed: false
  ai_runtime_validation_claims_allowed_without_evidence: false
  unvalidated_claim_marker: "[UNVALIDATED]"
  human_readability_requirement: "max_3_minutes"
  confluence_landing_page: "https://niccolopiazzi01.atlassian.net/wiki/spaces/IEHAP/overview"
  stakeholder_report_data_rules: "docs/governance/stakeholder-report-data-rules.md"
  confluence_authoritative_for:
    - stakeholder_hub
    - stakeholder_reports
    - stakeholder_forms
    - stakeholder_navigation
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
    - stakeholder_reports
    - stakeholder_forms
    - summary_navigation_layer
    - not_technical_source_of_truth
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
    - alarm_grade_claims
    - antifurto_claims
    - certified_access_control_claims
    - certified_intrusion_detection_claims
  target_service_boundaries:
    - services/ingestion/
    - services/device-registry/
    - services/read-model/
    - services/ai-insight/

HIDDEN_ANTI_REGRESSION_RULES:
  - The repository remains the source of truth for technical documentation, decisions, risks, policies, and technical baselines.
  - Jira must not duplicate source-of-truth documents; it must expose state, evidence links, review status, blockers, and stakeholder navigation.
  - Confluence is the stakeholder landing page, stakeholder report surface, stakeholder form surface, and navigation layer; it must not replace or duplicate repository technical source of truth.
  - Stakeholder reports live on Confluence because that surface is better suited for human reports and forms.
  - Stakeholder reports must summarize and link; they must not redefine technical truth.
  - Use docs/governance/stakeholder-report-data-rules.md for what stakeholder reports may show, link, redact, or block.
  - The only firmware node in the MVP remains firmware/room-env-node/.
  - firmware/room-env-node/ remains a generic room/door node.
  - The MVP includes temperature, humidity, local non-identifying presence detection, and door open/closed state.
  - Raw audio, person tracking, behavioral history, identity inference, window scope, 220V automation, and direct ESP32 Kafka publishing remain out of MVP.
  - The four service directories remain TARGET boundaries unless validated by later implementation evidence.
  - Stakeholder-facing pages and reports must not weaken, expand, or silently reinterpret MVP boundaries.
  - Any unproven claim must be marked as [UNVALIDATED].
  - Door state and presence state must not be presented as antifurto, alarm-grade, certified access control, certified intrusion detection, safety-critical monitoring, or protection of people, goods, or environments.
  - AI insight must not be presented as runtime validated without traceable runtime evidence.
-->

---

## 1. Decision

HomeEdge AI Platform uses three surfaces with different roles:

| Surface | Role | What it is for |
|---|---|---|
| **GitHub repository** | Technical source of truth | Official technical documents, decisions, risks, policies, technical baselines, PR evidence |
| **Jira** | Tracking and review | Task state, sprint visibility, blockers, evidence links, project-owner review |
| **Confluence** | Stakeholder hub and reports | Fast human overview, stakeholder-facing reports, forms, and links to Jira/GitHub |

Confluence helps a professor understand where to look and provides a convenient place for stakeholder reports and forms. It does not replace the repository technical source of truth.

---

## 2. Stakeholder reading path

A professor or reviewer should be able to follow the project like this:

```text
Confluence Stakeholder Hub / Report
  -> Jira board / Jira issue
  -> PR evidence
  -> repository source-of-truth document
```

The Confluence hub gives the first overview and hosts stakeholder reports/forms. Jira shows status and evidence. GitHub contains the durable technical truth.

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

The page or report must be short. If a stakeholder needs depth, they should follow links to Jira or GitHub.

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

If sensitive information is useful for debugging, it must be redacted before being shared in Jira, Confluence, screenshots, public repository documentation, stakeholder reports, or stakeholder forms.

---

## 6. Claim rule

Unclear maturity must be marked down, not up. Stakeholder wording must use the weakest accurate claim.

Use these labels consistently:

| Label | Meaning |
|---|---|
| `DONE` | Completed and supported by evidence |
| `PLANNED` | Intended but not implemented |
| `TARGET` | Architectural direction or boundary, not proof of runtime |
| `FUTURE` | Possible later scope, not implemented now |
| `IN REVIEW` | Produced, waiting for review |
| `STAKEHOLDER REVIEW` | Ready for stakeholder visibility, not Done |
| `RISK` | Known uncertainty or possible negative outcome |
| `DECISION` | Approved direction or constraint |
| `[UNVALIDATED]` | Not implemented, tested, reviewed, or proven |
| `OUT OF SCOPE` | Explicitly excluded |

Claim classes:

| Class | Allowed wording | Rule |
|---|---|---|
| Allowed | Educational, portfolio-grade, Sprint 0, MVP, target, planned, future, in review, stakeholder review | Use only when it matches linked evidence or source-of-truth scope. |
| Allowed only with `[UNVALIDATED]` | Backend service boundaries, mobile dashboard, cloud/deployment, event schema, storage behavior, ingestion, device registry, read model, AI insight | Preserve `[UNVALIDATED]` until implementation and runtime evidence exist. |
| Blocked | Production-ready, commercial-ready, security-certified, security-grade, safety-critical, alarm-grade, antifurto, certified access control, certified intrusion detection, protection of people, goods, or environments | Do not use in current stakeholder material. Future reconsideration requires reviewed source-of-truth change, implementation evidence, and Project Owner decision. |

Stakeholder-safe wording:

| Use | Avoid |
|---|---|
| `Door state telemetry is part of the MVP.` | `The system controls access or detects intrusions.` |
| `Presence is local, non-identifying room state.` | `The system tracks people or guarantees occupancy safety.` |
| `AI insight is a target/future boundary [UNVALIDATED].` | `AI insight is runtime validated.` |
| `Backend/mobile/cloud are target boundaries [UNVALIDATED].` | `Backend/mobile/cloud are already implemented production services.` |

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
- production/security-grade certification claims;
- antifurto, alarm-grade, certified access control, or certified intrusion detection claims.

Target service boundaries remain targets unless later implementation evidence proves otherwise:

```text
services/ingestion/
services/device-registry/
services/read-model/
services/ai-insight/
```

---

## 8. Stakeholder report rule

Stakeholder reports live on Confluence.

Reason:

- Confluence is easier for stakeholder-facing pages;
- Confluence supports forms and lightweight reporting workflows;
- professors/reviewers can navigate reports without reading repository internals first.

Constraint:

Stakeholder reports must not redefine Product Vision, MVP scope, ADRs, risk posture, technical baselines, or implementation maturity. They must summarize and link back to GitHub/Jira evidence.

For report data categories, claim handling, redaction, and blocked content, use `docs/governance/stakeholder-report-data-rules.md`.

---

## 9. Practical rule

The operating rule for IHAP stakeholder transparency is simple:

```text
Confluence reports and orients.
Jira tracks and links evidence.
GitHub defines the technical truth.
```

If they disagree on technical content, GitHub wins until the project owner approves a reviewed source-of-truth update.
