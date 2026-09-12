# IHAP-55 — Integrated Modular Edge PCB — Mainboard Architecture

**Status:** IN PROGRESS — architecture candidate for Project Owner review  
**Issue:** IHAP-55  
**Started:** 2026-09-11  
**Technical SoT branch:** `ihap-55-integrated-modular-edge-pcb`  
**Baseline main:** `30e43c3c470b35b80ac513b7691b4d04ed6340ed`

## 1. Scope and approval boundary

This document begins concrete PCB implementation from the Accepted upstream contracts. It does not approve a new ADR, promote IHAP-56 Proposed controls, authorize procurement/fabrication, or declare a final reference implementation.

The Project Owner review gate remains open for the final core/module partition and any architecture supersession. Components below marked **CANDIDATE** are design selections being developed for review, not procurement authorization.

## 2. Preserved Accepted contracts

The design shall preserve:

- ESP32-C3 compute family;
- GPIO0 `RADAR_RX_FROM_LD2410C_TX` at 256000 baud;
- GPIO1 `RADAR_TX_TO_LD2410C_RX_SERVICE_ONLY`, disabled by default;
- GPIO3 `DOOR_SENSE`;
- GPIO4 `ENV_DHT_DATA`;
- GPIO5 `SPARE_ADC_CAPABLE` / ADC2_CH0;
- GPIO6 `I2C_SDA`;
- GPIO7 `I2C_SCL`;
- GPIO10 `SPARE_DIGITAL`;
- GPIO2/GPIO8/GPIO9 outside reference application allocation;
- GPIO20/GPIO21 available for UART0/recovery when practical;
- DHT11 STANDARD and BME280 PRECISION as alternative profiles;
- OLED 0.96-inch-class 128x64 monochrome I2C at 3.3 V, reference `0x3C`;
- LD2410C at 5 V with receive path at 256000 baud and boolean-only product presence boundary;
- MC-38 topology: 10 kOhm pull-up, 1 kOhm series, optional 100 nF DNP;
- audio: zero GPIO, zero ADC, zero connector, zero power allocation;
- ADR-0007 Accepted power architecture only;
- RT-R012-01 and RT-R013-01 remain Proposed.

## 3. Architecture block diagram — revision A candidate

```text
                      USB-C 5 V INPUT
                    + USB 2.0 D+/D-
                            |
             +--------------+--------------+
             |                             |
       CC sink network                 USB ESD
       + input protection                  |
             |                        ESP32-C3 USB
             v                        Serial/JTAG
      MP2636GR-P CANDIDATE                  |
 charger / power path / boost               |
      |                    |                |
      |                    +---- BATT / NTC |
      |                                  +--+-------------------+
      v                                  | ESP32-C3-MINI-1-N4X |
 intermediate SYS                         | CANDIDATE MODULE     |
      |                                  +--+-------------------+
      v                                     |
 TPS63802DLAR CANDIDATE                      + GPIO0 -> radar RX
 buck-boost post-regulator                   + GPIO1 -> radar service TX
      |                                      + GPIO3 -> door
      +---- regulated SYS_5V                 + GPIO4 -> DHT
      |         |                            + GPIO5 -> ADC spare
      |         +---- J_RADAR                + GPIO6/7 -> I2C
      |                                      + GPIO10 -> digital spare
      v
 TLV62568DBVR CANDIDATE
 3.3 V buck regulator
      |
      +---- regulated SYS_3V3
            +---- ESP32-C3 module
            +---- J_OLED
            +---- J_ENV
            +---- MC-38 pull network
```

The power converter choices are not yet electrically frozen. They must pass complete input/output/current/tolerance/thermal calculations before schematic freeze.

## 4. ESP32-C3 implementation decision candidate

### 4.1 Preferred candidate

**ESP32-C3-MINI-1-N4X — CANDIDATE.**

Rationale:

- current Espressif datasheet marks `ESP32-C3-MINI-1-N4X` Recommended;
- 4 MB flash preserves the preferred ADR-0001 capacity;
- chip revision v1.1;
- integrated crystal, in-package flash and RF matching reduce board RF risk, assembly count and sourcing complexity compared with bare-chip implementation;
- integrated PCB antenna supports the compact core-mainboard direction;
- module still exposes the accepted GPIO contract and native USB Serial/JTAG path;
- avoids reproducing the uncontrolled SuperMini development-board regulator/USB implementation.

Bare-chip ESP32-C3 is retained as a rejected-first-revision alternative because it would require RF matching/antenna design, crystal/flash implementation and materially stronger RF/layout validation without a demonstrated MVP benefit.

This core/module partition remains subject to Project Owner review before being called final.

### 4.2 Boot, recovery and USB candidate contract

- native USB Serial/JTAG via GPIO18/GPIO19;
- USB differential pair routed as controlled differential pair per Espressif guidance;
- reserve USB series-resistor footprints close to the module; initial manufacturer guideline range 22/33 Ohm remains to be resolved to one schematic value;
- retain EN reset network and dedicated RESET control;
- retain GPIO9 BOOT control without assigning GPIO9 to application I/O;
- keep GPIO20/GPIO21 available for UART0/recovery test pads/header when practical;
- reproducible download/recovery remains `[UNVALIDATED]` until fabricated-board bring-up.

## 5. Power architecture candidate

### 5.1 USB-C front end

Candidate connector: **GCT USB4105-GF-A**, USB 2.0 Type-C receptacle with data pins.

Required architecture:

- USB-C sink operation, 5 V only; no PD;
- independent Rd on CC1 and CC2 per USB-C sink requirements;
- D+/D- routed to native ESP32-C3 USB Serial/JTAG;
- dedicated USB data-line ESD protection candidate: **ST USBLC6-2SC6**;
- VBUS protection/fusing/transient network not yet frozen `[UNVALIDATED]`;
- upstream backfeed prohibited by Accepted ADR-0007.

### 5.2 Charger / system path

**MP2636GR-P — Accepted preferred first direction, implementation CANDIDATE.**

The design must not treat MP2636 input pass-through as the regulated product 5 V bus.

### 5.3 Regulated 5 V post-stage

**TPS63802DLAR — CANDIDATE only.**

Manufacturer range 1.3–5.5 V input and adjustable output up to 5.2 V makes it topologically compatible with a 5.0 V buck-boost post-stage when the upstream intermediate SYS range is constrained accordingly.

Before schematic freeze IHAP-55 must calculate and record:

- complete MP2636 intermediate-SYS min/max/tolerance envelope;
- TPS63802 allowable operating envelope at 5.0 V output;
- >=0.5 A continuous capability at accepted range endpoints;
- >=1.0 A transient/headroom feasibility;
- inductor current/saturation/RMS requirements;
- input/output capacitance and voltage derating;
- feedback tolerance and resulting SYS_5V window;
- efficiency/loss/thermal estimates.

Until those calculations pass, TPS63802 is `[UNVALIDATED]` as the final post-regulator.

### 5.4 Regulated 3.3 V

**TLV62568DBVR — CANDIDATE only.**

Manufacturer profile: 2.5–5.5 V input, adjustable buck, 1 A output. It is supplied from regulated SYS_5V, not directly from the uncontrolled MP2636 intermediate node.

Before schematic freeze IHAP-55 must calculate feedback values/tolerance, inductor/capacitor requirements, ESP32-C3 Wi-Fi peak headroom and thermal margin. Final 3.3 V acceptance band remains component-derived and `[UNVALIDATED]` until populated-load limits are frozen.

## 6. External interface connector candidate freeze

The previous generic `PH2.0` label is replaced with a controlled first candidate ecosystem for low-power sensor interfaces:

| Interface | Board header candidate | Housing | Crimp contact | Logical pin order |
|---|---|---|---|---|
| `J_RADAR` | JST `B4B-PH-K-S` | `PHR-4` | `SPH-002T-P0.5S` | 1 GND; 2 SYS_5V; 3 RADAR_RX; 4 RADAR_SERVICE_TX |
| `J_OLED` | JST `B4B-PH-K-S` | `PHR-4` | `SPH-002T-P0.5S` | 1 GND; 2 SYS_3V3; 3 I2C_SCL; 4 I2C_SDA |
| `J_ENV` | JST `B5B-PH-K-S` | `PHR-5` | `SPH-002T-P0.5S` | 1 GND; 2 SYS_3V3; 3 ENV_DHT_DATA; 4 I2C_SCL; 5 I2C_SDA |
| `J_DOOR` | JST `B2B-PH-K-S` | `PHR-2` | `SPH-002T-P0.5S` | 1 GND; 2 DOOR_SENSE |

JST documents the PH family as 2.0 mm pitch and 2 A with AWG24. Actual availability varies by position/header and must be checked before procurement.

Battery/service-current interface first candidate:

- board header `B2B-XH-A`;
- mating housing `XHP-2`;
- contact `SXH-001T-P0.6` or conductor-specific compatible XH contact selected after wire gauge freeze;
- candidate pin 1 = BATT+, pin 2 = GND.

JST documents the XH family as 2.5 mm pitch and 3 A with AWG22. Connector keying does **not** by itself solve reverse insertion of an unkeyed removable 18650 in its holder; accepted reverse-cell prevention remains an open IHAP-55/IHAP-51 design item `[UNVALIDATED]`.

No connector purchase is authorized.

## 7. Passive population status

Already Accepted/frozen:

- `R_DOOR_PULLUP = 10 kOhm` to SYS_3V3;
- `R_DOOR_SERIES = 1 kOhm` near GPIO3;
- optional 100 nF DOOR_SENSE filter footprint, DNP by default.

Not yet frozen:

- I2C SDA/SCL pull-up population;
- DHT data pull-up population;
- USB CC exact resistor MPN/tolerance;
- converter passives;
- regulator feedback networks;
- input/transient protection passives;
- module/local decoupling beyond manufacturer reference requirements.

Final I2C/DHT population requires measurement/identification of pull-ups already present on the actual OLED, BME280 and DHT11 modules. Until then board pull-up footprints remain design placeholders, not populated final values.

## 8. Mechanical contract — gate A status

Final dimensions are **not invented at this stage**. No board outline dimension is frozen until component footprints and preliminary schematic placement establish a defensible envelope.

Already frozen for placement planning:

- ESP32-C3 module antenna must sit at/over a PCB edge where practical;
- no copper/components/routing in the module antenna keepout required by Espressif;
- enclosure must also preserve RF clearance; Espressif recommends at least 15 mm clearance around the PCB antenna inside the end product;
- USB-C must remain externally service-accessible;
- BOOT/RESET and test points must remain service-accessible;
- `J_RADAR`, `J_OLED`, `J_ENV`, `J_DOOR`, battery connector and NTC/service routing must not be trapped by the enclosure;
- final envelope/holes/connector coordinates are the next IHAP-55 mechanical handoff to IHAP-51.

## 9. Design gates

Current state:

- [x] Phase 1 reconciliation performed.
- [x] IHAP-55 entered In corso.
- [x] Single branch created.
- [x] Accepted/Proposed boundary preserved.
- [x] Architecture block diagram revision A drafted.
- [x] ESP32-C3 module candidate selected for review.
- [x] First power-regulator candidates identified with manufacturer sources.
- [x] Controlled connector-family candidates identified.
- [ ] Project Owner review of final core/module partition.
- [ ] Electrical calculations complete.
- [ ] Schematic source created.
- [ ] ERC review complete.
- [ ] Preliminary mechanical envelope frozen and handed to IHAP-51.
- [ ] IHAP-51 feedback incorporated.
- [ ] Layout / DRC / DFM complete.
- [ ] Exact BOM frozen.
- [ ] Fabrication package generated.
- [ ] Fabrication authorization — **Project Owner gate**.
- [ ] Physical validation.
- [ ] Final reference implementation declaration — **Project Owner gate**.

## 10. Claim boundary

Everything not demonstrated by Accepted upstream evidence or later IHAP-55 physical evidence remains `[UNVALIDATED]`. This document makes no production-ready, safety-grade, security-grade, certification, alarm, antifurto, access-control or commercial-readiness claim.