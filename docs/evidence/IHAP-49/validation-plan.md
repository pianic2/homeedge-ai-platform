# IHAP-49 — Power Subsystem Validation Plan / IHAP-55 Handoff

**Status:** Accepted PR #34 validation baseline + **Proposed IHAP-56 amendment overlay** pending explicit Project Owner approval

## Approval boundary

The Project Owner approved ADR-0007 / PR #34 on 2026-09-07. That accepted baseline includes the regulated 5 V USB-C + 1S backup architecture, post-MP2636 regulation/equivalent, reverse-insertion prevention, NTC monitoring, 0.5 A continuous / 1.0 A headroom targets, source transfer/backfeed checks, and the quantitative power handoff originally covering ADR-0001/0002/0004/0005.

IHAP-56 later proposed tighter treatment/verification detail for R-012/R-013. The following additions are **Proposed, not Accepted**, until the Project Owner explicitly approves the treatment/amendment scope:

- cell-side over-current interruption and V13 installed-path verification;
- mandatory NTC normal/hot/cold/open/short behavior;
- manufacturer-derived numeric thermal acceptance table and limits;
- worst-case ILIM <=1.50 A plus V14 combined node+charging priority test;
- bidirectional V7 load step with <=100 µs current edges;
- V8/V9 high/mid/low battery coverage and explicit no-reset restoration criterion;
- numeric V10 cutoff/recovery/hysteresis policy;
- V15 electrical reverse-blocking functional test;
- extension of quantitative ownership transfer to ADR-0003/reed current.

These proposed additions may be reviewed and improved before approval, but they must not be represented as already accepted implementation gates or as treatment approval evidence. IHAP-55 remains blocked by IHAP-56 until the applicable decision boundary is resolved.

## Objective — accepted baseline

Define the tests required to prove that the **custom PCB implementation** satisfies the accepted ADR-0007 baseline:

- regulated 5 V USB-C as the normal source;
- LG INR18650-MJ1 1S battery as backup only;
- integrated charger + system power path + battery boost;
- explicit post-regulation or equivalent topology maintaining the same regulated 5 V product bus in USB and battery modes;
- automatic source transfer without prohibited backfeed;
- controlled battery charging and low-voltage behavior;
- sufficient 5 V / 3.3 V headroom for the reference node;
- quantitative current/rail measurements transferred by the accepted baseline from ADR-0001/0002/0004/0005.

IHAP-49 owns the accepted baseline contract. **IHAP-55 executes fabricated-board tests after downstream gates are satisfied.** R-012/R-013 and IHAP-57 track the later proposed treatment/effectiveness work.

## Evidence already completed in IHAP-49

- battery Go/No-Go resolved: battery retained as backup only;
- planning power/autonomy budget produced;
- exact cell model selected: LG INR18650-MJ1;
- owned holder dimensions/limitations recorded;
- owned charger module visually identified as `4056E` family with `8205A` protection MOSFET stage;
- charger C0/C1 characterization recorded;
- legacy USB-A-to-USB-C input sanity passed at 4.95 V;
- tested USB-C-to-USB-C fast-charge input was not supported by the owned charger breakout;
- generic breakout stack rejected as final reference implementation;
- custom-PCB power contract accepted at the PR #34 baseline;
- MP2636 retained as preferred charger/power-path/battery-boost PMIC candidate;
- MP2636 input-pass-through limitation identified and addressed in the accepted architecture by requiring downstream 5 V regulation or an explicitly reviewed equivalent topology.

The unresolved exact RPROG/protection-controller behavior of the owned 4056E module is **not a closure blocker** because that module is not selected for the final reference PCB.

## Accepted reference implementation preconditions for IHAP-55

Before physical bring-up, the accepted baseline requires IHAP-55 to freeze:

- MP2636GR-P schematic implementation or an explicitly reviewed superseding PMIC/topology;
- downstream 5 V post-regulation stage capable of maintaining the product bus across the complete USB-pass-through and battery-boost intermediate range;
- intermediate SYS/boost setpoint compatible with that post-regulator;
- 4.2 V charge-voltage selection;
- ~1.0 A nominal charge-current setting;
- regulated product 5 V SYS acceptance band;
- >=0.5 A continuous / >=1.0 A transient SYS design envelope;
- USB-C CC/input-protection implementation;
- 3.3 V regulator;
- NTC network;
- **electrical reverse-battery blocking or a mechanically keyed interface that physically prevents reverse insertion**;
- holder connector/polarity;
- input-current-limit profile for the reference 5 V >=1.5 A source;
- automatic MODE/source-transfer logic;
- test points for VIN, BATT, intermediate SYS, product 5 V SYS and 3.3 V.

## Accepted baseline instrumentation

Minimum instrumentation:

- digital multimeter for voltage, continuity, resistance and steady-state current;
- serial/host logging sufficient to detect ESP32-C3 reboot/brownout/re-enumeration;
- timer/timestamps for endurance testing;
- temperature measurement suitable for comparative bench observation.

Additional instrumentation is mandatory for the accepted >=1.0 A headroom requirement:

- an electronic load, MOSFET load fixture or resistor-bank fixture capable of a repeatable load step to **1.0 A at the 5 V product SYS bus**;
- an oscilloscope or equivalent acquisition instrument with sufficient bandwidth to capture sub-millisecond rail excursions; **>=20 MHz analog bandwidth** is the reference minimum unless the final regulator validation method demonstrates an equivalent or stronger capture capability;
- a low-inductance probing arrangement at the product 5 V SYS test point.

A generic USB display power meter is not an acceptable substitute for the mandatory transient capture.

## Accepted physical test sequence — IHAP-55

### V1 — Unpowered PCB inspection

- verify polarity, continuity and absence of unintended shorts;
- inspect battery connector/holder polarity;
- verify reverse-battery blocking or mechanical keying implementation;
- verify USB-C CC and input-protection population;
- verify MP2636 / post-regulator / 3.3 V regulator / inductor / sense-network population against BOM;
- verify NTC path and test points.

### V2 — USB-C normal-source bring-up, no battery

- apply the accepted 5 V USB-C source;
- confirm VIN and the intermediate pass-through node;
- confirm **regulated 5 V product SYS**, not merely the MP2636 pass-through node;
- steady-state 5 V SYS PASS band: **4.75–5.25 V**, unless the selected downstream load requires tighter limits;
- confirm 3.3 V rail;
- verify the node can boot without a battery;
- record steady-state current and abnormal heating;
- verify no unintended voltage appears on disconnected battery terminals beyond expected charger behavior.

### V3 — Received cell / holder inspection

- confirm received LG MJ1 markings and condition;
- confirm non-destructive fit/contact pressure in the owned holder;
- verify polarity labeling;
- confirm the final reverse-insertion control cannot be bypassed during ordinary installation/service;
- record open-circuit cell voltage before first connection.

### V4 — Controlled charging

- verify ~1 A target charge current within the tolerance frozen in the schematic/PMIC configuration;
- verify cell terminal voltage approaches but does not exceed the accepted 4.2 V charging envelope;
- verify charge termination / auto-recharge behavior as observable;
- verify system-load priority while the node operates;
- observe battery/PMIC/inductor/post-regulator temperature behavior;
- verify NTC fault behavior non-destructively where practical.

### V5 — Battery mode / product 5 V regulation

Across representative battery voltages:

- verify intermediate boost behavior;
- verify product 5 V SYS remains **4.75–5.25 V steady-state**;
- verify 3.3 V rail stability;
- exercise ESP32 Wi-Fi, LD2410C, OLED and selected environmental/reed interface;
- record brownout/reset evidence.

### V6 — Mandatory 0.5 A continuous load test

With USB input and separately with battery backup at representative battery voltages:

- apply **0.5 A continuous** at the regulated 5 V product SYS bus in addition to, or using an equivalent controlled replacement for, the node load;
- maintain the test long enough to reach a stable comparative thermal condition defined by IHAP-55;
- PASS only if product SYS remains **4.75–5.25 V**, no protection oscillation occurs, and no board reset/brownout is observed;
- record regulator/PMIC/inductor temperatures and test conditions.

### V7 — Mandatory 1.0 A load-step / headroom test

This accepted baseline test is not optional.

- establish a repeatable baseline load representative of the node or approximately 0.1–0.15 A;
- step the product 5 V SYS load to **1.0 A** using the controlled load fixture;
- capture the 5 V SYS waveform at the PCB test point with the required oscilloscope/acquisition setup;
- repeat in normal USB mode and battery mode at representative high, mid and low accepted battery voltages where practical;
- log ESP32 reset/brownout state during the test.

Accepted baseline PASS criteria:

- no uncontrolled rail collapse or protection oscillation;
- no ESP32 reset/brownout attributable to the load step;
- steady-state after the step returns to **4.75–5.25 V**;
- captured transient does not fall below **4.5 V** or rise above **5.5 V**;
- the rail returns to the 4.75–5.25 V steady-state band within **2 ms** after the load transition;
- if any selected downstream component requires a tighter transient limit, the tighter component limit supersedes these generic acceptance numbers.

### V8 — USB loss / backup transfer

- start with normal USB operation and valid charged backup;
- remove normal USB input;
- verify automatic transition to battery-backed regulated 5 V;
- verify no prohibited backfeed toward USB;
- capture product 5 V SYS during the transfer with suitable bandwidth instrumentation;
- record whether any ESP32 reset/brownout occurs;
- **PASS target: no-reset transfer**.

### V9 — Normal-source restoration

- restore valid USB input;
- verify deterministic return to normal source;
- verify charging resumes as designed;
- verify no source oscillation or reset loop;
- verify no backfeed;
- capture product 5 V SYS during restoration;
- record reset/brownout state.

**Accepted-baseline boundary:** V9 did not originally define a numeric no-reset restoration PASS criterion. Therefore an isolated restoration reset must not be used to mark R-013 treatment effectiveness `Verified` under the accepted baseline. The Proposed IHAP-56 amendment below adds an explicit zero-reset restoration criterion at each required battery/load condition.

### V10 — Low-voltage / recovery behavior

Within safe non-destructive limits:

- verify battery discharge does not intentionally continue below the accepted cell boundary;
- verify any graceful low-battery warning/shutdown behavior;
- verify recovery after normal USB source returns;
- do not perform destructive short/reverse tests merely to claim protection.

### V11 — Mandatory quantitative load characterization transferred from prior ADRs

Accepted ownership transfer covers:

- ESP32-C3 final implementation: 3.3 V rail current in representative idle/Wi-Fi-active conditions and observable peak/transient behavior with appropriate instrumentation;
- LD2410C: quantitative 5 V current contribution on the final wiring/interface;
- OLED: active-display current, blank/sleep current where supported, and a documented sleep/power policy based on the measured values;
- DHT11 standard profile and BME280 precision profile: quantitative current contribution under the selected sampling policy;
- complete node: normal-source input current, 5 V product SYS current, 3.3 V rail current and brownout/reset evidence under representative operation.

These accepted transferred obligations come from **ADR-0001, ADR-0002, ADR-0004 and ADR-0005**. The proposed ADR-0003/reed-current ownership extension is listed below and is not yet accepted as an ADR-0007 amendment.

### V12 — Backup endurance

- fully charge the accepted cell;
- run the complete reference node on battery under representative workload;
- log start/end, periodic cell/SYS readings, resets and functional state;
- stop at the accepted low-voltage endpoint;
- record measured runtime.

Only V12 may support a measured backup-autonomy statement for the tested board/cell/configuration.

---

## Proposed IHAP-56 validation amendments — pending Project Owner approval

Everything in this section is **Proposed**. It may not advance RT-R012-01 or RT-R013-01 beyond `Proposed`, and it may not be represented as an Accepted ADR-0007 implementation gate until explicit Project Owner approval exists.

### Proposed thermal / voltage boundaries

Manufacturer-source limits proposed for explicit PASS/FAIL use:

| Item | Proposed boundary | Intended validation use |
|---|---:|---|
| LG INR18650-MJ1 charge operating temperature | **0 to 45 °C** | V4 charging |
| LG INR18650-MJ1 discharge operating temperature | **-20 to 60 °C** | battery-operation tests |
| LG INR18650-MJ1 maximum charge voltage | **4.20 ±0.05 V** | V4 |
| LG INR18650-MJ1 manufacturer discharge end voltage | **2.50 V** | hard lower boundary |
| MP2636 recommended operating junction temperature | **-40 to +125 °C** | powered validation |
| MP2636 thermal shutdown | approximately **150 °C**, recovery approximately **120 °C** | protective behavior only; entering shutdown would fail a treatment validation run |

The proposed treatment also requires IHAP-55 to register manufacturer limits for the selected post-regulator, 3.3 V regulator, inductor and protection element before thermal treatment evidence can pass.

### Proposed low-voltage product policy

- cutoff at **2.70 V ±0.05 V** under the defined validation load/measurement condition;
- no deliberate continued operation below **2.50 V**;
- restart only at **BATT >=3.00 V ±0.05 V** or valid USB input;
- nominal hysteresis **0.30 V** with no cutoff/restart oscillation.

### Proposed V4 strengthening — NTC / thermal / combined charging observations

- exercise NTC valid, cold, hot, open and short equivalents using a resistor/switching fixture;
- hot/cold/open/short must inhibit charging or be intercepted by an explicitly reviewed fail-bounded equivalent;
- recovery to valid NTC must be deterministic without charge oscillation;
- apply the proposed manufacturer-derived thermal limits;
- record source current, charge current, SYS rail and thermal data while the representative node operates.

### Proposed V7 strengthening — bidirectional dynamic test

- exercise **baseline -> 1.0 A** and **1.0 A -> baseline**;
- measure 10–90% current transition time on both edges and require **<=100 µs**, unless final measured load behavior requires a faster reference;
- capture both droop and load-release overshoot;
- require no reset/brownout on either edge and the accepted rail/recovery criteria on both transitions.

### Proposed V8 strengthening — source loss across battery range

Execute at:

- high: **4.10 V ±0.10 V**;
- mid: **3.60 V ±0.10 V**;
- low: **2.80 V ±0.05 V**.

At each condition use the representative node load and, where practical, a higher controlled load within the validated continuous envelope. Proposed PASS requires no prohibited backfeed, no source oscillation, rail/thermal compliance and no transfer-attributable reset/brownout if the no-reset treatment target is being verified.

### Proposed V9 strengthening — source restoration across battery range

Repeat restoration at the same high/mid/low battery conditions and relevant load conditions used by Proposed V8.

Proposed PASS criteria:

- deterministic return to normal source;
- no prohibited backfeed or source oscillation;
- charging resumes when permitted by cell state;
- product SYS remains within the applicable rail criteria;
- **zero ESP32 reset or brownout attributable to normal-source restoration at every required battery/load condition**;
- any restoration-attributable reset/brownout is an explicit **FAIL** for the proposed no-reset restoration treatment criterion, even if no reset loop occurs.

### Proposed V10 strengthening — numeric cutoff / recovery

Use a current-limited battery simulator or controlled discharge fixture. Proposed PASS requires the 2.70 V cutoff, >=3.00 V restart or valid USB, no deliberate sustained operation below 2.50 V, and no oscillatory restart.

### Proposed V11 extension — ADR-0003 / reed current

Add quantitative MC-38/reed closed-loop current contribution for the final pull/network selected by IHAP-50. This is a **Proposed ownership-transfer correction** from ADR-0003 to IHAP-55 and is not treated as accepted until explicitly approved or assigned by another accepted downstream decision.

### V13 — Proposed mandatory installed cell-side over-current verification

This proposed test verifies the actual fabricated protection path without intentionally shorting the real MJ1 cell.

Preconditions:

- schematic/BOM identify the cell-side protection element, location, current/time threshold or trip curve and sizing rationale;
- the real Li-ion cell is disconnected;
- a current-limited bench source or protected battery simulator represents the BAT source.

Verification method:

- inject the bounded test current **through the normal battery service input / installed holder connector and the actual fabricated PCB BAT path**, including the production connector, copper/traces, footprint, solder joints and the **installed protection element**;
- create the controlled over-current on the protected downstream BAT path so current necessarily traverses the installed protection chain;
- verify interruption/limiting within the frozen threshold/time and verify recovery/replacement behavior appropriate to the chosen protection technology;
- confirm PMIC SYS/boost current limiting is not the only element covering the upstream BAT fault path.

A loose sacrificial fuse/switch or off-board sample that bypasses the installed connector/traces/footprint/solder joints **cannot satisfy EV-03**. If a separate destructive test vehicle is necessary, it must be a production-identical assembled PCB revision/path with the same connector, copper geometry, footprint, component and assembly process, plus traceable assembly/continuity evidence tying that vehicle to the reference revision.

Proposed PASS criteria:

- installed/production-identical protected BAT path interrupts or limits as designed;
- observed behavior matches the frozen component specification and design rationale;
- no intentional hard short is applied across the actual Li-ion cell;
- post-test inspection shows no damage that invalidates the evidence path.

### V14 — Proposed combined source-current-limit / system-load-priority verification

- configure worst-case board ILIM, including tolerance, to **<=1.50 A** for the reference source;
- operate the representative complete node while the charger requests near-maximum charge current;
- increase controlled SYS load toward the source limit;
- measure total USB input current, charge current and product SYS voltage together.

Proposed PASS requires measured USB input <=1.50 A and <= frozen worst-case ILIM including uncertainty, charging current yielding before SYS leaves 4.75–5.25 V, and no source oscillation/reset/brownout/repeated charger loop.

### V15 — Proposed electrical reverse-polarity verification

If electrical reverse blocking is relied upon:

- disconnect the real MJ1;
- use a 4.20 V battery simulator with **10 mA maximum current limit**;
- reverse-connect through the normal service interface;
- require steady reversed current **<=1 mA** after settling unless the selected component specifies a lower limit;
- require product 5 V SYS and 3.3 V rails to remain **<=0.3 V** from the reversed source;
- require no abnormal heating/damage and normal recovery after correct polarity is restored.

If mechanical keying alone is selected, V15 electrical reverse-drive is N/A and V1/V3 must prove ordinary reverse insertion is physically impossible.

## Proposed risk-to-test map

| Canonical risk / exposure | Proposed primary evidence |
|---|---|
| R-012 battery charge / NTC fault behavior | strengthened V4 |
| R-012 over-discharge / recovery | strengthened V10 |
| R-012 reverse insertion | V1 + V3 + V15 when electrical blocking is used |
| R-012 cell-side over-current | V13 installed-path test |
| R-012/R-013 thermal overstress | proposed thermal limits + powered tests |
| R-013 1 A transient / brownout | strengthened V7 both edges |
| R-013 USB loss / backfeed | strengthened V8 high/mid/low |
| R-013 source restoration / reset / backfeed | strengthened V9 high/mid/low; any restoration reset fails no-reset verification |
| R-013 source-current limit / system priority | V14 |
| R-013 final-node quantitative loads | accepted V11 + proposed ADR-0003 extension if approved |
| R-013 measured backup runtime | V12 |

## Acceptance boundary

Physical PASS results support only the tested custom-board revision and conditions. They do not establish certification, fire safety, commercial readiness or universal cell/board equivalence.

**IHAP-49 remains closed on the accepted PR #34 architecture decision.** The IHAP-56 additions above remain Proposed until explicit Project Owner approval; they must not be used to claim treatment approval/effectiveness or to rewrite the 2026-09-07 acceptance record. Any downstream evidence that contradicts the accepted architecture must reopen/supersede ADR-0007 rather than silently weakening it.
