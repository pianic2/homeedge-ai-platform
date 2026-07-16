# Risk Assessment — Environmental Sensor Placement and Enclosure Measurement Bias

**Risk ID:** R-011  
**Risk status:** Newly Identified  
**Current assessment date:** 2026-07-16  
**Last reviewed:** 2026-07-16  
**Next review:** IHAP-51 enclosure/placement validation or material sensor-profile change  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Jira:** IHAP-45 / IHAP-51  
**PR:** [PR #28](https://github.com/pianic2/homeedge-ai-platform/pull/28)  
**Owner decision:** Pending

<!--
AI_AGENT_METADATA:
  document_type: risk_record
  source_of_truth: github_versioned_repository_documentation
  jira_role: operational_coordination_only
  confluence_role: stakeholder_summary_and_navigation_only
  risk_acceptance_authority: project_owner
  related_adr: docs/adr/ADR-0002-environmental-sensor-profiles.md
  unvalidated_claim_marker: "[UNVALIDATED]"

HIDDEN_ANTI_REGRESSION_RULES:
  - Do not treat ADR-0002 as risk acceptance or closure evidence.
  - Preserve the distinction between intrinsic sensor behavior and placement/enclosure effects.
  - Do not claim calibrated or absolute accuracy without independent reference evidence.
  - Do not mark RT-R011-01 Implemented or Verified before IHAP-51 evidence exists.
-->

---

## 1. Risk Statement

```text
There is a risk that temperature and relative-humidity observations are biased, delayed or made incomparable because sensor placement, airflow, thermal coupling, enclosure geometry, condensation or proximity to heat and moisture sources can affect the local microclimate seen by the sensor.
```

The comparative IHAP-45 run showed materially different responses among co-located owned specimens, especially under extreme humidity and temperature phases. Without an independent reference and a final enclosure, the portion attributable to intrinsic sensor behavior versus placement and packaging remains `[UNVALIDATED]`.

---

## 2. Source Trigger and Scope

**Source trigger:** IHAP45-RUN-01 observed wider and differently shaped responses across DHT11, DHT22 and BME280 during controlled transitions. The final node enclosure and installation location are not yet defined.

**In scope:**

- room-node and extended-environment sensor placement;
- enclosure vents, thermal isolation and airflow exposure;
- distance from the ESP32-C3, regulators, walls, windows, doors and environmental sources;
- condensation avoidance;
- comparability between repeated installations;
- validation of DHT11 and BME280 profile-specific placement.

**Out of scope:**

- calibrated laboratory certification;
- quantitative power and regulator characterization;
- pressure sensing;
- medical, safety-critical or industrial process-control claims;
- universal behavior of every DHT11 or BME280 unit.

This record does not introduce firmware, backend, mobile, cloud, runtime, security enforcement, or unsupported maturity claims.

---

## 3. Affected Assets and Trust Boundary

| Area | Detail |
|---|---|
| Assets | Environmental readings, room-state interpretation, automation thresholds, evidence comparability |
| Trust boundary | Physical interface between ambient environment, sensor element, breakout PCB and node enclosure |
| Data involved | Temperature and relative-humidity observations only |
| Stakeholder surface | Room comfort displays, automation decisions, test reports and architecture claims |

---

## 4. Current Assessment

| Field | Value | Rationale |
|---|---|---|
| Category | Technical / Claims | Physical placement can change readings and can lead to overclaiming sensor quality or room state |
| Likelihood | Medium | Final placement and enclosure are not yet verified, and the comparative run showed meaningful inter-sensor divergence |
| Impact | Medium | Biased readings may trigger poor automations or misleading stakeholder conclusions, but the MVP is not safety-critical |
| Residual risk | Pending Evidence | Treatment effectiveness depends on IHAP-51 physical validation |
| Evidence gap | `[UNVALIDATED]` | No final enclosure, installation profile or independent calibrated reference has been tested |
| Decision state | Pending Project Owner | No residual-risk acceptance, deferral or rejection has been made |

---

## 5. Existing Controls

| Control | Evidence | Coverage | Limitation |
|---|---|---|---|
| Comparative co-location protocol | `docs/evidence/IHAP-45/` | Partial | Temporary test arrangement, not final enclosure or installation |
| Explicit relative-only claim boundary | `docs/evidence/IHAP-45/summaries/environmental-IHAP45-RUN-01.summary.md` | Partial | Prevents absolute-accuracy overclaim but does not reduce physical bias |
| Profile-specific ADR | `docs/adr/ADR-0002-environmental-sensor-profiles.md` | Partial | Selects appropriate sensor classes but does not define placement |
| Pressure excluded from scope | IHAP-45 firmware and publication policy | Partial | Prevents scope expansion only |

Planned actions belong in Risk Treatments, not here.

---

## 6. Risk Treatment Summary

| Treatment ID | Title | Strategy | Lifecycle status | Jira | ADR | Last review |
|---|---|---|---|---|---|---|
| RT-R011-01 | Define and verify environmental sensor placement profile | Mitigate | Proposed | IHAP-51 / IHAP-50 coordination | ADR-0002 | 2026-07-16 |

---

## 7. Risk Treatments

### RT-R011-01 — Define and verify environmental sensor placement profile

**Strategy:** Mitigate  
**Lifecycle status:** Proposed  
**Treatment owner:** Hardware and enclosure workstream  
**Jira coordination:** IHAP-51 with IHAP-50 wiring input  
**Related ADRs:** ADR-0002  
**Introduced:** 2026-07-16  
**Last reviewed:** 2026-07-16  
**Next review trigger:** Final enclosure prototype or material change to sensor profile, wiring length or mounting location

#### Rationale

A repeatable physical placement profile is required to keep readings representative of the intended ambient environment and comparable across nodes. The correct vent geometry, separation distance and installation constraints remain `[UNVALIDATED]` until tested with the actual enclosure and wiring.

#### Planned Controls or Actions

- define profile-specific mounting rules for DHT11 and BME280;
- separate the sensing element from ESP32-C3 and regulator heat where practical;
- define vent openings and airflow path without direct drafts;
- prohibit contact with walls, wet surfaces and condensation-prone areas;
- define minimum separation from heat, cold and moisture sources;
- document orientation and cable-length constraints;
- repeat stable-baseline and controlled-transition checks in the enclosure prototype;
- compare enclosure readings with an independent reference when available;
- document threshold and hysteresis guidance for the DHT11 standard profile.

These are planned actions until implementation evidence exists.

#### Scope Coverage

| Risk cause or consequence | Coverage | Rationale |
|---|---|---|
| ESP32/regulator self-heating | Partial | Placement and thermal separation can reduce but not necessarily eliminate coupling |
| Restricted or directed airflow | Partial | Vent and mounting rules reduce local stagnation and drafts |
| Condensation and moisture contact | Partial | Installation rules and stop conditions reduce exposure but cannot control all environments |
| Inconsistent installation across nodes | Partial | A documented profile improves repeatability; field compliance remains to be verified |
| Absolute sensor accuracy | None | Requires independent reference and potentially calibration, outside this treatment's guarantee |

#### Remaining Exposure

Unit-to-unit variation, sensor aging, contamination, unusual room airflow and absence of calibrated reference remain. Outdoor installations may need additional weather shielding and validation beyond the standard room enclosure.

#### Source and Evidence Register

| ID | Source | Source type | Supports | Version / applicability | Verification | Checked on | Limitations |
|---|---|---|---|---|---|---|---|
| SRC-01 | `docs/evidence/IHAP-45/summaries/environmental-IHAP45-RUN-01.summary.json` | Internal evidence | Observed inter-sensor differences and transition behavior | Owned specimens, executed setup | Verified | 2026-07-16 | Relative comparison only; no independent reference |
| SRC-02 | `tools/hardware-validation/ihap-45-environmental-sensors/README.md` | Project docs | Co-location and safety constraints used for the comparative run | IHAP-45 harness | Verified | 2026-07-16 | Not a final enclosure specification |
| SRC-03 | `docs/adr/ADR-0002-environmental-sensor-profiles.md` | Project decision | Profile selection and remaining placement dependency | ADR-0002 | Verified | 2026-07-16 | Does not verify treatment effectiveness |

#### Implementation and Verification Evidence

| Evidence ID | Evidence | Evidence class | Expected result | Actual result | Status | Date |
|---|---|---|---|---|---|---|
| EV-01 | IHAP-51 enclosure and placement validation | Verification | Stable, repeatable readings without unacceptable self-heating, airflow or condensation bias | Not executed | `[UNVALIDATED]` | 2026-07-16 |

`Implemented` requires implementation evidence. `Verified` requires verification evidence and an effectiveness review.

#### Treatment Effectiveness Review

**Review date:** Pending  
**Evidence reviewed:** EV-01 pending  
**Effectiveness:** Pending Evidence  
**Likelihood after treatment:** Pending Evidence  
**Impact after treatment:** Pending Evidence  
**Residual risk:** Pending Evidence  
**Remaining exposure:** Unit variation, aging, contamination, field installation and absolute accuracy  
**Project Owner decision required:** Yes

This review does not accept, defer, or reject residual risk by itself.

---

## 8. Traceability

| Relationship | Link | Effect / Rule |
|---|---|---|
| Jira treatment task | IHAP-51 / IHAP-50 | Operational coordination only |
| Pull request | [PR #28](https://github.com/pianic2/homeedge-ai-platform/pull/28) | Adds risk record and proposed treatment; not verification evidence |
| Related ADR | `docs/adr/ADR-0002-environmental-sensor-profiles.md` | Partially mitigates inappropriate profile selection; leaves placement exposure unresolved |
| Related risks | None | Keep distinct from power, wiring and generic claim risks |
| Related policy or test | `docs/evidence/IHAP-45/`; `tools/hardware-validation/ihap-45-environmental-sensors/` | Comparative evidence and reproducible method |

---

## 9. Stakeholder Visibility

| Item | Rule | Rationale |
|---|---|---|
| Risk summary | Show | Physical measurement bias is relevant to decision quality |
| Treatment summary | Show | Planned placement verification is understandable and non-sensitive |
| Technical implementation | Link | Detailed enclosure and test evidence should remain in GitHub |
| Secrets, private topology, personal or domestic data | Block / Redact | None is required to communicate this risk |
| Maturity claim | Keep `[UNVALIDATED]` where evidence is missing | Final enclosure fitness and absolute accuracy are unproven |

Stakeholder-safe wording:

```text
Environmental readings can be affected by sensor placement and enclosure design. The project has selected sensor profiles, but final placement effectiveness remains to be verified with the enclosure prototype.
```

Confluence may summarize and link only. It must not duplicate this dossier.

---

## 10. Assessment History

| Date | Change | Treatment | Evidence | Decision |
|---|---|---|---|---|
| 2026-07-16 | Risk identified from IHAP-45 comparative evidence; treatment proposed | RT-R011-01 | SRC-01 through SRC-03 | Pending Project Owner residual-risk decision |

---

## 11. Review Notes

```text
[x] GitHub remains the canonical risk and treatment dossier.
[x] Jira coordinates work, status, blockers, and evidence links only.
[x] Confluence summarizes and links only.
[x] Existing controls are separated from planned actions.
[x] Every treatment has a stable RT-* ID.
[x] Sources identify the supported claim, verification state, date, and applicability.
[x] Implementation evidence and verification evidence are separate.
[x] Implemented is not treated as Verified.
[x] [UNVALIDATED] is preserved where proof is missing.
[x] Related Jira tasks and ADRs are linked in both directions when applicable.
[x] Review triggers and orphan indicators were checked.
[x] The ADR exists because a stable sensor-profile decision was required, not automatically because this risk exists.
[x] No production-ready, commercial-ready, security-grade, certified, safety-critical, alarm-grade, antifurto, access-control, intrusion-detection, or protection claim was introduced.
[x] No residual-risk acceptance, deferral, rejection or closure is claimed.
```

---

## 12. Practical Rule

```text
Select the appropriate sensor profile in ADR-0002.
Verify the physical placement and enclosure in IHAP-51.
Keep raw telemetry local and publish reviewed aggregate evidence only.
Leave residual-risk decisions to the Project Owner.
```
