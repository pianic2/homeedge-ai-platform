# ADR-0003 — Local Status Display

**Status:** Proposed  
**Date:** 2026-08-07  
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
  owned_specimen_status: candidate_pending_physical_validation
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
  - Keep the owned specimen conditional until physical validation is complete.
  - Do not mark this ADR Accepted until Project Owner review after physical validation.
-->

---

## 1. Context

The HomeEdge reference MVP room/door node already requires temperature, humidity, local non-identifying presence and door open/closed telemetry. ADR-0001 deliberately left local-display scope to IHAP-53 and did not reserve GPIO specifically for a display.

The Project Owner has now made a readable local UI an explicit MVP function. It must provide a compact local status and maintenance console without replacing serial diagnostics or backend observability.

The owned candidate is a blue 0.96-inch-class four-pin OLED physically observed with:

- `GND`, `VCC`, `SCL`, `SDA` pins;
- `0x3C` / `0x3D` address-selection marking;
- PCB marking `GME12864-11-12-13 V3.22`.

GoldenMorning documents the `GME12864-11/12/13` family as 0.96-inch, 128×64, monochrome, four-pin I2C, SSD1306, with the `-12` variant blue and a 3.3–5 V module supply range. The observed specimen is consistent with that family, but exact provenance, PCB-revision correspondence and owned-specimen electrical behavior remain `[UNVALIDATED]` until physical validation.

---

## 2. Decision

```text
We will include one 0.96-inch-class, 128x64, monochrome I2C local status display
in the reference MVP room/door node.

The display will be a read-only compact status/debug console. It will not be a
full terminal, touch UI or interactive application surface.

The owned GME12864-11-12-13 V3.22 blue module is the candidate reference
implementation and remains conditional until physical validation is complete.
```

This decision becomes authoritative only when this ADR is accepted by the Project Owner.

### 2.1 Reference display profile

| Property | Requirement |
|---|---|
| Size | 0.96-inch-class; small mechanical variance may be accepted by IHAP-51 |
| Resolution | 128×64 required |
| Display type | Monochrome OLED |
| Orientation | Landscape |
| Interface | I2C |
| Functional pins | `VCC`, `GND`, `SCL`, `SDA` |
| Logic | Direct 3.3 V-safe ESP32-C3 I2C operation; no external level shifter in the reference profile |
| Supply target | Direct operation from the node 3.3 V domain; owned specimen still requires validation |
| Address | `0x3C` reference; `0x3D` permitted when intentionally configured and collision-free |
| Controller | SSD1306 is the current candidate; exact owned-specimen compatibility must be demonstrated physically |
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
- BME280 accepted evidence uses `0x76`, which does not collide with display candidates `0x3C` / `0x3D`.
- Pull-up interaction, bus capacitance, final wiring and bus-recovery behavior remain IHAP-50 work.

### 2.9 Power, enclosure and BOM handoff

- IHAP-49 owns current measurement, sleep behavior and quantitative power-budget impact.
- The display remains an MVP requirement even if it increases consumption; IHAP-49 must adapt the power subsystem rather than silently remove it.
- IHAP-51 owns aperture, alignment, protection, mounting, serviceability and final mechanical tolerance.
- IHAP-17 must record the generic profile, tested reference implementation and dated replacement price after acceptance, even though the current specimen is already owned.

---

## 3. Alternatives Considered

| Alternative | Outcome | Reason |
|---|---|---|
| No local display | Rejected | Does not satisfy the explicit readable user/maintenance UI requirement |
| Status LED only | Rejected | Insufficient information density; no dedicated status LED is required |
| 0.96-inch 128×64 monochrome I2C OLED | Proposed | Proportionate information density, compact footprint and simple four-wire interface |
| Larger OLED/TFT/touch UI | Rejected | Adds firmware, GPIO, enclosure, power and UI complexity without an MVP need |
| SPI 0.96-inch display | Rejected for reference profile | Adds wiring/GPIO pressure without a demonstrated benefit |

---

## 4. Consequences

### Positive

- Immediate local telemetry for the user.
- Compact boot/error information for maintenance.
- Deterministic 128×64 UI contract.
- Serial/backend remain available for detailed diagnostics.
- I2C can be shared with the BME280 profile.
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
- Exact owned specimen remains conditional until IHAP-53 physical validation passes.
- Product Vision remains unchanged while this ADR is Proposed.

---

## 5. Related Risks and Treatments

| Risk | Treatment | Effect | Remaining exposure |
|---|---|---|---|
| None | None | Leaves current risk records unchanged | Display power, mechanical durability and exact replacement compatibility remain follow-up concerns; no risk is closed by this ADR |

---

## 6. Follow-up Work

| Item | Tracking |
|---|---|
| Run the owned-specimen validation protocol and record evidence | IHAP-53 |
| Freeze I2C pins, wiring, pull-up interaction and bus-recovery strategy | IHAP-50 |
| Measure display current and decide sleep/power policy | IHAP-49 |
| Define aperture, mounting, orientation and protection | IHAP-51 |
| Add generic profile + tested reference + dated replacement cost | IHAP-17 |
| Implement display driver and healthy/degraded/error UI | Future firmware implementation task |
| Add `local status display` to Product Vision after ADR acceptance | IHAP-53 post-acceptance |
| Add accepted display disposition to final hardware matrix | IHAP-43 |

---

## 7. Evidence Links

| Evidence | Link |
|---|---|
| Jira issue | [IHAP-53](https://niccolopiazzi01.atlassian.net/browse/IHAP-53) |
| Pull request | [PR #31](https://github.com/pianic2/homeedge-ai-platform/pull/31) |
| Validation/evidence package | [`docs/evidence/IHAP-53/README.md`](../evidence/IHAP-53/README.md) |
| Replacement sourcing snapshot | [`docs/evidence/IHAP-53/replacement-sourcing.md`](../evidence/IHAP-53/replacement-sourcing.md) |
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
[x] Owned-specimen claims remain conditional before physical validation.
[x] Error-code semantics and numbering structure are explicit.
[x] Display failure is not a sensing/telemetry single point of failure.
[x] Final pinout, power, enclosure and BOM responsibilities remain separated.
[x] Source-of-truth boundaries are preserved.
[x] Product Vision is not modified while this ADR is Proposed.
[x] [UNVALIDATED] is preserved on unproven owned-specimen claims.
[x] No unsupported production, commercial, security, safety, alarm, access-control or certification claim is introduced.
[ ] Physical validation completed.
[ ] Specialist reviews completed.
[ ] Project Owner PR review completed.
[ ] Project Owner acceptance recorded before status becomes Accepted.
```
