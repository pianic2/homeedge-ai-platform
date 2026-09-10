# IHAP-50 — Interconnect and Prototype Assembly Specification

**Status:** Proposed technical baseline — Project Owner approval pending  
**Issue:** IHAP-50 — Interconnect and Prototype Assembly Decision  
**Parent:** IHAP-43 — MVP Hardware Component Decision Baseline  
**Implementation consumer:** IHAP-55 — Integrated Modular Edge PCB  
**Mechanical consumer:** IHAP-51 — Edge Enclosure and Mounting Decision  
**Cost consumer:** IHAP-17 — Cost Governance and BOM Policy

<!--
AI_AGENT_METADATA:
  document_type: hardware_interconnect_specification
  issue: IHAP-50
  source_of_truth: github_versioned_repository_documentation
  status: proposed_until_project_owner_approval
  custom_pcb_direction: accepted_by_adr_0007
  breadboard_status: validation_only
  dupont_status: validation_only
  audio_gpio_allocation: 0
  audio_adc_allocation: 0
  audio_connector_allocation: 0
  machine_readable_matrix: docs/architecture/ihap-50-connection-matrix.json
  gpio_mapping_revision: 2
  unvalidated_claim_marker: "[UNVALIDATED]"

HIDDEN_ANTI_REGRESSION_RULES:
  - Preserve Accepted ADR-0001, ADR-0002, ADR-0003, ADR-0004, ADR-0005 and the Accepted baseline of ADR-0007.
  - Do not promote the Proposed IHAP-56 amendment package to Accepted by implication.
  - Keep the custom core PCB as the accepted final-reference direction; breadboard and Dupont remain validation/development-only.
  - Keep GPIO2, GPIO8 and GPIO9 outside the reference application allocation because they are ESP32-C3 strapping pins.
  - Keep GPIO20 and GPIO21 free for UART0/recovery when practical.
  - Preserve one real ADC-capable spare GPIO as required by ADR-0001.
  - Keep product presence output boolean-only and door state telemetry-only.
  - Do not allocate audio GPIO, ADC, connector, aperture or wiring in the reference MVP.
  - Do not treat generic PH2.0 naming as proof of a controlled connector manufacturer/series or universal mating compatibility.
  - Preserve [UNVALIDATED] on unmeasured pull-up interaction, final harness cut lengths, PCB electrical behavior and production maturity.
-->

---

## 1. Purpose and boundary

This document freezes the **logical and electrical interconnect contract** that the custom edge-node PCB must consume. It separates four maturity layers:

1. **validation/development assembly** — breadboard, Dupont jumpers and temporary fixture wiring;
2. **reference interconnect contract** — stable nets, GPIO allocation, connector roles, polarity and passive requirements;
3. **custom PCB implementation** — schematic, layout, protection devices, test points and final board implementation owned by IHAP-55;
4. **enclosure-dependent mechanics** — final harness cut lengths, strain-relief geometry and mounting owned by IHAP-51.

The specification does not reopen accepted sensor or power decisions. It converts them into one reproducible interface model.

No production-ready, certified, safety-grade, alarm-grade, antifurto, access-control or commercial-ready claim is created.

---

## 2. Upstream accepted constraints

| Source | Accepted constraint consumed here |
|---|---|
| ADR-0001 / IHAP-44 | ESP32-C3 family; 3.3 V GPIO; one I2C bus; one full-duplex UART; one interrupt-capable digital input; one spare ADC-capable GPIO; at least eight safe application GPIO. GPIO2/8/9 excluded from the conservative application baseline. GPIO20/21 should remain available for UART0/recovery when practical. |
| ADR-0002 / IHAP-45 | DHT11 standard indoor profile; BME280 precision/extended profile; both accepted validation paths used 3.3 V; final wiring belongs to IHAP-50. |
| ADR-0003 / IHAP-47 | Passive two-conductor reed contact. FAR/open -> HIGH; NEAR/closed -> LOW under pull-up topology. Open contact and interrupted conductor are electrically indistinguishable. |
| ADR-0004 / IHAP-53 | 0.96-inch-class 128x64 monochrome I2C OLED on 3.3 V. Reference address 0x3C. BME280 and OLED should share one I2C bus when the precision profile is used. |
| ADR-0005 / IHAP-46 | HLK-LD2410C-class radar. Accepted evidence uses 5 V supply and receive-only UART at 256000 baud. Product/event output remains boolean presence only. |
| IHAP-48 | Audio is outside the reference MVP: zero GPIO, zero ADC, zero connector and zero wiring allocation. |
| ADR-0007 / IHAP-49 | Regulated 5 V product bus, regulated 3.3 V domain, USB-C normal source plus 1S backup, custom core PCB as final reference direction. |
| IHAP-56 / PR #35 | Remediation merged. Any controls explicitly marked Proposed remain Proposed until explicit Project Owner approval. |

Primary references for the electrical mapping are the current Espressif ESP32-C3 datasheet/hardware guidelines plus the manufacturer documentation already linked by the accepted sensor ADRs.

---

## 3. Physical maturity decision

### 3.1 Breadboard

**Validation/development-only.** A solderless breadboard may reproduce sensor tests and debug interfaces, but it is not part of the final reference node and must not be presented as installable hardware.

### 3.2 Dupont jumpers

**Validation/development-only.** Loose Dupont jumpers are acceptable on the bench but rejected for the final installable reference because they are unkeyed, easy to reverse/dislodge and provide no deterministic strain relief.

### 3.3 Perfboard / stripboard

**Optional intermediate prototype only.** Use only if it removes a concrete temporary integration blocker. Do not create a second quasi-final architecture between breadboard and the accepted custom PCB direction.

### 3.4 Custom core PCB

**Accepted direction from ADR-0007.** The custom PCB is no longer FUTURE. IHAP-55 must implement this contract or document a reviewed remap without weakening upstream constraints.

---

## 4. Reference GPIO allocation — revision 2

The mapping is optimized around these invariants:

- do not allocate strapping pins GPIO2, GPIO8 or GPIO9;
- keep GPIO20/21 available for UART0/recovery when practical;
- keep two application GPIO as engineering margin;
- ensure that one spare is **actually ADC-capable**.

Espressif maps ADC capability on ESP32-C3 to GPIO0–GPIO5. The first IHAP-50 draft incorrectly labelled GPIO10 as ADC-capable. Static review classified that as **MAJOR** and remediated it before any integrated gate or PCB handoff.

### 4.1 Corrected reference allocation

| GPIO | Reference net | Direction | Rationale |
|---:|---|---|---|
| GPIO0 | `RADAR_RX_FROM_LD2410C_TX` | input | Dedicated LD2410C receive path at 256000 baud. |
| GPIO1 | `RADAR_TX_TO_LD2410C_RX_SERVICE_ONLY` | output | Optional service/configuration direction; disabled by default. |
| GPIO3 | `DOOR_SENSE` | input | Reed-contact input with controlled external pull-up. |
| GPIO4 | `ENV_DHT_DATA` | bidirectional single-wire | Standard DHT11 profile data line. |
| GPIO5 | `SPARE_ADC_CAPABLE` | spare | Real ADC-capable engineering margin; ESP32-C3 ADC2_CH0. |
| GPIO6 | `I2C_SDA` | bidirectional open-drain | Shared OLED/BME280 data bus. |
| GPIO7 | `I2C_SCL` | bidirectional open-drain | Shared OLED/BME280 clock bus. |
| GPIO10 | `SPARE_DIGITAL` | spare | Digital/routing engineering margin. |

### 4.2 Reserved / protected pins

| GPIO | Reference disposition |
|---:|---|
| GPIO2 | Do not allocate — strapping pin. |
| GPIO8 | Do not allocate — strapping pin. |
| GPIO9 | Do not allocate — strapping/boot pin. |
| GPIO20 | Keep available for UART0/recovery when practical. |
| GPIO21 | Keep available for UART0/recovery when practical. |

GPIO4/5/6/7 overlap external JTAG functions. The reference node prioritizes application I/O there and retains the native USB Serial/JTAG and boot/recovery path. IHAP-55 must prove reproducible flashing, reset and recovery with the selected implementation.

The ESP32-C3 GPIO matrix allows the I2C peripheral signals to be routed to GPIO6/GPIO7; therefore moving I2C away from the historical GPIO5/GPIO6 validation fixture does not change the accepted I2C architecture.

A PCB routing remap is allowed only if IHAP-55 records the reason and preserves: the logical net contract, safe boot behavior, recovery capability, one ADC-capable spare and a second engineering-margin GPIO.

---

## 5. Canonical connection matrix

| Module / function | Power | Signals | Reference connector | Notes |
|---|---|---|---|---|
| ESP32-C3 core | `SYS_3V3` | GPIO nets below | PCB internal | Exact module/chip implementation owned by IHAP-55. |
| LD2410C | `SYS_5V`, GND | TX -> GPIO0; optional RX <- GPIO1 | `J_RADAR`, 4 positions | Runtime receive-only path is sufficient for accepted presence acquisition. `OUT` has no MVP allocation. |
| OLED | `SYS_3V3`, GND | GPIO7 SCL, GPIO6 SDA | `J_OLED`, 4 positions | Reference address 0x3C. |
| DHT11 profile | `SYS_3V3`, GND | GPIO4 data | `J_ENV`, 5 positions | Standard indoor profile. |
| BME280 profile | `SYS_3V3`, GND | GPIO7 SCL, GPIO6 SDA | `J_ENV`, 5 positions | Precision profile; shares I2C with OLED. |
| MC-38-class reed | no sensor supply; GND reference | GPIO3 `DOOR_SENSE` | `J_DOOR`, 2 positions | Passive contact; no tamper/wire-supervision semantics. |
| Audio | none | none | none | Explicitly outside reference MVP. |

### 5.1 `J_RADAR`

Board-side logical order:

1. GND
2. `SYS_5V`
3. `RADAR_RX_FROM_LD2410C_TX`
4. `RADAR_TX_TO_LD2410C_RX_SERVICE_ONLY`

The module-side harness must map against the actual module pin labels; cable color is never authoritative. LD2410C `OUT` is intentionally not allocated. Existence of the service TX line does not authorize new product semantics or persistent detailed radar telemetry.

### 5.2 `J_OLED`

Board-side logical order:

1. GND
2. `SYS_3V3`
3. `I2C_SCL`
4. `I2C_SDA`

Equivalent displays must adapt to this logical order; appearance alone does not prove identical pin order.

### 5.3 `J_ENV`

One five-position board interface supports either accepted environmental profile:

1. GND
2. `SYS_3V3`
3. `ENV_DHT_DATA`
4. `I2C_SCL`
5. `I2C_SDA`

Profile use:

- DHT11: pins 1/2/3; 4/5 NC at module harness;
- BME280: pins 1/2/4/5; 3 NC at module harness.

This keeps one scalable PCB interface without pretending the two sensor protocols are interchangeable.

### 5.4 `J_DOOR`

1. GND
2. `DOOR_SENSE`

The contact closes `DOOR_SENSE` to ground. It is not a powered sensor interface.

---

## 6. Bus and passive rules

### 6.1 I2C — OLED + BME280

Reference bus:

- SDA = GPIO6;
- SCL = GPIO7;
- bus voltage = `SYS_3V3` only;
- OLED accepted reference address = `0x3C`;
- BME280 accepted specimen address = `0x76`;
- no address collision exists in the accepted evidence set.

PCB requirements:

- footprints for `R_I2C_SDA` and `R_I2C_SCL`;
- candidate value **4.7 kOhm to `SYS_3V3`**;
- final population must account for pull-ups already present on the selected OLED/BME280 modules;
- no I2C line may be pulled to 5 V;
- actual equivalent pull-up resistance, rise time and simultaneous bus behavior remain `[UNVALIDATED]` until measured with the selected modules.

Reference internal harness target: <=150 mm from board to each I2C module. Longer routing requires explicit integrated evidence. Final exact cut lengths belong to IHAP-51.

### 6.2 DHT11

Reference contract:

- supply = `SYS_3V3`;
- data = GPIO4;
- provide a board pull-up footprint targeting an effective value around **5.1 kOhm to `SYS_3V3`**;
- if the selected three-pin breakout already contains a pull-up, final population must avoid an unnecessarily strong parallel network;
- provide local 100 nF decoupling at the environment interface unless the final schematic demonstrates an equivalent local decoupling path.

The owned DHT11 validation path has already operated at 3.3 V. Exact onboard pull-up value on the selected breakout remains `[UNVALIDATED]` until measured/identified.

### 6.3 MC-38 reed input

Proposed reference topology:

```text
SYS_3V3
   |
  10k
   |
DOOR_SENSE ---- 1k series ---- ESP32-C3 GPIO3
   |
 reed contact
   |
  GND
```

Proposed passives:

- `R_DOOR_PULLUP = 10 kOhm` to `SYS_3V3`;
- `R_DOOR_SERIES = 1 kOhm` close to the MCU input;
- `C_DOOR_FILTER = 100 nF` footprint, DNP by default; populate only if integrated noise/bounce evidence justifies it.

Logical behavior remains FAR/open -> HIGH and NEAR/closed -> LOW. An interrupted conductor remains indistinguishable from a legitimate open contact. No fault/tamper state is introduced.

### 6.4 LD2410C UART

Reference runtime path:

- supply = regulated `SYS_5V`;
- common ground mandatory;
- module TX -> GPIO0;
- baud = 256000;
- GPIO1 -> module RX only as service/configuration path, disabled by default;
- module `OUT` unallocated.

The owned specimen has evidence for its receive-only TX-to-ESP32 path. Replacement electrical equivalence remains `[UNVALIDATED]` until a replacement profile is reviewed.

---

## 7. Connector strategy

The owned `PH2.0`-labelled kit is acceptable as prototype inventory, but the generic label is not a controlled manufacturer series and does not prove universal mating compatibility.

For the custom PCB, a PH2.0-style family is acceptable only after IHAP-55 freezes:

- exact board header/footprint;
- mating housing/contact;
- pitch and orientation;
- polarity/keying;
- current capability for the connected module;
- crimp/assembly method;
- replacement source.

Reference classes:

| Connection | Preferred class | Rationale |
|---|---|---|
| Radar | keyed/polarized 4-position low-voltage connector | Carries 5 V + UART. |
| OLED | keyed/polarized 4-position low-voltage connector | Front-panel/serviceable module. |
| Environment | keyed/polarized 5-position low-voltage connector | One port supports either accepted environmental profile. |
| Door | keyed/polarized 2-position connector; terminal-block fallback | Passive field-mounted cable; terminal block only if IHAP-51 demonstrates serviceability need. |

Wire color must not encode the only polarity information.

---

## 8. Wire and harness rules

### Validation/development

- Dupont permitted;
- keep runs short and visible;
- remove power before rewiring;
- follow net/pin labels rather than breadboard row memory or cable colors.

### Reference PCB harness

Candidate low-voltage harness range:

- stranded copper;
- 26–28 AWG for short module harnesses, subject to the selected connector contact specification;
- prefer 26 AWG for radar 5 V/GND where the chosen contact supports it;
- exact conductor gauge must remain compatible with connector crimp range and measured load;
- internal module harness target <=150 mm unless IHAP-51 geometry requires more;
- final cut lengths remain `[UNVALIDATED]` until PCB connector placement and enclosure geometry are frozen.

Every harness leaving the PCB must receive mechanical strain relief. Solder joints alone are not strain relief.

Battery-service conductors, USB-C input routing and high-current converter paths remain IHAP-55 / ADR-0007 implementation scope.

---

## 9. Logical interconnect diagram

```mermaid
flowchart LR
    USB[USB-C / power subsystem] --> SYS5[Regulated SYS_5V]
    SYS5 --> RADAR[LD2410C]
    SYS5 --> REG33[3.3 V regulator]
    REG33 --> SYS33[SYS_3V3]
    SYS33 --> MCU[ESP32-C3]
    SYS33 --> OLED[OLED]
    SYS33 --> ENV[ENV profile]
    SYS33 --> RPULL[Door pull-up]

    MCU <-->|GPIO6 SDA / GPIO7 SCL| OLED
    MCU <-->|GPIO6 SDA / GPIO7 SCL when BME280| ENV
    MCU <-->|GPIO4 when DHT11| ENV
    MCU <-->|GPIO0 RX / GPIO1 service TX| RADAR
    DOOR[MC-38 reed] -->|GPIO3 DOOR_SENSE| MCU
    ADC[GPIO5 ADC-capable spare] --- MCU
    SPARE[GPIO10 digital spare] --- MCU
```

This is a logical interface view, not a PCB schematic.

---

## 10. Per-node allocation model

| Item | Qty / node | Rule |
|---|---:|---|
| Radar detachable interface | 1 | 4 positions |
| OLED detachable interface | 1 | 4 positions |
| Environment-profile interface | 1 | 5 positions |
| Door detachable interface | 1 | 2 positions |
| I2C pull-up footprints | 2 | population after module-network measurement |
| DHT pull-up footprint | 1 | profile-dependent population |
| Environment 100 nF decoupling | 1 | unless equivalent local decoupling is demonstrated |
| Door 10 kOhm pull-up | 1 | proposed populated baseline |
| Door 1 kOhm series resistor | 1 | proposed populated baseline |
| Door 100 nF filter footprint | 1 | DNP by default |
| Audio interface/passives | 0 | outside reference MVP |
| Breadboard | 0 final; optional bench | development only |
| Dupont wiring | 0 final; as needed bench | development only |

IHAP-17 must cost only final selected/populated per-node parts after Project Owner approval and exact IHAP-55 part selection. Bulk-kit acquisition cost must not be divided arbitrarily over unused stock.

---

## 11. Minimum integrated validation gate

Before closure, execute only the evidence that cannot be established statically:

1. **Boot/recovery:** normal boot, reset, flashing and recovery remain reproducible with all selected peripherals attached.
2. **I2C coexistence:** OLED + BME280 profile operate concurrently on GPIO6/GPIO7 without address collision or repeated bus failure.
3. **DHT profile:** DHT11 communicates on GPIO4 while OLED and radar remain active.
4. **Radar:** valid LD2410C UART frames at 256000 baud on GPIO0 while other interfaces operate.
5. **Door:** open/closed transitions map HIGH/LOW as accepted; a disconnected conductor remains HIGH and is explicitly recorded as indistinguishable from open.
6. **Engineering margin:** GPIO5 remains usable as an ADC-capable spare and GPIO10 remains free as digital margin on the exact implementation.
7. **Pull networks:** effective I2C/DHT pull-ups are measured or identified before final PCB population values are frozen.
8. **Connector review:** every powered module connector has explicit GND/supply/signal order and keyed orientation.
9. **No-audio regression:** no audio GPIO, ADC, connector or wiring exists in the reference assembly.

Quantitative rail/load/thermal/battery/source-transfer tests remain IHAP-55 under ADR-0007. Proposed IHAP-56 strengthening is not converted into an Accepted gate here.

---

## 12. Static review finding and remediation

### SR-50-01 — incorrect ADC capability in initial draft

- **Severity:** MAJOR before remediation.
- **Initial defect:** GPIO10 was labelled `SPARE_ADC_CAPABLE`.
- **Authoritative correction:** ESP32-C3 ADC-capable GPIO are GPIO0–GPIO5; GPIO10 is not ADC-capable.
- **Fix:** move shared I2C to GPIO6/GPIO7; reserve GPIO5 as `SPARE_ADC_CAPABLE`; retain GPIO10 as `SPARE_DIGITAL`.
- **Result:** ADR-0001's spare ADC capability is now preserved without consuming strapping or UART0/recovery pins.
- **Status:** REMEDIATED before integrated testing and before IHAP-55 handoff.

This finding remains recorded as evidence rather than being erased from the review history.

---

## 13. ADR necessity

**Proposed conclusion: ADR NOT REQUIRED.**

The architecture-significant component decisions already live in ADR-0001 through ADR-0007. IHAP-50 derives a reproducible implementation contract from those accepted decisions. GPIO, connector and passive allocation must remain reviewable implementation details that IHAP-55 can remap only with explicit compatibility evidence.

A new ADR becomes necessary only if a new stable cross-cutting decision changes an accepted interface architecture rather than merely implementing it.

Project Owner approval is required before this conclusion and the final specification are treated as closed IHAP-50 decisions.

---

## 14. Handoff

### IHAP-55 receives

- canonical logical net names;
- corrected reference GPIO allocation;
- reserved/boot/recovery policy;
- required preservation of a real ADC-capable spare;
- connector roles and logical pin order;
- proposed I2C/DHT/reed passive footprints;
- UART receive/service split;
- development-only breadboard/Dupont boundary;
- pull-up reconciliation and exact connector-part freeze requirements;
- minimum integrated validation gate.

### IHAP-51 receives

- four external-module interface roles;
- keyed-orientation and strain-relief requirement;
- <=150 mm internal-harness design target unless geometry proves otherwise;
- final exact harness cut-length ownership;
- radar/OLED/environment/door service-access needs.

### IHAP-17 receives after approval

- final per-node connector/harness/passive quantities;
- zero final breadboard/Dupont allocation;
- zero audio allocation;
- exact selected connector/passive prices only after IHAP-55 freezes manufacturer parts.

---

## 15. Remaining `[UNVALIDATED]`

- effective I2C pull-up network with selected OLED+BME280 modules;
- DHT breakout onboard pull-up value;
- exact connector manufacturer/series/mating compatibility;
- final harness cut lengths;
- simultaneous operation on the corrected final mapping;
- GPIO5 ADC spare usability on the exact final implementation;
- custom-PCB electrical behavior, protection, rail quality, thermal behavior and source transfer;
- replacement-lot equivalence for low-cost sensor modules.

These are implementation evidence gates, not reasons to reopen already accepted component architecture.
