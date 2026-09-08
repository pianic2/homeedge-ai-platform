# IHAP-49 — Downstream Contracts

## Approval boundary

The 2026-09-07 Project Owner approval covers ADR-0007 / PR #34. IHAP-56 introduces additional R-012/R-013 treatment and validation detail that remains **Proposed** until explicit Project Owner approval. Downstream tasks must distinguish those two layers.

## IHAP-50 — Interconnect and Prototype Assembly

IHAP-50 must produce the canonical connection/interface matrix consumed by the custom PCB and preserve the accepted baseline:

- one regulated 5 V system domain serving LD2410C and the 3.3 V regulator;
- accepted ESP32-C3 signal/peripheral requirements;
- DHT11 standard profile / BME280 precision profile distinction;
- passive reed-contact semantics and final pull-network purpose/current;
- polarized/keyed connector requirements where polarity matters;
- field wiring / strain-relief requirements for external modules.

IHAP-50 should no longer treat a permanent breadboard/Dupont stack as the desired final reference implementation. Commodity prototype wiring may remain development evidence only.

## IHAP-55 — Integrated Modular Edge PCB

IHAP-55 is the primary implementation consumer of ADR-0007, `custom-pcb-power-contract.md` and `validation-plan.md`.

### Accepted PR #34 baseline

IHAP-55 must implement or explicitly supersede through reviewed evidence:

- custom core PCB rather than stacked power breakouts;
- normal USB-C 5 V input with correct Type-C sink termination;
- 5 V source profile >=1.5 A available/advertised;
- LG INR18650-MJ1 1S backup cell;
- preferred first PMIC direction: `MP2636GR-P`;
- explicit **post-MP2636 5 V regulation stage**, or reviewed equivalent topology, so USB pass-through and battery boost both feed the same regulated 5.0 V product SYS;
- 4.2 V battery-full target;
- ~1.0 A nominal charge-current target;
- NTC battery-temperature monitoring;
- system-load priority while charging;
- regulated 5.0 V SYS;
- >=0.5 A continuous / >=1.0 A transient/headroom design capability;
- automatic USB-priority battery takeover;
- prohibited backfeed into upstream USB;
- no-reset transfer as the reference target, still `[UNVALIDATED]`;
- integrated 3.3 V rail sized from the ESP32-C3 + accepted peripheral budget;
- test points and staged bring-up;
- electrical reverse-battery blocking or a mechanically keyed interface that physically prevents reverse insertion; procedure alone is insufficient;
- quantitative final-node measurements transferred by the accepted baseline from **ADR-0001, ADR-0002, ADR-0004 and ADR-0005**;
- external modular interfaces for placement-sensitive/serviceable sensors.

### Proposed IHAP-56 treatment / validation additions — not yet accepted

The following must remain **Proposed** and must not be treated as accepted IHAP-55 gates until explicit Project Owner approval exists:

- configured input-current limit whose worst-case maximum including tolerance is <=1.50 A plus V14 combined source-limit/system-priority verification;
- mandatory NTC normal/hot/cold/open/short functional verification;
- **cell-side over-current interruption** protecting holder/BAT-net faults upstream of PMIC SYS/boost limiting;
- V13 installed-path over-current verification through the actual fabricated battery-service path;
- bounded V15 electrical reverse-polarity verification when electrical blocking is used;
- manufacturer-derived thermal acceptance table and numeric PASS/FAIL limits;
- V7 bidirectional baseline<->1 A waveform capture with <=100 µs 10–90% current edges;
- V8/V9 transfer/restoration at high/mid/low battery conditions, including zero restoration-attributable reset/brownout for proposed no-reset effectiveness verification;
- numeric V10 cutoff/recovery/hysteresis policy;
- extension of quantitative ownership transfer to **ADR-0003 / reed current**.

Canonical treatment dossiers are R-012 and R-013. RT-R012-01 and RT-R013-01 remain **Proposed**; implementation/effectiveness remain `[UNVALIDATED]`.

IHAP-55 execution remains blocked by IHAP-56 until the remediation/approval boundary is resolved.

## IHAP-51 — Edge Enclosure and Mounting

IHAP-51 must consume the frozen custom-board mechanical envelope and preserve:

- serviceable 18650 holder/cell access;
- battery retention;
- accepted reverse-insertion prevention requirement when mechanical keying is selected;
- NTC placement / thermal spacing constraints;
- USB-C access;
- LD2410C antenna/field-of-view constraints;
- environmental-sensor airflow;
- OLED viewing/aperture constraints;
- MC-38 field wiring/strain relief;
- no unsupported IP, fire, tamper, electrical-safety or certification claim.

## IHAP-17 — Cost Governance / BOM

IHAP-17 may record the accepted architecture/cell/PMIC direction from PR #34. The definitive assembled-board replication total remains downstream evidence from IHAP-55 and must distinguish board BOM, fabrication/assembly allocation, battery/holder, external modules, shared inventory/tooling and dated supplier prices.

## IHAP-43 — Hardware Decision Baseline

The accepted power decision is:

**normal 5 V USB-C + LG MJ1 1S backup + integrated custom-board power path, first implementation direction MP2636GR-P plus regulated 5 V post-stage or reviewed equivalent.**

IHAP-43 must not imply that the fabricated PCB, proposed treatment approval/effectiveness or measured runtime already exists.

## Runtime / event integrity

IHAP-49 does not redefine runtime/event contracts. No-reset transfer is the accepted hardware target and remains `[UNVALIDATED]`. If downstream evidence shows a controlled reboot is unavoidable, that result must be explicit and runtime/event validation must account for reboot/event-integrity behavior rather than silently accepting duplicates or gaps. The stronger high/mid/low and zero-reset-restoration criteria proposed by IHAP-56 remain pending approval.
