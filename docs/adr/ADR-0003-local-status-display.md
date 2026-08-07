# ADR-0003 — Local Status Display

**Status:** Proposed  
**Date:** 2026-08-07  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Jira:** [IHAP-53](https://niccolopiazzi01.atlassian.net/browse/IHAP-53)  
**PR:** Pending  
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
  - Do not assume seller/lot identity from PCB similarity alone.
  - Do not mark this ADR Accepted until Project Owner review after physical validation.
-->

---

## 1. Context

The HomeEdge reference MVP room/door node already requires temperature, humidity, local non-identifying presence and door open/closed telemetry. ADR-0001 deliberately left local-display scope to IHAP-53 and did not reserve GPIO specifically for a display.

The Project Owner has now made a readable local UI an explicit MVP function. The display is intended to provide a compact local status and maintenance console without replacing serial diagnostics or backend observability.

The owned candidate is a blue 0.96-inch-class four-pin OLED board physically observed with:

- `GND`, `VCC`, `SCL`, `SDA` pins;
- `0x3C` / `0x3D` address-selection marking;
- PCB marking `GME12864-11-12-13 V3.22`.

A primary manufacturer page for the `GME12864-11/12/13` family identifies it as a 0.96-inch, 128×64, monochrome, four-pin I2C module using SSD1306, with the `-12` variant blue. The same source states a 3.3–5 V module supply range. The observed blue specimen and family marking are consistent with `GME12864-12`, but exact provenance, PCB revision correspondence and electrical behavior of the owned specimen remain `[UNVALIDATED]` until physical validation.

The architectural problem is therefore not whether a local display exists, but how to define a minimal, reproducible display contract that does not couple the MVP to one anonymous seller board.

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

This section becomes authoritative only when this ADR is accepted by the Project Owner.

### 2.1 Reference display profile

The minimum reference profile is:

| Property | Requirement |
|---|---|
| Size | 0.96-inch-class; small mechanical variance may be accepted by IHAP-51 |
| Resolution | 128×64 required |
| Display type | Monochrome OLED |
| Orientation | Landscape |
| Interface | I2C |
| Functional pins | `VCC`, `GND`, `SCL`, `SDA` |
| Logic | Must operate directly with 3.3 V-safe ESP32-C3 I2C logic; no external level shifter in the reference profile |
| Supply target | Must support direct use from the node 3.3 V domain; exact module behavior requires validation |
| Address | `0x3C` reference; `0x3D` permitted when intentionally configured and collision-free |
| Controller | One tested controller profile; SSD1306 is the current candidate based on primary family documentation, exact owned-specimen correspondence pending validation |
| Replacement | Multi-vendor equivalents allowed when they satisfy this profile and require at most a small controller/configuration abstraction |
| Input | Read-only; no buttons or touch controls |
| Dedicated status LED | Not required |

### 2.2 Healthy UI

When the node is healthy, one fixed dashboard is shown. It contains:

- human-readable room label;
- temperature;
- humidity;
- `Presence: DETECTED` or `Presence: CLEAR`;
- `Door: OPEN` or `Door: CLOSED`.

Wi-Fi state is omitted when healthy. Firmware version and technical node ID are not permanently displayed.

### 2.3 Boot UI

During boot the display shows:

```text
HomeEdge
Starting...
```

Boot progress may show short subsystem steps such as Wi-Fi, sensor and backend initialization. The display must not expose credentials, SSID or other private network metadata.

### 2.4 Health-state model

The local UI uses three operational states:

- `HEALTHY`: normal dashboard;
- `DEGRADED`: dashboard remains visible with a compact diagnostic indication when useful data is still available;
- `ERROR`: diagnostic screen replaces the dashboard when a core MVP function cannot provide meaningful service or when a fatal local state requires maintenance attention.

Loss of Wi-Fi or backend reachability does not erase locally available sensor data. Display failure itself must not stop sensing or telemetry; it is recorded through serial/backend diagnostics when those channels remain available.

### 2.5 Error-code contract

Display-visible diagnostic codes use a stable three-digit model inspired by familiar full-stack HTTP status-code families but are HomeEdge device diagnostic codes, not HTTP responses.

```text
4xy = local/configuration/component fault
5xy = runtime/network/backend/dependency fault

x = subsystem family
y = progressive error within that subsystem
```

Subsystem tens digit:

| x | Subsystem |
|---:|---|
| 0 | backend/server dependency |
| 1 | Wi-Fi/network connectivity |
| 2 | local display |
| 3 | environmental sensing |
| 4 | presence sensing |
| 5 | door-state sensing |
| 6 | node configuration / boot contract |
| 7–9 | reserved |

Initial MVP catalogue:

| Code | State | Human message | Meaning |
|---:|---|---|---|
| `400` | ERROR | `Invalid node configuration` | Required local configuration is missing or invalid |
| `420` | DEGRADED | `Display initialization failed` | Display could not initialize; node must continue sensing/telemetry if otherwise healthy |
| `421` | DEGRADED | `Display update failed` | Display update path failed after initialization |
| `430` | DEGRADED | `Environment sensor unavailable` | Temperature/humidity source unavailable |
| `440` | DEGRADED | `Presence sensor unavailable` | Local presence source unavailable |
| `450` | DEGRADED | `Door sensor unavailable` | Door-state source unavailable |
| `500` | DEGRADED | `Backend unavailable` | Node has local operation but backend/server cannot be reached |
| `501` | DEGRADED | `Backend request timeout` | Backend request exceeded configured timeout |
| `510` | DEGRADED | `Wi-Fi unavailable` | Node is not currently connected to Wi-Fi |
| `511` | DEGRADED | `Network configuration failed` | Network configuration cannot establish usable connectivity |
| `560` | ERROR | `Boot contract failed` | Required boot invariant failed and meaningful MVP operation cannot start |

The firmware implementation task may extend the catalogue only while preserving the family/subsystem/progressive-number model and documenting new codes. Detailed stack traces and verbose logs remain serial/backend-only.

### 2.6 Update policy

The display should update when a relevant state changes rather than rendering continuously at high frequency.

- environmental values: approximately every 5 seconds unless a later firmware task justifies a different cadence;
- presence, door, degraded and error transitions: update promptly on state change;
- no UI history is stored or displayed by this decision.

### 2.7 Privacy boundary

The local display may show current room-level telemetry only.

It must not show:

- person identity;
- individual tracking;
- behavioral or occupancy history;
- SSID;
- credentials;
- security/alarm state;
- access-control or antifurto semantics.

IP address may appear only on a maintenance/diagnostic screen when needed and must not be part of the normal dashboard.

### 2.8 I2C and GPIO direction

The display uses the ESP32-C3 I2C capability already preserved by ADR-0001. Final pins remain owned by IHAP-50.

- Standard DHT11 profile remains a separate single-data-line interface.
- When the BME280 profile is used, display and BME280 should share one I2C bus unless physical evidence shows a conflict.
- BME280 accepted evidence uses address `0x76`, which does not collide with display candidates `0x3C` / `0x3D`.
- Pull-up interaction, bus capacitance, wiring and final recovery behavior remain part of IHAP-50 validation.

### 2.9 Power, enclosure and BOM handoff

- IHAP-49 owns current measurement, sleep behavior and quantitative power-budget impact.
- The display remains an MVP requirement even if it increases consumption; IHAP-49 adapts the power subsystem rather than silently removing the display.
- IHAP-51 owns aperture, alignment, protection, mounting, serviceability and final mechanical tolerance.
- IHAP-17 must record both the generic profile and a tested reference implementation after acceptance, using a dated replacement-price snapshot even though the current specimen is already owned.

---

## 3. Alternatives Considered

| Alternative | Outcome | Reason |
|---|---|---|
| No local display | Rejected | Does not satisfy the Project Owner requirement for a readable user/maintenance status console |
| Status LED only | Rejected | Too little information for the requested local console; no dedicated status LED is required |
| 0.96-inch 128×64 monochrome I2C OLED | Proposed | Proportionate information density, simple four-wire interface, compact enclosure footprint and broad replacement availability |
| Larger OLED/TFT/touch UI | Rejected | Adds GPIO, firmware, enclosure, power and UI complexity without an MVP need |
| SPI 0.96-inch display | Rejected for reference profile | Adds wiring/GPIO pressure without a demonstrated advantage for the selected UI |

---

## 4. Consequences

### Positive

- Gives users immediate room telemetry without requiring a backend client.
- Gives maintainers compact local boot and diagnostic information.
- Uses a deterministic 128×64 UI contract that can be tested and reproduced.
- Preserves serial/backend diagnostics for detailed engineering information.
- Can share I2C with the BME280 specialized environmental profile.
- Avoids a separate mandatory status LED.

### Negative / Trade-offs

- Adds display-driver, rendering, font, state-machine and I2C failure-handling work to future firmware tasks.
- Adds a recurring BOM line, enclosure aperture and assembly requirement to every reference node.
- Adds power consumption that must be quantified by IHAP-49.
- A 0.96-inch display has limited text area, so diagnostic messages must remain compact.
- Generic 0.96-inch modules are not interchangeable solely by appearance; controller, electrical and mechanical compatibility must be checked.

### Neutral / Operational

- Final GPIO assignment remains open under IHAP-50.
- Final sleep policy remains open under IHAP-49.
- Final enclosure aperture dimensions remain open under IHAP-51.
- The exact owned specimen remains conditional until IHAP-53 physical validation passes.
- Product Vision remains unchanged while this ADR is Proposed and is updated only after Project Owner acceptance.

---

## 5. Related Risks and Treatments

| Risk | Treatment | Effect | Remaining exposure |
|---|---|---|---|
| None | None | Leaves current risk records unchanged | Display power, mechanical durability and exact generic-module compatibility remain validation/follow-up concerns rather than accepted risk closures |

---

## 6. Follow-up Work

| Item | Tracking |
|---|---|
| Run the owned-specimen validation protocol and record evidence | IHAP-53 |
| Freeze final I2C pins, wiring, pull-up interaction and bus-recovery strategy | IHAP-50 |
| Measure display current and decide runtime/sleep power policy | IHAP-49 |
| Define aperture, mounting, orientation and protection | IHAP-51 |
| Add generic profile + tested reference SKU/source + dated replacement cost | IHAP-17 |
| Implement display driver, healthy/degraded/error UI and error catalogue | Future firmware implementation task |
| Add `local status display` to canonical Product Vision after ADR acceptance | IHAP-53 post-acceptance propagation |
| Add the accepted display disposition to the IHAP-43 final hardware matrix | IHAP-43 |

---

## 7. Evidence Links

| Evidence | Link |
|---|---|
| Jira issue | [IHAP-53](https://niccolopiazzi01.atlassian.net/browse/IHAP-53) |
| Pull request | Pending |
| Validation/evidence package | [`docs/evidence/IHAP-53/README.md`](../evidence/IHAP-53/README.md) |
| Product boundary | [`docs/product/product-vision.md`](../product/product-vision.md) |
| Compute ADR | [`ADR-0001`](ADR-0001-mvp-edge-compute-platform.md) |
| Environmental profiles | [`ADR-0002`](ADR-0002-environmental-sensor-profiles.md) |
| Manufacturer family page | https://goldenmorninglcd.com/oled-display-module/0.96-inch-128x64-ssd1306-gme12864-11/ |
| Current Italian replacement-price snapshot example | https://www.homotix.it/vendita/display-oled/display-oled-128x64-096-pollici-i2c-bianco |
| Related Risk Records | None |
| Related treatments | None |

---

## 8. Review Notes

```text
[x] One stable architectural decision only.
[x] ADR necessity is explicit and follows the Project Owner product decision.
[x] No-display and status-LED alternatives remain visible.
[x] The owned specimen is not treated as universally reproducible before validation.
[x] Error-code semantics are explicit and stable.
[x] Display failure does not become a sensing/telemetry single point of failure.
[x] Final pinout, power, enclosure and BOM responsibilities remain in their owning tasks.
[x] Source-of-truth boundaries are preserved.
[x] Product Vision is not modified while this ADR is Proposed.
[x] [UNVALIDATED] is preserved on unproven owned-specimen claims.
[x] No production-ready, commercial-ready, security-grade, certified, safety-critical, alarm-grade, antifurto, access-control or protection claim is introduced.
[ ] Physical validation completed.
[ ] Specialist reviews completed.
[ ] Project Owner PR review completed.
[ ] Project Owner acceptance recorded before status becomes Accepted.
```
