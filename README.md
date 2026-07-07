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
