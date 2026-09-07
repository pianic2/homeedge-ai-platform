# IHAP-49 — Power Subsystem Validation Plan / IHAP-55 Handoff

**Status:** accepted architecture validation contract; physical implementation validation delegated to IHAP-55

## Objective

Define the tests required to prove that the **custom PCB implementation** satisfies ADR-0007:

- regulated 5 V USB-C as the normal source;
- LG INR18650-MJ1 1S battery as backup only;
- integrated charger + system power path + battery boost;
- explicit post-regulation or equivalent topology maintaining the same regulated 5 V product bus in USB and battery modes;
- automatic source transfer without prohibited backfeed;
- controlled battery charging and low-voltage behavior;
- sufficient 5 V / 3.3 V headroom for the reference node;
- quantitative current/rail measurements transferred from earlier accepted ADRs.

IHAP-49 owns this validation contract. **IHAP-55 executes the fabricated-board tests.**

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
- custom-PCB power contract accepted;
- MP2636 retained as preferred charger/power-path/battery-boost PMIC candidate;
- MP2636 input-pass-through limitation identified and remediated at architecture level by requiring downstream 5 V regulation or an explicitly reviewed equivalent topology.

The unresolved exact RPROG/protection-controller behavior of the owned 4056E module is **not a closure blocker** because that module is not selected for the final reference PCB.

## Reference implementation preconditions for IHAP-55

Before physical bring-up, IHAP-55 must freeze:

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

## Required instrumentation

Minimum instrumentation for ordinary bring-up:

- digital multimeter for voltage, continuity, resistance and steady-state current;
- serial/host logging sufficient to detect ESP32-C3 reboot/brownout/re-enumeration;
- timer/timestamps for endurance testing;
- temperature measurement suitable for comparative bench observation.

Additional instrumentation is **mandatory for the frozen >=1.0 A transient/headroom requirement**:

- an electronic load, MOSFET load fixture or resistor-bank fixture capable of a repeatable load step to **1.0 A at the 5 V product SYS bus**;
- an oscilloscope or equivalent acquisition instrument with sufficient bandwidth to capture sub-millisecond rail excursions; **>=20 MHz analog bandwidth** is the reference minimum unless the final regulator validation method demonstrates an equivalent or stronger capture capability;
- a low-inductance probing arrangement at the product 5 V SYS test point.

A generic USB display power meter is not an acceptable substitute for the mandatory transient capture.

## Physical test sequence — IHAP-55

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
- verify no unintended voltage appears on disconnected battery terminals beyond the expected charger behavior.

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

This test is **not optional**.

- establish a repeatable baseline load representative of the node or approximately 0.1–0.15 A;
- step the product 5 V SYS load to **1.0 A** using the controlled load fixture;
- capture the 5 V SYS waveform at the PCB test point with the required oscilloscope/acquisition setup;
- repeat in normal USB mode and battery mode at representative high, mid and low accepted battery voltages where practical;
- log ESP32 reset/brownout state during the test.

PASS criteria:

- no uncontrolled rail collapse or protection oscillation;
- no ESP32 reset/brownout attributable to the load step;
- steady-state after the step returns to **4.75–5.25 V**;
- captured transient does not fall below **4.5 V** or rise above **5.5 V**;
- the rail returns to the 4.75–5.25 V steady-state band within **2 ms** after the load transition;
- if any selected downstream component requires a tighter transient limit, the tighter component limit supersedes these generic acceptance numbers.

The waveform, load-step method, battery voltage and probe point are mandatory evidence.

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
- capture product 5 V SYS during restoration.

### V10 — Low-voltage / recovery behavior

Within safe non-destructive limits:

- verify battery discharge does not intentionally continue below the accepted cell boundary;
- verify any graceful low-battery warning/shutdown behavior;
- verify recovery after normal USB source returns;
- do not perform destructive short/reverse tests merely to claim protection.

### V11 — Mandatory quantitative load characterization transferred from prior ADRs

The following measurements remain mandatory even though ownership moved from IHAP-49 to IHAP-55:

- ESP32-C3 final implementation: 3.3 V rail current in representative idle/Wi-Fi-active conditions and observable peak/transient behavior with appropriate instrumentation;
- LD2410C: quantitative 5 V current contribution on the final wiring/interface;
- OLED: active-display current, blank/sleep current where supported, and a documented sleep/power policy based on the measured values;
- DHT11 standard profile and BME280 precision profile: quantitative current contribution under the selected sampling policy;
- complete node: normal-source input current, 5 V product SYS current, 3.3 V rail current and brownout/reset evidence under representative operation.

These measurements satisfy the still-valid quantitative power obligations originally assigned to IHAP-49 by ADR-0001, ADR-0002, ADR-0004 and ADR-0005. ADR-0007 transfers execution ownership to IHAP-55; it does not waive the evidence.

### V12 — Backup endurance

- fully charge the accepted cell;
- run the complete reference node on battery under representative workload;
- log start/end, periodic cell/SYS readings, resets and functional state;
- stop at the accepted low-voltage endpoint;
- record measured runtime.

Only V12 may support a measured backup-autonomy statement for the tested board/cell/configuration.

## Acceptance boundary

Physical PASS results support only the tested custom-board revision and conditions. They do not establish certification, fire safety, commercial readiness or universal cell/board equivalence.

**IHAP-49 may close after the accepted architecture contract is merged because ADR-0007 explicitly transfers these still-mandatory implementation measurements to IHAP-55.** Any downstream evidence that contradicts this contract must reopen/supersede ADR-0007 rather than silently weakening tests.
