# AI Review Agents Policy — Sprint 0 Regression Control

**Issue:** IHAP-34 — S0-025 — Configure Review Agents; extended by IHAP-54 — Strengthen ADR Review Agents  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Document type:** AI Governance / Review Governance  
**Status:** Sprint 0 draft for review  
**Source of truth:** This versioned GitHub document is the canonical policy for Sprint 0 advisory review agents until superseded by a later reviewed change.

<!--
AI_AGENT_METADATA:
  issue: IHAP-34
  extended_by:
    - IHAP-54
  document_type: ai_review_agents_policy
  source_of_truth: github_versioned_repository_documentation
  task_scope: documentation_governance_only
  runtime_changes_allowed: false
  firmware_changes_allowed: false
  backend_changes_allowed: false
  mobile_changes_allowed: false
  cloud_changes_allowed: false
  ci_runtime_enforcement_allowed: false
  autonomous_decision_authority: false
  adr_approval_allowed: false
  issue_closure_allowed: false
  issue_transition_allowed_without_project_owner_instruction: false
  production_ready_claims_allowed: false
  safety_critical_claims_allowed: false
  commercial_ready_claims_allowed: false
  security_grade_claims_allowed: false
  unvalidated_claim_marker: "[UNVALIDATED]"
  severity_model:
    - BLOCKER
    - MAJOR
    - MINOR
    - NOTE
  canonical_source_of_truth_policy: "docs/governance/source-of-truth.md"
  canonical_documentation_strategy: "docs/governance/documentation-strategy.md"
  canonical_shift_left_baseline: "docs/governance/shift-left-governance-baseline.md"
  canonical_governance_lane_review_gate: "docs/governance/governance-lane-review-gate.md"
  canonical_stakeholder_transparency: "docs/governance/stakeholder-transparency.md"
  canonical_adr_index: "docs/adr/README.md"
  canonical_adr_template: "docs/adr/template.md"
  canonical_risk_model: "docs/risks/risk-model-baseline.md"
  root_semantic_index: "README.md"
  review_agents:
    - source_of_truth_guardian
    - architecture_regression_reviewer
    - event_contract_reviewer
    - security_privacy_reviewer
    - testing_evidence_reviewer
    - stakeholder_clarity_reviewer
    - adr_conformance_reviewer

HIDDEN_ANTI_REGRESSION_RULES:
  - Review agents are advisory only.
  - Review agents may detect, classify, recommend, and report findings.
  - Review agents must not approve ADRs, close issues, declare Ready or Done, or transition Jira issues without explicit Project Owner instruction.
  - ADR status changes to Accepted, Rejected, or Superseded remain Project Owner decisions.
  - Governance-lane movement toward Review, Stakeholder Review, or Done must follow docs/governance/governance-lane-review-gate.md.
  - GitHub remains the technical source of truth for technical documents, policies, governance rules, ADRs, risks, source code, and PR evidence.
  - Jira remains authoritative for backlog, task state, workflow state, review state, blockers, and evidence links.
  - Confluence remains authoritative for stakeholder hub, stakeholder reports, stakeholder forms, and stakeholder navigation.
  - Confluence must not duplicate long-form GitHub technical documentation.
  - Any unproven implementation, AI, reliability, security, production, safety, commercial, or stakeholder-facing claim must keep [UNVALIDATED].
  - The protected MVP boundary must not be silently expanded.
  - Target service boundaries must not be described as implemented runtime without traceable evidence.
  - ADR conformance checks must link the canonical ADR template; they must not duplicate it as a competing template.
-->

---

## 1. Purpose

This document defines the Sprint 0 AI review-agent model for HomeEdge AI Platform.

The purpose is to catch documentation, governance, source-of-truth, evidence, architecture, ADR-conformance, stakeholder, and claim-control regressions before they reach review or Done.

The agents in this policy are advisory reviewers. They identify problems and produce findings, but they do not make final project decisions.

Core rule:

```text
Review agents detect and report.
The Project Owner decides Ready, ADR status, and Done.
GitHub defines technical truth.
Jira tracks workflow and evidence.
Confluence reports and orients stakeholders.
```

This policy is governance-only. It does not introduce firmware, backend, mobile, cloud, runtime automation, CI enforcement, production readiness, safety-critical guarantees, commercial readiness, or security-grade certification.

---

## 2. Scope

Included:

- advisory review-agent roles for Sprint 0;
- purpose, inputs, checks, outputs, severity guidance, and decision limits for each agent;
- document-type routing and mandatory ADR conformance when an ADR is detected;
- review severity model;
- review output and summary templates;
- blocking conditions;
- source-of-truth protection rules;
- `[UNVALIDATED]` claim-control rules;
- evidence and review-provenance checks;
- DOC-REGRESSION detection support;
- Governance Lane Review Gate alignment.

Excluded:

- autonomous approval authority;
- autonomous Jira transitions or issue closure;
- autonomous ADR approval, rejection, acceptance, or supersession;
- runtime or CI implementation of review agents;
- automatic correction of reviewed documents;
- firmware, backend, mobile, or cloud implementation;
- production-ready, safety-critical, commercial-ready, or security-grade claims.

---

## 3. Source-of-Truth Boundaries

| Surface | Authority | Review-agent rule |
|---|---|---|
| GitHub | Technical truth, code, versioned technical documents, policies, ADRs, risks, PR evidence | Use GitHub as the canonical source when technical content conflicts. |
| Jira | Backlog, task state, workflow state, review state, blockers, evidence links | Use Jira to check status, scope, acceptance criteria, blockers, approval evidence, and evidence links. |
| Confluence | Stakeholder hub, stakeholder reports, stakeholder forms, stakeholder navigation | Check stakeholder clarity, but do not treat Confluence as technical truth. |

If GitHub and Jira or Confluence diverge on technical content, GitHub wins until a reviewed GitHub source-of-truth change updates the project truth.

Confluence stakeholder reports may summarize project state, but they must link back to GitHub/Jira evidence and preserve `[UNVALIDATED]` markers for unproven claims.

---

## 4. Review Agents Overview

| Agent | Main responsibility | Typical blocking concern |
|---|---|---|
| Source of Truth Guardian | Protect GitHub/Jira/Confluence boundaries | Technical truth moved out of GitHub or duplicated incorrectly. |
| Architecture Regression Reviewer | Protect MVP and architecture maturity boundaries | Target architecture described as implemented runtime or silent MVP expansion. |
| Event Contract Reviewer | Protect event/schema/streaming claims | Event contracts or Kafka/event streaming declared implemented without evidence. |
| Security & Privacy Reviewer | Protect security, privacy, and sensitive-data boundaries | Safety/security/privacy claim or data exposure without evidence. |
| Testing & Evidence Reviewer | Protect evidence quality before review/Done | Missing PR, test, log, review, or evidence link. |
| Stakeholder Clarity Reviewer | Protect stakeholder readability and non-duplication | Stakeholder material contradicts canonical truth or weakens `[UNVALIDATED]`. |
| ADR Conformance Reviewer | Protect ADR structure, writing quality, review provenance, and approval boundaries | Missing/ambiguous decision, template non-conformance, unsupported review claims, or unauthorized ADR status. |

---

## 5. Review Agent Definitions

### 5.1 Source of Truth Guardian

**Purpose**  
Prevent parallel truths across GitHub, Jira, and Confluence.

**Inputs**

- `docs/governance/source-of-truth.md`
- `docs/governance/shift-left-governance-baseline.md`
- `docs/governance/governance-lane-review-gate.md` when reviewing governance-lane movement
- README semantic index
- relevant Jira issue description, status, blockers, comments, and evidence links
- relevant Confluence stakeholder summary or report, when applicable

**Primary checks**

- GitHub remains the technical source of truth.
- Jira tracks backlog, task state, workflow state, review state, blockers, and evidence links.
- Confluence reports, orients, hosts forms, and provides stakeholder navigation.
- Long-form technical documents are not duplicated into Confluence as competing truth.
- Canonical paths are not changed without updating semantic links.
- `[UNVALIDATED]` is preserved for unproven claims.

**Output**  
Findings about divergence, missing links, missing markers, or source-of-truth misuse.

**Decision limits**  
This agent cannot approve source-of-truth changes, approve ADRs, close issues, declare Ready or Done, or transition Jira tickets.

---

### 5.2 Architecture Regression Reviewer

**Purpose**  
Prevent silent MVP expansion and target/runtime confusion.

**Inputs**

- `docs/product/product-vision.md`
- `docs/governance/source-of-truth.md`
- README architecture and MVP sections
- issue description and PR diff, when applicable

**Primary checks**

- The only MVP firmware node remains `firmware/room-env-node/`.
- The MVP node remains a generic room/door node.
- MVP includes temperature, humidity, local non-identifying presence detection, and door open/closed state.
- Raw audio, person tracking, behavioral history, person identification, window sensor scope, 220V automation, direct ESP32 Kafka producer, commercial claims, safety-critical claims, and production/security-grade certification claims remain outside MVP unless a later reviewed source-of-truth change says otherwise.
- Target service boundaries are not described as implemented runtime without evidence.

**Output**  
Findings about scope expansion, architectural maturity overclaiming, or missing `[UNVALIDATED]` markers.

**Decision limits**  
This agent cannot approve architecture changes or redefine MVP scope.

---

### 5.3 Event Contract Reviewer

**Purpose**  
Prevent unsupported claims about event schemas, event contracts, producers, consumers, ingestion, Kafka, or event streaming.

**Inputs**

- README service-boundary sections
- `schemas/` when present
- `services/ingestion/` when present
- relevant architecture documents, ADRs, PR diffs, or issue descriptions

**Primary checks**

- Event contracts are not presented as stable or implemented without reviewed evidence.
- Backend-side event streaming remains `[UNVALIDATED]` until implementation and review evidence exist.
- Direct ESP32 Kafka publishing is not introduced into MVP.
- Schema, payload, producer, consumer, ingestion, or event-routing claims have traceable evidence.
- Placeholder directories are not treated as runtime proof.

**Output**  
Findings about contract maturity, missing schemas, unsupported streaming claims, or target/runtime confusion.

**Decision limits**  
This agent cannot approve event contracts or declare schemas stable.

---

### 5.4 Security & Privacy Reviewer

**Purpose**  
Prevent unsafe security, privacy, compliance, and stakeholder-facing claims.

**Inputs**

- Shift Left Impact block
- `docs/governance/source-of-truth.md`
- `docs/governance/stakeholder-transparency.md`
- relevant issue, PR, README, governance, product, or stakeholder text

**Primary checks**

- No production-ready, security-grade, safety-critical, commercial-ready, certified access-control, or alarm-grade claim appears without traceable evidence.
- Presence detection remains local and non-identifying inside MVP.
- Raw audio, person identification, individual tracking, behavioral history, and sensitive domestic data are not introduced silently.
- Stakeholder-facing content does not expose tokens, passwords, API keys, private network details, addresses, sensitive logs, private images/videos, raw audio, individual tracking, or behavioral history.
- Privacy-sensitive and security-sensitive claims remain `[UNVALIDATED]` when not proven.

**Output**  
Findings about security/privacy risk, misleading compliance posture, sensitive data exposure, or missing `[UNVALIDATED]` markers.

**Decision limits**  
This agent cannot certify security, approve privacy posture, or authorize safety/compliance claims.

---

### 5.5 Testing & Evidence Reviewer

**Purpose**  
Ensure claims and completion states are backed by traceable evidence.

**Inputs**

- Jira acceptance criteria and evidence links
- PRs, commits, diffs, tests, logs, screenshots, evidence files, review comments, and unresolved review threads
- Shift Left Impact block
- relevant source-of-truth documents
- `docs/governance/governance-lane-review-gate.md` when reviewing governance-lane movement

**Primary checks**

- Every completed claim has evidence.
- Missing evidence keeps the claim `[UNVALIDATED]`.
- Documentation-only changes have reviewable diff evidence.
- Implementation claims have implementation, test, log, runtime, or review evidence.
- Referenced evidence exists, is accessible, and supports the stated claim.
- Jira contains evidence links before movement toward Done.
- No unresolved blocking finding remains before closure.
- Governance-lane movement respects `docs/governance/governance-lane-review-gate.md`.

**Output**  
Findings about missing evidence, weak evidence, broken provenance, incomplete acceptance criteria, or premature Done risk.

**Decision limits**  
This agent cannot declare acceptance criteria satisfied, close the task, or transition the issue.

---

### 5.6 Stakeholder Clarity Reviewer

**Purpose**  
Keep stakeholder-facing material readable, link-based, and aligned with canonical technical truth.

**Inputs**

- `docs/governance/stakeholder-transparency.md`
- `docs/governance/governance-lane-review-gate.md` when reviewing governance-lane stakeholder movement
- Confluence stakeholder hub/report, when applicable
- Jira issue summary, status, comments, blockers, and evidence links
- GitHub canonical documents linked by the stakeholder material

**Primary checks**

- Stakeholder-facing content is short, readable, and navigable.
- Confluence reports summarize and link; they do not redefine technical truth.
- Stakeholders can quickly find current phase, active task state, completed work, review state, blockers, risks, decisions, PR/document evidence, and `[UNVALIDATED]` claims.
- Technical depth remains in GitHub.
- Jira remains the tracking and evidence-link layer.
- Governance-lane stakeholder movement respects `docs/governance/governance-lane-review-gate.md`.

**Output**  
Findings about stakeholder confusion, duplicated technical documentation, missing links, missing evidence, or misleading maturity wording.

**Decision limits**  
This agent cannot approve stakeholder reports as final project truth or override GitHub source-of-truth documents.

---

### 5.7 ADR Conformance Reviewer

**Purpose**  
Verify that an Architecture Decision Record follows the canonical ADR model, contains one stable and human-readable decision, separates visible content from AI-only metadata, and uses traceable evidence and approval records.

**Mandatory inputs**

- the ADR target at an exact commit or branch ref;
- `docs/adr/template.md`;
- `docs/adr/README.md`;
- `docs/governance/documentation-strategy.md`;
- `docs/governance/source-of-truth.md`;
- `docs/risks/risk-model-baseline.md` when risks or treatments are referenced;
- the complete Jira issue, including status, acceptance criteria, comments, relationships, dependencies, and Project Owner decisions;
- the relevant PR diff, reviews, comments, unresolved threads, and cited evidence files.

**Primary checks**

| Check ID | Requirement |
|---|---|
| `ADR-CONF-01` | Detect and report the document type. Apply the ADR lens to ADR targets only. |
| `ADR-CONF-02` | Compare headings and section order directly with `docs/adr/template.md`. |
| `ADR-CONF-03` | Confirm every required template section is complete or explicitly records `None` where the template permits it. |
| `ADR-CONF-04` | Confirm one stable architectural decision per ADR; independently actionable decisions require separate ownership or ADRs. |
| `ADR-CONF-05` | Confirm the decision, scope, limitations, consequences, and remaining uncertainty are visible and understandable to human reviewers. |
| `ADR-CONF-06` | Confirm hidden metadata is limited to AI routing, canonical-path discovery, anti-regression constraints, forbidden-claim reminders, and surface-responsibility hints. Human-required truth must not exist only in metadata, and metadata must not become a competing decision record. |
| `ADR-CONF-07` | Confirm the ADR status is allowed and any `Accepted`, `Rejected`, or `Superseded` status has traceable Project Owner decision evidence. |
| `ADR-CONF-08` | Confirm alternatives are realistic, outcomes are explicit, and rationale is proportionate to the decision. |
| `ADR-CONF-09` | Confirm evidence links resolve to the cited artifacts, identify what each artifact supports, and do not treat missing or broken references as validated evidence. |
| `ADR-CONF-10` | Confirm unproven claims preserve `[UNVALIDATED]` and no unsupported maturity, reliability, security, safety, commercial, or certification claim is introduced. |
| `ADR-CONF-11` | Confirm ADR-to-risk and treatment links follow the canonical many-to-many model, including inverse Risk Record links when applicable; an ADR must not close or accept a risk by itself. |
| `ADR-CONF-12` | Confirm Review Notes are author/reviewer checklists, not independent review evidence by themselves. Generic `PASS` claims require reviewer identity, target ref, sources checked, observed evidence, and traceable review provenance. |
| `ADR-CONF-13` | Confirm the ADR does not silently expand the protected MVP boundary or introduce hidden downstream requirements. |

**Output**

ADR-oriented findings must include the common finding fields plus:

```text
Check ID:
Document type detected:
Target ref:
Observed evidence:
Related reviewer:
Review provenance:
```

A full ADR review summary must additionally report:

```text
Canonical template checked:
Template conformance:
Required sections complete:
One-decision rule:
Human readability:
AI metadata boundary:
Status and approval authority:
Evidence traceability:
Risk and treatment traceability:
[UNVALIDATED] preserved:
Review provenance:
Unresolved findings:
```

**ADR-specific severity guidance**

- `BLOCKER`: missing or ambiguous architectural decision; multiple independent decisions mixed in one ADR; unauthorized ADR status; source-of-truth contradiction; silent MVP expansion.
- `MAJOR`: canonical template or required order not followed; mandatory section missing; important truth hidden only in metadata; metadata duplicates a material decision surface; evidence provenance missing or broken; unsupported Review Notes or generic `PASS` claims; risk traceability materially incomplete.
- `MINOR`: unclear wording, weak navigation, incomplete caption, or non-blocking formatting inconsistency.
- `NOTE`: optional improvement without correctness, authority, or traceability impact.

**Decision limits**

This agent cannot:

- approve, accept, reject, or supersede an ADR;
- change ADR status;
- approve architecture or redefine MVP scope;
- accept, defer, reject, or close a risk;
- declare acceptance criteria satisfied;
- approve a PR, declare Ready or Done, close an issue, or transition Jira.

---

## 6. Reviewer Ownership and Anti-Duplication

The first reviewer listed below is the primary owner of the finding. Other reviewers should reference the same finding or check ID instead of repeating it as a separate finding.

| Dimension | Primary reviewer | ADR Conformance Reviewer boundary |
|---|---|---|
| ADR structure, required order, section completion | ADR Conformance Reviewer | Full ownership. |
| One stable decision | ADR Conformance Reviewer | Full ownership; Architecture Reviewer evaluates architectural correctness and scope. |
| Human readability inside the ADR | ADR Conformance Reviewer | Decision, limits, consequences, and uncertainty must be visible. |
| External stakeholder readability | Stakeholder Clarity Reviewer | ADR reviewer may cross-reference, not duplicate. |
| Evidence existence and technical sufficiency | Testing & Evidence Reviewer | ADR reviewer verifies traceability and references the evidence finding. |
| ADR status and approval record | ADR Conformance Reviewer | Verifies coherence; Project Owner remains the decision authority. |
| Source-of-truth divergence | Source of Truth Guardian | ADR reviewer may detect and cross-reference. |
| Architecture or MVP regression | Architecture Regression Reviewer | ADR reviewer applies `ADR-CONF-13` and cross-references architectural analysis. |
| Security/privacy correctness | Security & Privacy Reviewer | ADR reviewer checks claim/evidence boundaries, not certification. |
| Risk acceptance or treatment effectiveness | Risk governance and Project Owner | ADR reviewer checks links only; it never accepts risk. |

Every finding must identify its primary reviewer and may identify one or more related reviewers.

---

## 7. Severity Model

| Severity | Blocking | Meaning | Examples |
|---|---|---|---|
| `BLOCKER` | Yes | Contradicts protected source-of-truth, silently expands MVP, removes `[UNVALIDATED]` without evidence, creates premature Done risk, or invalidates the core ADR decision/authority boundary. | Direct ESP32 Kafka producer in MVP; production-ready claim; missing evidence for Done; unauthorized `Accepted` ADR; multiple unrelated decisions in one ADR. |
| `MAJOR` | Usually yes | Creates serious ambiguity, divergence, misleading maturity, missing evidence, approval-authority risk, or material ADR non-conformance. | Target service boundary described as implemented; mandatory ADR section absent; evidence link broken; Review Notes presented as independent review evidence. |
| `MINOR` | No by default | Correctable issue that does not invalidate the review by itself. | Weak link label, incomplete recommendation, unclear but non-misleading wording. |
| `NOTE` | No | Suggestion or observation with no blocking impact. | Improve navigation wording; add optional cross-link. |

Mapping to DOC-REGRESSION severity:

```text
BLOCKER = S0 DOC-REGRESSION
MAJOR   = S1 or review-blocking S2 DOC-REGRESSION
MINOR   = non-blocking S2 or S3 DOC-REGRESSION
NOTE    = non-regression observation
```

---

## 8. Blocking Rules

A review must block the requested movement when any of these conditions exists:

- unresolved `BLOCKER` finding;
- unresolved `MAJOR` finding that affects source-of-truth, MVP scope, claim maturity, stakeholder correctness, evidence, ADR conformance, risk traceability, or approval authority;
- missing Jira evidence link for a completed governance or implementation claim;
- unproven claim without `[UNVALIDATED]`;
- GitHub technical truth moved into Jira or Confluence as a competing source;
- Confluence duplicates long-form technical documentation instead of linking and summarizing;
- production-ready, safety-critical, commercial-ready, certification, or security-grade claim without evidence;
- missing or ambiguous ADR decision;
- multiple independently actionable architectural decisions in one ADR;
- ADR status inconsistent with the allowed model or missing Project Owner decision evidence;
- required ADR section absent or material evidence provenance missing;
- Project Owner approval missing for a Ready or Done decision.

Governance-lane movement toward Review, Stakeholder Review, or Done must additionally use `docs/governance/governance-lane-review-gate.md`.

Review agents may mark a finding as blocking, but they cannot perform the final workflow decision.

Fixture findings do not authorize fixture correction. They demonstrate whether the reviewer detects the expected condition.

---

## 9. Review Output Template

Use this format in PR reviews, Jira comments, review notes, or local review summaries:

```text
AI REVIEW FINDING

Check ID: <role-specific ID or N/A>
Reviewer:
Primary reviewer:
Related reviewer:
Severity: BLOCKER / MAJOR / MINOR / NOTE
Blocking: yes / no
Affected source:
Target ref:
Canonical source checked:
Observed evidence:
Finding:
Risk:
Recommendation:
Evidence:
Review provenance:
Required Project Owner decision: yes / no
```

Findings must cite observed evidence. A severity label or generic `PASS` statement without target ref, sources checked, and traceable evidence is not a valid review finding.

---

## 10. Review Summary Template

Use this format when summarizing a full review pass:

```text
AI REVIEW SUMMARY

Issue:
Scope reviewed:
Target refs:
Document types detected:
Sources checked:
Reviewers applied:
Review provenance:
Findings:
- BLOCKER:
- MAJOR:
- MINOR:
- NOTE:

Unresolved blocking items:
[UNVALIDATED] claims preserved: yes / no
Source-of-truth boundaries preserved: yes / no
Evidence links checked: yes / no
Project Owner action required:
```

When an ADR is detected, append the ADR summary fields defined in section 5.7. When no ADR is detected, report:

```text
ADR conformance lens: not applicable — no ADR target detected.
```

---

## 11. Agent Decision Limits

Review agents may:

- read Jira, GitHub, and Confluence content;
- compare issue descriptions, PR diffs, repository documents, stakeholder summaries, evidence links, and review threads;
- identify regressions, missing evidence, unsupported claims, and ADR-conformance defects;
- classify findings by severity;
- recommend corrections;
- produce review summaries.

Review agents must not:

- approve, accept, reject, supersede, or change the status of ADRs;
- approve architecture changes;
- declare issues Ready or Done;
- close issues;
- transition Jira issues without explicit Project Owner instruction;
- accept, defer, reject, or close risks;
- remove `[UNVALIDATED]` without traceable evidence;
- introduce production-ready, safety-critical, commercial-ready, certification, or security-grade claims;
- treat placeholder directories, self-completed checklists, generic `PASS` statements, or missing artifacts as proof;
- duplicate long-form GitHub technical documentation into Confluence.

Allowed final phrasing:

```text
No blocking findings detected by this review pass. Project Owner review is still required.
```

Forbidden final phrasing:

```text
Approved.
Done.
Ready authorized.
ADR accepted.
Risk accepted.
Production-ready.
Security-grade.
```

---

## 12. `[UNVALIDATED]` Handling

`[UNVALIDATED]` must remain attached to any claim that is not yet proven by implementation, tests, logs, reviewed PRs, runtime evidence, approved ADRs, or explicit Project Owner approval recorded in the proper source.

Use `[UNVALIDATED]` for:

- target architecture not implemented yet;
- service boundaries without runtime evidence;
- firmware behavior not tested yet;
- backend integrations not implemented yet;
- AI insight claims without validation;
- reliability or performance claims without measurement;
- security or privacy claims without specific validation;
- stakeholder-facing claims that may be read as already proven.

Removing `[UNVALIDATED]` is a review-sensitive action and must be backed by traceable evidence.

---

## 13. DOC-REGRESSION Handling

When an agent detects a DOC-REGRESSION, it must report:

```text
DOC-REGRESSION

Severity: BLOCKER / MAJOR / MINOR / NOTE
Location:
Canonical source violated:
Problem:
Expected correction:
Evidence:
```

A DOC-REGRESSION is blocking when it contradicts protected MVP scope, source-of-truth hierarchy, claim maturity, stakeholder correctness, evidence requirements, ADR conformance, or approval authority.

---

## 14. Acceptance Criteria

This policy satisfies IHAP-34, extends it through IHAP-54, and stays aligned with IHAP-35 when:

- the policy exists as a canonical GitHub document;
- README links this policy from the semantic index;
- each review agent has purpose, inputs, checks, outputs, and decision limits;
- the ADR Conformance Reviewer is registered in the role inventory;
- ADR reviews compare directly with the canonical ADR index, template, Documentation Strategy, Jira issue, PR diff, reviews, and evidence;
- ADR checks cover structure, required order, completeness, one-decision rule, human readability, metadata boundary, status authority, evidence, `[UNVALIDATED]`, risk traceability, review provenance, and MVP scope;
- the universal review flow applies the ADR lens when an ADR is detected and reports not applicable otherwise;
- reviewer ownership prevents duplicate findings;
- generic `PASS` statements and self-completed Review Notes are not treated as independent evidence;
- severity levels `BLOCKER`, `MAJOR`, `MINOR`, and `NOTE` are defined with ADR-specific examples;
- the review output includes finding, severity, affected source, recommendation, observed evidence, provenance, and blocking status;
- agents are explicitly advisory and non-decision-making;
- agents cannot approve ADRs, close issues, declare Ready or Done, or transition Jira issues without explicit Project Owner instruction;
- Governance Lane Review Gate is referenced for governance-lane movement toward Review, Stakeholder Review, or Done;
- GitHub/Jira/Confluence source-of-truth boundaries are preserved;
- `[UNVALIDATED]` handling is explicit;
- no firmware, backend, mobile, cloud, runtime, CI enforcement, production-ready, safety-critical, commercial-ready, or security-grade claim is introduced.

---

## 15. Related Documents

This policy must stay aligned with:

- `README.md`;
- `docs/governance/source-of-truth.md`;
- `docs/governance/documentation-strategy.md`;
- `docs/governance/shift-left-governance-baseline.md`;
- `docs/governance/governance-lane-review-gate.md`;
- `docs/governance/stakeholder-transparency.md`;
- `docs/governance/ai-review-agent-playbook.md`;
- `docs/adr/README.md`;
- `docs/adr/template.md`;
- `docs/risks/risk-model-baseline.md`;
- `docs/product/product-vision.md`.

If this policy conflicts with `docs/governance/source-of-truth.md`, the source-of-truth policy wins until a reviewed GitHub change resolves the conflict.

---

## 16. Practical Rule

```text
Review agents report evidence-backed findings.
The ADR Conformance Reviewer checks the record; it does not make the decision.
Project Owner decides ADR status and transitions.
GitHub defines technical truth.
Jira tracks evidence and state.
Confluence reports and orients.
```
