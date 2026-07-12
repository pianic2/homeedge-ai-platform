# R-003 — Technical Metadata Inference

**Risk ID:** R-003  
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
  risk_id: R-003
  document_type: living_risk_record
  runtime_changes_allowed: false
  orphan_status: not_orphan
  unvalidated_claim_marker: "[UNVALIDATED]"
-->

---

## 1. Risk Statement

There is a risk that MVP technical metadata reveals domestic context when timestamps, device identifiers, room labels or network details are retained, correlated or exposed.

## 2. Source Trigger and Scope

Technical metadata is useful for debugging and evidence, but combinations may reveal topology or activity patterns.

In scope: MVP metadata, logs, retention, screenshots, examples and stakeholder summaries.  
Out of scope: behavioral profiling, AI inference and other FUTURE capabilities.

## 3. Affected Assets and Trust Boundary

| Area | Detail |
|---|---|
| Assets | Technical metadata, logs, screenshots, examples and stakeholder summaries |
| Trust boundary | Runtime telemetry -> logs/storage -> stakeholder evidence |
| Data involved | Timestamps, device identifiers, generic room labels, firmware version and network metadata |
| Stakeholder surface | Generic summaries allowed; private topology and network details are redacted or blocked |

## 4. Current Assessment

| Field | Value | Rationale |
|---|---|---|
| Category | Privacy / Stakeholder Visibility | MVP metadata exposure |
| Likelihood | Medium | Metadata is likely to appear in engineering evidence |
| Impact | Medium | Correlation may reveal topology or activity timing |
| Residual risk | Pending Evidence | Retention and correlation controls are not implemented |
| Decision state | Pending Project Owner | No residual-risk decision is inferred |

## 5. Existing Controls

| Control | Evidence | Coverage | Limitation |
|---|---|---|---|
| Private network metadata excluded from stakeholder view | `docs/product/product-vision.md` | Partial | Runtime collection and retention remain unknown |
| Redaction and link-only reporting | `docs/governance/stakeholder-report-data-rules.md` | Partial | Requires repeated human review |

## 6. Risk Treatment Summary

| Treatment ID | Title | Strategy | Lifecycle status | Jira | ADR | Last review |
|---|---|---|---|---|---|---|
| RT-R003-01 | Stakeholder metadata redaction | Mitigate | Proposed | Not required — existing policy and review | None | 2026-07-12 |
| RT-R003-02 | Metadata minimization and retention boundary | Mitigate | Proposed | IHAP-42 | Candidate | 2026-07-12 |

## 7. Risk Treatments

### RT-R003-01 — Stakeholder metadata redaction

**Strategy:** Mitigate  
**Lifecycle status:** Proposed  
**Treatment owner:** Documentation / stakeholder review  
**Jira coordination:** Not required — existing policy and review  
**Related ADRs:** None  
**Next review trigger:** A report, demo, screenshot, payload example or public log is prepared.

Planned actions:

- use generic room labels;
- remove private addresses and topology;
- omit network identifiers;
- review examples and screenshots before publication.

**Remaining exposure:** Human review can fail; runtime metadata still requires RT-R003-02.

Source: `docs/governance/stakeholder-report-data-rules.md` — Verified on 2026-07-12.

### RT-R003-02 — Metadata minimization and retention boundary

**Strategy:** Mitigate  
**Lifecycle status:** Proposed  
**Treatment owner:** Event contract / backend engineering  
**Jira coordination:** IHAP-42  
**Related ADRs:** Candidate  
**Next review trigger:** IHAP-42 begins schema, logging, retention, implementation or verification work.

Planned actions:

- classify and justify metadata fields;
- define generic versus private labels;
- bound retention and disposal;
- test correlation and disclosure paths.

**Remaining exposure:** Some timestamps and identifiers may remain necessary for operation and evidence.

### Source and Evidence Register

| ID | Source | Type | Supports | Verification | Checked on | Limitations |
|---|---|---|---|---|---|---|
| SRC-01 | [Regulation (EU) 2016/679, Article 5](https://eur-lex.europa.eu/eli/reg/2016/679/oj) | Regulation | Minimization and storage limitation | Verified | 2026-07-12 | Applicability depends on context |
| SRC-02 | [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html) | Official security guidance | Logging exclusion, protection and disposal | Verified | 2026-07-12 | Guidance only |
| SRC-03 | `docs/product/product-vision.md` | Project docs | MVP data boundary | Verified | 2026-07-12 | Design evidence only |
| SRC-04 | IHAP-42 | Jira coordination | Approved implementation and verification work path | Verified | 2026-07-12 | Coordination evidence only; not implementation evidence |

### Evidence and Effectiveness

| Evidence | Treatment | Expected result | Actual result | Status |
|---|---|---|---|---|
| EV-01 | RT-R003-01 | Published evidence excludes private topology and network metadata | Not executed | `[UNVALIDATED]` |
| EV-02 | RT-R003-02 | Metadata fields and retention are justified, bounded and tested | Not executed | `[UNVALIDATED]` |

**Effectiveness:** Pending Evidence  
**Residual risk after treatment:** Pending Evidence  
**Project Owner decision required:** Yes

## 8. Traceability

| Relationship | Link | Rule |
|---|---|---|
| Jira review task | IHAP-40 | Record migration and treatment topology |
| Jira treatment task | IHAP-42 | Shared operational coordination with R-002 |
| Pull request | #21 | Risk record migration and Jira link update |
| Related ADR | Candidate for RT-R003-02 | No ADR created by IHAP-40 |
| Related risks | R-002 | Shared payload and metadata boundary |

## 9. Stakeholder Visibility

```text
Technical metadata is useful for MVP evidence but may expose domestic context. Private topology and network details are redacted or omitted; runtime controls remain [UNVALIDATED] until implemented through IHAP-42.
```

## 10. Assessment History

| Date | Change | Treatment | Decision |
|---|---|---|---|
| 2026-07-12 | Migrated and split into governance/runtime treatments | RT-R003-01; RT-R003-02 Proposed | Pending |
| 2026-07-12 | Linked approved operational task IHAP-42 | RT-R003-02 remains Proposed | Pending |

## 11. Review Notes

```text
[x] Both treatments start as Proposed.
[x] Policy and runtime responsibilities are separated.
[x] Jira treatment task IHAP-42 is linked to RT-R003-02.
[x] Runtime and effectiveness evidence remain [UNVALIDATED].
[x] ADR is Candidate only for the runtime boundary.
[x] Orphan check passed through treatment paths.
[x] Non-MVP profiling and AI inference were excluded.
```
