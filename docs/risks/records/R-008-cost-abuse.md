# R-008 — Cost Abuse and Operational Overhead

**Risk ID:** R-008  
**Risk status:** Under Treatment  
**Current assessment date:** 2026-07-12  
**Last reviewed:** 2026-07-12  
**Next review:** Event-driven  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Jira:** IHAP-40; IHAP-17  
**Owner decision:** Pending

<!--
AI_AGENT_METADATA:
  issue: IHAP-40
  risk_id: R-008
  document_type: living_risk_record
  runtime_changes_allowed: false
  orphan_status: not_orphan
-->

## 1. Risk Statement

There is a risk that MVP hardware replication, event volume, logs, tooling or later hosted execution create uncontrolled cost because assumptions and measurements are incomplete.

## 2. Source Trigger and Scope

The MVP requires a low-cost reproducible node and may later connect to target ingestion or hosted tooling.

In scope: MVP BOM, contributor replication cost, development tools, event/log assumptions and any later hosted boundary explicitly admitted into scope.  
Out of scope: AI-provider cost while AI remains outside MVP, purchases in IHAP-40, and runtime enforcement.

## 3. Current Assessment

| Field | Value | Rationale |
|---|---|---|
| Category | Cost / Technical | MVP replicability and operational overhead |
| Likelihood | Medium | Hardware and tooling costs exist; runtime volume is not measured |
| Impact | Medium | Unbounded cost can block replication or continuation |
| Residual risk | Pending Evidence | IHAP-17 and runtime measurements are incomplete |
| Decision state | Pending Project Owner | No residual-risk decision is inferred |

## 4. Existing Controls

| Control | Evidence | Coverage | Limitation |
|---|---|---|---|
| Cost governance task | IHAP-17 | Partial | Policy is not yet implemented or merged |
| Runtime and paid services remain `[UNVALIDATED]` | Product Vision and claim policy | Partial | No measured limits exist |

## 5. Risk Treatment

### RT-R008-01 — Establish MVP cost assumptions and guardrails

**Strategy:** Mitigate  
**Lifecycle status:** Proposed  
**Treatment owner:** Cost governance / Project Owner  
**Jira coordination:** IHAP-17  
**Related ADRs:** None  
**Next review trigger:** IHAP-17 completes, the MVP BOM changes, or hosted runtime/log retention is proposed.

Planned actions:

- record dated BOM price snapshots;
- show MVP replication cost;
- document free versus paid tooling;
- define event-rate and log-retention assumptions when runtime is proposed;
- require explicit approval before paid cloud or tooling commitments.

**Remaining exposure:** Actual hosted usage, billing alerts and runtime kill-switches remain `[UNVALIDATED]` until hosted execution exists.

### Source and Evidence Register

| ID | Source | Verification | Checked on | Limitations |
|---|---|---|---|---|
| SRC-01 | IHAP-17 | Verified | 2026-07-12 | Governance task, not runtime evidence |
| SRC-02 | `docs/product/product-vision.md` | Verified | 2026-07-12 | Defines MVP/FUTURE boundaries only |

### Evidence and Effectiveness

| Evidence | Expected result | Actual result | Status |
|---|---|---|---|
| EV-01 | MVP replication cost and paid-service assumptions are explicit, dated and reviewable | Not executed | `[UNVALIDATED]` |

**Effectiveness:** Pending Evidence  
**Project Owner decision required:** Yes

## 6. Traceability

| Relationship | Link | Rule |
|---|---|---|
| Jira review task | IHAP-40 | Record migration and scope reduction |
| Jira treatment task | IHAP-17 | Canonical cost/BOM coordination |
| Related ADR | None | No architectural decision required now |

## 7. Stakeholder Visibility

```text
MVP cost exposure is tracked through dated BOM and tooling assumptions. Hosted runtime cost remains [UNVALIDATED] until a hosted design and measurements exist.
```

## 8. Assessment History

| Date | Change | Treatment | Decision |
|---|---|---|---|
| 2026-07-12 | Narrowed to MVP cost and reproducibility; AI-provider scope removed | RT-R008-01 Proposed | Pending |

## 9. Review Notes

```text
[x] Treatment starts as Proposed.
[x] IHAP-17 is the existing coordination path.
[x] AI-provider cost was removed while AI remains outside MVP.
[x] No third treatment task was introduced.
[x] Orphan check passed through IHAP-17 linkage.
```