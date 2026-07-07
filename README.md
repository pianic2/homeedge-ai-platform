# HomeEdge AI Platform

**Edge-first smart home platform based on ESP32-C3 nodes, backend services, mobile monitoring, and structured documentation.**

HomeEdge is a portfolio project focused on building a smart home system from hardware nodes to backend APIs and mobile dashboards.

---

## Purpose

The project is designed to demonstrate a complete engineering path:

- embedded firmware for ESP32-C3 devices;
- smart home sensor integration;
- structured event collection;
- backend API design;
- mobile-first monitoring;
- reproducible setup;
- technical documentation.

---

## Sprint 0 Repository Skeleton

This repository starts with a deliberately small and explicit skeleton. The goal is to make project boundaries visible before runtime implementation begins.

```text
homeedge-ai-platform/
├── apps/
│   └── mobile/
├── docs/
│   ├── adr/
│   └── architecture/
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

- `firmware/room-env-node/`

Future nodes such as door/window sensors, presence radar nodes, raw audio processing, 220V automation, and Kafka edge-side producers are intentionally outside the Sprint 0 MVP skeleton unless a later ADR explicitly changes this boundary.

### Backend target topology

The backend target is represented as four service boundaries:

- `services/ingestion/`
- `services/device-registry/`
- `services/read-model/`
- `services/ai-insight/`

These directories are **target service boundaries**, not proof that production-ready services already exist.

---

## Architecture

```text
Edge Nodes -> Backend Services -> Mobile Dashboard
```

- **Edge Nodes:** collect room and device signals.
- **Backend Services:** receive, validate, and expose data.
- **Mobile Dashboard:** shows room state, latest telemetry, and device health.

---

## Stack

| Area | Stack |
|---|---|
| Firmware | ESP32-C3, ESP-IDF, C |
| Backend | Java, Spring Boot, REST APIs |
| Mobile | TypeScript, React Native, Expo |
| DevOps | Docker, GitHub Actions, Linux |
| Docs | Architecture notes, ADRs, project planning |

---

## Current Status

This repository is in early development. The current focus is Sprint 0: repository structure, architecture documentation, firmware baseline, backend ingestion contract, and mobile dashboard scope.

---

## Why It Matters

HomeEdge is intended to be the main technical portfolio project: it combines embedded systems, backend architecture, mobile development, DevOps basics, and project documentation in one coherent platform.
