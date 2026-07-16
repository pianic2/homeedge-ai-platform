# R-002 — Event Payload Leakage

**Risk ID:** R-002  
**Risk status:** Under Treatment  
**Current assessment date:** 2026-07-12  
**Last reviewed:** 2026-07-12  
**Next review:** Event-driven  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Jira:** IHAP-40, IHAP-42  
**PR:** #21  
**Owner decision:** Pending

<!--
AI_AGENT_METADATA:
  issue: IHAP-40
  risk_id: R-002
  document_type: living_risk_record
  runtime_changes_allowed: false
  orphan_status: not_orphan
  unvalidated_claim_marker: "[UNVALIDATED]"
-->

---

## 1. Risk Statement

There is a risk that MVP event payloads or logs expose unnecessary domestic or operational details because schema, transport, logging and retention behavior remain `[UNVALIDATED]`.

## 2. Source Trigger and Scope

The MVP includes temperature, humidity, local non-identifying presence and door-state telemetry moving toward a target ingestion boundary.

In scope: MVP payload fields, logs, retention, examples, screenshots and stakeholder evidence.  
Out of scope: AI data flows, runtime implementation in IHAP-40, and residual-risk decisions.

## 3. Affected Assets and Trust Boundary

| Area | Detail |
|---|---|
| Assets | Event payload, logs, examples, screenshots and stakeholder reports |
| Trust boundary | Device -> network -> ingestion -> logs/evidence |
| Data involved | Environmental telemetry, door/presence state and technical metadata |
| Stakeholder surface | Summary allowed; raw payloads and logs require minimization and redaction |

## 4. Current Assessment

| Field | Value | Rationale |
|---|---|---|
| Category | Security / Privacy | MVP telemetry disclosure risk |
| Likelihood | Medium | Payload and logging behavior are not implemented |
| Impact | High | Correlated telemetry can reveal domestic patterns |
| Residual risk | Pending Evidence | No runtime enforcement or tests exist |
| Decision state | Pending Project Owner | No residual-risk decision is inferred |

## 5. Existing Controls

| Control | Evidence | Coverage | Limitation |
|---|---|---|---|
| Blocked data categories | `docs/product/product-vision.md` | Partial | Documentation does not enforce runtime payloads |
| Stakeholder report redaction | `docs/governance/stakeholder-report-data-rules.md` | Partial | Does not cover service logs or retention |

## 6. Risk Treatment Summary

| Treatment ID | Title | Strategy | Lifecycle status | Jira | ADR | Last review |
|---|---|---|---|---|---|---|
| RT-R002-01 | Payload minimization and disclosure controls | Mitigate | Proposed | IHAP-42 | Candidate | 2026-07-12 |

## 7. RT-R002-01 — Payload minimization and disclosure controls

**Strategy:** Mitigate  
**Lifecycle status:** Proposed  
**Treatment owner:** Event contract / backend engineering  
**Jira coordination:** IHAP-42  
**Related ADRs:** Candidate  
**Next review trigger:** IHAP-42 begins schema, logging, retention, implementation or verification work.

Planned actions:

- define the minimum event fields;
- exclude OUT OF MVP and identifying fields;
- define logging, redaction, retention and disposal rules;
- test payloads, logs and stakeholder evidence against blocked fields.

Remaining exposure: transport confidentiality, access control and runtime retention remain implementation-specific and `[UNVALIDATED]`.

### Source and Evidence Register

| ID | Source | Type | Supports | Verification | Checked on | Limitations |
|---|---|---|---|---|---|---|
| SRC-01 | [Regulation (EU) 2016/679, Article 5](https://eur-lex.europa.eu/eli/reg/2016/679/oj) | Regulation | Minimization, storage limitation, integrity and confidentiality | Verified | 2026-07-12 | Applicability depends on identifiability and processing context |
| SRC-02 | [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html) | Official security guidance | Logging exclusion, protection, verification and disposal | Verified | 2026-07-12 | Guidance, not implementation evidence |
| SRC-03 | `docs/governance/stakeholder-report-data-rules.md` | Project docs | Stakeholder disclosure boundary | Verified | 2026-07-12 | Stakeholder surfaces only |
| SRC-04 | IHAP-42 | Jira coordination | Approved implementation and verification work path | Verified | 2026-07-12 | Coordination evidence only; not implementation evidence |

### Evidence and Effectiveness

| Evidence | Class | Expected result | Actual result | Status |
|---|---|---|---|---|
| EV-01 | Implementation / Verification | Only approved fields appear and sensitive values are absent from shared evidence | Not executed | `[UNVALIDATED]` |

**Effectiveness:** Pending Evidence  
**Residual risk after treatment:** Pending Evidence  
**Project Owner decision required:** Yes

## 8. Traceability

| Relationship | Link | Rule |
|---|---|---|
| Jira review task | IHAP-40 | Record migration and treatment topology |
| Jira treatment task | IHAP-42 | Shared operational coordination with R-003 |
| Pull request | #21 | Risk record migration and Jira link update |
| Related ADR | Candidate | No ADR created by IHAP-40 |
| Related risks | R-003 | Shared payload and metadata boundary |

## 9. Stakeholder Visibility

```text
Event payload leakage is tracked as an MVP privacy/security risk. Payload, logging and redaction behavior remain [UNVALIDATED] until implemented and reviewed through IHAP-42.
```

## 10. Assessment History

| Date | Change | Treatment | Decision |
|---|---|---|---|
| 2026-07-12 | Migrated to IHAP-39 treatment model | RT-R002-01 Proposed | Pending |
| 2026-07-12 | Linked approved operational task IHAP-42 | RT-R002-01 remains Proposed | Pending |

## 11. Review Notes

```text
[x] Treatment starts as Proposed.
[x] Jira treatment task IHAP-42 is linked.
[x] Runtime and effectiveness evidence remain [UNVALIDATED].
[x] ADR is Candidate only.
[x] Orphan check passed through a proposed treatment and Jira path.
[x] AI and other non-MVP flows were excluded.
[x] Project Owner decision remains Pending.
```
