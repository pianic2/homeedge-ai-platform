# Product Vision, MVP Boundaries and Glossary

**Issue:** IHAP-11 — S0-002 — Product Vision, MVP Boundaries and Glossary  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Document type:** Product foundation / governance documentation  
**Status:** Sprint 0 draft for review  
**Source of truth:** This versioned GitHub document is the technical source of truth for the Product Vision, MVP boundaries, and initial glossary until superseded by a later reviewed change.

---

## 1. Document Control

This document defines the initial product framing for HomeEdge AI Platform.

It is intentionally limited to product documentation and governance. It does **not** introduce firmware, backend, mobile, infrastructure, CI/CD, cloud, Kafka, AI runtime, or production implementation.

### 1.1 Scope of this document

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

### 1.2 Claim policy

Any capability that is not implemented, tested, and supported by runtime evidence must be marked as `[UNVALIDATED]`.

A statement may describe a **TARGET** architecture only when it is explicitly framed as target, planned, or future work.

---

## 2. Product Vision

### 2.1 What HomeEdge AI Platform is

HomeEdge AI Platform is an educational, portfolio-grade smart home platform that connects edge devices, backend services, mobile monitoring, structured documentation, and an AI-ready insight layer.

The platform is designed around an edge-first architecture:

```text
Edge Nodes -> Backend Services -> Mobile Dashboard -> AI-ready Insights
```

At Sprint 0, this is a product and architecture direction, not proof that all runtime components already exist.

### 2.2 Why it exists

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

### 2.3 Problem it solves

HomeEdge addresses the problem of building a smart home system in a controlled, incremental, and reviewable way.

Instead of starting from a broad and ambiguous smart home vision, the project narrows the first vertical slice to a single room environment node and a minimal telemetry flow.

The project solves these early engineering problems:

- making hardware, firmware, backend, mobile, and documentation boundaries explicit;
- preventing uncontrolled scope expansion;
- avoiding unverified production-ready claims;
- keeping stakeholder visibility high;
- documenting what is implemented, what is targeted, and what is explicitly out of scope;
- creating a project structure that can scale without hiding current maturity.

### 2.4 Educational and portfolio value

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

### 2.5 Technical value

HomeEdge is technically valuable because it is structured as a scalable platform rather than a single prototype script.

The main technical axes are:

- **Edge devices:** ESP32-class nodes collecting room-level signals.
- **Backend services:** target service boundaries for ingestion, device registry, read model, and AI insight.
- **Mobile monitoring:** mobile-first dashboard direction for telemetry and device health visibility.
- **AI-ready insight layer:** future service boundary for deriving insights from validated data.
- **Governance:** Jira for workflow and evidence, GitHub for versioned technical source of truth, and PR reviews for change validation.

At Sprint 0, these axes define direction and boundaries. They do not imply that every component is implemented.

---

## 3. MVP Boundaries

### 3.1 MVP definition

The MVP is the smallest reviewable vertical slice of HomeEdge.

It must prove the platform direction without expanding into high-risk or unvalidated smart home automation features.

The MVP is centered on one firmware node:

```text
firmware/room-env-node/
```

No other firmware node is part of the MVP unless a later ADR explicitly changes this boundary.

### 3.2 MVP included

The MVP includes the following scope:

| Area | MVP scope | Status framing |
|---|---|---|
| Firmware node | One Room Environment Node under `firmware/room-env-node/` | MVP |
| Telemetry | Temperature and humidity collection | MVP |
| Transport | HTTP/JSON event sent toward ingestion backend | MVP target until implemented and verified |
| Event model | Minimal event schema for room environment telemetry | MVP target until implemented and verified |
| Backend | Ingestion boundary as target service area | TARGET |
| Device registry | Device identity/metadata boundary as target service area | TARGET |
| Read model | Query/read-oriented boundary as target service area | TARGET |
| AI insight | AI-ready insight boundary as target service area | TARGET / FUTURE |
| Mobile dashboard | Mobile monitoring documented as target | TARGET |
| Documentation | GitHub versioned documentation as source of truth | MVP governance |
| Jira governance | Jira comments/status/evidence for task tracking | MVP governance |

### 3.3 Minimal event direction

The MVP event direction is HTTP/JSON from `room-env-node` toward an ingestion backend.

A minimal room environment event may include fields such as:

```json
{
  "event_type": "room.environment.sampled",
  "device_id": "room-env-01",
  "timestamp": "2026-07-07T00:00:00Z",
  "temperature_c": 24.5,
  "humidity_percent": 55.0,
  "firmware_version": "0.0.0-unvalidated"
}
```

This schema is directional and must remain `[UNVALIDATED]` until the schema is formally versioned, implemented, and tested.

### 3.4 MVP acceptance boundary

The MVP must remain understandable without requiring any of the following:

- multiple hardware node types;
- raw audio collection;
- presence tracking;
- door/window detection;
- 220V automation;
- direct Kafka production from ESP32;
- cloud deployment;
- production-grade security certification;
- commercial or safety-critical positioning.

---

## 4. FUTURE Scope

The following items are intentionally future scope. They may be explored later only through explicit tasks, ADRs, risk assessments, and review evidence.

| Area | FUTURE item | Notes |
|---|---|---|
| Presence | Presence radar | Not part of MVP runtime scope. |
| Openings | Door/window sensors | Not part of MVP runtime scope. |
| Audio-derived signals | Noise detection derived from local processing | Raw audio collection remains OUT OF MVP. |
| Automation | Smart home automations | Requires safety and risk review. |
| AI | Advanced AI insight generation | Requires validated data and clear privacy boundaries. |
| Event streaming | Kafka on backend/event streaming side | Backend-side target only, not ESP32 direct producer in MVP. |
| DevOps | More complete CI/CD | Future hardening task. |
| Deployment | Cloud deployment | Future deployment milestone. |
| Mobile | Full mobile dashboard implementation | Target beyond initial documentation unless separately implemented. |

FUTURE means planned or possible later work. It does not mean implemented.

---

## 5. OUT OF MVP Scope

The following items are explicitly out of the MVP and must not be implied as delivered by Sprint 0 documentation.

| Item | Reason |
|---|---|
| Raw audio collection | Privacy risk and not needed for the first telemetry vertical slice. |
| Presence tracking in MVP | Privacy and behavior-tracking concerns; not required for temperature/humidity slice. |
| Door/window sensors in MVP | Scope expansion beyond the first Room Environment Node. |
| 220V automation | Safety risk and requires dedicated electrical/security review. |
| Production-grade security/certification | Not implemented or verified in Sprint 0. |
| Kafka client directly on ESP32 | Too heavy and outside the MVP boundary; backend event streaming may be future scope. |
| Commercial claims | Project is educational/portfolio-oriented unless later validated otherwise. |
| Safety-critical claims | No safety-critical guarantees are provided. |
| Full AI automation | AI insight is a target boundary, not a validated runtime capability in Sprint 0. |

---

## 6. Target Service Boundaries

The repository skeleton defines four backend service boundaries:

```text
services/ingestion/
services/device-registry/
services/read-model/
services/ai-insight/
```

These are **target service boundaries**.

They do not prove that production-ready services exist. They define where backend responsibilities should be modeled as the platform evolves.

### 6.1 Ingestion boundary

The ingestion boundary is responsible for receiving, validating, and accepting telemetry events from edge nodes.

At Sprint 0, this is a target boundary unless implementation evidence exists in a later task.

### 6.2 Device Registry boundary

The device registry boundary is responsible for device identity, metadata, and lifecycle state.

At Sprint 0, this is a target boundary unless implementation evidence exists in a later task.

### 6.3 Read Model boundary

The read model boundary is responsible for query-oriented representations of device state and telemetry.

At Sprint 0, this is a target boundary unless implementation evidence exists in a later task.

### 6.4 AI Insight boundary

The AI insight boundary is responsible for future interpretation, classification, summarization, anomaly detection, or insight generation from validated data.

At Sprint 0, this is a target/future boundary, not a validated AI runtime.

---

## 7. Glossary

| Term | Definition |
|---|---|
| Edge Node | A physical embedded device near the environment being observed. In this project, edge nodes are expected to use ESP32-class hardware unless changed by ADR. |
| Room Environment Node | The MVP firmware node located at `firmware/room-env-node/`. Its MVP responsibility is temperature/humidity telemetry. |
| Event | A structured record describing something observed or produced by the system, such as a room environment sample. |
| Ingestion | The backend boundary responsible for receiving and validating incoming events. |
| Device Registry | The backend boundary responsible for device identity, metadata, ownership, lifecycle, and known-device state. |
| Read Model | A query-optimized representation of data used by dashboards, APIs, or monitoring views. |
| AI Insight | A future or target capability that derives higher-level interpretation from validated data. It is not a Sprint 0 runtime claim. |
| Source of Truth | The authoritative place where a technical decision, boundary, or project fact is maintained. For versioned technical documentation, this is GitHub unless explicitly superseded. |
| ADR | Architecture Decision Record. A reviewed document that captures an architectural decision, context, consequences, and alternatives. |
| MVP | Minimum Viable Product. The smallest coherent and reviewable vertical slice of the platform. |
| FUTURE | A planned or possible later capability. It is not implemented unless separate evidence proves it. |
| OUT OF MVP | Explicitly excluded from the current MVP scope. These items must not be implied as delivered. |
| `[UNVALIDATED]` | Marker for a claim, capability, schema, flow, or assumption that has not yet been implemented, tested, and supported by runtime evidence. |
| Stakeholder Report | A concise status report for stakeholders, such as ITS professors, that communicates progress, risks, evidence, and next steps without leaking sensitive data or making unsupported claims. |
| Runtime Evidence | Concrete evidence from running software or hardware, such as logs, tests, screenshots, traces, build outputs, or verified API responses. |

---

## 8. Anti-regression Rules

These rules protect the Sprint 0 baseline and IHAP-10 repository skeleton.

1. This document must not contradict the repository skeleton introduced by IHAP-10.
2. The only firmware node in the MVP is `firmware/room-env-node/`.
3. The four backend directories remain target service boundaries, not proof of completed production services.
4. Kafka direct production from ESP32 remains OUT OF MVP.
5. Backend-side Kafka/event streaming remains FUTURE unless a later ADR and implementation task validate it.
6. Raw audio collection remains OUT OF MVP.
7. Presence tracking remains OUT OF MVP.
8. Door/window sensors remain FUTURE and OUT OF MVP unless changed by ADR.
9. 220V automation remains OUT OF MVP.
10. Mobile monitoring is a target direction unless supported by implementation evidence.
11. AI insight is a target/future service boundary unless supported by implementation evidence.
12. Stakeholder reports must not contain sensitive data, raw personal telemetry, raw audio, or unsupported production/safety/commercial claims.
13. Any unproven claim must be marked as `[UNVALIDATED]`.
14. Documentation must distinguish clearly between MVP, FUTURE, OUT OF MVP, and TARGET.
15. Jira must track status, evidence, decisions, and review state.
16. GitHub must remain the source of truth for versioned technical documentation.

---

## 9. Evidence Expectations

For IHAP-11, expected evidence is:

- A GitHub branch dedicated to the task.
- A draft pull request linked to IHAP-11.
- This versioned document under `docs/product/product-vision.md`.
- A Jira comment linking the PR and summarizing the documentation scope.
- Jira status moved to review after PR creation.
- No transition to completed until explicit project owner approval.

---

## 10. Review Checklist

Before this document can be considered accepted, reviewers should verify:

- Product Vision is understandable by ITS stakeholders.
- MVP scope is explicit and narrow.
- FUTURE and OUT OF MVP are separated.
- Runtime claims are not overstated.
- `[UNVALIDATED]` is used for directional schema or unproven capabilities.
- `firmware/room-env-node/` remains the only MVP firmware node.
- Raw audio, presence tracking, 220V automation, and Kafka client on ESP32 are not included in MVP.
- The four backend service boundaries are described as targets, not completed runtime services.
- The document does not regress IHAP-10.
