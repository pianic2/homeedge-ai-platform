# Architecture Decision Records

**Issue:** IHAP-22 — S0-013 — ADR Index and ADR Template  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Document type:** ADR index  
**Source of truth:** This versioned GitHub document is the canonical ADR index for HomeEdge AI Platform until superseded by a later reviewed change.

<!--
AI_AGENT_METADATA:
  issue: IHAP-22
  document_type: adr_index
  canonical_path: docs/adr/README.md
  adr_template: docs/adr/template.md
  source_of_truth_policy: docs/governance/source-of-truth.md
  approval_authority: project_owner
  jira_role: evidence_links_only
  confluence_role: stakeholder_navigation_only
  unvalidated_claim_marker: "[UNVALIDATED]"

HIDDEN_ANTI_REGRESSION_RULES:
  - ADR content lives in GitHub.
  - Jira tracks ADR work state and evidence links only.
  - Confluence may summarize or link ADRs for stakeholder navigation, but must not duplicate long-form ADR content.
  - ADR status changes to Accepted, Rejected or Superseded require Project Owner approval.
  - Do not create ADRs only to increase document count.
  - Preserve [UNVALIDATED] on unproven claims.
  - Do not introduce production-ready, safety-critical, commercial-ready, certification or security-grade claims.
-->

---

## 1. Purpose

This folder contains Architecture Decision Records for HomeEdge AI Platform.

ADRs record reviewed architectural decisions, their context, alternatives, consequences, risks, follow-up work and evidence links. They do not approve themselves: acceptance requires Project Owner approval.

---

## 2. Source-of-Truth Rule

```text
GitHub stores ADR content.
Jira tracks work state and links evidence.
Confluence summarizes and links only.
```

---

## 3. ADR Naming Convention

```text
ADR-0001-short-kebab-title.md
ADR-0002-short-kebab-title.md
```

Rules:

- four-digit sequential number;
- lowercase kebab-case title;
- one decision per ADR;
- no renumbering after merge;
- superseded ADRs stay in the index.

---

## 4. ADR Status Model

| Status | Meaning |
|---|---|
| `Proposed` | Draft decision under review. Not accepted yet. |
| `Accepted` | Decision accepted by the Project Owner and linked to evidence. |
| `Superseded` | Replaced by a later ADR. Keep the historical record. |
| `Rejected` | Considered and explicitly rejected. Keep the rationale. |

Only the Project Owner can accept, reject or supersede an ADR.

---

## 5. Link Policy

Every ADR should link Jira work, PR evidence, related ADRs when relevant, and evidence for validated claims. Confluence is optional navigation only. Unproven claims keep `[UNVALIDATED]`.

---

## 6. ADR Index

| ADR | Title | Status | Jira | PR | Notes |
|---|---|---|---|---|---|
| [ADR-0001](ADR-0001-mvp-edge-compute-platform.md) | MVP Edge Compute Platform | Accepted | [IHAP-44](https://niccolopiazzi01.atlassian.net/browse/IHAP-44) | [PR #23](https://github.com/pianic2/homeedge-ai-platform/pull/23) | Accepts ESP32-C3 as the MVP family, the purchased SuperMini-compatible board as preferred conditional implementation and ESP32-C3-DevKitC-02 as official control/fallback. Exact commercial SKU reproducibility and quantitative power remain `[UNVALIDATED]`. |
| [ADR-0002](ADR-0002-environmental-sensor-profiles.md) | Environmental Sensor Profiles | Accepted | [IHAP-45](https://niccolopiazzi01.atlassian.net/browse/IHAP-45) | [PR #29](https://github.com/pianic2/homeedge-ai-platform/pull/29) | Selects DHT11 as the standard indoor profile and BME280 as the precision/extended-environment profile. DHT22 is not selected. Absolute accuracy remains `[UNVALIDATED]`; pressure remains outside the MVP measurement contract. |
| [ADR-0003](ADR-0003-mvp-door-state-sensor.md) | MVP Door State Sensor | **Accepted** | [IHAP-47](https://niccolopiazzi01.atlassian.net/browse/IHAP-47) | [PR #26](https://github.com/pianic2/homeedge-ai-platform/pull/26) | Accepted 2026-09-01. Passive wired two-conductor magnetic reed-contact technology for binary door-state telemetry; `MC38-A` is the tested local specimen. Open contact and interrupted conductor remain electrically indistinguishable. |
| [ADR-0004](ADR-0004-local-status-display.md) | Local Status Display | **Accepted** | [IHAP-53](https://niccolopiazzi01.atlassian.net/browse/IHAP-53) | [PR #31](https://github.com/pianic2/homeedge-ai-platform/pull/31) | Accepted 2026-08-31. Reference MVP includes a 0.96-inch-class 128×64 monochrome I2C local status/debug display; exact controller/provenance/power/replacement reproducibility remain bounded by evidence. |
| [ADR-0005](ADR-0005-mvp-presence-sensor.md) | MVP Presence Sensor | **Accepted** | [IHAP-46](https://niccolopiazzi01.atlassian.net/browse/IHAP-46) | [PR #25](https://github.com/pianic2/homeedge-ai-platform/pull/25), [PR #33](https://github.com/pianic2/homeedge-ai-platform/pull/33) | Accepted 2026-09-01. Selects HLK-LD2410C-class radar for local boolean presence only; onset/release and replacement-equivalence limitations remain explicit. |
| [ADR-0006](ADR-0006-mvp-central-node-hardware-profile.md) | MVP Central Node Hardware Profile | **Proposed** | [IHAP-52](https://niccolopiazzi01.atlassian.net/browse/IHAP-52) | [PR #30](https://github.com/pianic2/homeedge-ai-platform/pull/30) | Vendor-neutral 64-bit Linux profile with Raspberry Pi 4 Model B >=4 GB / 32 GB A2 as first reference-validation candidate. Physical validation is pending; workload sufficiency, storage endurance/retention and AI acceleration remain `[UNVALIDATED]`. |

---

## 7. Practical Rule

```text
Create ADRs because a decision needs traceability.
Do not create ADRs to increase document count.
```
