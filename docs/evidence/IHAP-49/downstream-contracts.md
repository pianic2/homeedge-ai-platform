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

IHAP-55 is the primary implementation consumer of ADR-0007 and of `custom-pcb-power-contract.md` / `validation-plan.md`.

It must implement or explicitly supersede through reviewed evidence the following contract:

- custom core PCB rather than stacked power breakouts;
- normal USB-C 5 V input with correct Type-C sink termination;
- 5 V source profile >=1.5 A available/advertised;
- configured input-current limit whose worst-case maximum, including tolerance, is <=1.50 A;
- LG INR18650-MJ1 1S backup cell;
- preferred first PMIC direction: `MP2636GR-P`;
- explicit **post-MP2636 5 V regulation stage**, or reviewed equivalent topology, so USB pass-through and battery boost both feed the same regulated 5.0 V product SYS;
- 4.2 V battery-full target;
- ~1.0 A nominal charge-current target;
- NTC battery-temperature monitoring with mandatory normal/hot/cold/open/short functional verification;
- system-load priority while charging, demonstrated under combined node + charging load;
- regulated 5.0 V SYS;
- >=0.5 A continuous / >=1.0 A transient SYS design capability;
- mandatory bidirectional baseline<->1 A load-step capture with defined edge rate and rail/reset criteria;
- automatic USB-priority battery takeover and restoration across representative high/mid/low accepted battery voltages;
- prohibited backfeed into upstream USB;
- no-reset transfer as the reference target;
- integrated 3.3 V rail sized from the ESP32-C3 + peripheral budget;
- test points and staged bring-up;
- **cell-side over-current interruption** protecting holder/BAT-net faults upstream of PMIC SYS/boost limiting;
- electrical reverse-battery blocking or a mechanically keyed interface that physically prevents reverse insertion; procedure alone is insufficient;
- bounded functional reverse-polarity verification with a current-limited simulator when electrical blocking is used;
- numeric low-voltage cutoff/recovery/hysteresis contract from `validation-plan.md`;
- manufacturer-derived thermal acceptance table and numeric PASS/FAIL limits before powered thermal validation;
- quantitative final-node measurements transferred from **ADR-0001, ADR-0002, ADR-0003, ADR-0004 and ADR-0005**, including reed/pull-network current;
- external modular interfaces for placement-sensitive/serviceable sensors.

Mandatory physical evidence is defined in `docs/evidence/IHAP-49/validation-plan.md`, including V4/V6 thermal checks, V7 bidirectional load step, V8/V9 high-mid-low transfer/restoration, V10 numeric low-voltage behavior, V13 cell-side over-current, V14 combined source-current-limit/system-priority, and V15 electrical reverse-blocking when applicable.

Canonical treatment dossiers are R-012 and R-013. Their treatment lifecycle remains **Proposed** until explicit Project Owner treatment approval evidence exists; implementation/effectiveness remain `[UNVALIDATED]` regardless of ADR-0007 acceptance.

## IHAP-51 — Edge Enclosure and Mounting

IHAP-51 must consume the frozen custom-board mechanical envelope and preserve:

- serviceable 18650 holder/cell access;
- battery retention;
- physical reverse-insertion prevention when mechanical keying is selected as the primary control;
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

**normal 5 V USB-C + LG MJ1 1S backup + integrated custom-board power path, first implementation direction MP2636GR-P plus regulated 5 V post-stage or reviewed equivalent.**

IHAP-43 must not imply that the fabricated PCB, verified treatment effectiveness or measured runtime already exists.

## Runtime / event integrity

IHAP-49 does not redefine runtime/event contracts. However, no-reset source transfer is the hardware target. If IHAP-55 evidence shows a controlled reboot is unavoidable, that result must be made explicit and downstream runtime/event validation must account for reboot/event-integrity behavior rather than silently accepting duplicates or gaps.
