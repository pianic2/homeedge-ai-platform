# Shift Left Governance Baseline

**Issue:** IHAP-14 — S0-005 — Shift Left Governance Baseline  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Document type:** Governance / Shift Left  
**Status:** Sprint 0 draft for review  
**Source of truth:** This versioned GitHub document is the canonical Shift Left baseline for issue-level impact checks until superseded by a later reviewed change.

<!--
AI_AGENT_METADATA:
  issue: IHAP-14
  document_type: shift_left_governance_baseline
  source_of_truth: github_versioned_repository_documentation
  canonical_path: "docs/governance/shift-left-governance-baseline.md"
  related_source_of_truth_policy: "docs/governance/source-of-truth.md"
  canonical_product_vision: "docs/product/product-vision.md"
  canonical_stakeholder_transparency: "docs/governance/stakeholder-transparency.md"
  task_scope: documentation_governance_only
  runtime_changes_allowed: false
  firmware_changes_allowed: false
  backend_changes_allowed: false
  mobile_changes_allowed: false
  jira_commit_convention: "IHAP-XX: Commit message"
  unvalidated_claim_marker: "[UNVALIDATED]"
  required_shift_left_dimensions:
    - Security
    - Privacy
    - Cost
    - Compliance
    - Testing
    - Documentation
    - Stakeholder Visibility
  impact_scale:
    - N/A
    - Low
    - Medium
    - High
  mandatory_block_rule: "Every task MUST include the same minimum Shift Left impact block, with all dimensions present in the same order."

HIDDEN_ANTI_REGRESSION_RULES:
  - GitHub remains the source of truth for technical documents, decisions, risks, policies, technical baselines, governance rules, source code, and PR evidence.
  - Jira remains authoritative for backlog, task state, workflow state, review state, blockers, and evidence links.
  - Confluence remains authoritative for stakeholder hub, stakeholder reports, stakeholder forms, and stakeholder navigation.
  - Stakeholder reports live only in Confluence.
  - Confluence must not duplicate long-form technical source-of-truth documents from GitHub.
  - If GitHub and Jira or Confluence diverge on technical content, GitHub wins until a reviewed GitHub change updates the source of truth.
  - The only firmware node in the MVP remains firmware/room-env-node/.
  - firmware/room-env-node/ remains a generic room/door node.
  - The MVP includes temperature, humidity, local non-identifying presence detection, and door open/closed state.
  - Raw audio, person tracking, behavioral history, identity inference, window scope, 220V automation, direct ESP32 Kafka publishing, commercial claims, safety-critical claims, and production/security-grade certification claims remain out of MVP.
  - The four services directories are target service boundaries [UNVALIDATED] unless validated by later implementation evidence.
  - Any unproven claim must be marked as [UNVALIDATED].
-->

---

## 1. Purpose

This baseline defines a lightweight Shift Left control for HomeEdge AI Platform issues.

Its goal is to make security, privacy, cost, compliance, testing, documentation, and stakeholder visibility impacts explicit before implementation, while remaining sustainable for a single operator.

This document is governance-only. It does not introduce firmware, backend, mobile, infrastructure, cloud, Kafka runtime, AI runtime, production-readiness, safety-critical guarantees, or security-grade certification.

---

## 2. Scope

Included:

- a fixed issue-level Shift Left impact block;
- mandatory impact dimensions;
- an explicit impact scale;
- motivated `N/A` handling;
- lightweight review and blocker rules;
- operational examples;
- a reusable issue template section;
- commit convention for Jira-linked work.

Excluded:

- enterprise-grade governance gates;
- blocking every issue by default;
- heavyweight compliance workflows;
- runtime validation;
- security certification;
- privacy/legal certification;
- stakeholder report creation;
- duplication of GitHub technical source of truth into Confluence.

---

## 3. Non-Regression Boundaries

This document does not redefine the MVP scope, source-of-truth policy, stakeholder reporting policy, or service boundary validation status.

Protected baselines:

- GitHub remains the technical source of truth.
- Jira remains the tracking, workflow, blocker, review-state, and evidence-link system.
- Confluence remains the stakeholder hub, stakeholder report, stakeholder form, and navigation layer.
- Stakeholder reports live only in Confluence.
- Confluence must not duplicate GitHub as the technical source of truth.
- If GitHub and Jira or Confluence diverge on technical content, GitHub wins until a reviewed GitHub source-of-truth change updates the project truth.
- Every unproven claim must be marked `[UNVALIDATED]`.
- `docs/governance/source-of-truth.md` remains the canonical policy for source-of-truth, DOC-REGRESSION, and `[UNVALIDATED]` governance.
- `firmware/room-env-node/` remains the only MVP firmware node.
- The MVP node remains a generic room/door node.
- The four service boundaries remain target directories `[UNVALIDATED]`:
  - `services/ingestion/`;
  - `services/device-registry/`;
  - `services/read-model/`;
  - `services/ai-insight/`.

Inside MVP:

- temperature;
- humidity;
- local non-identifying presence detection;
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

---

## 4. Shift Left Dimensions

Every task must evaluate the same seven dimensions.

| Dimension | Required evaluation |
|---|---|
| Security | Access control, abuse path, trust boundary, integrity, device/backend exposure, unsafe technical expansion. |
| Privacy | Data collection, identifiability, inference risk, retention, minimization, behavioral profiling risk. |
| Cost | Cloud usage, hardware cost, maintenance load, operational overhead, tooling or deployment cost. |
| Compliance | Legal/regulatory sensitivity, safety-sensitive behavior, certification language, claim discipline, stakeholder-facing risk. |
| Testing | Minimum validation evidence, manual check, automated test, reproducible log, or justified `N/A`. |
| Documentation | Canonical docs, README semantic links, ADR/risk docs, product boundaries, stakeholder summaries, or justified `N/A`. |
| Stakeholder Visibility | Jira evidence, Confluence navigation/report need, review visibility, stakeholder-facing explanation, or justified `N/A`. |

Impact scale:

```text
N/A | Low | Medium | High
```

Rules:

- `N/A` is valid only when explicitly justified.
- `Low`, `Medium`, and `High` must include a rationale.
- `High` impact must identify either mitigation, deferral, rejection, or required review evidence.
- Missing impact information is a governance defect.

---

## 5. Minimum Required Impact Block

Every task MUST include the same minimum Shift Left impact block.

The block is mandatory for all Jira issues, regardless of issue type. Each dimension must be present in the same order, even when the impact is `N/A`.

`N/A` is allowed only when explicitly justified.

### 5.1 Required Block

| Dimension | Impact | Rationale | Evidence / Action |
|---|---:|---|---|
| Security | N/A / Low / Medium / High | ... | ... |
| Privacy | N/A / Low / Medium / High | ... | ... |
| Cost | N/A / Low / Medium / High | ... | ... |
| Compliance | N/A / Low / Medium / High | ... | ... |
| Testing | N/A / Low / Medium / High | ... | ... |
| Documentation | N/A / Low / Medium / High | ... | ... |
| Stakeholder Visibility | N/A / Low / Medium / High | ... | ... |

### 5.2 Review Rule

A task is not ready for review if the Shift Left impact block is missing, incomplete, reordered, or contains unjustified `N/A` values.

This is a lightweight consistency rule, not an enterprise gate. The goal is to make impact explicit, not to stop development by default.

---

## 6. `N/A` Rule

`N/A` is allowed only when the issue has no meaningful impact on that dimension and the reason is explicitly stated.

Valid examples:

```text
Testing: N/A — documentation-only change, no executable behavior modified.
Cost: N/A — no infrastructure, cloud, hardware, tooling, or runtime component introduced.
Privacy: N/A — no data collection, storage, inference, retention, or identification behavior changed.
Stakeholder Visibility: N/A — internal cleanup with no stakeholder-facing state, report, or navigation impact.
```

Invalid examples:

```text
Testing: N/A — not needed.
Privacy: N/A — obvious.
Compliance: N/A — probably fine.
Documentation: N/A — later.
```

Reason: these do not explain why the dimension is not applicable.

---

## 7. Lightweight Blocking Rules

Shift Left does not block every issue by default.

A task or PR should be blocked only when one of the following conditions exists:

- `Security = High` without mitigation, rejection, deferral, or explicit review evidence.
- `Privacy = High` without minimization, boundary definition, rejection, deferral, or explicit review evidence.
- `Compliance = High` without claim control, `[UNVALIDATED]` marking, rejection, deferral, or explicit review evidence.
- A technical, commercial, safety, security-grade, or AI claim is unproven and not marked `[UNVALIDATED]`.
- The change expands the protected MVP boundary without reviewed approval.
- The change presents target service boundaries as implemented runtime without evidence.
- The change moves technical source of truth from GitHub into Jira or Confluence.
- The change creates a DOC-REGRESSION under `docs/governance/source-of-truth.md`.

A task or PR should not be blocked solely because:

- one or more dimensions are `Low` or `Medium` with sufficient rationale;
- one or more dimensions are `N/A` with explicit justification;
- the change is documentation-only;
- the risk is known, bounded, and tracked;
- the required action is a link, note, or future issue rather than immediate implementation.

---

## 8. Issue Shift Left Template

Use this section as the reusable issue-level template.

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

Minimum completion standard:

```text
Each row must contain an impact value, a rationale, and an evidence/action note.
```

---

## 9. Operational Examples

### 9.1 Documentation-Only Governance Issue

Example: creating or updating a governance baseline.

| Dimension | Impact | Rationale | Evidence / Action |
|---|---:|---|---|
| Security | Low | Improves control policy, no runtime security behavior changed. | Link governance doc or PR. |
| Privacy | Low | Clarifies privacy review expectations, no personal data processed. | Link governance doc or PR. |
| Cost | N/A | No infrastructure, cloud, hardware, tooling, or runtime component introduced. | No cost action required. |
| Compliance | Medium | Establishes review language for compliance-sensitive claims. | Preserve claim discipline and `[UNVALIDATED]` policy. |
| Testing | N/A | Documentation-only change, no executable behavior modified. | Review diff only. |
| Documentation | High | Canonical governance document created or updated. | Link canonical GitHub document. |
| Stakeholder Visibility | Medium | Jira evidence link required; Confluence may link without duplicating. | Link PR/doc from Jira and, if useful, Confluence navigation. |

### 9.2 Firmware Room/Door Node Change

Example: changing `firmware/room-env-node/` behavior.

| Dimension | Impact | Rationale | Evidence / Action |
|---|---:|---|---|
| Security | Medium | Device behavior and local event production may affect trust boundaries. | Provide implementation diff and review notes. |
| Privacy | Medium | Presence and door state are local non-identifying signals, but still privacy-relevant. | Confirm no person identification, raw audio, or behavioral history. |
| Cost | Low | No cloud cost unless event volume, hardware, or infrastructure changes. | Note hardware/runtime impact. |
| Compliance | Medium | Must avoid safety-critical, security-grade, or certification claims. | Preserve `[UNVALIDATED]` where evidence is missing. |
| Testing | High | Firmware behavior requires validation logs or reproducible test evidence. | Attach logs, manual test output, or automated test result. |
| Documentation | Medium | Firmware README or product boundary docs may need update. | Link updated docs or explain no doc impact. |
| Stakeholder Visibility | Low | Jira evidence link is usually sufficient. | Link PR and relevant test evidence. |

### 9.3 New AI Insight Claim

Example: describing future AI insight behavior.

| Dimension | Impact | Rationale | Evidence / Action |
|---|---:|---|---|
| Security | Medium | Generated insights may influence interpretation or future automation design. | Bound the claim and avoid runtime/security guarantees. |
| Privacy | High | Inference can become behavioral profiling if not bounded. | Reject, defer, or mark as target `[UNVALIDATED]`; define minimization boundary. |
| Cost | Medium | AI processing may introduce compute, storage, or provider cost. | Estimate or mark as future target `[UNVALIDATED]`. |
| Compliance | High | AI capability claims can become misleading if unvalidated. | Mark unproven claims `[UNVALIDATED]`. |
| Testing | Medium | Expected output and failure behavior need evidence before validation. | Require future evaluation evidence. |
| Documentation | High | Product boundaries and claim status must be updated. | Link product/governance update. |
| Stakeholder Visibility | Medium | Stakeholders may need a clear explanation if visible externally. | Link stakeholder-facing summary only; keep technical truth in GitHub. |

### 9.4 Out-of-Scope Technical Request

Example: direct ESP32 Kafka publishing or 220V automation.

| Dimension | Impact | Rationale | Evidence / Action |
|---|---:|---|---|
| Security | High | Expands attack surface or unsafe control boundary beyond MVP. | Reject for MVP or defer through reviewed future task. |
| Privacy | Medium | Depends on emitted data, retention, and downstream linkage. | Require future privacy review if reconsidered. |
| Cost | Medium | Introduces infrastructure, hardware, operational, or maintenance complexity. | Require future cost review if reconsidered. |
| Compliance | High | May trigger safety, certification, or regulatory concerns. | Keep out of MVP unless reviewed and explicitly approved. |
| Testing | High | Requires validation beyond current MVP baseline. | No MVP test action; future validation required if approved. |
| Documentation | High | Must be marked out of scope unless explicitly re-approved. | Preserve MVP boundary in Product Vision/source-of-truth docs. |
| Stakeholder Visibility | Medium | Jira rationale is required when rejecting/defering scope. | Link decision rationale from Jira. |

Decision:

```text
Reject for MVP or mark as future target [UNVALIDATED] through a reviewed source-of-truth change.
```

---

## 10. Commit Convention

All commits related to Jira issues MUST start with the Jira issue key.

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

## 11. Evidence Expectations

Each task should leave evidence proportional to its impact.

| Situation | Minimum evidence |
|---|---|
| Documentation-only | GitHub doc diff or PR link. |
| Firmware behavior | Code diff plus validation log, manual test note, or automated test output. |
| Backend/API behavior `[UNVALIDATED]` | Design doc, schema, test evidence, or explicit future-target marker. |
| Privacy-sensitive change | Data boundary, minimization note, retention note, or rejection rationale. |
| Cost-sensitive change | Cost note, infrastructure impact, or explicit no-runtime-cost rationale. |
| Compliance-sensitive change | Claim-control note, `[UNVALIDATED]` marker, or rejection/defer rationale. |
| Stakeholder-visible change | Jira evidence link and optional Confluence navigation/report link without duplicating GitHub technical truth. |

Evidence must be linkable from Jira when the task moves to review.

---

## 12. Review Checklist

Use this checklist before requesting review:

```text
[ ] The task includes the mandatory Shift Left impact block.
[ ] All seven dimensions are present in the required order.
[ ] Every N/A has an explicit rationale.
[ ] Every High impact has mitigation, rejection, deferral, or evidence action.
[ ] No protected MVP boundary was expanded silently.
[ ] No unproven claim appears without [UNVALIDATED].
[ ] GitHub remains the technical source of truth.
[ ] Jira is used for tracking and evidence links only.
[ ] Confluence is used for stakeholder navigation/reports only.
[ ] README semantic links are updated when canonical paths change or new canonical docs are added.
[ ] Commit messages start with the Jira issue key.
```

---

## 13. Relationship to Existing Governance

This document depends on and must not contradict:

- `docs/governance/source-of-truth.md`;
- `docs/product/product-vision.md`;
- `docs/governance/stakeholder-transparency.md`;
- `README.md` as root semantic index.

If this baseline conflicts with `docs/governance/source-of-truth.md`, the source-of-truth policy wins until a reviewed GitHub change resolves the conflict.
