# ADR-0001 — MVP Edge Compute Platform

**Status:** Proposed  
**Date:** 2026-07-14  
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
  status: Proposed
  approval_authority: project_owner
  source_of_truth: github_versioned_repository_documentation
  jira_role: workflow_state_blockers_and_evidence_links
  confluence_role: optional_stakeholder_summary_and_navigation_only
  preferred_chip_family: esp32_c3
  purchased_board_status: conditional_unvalidated
  documented_fallback: esp32_c3_devkitc_02
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
  - This ADR remains Proposed until explicit Project Owner approval.
  - ESP32-C3 family selection, board conformance profile and purchased physical SKU are separate decision levels.
  - Ownership and historical purchase price do not approve a board.
  - The purchased SuperMini-compatible board remains conditional until its physical revision and conformance are verified.
  - The project-supplied catalog image is not proof that it describes the tested specimen or the original order.
  - Bluetooth availability does not make Bluetooth an MVP requirement.
  - GY-MAX4466 impact may be quantified but audio acquisition and audio-derived runtime behavior are not authorized.
  - Chip current figures must not be presented as measured board or complete-node consumption.
  - Quantitative rail, regulator and current validation belongs to IHAP-49.
  - No production-ready, commercial-ready, security-grade, certified, safety-critical, alarm-grade, antifurto, access-control, intrusion-detection, reliability or battery-autonomy claim is authorized.
-->

---

## 1. Context

HomeEdge MVP uses one generic room/door edge node supporting:

- temperature and humidity telemetry;
- local non-identifying presence state;
- door open/closed telemetry;
- one local 0.96-inch 128×64 OLED;
- 2.4 GHz Wi-Fi toward the target HTTP/JSON ingestion direction `[UNVALIDATED]`;
- reproducible flashing, recovery and diagnostics.

The compute platform determines GPIO and peripheral capacity, electrical boundaries, radio and debug surfaces, enclosure impact, replacement cost and firmware portability. The decision must not be based solely on the fact that a low-cost board is already owned.

This ADR distinguishes three levels:

1. **chip family** — the MCU architecture and maintained SDK;
2. **board conformance profile** — capabilities any acceptable board must provide;
3. **physical board revision** — the exact purchased or replacement PCB qualified against the profile.

The commercial label **ESP32-C3 SuperMini** is not an Espressif board standard. Boards sold under that name may differ between sellers or production batches.

### 1.1 Protected scope

This ADR does not:

- implement or change firmware;
- authorize Bluetooth as an MVP transport or provisioning requirement;
- authorize audio collection or processing;
- select the final environmental, presence, door, power, interconnect or enclosure subsystem;
- calculate battery autonomy;
- validate rail voltage, current draw or regulator capacity;
- approve IHAP-17 BOM lines;
- claim production, commercial, security, safety, alarm, access-control or certification maturity.

### 1.2 Evidence layers

| Layer | Meaning | Decision use |
|---|---|---|
| Chip-family evidence | Espressif datasheets and ESP-IDF documentation | May justify the ESP32-C3 family |
| Official-board evidence | Manufacturer guide, schematic, layout and pinout | May justify a documented control/fallback board |
| Specimen evidence | Runtime logs, firmware and direct observation of one board | Qualifies only the tested specimen and wiring |
| Commercial identity | Seller, listing, order, PCB fingerprint and revision | Required before claiming a reproducible purchased-board SKU |
| Integrated-node evidence | Tests with representative peripherals and USB PC power | Required for functional stability; quantitative power remains IHAP-49 |

---

## 2. Evidence Register

| Evidence | State | Source class | Reliability | Remaining gap |
|---|---|---|---|---|
| ESP32-C3 Wi-Fi, BLE, RISC-V CPU and maintained ESP-IDF support | Manufacturer declared | Espressif | High | Does not prove a specific board |
| Stable ESP-IDF documentation checked at v6.0.2 | Manufacturer declared, checked 2026-07-14 | Espressif | High | Normal future maintenance applies |
| ESP32-C3 variants expose different GPIO totals depending on package and embedded flash | Manufacturer declared | ESP32-C3 datasheet v2.4 | High | Exact purchased part must be identified |
| GPIO2, GPIO8 and GPIO9 are strapping pins | Manufacturer declared | ESP32-C3 datasheet v2.4 | High | External loads during reset require verification |
| GPIO18/GPIO19 provide USB Serial/JTAG by default | Manufacturer declared | ESP32-C3 datasheet v2.4 | High | Exact board USB routing remains board-specific |
| One specimen identified as ESP32-C3 QFN32 rev. v0.4 with 4 MB XMC embedded flash and USB Serial/JTAG | Observed | Project Owner runtime log | High for one specimen | Does not identify seller, PCB revision or other units |
| The same specimen was flashed and hard-reset successfully over USB | Observed | Project Owner runtime log | High for one execution | Long-run and representative-peripheral stability not proven |
| Firmware used a 2 MB flash configuration while physical flash was detected as 4 MB | Observed | Runtime log | High | Firmware partition correction is separate work |
| Historical prototype used OLED GPIO0/1, DHT11 GPIO2, LED GPIO3, ADC GPIO4, LD2410C RX GPIO5 and MC-38 GPIO6 | Observed | Project Owner firmware | Medium-high for that prototype | Not an approved final mapping |
| Project-supplied catalog depicts a USB-C board approximately 27.5 × 23 mm with GPIO0,4–10,20,21 and RX/TX labels for GPIO5/6 | Catalog-style declaration, provenance not established | Project-supplied image | Medium-low | Not linked to original seller/order or tested specimen |
| Catalog pinout conflicts with the prototype use of GPIO1, GPIO2 and GPIO3 | Verified inconsistency | Comparison of project evidence | High | Indicates different revision, inaccurate catalog or mismatched evidence |
| Catalog image states specifications may vary between production batches | Catalog-style declaration | Project-supplied image | Medium | Reinforces variant-control risk |
| Historical acquisition: 3 boards for €8.75, €2.9167/unit; 2 additional units at €0 | Project Owner inventory E2 | IHAP-17 Draft PR #22 | Medium | Not a current replication price |
| Exact seller, order listing and purchased PCB revision | Not available | None | None | Required for exact-SKU reproducibility |
| Regulator identity, LED mapping and complete power path | Not available | None | None | Physical inspection; quantitative validation in IHAP-49 |
| Current replication price and stock for the same revision | Not available | None | None | Dated market evidence required |
| Comparable current landed prices for alternatives | Not normalized | None | None | Cost remains non-decisive until sourced |

The catalog/runtime mismatch is material. The catalog image must not be treated as the pinout of the tested board until a physical comparison confirms that relationship.

---

## 3. Platform Requirements

### 3.1 Mandatory

| Requirement | Minimum profile |
|---|---|
| MCU family | ESP32-C3 supported by the selected ESP-IDF baseline |
| Wi-Fi | Integrated 2.4 GHz 802.11 b/g/n |
| SDK | Officially maintained C/C++ SDK with reproducible Linux/CI tooling |
| Flash | At least 2 MB usable flash and identified physical capacity; 4 MB is preferred, not yet an MVP necessity |
| GPIO logic | 3.3 V; no direct 5 V signal exposure |
| Application GPIO | At least 8 usable board-level pins after flash, USB, boot, debug and onboard-load constraints |
| I2C | One stable bus for OLED and an optional shared environmental sensor |
| UART | One full-duplex UART reserved for LD2410C until IHAP-46 narrows the requirement |
| Digital input | One interrupt-capable input for MC-38 |
| ADC | At least one spare ADC-capable pin; audio remains unauthorized |
| Flash/recovery | Repeatable flashing, console, hard reset and bootloader recovery |
| Power input | USB-PC-powered reference operation; board input path must be identified |
| Functional stability | No observed brownout/reset loop with the representative MVP configuration under USB PC power |
| Identity | PCB fingerprint and board-level pinout documented for any exact physical reference |
| Replaceability | Compliance with Section 9 |

### 3.2 Preferred

- 4 MB physical flash for configuration headroom;
- native USB Serial/JTAG;
- accessible BOOT and RESET controls;
- public schematic and board files;
- documented regulator and LED circuits;
- compact board dimensions;
- at least one additional ADC-capable spare pin;
- dated availability from more than one source or a strong equivalence path.

### 3.3 Outside this ADR

- battery operation and autonomy;
- TP4056, cell, holder and regulator selection;
- quantitative board current or rail measurements;
- final GPIO wiring specification;
- enclosure approval;
- Bluetooth runtime use;
- audio or derived-noise functionality;
- OTA design;
- production or certification claims.

---

## 4. Proposed Decision

```text
We propose ESP32-C3 as the HomeEdge MVP edge-compute chip family.

We propose a board conformance profile with:
- at least 2 MB usable flash, with 4 MB preferred;
- 3.3 V GPIO;
- repeatable flashing and recovery;
- at least eight safe application GPIOs;
- one I2C bus;
- one full-duplex UART;
- one interrupt-capable digital input;
- one spare ADC-capable pin;
- functional stability from a PC USB supply.

The purchased ESP32-C3 SuperMini-compatible board remains the preferred compact
candidate only after physical conformance evidence. Its exact commercial-board
selection remains [UNVALIDATED].

ESP32-C3-DevKitC-02 is the documented official control and fallback if the
purchased board cannot be identified, reproduced or shown to satisfy the profile.
```

This proposal becomes authoritative only if the Project Owner changes the ADR status beyond `Proposed`.

### 4.1 Why ESP32-C3

ESP32-C3 is preferred because it:

- satisfies current sensor, display, radio and debug requirements without a Linux OS;
- preserves the project ESP-IDF and C direction;
- provides Wi-Fi and optional BLE without making BLE an MVP requirement;
- avoids the porting cost of a different SDK ecosystem;
- avoids the additional compute, GPIO and complexity of ESP32-S3;
- has an official documented development board available as a qualification control.

### 4.2 OLED boundary

The OLED remains an active MVP hardware requirement. The following remain `[UNVALIDATED]` for the purchased modules:

- exact controller;
- address across every unit;
- accepted supply range;
- onboard regulator or level shifting;
- pull-up values and pull-up voltage;
- dimensions and mounting holes;
- representative current.

The OLED makes I2C mandatory. BME280 may share the bus only after IHAP-45 verifies address, pull-ups and voltage compatibility.

---

## 5. GPIO and Peripheral Budget

### 5.1 Functional budget

| Function | Component | Protocol | GPIO | Voltage constraint | Notes | Evidence state |
|---|---|---|---:|---|---|---|
| Local display | OLED 0.96-inch 128×64 | I2C | 2 shared | Module details `[UNVALIDATED]`; MCU logic 3.3 V | Mandatory bus | Prototype observed |
| Environment option A | BME280 | I2C | 0 additional | Module pull-ups/level shifting to verify | Shares OLED bus | Pending IHAP-45 |
| Environment option B | DHT11/DHT22 | Digital | 1 | Pull-up to 3.3 V | Adds one GPIO | Pending IHAP-45 |
| Presence telemetry | LD2410C | UART RX | 1 | Module UART level to verify | Prototype used RX-only | Prototype observed |
| Presence configuration | LD2410C | UART TX | +1 | Module UART level to verify | Reserved so Bluetooth is not mandatory | Pending IHAP-46 |
| Door state | MC-38 | Digital input/interrupt | 1 | Pull network at 3.3 V | Avoid uncontrolled boot strap interaction | Prototype observed |
| USB flash/debug | SoC/board | USB Serial/JTAG | GPIO18/19 reserved when used | USB board-specific | Observed on one specimen | Specimen verified |
| Recovery console | SoC/board | UART0 | GPIO20/21 conditioned | 3.3 V | Keep available when practical | Board-specific |
| Onboard LED | Board-specific | Digital | 0 or 1 loaded GPIO | Board-specific | Must not consume a required pin silently | `[UNVALIDATED]` |
| Audio impact only | GY-MAX4466 | ADC | 1 optional | Must remain in ADC range | Does not authorize audio | OUT OF MVP runtime |
| Margin | None | Digital/ADC | 2 | 3.3 V | At least one ADC-capable | Required |

### 5.2 Scenario totals

| Scenario | Functional GPIO | Required margin | Minimum usable GPIO |
|---|---:|---:|---:|
| OLED + BME280 + LD2410C full duplex + MC-38 | 5 | 2 | 7 |
| OLED + DHT11/DHT22 + LD2410C full duplex + MC-38 | 6 | 2 | 8 |
| Previous scenario plus MAX4466 impact reservation | +1 | Consumes ADC spare | 9, not an active-MVP requirement |

The mandatory profile is **eight safe application GPIOs**:

- 2 I2C;
- 2 UART;
- 1 door input;
- 1 DHT-class optional input;
- 2 spare pins, at least one ADC-capable.

### 5.3 Candidate mapping status

This table is compatibility analysis, not an approved wiring specification.

| GPIO | Candidate role | Status | Constraint |
|---:|---|---|---|
| 0 | I2C SDA | Candidate | Prototype observed; ADC-capable |
| 1 | I2C SCL | Specimen-observed only | Catalog image does not show GPIO1; exact board revision unresolved |
| 2 | Historical DHT data | Avoid for final mapping when possible | Strapping pin; prototype success is not reset-matrix proof |
| 3 | DHT alternative or spare | Specimen-observed only | Catalog image does not show GPIO3 |
| 4 | ADC spare | Candidate | Audio runtime unauthorized |
| 5 | LD2410C TX → MCU RX | Candidate | Prototype observed at 256000 baud |
| 6 | LD2410C RX path or door alternative | Candidate | Prototype observed as MC-38 input |
| 7 | Door or spare candidate | Catalog-declared only | Physical exposure on purchased specimen not verified |
| 8 | No default application allocation | Avoid/conditional | Strapping; official DevKitC-02 also loads RGB LED |
| 9 | BOOT/download | Reserved | Strapping and recovery |
| 10 | Spare candidate | Catalog-declared only | Physical verification required |
| 11–17 | No application allocation | Reserved/unavailable by variant | Embedded flash/package constraints |
| 18/19 | Native USB | Reserved when used | USB D-/D+ |
| 20/21 | UART0/recovery | Conditioned | Runtime log showed console UART use; catalog declares exposure |

The catalog conflict means GPIO1, GPIO2 and GPIO3 cannot be assumed to exist on every board sold as SuperMini. Final wiring belongs to IHAP-50 after exact-board qualification.

---

## 6. Electrical and Power Constraints

### 6.1 Chip-level facts

The ESP32-C3 datasheet establishes:

- a nominal 3.3 V power domain;
- no basis for treating GPIO as 5 V tolerant;
- GPIO2, GPIO8 and GPIO9 as strapping pins;
- GPIO18 and GPIO19 as default USB Serial/JTAG pins;
- GPIO20 and GPIO21 as UART0-capable pins;
- package-dependent GPIO availability;
- RF transmit current up to 335 mA under one listed chip test condition;
- a 5 µA deep-sleep figure for the chip under listed conditions.

These chip-level inputs do not prove complete board current, regulator capacity, rail stability, OLED/radar current, complete-node sleep or battery autonomy.

### 6.2 IHAP-44 functional validation boundary

IHAP-44 may use evidence for:

- USB flashing;
- hard reset;
- bootloader recovery;
- serial console;
- representative peripherals attached;
- Wi-Fi functional operation when available;
- absence of observed brownout or reset loops on PC USB.

IHAP-44 does not require multimeter rail measurements, current logging, regulator load testing, thermal testing or autonomy calculation. Those measurements and the complete power architecture belong to IHAP-49.

### 6.3 Inputs to IHAP-49

| Item | Preliminary input | Meaning |
|---|---|---|
| ESP32-C3 Wi-Fi peak | Up to 335 mA in one datasheet RF condition | Conservative chip input, not board measurement |
| Physical flash | 4 MB observed on one specimen | Does not determine power |
| Board regulator | `[UNVALIDATED]` | Identity and capacity unknown |
| Board LEDs | `[UNVALIDATED]` | Mapping and current unknown |
| OLED | `[UNVALIDATED]` | Exact module and current unknown |
| LD2410C | Deferred to IHAP-46/IHAP-49 | Exact interface/current needed |
| Environmental sensor | Deferred to IHAP-45/IHAP-49 | Depends on selection |
| MC-38 | Passive contact | Pull-network current depends on circuit |
| Complete node | `[UNVALIDATED]` | Requires integrated measurement |

No battery result may be derived from this table.

---

## 7. Alternatives Considered

### 7.1 Evaluation gates

No aggregate score is used. Numerical weighting would create false precision while board identity, current prices and power evidence are incomplete.

| Gate | Requirement |
|---|---|
| G1 — Functional fit | Wi-Fi and sufficient board-level GPIO/peripherals |
| G2 — Electrical fit | 3.3 V logic and documentable input/power path |
| G3 — Toolchain | Maintained official C/C++ SDK and reproducible flashing |
| G4 — Reproducibility | Identifiable board or enforceable conformance profile |
| G5 — Scope efficiency | No disproportionate OS, compute or porting overhead |
| G6 — Cost evidence | Historical and current replication prices kept separate |

Cost cannot compensate for failure of a mandatory technical gate.

### 7.2 Comparison matrix

| Platform | G1 | G2 | G3 | G4 | G5 | Cost evidence | Outcome |
|---|---|---|---|---|---|---|---|
| Purchased ESP32-C3 SuperMini-compatible board | Conditional: one prototype works, eight-safe-pin profile not proven | Conditional: USB works; regulator/path incomplete | Pass at chip/toolchain level | Fail for exact SKU today | Pass | Historical €2.9167/unit E2; current price absent | Preferred compact candidate, conditional `[UNVALIDATED]` |
| ESP32-C3-DevKitC-02 | Pass with strapping care | Pass from official documentation | Pass | Pass | Conditional only for larger size | Current landed EUR price not normalized | Official control and fallback |
| ESP32 DevKit V1 / ESP-WROOM-32 class | Pass | Conditional by clone; official DevKitC documented | Pass | Conditional: “DevKit V1” is generic | Conditional: extra resources and size | Comparable current price absent | Not preferred; fallback only if C3 infeasible |
| ESP32-S3 development board | Pass with large margin | Pass on official board | Pass | Pass on official SKU | Fail/conditional: disproportionate for MVP | Comparable current price absent | Rejected as overengineering |
| Raspberry Pi Pico W | Pass | Pass | Pass, different SDK | Pass | Conditional: porting without required benefit | Official launch price is not a current landed EUR price | Rejected for current architecture |
| ESP8266 | Conditional with reduced margin | Conditional by board | Legacy | Weak | No decisive benefit | Low price cannot override lifecycle/tooling risk | Rejected legacy candidate |

### 7.3 Alternative rationale

**ESP32-C3-DevKitC-02** is the strongest control because Espressif documents its module, flash, USB-UART bridge, BOOT, RESET, power LED, LDO, pinout, schematic, PCB layout and dimensions.

**ESP32 classic** has sufficient peripherals but adds Bluetooth Classic and broader resources not required by the node. Generic “DevKit V1” boards also reproduce the variant-control problem.

**ESP32-S3** provides more compute and I/O than required. No approved camera, LCD, USB-host, vector-processing or large-GPIO workload justifies that complexity.

**Raspberry Pi Pico W** is well documented and electrically capable, but moving from ESP-IDF to the Pico SDK creates firmware, build and maintenance porting without an MVP requirement ESP32-C3 cannot meet.

**ESP8266** is unsuitable for a new baseline because it has lower margin, a legacy ecosystem and no architectural advantage over ESP32-C3.

A Linux SBC at each room node is disproportionate: it adds OS boot, storage, patching, filesystem, process supervision, power and enclosure concerns to a node requiring deterministic sensor I/O, local display and Wi-Fi telemetry.

---

## 8. Consequences

### Positive

- Preserves ESP-IDF and C.
- Keeps the compute family proportionate.
- Defines an explicit board-level GPIO profile.
- Preserves a full-duplex LD2410C UART without making Bluetooth mandatory.
- Separates stable MCU architecture from replaceable PCB implementation.
- Provides an official fallback for qualification and debugging.
- Supplies explicit inputs to IHAP-45 through IHAP-50.

### Negative / Trade-offs

- The purchased board cannot yet be accepted as the exact reproducible reference.
- Physical and commercial identity evidence is incomplete.
- Eight safe GPIO leave limited margin compared with ESP32-S3.
- Compact boards increase wiring and enclosure sensitivity.
- Native USB, strapping and onboard loads may create revision-specific constraints.
- Current price ranking remains incomplete.

### Neutral / Operational

- BLE may exist in silicon but is not authorized as an MVP runtime requirement.
- Hardware security features are not configuration or security claims.
- The final pin assignment remains downstream.
- The physical 4 MB/configured 2 MB mismatch is a future firmware-configuration concern, not a hardware rejection.
- Quantitative power evidence remains owned by IHAP-49.

---

## 9. Qualification, Replacement and Rejection

### 9.1 Purchased-board qualification

The purchased board may become the exact reference only after:

```text
[ ] Seller/order/listing evidence is recovered, or the board is explicitly classified as locally qualified but not universally reproducible.
[ ] Front and back photographs establish a repeatable PCB fingerprint.
[ ] At least two owned specimens are compared for revision consistency.
[ ] Chip revision and physical flash are recorded without exposing unique identifiers.
[ ] Physical pin labels are reconciled with the catalog and prototype.
[ ] At least eight safe application GPIO satisfy the budget.
[ ] USB flash, hard reset and recovery work with representative peripherals.
[ ] PC USB operation shows no observed brownout or reset loop.
[ ] Regulator, LED, BOOT and RESET circuits are identified where markings permit.
[ ] Dimensions, header spacing and antenna keep-out are recorded.
[ ] A dated current listing exists for the same revision, or equivalence is proven through this profile.
[ ] OLED and selected sensor bus voltage/pull-up compatibility is verified.
```

Regulator load capacity, rail voltage and quantitative current measurements are not IHAP-44 qualification gates; they remain `[UNVALIDATED]` for IHAP-49.

### 9.2 Equivalent board replacement

A replacement does not require a new platform ADR when it:

- uses an ESP32-C3 variant supported by the selected ESP-IDF baseline;
- provides at least 2 MB usable flash; 4 MB remains preferred;
- provides at least eight safe application GPIO with required I2C, UART, digital input and ADC margin;
- preserves 3.3 V GPIO;
- supports PC USB power for reference validation;
- provides repeatable flashing, console and recovery;
- documents or verifies boot, strapping, LED and debug behavior;
- stays within IHAP-49 power assumptions;
- has wiring/enclosure effects handled by IHAP-50/IHAP-51;
- does not change firmware architecture or MVP scope;
- has an identifiable revision and dated source.

A board change may require wiring or enclosure updates even when it does not supersede this ADR.

### 9.3 Rejection conditions

Reject the purchased board as the definitive reference when:

- its revision cannot be distinguished and no enforceable profile can be verified;
- fewer than eight safe application GPIO are available;
- core functions depend on uncontrolled strapping states;
- GPIO are exposed to 5 V without appropriate interfacing;
- USB flash or recovery is unreliable with representative wiring;
- owned units materially differ in pinout or circuitry;
- the board cannot operate functionally from PC USB without observed reset/brownout problems;
- replacement units cannot be qualified through the equivalence profile;
- wiring or enclosure becomes irreducibly seller-revision-specific.

Board-level rejection does not reject the ESP32-C3 family. ESP32-C3-DevKitC-02 becomes the default fallback. A move to another MCU family requires a superseding ADR.

---

## 10. Inputs to Dependent Tasks

| Task | Input produced |
|---|---|
| IHAP-45 | I2C is mandatory for OLED; BME280 may share it only after voltage/address/pull-up validation; DHT adds one GPIO |
| IHAP-46 | Reserve full-duplex UART; verify module logic and supply; Bluetooth is not required |
| IHAP-47 | Reserve one interrupt-capable 3.3 V input; avoid uncontrolled strapping; circuit remains downstream |
| IHAP-48 | ADC exists only as an impact/margin item; no audio runtime is authorized |
| IHAP-49 | Use chip current only as a preliminary ceiling input; quantify regulator, rail, OLED, radar and complete-node current there |
| IHAP-50 | Freeze wiring only after exact-board pinout; preserve USB, BOOT and RESET access |
| IHAP-51 | Preserve antenna keep-out, connector access and OLED aperture; exact dimensions remain board-dependent |
| IHAP-17 | Historical board cost remains E2; no definitive BOM or replication price before Project Owner decision |

---

## 11. Related Risks and Treatments

| Risk | Treatment | Effect | Remaining exposure |
|---|---|---|---|
| None directly modified by this ADR | None | None | Generic source-of-truth, claim, scope and cost controls remain applicable through their canonical policies |

No existing Risk Record treatment is changed by selecting a proposed compute family. Therefore no Risk Record is modified and no inverse ADR link is required. A new hardware-variant risk must not be created automatically without a separate task and Project Owner scope decision.

---

## 12. Follow-up Work

| Item | Tracking |
|---|---|
| Project Owner family/board strategy decision | IHAP-44 |
| Recover exact seller/order/listing evidence | IHAP-44 evidence checkpoint |
| Photograph and compare at least two owned boards | IHAP-44 evidence checkpoint |
| Verify physical pinout and functional USB/recovery stability | IHAP-44 evidence checkpoint |
| Quantitative rail, regulator and current validation | IHAP-49 |
| Environmental sensor selection | IHAP-45 |
| LD2410C interface and power decision | IHAP-46 |
| MC-38 circuit decision | IHAP-47 |
| GY-MAX4466 physical disposition | IHAP-48 |
| Final wiring and assembly | IHAP-50 |
| Enclosure and mounting | IHAP-51 |
| Current market-price propagation | IHAP-17 after approved hardware decision |
| Flash partition correction if required | Separate future firmware task |

---

## 13. Evidence Links

| Evidence | Link |
|---|---|
| Jira issue | [IHAP-44](https://niccolopiazzi01.atlassian.net/browse/IHAP-44) |
| Parent task | [IHAP-43](https://niccolopiazzi01.atlassian.net/browse/IHAP-43) |
| Pull request | [PR #23](https://github.com/pianic2/homeedge-ai-platform/pull/23) |
| Cost/BOM draft | [IHAP-17](https://niccolopiazzi01.atlassian.net/browse/IHAP-17), [Draft PR #22](https://github.com/pianic2/homeedge-ai-platform/pull/22) |
| Product boundary | [`docs/product/product-vision.md`](../product/product-vision.md) |
| ADR policy | [`docs/adr/README.md`](README.md) |
| ESP32-C3 datasheet v2.4 | https://www.espressif.com/documentation/esp32-c3_datasheet_en.pdf |
| ESP32-C3 stable ESP-IDF documentation | https://docs.espressif.com/projects/esp-idf/en/stable/esp32c3/get-started/index.html |
| ESP32-C3-DevKitC-02 official guide | https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32c3/esp32-c3-devkitc-02/user_guide.html |
| ESP32 DevKitC official guide | https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html |
| ESP32-S3 datasheet | https://www.espressif.com/documentation/esp32-s3_datasheet_en.pdf |
| ESP8266EX datasheet | https://www.espressif.com/documentation/0a-esp8266ex_datasheet_en.pdf |
| Raspberry Pi Pico documentation | https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html |
| Runtime specimen evidence | Project Owner supplied log; unique device identifiers intentionally omitted |
| Prototype firmware evidence | Project Owner supplied historical firmware; not introduced into this repository by IHAP-44 |
| Board/OLED catalog image | Project Owner supplied image; provenance and correspondence to purchased specimen remain `[UNVALIDATED]` |
| Related Risk Records | None directly modified |
| Related treatments | None |
| Related ADRs | None |

---

## 14. Review Notes

### Architecture Regression Reviewer

- **PASS:** ESP32-C3 family, board profile and exact SKU are separated.
- **PASS:** no Bluetooth, audio, Linux-per-node or larger-MCU feature is introduced.
- **PASS:** status remains `Proposed`.

### Hardware Compatibility Reviewer

- **MAJOR:** catalog pinout and prototype pinout conflict; exact purchased revision remains unresolved.
- **MAJOR:** eight-safe-GPIO profile is not yet proven on the purchased board.
- **PASS:** GPIO2 remains a conditional historical mapping because it is a strapping pin.
- **PASS:** quantitative rail/current evidence is correctly deferred to IHAP-49.

### Testing & Evidence Reviewer

- **MAJOR:** runtime evidence qualifies one specimen only.
- **MAJOR:** at least two owned boards must be compared before claiming lot consistency.
- **PASS:** successful flash/reset and specimen identity are recorded without copying the MAC.
- **PASS:** unproven board and power claims remain `[UNVALIDATED]`.

### Cost Governance Reviewer

- **MAJOR:** no current reproducible price exists for the purchased revision.
- **PASS:** €2.9167 is historical E2 acquisition evidence only.
- **PASS:** no arbitrary score or unsupported current-price ranking is published.
- **PASS:** IHAP-17 is linked but not modified.

### Source of Truth Guardian

- **PASS:** one ADR contains decision, GPIO budget, comparison and replacement policy.
- **PASS:** PR #23 is linked directly; the unmerged cost policy path is not referenced as if present on `main`.
- **PASS:** no duplicate ADR, Risk Record or Confluence technical copy is created.

### Security & Privacy Reviewer

- **PASS:** unique device identifiers are not reproduced.
- **PASS:** audio remains blocked.
- **PASS:** presence and door state remain telemetry-only.
- **PASS:** no security or maturity claim is introduced.

### Review result

```text
BLOCKER for keeping ADR Proposed: none.

BLOCKER for exact purchased-board acceptance:
- commercial identity and PCB correspondence unresolved;
- catalog/prototype pinout conflict unresolved;
- eight-safe-GPIO conformance not proven;
- current replication availability absent.

Project Owner decision required:
1. accept the ESP32-C3 family/profile proposal while keeping SuperMini conditional;
2. select ESP32-C3-DevKitC-02 as the immediate exact reference;
3. request changes or suspend the decision.
```
