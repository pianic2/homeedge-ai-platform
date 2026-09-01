# IHAP-46 — Final Review Summary

**Issue:** [IHAP-46](https://niccolopiazzi01.atlassian.net/browse/IHAP-46)  
**PR:** [#25](https://github.com/pianic2/homeedge-ai-platform/pull/25)  
**Decision state:** evidence complete; Project Owner decision pending; ADR-0005 remains `Proposed`

## Recommendation

**SELECT LD2410C** as the reference MVP presence-sensing technology for a
current, local, non-identifying boolean presence state only.

PIR is rejected for this decision because its motion/change-based sensing is a
weaker fit for the required stationary-presence state. No presence sensor is
rejected because it removes the current-presence capability stated by the
Product Vision.

The selection explicitly does not create an occupancy guarantee. The owned
specimen exceeded the original operational onset threshold in 3/10 strict
entries and exceeded the original operational release threshold in both clean
corrected exit repetitions. Those limitations are accepted as product telemetry
behavior to be communicated and constrained, not hidden by rewritten gates.

## Cross-functional gate

| Review gate | Result | Basis |
|---|---|---|
| Hardware Compatibility | **PASS** | Receive-only UART at 256000 baud is physically demonstrated with ESP32-C3 and stable enough for the decision; final pins and protection remain IHAP-50 |
| Testing & Evidence | **PASS** | Lean automated evidence covers moving, stationary, empty, release and adjacent-path behavior; raw reanalysis is coherent and failures remain recorded |
| Security & Privacy | **PASS** | Only a current boolean presence state may cross the product boundary; identity, tracking, person count, behavioral history and persistent raw radar are prohibited |
| Architecture Regression | **PASS** | The proposal is consistent with current `main`, ADR-0001 through ADR-0004, Product Vision and R-004; downstream ownership is preserved |
| Event Contract | **PASS** | Authorized semantics are limited to `presence_detected: true \| false`, or a strictly equivalent current local state |
| Cost Governance | **PASS** | Owned inventory, tested specimen, reference quantity, acquired cost and dated replacement snapshot are distinguished; definitive BOM propagation remains IHAP-17 |
| Source of Truth | **PASS** | GitHub contains the technical decision, evidence and tooling; Jira contains workflow/gate state; Confluence is intentionally deferred until acceptance and merge |
| Stakeholder Clarity | **PASS** | The recommendation, limitations, prohibited claims and handoffs are explicit and readable without implying acceptance |

```text
BLOCKER = 0
MAJOR = 0
MINOR = 0
```

## Intentional notes and handoffs

1. Strict entry met the original 2,000 ms operational-onset threshold in 7/10
   repetitions; all ten entries were eventually detected.
2. The two accepted corrected exit repetitions cleared at 18,506 ms and
   18,754 ms from `START NOW`, failing the original 10,000 ms operational gate.
3. Physical results apply to one owned `HLK-LD2410C V1.1` specimen and the
   documented setups. The open-door adjacent test used an approximately 3 m
   external corridor path, door open about 30 degrees, with the threshold never
   crossed.
4. Seller, revision, lot and replacement-module equivalence remain
   `[UNVALIDATED]`; current sourcing and definitive BOM ownership remain IHAP-17.
5. Quantitative power remains IHAP-49, final wiring/interconnect remains IHAP-50,
   and placement/range/mounting/enclosure remain IHAP-51.

## Product and event boundary

The maximum authorized product output is semantically equivalent to:

```json
{
  "presence_detected": true
}
```

The module may expose richer fields internally. They are limited to temporary,
controlled local diagnostics and are not authorized as product events, stored
history or stakeholder evidence. Coordinates, trajectories, identity, person
count, behavioral profiles, persistent raw radar, individual room history,
occupancy guarantees, alarm, antifurto, intrusion-detection, safety and
protection claims remain prohibited.

## Project Owner decision gate

The evidence supports the proposed selection. ADR-0005 must remain `Proposed`,
PR #25 must remain unmerged, and Jira must remain `In corso` until the Project
Owner explicitly accepts or rejects the decision.
