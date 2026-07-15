# ADR-0001 — MVP Edge Compute Platform

**Status:** Accepted  
**Date:** 2026-07-14  
**Accepted by:** Project Owner  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Jira:** [IHAP-44](https://niccolopiazzi01.atlassian.net/browse/IHAP-44)  
**PR:** [#23](https://github.com/pianic2/homeedge-ai-platform/pull/23)  
**Supersedes:** None  
**Superseded by:** None

<!--
AI_AGENT_METADATA:
  document_type: architecture_decision_record
  decision_scope: mvp_edge_compute_platform
  issue: IHAP-44
  parent_issue: IHAP-43
  status: Accepted
  approval_authority: project_owner
  source_of_truth: github_versioned_repository_documentation
  jira_role: workflow_state_blockers_and_evidence_links
  confluence_role: optional_stakeholder_summary_and_navigation_only
  accepted_chip_family: esp32_c3
  purchased_board_status: preferred_conditional_candidate
  documented_control_and_fallback: esp32_c3_devkitc_02
  minimum_usable_flash_mb: 2
  preferred_flash_mb: 4
  minimum_application_gpio: 8
  local_display_mvp_status: pending_ihap_53
  raw_audio_allowed: false
  bluetooth_required: false
  quantitative_power_validation_issue: IHAP-49
  firmware_changes_allowed: false
  runtime_changes_allowed: false
  unvalidated_claim_marker: "[UNVALIDATED]"

HIDDEN_ANTI_REGRESSION_RULES:
  - The accepted decision is the ESP32-C3 family plus a board conformance profile, not unconditional approval of every board sold as SuperMini.
  - The purchased SuperMini-compatible board remains conditional until representative physical and functional qualification is complete.
  - ESP32-C3-DevKitC-02 remains the official control and fallback.
  - A photographed or owned peripheral is not an MVP requirement without a dedicated accepted decision and any required Product Vision update.
  - The photographed OLED is evidence for IHAP-53 only and is not made mandatory by this ADR.
  - I2C remains in the compute profile to preserve the BME280 environmental-sensor option, not to pre-approve a display.
  - Ownership and historical purchase price do not prove reproducibility.
  - Bluetooth availability does not make Bluetooth an MVP requirement.
  - Audio acquisition and audio-derived runtime behavior remain unauthorized.
  - Chip current figures must not be represented as measured board or complete-node consumption.
  - Quantitative rail, regulator and current validation belongs to IHAP-49.
  - No production-ready, commercial-ready, security-grade, certified, safety-critical, alarm-grade, antifurto, access-control, intrusion-detection, reliability or battery-autonomy claim is authorized.
-->

---

## 1. Decision Summary

The Project Owner accepts the following three-level compute strategy:

```text
MVP chip family: ESP32-C3.

Preferred compact implementation:
the purchased ESP32-C3 SuperMini-compatible board, conditionally qualified.

Official qualification control and fallback:
ESP32-C3-DevKitC-02.
```

The accepted board conformance profile requires:

- integrated 2.4 GHz Wi-Fi;
- officially maintained ESP-IDF C/C++ support;
- at least 2 MB usable flash, with 4 MB preferred;
- 3.3 V GPIO logic;
- repeatable flashing, console, reset and bootloader recovery;
- one I2C bus so IHAP-45 may still select an I2C environmental sensor;
- one full-duplex UART;
- one interrupt-capable digital input;
- one spare ADC-capable GPIO;
- at least eight safe application GPIO after flash, USB, boot, debug and onboard-load constraints;
- functional stability from PC USB without observed brownout or reset loops;
- an identifiable physical PCB revision for any exact reference board.

Acceptance of this ADR does **not**:

- make the photographed SuperMini a universally reproducible SKU;
- select an environmental sensor, presence sensor, door circuit, display, power subsystem, interconnect or enclosure;
- add a local display to the canonical MVP boundary.

The exact commercial SuperMini listing, seller and lot relationship remain `[UNVALIDATED]`.

---

## 2. Canonical Context and Scope

The canonical Product Vision defines one generic room/door node with:

- temperature telemetry;
- humidity telemetry;
- local non-identifying presence state;
- door open/closed telemetry;
- target HTTP/JSON transport `[UNVALIDATED]`;
- reproducible flashing and diagnostics.

A local display is **not currently listed as an MVP requirement** in the Product Vision. The photographed 0.96-inch OLED therefore remains physical evidence and an optional compatibility impact pending [IHAP-53 — Local Display Decision](https://niccolopiazzi01.atlassian.net/browse/IHAP-53).

The compute platform determines GPIO capacity, electrical boundaries, radio and debug surfaces, enclosure impact, replacement cost and firmware portability.

This ADR deliberately separates:

1. **chip family** — ESP32-C3 and ESP-IDF;
2. **board conformance profile** — the capabilities an acceptable board must provide;
3. **physical board revision** — the exact PCB qualified against that profile;
4. **attached component decisions** — environmental, presence, door, display, power and interconnect choices decided by their own tasks.

The commercial name **ESP32-C3 SuperMini** is not an Espressif board standard and may cover materially different boards.

### 2.1 Protected boundaries

This ADR does not:

- implement or change firmware;
- authorize Bluetooth as an MVP transport or provisioning requirement;
- authorize audio collection or processing;
- authorize a local OLED/LCD/display as an MVP feature;
- select the final environmental, presence, door, power, interconnect or enclosure subsystem;
- calculate battery autonomy;
- validate quantitative rail voltage, current draw or regulator capacity;
- approve IHAP-17 BOM lines;
- claim production, commercial, security, safety, alarm, access-control or certification maturity.

---

## 3. Evidence Register

### 3.1 Manufacturer and runtime evidence

| Evidence | State | Reliability | Remaining gap |
|---|---|---:|---|
| ESP32-C3 Wi-Fi, BLE, RISC-V CPU and maintained ESP-IDF support | Manufacturer declared | High | Does not prove a specific board |
| ESP32-C3 package and embedded-flash variants expose different GPIO totals | Manufacturer declared | High | Exact board part and routing remain board-specific |
| GPIO2, GPIO8 and GPIO9 are strapping pins | Manufacturer declared | High | External reset-state loads require verification |
| GPIO18/GPIO19 provide USB Serial/JTAG by default | Manufacturer declared | High | Exact board USB routing remains board-specific |
| One specimen identified as ESP32-C3 QFN32 rev. v0.4 with 4 MB XMC embedded flash and USB Serial/JTAG | Project Owner runtime log | High for one specimen | Does not identify seller or lot |
| The specimen flashed, verified, hard-reset and booted over PC USB | Project Owner runtime log | High for that execution | Representative peripheral stability remains to be exercised |
| Historical prototype used GPIO0–GPIO6 for several attached modules | Project Owner firmware/log | Medium-high | Not an accepted final wiring map or proof that every attached module is MVP |
| Physical flash was 4 MB while firmware was configured for 2 MB | Observed | High | Firmware partition correction is separate work |

Unique device identifiers from logs are intentionally not reproduced.

### 3.2 Physical ESP32-C3 SuperMini evidence received 2026-07-14

Project Owner front/back photographs establish the following for one physical specimen:

- PCB silkscreen: `ESP32 C3 Super Mini`;
- USB-C connector;
- dedicated `BOOT` and `RST` buttons;
- visible 40 MHz crystal;
- chip marking visually consistent with `ESP32-C3FH4`, aligned with independent 4 MB runtime detection;
- exposed supply pins: `5V`, `G`, `3.3`;
- exposed GPIO labels:
  - left side: `4`, `3`, `2`, `1`, `0`;
  - right side: `5`, `6`, `7`, `8`, `9`, `10`, `20`, `21`;
- PCB antenna area at the board edge;
- onboard indicator components whose exact GPIO mapping remains `[UNVALIDATED]`;
- regulator marking and complete power-path schematic remain `[UNVALIDATED]`.

This resolves the earlier catalog/prototype pinout discrepancy for the photographed specimen because GPIO1, GPIO2 and GPIO3 are physically exposed. It does not prove that every board sold under the SuperMini name has the same PCB.

### 3.3 Observed display-module evidence — no MVP authorization

The photographed display module provides:

- four pins marked `GND`, `VCC`, `SCL`, `SDA`;
- an I2C address-selection area marked `0x3C` / `0x3D`;
- PCB marking `GME12864-11-12-13 V3.22`.

This evidence confirms an I2C OLED-class form factor for the photographed unit only. It does **not** make the display part of the MVP and does not reserve an enclosure aperture or mandatory GPIO allocation.

The following remain `[UNVALIDATED]` and belong to IHAP-53/IHAP-49 if the display is later accepted:

- exact controller;
- allowed supply range;
- pull-up voltage and values;
- regulator or level shifting;
- current consumption;
- dimensions and mounting requirements;
- exact seller/listing and replacement profile.

### 3.4 Environmental-module evidence received 2026-07-14

The photographed blue sensor module is physically consistent with a DHT11-class breakout and exposes three pins marked `+`, `OUT`, `-`. The rear PCB includes an onboard resistor marked `512`.

The photograph does not by itself prove the module voltage range or complete circuit. Selection and electrical validation remain IHAP-45 work.

### 3.5 Cost and commercial identity

| Evidence | State |
|---|---|
| Three ESP32-C3 boards acquired for €8.75 total, €2.9167/unit | Historical E2 inventory evidence only |
| Two additional boards recorded at €0 acquisition cost | Inventory evidence only; not a replicable market price |
| Exact seller, order listing and lot relationship | `[UNVALIDATED]` |
| Current price and stock for an equivalent PCB revision | `[UNVALIDATED]` |
| Current normalized landed price for ESP32-C3-DevKitC-02 | `[UNVALIDATED]` |

Cost remains secondary to mandatory technical and reproducibility gates.

---

## 4. GPIO and Peripheral Budget

### 4.1 Canonical MVP functional budget

The compute profile must preserve both environmental-sensor alternatives until IHAP-45 decides between them.

| Function | Protocol | GPIO required | Boundary |
|---|---|---:|---|
| BME280 environmental option | I2C | 2 | Candidate pending IHAP-45 |
| DHT11/DHT22 environmental option | Digital | 1 | Alternative pending IHAP-45 |
| LD2410C telemetry and configuration | Full-duplex UART | 2 | Reserved until IHAP-46 narrows it |
| MC-38 door state | Digital interrupt | 1 | Circuit selected in IHAP-47 |
| Spare margin | Digital/ADC | 2 | At least one ADC-capable |
| MAX4466 impact | ADC | 1 optional | Does not authorize audio runtime |
| Local display impact | I2C | 0 or 2 additional | Optional; pending IHAP-53, not an MVP requirement |

Canonical core scenarios:

| Scenario | Functional GPIO | Required margin | Minimum usable GPIO |
|---|---:|---:|---:|
| BME280 + full-duplex LD2410C + MC-38 | 5 | 2 | 7 |
| DHT11/DHT22 + full-duplex LD2410C + MC-38 | 4 | 2 | 6 |

The accepted board profile remains **eight safe application GPIOs**. This provides one additional board-level margin above the worst canonical core scenario and improves replacement tolerance. The eighth pin is not a silent display reservation.

Optional display impact, to be decided only by IHAP-53:

- with BME280, a compatible display could share the already-required I2C bus and add no GPIO;
- with a DHT-class sensor, a display would add two I2C GPIO;
- either case would add power, firmware/UI, BOM, interconnect and enclosure impacts.

### 4.2 Photographed-board static pin budget

The photographed board exposes GPIO0–10 and GPIO20–21, excluding GPIO11–19 from application access except native USB routing.

A conservative candidate allocation excludes the three strapping pins and preserves UART0:

| Classification | GPIO |
|---|---|
| Candidate application set | `0`, `1`, `3`, `4`, `5`, `6`, `7`, `10` |
| Avoid for baseline application mapping | `2`, `8`, `9` — strapping constraints |
| Preserve for console/recovery when practical | `20`, `21` |
| Native USB | `18`, `19`, internally routed and not exposed as application pins |

This produces exactly eight physically exposed candidate application pins without depending on GPIO2, GPIO8, GPIO9, GPIO20 or GPIO21.

The static pin budget passes for the photographed revision. Final safety still requires representative boot/recovery testing and confirmation that no unidentified onboard circuit loads the candidate set.

### 4.3 Candidate mapping status

This is compatibility analysis, not the final wiring specification.

| GPIO | Candidate role | Status |
|---:|---|---|
| 0 | I2C SDA when an accepted component requires I2C | Physically exposed; prototype observed |
| 1 | I2C SCL when an accepted component requires I2C | Physically exposed; prototype observed |
| 2 | Historical DHT input | Avoid when possible; strapping pin |
| 3 | DHT option or spare | Physically exposed; prototype observed as LED output |
| 4 | ADC-capable spare | Physically exposed |
| 5 | LD2410C sensor TX → MCU RX | Physically exposed; prototype observed |
| 6 | MCU TX → LD2410C or door alternative | Physically exposed; prototype observed as door input |
| 7 | Door input or spare | Physically exposed; runtime validation pending |
| 8 | No baseline allocation | Strapping; onboard-load mapping `[UNVALIDATED]` |
| 9 | BOOT/download | Reserved |
| 10 | Digital spare | Physically exposed; runtime validation pending |
| 20/21 | UART0/recovery | Preserve when practical |

Final wiring belongs to IHAP-50 after the component decisions complete. No pin is reserved for a display until IHAP-53 is accepted.

---

## 5. Electrical and Power Boundary

ESP32-C3 manufacturer data establishes:

- nominal 3.3 V logic/power domain;
- no basis for treating GPIO as 5 V tolerant;
- strapping constraints on GPIO2, GPIO8 and GPIO9;
- USB Serial/JTAG on GPIO18/GPIO19 by default;
- package-dependent GPIO availability;
- RF transmit current up to 335 mA under one listed chip condition;
- a 5 µA deep-sleep figure under listed chip conditions.

These values are not complete-board or complete-node measurements.

### 5.1 IHAP-44 functional gate

IHAP-44 requires only:

- repeatable USB flashing;
- hard reset;
- bootloader recovery;
- serial diagnostics;
- representative **accepted MVP peripheral** operation;
- Wi-Fi functional operation when exercised;
- no observed brownout or reset loop using PC USB power.

An unaccepted display must not become part of the mandatory IHAP-44 representative configuration.

Multimeter rail measurements, current logging, regulator load testing, thermal testing and autonomy calculation are not IHAP-44 blockers.

### 5.2 IHAP-49 handoff

IHAP-49 owns:

- regulator identification and capacity validation;
- 3.3 V rail measurements;
- idle, Wi-Fi and reset current;
- selected environmental and presence-sensor current;
- display current only if IHAP-53 accepts a display;
- integrated-node peaks;
- battery, charger and regulator architecture;
- autonomy calculations.

No autonomy or reliability result may be derived from this ADR.

---

## 6. Alternatives Considered

| Platform | Functional fit | Reproducibility | Toolchain impact | Scope efficiency | Outcome |
|---|---|---|---|---|---|
| Purchased ESP32-C3 SuperMini-compatible board | Static eight-GPIO profile passes for photographed revision; integrated stability pending | Commercial SKU/lot still conditional | Preserves ESP-IDF | Compact and proportionate | Preferred conditional implementation |
| ESP32-C3-DevKitC-02 | Passes with documented pinout, power, BOOT/RESET and debug | Strong official documentation | Preserves ESP-IDF | Larger but controlled | Official control and fallback |
| ESP32 DevKit V1 / ESP-WROOM-32 class | Sufficient | Generic clone name remains variable | Compatible ecosystem but different baseline | Extra size/resources | Not preferred |
| ESP32-S3 development board | Large margin | Strong for official boards | ESP-IDF retained | Disproportionate compute and GPIO | Rejected as overengineering |
| Raspberry Pi Pico W | Sufficient | Strong official documentation | Requires Pico SDK porting | No required MVP benefit | Rejected for current architecture |
| ESP8266 | Reduced margin | Weak/legacy board variability | Legacy direction | No decisive advantage | Rejected legacy candidate |
| Linux SBC per room | Functionally possible | Higher operational burden | OS/runtime stack | Adds storage, patching, boot and power complexity | Rejected as disproportionate |

ESP32-C3-DevKitC-02 remains essential as a controlled comparison board even when the compact SuperMini implementation is used.

---

## 7. Consequences

### Positive

- establishes one proportionate MCU family;
- preserves ESP-IDF and C;
- preserves I2C as an environmental-sensor option without pre-approving an OLED;
- reserves full-duplex UART without making Bluetooth mandatory;
- separates architecture from seller-specific PCB details;
- separates compute selection from attached-component scope decisions;
- provides an official fallback and debug control;
- avoids Linux-per-node complexity;
- supplies bounded inputs to downstream component decisions.

### Negative / Trade-offs

- the exact commercial SuperMini SKU remains non-reproducible until order/listing evidence is recovered or equivalence is documented;
- only one physical board revision has been photographed;
- the eight-pin safe profile has limited surplus;
- compact boards increase wiring and enclosure sensitivity;
- onboard LED/regulator circuits remain partly unidentified;
- current replication prices are incomplete.

### Neutral / Operational

- BLE may be present but is not an MVP requirement;
- the photographed OLED remains inventory/evidence pending IHAP-53;
- hardware security capabilities are not configured security controls;
- the final pin mapping remains downstream;
- the 4 MB physical / 2 MB configured flash mismatch remains future firmware work;
- quantitative power evidence remains IHAP-49 work.

---

## 8. Qualification and Replacement Policy

### 8.1 Remaining qualification for the purchased board

The purchased board may be promoted from **preferred conditional implementation** to **exact reference PCB** after:

```text
[ ] At least one second owned board is photographed and compared for PCB consistency.
[ ] GPIO7 and GPIO10 are exercised or otherwise verified as usable application pins.
[ ] USB flashing, reset and recovery are repeated with representative accepted MVP peripherals attached.
[ ] PC USB operation shows no observed brownout or reset loop.
[ ] Onboard LED and other GPIO-loaded circuits are identified sufficiently to protect the eight-pin profile.
[ ] Selected component voltage and interface compatibility is verified by their own decision tasks.
[ ] Seller/order/listing evidence is recovered, or the board is explicitly documented as locally qualified but not universally reproducible.
[ ] A dated source for an equivalent replacement revision is recorded.
```

Display compatibility is not a qualification gate unless IHAP-53 later accepts a display into the MVP.

Quantitative current and rail measurements remain IHAP-49 gates, not IHAP-44 gates.

### 8.2 Equivalent replacement

A replacement board does not require a new platform ADR when it:

- uses an ESP32-C3 variant supported by the selected ESP-IDF baseline;
- provides at least 2 MB usable flash, with 4 MB preferred;
- provides at least eight safe application GPIO with required I2C, UART, digital-input and ADC capacity;
- preserves 3.3 V GPIO;
- supports PC USB reference operation;
- provides repeatable flashing, console and recovery;
- documents or verifies boot, strapping, LED and debug behavior;
- stays within IHAP-49 power assumptions;
- has wiring/enclosure effects handled by IHAP-50/IHAP-51;
- does not change firmware architecture or MVP scope;
- has an identifiable revision and dated source.

A board replacement may require wiring or enclosure updates without superseding this ADR.

### 8.3 Rejection conditions

Reject a SuperMini revision as the exact reference when:

- fewer than eight safe application GPIO are available;
- core functions depend on uncontrolled strapping states;
- GPIO are exposed to 5 V without suitable interfacing;
- USB flashing or recovery is unreliable with representative wiring;
- PC USB operation produces repeatable reset/brownout failures;
- owned or replacement units materially differ in pinout or circuitry and cannot be qualified through the profile;
- wiring or enclosure becomes irreducibly seller-revision-specific.

Board-level rejection does not reject ESP32-C3. ESP32-C3-DevKitC-02 becomes the fallback implementation. A different MCU family requires a superseding ADR.

---

## 9. Inputs to Dependent Tasks

| Task | Input produced by ADR-0001 |
|---|---|
| IHAP-45 — Environmental Sensor | Compute profile preserves both I2C BME280 and one-wire DHT-class alternatives; select exact sensor and electrical interface independently |
| IHAP-46 — Presence Sensor | Reserve full-duplex UART; verify LD2410C supply and logic; Bluetooth is not required |
| IHAP-47 — Door State Sensor | Reserve one interrupt-capable 3.3 V input; avoid uncontrolled strapping; define pull/debounce/cable circuit downstream |
| IHAP-48 — Audio Disposition | ADC exists only as an impact/margin item; no audio runtime is authorized |
| IHAP-49 — Power Subsystem | Quantify regulator, rail, accepted sensors and complete-node current; include display current only after IHAP-53 acceptance |
| IHAP-50 — Interconnect | Freeze wiring only after component decisions and exact pin qualification; do not reserve display wiring before IHAP-53 acceptance |
| IHAP-51 — Enclosure | Preserve PCB antenna keep-out and USB/BOOT/RST access; do not require a display aperture before IHAP-53 acceptance |
| IHAP-53 — Local Display | Decide no display vs status LED vs 0.96-inch I2C OLED; owns display necessity, electrical profile, GPIO/power/BOM/enclosure impact and any Product Vision update |
| IHAP-17 — Cost/BOM | Record the family decision; keep purchased-board prices historical until current equivalent-source evidence exists; display remains undecided |

---

## 10. Related Risks and Treatments

| Risk | Treatment | Effect | Remaining exposure |
|---|---|---|---|
| None directly modified by this ADR | None | None | Canonical source-of-truth, claim, scope, privacy and cost controls remain applicable |

No existing Risk Record treatment is directly changed by the compute-family decision. No Risk Record or inverse ADR link is added automatically.

---

## 11. Evidence Links

| Evidence | Link |
|---|---|
| Jira issue | [IHAP-44](https://niccolopiazzi01.atlassian.net/browse/IHAP-44) |
| Parent task | [IHAP-43](https://niccolopiazzi01.atlassian.net/browse/IHAP-43) |
| Display decision | [IHAP-53](https://niccolopiazzi01.atlassian.net/browse/IHAP-53) |
| Pull request | [PR #23](https://github.com/pianic2/homeedge-ai-platform/pull/23) |
| Cost/BOM draft | [IHAP-17](https://niccolopiazzi01.atlassian.net/browse/IHAP-17), [Draft PR #22](https://github.com/pianic2/homeedge-ai-platform/pull/22) |
| Product boundary | [`docs/product/product-vision.md`](../product/product-vision.md) |
| ADR policy | [`docs/adr/README.md`](README.md) |
| ESP32-C3 datasheet | https://www.espressif.com/documentation/esp32-c3_datasheet_en.pdf |
| ESP32-C3 stable ESP-IDF documentation | https://docs.espressif.com/projects/esp-idf/en/stable/esp32c3/get-started/index.html |
| ESP32-C3-DevKitC-02 guide | https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32c3/esp32-c3-devkitc-02/user_guide.html |
| ESP32-S3 datasheet | https://www.espressif.com/documentation/esp32-s3_datasheet_en.pdf |
| ESP8266EX datasheet | https://www.espressif.com/documentation/0a-esp8266ex_datasheet_en.pdf |
| Raspberry Pi Pico documentation | https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html |
| Runtime and prototype evidence | Project Owner supplied log and historical firmware; unique identifiers omitted |
| Physical photographs | Project Owner supplied front/back photographs of one ESP32-C3 SuperMini, one OLED module and one DHT11-class module on 2026-07-14 |
| Related Risk Records | None directly modified |
| Related treatments | None |
| Related ADRs | None |

---

## 12. Review Result After Scope Correction

### Architecture Regression Reviewer

- **PASS:** ESP32-C3 family, conformance profile and physical SKU remain separate.
- **PASS:** the Project Owner-accepted compute strategy is unchanged.
- **PASS:** the display is no longer introduced as an implicit MVP feature.
- **PASS:** no Bluetooth, audio, Linux-per-node or larger-MCU scope is introduced.

### Hardware Compatibility Reviewer

- **PASS:** the physical board exposes GPIO0–10 and GPIO20–21.
- **PASS:** a conservative eight-pin candidate set exists without using GPIO2, GPIO8, GPIO9, GPIO20 or GPIO21.
- **PASS:** the mandatory core sensor budget is recalculated independently from the display.
- **MAJOR:** GPIO7, GPIO10 and onboard-load interactions still require representative functional validation.
- **PASS:** quantitative rail/current evidence remains IHAP-49 work.

### Testing & Evidence Reviewer

- **PASS:** photographs resolve the physical pinout for one specimen.
- **PASS:** OLED photographs are retained as evidence without being promoted to an MVP requirement.
- **MAJOR:** lot consistency requires comparison with at least one second owned board.
- **MAJOR:** integrated accepted-peripheral/no-brownout evidence is still required before promoting the exact PCB.

### Cost Governance Reviewer

- **PASS:** historical price remains E2 acquisition evidence.
- **PASS:** display cost is not propagated into the definitive MVP BOM before IHAP-53 acceptance.
- **MAJOR:** exact current replacement price and availability remain absent.

### Source of Truth Guardian

- **PASS:** Product Vision remains canonical and unchanged.
- **PASS:** the unapproved display requirement has been removed from ADR-0001.
- **PASS:** IHAP-53 now owns the display decision and any future Product Vision update.
- **PASS:** Jira contains workflow/evidence coordination; no Confluence duplicate is created.

### Security & Privacy Reviewer

- **PASS:** unique device identifiers are omitted.
- **PASS:** audio remains blocked.
- **PASS:** presence and door state remain telemetry-only.
- **PASS:** a local display is not authorized to expose domestic telemetry before its own privacy/stakeholder review.

### Stakeholder Clarity Reviewer

- **PASS:** terminology consistently uses **OLED/display**, not LCD.
- **PASS:** owned hardware, observed evidence, MVP requirement and future decision are clearly separated.

### Final state

```text
ADR decision: Accepted.
ESP32-C3 family/profile: Accepted.
Purchased SuperMini-compatible board: preferred conditional implementation.
ESP32-C3-DevKitC-02: official control and fallback.
Local display: not yet an MVP requirement; decision moved to IHAP-53.
Exact commercial SKU reproducibility: [UNVALIDATED].
Quantitative power suitability: deferred to IHAP-49.
```
