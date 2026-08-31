# ADR-0004 — Local Status Display

**Status:** Proposed  
**Date:** 2026-08-07  
**Last evidence review:** 2026-08-31  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Jira:** [IHAP-53](https://niccolopiazzi01.atlassian.net/browse/IHAP-53)  
**PR:** [#31](https://github.com/pianic2/homeedge-ai-platform/pull/31)  
**Supersedes:** None  
**Superseded by:** None

<!--
AI_AGENT_METADATA:
  document_type: architecture_decision_record
  decision_scope: local_status_display
  issue: IHAP-53
  parent_issue: IHAP-43
  status: Proposed
  approval_authority: project_owner
  approval_recorded: false
  source_of_truth: github_versioned_repository_documentation
  jira_role: workflow_state_blockers_and_evidence_links
  confluence_role: stakeholder_summary_and_navigation_only
  reference_profile: 0.96-inch-class_128x64_monochrome_i2c
  owned_specimen_marking: GME12864-11-12-13_V3.22
  owned_specimen_status: physical_validation_pass_pending_project_owner_acceptance
  dedicated_status_led_required: false
  final_pinout_owner: IHAP-50
  quantitative_power_owner: IHAP-49
  enclosure_owner: IHAP-51
  bom_owner: IHAP-17
  product_vision_update_after_acceptance: true
  runtime_changes_allowed: false
  unvalidated_claim_marker: "[UNVALIDATED]"

HIDDEN_ANTI_REGRESSION_RULES:
  - Keep one stable decision: the reference MVP includes a compact local status/debug display profile.
  - Do not turn the display into a full terminal or interactive application UI.
  - Do not add buttons, touch input, a dedicated status LED, history, identity or behavioral data.
  - Keep sensing and telemetry operational when the display itself fails.
  - Keep final GPIO/pin assignment in IHAP-50 and quantitative power validation in IHAP-49.
  - Keep enclosure mechanics in IHAP-51 and definitive BOM accounting in IHAP-17.
  - Treat the owned specimen as physically validated only within the tested 3.3 V / I2C / SSD1306-profile conditions.
  - Do not claim the physical controller die, seller provenance, lot reproducibility, current consumption or final product wiring from IHAP-53 evidence.
  - Do not mark this ADR Accepted until explicit Project Owner acceptance after evidence and review.
-->

---

## 1. Context

The HomeEdge reference MVP room/door node already requires temperature, humidity, local non-identifying presence and door open/closed telemetry. ADR-0001 deliberately left local-display scope to IHAP-53 and did not reserve GPIO specifically for a display.

The Project Owner has made a readable local UI an explicit MVP function. It must provide a compact local status and maintenance console without replacing serial diagnostics or backend observability.

The owned blue 0.96-inch-class four-pin OLED is physically observed with:

- `GND`, `VCC`, `SCL`, `SDA` pins;
- `0x3C` / `0x3D` address-selection marking;
- PCB marking `GME12864-11-12-13 V3.22`.

GoldenMorning documents the `GME12864-11/12/13` family as 0.96-inch, 128×64, monochrome, four-pin I2C, SSD1306, with the `-12` variant blue and a 3.3–5 V module supply range.

Physical run `IHAP53-DISPLAY-01` subsequently demonstrated, for the owned specimen under the documented validation wiring:

- I2C response at `0x3C` and no response at `0x3D`;
- successful use of the SSD1306 command/data profile used by the harness;
- correct full-on, full-off, checkerboard and text-card rendering by operator observation;
- repeated updates beyond 3600 seconds without an invalidating I2C failure, brownout, unexpected reset, freeze or visible corruption;
- successful rediscovery, reinitialization and rendering after one controlled ESP32-C3 reset;
- operation from the ESP32-C3 3.3 V validation supply.

This evidence validates functional compatibility of the tested specimen with the SSD1306 profile used by the harness. It does **not** independently identify the physical controller die or prove seller/lot provenance, onboard regulator/pull-up implementation, quantitative current, final product wiring or universal compatibility of all similarly marked boards.

---

## 2. Decision

```text
We will include one 0.96-inch-class, 128x64, monochrome I2C local status display
in the reference MVP room/door node.

The display will be a read-only compact status/debug console. It will not be a
full terminal, touch UI or interactive application surface.

The owned GME12864-11-12-13 V3.22 blue specimen has passed the IHAP-53 physical
validation under the documented 3.3 V / I2C test conditions and is the tested
reference candidate pending explicit Project Owner acceptance of this ADR.
```

This decision becomes authoritative only when this ADR is accepted by the Project Owner.

### 2.1 Reference display profile

| Property | Requirement / evidence boundary |
|---|---|
| Size | 0.96-inch-class; small mechanical variance may be accepted by IHAP-51 |
| Resolution | 128×64 required |
| Display type | Monochrome OLED |
| Orientation | Landscape |
| Interface | I2C |
| Functional pins | `VCC`, `GND`, `SCL`, `SDA` |
| Logic | Direct 3.3 V-safe ESP32-C3 I2C operation in the reference profile; tested specimen passed without an external level shifter |
| Supply target | Direct operation from node 3.3 V domain; tested specimen passed at 3.3 V |
| Address | `0x3C` reference; tested specimen validated at `0x3C`; `0x3D` permitted for equivalent modules when intentionally configured and collision-free |
| Controller compatibility | SSD1306 command/data profile is functionally validated for the tested specimen; exact physical controller identity is not independently proven |
| Replacement | Multi-vendor equivalents allowed when they satisfy the profile and require at most a small controller/configuration abstraction |
| Input | Read-only; no buttons or touch controls |
| Dedicated status LED | Not required |

### 2.2 Healthy UI

When healthy, one fixed dashboard shows:

- human-readable room label;
- temperature;
- humidity;
- `Presence: DETECTED` or `Presence: CLEAR`;
- `Door: OPEN` or `Door: CLOSED`.

Healthy Wi-Fi state is omitted. Firmware version and technical node ID are not permanently displayed.

### 2.3 Boot UI

Boot begins with:

```text
HomeEdge
Starting...
```

Short subsystem progress steps may be displayed for Wi-Fi, sensors and backend initialization. Credentials, SSID and other private network metadata must not be shown.

### 2.4 Health-state model

The UI has three states:

- `HEALTHY`: normal dashboard;
- `DEGRADED`: available telemetry remains visible with a compact diagnostic indication;
- `ERROR`: a diagnostic screen replaces the dashboard when meaningful MVP operation cannot continue.

Loss of Wi-Fi or backend reachability does not erase locally available sensor data. A display failure must not stop sensing or telemetry.

### 2.5 Error-code contract

Display-visible diagnostic codes are HomeEdge device codes inspired by familiar full-stack HTTP status families. They are **not HTTP response status codes**.

```text
4xy = local/configuration/component fault
5xy = runtime/network/backend/dependency fault

x = subsystem family
y = progressive error within that subsystem
```

The tens digit is stable by subsystem:

| x | Subsystem family |
|---:|---|
| 0 | platform / service boundary |
| 1 | Wi-Fi / network connectivity |
| 2 | local display |
| 3 | environmental sensing |
| 4 | presence sensing |
| 5 | door-state sensing |
| 6 | node configuration / boot lifecycle |
| 7–9 | reserved |

The `0` subsystem intentionally represents the platform/service boundary: in the 4xx family it is a generic local-platform fallback, while in the 5xx family it covers the backend/server dependency boundary. This preserves the Project Owner requirement that `500` means backend/server unavailable while keeping the tens digit meaningful.

Initial MVP catalogue:

| Code | State | Human message | Meaning |
|---:|---|---|---|
| `400` | ERROR | `Local node fault` | Generic local-platform fault when no more specific 4xy code applies |
| `420` | DEGRADED | `Display initialization failed` | Display could not initialize; sensing/telemetry must continue if otherwise healthy |
| `421` | DEGRADED | `Display update failed` | Display update path failed after initialization |
| `430` | DEGRADED | `Environment sensor unavailable` | Temperature/humidity source unavailable |
| `440` | DEGRADED | `Presence sensor unavailable` | Local presence source unavailable |
| `450` | DEGRADED | `Door sensor unavailable` | Door-state source unavailable |
| `460` | ERROR | `Invalid node configuration` | Required local configuration is missing or invalid |
| `500` | DEGRADED | `Backend unavailable` | Node is operational locally but the backend/server cannot be reached |
| `501` | DEGRADED | `Backend request timeout` | Backend request exceeded the configured timeout |
| `510` | DEGRADED | `Wi-Fi unavailable` | Node is not currently connected to Wi-Fi |
| `511` | DEGRADED | `Network configuration failed` | Network configuration cannot establish usable connectivity |
| `560` | ERROR | `Boot contract failed` | Required boot invariant failed and meaningful MVP operation cannot start |

Future firmware work may extend the catalogue only while preserving the 4xy/5xy, subsystem-digit and progressive-unit model and documenting every new code. Detailed logs remain serial/backend-only.

### 2.6 Update policy

- environmental values: approximately every 5 seconds unless later firmware evidence justifies another cadence;
- presence, door, degraded and error transitions: prompt update on state change;
- no history is stored or displayed by this decision.

### 2.7 Privacy boundary

The display may show current room-level telemetry only. It must not show person identity, individual tracking, behavioral/occupancy history, SSID, credentials, security/alarm state, access-control or antifurto semantics.

IP address may appear only on a maintenance/diagnostic screen when needed and must not be part of the normal dashboard.

### 2.8 I2C and GPIO direction

The display uses the ESP32-C3 I2C capability already preserved by ADR-0001. Final pins remain owned by IHAP-50.

- Standard DHT11 remains a separate single-data-line interface.
- When BME280 is used, display and BME280 should share one I2C bus unless physical evidence shows a conflict.
- BME280 accepted evidence uses `0x76`, which does not collide with display `0x3C` / permitted `0x3D` candidates.
- Pull-up interaction, bus capacitance, final wiring and bus-recovery behavior remain IHAP-50 work.

The IHAP-53 validation wiring (`SDA=GPIO5`, `SCL=GPIO6`) is evidence-fixture wiring only and is not the final product pinout.

### 2.9 Power, enclosure and BOM handoff

- IHAP-49 owns current measurement, sleep behavior and quantitative power-budget impact.
- The display remains an MVP requirement if this ADR is accepted; IHAP-49 must adapt the power subsystem rather than silently remove it.
- IHAP-51 owns aperture, alignment, protection, mounting, serviceability and final mechanical tolerance.
- IHAP-17 must record the generic profile, tested reference implementation and dated replacement price after acceptance, even though the current specimen is already owned.

---

## 3. Alternatives Considered

| Alternative | Outcome | Reason |
|---|---|---|
| No local display | Rejected by functional direction | Does not satisfy the explicit readable user/maintenance UI requirement |
| Status LED only | Rejected by functional direction | Insufficient information density; no dedicated status LED is required |
| 0.96-inch 128×64 monochrome I2C OLED | Proposed | Proportionate information density, compact footprint, simple four-wire interface and successful physical validation of the owned specimen |
| Larger OLED/TFT/touch UI | Rejected | Adds firmware, GPIO, enclosure, power and UI complexity without an MVP need |
| SPI 0.96-inch display | Rejected for reference profile | Adds wiring/GPIO pressure without a demonstrated benefit |

---

## 4. Consequences

### Positive

- Immediate local telemetry for the user.
- Compact boot/error information for maintenance.
- Deterministic 128×64 UI contract.
- Tested specimen has evidence for 3.3 V operation, `0x3C`, SSD1306-profile rendering, one-hour functional stability and reboot reinitialization.
- Serial/backend remain available for detailed diagnostics.
- I2C can be shared with the BME280 profile subject to IHAP-50 final bus validation.
- No separate mandatory status LED.

### Negative / Trade-offs

- Adds driver, rendering, font, state-machine and failure-handling work to future firmware.
- Adds a recurring BOM line and enclosure aperture to every reference node.
- Adds power consumption to be quantified by IHAP-49.
- Limited screen area requires compact messages.
- Generic 0.96-inch modules are not interchangeable by appearance alone.

### Neutral / Operational

- Final GPIO assignment: IHAP-50.
- Final sleep/power policy: IHAP-49.
- Final aperture/mechanical tolerance: IHAP-51.
- Physical validation of the owned specimen is complete; architectural acceptance remains pending explicit Project Owner approval.
- Product Vision remains unchanged while this ADR is `Proposed`.

---

## 5. Related Risks and Treatments

| Risk | Treatment | Effect | Remaining exposure |
|---|---|---|---|
| None | None | Leaves current risk records unchanged | Display power, mechanical durability, final bus integration and exact replacement compatibility remain follow-up concerns; no risk is closed by this ADR |

---

## 6. Follow-up Work

| Item | Tracking |
|---|---|
| Physical validation of owned specimen | IHAP-53 — completed, `IHAP53-DISPLAY-01` PASS |
| Final Project Owner acceptance of this decision | IHAP-53 |
| Freeze I2C pins, wiring, pull-up interaction and bus-recovery strategy | IHAP-50 |
| Measure display current and decide sleep/power policy | IHAP-49 |
| Define aperture, mounting, orientation and protection | IHAP-51 |
| Add generic profile + tested reference + dated replacement cost | IHAP-17 after acceptance |
| Implement display driver and healthy/degraded/error UI | Future firmware implementation task |
| Add `local status display` to Product Vision | IHAP-53 only after ADR acceptance |
| Add accepted display disposition to final hardware matrix | IHAP-43 after acceptance |

---

## 7. Evidence Links

| Evidence | Link |
|---|---|
| Jira issue | [IHAP-53](https://niccolopiazzi01.atlassian.net/browse/IHAP-53) |
| Pull request | [PR #31](https://github.com/pianic2/homeedge-ai-platform/pull/31) |
| Validation/evidence runbook | [`docs/evidence/IHAP-53/README.md`](../evidence/IHAP-53/README.md) |
| Published run record | [`IHAP53-DISPLAY-01/run-record.md`](../evidence/IHAP-53/IHAP53-DISPLAY-01/run-record.md) |
| Front text-card photograph | [`photo-front-text-card.png`](../evidence/IHAP-53/IHAP53-DISPLAY-01/photo-front-text-card.png) |
| Rear PCB photograph | [`photo-rear-marking.png`](../evidence/IHAP-53/IHAP53-DISPLAY-01/photo-rear-marking.png) |
| Annotated wiring photograph | [`photo-wiring-annotated.png`](../evidence/IHAP-53/IHAP53-DISPLAY-01/photo-wiring-annotated.png) |
| Replacement sourcing snapshot | [`docs/evidence/IHAP-53/replacement-sourcing.md`](../evidence/IHAP-53/replacement-sourcing.md) |
| Final specialist review | [`docs/evidence/IHAP-53/final-review-summary.md`](../evidence/IHAP-53/final-review-summary.md) |
| Product boundary | [`docs/product/product-vision.md`](../product/product-vision.md) |
| Compute ADR | [`ADR-0001`](ADR-0001-mvp-edge-compute-platform.md) |
| Environmental profiles | [`ADR-0002`](ADR-0002-environmental-sensor-profiles.md) |
| GoldenMorning family source | https://goldenmorninglcd.com/oled-display-module/0.96-inch-128x64-ssd1306-gme12864-11/ |
| Solomon Systech SSD1306 source | https://www.solomon-systech.com/en/product/SSD1306 |
| Related Risk Records | None |
| Related treatments | None |

---

## 8. Review Notes

```text
[x] One stable architectural decision only.
[x] ADR necessity follows an explicit Project Owner product decision.
[x] No-display and status-LED alternatives remain visible.
[x] Physical validation evidence is linked and claim-bounded.
[x] Exact controller die identity is not inferred from SSD1306-profile compatibility.
[x] Error-code semantics and numbering structure are explicit.
[x] Display failure is not a sensing/telemetry single point of failure.
[x] Final pinout, power, enclosure and BOM responsibilities remain separated.
[x] Source-of-truth boundaries are preserved.
[x] Product Vision remains unchanged while this ADR is Proposed.
[x] [UNVALIDATED] is preserved on provenance, replacement, quantitative power and other unproven claims.
[x] No unsupported production, commercial, security, safety, alarm, access-control or certification claim is introduced.
[x] Physical validation completed.
[x] Specialist reviews completed after final remediation.
[ ] Project Owner PR review completed.
[ ] Project Owner acceptance recorded before status becomes Accepted.
```
