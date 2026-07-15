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

ADRs record reviewed architectural decisions, their context, alternatives, consequences, risks, follow-up work and evidence links.

They do not approve themselves. ADR acceptance requires Project Owner approval.

---

## 2. Source-of-Truth Rule

```text
GitHub stores ADR content.
Jira tracks work state and links evidence.
Confluence summarizes and links only.
```

Confluence must not duplicate full ADR content as a competing technical source of truth.

---

## 3. ADR Naming Convention

Use this file format:

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

Every ADR should link:

| Link | Required when |
|---|---|
| Jira issue | Always, when decision work is tracked in Jira. |
| Pull request | Required when the ADR is added or changed through PR. |
| Related ADRs | Required when superseding or depending on another ADR. |
| Evidence | Required when a claim is treated as validated. |
| Confluence | Optional; only for stakeholder navigation or report links. |

Unproven claims must keep `[UNVALIDATED]`.

---

## 6. ADR Index

| ADR | Title | Status | Jira | PR | Notes |
|---|---|---|---|---|---|
| [ADR-0001](ADR-0001-mvp-edge-compute-platform.md) | MVP Edge Compute Platform | Accepted | [IHAP-44](https://niccolopiazzi01.atlassian.net/browse/IHAP-44) | [PR #23](https://github.com/pianic2/homeedge-ai-platform/pull/23) | Accepts ESP32-C3 as the MVP family, the purchased SuperMini-compatible board as preferred conditional implementation and ESP32-C3-DevKitC-02 as official control/fallback. Physical pinout is evidenced for one specimen; exact commercial SKU reproducibility and quantitative power remain `[UNVALIDATED]`. A local display is not accepted by this ADR and is decided separately by [IHAP-53](https://niccolopiazzi01.atlassian.net/browse/IHAP-53). |

---

## 7. Practical Rule

```text
Create ADRs because a decision needs traceability.
Do not create ADRs to increase document count.
```
