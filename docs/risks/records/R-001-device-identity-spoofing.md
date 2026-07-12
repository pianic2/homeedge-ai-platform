# R-001 — Device Identity Spoofing

**Risk ID:** R-001  
**Risk status:** Under Treatment  
**Current assessment date:** 2026-07-12  
**Last reviewed:** 2026-07-12  
**Next review:** Event-driven  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Jira:** IHAP-40  
**PR:** Pending  
**Owner decision:** Pending

<!--
AI_AGENT_METADATA:
  issue: IHAP-40
  risk_id: R-001
  document_type: living_risk_record
  runtime_changes_allowed: false
  risk_acceptance_authority: project_owner
  orphan_status: not_orphan
  unvalidated_claim_marker: "[UNVALIDATED]"
-->

---

## 1. Risk Statement

There is a risk that a fake, cloned, disabled, or unknown MVP room/door node is treated as trusted because device identity and registry behavior remain `[UNVALIDATED]`.

## 2. Source Trigger and Scope

The MVP includes one ESP32-class room/door node and target ingestion/registry boundaries. The system must eventually distinguish known from unknown devices.

In scope: MVP node identity, registration, ingestion validation, rejection behavior and evidence.  
Out of scope: runtime implementation in IHAP-40, future nodes, and residual-risk decisions.

## 3. Affected Assets and Trust Boundary

| Area | Detail |
|---|---|
| Assets | Room/door node, device identifier, event origin, ingestion and registry boundaries |
| Trust boundary | Device -> network -> ingestion -> registry/read model |
| Data involved | Device identifier and technical event metadata |
| Stakeholder surface | Risk summary may be shown; credentials, secrets and private topology are blocked |

## 4. Current Assessment

| Field | Value | Rationale |
|---|---|---|
| Category | Security / Technical | Current MVP trust boundary |
| Likelihood | Medium | No runtime identity control exists |
| Impact | High | Untrusted events could corrupt telemetry and evidence |
| Residual risk | Pending Evidence | No implementation or verification evidence exists |
| Decision state | Pending Project Owner | No residual-risk decision is inferred |

## 5. Existing Controls

| Control | Evidence | Coverage | Limitation |
|---|---|---|---|
| Single generic MVP node boundary | `docs/product/product-vision.md` | Partial | Limits scope but does not authenticate a device |
| Target boundaries remain `[UNVALIDATED]` | `README.md` and Product Vision | Partial | Prevents overclaiming but provides no runtime control |

## 6. Risk Treatment Summary

| Treatment ID | Title | Strategy | Lifecycle status | Jira | ADR | Last review |
|---|---|---|---|---|---|---|
| RT-R001-01 | Device identity and ingestion trust boundary | Mitigate | Proposed | Pending Project Owner approval — future task 1 | Candidate | 2026-07-12 |

## 7. RT-R001-01 — Device identity and ingestion trust boundary

**Strategy:** Mitigate  
**Lifecycle status:** Proposed  
**Treatment owner:** Device / backend engineering  
**Jira coordination:** Pending Project Owner approval — future task 1  
**Related ADRs:** Candidate  
**Next review trigger:** A device registry, ingestion endpoint, provisioning flow, or event contract is proposed.

Planned actions:

- define stable device identity semantics;
- define registration, disablement and rejection behavior;
- validate event origin at ingestion;
- produce privacy-safe audit evidence;
- test unknown, disabled and malformed device handling.

Remaining exposure: provisioning, rotation, compromise recovery and cryptographic strength remain undecided and `[UNVALIDATED]`.

### Source and Evidence Register

| ID | Source | Type | Supports | Verification | Checked on | Limitations |
|---|---|---|---|---|---|---|
| SRC-01 | [NIST IR 8259A](https://csrc.nist.gov/pubs/ir/8259/a/final) | Official guidance | IoT device cybersecurity capability baseline | Verified | 2026-07-12 | Does not prescribe the project mechanism |
| SRC-02 | `docs/product/product-vision.md` | Project docs | MVP node and target service boundary | Verified | 2026-07-12 | Design evidence only |

### Evidence and Effectiveness

| Evidence | Class | Expected result | Actual result | Status |
|---|---|---|---|---|
| EV-01 | Implementation / Verification | Unknown, disabled and malformed identities are rejected | Not executed | `[UNVALIDATED]` |

**Effectiveness:** Pending Evidence  
**Residual risk after treatment:** Pending Evidence  
**Project Owner decision required:** Yes

## 8. Traceability

| Relationship | Link | Rule |
|---|---|---|
| Jira review task | IHAP-40 | Record migration only |
| Jira treatment task | Pending Project Owner approval — future task 1 | Operational coordination only |
| Related ADR | Candidate | No ADR created by IHAP-40 |
| Related risks | R-002 | Event origin validation may partially support payload trust |

## 9. Stakeholder Visibility

Stakeholder-safe wording:

```text
Device identity is a tracked MVP risk and remains [UNVALIDATED] until registry and ingestion behavior are implemented and tested.
```

## 10. Assessment History

| Date | Change | Treatment | Decision |
|---|---|---|---|
| 2026-07-12 | Migrated to IHAP-39 treatment model | RT-R001-01 Proposed | Pending |

## 11. Review Notes

```text
[x] Existing controls are separated from planned actions.
[x] Treatment starts as Proposed.
[x] Implementation and verification remain [UNVALIDATED].
[x] ADR is Candidate only; no ADR was created.
[x] Orphan check passed through a proposed treatment path.
[x] No runtime or MVP expansion was introduced.
[x] Project Owner decision remains Pending.
```