# ADR-0002 — Environmental Sensor Profiles

**Status:** Accepted  
**Date:** 2026-07-16  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Jira:** IHAP-45  
**PR:** Pending  
**Supersedes:** None  
**Superseded by:** None

<!--
AI_AGENT_METADATA:
  document_type: architecture_decision_record
  status_allowed_values:
    - Proposed
    - Accepted
    - Superseded
    - Rejected
  approval_authority: project_owner
  source_of_truth: github_versioned_repository_documentation
  jira_role: evidence_links_only
  confluence_role: stakeholder_navigation_only
  related_risk_model: docs/risks/risk-model-baseline.md
  unvalidated_claim_marker: "[UNVALIDATED]"

HIDDEN_ANTI_REGRESSION_RULES:
  - Keep one stable architectural decision per ADR.
  - Preserve DHT11 as the default standard-indoor profile unless a later accepted ADR supersedes this decision.
  - Preserve BME280 as the precision and extended-environment profile, not merely an error fallback.
  - Do not promote DHT22 without new reviewed evidence and a superseding decision.
  - Do not claim absolute accuracy from IHAP45-RUN-01 because no independent reference instrument was used.
  - Pressure remains outside the MVP measurement contract.
  - This ADR does not close or accept R-011.
-->

---

## 1. Context

The MVP room node needs temperature and relative-humidity observations for ordinary domestic monitoring. The default room use case involves slow, gradual environmental changes and does not require calibrated, medical, safety-critical or precision-control measurements.

IHAP-45 compared the owned DHT11, DHT22 and BME280 specimens in parallel through a controlled 115-minute protocol. The accepted run produced 5,771 structured records, completed every required phase, retained one boot and one successful BME280 probe, and published only aggregate evidence.

The owned specimens showed:

- DHT11: 1,923 valid samples from 1,923 records and no observed communication errors;
- DHT22: 1,922 valid samples from 1,924 records and two `NO_RESPONSE` errors;
- BME280: 1,924 valid samples from 1,924 records and no observed communication errors;
- BME280 identity: I2C address `0x76`, chip ID `0x60`, humidity supported;
- materially different responses under extreme temperature and humidity phases;
- no independent reference observations, so absolute accuracy remains `[UNVALIDATED]`.

The Project Owner selected the lowest-cost adequate component for standard indoor nodes while retaining a more capable profile for demanding environments.

---

## 2. Decision

```text
We will use DHT11 as the default environmental sensor profile for standard indoor room nodes.

We will use BME280 as the precision and extended-environment profile for outdoor nodes, tightly controlled rooms, or environments expected to experience rapid, wide or operationally significant temperature and humidity changes.

DHT22 is not selected for either profile.
```

The profiles are defined as follows:

| Profile | Sensor | Intended use |
|---|---|---|
| Standard indoor | DHT11 | Cost-optimized domestic room monitoring with slow, gradual changes and broad comfort-oriented thresholds |
| Precision / extended environment | BME280 | Outdoor nodes, controlled rooms, wider environmental excursions, tighter operational thresholds or finer observation requirements |

BME280 may also serve as a procurement fallback when DHT11 is unavailable and the increased unit cost is acceptable, but its primary architectural role is the specialized profile rather than failure recovery.

The MVP measurement contract remains temperature and relative humidity only. Pressure is not added by this decision.

---

## 3. Alternatives Considered

| Alternative | Outcome | Reason |
|---|---|---|
| DHT11 for every environmental node | Partially accepted | Adequate and lowest-cost for standard indoor nodes, but not preferred for extended or precision-oriented environments |
| DHT22 for standard or precision nodes | Rejected | Higher cost than DHT11, two observed `NO_RESPONSE` errors, and no decisive benefit sufficient to establish a distinct profile |
| BME280 for every node | Rejected | Strong functional results and wider observed response, but unnecessary cost and capability for ordinary indoor rooms with slow changes |
| DHT11 default plus BME280 specialized profile | Accepted | Matches observed specimen behavior, MVP room requirements and cost proportionality while preserving a higher-capability option |

---

## 4. Consequences

### Positive

- The standard room-node BOM uses the lowest-cost tested sensor that completed the run without observed errors.
- Ordinary indoor nodes avoid overengineering where temperature and humidity normally change slowly.
- BME280 remains available for outdoor, precision-oriented or tightly controlled environments.
- DHT22 is removed from the supported profile matrix, reducing unnecessary variants.
- The decision is backed by reproducible firmware, protocol, validators and sanitized aggregate evidence.

### Negative / Trade-offs

- DHT11 has coarser resolution and showed meaningful disagreement with BME280, particularly for relative humidity.
- Standard room automations must use broad thresholds, filtering and hysteresis rather than tight control bands.
- Absolute accuracy of all three owned specimens remains `[UNVALIDATED]` because no independent reference instrument was used.
- Maintaining two profiles introduces conditional BOM, firmware-driver and wiring paths.
- BME280 costs more than DHT11 and requires I2C rather than a single proprietary data line.

### Neutral / Operational

- Results apply to the tested owned specimens and executed setup, not every unit or seller lot.
- Final wiring remains owned by IHAP-50.
- Final enclosure and placement remain owned by IHAP-51.
- Quantitative current draw, rail capacity and autonomy remain owned by IHAP-49.
- Placement and enclosure bias remain documented under R-011 and are not resolved by this ADR.

---

## 5. Related Risks and Treatments

| Risk | Treatment | Effect | Remaining exposure |
|---|---|---|---|
| [R-011](../risks/records/R-011-environmental-sensor-placement-bias.md) | RT-R011-01 | Partially mitigates | Profile selection reduces inappropriate sensor use, but placement, airflow, thermal coupling, enclosure geometry and condensation can still bias measurements; effectiveness is pending physical enclosure evidence |

---

## 6. Follow-up Work

| Item | Tracking |
|---|---|
| Apply the selected profile to the definitive MVP BOM and cost model | IHAP-17 / IHAP-43 follow-up |
| Validate quantitative power and supply suitability | IHAP-49 |
| Freeze final signal and power wiring for both profiles | IHAP-50 |
| Define and verify placement and enclosure rules | IHAP-51 / RT-R011-01 |
| Update production firmware only when the corresponding node implementation task is approved | Future implementation task |

---

## 7. Evidence Links

| Evidence | Link |
|---|---|
| Jira issue | [IHAP-45](https://niccolopiazzi01.atlassian.net/browse/IHAP-45) |
| Pull request | Pending |
| Evidence index | [IHAP-45 evidence](../evidence/IHAP-45/README.md) |
| Environmental summary | [Markdown](../evidence/IHAP-45/summaries/environmental-IHAP45-RUN-01.summary.md) |
| Machine-readable aggregate summary | [JSON](../evidence/IHAP-45/summaries/environmental-IHAP45-RUN-01.summary.json) |
| Aggregate-only visual report | [HTML](../evidence/IHAP-45/summaries/environmental-IHAP45-RUN-01.summary.html) |
| Validation harness | [IHAP-45 harness](../../tools/hardware-validation/ihap-45-environmental-sensors/README.md) |
| Related Risk Records | [R-011](../risks/records/R-011-environmental-sensor-placement-bias.md) |
| Related treatments | RT-R011-01 |
| Related ADRs | [ADR-0001](ADR-0001-mvp-edge-compute-platform.md) |

---

## 8. Review Notes

```text
[x] One stable architectural decision only.
[x] ADR necessity is explicit; this records the stable environmental-sensor profile decision.
[x] Related risks and treatments are listed when relevant.
[x] Effect and remaining exposure are explicit for every linked risk.
[x] Linked Risk Records contain inverse links.
[x] The ADR is not treated as risk acceptance or closure evidence.
[x] Source-of-truth boundaries are preserved.
[x] MVP boundary is not silently expanded.
[x] [UNVALIDATED] is preserved on absolute accuracy and population-wide behavior.
[x] No pressure field or measurement is added to the MVP contract.
[x] No production-ready, commercial-ready, security-grade, certified, safety-critical, alarm-grade, antifurto, access-control, intrusion-detection, or protection claim is introduced.
[x] Project Owner decision was explicitly recorded before status became Accepted.
```
