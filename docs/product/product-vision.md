# Product Vision, MVP Boundaries and Glossary

**Issue:** IHAP-11 — S0-002 — Product Vision, MVP Boundaries and Glossary  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Document type:** Product foundation / governance documentation  
**Status:** Sprint 0 draft for review  
**Source of truth:** This versioned GitHub document is the technical source of truth for the Product Vision, MVP boundaries, and initial glossary until superseded by a later reviewed change.

<!--
AI_AGENT_METADATA:
  issue: IHAP-11
  document_type: product_foundation
  source_of_truth: github_versioned_documentation
  task_scope: documentation_governance_only
  runtime_changes_allowed: false
  firmware_changes_allowed: false
  backend_changes_allowed: false
  mobile_changes_allowed: false
  production_ready_claims_allowed: false
  unvalidated_claim_marker: "[UNVALIDATED]"
  mvp_firmware_node: "firmware/room-env-node/"
  mvp_node_semantics: "generic_room_door_node"
  mvp_physical_positioning: "near_room_door"
  mvp_includes:
    - temperature_collection
    - humidity_collection
    - local_presence_detection
    - door_open_closed_state
    - http_json_event_direction
    - minimal_event_schema_direction
    - documentation_governance
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
  service_boundaries_target_only:
    - services/ingestion/
    - services/device-registry/
    - services/read-model/
    - services/ai-insight/
  review_policy:
    - do_not_close_jira_without_project_owner_approval
    - keep_mvp_future_out_of_mvp_target_distinction
    - do_not_overstate_runtime_maturity
-->

---

## 1. Product Snapshot

HomeEdge AI Platform is an educational, portfolio-grade smart home platform built around a first edge node, backend service boundaries, mobile monitoring, and source-of-truth documentation.

The first MVP node is a **generic room/door node** positioned near the room door.

The MVP focuses on a small, reviewable smart home vertical slice:

- room temperature;
- room humidity;
- local non-identifying presence detection;
- room door open/closed state;
- HTTP/JSON event direction toward ingestion;
- documented backend service boundaries;
- governance through GitHub and Jira.

The MVP does **not** include person tracking, behavioral history, raw audio collection, certified access control, alarm-grade intrusion detection, 220V automation, or direct Kafka production from ESP32.

---

## 2. Document Control

This document defines the initial product framing for HomeEdge AI Platform.

It is intentionally limited to product documentation and governance. It does **not** introduce firmware, backend, mobile, infrastructure, CI/CD, cloud, Kafka, AI runtime, or production implementation.

### 2.1 Scope of this document

Included:

- Product Vision.
- MVP boundaries.
- FUTURE scope.
- OUT OF MVP scope.
- Initial glossary.
- Anti-regression rules for Sprint 0.
- Evidence expectations.

Excluded:

- Runtime implementation.
- Firmware implementation changes.
- Backend service implementation.
- Mobile app implementation.
- Production-readiness claims.
- Safety-critical claims.
- Commercial claims.

### 2.2 Claim policy

Any capability that is not implemented, tested, and supported by runtime evidence must be marked as `[UNVALIDATED]`.

A statement may describe a **TARGET** architecture only when it is explicitly framed as target, planned, or future work.

---

## 3. Product Vision

### 3.1 What HomeEdge AI Platform is

HomeEdge AI Platform is an educational, portfolio-grade smart home platform that connects edge devices, backend services, mobile monitoring, structured documentation, and an AI-ready insight layer.

The platform is designed around an edge-first architecture:

```text
Edge Nodes -> Backend Services -> Mobile Dashboard -> AI-ready Insights
```

At Sprint 0, this is a product and architecture direction, not proof that all runtime components already exist.

### 3.2 Why it exists

HomeEdge exists to create a coherent end-to-end engineering project suitable for the ITS context and for a technical portfolio.

The project connects multiple disciplines in one traceable system:

- embedded firmware on ESP32-class devices;
- sensor-based smart home telemetry;
- HTTP/JSON event ingestion;
- backend service boundaries;
- mobile-first monitoring;
- documentation as source of truth;
- governance through Jira, GitHub, and review evidence;
- AI-ready data interpretation as a later architectural target.

### 3.3 Problem it solves

HomeEdge addresses the problem of building a smart home system in a controlled, incremental, and reviewable way.

Instead of starting from a broad and ambiguous smart home vision, the project narrows the first vertical slice to a single generic room/door node and a minimal telemetry flow.

The project solves these early engineering problems:

- making hardware, firmware, backend, mobile, and documentation boundaries explicit;
- preventing uncontrolled scope expansion;
- avoiding unverified production-ready claims;
- keeping stakeholder visibility high;
- documenting what is implemented, what is targeted, and what is explicitly out of scope;
- creating a project structure that can scale without hiding current maturity.

### 3.4 Educational and portfolio value

HomeEdge is valuable as a learning and portfolio project because it demonstrates how to model a real platform from the beginning, not only how to write isolated code.

It shows:

- product thinking;
- architectural decomposition;
- embedded-to-cloud reasoning;
- source-of-truth documentation;
- issue-driven delivery;
- pull-request evidence;
- anti-regression governance;
- explicit MVP scoping;
- clear distinction between implemented features and target architecture.

This makes the project readable for ITS stakeholders, reviewers, recruiters, and future collaborators.

### 3.5 Technical value

HomeEdge is technically valuable because it is structured as a scalable platform rather than a single prototype script.

The main technical axes are:

- **Edge devices:** ESP32-class nodes collecting room-level signals.
- **Backend services:** target service boundaries for ingestion, device registry, read model, and AI insight.
- **Mobile monitoring:** mobile-first dashboard direction for telemetry and device health visibility.
- **AI-ready insight layer:** future service boundary for deriving insights from validated data.
- **Governance:** Jira for workflow and evidence, GitHub for versioned technical source of truth, and PR reviews for change validation.

At Sprint 0, these axes define direction and boundaries. They do not imply that every component is implemented.

---

## 4. MVP Boundaries

### 4.1 MVP definition

The MVP is the smallest reviewable vertical slice of HomeEdge.

It must prove the platform direction without expanding into high-risk or unvalidated smart home automation features.

The MVP is centered on one firmware node:

```text
firmware/room-env-node/
```

This node is the first generic room/door node of the smart home platform. It is assumed to be positioned near the room door and is responsible for collecting minimal room-level signals.

In the MVP, the node may collect:

- temperature;
- humidity;
- local non-identifying presence state;
- door open/closed state.

No other firmware node is part of the MVP unless a later ADR explicitly changes this boundary.

### 4.2 MVP included

The MVP includes the following scope:

| Area | MVP scope | Status framing |
|---|---|---|
| Firmware node | One generic Room/Door Environment Node under `firmware/room-env-node/` | MVP |
| Physical placement | Node positioned near the room door | MVP assumption |
| Environment telemetry | Temperature and humidity collection | MVP |
| Local presence | Local presence detection as a boolean or state signal, without identity, behavioral history, or individual tracking | MVP |
| Door state | Door open/closed state detection | MVP |
| Transport | HTTP/JSON event sent toward ingestion backend | MVP target until implemented and verified |
| Event model | Minimal event schema for room environment, presence state, and door state | MVP target until implemented and verified |
| Backend | Ingestion boundary as target service area | TARGET |
| Device registry | Device identity/metadata boundary as target service area | TARGET |
| Read model | Query/read-oriented boundary as target service area | TARGET |
| AI insight | AI-ready insight boundary as target service area | TARGET / FUTURE |
| Mobile dashboard | Mobile monitoring documented as target | TARGET |
| Documentation | GitHub versioned documentation as source of truth | MVP governance |
| Jira governance | Jira comments/status/evidence for task tracking | MVP governance |

Presence detection in the MVP means detecting whether presence is currently observed in a room-level context.

Presence detection does **not** mean tracking people, identifying people, storing behavioral history, profiling routines, or producing safety-critical occupancy guarantees.

Door state detection in the MVP means detecting whether the room door is open or closed.

Door state detection does **not** mean access control, intrusion certification, alarm-grade security, or safety-critical monitoring.

### 4.3 Minimal event direction

The MVP event direction is HTTP/JSON from `room-env-node` toward an ingestion backend.

A minimal room environment event may include fields such as:

```json
{
  "event_type": "room.environment.sampled",
  "device_id": "room-env-01",
  "timestamp": "2026-07-07T00:00:00Z",
  "temperature_c": 24.5,
  "humidity_percent": 55.0,
  "presence_detected": false,
  "door_open": false,
  "firmware_version": "0.0.0-unvalidated"
}
```

This schema is directional and must remain `[UNVALIDATED]` until the schema is formally versioned, implemented, and tested.

The `presence_detected` field represents a local, non-identifying room-level state. It must not be interpreted as identity, person tracking, behavioral profiling, or safety-critical occupancy evidence.

The `door_open` field represents the local open/closed state of the room door. It must not be interpreted as certified access control, intrusion detection, or safety-critical security evidence.

### 4.4 MVP acceptance boundary

The MVP must remain understandable without requiring any of the following:

- multiple hardware node types;
- raw audio collection;
- individual presence tracking;
- behavioral presence history;
- person identification;
- window detection;
- certified access control;
- alarm-grade intrusion detection;
- 220V automation;
- direct Kafka production from ESP32;
- cloud deployment;
- production-grade security certification;
- commercial or safety-critical positioning.

---

## 5. FUTURE Scope

The following items are intentionally future scope. They may be explored later only through explicit tasks, ADRs, risk assessments, and review evidence.

| Area | FUTURE item | Notes |
|---|---|---|
| Presence | Advanced presence radar features | Basic local presence detection is MVP; identity, tracking, behavioral history, room-to-room movement analysis, and advanced presence analytics are not MVP. |
| Openings | Window sensors and multi-opening topology | Door open/closed state for the first room/door node is MVP; window sensors and multi-opening modeling are FUTURE. |
| Audio-derived signals | Noise detection derived from local processing | Raw audio collection remains OUT OF MVP. |
| Automation | Smart home automations | Requires safety and risk review. |
| AI | Advanced AI insight generation | Requires validated data and clear privacy boundaries. |
| Event streaming | Kafka on backend/event streaming side | Backend-side target only, not ESP32 direct producer in MVP. |
| DevOps | More complete CI/CD | Future hardening task. |
| Deployment | Cloud deployment | Future deployment milestone. |
| Mobile | Full mobile dashboard implementation | Target beyond initial documentation unless separately implemented. |

FUTURE means planned or possible later work. It does not mean implemented.

---

## 6. OUT OF MVP Scope

The following items are explicitly out of the MVP and must not be implied as delivered by Sprint 0 documentation.

| Item | Reason |
|---|---|
| Raw audio collection | Privacy risk and not needed for the first telemetry vertical slice. |
| Individual presence tracking | OUT OF MVP. The MVP may detect local presence state, but must not identify people, track individuals, store behavioral history, or profile routines. |
| Behavioral presence history | OUT OF MVP. Presence events must not become a person-level movement log or routine inference system in the MVP. |
| Window sensors in MVP | OUT OF MVP. The first MVP node may detect the room door open/closed state, but window sensors are future scope. |
| Certified access control | OUT OF MVP. Door open/closed state is telemetry only, not an access-control or alarm-grade security feature. |
| Alarm-grade intrusion detection | OUT OF MVP. Door state and presence state must not be presented as certified intrusion detection. |
| 220V automation | Safety risk and requires dedicated electrical/security review. |
| Production-grade security/certification | Not implemented or verified in Sprint 0. |
| Kafka client directly on ESP32 | Too heavy and outside the MVP boundary; backend event streaming may be future scope. |
| Commercial claims | Project is educational/portfolio-oriented unless later validated otherwise. |
| Safety-critical claims | No safety-critical guarantees are provided. |
| Full AI automation | AI insight is a target boundary, not a validated runtime capability in Sprint 0. |

---

## 7. Target Service Boundaries

The repository skeleton defines four backend service boundaries:

```text
services/ingestion/
services/device-registry/
services/read-model/
services/ai-insight/
```

These are **target service boundaries**.

They do not prove that production-ready services exist. They define where backend responsibilities should be modeled as the platform evolves.

### 7.1 Ingestion boundary

The ingestion boundary is responsible for receiving, validating, and accepting telemetry events from edge nodes.

At Sprint 0, this is a target boundary unless implementation evidence exists in a later task.

### 7.2 Device Registry boundary

The device registry boundary is responsible for device identity, metadata, and lifecycle state.

At Sprint 0, this is a target boundary unless implementation evidence exists in a later task.

### 7.3 Read Model boundary

The read model boundary is responsible for query-oriented representations of data used by dashboards, APIs, or monitoring views.

At Sprint 0, this is a target boundary unless implementation evidence exists in a later task.

### 7.4 AI Insight boundary

The AI insight boundary is responsible for future interpretation, classification, summarization, anomaly detection, or insight generation from validated data.

At Sprint 0, this is a target/future boundary, not a validated AI runtime.

---

## 8. Glossary

| Term | Definition |
|---|---|
| Edge Node | A physical embedded device near the environment being observed. In this project, edge nodes are expected to use ESP32-class hardware unless changed by ADR. |
| Generic Room/Door Node | The first MVP smart home node placed near a room door. It collects minimal room environment data, local presence state, and door open/closed state. |
| Room Environment Node | The MVP firmware node located at `firmware/room-env-node/`. In the MVP, it acts as a generic room/door node responsible for temperature, humidity, local presence detection, and door open/closed state. |
| Event | A structured record describing something observed or produced by the system, such as a room environment sample. |
| Door State | A local telemetry signal indicating whether the room door is open or closed. It is allowed in the MVP as a non-certified state signal. |
| Presence Detection | A local, non-identifying room-level signal indicating whether presence is currently detected. It is allowed in the MVP only as a minimal state signal. |
| Presence Tracking | Person-level, historical, behavioral, or identity-linked tracking of presence over time. This is OUT OF MVP. |
| Ingestion | The backend boundary responsible for receiving and validating incoming events. |
| Device Registry | The backend boundary responsible for device identity, metadata, ownership, lifecycle, and known-device state. |
| Read Model | A query-optimized representation of data used by dashboards, APIs, or monitoring views. |
| AI Insight | A future or target capability that derives higher-level interpretation from validated data. It is not a Sprint 0 runtime claim. |
| Source of Truth | The authoritative place where a technical decision, boundary, or project fact is maintained. For versioned technical documentation, this is GitHub unless explicitly superseded. |
| ADR | Architecture Decision Record. A reviewed document that captures an architectural decision, context, consequences, and alternatives. |
| MVP | Minimum Viable Product. The smallest coherent and reviewable vertical slice of the platform. |
| FUTURE | A planned or possible later capability. It is not implemented unless separate evidence proves it. |
| OUT OF MVP | Explicitly excluded from the current MVP scope. These items must not be implied as delivered. |
| TARGET | A documented architectural direction or service boundary. It is not proof of implementation. |
| `[UNVALIDATED]` | Marker for a claim, capability, schema, flow, or assumption that has not yet been implemented, tested, and supported by runtime evidence. |
| Stakeholder Report | A concise status report for stakeholders, such as ITS professors, that communicates progress, risks, evidence, and next steps without leaking sensitive data or making unsupported claims. |
| Runtime Evidence | Concrete evidence from running software or hardware, such as logs, tests, screenshots, traces, build outputs, or verified API responses. |

---

## 9. Anti-regression Rules

These rules protect the Sprint 0 baseline and IHAP-10 repository skeleton.

1. This document must not contradict the repository skeleton introduced by IHAP-10.
2. The only firmware node in the MVP is `firmware/room-env-node/`.
3. `firmware/room-env-node/` represents the first generic room/door node positioned near the room door.
4. The MVP includes temperature, humidity, local non-identifying presence detection, and door open/closed state.
5. The four backend directories remain target service boundaries, not proof of completed production services.
6. Kafka direct production from ESP32 remains OUT OF MVP.
7. Backend-side Kafka/event streaming remains FUTURE unless a later ADR and implementation task validate it.
8. Raw audio collection remains OUT OF MVP.
9. Local, non-identifying presence detection is allowed inside the MVP.
10. Individual presence tracking, behavioral history, identity inference, and routine profiling remain OUT OF MVP.
11. Door open/closed state is allowed inside the MVP as telemetry only.
12. Door state must not be presented as certified access control, alarm-grade intrusion detection, or safety-critical security evidence.
13. Window sensors remain FUTURE and OUT OF MVP unless changed by ADR.
14. 220V automation remains OUT OF MVP.
15. Mobile monitoring is a target direction unless supported by implementation evidence.
16. AI insight is a target/future service boundary unless supported by implementation evidence.
17. Stakeholder reports must not contain sensitive data, raw personal telemetry, raw audio, behavioral tracking, or unsupported production/safety/commercial claims.
18. Any unproven claim must be marked as `[UNVALIDATED]`.
19. Documentation must distinguish clearly between MVP, FUTURE, OUT OF MVP, and TARGET.
20. Jira must track status, evidence, decisions, and review state.
21. GitHub must remain the source of truth for versioned technical documentation.

---

## 10. Evidence Expectations

For IHAP-11, expected evidence is:

- A GitHub branch dedicated to the task.
- A draft pull request linked to IHAP-11.
- This versioned document under `docs/product/product-vision.md`.
- A Jira comment linking the PR and summarizing the documentation scope.
- Jira status moved to review after PR creation.
- No transition to completed until explicit project owner approval.

---

## 11. Review Checklist

Before this document can be considered accepted, reviewers should verify:

- Product Vision is understandable by ITS stakeholders.
- MVP scope is explicit and narrow.
- FUTURE and OUT OF MVP are separated.
- Runtime claims are not overstated.
- `[UNVALIDATED]` is used for directional schema or unproven capabilities.
- `firmware/room-env-node/` remains the only MVP firmware node.
- The MVP node is correctly framed as a generic room/door node positioned near the room door.
- Temperature, humidity, local non-identifying presence detection, and door open/closed state are included in MVP.
- Raw audio, individual presence tracking, behavioral presence history, window sensors, 220V automation, and Kafka client on ESP32 are not included in MVP.
- Local, non-identifying presence detection is correctly separated from presence tracking.
- Door open/closed state is correctly separated from certified access control or alarm-grade intrusion detection.
- The four backend service boundaries are described as targets, not completed runtime services.
- The document does not regress IHAP-10.
