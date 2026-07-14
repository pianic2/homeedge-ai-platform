# ADR-0001 — MVP Edge Compute Platform

**Status:** Proposed  
**Date:** 2026-07-14  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Jira:** IHAP-44  
**PR:** Pending  
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
  exact_purchased_board_status: unvalidated
  preferred_chip_family: esp32_c3
  preferred_board_candidate: purchased_esp32_c3_supermini_compatible_board
  documented_fallback: esp32_c3_devkitc_02
  oled_in_mvp: true
  oled_profile: 0.96_inch_128x64_i2c
  raw_audio_allowed: false
  bluetooth_required: false
  firmware_changes_allowed: false
  runtime_changes_allowed: false
  unvalidated_claim_marker: "[UNVALIDATED]"

HIDDEN_ANTI_REGRESSION_RULES:
  - This ADR remains Proposed until explicit Project Owner approval.
  - The ESP32-C3 chip family and the exact physical development board are separate decision levels.
  - Ownership and historical purchase price do not approve a board.
  - The exact purchased SuperMini-compatible board remains [UNVALIDATED] until its listing, PCB revision, regulator, LED, dimensions, complete pinout, and power behavior are identified.
  - The 0.96-inch 128x64 OLED is included in the MVP by Project Owner decision, but its controller, module voltage range, onboard pull-ups, regulator, and exact listing remain [UNVALIDATED].
  - Bluetooth availability does not make Bluetooth an MVP requirement.
  - GY-MAX4466 impact may be quantified but audio acquisition and audio-derived runtime behavior are not authorized.
  - Deep-sleep and RF-current figures for the chip must not be presented as measured board or complete-node consumption.
  - No production-ready, commercial-ready, security-grade, certified, safety-critical, alarm-grade, antifurto, access-control, intrusion-detection, reliability, or battery-autonomy claim is authorized.
-->

---

## 1. Context

HomeEdge MVP requires one generic room/door edge node that can support:

- temperature and humidity telemetry;
- local non-identifying presence state;
- door open/closed telemetry;
- a local 0.96-inch 128×64 OLED display selected by the Project Owner;
- Wi-Fi transport toward the target HTTP/JSON ingestion direction `[UNVALIDATED]`;
- reproducible flashing, recovery and diagnostics.

The edge compute board determines the available GPIO and peripheral budget, voltage domains, radio and debug surfaces, preliminary current envelope, enclosure footprint, replication cost and firmware portability. The board therefore requires a durable architecture decision rather than an inventory-only BOM classification.

The current Project Owner inventory contains boards sold or described as ESP32-C3 SuperMini-compatible development boards. Historical cost evidence in the IHAP-17 draft records three units at €8.75 total, or €2.9167 per unit, plus two inventory-owned units recorded at zero historical cost. These prices are acquisition evidence only; they are not a current replication price or evidence that the same hardware revision can be purchased again.

A previous Project Owner prototype supplied runtime evidence for one physical specimen:

- `esptool` identified an ESP32-C3 QFN32 revision v0.4;
- embedded XMC flash was detected as 4 MB;
- USB mode was identified as USB Serial/JTAG;
- GPIO0 and GPIO1 operated as an I2C bus with an OLED at address `0x3C`;
- GPIO2 operated with DHT11;
- GPIO3 operated as a status LED output;
- GPIO4 operated as ADC impact evidence;
- GPIO5 received LD2410C UART telemetry;
- GPIO6 received MC-38 door-contact state.

The runtime log contained a device MAC address and is not copied into this ADR. The observations qualify only the tested specimen and wiring. They do not identify the commercial listing, PCB revision, regulator, complete exposed pinout, current capability, or another board sold under the same SuperMini name.

The decision must distinguish four evidence layers:

1. ESP32-C3 chip-family capabilities published by Espressif;
2. board-level capabilities documented for a specific development board;
3. characteristics observed on the purchased specimen;
4. characteristics not yet physically or commercially verified.

### 1.1 Protected scope

This ADR does not:

- implement or change firmware;
- authorize Bluetooth as a required transport or provisioning mechanism;
- authorize audio collection or processing;
- select the final environmental, presence, door, power, interconnect, or enclosure subsystem;
- calculate battery autonomy;
- approve IHAP-17 BOM lines;
- claim production, commercial, security, safety, alarm, access-control or certification maturity.

### 1.2 Primary requirements

The platform must provide:

- 2.4 GHz Wi-Fi;
- an officially maintained C/C++ SDK and reproducible Linux/CI toolchain;
- at least 4 MB flash as the proposed minimum profile;
- stable flashing, console and recovery paths;
- I2C for the OLED and a possible I2C environmental sensor;
- UART for LD2410C, with full duplex reserved until IHAP-46 decides whether RX-only is sufficient;
- a digital interrupt-capable input for MC-38;
- an additional digital GPIO when DHT11 or DHT22 is selected;
- at least two spare application GPIOs, one ADC-capable;
- 3.3 V GPIO logic and no direct 5 V signal exposure;
- a documented or physically verified power path and regulator;
- a replaceable board profile that does not depend solely on a seller marketing name.

### 1.3 Evidence state

| Evidence | State | Source class | Reliability | Remaining gap |
|---|---|---|---|---|
| ESP32-C3 Wi-Fi, BLE, RISC-V CPU and official ESP-IDF support | Manufacturer declared | Espressif ESP-IDF and datasheet | High | No board-level gap resolved |
| ESP-IDF stable support at v6.0.2 | Manufacturer declared, checked 2026-07-14 | Espressif documentation | High | Future updates require normal maintenance |
| 22 theoretical GPIO for relevant ESP32-C3 variants | Manufacturer declared | ESP32-C3 datasheet v2.4 | High | Flash, USB, strapping and board circuits reduce usable GPIO |
| GPIO2, GPIO8 and GPIO9 are strapping pins | Manufacturer declared | ESP32-C3 datasheet v2.4 | High | Exact board pull circuits remain unknown |
| GPIO18 and GPIO19 are USB Serial/JTAG pins by default | Manufacturer declared | ESP32-C3 datasheet v2.4 | High | Exact board USB wiring remains to be inspected |
| Recommended chip supply is 3.0–3.6 V | Manufacturer declared | ESP32-C3 datasheet v2.4 | High | Board 5 V input and LDO remain unidentified |
| RF TX peak up to 335 mA in listed chip test condition | Manufacturer declared | ESP32-C3 datasheet v2.4 | High for stated conditions | Not complete board/node consumption |
| Chip deep-sleep figure of 5 µA | Manufacturer declared | ESP32-C3 datasheet v2.4 | High for the chip | Not board, OLED, radar or regulator consumption |
| Tested specimen: ESP32-C3 rev. 0.4, 4 MB XMC embedded flash, native USB Serial/JTAG | Observed | Project Owner runtime log | High for one specimen | Not committed as durable repository evidence; commercial identity absent |
| OLED `0x3C` on GPIO0/GPIO1 operated in prototype | Observed | Project Owner firmware/log evidence | Medium-high for the tested pair | Controller, voltage, pull-ups and exact listing absent |
| GPIO0–GPIO6 operated in one prototype | Observed | Project Owner firmware/log evidence | Medium-high | Power-cycle, recovery and full MVP configuration not validated |
| Exact SuperMini seller, listing and PCB revision | Not available | None | None | Required before exact-board acceptance |
| Exact SuperMini regulator, onboard LED and dimensions | Not available | None | None | Physical inspection required |
| GPIO7, GPIO10, GPIO20 and GPIO21 exposed on purchased board | `[UNVALIDATED]` | Common board patterns are not accepted as evidence | None | Physical pinout verification required |
| Current replication price of purchased SuperMini revision | Not available | Exact listing absent | None | Dated listing and stock evidence required |
| Current normalized prices for official alternative boards | Partial | Manufacturer or retailer snapshots | Medium | Use dated landed-price snapshots before final cost ranking |

---

## 2. Decision

```text
We propose ESP32-C3 as the HomeEdge MVP edge-compute chip family.

We propose an ESP32-C3 board profile with at least 4 MB flash, a reproducible
flashing/recovery path, 3.3 V GPIO, and at least eight application GPIOs that
satisfy the OLED, sensor, UART, interrupt and margin budget.

The purchased ESP32-C3 SuperMini-compatible board is the preferred compact
physical candidate only after exact-board qualification. Until that evidence
exists, its board-level selection remains [UNVALIDATED].

ESP32-C3-DevKitC-02 is the documented qualification and fallback reference if
the purchased board cannot be identified, replicated or shown to meet the
profile.
```

This proposal becomes authoritative only if the Project Owner changes this ADR from `Proposed` to `Accepted`.

### 2.1 Required board profile

| Requirement | Mandatory profile |
|---|---|
| SoC family | ESP32-C3 supported by the selected ESP-IDF baseline |
| Flash | At least 4 MB; exact chip/package must be identified |
| Wi-Fi | Integrated 2.4 GHz 802.11 b/g/n |
| Bluetooth | May be present; not an MVP runtime requirement |
| GPIO logic | 3.3 V; no direct 5 V input |
| Application GPIO | At least 8 usable pins after flash, USB, boot, debug and onboard loads |
| I2C | One stable bus for OLED and optional BME280 sharing |
| UART | One full-duplex UART reserved for LD2410C until IHAP-46 narrows it |
| ADC | At least one spare ADC-capable GPIO; audio remains unauthorized |
| Digital input | One interrupt-capable pin for MC-38 |
| Flashing/recovery | Documented USB or USB-UART flashing plus repeatable boot recovery |
| Power | Identified 5 V/USB input path and 3.3 V regulator or equivalent evidence |
| Board identity | Seller/SKU, PCB fingerprint, pinout, LED, buttons, dimensions and revision recorded |
| Replaceability | Meets the equivalence rules in Section 8 |

### 2.2 OLED decision boundary

The Project Owner has included the AOICRIE-listed 0.96-inch white 128×64 OLED in the physical and active MVP node profile. Historical acquisition evidence is five modules for €7.71, or €1.5420 per unit.

The following remain `[UNVALIDATED]` until physical/listing evidence exists:

- SSD1306 versus SH1106 or another controller;
- I2C-only versus a different module variant;
- address `0x3C` as a property of every purchased unit;
- accepted supply-voltage range;
- onboard regulator or level shifting;
- onboard pull-up values and pull-up voltage;
- exact dimensions and mounting-hole positions;
- representative and worst-case current.

The OLED makes I2C mandatory even if IHAP-45 selects DHT11 or DHT22. If BME280 is selected, the environmental sensor may share the I2C bus only after address, pull-up and voltage compatibility are verified.

---

## 3. GPIO and Peripheral Budget

### 3.1 Functional budget

| Function | Component | Protocol | GPIO required | Voltage constraint | Notes / conflicts | Evidence state |
|---|---|---|---:|---|---|---|
| Local display | OLED 0.96-inch 128×64 | I2C | 2 shared | Module supply and pull-ups `[UNVALIDATED]`; MCU logic 3.3 V | Mandatory bus; observed at `0x3C` on one specimen | Project Owner included; prototype observed |
| Environmental option A | BME280 module | I2C | 0 additional | Module-level voltage and pull-ups must be verified | Shares OLED SDA/SCL when compatible | Pending IHAP-45 |
| Environmental option B | DHT11 or DHT22 | Proprietary digital | 1 | Pull-up must terminate at 3.3 V | Uses an additional GPIO because OLED already consumes I2C bus | Pending IHAP-45 |
| Presence telemetry | LD2410C | UART sensor TX to MCU RX | 1 | UART logic level must be verified | Minimum passive telemetry path | Prototype observed on GPIO5 |
| Presence configuration | LD2410C | UART MCU TX to sensor RX | +1 | UART logic level must be verified | Reserved to avoid making Bluetooth mandatory | Pending IHAP-46 |
| Door state | MC-38 | Digital input / interrupt | 1 | Pull strategy at 3.3 V | Must not rely on a conflicting strapping level | Prototype observed on GPIO6 |
| Wi-Fi | ESP32-C3 radio | Internal | 0 | Affects current, rail stability and RF keep-out | Required |
| Bluetooth | ESP32-C3 radio | Internal | 0 | No GPIO allocation | Available but not required |
| USB flash/debug | USB Serial/JTAG | USB | GPIO18/GPIO19 reserved by default | Board USB/VBUS circuit is board-specific | Observed on tested specimen |
| Recovery UART | UART0 | UART | GPIO20/GPIO21 preferred reserve when exposed | 3.3 V | Optional if native USB recovery is proven; useful fallback | Purchased board exposure `[UNVALIDATED]` |
| Onboard LED | Board-specific | Digital | 0 or 1 board-loaded GPIO | Board-specific | GPIO and polarity unknown; may conflict with boot or budget | `[UNVALIDATED]` |
| Audio impact only | GY-MAX4466 | ADC | 1 | Output must stay inside selected ADC range | Quantified only; runtime audio is not authorized | OUT OF MVP runtime |
| Minimum margin | None | Digital / ADC | 2 | 3.3 V | At least one spare must be ADC-capable | Required profile |

### 3.2 Scenario totals

| Scenario | Functional application GPIO | Required spare GPIO | Minimum board-level usable GPIO |
|---|---:|---:|---:|
| OLED + BME280 + LD2410C full duplex + MC-38 | 5 | 2 | 7 |
| OLED + DHT11/DHT22 + LD2410C full duplex + MC-38 | 6 | 2 | 8 |
| Previous scenario plus one ADC audio-impact reservation | +1 | Consumes ADC spare | 9 worst-case impact; not the mandatory active-MVP requirement |

The mandatory profile is therefore **eight board-level application GPIOs**, including:

- two I2C-capable GPIOs;
- two UART-capable GPIOs;
- one interrupt-capable digital input;
- one additional digital GPIO for a DHT-class option;
- two spare GPIOs, at least one ADC-capable.

ESP32-C3 peripherals can be routed through the GPIO matrix, but a theoretical route does not override flash, USB, strapping, debugging or board-circuit constraints.

### 3.3 Preliminary candidate mapping

This is an allocation model for compatibility review, not an approved wiring specification.

| GPIO | Candidate role | Classification | Rationale / limitation |
|---:|---|---|---|
| GPIO0 | I2C SDA for OLED and possible BME280 | Candidate | ADC-capable; prototype observed |
| GPIO1 | I2C SCL for OLED and possible BME280 | Candidate | ADC-capable; prototype observed |
| GPIO2 | DHT data in previous prototype | Conditional / strapping | Prototype worked, but ESP32-C3 boot guidance requires caution and normally recommends the correct startup level; do not freeze this mapping before power-cycle evidence |
| GPIO3 | DHT alternative or digital spare | Candidate | Prototype observed as status LED output; external board LED relationship unknown |
| GPIO4 | ADC spare | Candidate | ADC1_CH4; audio use remains unauthorized |
| GPIO5 | LD2410C TX to MCU RX | Candidate | Prototype observed at 256000 baud |
| GPIO6 | MCU TX to LD2410C RX or MC-38 alternative | Candidate | Prototype observed as MC-38 input; full-duplex radar path not yet tested |
| GPIO7 | MC-38 candidate | `[UNVALIDATED]` | Must be physically exposed and tested on purchased board |
| GPIO8 | No application allocation by default | Avoid / strapping | Boot/ROM-message strapping; often board-loaded by LED on documented DevKitC-02 |
| GPIO9 | BOOT / download mode | Reserved | Strapping and recovery path |
| GPIO10 | Digital spare | `[UNVALIDATED]` | Purchased-board exposure must be verified |
| GPIO11–GPIO17 | No application allocation | Reserved / unavailable depending on chip variant | Flash/power restrictions vary by ESP32-C3 part number |
| GPIO18/GPIO19 | Native USB Serial/JTAG | Reserved | Default USB D-/D+ path |
| GPIO20/GPIO21 | UART0 recovery reserve | `[UNVALIDATED]` on purchased board | Documented on official DevKitC-02; purchased-board exposure unknown |

The previous prototype used GPIO2 for DHT11 and operated. That is evidence of one successful configuration, not sufficient power-cycle and recovery evidence for a final reference mapping.

---

## 4. Electrical and Power Constraints

### 4.1 Chip-level constraints

According to the ESP32-C3 Series Datasheet v2.4:

- recommended ESP32-C3 power-domain input is 3.0–3.6 V, nominally 3.3 V;
- GPIO inputs must not be treated as 5 V tolerant;
- GPIO2, GPIO8 and GPIO9 are strapping pins;
- GPIO18 and GPIO19 default to USB Serial/JTAG;
- GPIO4–GPIO7 are associated with JTAG functions and GPIO20/GPIO21 with UART0, requiring deliberate allocation;
- some variants allocate GPIO to in-package flash and expose fewer general-purpose pins;
- Wi-Fi TX peak reaches 335 mA under the listed 802.11b 1 Mbps, 21 dBm chip test condition;
- the advertised 5 µA deep-sleep figure is a chip-level figure.

These values do not prove the purchased board regulator capacity, USB path, brownout margin, complete-node peak, sleep current or battery autonomy.

### 4.2 Board-level unknowns

Before the purchased SuperMini-compatible board may be accepted, execution evidence must identify:

- exact ESP32-C3 part marking or reliable `esptool` identity for each reference batch;
- PCB front and back fingerprint;
- USB connector type and wiring;
- native USB versus an added USB-UART bridge;
- 5 V input path;
- regulator part number and rated/thermal capability;
- power LED and user LED GPIO or rail loading;
- BOOT and RESET circuits;
- exposed 3.3 V and 5 V pins;
- dimensions and antenna keep-out;
- board current in representative idle, Wi-Fi transmit and reset conditions.

Until measured, IHAP-49 must use a conservative preliminary compute-board current assumption and maintain board/node consumption as `[UNVALIDATED]`.

### 4.3 Preliminary current inputs for IHAP-49

| Item | Preliminary assumption | Evidence meaning |
|---|---|---|
| ESP32-C3 chip Wi-Fi peak | Up to 335 mA under one specified RF TX condition | Datasheet ceiling input; not measured board consumption |
| ESP32-C3 chip deep sleep | 5 µA | Chip-only reference; not usable as complete-node autonomy input |
| Board regulator quiescent current | `[UNVALIDATED]` | Regulator not identified |
| Board power/user LED current | `[UNVALIDATED]` | LED circuit not identified |
| OLED current | `[UNVALIDATED]` | Must be measured with representative screen content |
| LD2410C current | Deferred to IHAP-46/IHAP-49 | Must use exact module evidence |
| Environmental sensor current | Deferred to IHAP-45/IHAP-49 | Depends on selected sensor/module |
| MC-38 current | Passive contact; pull-network current `[UNVALIDATED]` | Circuit determined in IHAP-47/IHAP-50 |
| Complete-node peak and steady state | `[UNVALIDATED]` | Requires integrated bench measurement |

No battery-autonomy result may be derived from this table.

---

## 5. Alternatives Considered

### 5.1 Evaluation method

A candidate must first pass these hard gates:

| Gate | Requirement |
|---|---|
| G1 | Integrated 2.4 GHz Wi-Fi |
| G2 | 3.3 V GPIO compatibility and a documentable power path |
| G3 | At least eight board-level application GPIOs satisfying I2C, UART, digital interrupt, optional DHT and ADC margin |
| G4 | Officially maintained SDK/toolchain suitable for C/C++ and CI |
| G5 | Reproducible flashing and recovery |
| G6 | Identifiable board/SKU or an enforceable equivalence profile |

Cost cannot compensate for failure of a mandatory gate.

The following weighted criteria are retained for a later evidence-complete score:

| Criterion group | Weight |
|---|---:|
| GPIO, peripherals and electrical compatibility | 25% |
| Reproducibility, documentation and variant control | 25% |
| Toolchain, maintainability and firmware portability | 15% |
| Power characteristics and evidence quality | 15% |
| Dimensions and enclosure impact | 10% |
| Replication cost and availability | 10% |

No weighted total is published in this Proposed ADR because the exact SuperMini SKU and normalized current prices are incomplete. A numerical ranking would create false precision.

### 5.2 Comparison matrix

| Platform | Mandatory interfaces | Radio | Flash/debug | Documentation and variant control | Power / size | Cost evidence | Outcome |
|---|---|---|---|---|---|---|---|
| Purchased ESP32-C3 SuperMini-compatible board | Likely sufficient; GPIO0–GPIO6 observed; complete 8-pin safe budget not yet proven | Wi-Fi + BLE at chip level | 4 MB XMC embedded flash and native USB Serial/JTAG observed on one specimen | Weak until seller, listing, PCB, regulator and full pinout are identified | Compact direction; exact dimensions and board consumption absent | Historical €2.9167/unit; current replication price absent | Preferred compact candidate, conditional `[UNVALIDATED]` |
| ESP32-C3-DevKitC-02 | GPIO0–GPIO10 and GPIO18–GPIO21 are documented; UART, I2C and ADC profile sufficient with strapping care | Wi-Fi + BLE | 4 MB module flash; USB-to-UART bridge; BOOT and RESET documented | Strong: official user guide, schematic, PCB layout and dimensions | Larger and Micro-USB; 5 V-to-3.3 V LDO documented | Current landed price not yet normalized | Documented fallback and qualification control |
| ESP32 DevKit V1 / ESP-WROOM-32 class | GPIO and peripheral capacity sufficient | Wi-Fi + Bluetooth Classic/BLE depending on exact module | USB-UART common; clone details vary | Official DevKitC exists, but “DevKit V1” clone identity is highly variable | Larger; extra resources not required | Project has one historical unit but no normalized comparable price | Rejected for current MVP unless ESP32-C3 becomes infeasible |
| ESP32-S3 development board | Far exceeds GPIO/peripheral requirement: 45 theoretical GPIO, 3 UART, 2 I2C, up to 20 ADC channels | Wi-Fi + BLE | USB OTG and USB Serial/JTAG available | Strong for official boards | More compute, interfaces and potential power/enclosure complexity than required | Current normalized price absent | Rejected as overengineering for current scope |
| Raspberry Pi Pico W | 26 GPIO, 3 ADC inputs, 2 UART and 2 I2C satisfy interface budget | 2.4 GHz Wi-Fi + Bluetooth 5.2 | Drag-and-drop USB programming; separate debug-probe path for full debug | Very strong official documentation, design files and production statement through at least January 2036 | 51 × 21 mm; different power and enclosure profile | Official target price $6 at check date; local landed price not normalized | Rejected because changing SDK/ecosystem provides no required MVP benefit |
| ESP8266EX / ESP8266 board | Possible basic Wi-Fi telemetry but weaker GPIO/ADC and board constraints | Wi-Fi only | Legacy tooling and board variability | Espressif marked ESP8266EX Not Recommended for New Designs in datasheet v7.1 | No decisive advantage for this architecture | Low price cannot override lifecycle gate | Rejected legacy candidate |

### 5.3 Why not a Linux SBC at every room node

A Linux SBC is excluded as disproportionate because the node requires deterministic sensor I/O, local display output and Wi-Fi event production, not a general-purpose operating system. A per-room SBC would add storage, boot, patching, process supervision, filesystem integrity, power, enclosure and replication-cost responsibilities that belong to the central-node decision or future scope.

---

## 6. Consequences

### Positive

- Preserves the current ESP-IDF and C direction.
- Uses a proportionate Wi-Fi MCU rather than a larger MCU or Linux SBC.
- Supports the mandatory OLED, environmental sensor options, LD2410C and MC-38 with a measurable GPIO profile.
- Reserves full-duplex UART so Bluetooth is not silently converted into a requirement.
- Separates stable chip-family architecture from replaceable board implementation.
- Provides a documented official fallback when a generic compact board cannot be reproduced.
- Makes GPIO, USB, boot, power and replacement constraints explicit before IHAP-45 through IHAP-50 finalize their decisions.

### Negative / Trade-offs

- The purchased board cannot yet be approved as the exact reference board.
- Physical identification and bench evidence are still required.
- Eight safe application GPIOs leave limited margin compared with ESP32-S3 or larger boards.
- The compact board may force tighter interconnect and enclosure constraints.
- Native USB, strapping pins and onboard LEDs can create board-specific recovery conflicts.
- A generic SuperMini listing may silently change PCB, regulator, flash package or LED mapping.
- The official DevKitC-02 fallback is larger and likely more expensive after landed cost is normalized.

### Neutral / Operational

- Bluetooth remains available in silicon but is not enabled or required by this decision.
- Secure-boot and flash-encryption hardware capabilities are not security claims and are not configured by this ADR.
- GPIO mapping remains provisional until sensor and interconnect tasks complete.
- The OLED inclusion creates I2C, power and enclosure requirements but does not require a separate compute ADR.
- The firmware flash-size mismatch previously observed—4 MB physical flash with a 2 MB image header—belongs to future firmware configuration work and does not alter this hardware decision.

---

## 7. Qualification Gates and Rejection Conditions

### 7.1 Purchased-board qualification

The purchased SuperMini-compatible board may become the exact reference only when all of the following evidence exists:

```text
[ ] Seller, listing URL, order date and advertised variant are recorded.
[ ] Front and back PCB photographs identify a repeatable fingerprint.
[ ] ESP32-C3 part/revision and 4 MB-or-greater flash are verified.
[ ] Complete exposed pinout is verified against the physical PCB.
[ ] At least eight application GPIOs meet the budget without unsafe boot conflicts.
[ ] GPIO7/GPIO10 or equivalent margin pins are physically exposed and tested.
[ ] USB flashing, console and recovery work with representative peripherals attached.
[ ] Regulator, input path, 3.3 V rail and onboard LED circuits are identified.
[ ] Board dimensions, header spacing and antenna keep-out are recorded.
[ ] Representative idle, reset and Wi-Fi peak board-current evidence is recorded.
[ ] A dated current replication listing is available for the same or provably equivalent revision.
[ ] The OLED and selected sensor bus do not create incompatible pull-up or voltage conditions.
```

### 7.2 Conditions that reject the purchased board

The board is rejected as the definitive reference when any of these conditions remains material:

- exact revision cannot be distinguished or repurchased;
- fewer than eight safe application GPIOs are available;
- required pins depend on uncontrolled strapping levels;
- the board exposes 5 V signals to ESP32-C3 inputs without suitable interfacing;
- regulator/rail evidence cannot support the integrated node current envelope;
- USB or recovery becomes unreliable with representative wiring;
- onboard LED or boot circuits consume required pins without a stable workaround;
- replacement units under the same listing materially change pinout or circuitry;
- landed replication cost approaches a documented official board without compensating compactness benefit;
- enclosure or interconnect becomes revision-specific and cannot be captured by an equivalence profile.

When rejected at board level, the ESP32-C3 family remains the proposed platform and ESP32-C3-DevKitC-02 becomes the default documented fallback candidate. A different chip family still requires a superseding ADR.

---

## 8. Replacement and Supersession Policy

### 8.1 Board-level equivalent replacement

A replacement board may be treated as equivalent without a new platform ADR only when it:

- uses an ESP32-C3 variant supported by the selected ESP-IDF baseline;
- provides at least 4 MB flash;
- provides at least eight safe application GPIOs with the required I2C, UART, digital-input and ADC profile;
- preserves 3.3 V GPIO and compatible 5 V/USB power input behavior;
- provides repeatable flashing, console and recovery;
- has documented boot/strapping, onboard LED and debug behavior;
- stays inside the current assumptions passed to IHAP-49;
- has enclosure and connector effects handled by IHAP-50 and IHAP-51;
- does not require a different firmware architecture or broaden MVP scope;
- has a dated source and identifiable hardware revision.

A board replacement may require wiring or enclosure revisions even when it does not require a new platform ADR.

### 8.2 Platform-level change

A move to ESP32 classic, ESP32-S3, RP2040/RP2350, ESP8266, Linux SBC or another MCU family must supersede this ADR because it changes toolchain, porting, power, debug, replacement and maintenance assumptions.

---

## 9. Inputs to Dependent Tasks

| Task | Input produced by this ADR |
|---|---|
| IHAP-45 — Environmental Sensor | I2C is mandatory for OLED; BME280 can share the bus only after voltage/address/pull-up validation; DHT adds one GPIO; environmental option must fit the eight-pin budget |
| IHAP-46 — Presence Sensor | Reserve one full-duplex UART; sensor UART levels and 5 V supply must be verified; Bluetooth is not a required configuration path; current feeds IHAP-49 |
| IHAP-47 — Door State Sensor | Reserve one interrupt-capable 3.3 V input; avoid uncontrolled strapping behavior; pull/debounce/cable circuit remains downstream |
| IHAP-48 — Audio Disposition | One ADC pin exists only as an impact/margin item; no audio runtime is authorized; physical removal remains the preferred minimal privacy posture for that task to decide |
| IHAP-49 — Power Subsystem | Use 335 mA only as a chip RF peak input, not board/node peak; regulator, OLED, radar and integrated consumption remain `[UNVALIDATED]`; do not estimate autonomy yet |
| IHAP-50 — Interconnect | Produce final wiring from the accepted board pinout; OLED requires VCC, GND, SDA and SCL; distinguish native USB/recovery access from application wiring |
| IHAP-51 — Enclosure | Preserve antenna keep-out, USB/BOOT/RESET access and visible OLED aperture; exact dimensions depend on qualified board and OLED modules |
| IHAP-17 — Cost/BOM | Keep board and OLED prices as historical snapshots; do not mark definitive hardware or replication totals until Project Owner acceptance and current price evidence |

---

## 10. Related Risks and Treatments

| Risk | Treatment | Effect | Remaining exposure |
|---|---|---|---|
| [R-001 — Device Identity Spoofing](../risks/records/R-001-device-identity-spoofing.md) | None created by this ADR | Leaves unresolved | Board family contains security hardware, but device identity and registry behavior remain target/runtime work `[UNVALIDATED]` |
| [R-004 — Presence and Door State Misinterpretation](../risks/records/R-004-presence-door-state-misinterpretation.md) | Existing claim/scope controls | Leaves unresolved | Compute capacity does not authorize tracking, alarm, access-control or protection semantics |
| [R-005 — Target Boundary Overclaim](../risks/records/R-005-target-boundary-overclaim.md) | Preserve Proposed and `[UNVALIDATED]` wording | Partially mitigates | Hardware feasibility does not prove firmware, HTTP/JSON, backend or mobile runtime |
| [R-010 — Risk-Driven Scope Creep](../risks/records/R-010-risk-driven-scope-creep.md) | Hard non-scope and equivalence gates | Partially mitigates | Future security, audio, Bluetooth or power work still requires separate approved scope |

No current Risk Record specifically covers generic-board variant drift, unidentified regulators, GPIO/boot incompatibility or electrical reproducibility. This ADR records the evidence gap but does not create a new risk or treatment task automatically.

---

## 11. Follow-up Work

| Item | Tracking |
|---|---|
| Recover exact SuperMini order/listing and seller evidence | IHAP-44 before Project Owner exact-board decision |
| Photograph and fingerprint all purchased boards | IHAP-44 evidence checkpoint |
| Verify exposed GPIO, regulator, LED, buttons, dimensions and recovery | IHAP-44 bench evidence |
| Capture current dated replication prices and stock for the exact board and fallback | IHAP-44 / IHAP-17 after architecture decision |
| Decide environmental interface and exact sensor | IHAP-45 |
| Decide LD2410C interface, levels, power and Bluetooth disposition | IHAP-46 |
| Decide MC-38 circuit and final input pin | IHAP-47 |
| Decide GY-MAX4466 physical disposition | IHAP-48 |
| Produce complete measured current and power architecture | IHAP-49 |
| Freeze final wiring and per-node quantities | IHAP-50 |
| Freeze enclosure aperture, board mounting and antenna keep-out | IHAP-51 |
| Correct firmware flash-size configuration if the qualified board remains 4 MB | Future firmware implementation task; not introduced here |

---

## 12. Evidence Links

| Evidence | Link |
|---|---|
| Jira issue | [IHAP-44](https://niccolopiazzi01.atlassian.net/browse/IHAP-44) |
| Parent hardware decision gate | [IHAP-43](https://niccolopiazzi01.atlassian.net/browse/IHAP-43) |
| Pull request | Pending |
| Cost/BOM draft baseline | [IHAP-17](https://niccolopiazzi01.atlassian.net/browse/IHAP-17) and Draft PR #22 |
| Product boundary | [`docs/product/product-vision.md`](../product/product-vision.md) |
| Cost governance | [`docs/governance/cost-governance-and-bom-policy.md`](../governance/cost-governance-and-bom-policy.md) on the IHAP-17 draft branch until merged |
| ADR policy | [`docs/adr/README.md`](README.md) |
| ESP32-C3 datasheet v2.4 | https://www.espressif.com/documentation/esp32-c3_datasheet_en.pdf |
| ESP32-C3 stable ESP-IDF v6.0.2 documentation | https://docs.espressif.com/projects/esp-idf/en/stable/esp32c3/get-started/index.html |
| ESP32-C3-DevKitC-02 official guide | https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32c3/esp32-c3-devkitc-02/user_guide.html |
| ESP32-S3 datasheet v2.2 | https://www.espressif.com/documentation/esp32-s3_datasheet_en.pdf |
| ESP8266EX datasheet v7.1 / NRND | https://www.espressif.com/documentation/0a-esp8266ex_datasheet_en.pdf |
| Raspberry Pi Pico family official product page | https://www.raspberrypi.com/products/raspberry-pi-pico/ |
| Runtime specimen evidence | Project Owner supplied log and firmware during IHAP-44 planning; sensitive identifiers omitted; durable repository artifact still missing |
| Related Risk Records | `docs/risks/records/R-001-*`, `R-004-*`, `R-005-*`, `R-010-*` |
| Related treatments | None introduced by IHAP-44 |
| Related ADRs | None |

---

## 13. Review Notes

### 13.1 Architecture Regression Reviewer

- ESP32-C3 family and exact board implementation are separated.
- OLED inclusion is bounded as local display hardware, not a new data or automation feature.
- Bluetooth, audio, Linux-per-node and larger MCU capabilities are not silently added.
- No runtime or maturity claim is introduced.

### 13.2 Hardware Compatibility Reviewer

- The decision uses board-level usable GPIO rather than theoretical chip GPIO.
- Flash, USB, strapping, JTAG, UART0 and onboard loads are explicit.
- The previous GPIO2 DHT mapping remains conditional because GPIO2 is a strapping pin.
- Voltage, regulator and integrated current evidence remain blocking for exact-board approval.

### 13.3 Testing & Evidence Reviewer

- Runtime evidence is explicitly specimen-specific.
- Missing seller, PCB, regulator, complete pinout and price evidence remain `[UNVALIDATED]`.
- No autonomy, reliability or full-node consumption claim is made.
- The exact purchased board must not become Accepted solely from the current evidence package.

### 13.4 Cost Governance Reviewer

- Historical acquisition price is separated from current replication price.
- Zero-price inventory does not become a universal price.
- No weighted cost ranking is published while comparable landed prices are incomplete.
- IHAP-17 is linked but not modified or approved.

### 13.5 Source of Truth Guardian

- One ADR contains the platform decision, matrix, GPIO budget, electrical constraints and replacement policy.
- No duplicate GPIO, USB, power or OLED ADR is created.
- Jira remains workflow/evidence coordination; Confluence remains unchanged.

### 13.6 Security & Privacy Reviewer

- Radio and debug surfaces are disclosed without security certification claims.
- Raw audio remains blocked.
- Presence and door state remain telemetry-only.
- Bluetooth availability is not treated as authorization or requirement.

### 13.7 Final checklist

```text
[x] One stable architectural decision scope.
[x] ADR necessity is explicit.
[x] OLED 0.96-inch 128×64 inclusion is reflected in the compute requirements.
[x] At least six realistic platform alternatives are addressed.
[x] GPIO and peripheral budget is board-level and scenario-based.
[x] Electrical constraints separate chip data from board/node evidence.
[x] Preliminary current assumptions are explicitly non-measured.
[x] Replacement and rejection conditions are explicit.
[x] Related risks are linked without claiming closure or acceptance.
[x] GitHub remains the technical source of truth.
[x] Jira remains the task, blocker and evidence-link surface.
[x] Confluence is not duplicated or modified.
[x] IHAP-17 is not modified.
[x] MVP boundary is not silently expanded.
[x] [UNVALIDATED] is preserved on unproven claims.
[x] No production-ready, commercial-ready, security-grade, certified, safety-critical, alarm-grade, antifurto, access-control, intrusion-detection or protection claim is introduced.
[x] Project Owner decision is required before any status beyond Proposed.
```
