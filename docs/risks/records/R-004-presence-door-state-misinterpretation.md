# R-004 — Presence and Door State Misinterpretation

**Risk ID:** R-004  
**Risk status:** Under Treatment  
**Current assessment date:** 2026-07-12  
**Last reviewed:** 2026-07-12  
**Next review:** Event-driven  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Jira:** IHAP-40  
**Owner decision:** Pending

<!--
AI_AGENT_METADATA:
  issue: IHAP-40
  risk_id: R-004
  document_type: living_risk_record
  runtime_changes_allowed: false
  orphan_status: not_orphan
-->

## 1. Risk Statement

There is a risk that MVP local presence or door-state telemetry is misrepresented as person tracking, access control, intrusion detection, alarm-grade, antifurto, safety-critical or protection capability.

## 2. Source Trigger and Scope

The MVP includes local non-identifying presence and door open/closed telemetry only.

In scope: Product Vision wording, reports, demos and evidence.  
Out of scope: implementing security, safety, tracking, alarm or access-control capabilities.

## 3. Current Assessment

| Field | Value | Rationale |
|---|---|---|
| Category | Privacy / Compliance / Claims | Stakeholder interpretation of MVP telemetry |
| Likelihood | High | Door and presence wording is easily overread |
| Impact | High | Misrepresentation would violate claim boundaries |
| Residual risk | High | Every new stakeholder surface can reintroduce the risk |
| Decision state | Pending Project Owner | No residual-risk decision is inferred |

## 4. Existing Controls

| Control | Evidence | Coverage | Limitation |
|---|---|---|---|
| Telemetry-only boundary | `docs/product/product-vision.md` | Full for documented scope | Does not prevent future wording mistakes |
| Blocked stakeholder claims | `docs/governance/stakeholder-report-data-rules.md` | Full for governed reports | Requires review on each new surface |

## 5. Risk Treatment

### RT-R004-01 — Avoid security and safety reinterpretation

**Strategy:** Avoid  
**Lifecycle status:** Proposed  
**Treatment owner:** Governance / stakeholder review  
**Jira coordination:** Not required — existing policy and review  
**Related ADRs:** None  
**Next review trigger:** A report, demo, README claim or stakeholder summary mentions presence or door state.

Planned actions:

- describe door state only as telemetry or state;
- describe presence only as local non-identifying room state;
- block alarm, antifurto, tracking, access-control and protection wording;
- review demos and stakeholder summaries before publication.

**Remaining exposure:** Human error remains possible on new stakeholder surfaces.

### Source and Evidence Register

| ID | Source | Verification | Checked on | Limitations |
|---|---|---|---|---|
| SRC-01 | `docs/product/product-vision.md` | Verified | 2026-07-12 | Defines scope, not recurring compliance |
| SRC-02 | `docs/governance/stakeholder-report-data-rules.md` | Verified | 2026-07-12 | Requires application to each surface |

### Evidence and Effectiveness

| Evidence | Expected result | Actual result | Status |
|---|---|---|---|
| EV-01 | Stakeholder material uses telemetry-safe wording only | Not executed for future surfaces | `[UNVALIDATED]` |

**Effectiveness:** Pending Evidence  
**Project Owner decision required:** Yes

## 6. Traceability

| Relationship | Link | Rule |
|---|---|---|
| Jira review task | IHAP-40 | Record migration only |
| Jira treatment task | Not required | Existing policy/review is sufficient |
| Related ADR | None | No stable architectural decision required |

## 7. Stakeholder Visibility

```text
The MVP describes local presence and door state as telemetry only. It is not tracking, alarm, antifurto, access control, intrusion detection or protection.
```

## 8. Assessment History

| Date | Change | Treatment | Decision |
|---|---|---|---|
| 2026-07-12 | Legacy Reject proposal reclassified under IHAP-39 | RT-R004-01 Avoid / Proposed | Pending |

## 9. Review Notes

```text
[x] Treatment starts as Proposed.
[x] Avoid replaces the obsolete Reject treatment label.
[x] Existing policy is separated from future evidence.
[x] No runtime or MVP expansion was introduced.
[x] Orphan check passed through a governance treatment.
```