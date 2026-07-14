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
  oled_in_mvp: true
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
  - Ownership and historical purchase price do not prove reproducibility.
  - Bluetooth availability does not make Bluetooth an MVP requirement.
  - Audio acquisition and audio-derived runtime behavior remain unauthorized.
  - Chip current figures must not be represented as measured board or complete-node consumption.
  - Quantitative rail, regulator and current validation belongs to IHAP-49.
  - No production-ready, commercial-ready, security-grade, certified, safety-critical, alarm-grade, antifurto, access-control, intrusion-detection, reliability or battery-autonomy claim is authorized.
-->

---

## 1. Decision Summary

The Project Owner accepts the following three-level strategy:

```text
MVP chip family: ESP32-C3.

Preferred compact implementation:
the purchased ESP32-C3 SuperMini-compatible board, conditionally qualified.

Official qualification control and fallback:
ESP32-C3-DevKitC-02.
```

The accepted board conformance profile requires:

- integrated 2.4 GHz Wi-Fi;
- official maintained ESP-IDF C/C++ support;
- at least 2 MB usable flash, with 4 MB preferred;
- 3.3 V GPIO logic;
- repeatable flashing, console, reset and bootloader recovery;
- one I2C bus;
- one full-duplex UART;
- one interrupt-capable digital input;
- one spare ADC-capable GPIO;
- at least eight safe application GPIO after flash, USB, boot, debug and onboard-load constraints;
- functional stability from PC USB without observed brownout or reset loops;
- an identifiable physical PCB revision for any exact reference board.

Acceptance of this ADR does **not** make the photographed SuperMini a universally reproducible SKU. The exact commercial listing, seller and lot relationship remain `[UNVALIDATED]`.

---

## 2. Context and Scope

HomeEdge MVP uses one generic room/door edge node supporting:

- temperature and humidity telemetry;
- local non-identifying presence state;
- door open/closed telemetry;
- one local 0.96-inch 128×64 OLED;
- Wi-Fi transport toward the target HTTP/JSON ingestion direction `[UNVALIDATED]`;
- reproducible flashing and diagnostics.

The compute platform determines GPIO capacity, electrical boundaries, radio and debug surfaces, enclosure impact, replacement cost and firmware portability.

This ADR deliberately separates:

1. **chip family** — ESP32-C3 and ESP-IDF;
2. **board conformance profile** — the capabilities an acceptable board must provide;
3. **physical board revision** — the exact PCB qualified against that profile.

The commercial name **ESP32-C3 SuperMini** is not an Espressif board standard and may cover materially different boards.

### 2.1 Protected boundaries

This ADR does not:

- implement or change firmware;
- authorize Bluetooth as an MVP transport or provisioning requirement;
- authorize audio collection or processing;
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
| One specimen identified as ESP32-C3 QFN32 rev. v0.4 with 4 MB XMC embedded flash and USB Serial/JTAG | Observed in Project Owner runtime log | High for one specimen | Does not identify seller or lot |
| The specimen flashed, verified, hard-reset and booted over PC USB | Observed in runtime log | High for that execution | Representative peripheral stability remains to be exercised |
| Historical prototype operated OLED GPIO0/1, DHT11 GPIO2, LED GPIO3, ADC GPIO4, LD2410C RX GPIO5 and MC-38 GPIO6 | Project Owner firmware/log | Medium-high | Not the accepted final mapping |
| Physical flash was 4 MB while firmware was configured for 2 MB | Observed | High | Firmware partition correction is separate work |

Unique device identifiers from logs are intentionally not reproduced.

### 3.2 Physical ESP32-C3 SuperMini evidence received 2026-07-14

Project Owner front/back photographs establish the following for one physical specimen:

- PCB silkscreen: `ESP32 C3 Super Mini`;
- USB-C connector;
- dedicated `BOOT` and `RST` buttons;
- visible 40 MHz crystal;
- chip marking visually consistent with `ESP32-C3FH4`, aligned with the independent 4 MB runtime detection;
- exposed supply pins: `5V`, `G`, `3.3`;
- exposed GPIO labels:
  - left side: `4`, `3`, `2`, `1`, `0`;
  - right side: `5`, `6`, `7`, `8`, `9`, `10`, `20`, `21`;
- PCB antenna area at the board edge;
- onboard indicator components are present, but their exact GPIO mapping remains `[UNVALIDATED]`;
- regulator marking and complete power-path schematic remain `[UNVALIDATED]`.

This physical pinout resolves the earlier catalog/prototype discrepancy for the photographed specimen: GPIO1, GPIO2 and GPIO3 are physically exposed on this board.

It does not prove that every board sold under the SuperMini name has the same PCB.

### 3.3 OLED evidence received 2026-07-14

The photographed OLED module provides:

- four pins marked `GND`, `VCC`, `SCL`, `SDA`;
- an I2C address-selection area marked `0x3C` / `0x3D`;
- PCB marking `GME12864-11-12-13 V3.22`.

This confirms an I2C module form factor for the photographed unit. The exact display controller, allowed supply range, pull-up voltage, regulator/level shifting and current remain `[UNVALIDATED]` and are handled with IHAP-45/IHAP-49.

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

### 4.1 Functional requirement

| Function | Protocol | GPIO required | Boundary |
|---|---|---:|---|
| OLED | I2C | 2 shared | Mandatory |
| BME280 option | I2C | 0 additional | May share OLED bus after IHAP-45 validation |
| DHT11/DHT22 option | Digital | 1 | Alternative environmental option |
| LD2410C telemetry and configuration | Full-duplex UART | 2 | Reserved until IHAP-46 narrows it |
| MC-38 door state | Digital interrupt | 1 | Circuit selected in IHAP-47 |
| Spare margin | Digital/ADC | 2 | At least one ADC-capable |
| MAX4466 impact | ADC | 1 optional | Does not authorize audio runtime |

Scenario totals:

| Scenario | Functional GPIO | Margin | Minimum usable GPIO |
|---|---:|---:|---:|
| OLED + BME280 + full-duplex LD2410C + MC-38 | 5 | 2 | 7 |
| OLED + DHT11/DHT22 + full-duplex LD2410C + MC-38 | 6 | 2 | 8 |

The accepted mandatory profile is therefore **eight safe application GPIOs**.

### 4.2 Photographed-board static pin budget

The photographed board exposes GPIO0–10 and GPIO20–21, excluding GPIO11–19 from application access except native USB routing.

A conservative candidate allocation excludes the three strapping pins and preserves UART0:

| Classification | GPIO |
|---|---|
| Candidate application set | `0`, `1`, `3`, `4`, `5`, `6`, `7`, `10` |
| Avoid for baseline application mapping | `2`, `8`, `9` — strapping constraints |
| Preserve for console/recovery when practical | `20`, `21` |
| Native USB | `18`, `19`, internally routed and not exposed as application pins |

This produces exactly **eight physically exposed candidate application pins** without depending on GPIO2, GPIO8, GPIO9, GPIO20 or GPIO21.

The static pin budget therefore passes for the photographed revision. Final safety still requires representative boot/recovery testing and confirmation that no unidentified onboard circuit loads GPIO0, GPIO1, GPIO3, GPIO4, GPIO5, GPIO6, GPIO7 or GPIO10.

### 4.3 Candidate mapping status

This is compatibility analysis, not the final wiring specification.

| GPIO | Candidate role | Status |
|---:|---|---|
| 0 | I2C SDA | Physically exposed; prototype observed |
| 1 | I2C SCL | Physically exposed; prototype observed |
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

Final wiring belongs to IHAP-50 after IHAP-45, IHAP-46 and IHAP-47 complete their component decisions.

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
- representative peripheral operation;
- Wi-Fi functional operation when exercised;
- no observed brownout or reset loop using PC USB power.

Multimeter rail measurements, current logging, regulator load testing, thermal testing and autonomy calculation are not IHAP-44 blockers.

### 5.2 IHAP-49 handoff

IHAP-49 owns:

- regulator identification and capacity validation;
- 3.3 V rail measurements;
- idle, Wi-Fi and reset current;
- OLED, LD2410C and environmental-sensor current;
- integrated-node peaks;
- battery, charger and regulator architecture;
- autonomy calculations.

No autonomy or reliability result may be derived from this ADR.

---

## 6. Alternatives Considered

| Platform | Functional fit | Reproducibility | Toolchain impact | Scope efficiency | Outcome |
|---|---|---|---|---|---|
| Purchased ESP32-C3 SuperMini-compatible board | Static GPIO profile passes for photographed revision; integrated stability pending | Commercial SKU/lot still conditional | Preserves ESP-IDF | Compact and proportionate | Preferred conditional implementation |
| ESP32-C3-DevKitC-02 | Passes with documented pinout, power, BOOT/RESET and debug | Strong official documentation | Preserves ESP-IDF | Larger but controlled | Official control and fallback |
| ESP32 DevKit V1 / ESP-WROOM-32 class | Sufficient | Generic clone name remains variable | Compatible family but different baseline | Extra size/resources | Not preferred |
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
- supports the OLED-aware GPIO budget;
- reserves full-duplex UART without making Bluetooth mandatory;
- separates architecture from seller-specific PCB details;
- provides an official fallback and debug control;
- avoids Linux-per-node complexity;
- supplies bounded inputs to IHAP-45 through IHAP-50.

### Negative / Trade-offs

- the exact commercial SuperMini SKU remains non-reproducible until order/listing evidence is recovered or equivalence is documented;
- only one physical board revision has been photographed;
- the eight-pin safe budget has little surplus;
- compact boards increase wiring and enclosure sensitivity;
- onboard LED/regulator circuits remain partly unidentified;
- current replication prices are incomplete.

### Neutral / Operational

- BLE may be present but is not an MVP requirement;
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
[ ] USB flashing, reset and recovery are repeated with representative MVP peripherals attached.
[ ] PC USB operation shows no observed brownout or reset loop.
[ ] Onboard LED and other GPIO-loaded circuits are identified sufficiently to protect the eight-pin budget.
[ ] OLED and selected environmental sensor voltage/pull-up compatibility is verified.
[ ] Seller/order/listing evidence is recovered, or the board is explicitly documented as locally qualified but not universally reproducible.
[ ] A dated source for an equivalent replacement revision is recorded.
```

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
| IHAP-45 — Environmental Sensor | OLED is confirmed as a four-wire I2C module for the photographed unit; BME280 may share I2C after voltage/address/pull-up validation; photographed DHT11-class module uses `+ / OUT / -` and adds one GPIO |
| IHAP-46 — Presence Sensor | Reserve full-duplex UART; verify LD2410C supply and logic; Bluetooth is not required |
| IHAP-47 — Door State Sensor | Reserve one interrupt-capable 3.3 V input; avoid uncontrolled strapping; define pull/debounce/cable circuit downstream |
| IHAP-48 — Audio Disposition | ADC exists only as an impact/margin item; no audio runtime is authorized |
| IHAP-49 — Power Subsystem | Quantify regulator, rail, OLED, radar, environmental sensor and complete-node current; PC USB functional evidence from IHAP-44 is not a power measurement |
| IHAP-50 — Interconnect | Freeze wiring only after exact pin qualification; preserve USB, BOOT and RESET access |
| IHAP-51 — Enclosure | Preserve PCB antenna keep-out, USB/BOOT/RST access and OLED aperture |
| IHAP-17 — Cost/BOM | Record the family decision; keep purchased-board prices historical until current equivalent-source evidence exists |

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

## 12. Review Result

### Architecture Regression Reviewer

- **PASS:** ESP32-C3 family, conformance profile and physical SKU remain separate.
- **PASS:** the Project Owner explicitly accepted the three-level strategy.
- **PASS:** no Bluetooth, audio, Linux-per-node or larger-MCU scope is introduced.

### Hardware Compatibility Reviewer

- **PASS:** the physical board exposes GPIO0–10 and GPIO20–21.
- **PASS:** a conservative eight-pin candidate set exists without using GPIO2, GPIO8, GPIO9, GPIO20 or GPIO21.
- **MAJOR:** GPIO7, GPIO10 and onboard-load interactions still require representative functional validation.
- **PASS:** quantitative rail/current evidence remains IHAP-49 work.

### Testing & Evidence Reviewer

- **PASS:** photographs resolve the physical pinout for one specimen.
- **PASS:** chip marking, USB-C, BOOT/RST and supply pins are recorded without unique identifiers.
- **MAJOR:** lot consistency requires comparison with at least one second owned board.
- **MAJOR:** integrated peripheral/no-brownout evidence is still required before promoting the exact PCB.

### Cost Governance Reviewer

- **PASS:** historical price remains E2 acquisition evidence.
- **MAJOR:** exact current replacement price and availability remain absent.
- **PASS:** no unsupported numerical ranking is published.

### Source of Truth Guardian

- **PASS:** the durable decision remains one ADR plus its index.
- **PASS:** Jira contains workflow/evidence coordination only.
- **PASS:** no duplicate Confluence technical decision or Risk Record was created.

### Security & Privacy Reviewer

- **PASS:** unique device identifiers are omitted.
- **PASS:** audio remains blocked.
- **PASS:** presence and door state remain telemetry-only.
- **PASS:** no security or maturity claim is introduced.

### Final state

```text
ADR decision: Accepted.
ESP32-C3 family/profile: Accepted.
Purchased SuperMini-compatible board: preferred conditional implementation.
ESP32-C3-DevKitC-02: official control and fallback.
Exact commercial SKU reproducibility: [UNVALIDATED].
Quantitative power suitability: deferred to IHAP-49.
```
