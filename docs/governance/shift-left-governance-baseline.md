# Shift Left Governance Baseline

**Issue:** IHAP-14 — S0-005 — Shift Left Governance Baseline  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Document type:** Governance / Shift Left  
**Status:** Sprint 0 draft for review  
**Source of truth:** GitHub repository documentation.

<!--
AI_AGENT_METADATA:
  issue: IHAP-14
  canonical_path: docs/governance/shift-left-governance-baseline.md
  policy_role: issue_level_shift_left_baseline
  source_of_truth_policy: docs/governance/source-of-truth.md
  required_block: Security, Privacy, Cost, Compliance, Testing, Documentation, Stakeholder Visibility
  impact_scale: N/A, Low, Medium, High
  invariant: every_task_uses_same_block_same_order
  na_rule: explicit_rationale_required
  commit_convention: "IHAP-XX: Commit message"
  protected_scope: MVP boundary and [UNVALIDATED] policy must not be changed here
-->

---

## 1. Why This Document Exists

Every task must consider risk early, before implementation expands.

This baseline defines a lightweight Shift Left check for:

- security;
- privacy;
- cost;
- compliance;
- testing;
- documentation;
- stakeholder visibility.

The goal is simple: make the impact of each task explicit without creating an enterprise-style approval process.

This must remain sustainable for a single operator.

---

## 2. What This Document Does Not Change

This document does **not** redefine the project scope.

The following rules stay unchanged:

- GitHub is the technical source of truth.
- Jira tracks backlog, workflow state, blockers, review state, and evidence links.
- Confluence is the stakeholder hub, stakeholder report surface, form surface, and navigation layer.
- Stakeholder reports live only in Confluence.
- Confluence must not duplicate GitHub as the technical source of truth.
- If GitHub and Jira/Confluence diverge on technical content, GitHub wins until a reviewed GitHub change updates the project truth.
- Every unproven claim must be marked `[UNVALIDATED]`.
- `docs/governance/source-of-truth.md` remains the canonical source-of-truth and DOC-REGRESSION policy.

Protected MVP boundary:

- the only MVP firmware node is `firmware/room-env-node/`;
- the MVP node is a generic room/door node;
- the MVP includes temperature, humidity, local non-identifying presence detection, and door open/closed state;
- the MVP excludes person tracking, behavioral history, person identification, raw audio, window sensors, 220V automation, direct ESP32 Kafka publishing, commercial claims, safety-critical claims, and production/security-grade certification claims;
- `services/ingestion/`, `services/device-registry/`, `services/read-model/`, and `services/ai-insight/` remain target service boundaries `[UNVALIDATED]`.

---

## 3. Mandatory Shift Left Block

Every Jira task must include the same minimum Shift Left block.

The block is mandatory for every issue type. All rows must stay in the same order, even when the impact is `N/A`.

| Dimension | Impact | Rationale | Evidence / Action |
|---|---:|---|---|
| Security | N/A / Low / Medium / High | ... | ... |
| Privacy | N/A / Low / Medium / High | ... | ... |
| Cost | N/A / Low / Medium / High | ... | ... |
| Compliance | N/A / Low / Medium / High | ... | ... |
| Testing | N/A / Low / Medium / High | ... | ... |
| Documentation | N/A / Low / Medium / High | ... | ... |
| Stakeholder Visibility | N/A / Low / Medium / High | ... | ... |

A task is not ready for review if this block is missing, incomplete, reordered, or contains unjustified `N/A` values.

---

## 4. Impact Levels

Use only these values:

| Impact | Meaning |
|---|---|
| `N/A` | The dimension has no meaningful impact. A reason is still required. |
| `Low` | Minor impact. No special action beyond normal review. |
| `Medium` | Relevant impact. The rationale and evidence/action must be clear. |
| `High` | Critical impact. The task needs mitigation, deferral, rejection, or explicit review evidence. |

---

## 5. Dimensions

| Dimension | What to check |
|---|---|
| Security | Attack surface, trust boundary, access, abuse, integrity, unsafe expansion. |
| Privacy | Data collection, identifiability, retention, inference, minimization, profiling risk. |
| Cost | Cloud cost, hardware cost, tooling cost, maintenance load, operational overhead. |
| Compliance | Legal sensitivity, safety claims, certification claims, misleading claims, regulatory risk. |
| Testing | Required validation, manual check, automated test, logs, or justified `N/A`. |
| Documentation | README, governance docs, product docs, ADRs, risk docs, or justified `N/A`. |
| Stakeholder Visibility | Jira evidence, stakeholder-facing summary need, Confluence navigation/report impact. |

---

## 6. `N/A` Rule

`N/A` is allowed only when the reason is explicit.

Good examples:

```text
Testing: N/A — documentation-only change, no executable behavior modified.
Cost: N/A — no infrastructure, cloud, hardware, tooling, or runtime component introduced.
Privacy: N/A — no data collection, storage, inference, retention, or identification behavior changed.
```

Bad examples:

```text
Testing: N/A — not needed.
Privacy: N/A — obvious.
Compliance: N/A — probably fine.
Documentation: N/A — later.
```

Reason: these do not explain why the dimension is not applicable.

---

## 7. When Review Should Block

Shift Left must not block development by default.

Block review only when there is a real governance risk, such as:

- `Security = High` without mitigation, deferral, rejection, or evidence;
- `Privacy = High` without minimization, boundary definition, deferral, rejection, or evidence;
- `Compliance = High` without claim control, `[UNVALIDATED]` marking, deferral, rejection, or evidence;
- an unproven technical, commercial, safety, security-grade, or AI claim without `[UNVALIDATED]`;
- silent MVP expansion;
- target service boundaries presented as implemented runtime without evidence;
- technical source of truth moved from GitHub to Jira or Confluence;
- DOC-REGRESSION under `docs/governance/source-of-truth.md`.

Do not block review only because a dimension is `Low`, `Medium`, or justified `N/A`.

---

## 8. Template to Copy Into Tasks

```md
## Shift Left Impact

| Dimension | Impact | Rationale | Evidence / Action |
|---|---:|---|---|
| Security | N/A / Low / Medium / High |  |  |
| Privacy | N/A / Low / Medium / High |  |  |
| Cost | N/A / Low / Medium / High |  |  |
| Compliance | N/A / Low / Medium / High |  |  |
| Testing | N/A / Low / Medium / High |  |  |
| Documentation | N/A / Low / Medium / High |  |  |
| Stakeholder Visibility | N/A / Low / Medium / High |  |  |
```

Each row must contain:

1. an impact value;
2. a short rationale;
3. evidence, action, mitigation, deferral, rejection, or a clear `N/A` reason.

---

## 9. Examples

### 9.1 Documentation-only governance task

| Dimension | Impact | Rationale | Evidence / Action |
|---|---:|---|---|
| Security | Low | Improves governance, no runtime security behavior changed. | Link PR/doc. |
| Privacy | Low | Clarifies privacy checks, no personal data processed. | Link PR/doc. |
| Cost | N/A | No infrastructure, cloud, hardware, tooling, or runtime component introduced. | No action. |
| Compliance | Medium | Adds claim-control rules. | Preserve `[UNVALIDATED]` policy. |
| Testing | N/A | Documentation-only change. | Review diff. |
| Documentation | High | Canonical governance document created or updated. | Link GitHub doc. |
| Stakeholder Visibility | Medium | Jira evidence link required. | Link PR/doc from Jira. |

### 9.2 Firmware room/door node task

| Dimension | Impact | Rationale | Evidence / Action |
|---|---:|---|---|
| Security | Medium | Device behavior can affect trust boundaries. | Review implementation diff. |
| Privacy | Medium | Presence and door state are privacy-relevant even if non-identifying. | Confirm no identification, raw audio, or behavioral history. |
| Cost | Low | No cloud cost unless event volume, hardware, or infrastructure changes. | Note hardware/runtime impact. |
| Compliance | Medium | Avoid safety-critical, security-grade, or certification claims. | Preserve `[UNVALIDATED]` where needed. |
| Testing | High | Firmware behavior needs evidence. | Attach logs or test output. |
| Documentation | Medium | Firmware docs may need update. | Link docs or explain no doc impact. |
| Stakeholder Visibility | Low | Jira evidence is usually enough. | Link PR and test evidence. |

### 9.3 New AI insight claim

| Dimension | Impact | Rationale | Evidence / Action |
|---|---:|---|---|
| Security | Medium | Insights may influence interpretation or later automation. | Bound the claim. |
| Privacy | High | Inference can become behavioral profiling. | Defer, reject, or mark `[UNVALIDATED]`. |
| Cost | Medium | AI processing may introduce compute or provider cost. | Estimate or mark future target `[UNVALIDATED]`. |
| Compliance | High | AI capability claims can be misleading if unvalidated. | Mark unproven claims `[UNVALIDATED]`. |
| Testing | Medium | Expected output needs evidence before validation. | Require future evaluation evidence. |
| Documentation | High | Product boundaries and claim status must stay clear. | Update canonical docs. |
| Stakeholder Visibility | Medium | Stakeholders may need a clear summary if externally visible. | Link summary without duplicating technical truth. |

### 9.4 Out-of-scope technical request

Example: direct ESP32 Kafka publishing or 220V automation.

| Dimension | Impact | Rationale | Evidence / Action |
|---|---:|---|---|
| Security | High | Expands attack surface or unsafe control boundary beyond MVP. | Reject for MVP or defer. |
| Privacy | Medium | Depends on emitted data, retention, and linkage. | Require future privacy review if reconsidered. |
| Cost | Medium | Adds infrastructure, hardware, or maintenance complexity. | Require future cost review if reconsidered. |
| Compliance | High | May trigger safety, certification, or regulatory concerns. | Keep out of MVP unless reviewed and approved. |
| Testing | High | Requires validation beyond current MVP baseline. | Future validation required if approved. |
| Documentation | High | Must remain out of scope unless re-approved. | Preserve MVP boundary docs. |
| Stakeholder Visibility | Medium | Jira rationale required when rejecting or deferring scope. | Link decision rationale. |

Decision for MVP:

```text
Reject, defer, or mark as future target [UNVALIDATED] through a reviewed source-of-truth change.
```

---

## 10. Commit Convention

All commits related to Jira issues must start with the Jira issue key.

Format:

```text
IHAP-XX: Commit message
```

Examples:

```text
IHAP-14: Add Shift Left governance baseline
IHAP-14: Link Shift Left baseline from README
IHAP-15: Add risk register baseline
```

Do not place the Jira issue key at the end of the commit message.

---

## 11. Review Checklist

Before requesting review, check:

```text
[ ] The task includes the mandatory Shift Left block.
[ ] All seven dimensions are present in the required order.
[ ] Every N/A has a clear reason.
[ ] Every High impact has mitigation, rejection, deferral, or evidence.
[ ] No MVP boundary was expanded silently.
[ ] No unproven claim appears without [UNVALIDATED].
[ ] GitHub remains the technical source of truth.
[ ] Jira is used for tracking and evidence links.
[ ] Confluence is used for stakeholder navigation/reports only.
[ ] README links are updated when canonical docs are added or moved.
[ ] Commit messages start with the Jira issue key.
```

---

## 12. Related Documents

This baseline must stay aligned with:

- `docs/governance/source-of-truth.md`;
- `docs/product/product-vision.md`;
- `docs/governance/stakeholder-transparency.md`;
- `README.md`.

If this document conflicts with `docs/governance/source-of-truth.md`, the source-of-truth policy wins until a reviewed GitHub change resolves the conflict.
