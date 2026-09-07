# IHAP-49 — Downstream Contracts

## IHAP-50 — Interconnect and Prototype Assembly

IHAP-50 must produce the canonical connection/interface matrix consumed by the custom PCB and preserve:

- one regulated 5 V system domain serving LD2410C and the 3.3 V regulator;
- accepted ESP32-C3 signal/peripheral requirements;
- DHT11 standard profile / BME280 precision profile distinction;
- passive reed-contact semantics and final pull-network purpose/current;
- polarized/keyed connector requirements where polarity matters;
- field wiring / strain-relief requirements for external modules.

IHAP-50 should no longer treat a permanent breadboard/Dupont stack as the desired final reference implementation. Commodity prototype wiring may remain development evidence only.

## IHAP-55 — Integrated Modular Edge PCB

IHAP-55 is the primary implementation consumer of ADR-0007.

It must implement or explicitly supersede the following contract:

- custom core PCB rather than stacked power breakouts;
- normal USB-C 5 V input with correct Type-C sink termination;
- 5 V source profile >=1.5 A available/advertised;
- LG INR18650-MJ1 1S backup cell;
- preferred first PMIC direction: `MP2636GR-P`;
- 4.2 V battery-full target;
- ~1.0 A nominal charge-current target;
- NTC battery-temperature monitoring;
- system-load priority while charging;
- regulated 5.0 V SYS;
- >=0.5 A continuous / >=1.0 A transient SYS design capability;
- automatic USB-priority battery takeover;
- prohibited backfeed into upstream USB;
- no-reset transfer as the reference target;
- integrated 3.3 V rail sized from the ESP32-C3 + peripheral budget;
- test points and staged bring-up;
- reverse-cell mitigation;
- external modular interfaces for placement-sensitive/serviceable sensors.

Physical charge/thermal/rail/switchover/endurance evidence belongs to IHAP-55, not IHAP-49 closure.

## IHAP-51 — Edge Enclosure and Mounting

IHAP-51 must consume the frozen custom-board mechanical envelope and preserve:

- serviceable 18650 holder/cell access;
- battery retention;
- reverse-insertion mitigation where mechanical prevention is used;
- NTC placement / thermal spacing constraints;
- USB-C access;
- LD2410C antenna/field-of-view constraints;
- environmental-sensor airflow;
- OLED viewing/aperture constraints;
- MC-38 field wiring/strain relief;
- no unsupported IP, fire, tamper, electrical-safety or certification claim.

## IHAP-17 — Cost Governance / BOM

After Project Owner acceptance of IHAP-49, IHAP-17 may record the accepted architecture/cell/PMIC direction.

The definitive assembled-board replication total remains downstream evidence from IHAP-55 and must distinguish:

- board BOM;
- PCB/fabrication/assembly allocation;
- battery/holder;
- external modules;
- shared inventory/tooling;
- current dated supplier prices.

## IHAP-43 — Hardware Decision Baseline

After ADR-0007 acceptance, IHAP-43 records the power decision as:

**normal 5 V USB-C + LG MJ1 1S backup + integrated custom-board power path, first implementation direction MP2636GR-P.**

IHAP-43 must not imply that the fabricated PCB or measured runtime already exists.

## Runtime / event integrity

IHAP-49 does not redefine runtime/event contracts. However, no-reset source transfer is the hardware target. If IHAP-55 evidence shows a controlled reboot is unavoidable, that result must be made explicit and downstream runtime/event validation must account for reboot/event-integrity behavior rather than silently accepting duplicates or gaps.
