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
- cell-side over-current interruption and reverse-insertion prevention for the unprotected MJ1 path;
- functional NTC hot/cold/open/short behavior;
- bounded thermal operation against manufacturer/component limits;
- input-current limiting and system-load priority within the 5 V / 1.5 A reference-source envelope;
- sufficient 5 V / 3.3 V headroom for the reference node;
- quantitative current/rail measurements transferred from earlier accepted ADRs.

IHAP-49 owns this validation contract. **IHAP-55 executes the fabricated-board tests.** Canonical residual-risk/effectiveness tracking is in R-012/R-013 and Jira IHAP-57.

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
- NTC network and its expected valid/hot/cold/open/short behavior;
- **cell-side over-current interruption element** located so holder-lead/BAT-net faults upstream of PMIC SYS protection are covered;
- cell-side protection threshold/time rationale against worst-case normal charge/discharge/transient current and conductor/trace ampacity;
- **electrical reverse-battery blocking or a mechanically keyed interface that physically prevents reverse insertion**;
- holder connector/polarity;
- input-current-limit profile whose worst-case configured maximum, including tolerance, is **<=1.50 A** for the reference source;
- automatic MODE/source-transfer logic;
- test points for VIN, BATT, intermediate SYS, product 5 V SYS and 3.3 V;
- numeric thermal acceptance table for every dissipative power component used in V4/V6/V7/V8/V9, derived from its manufacturer datasheet and the final PCB thermal model.

### Frozen cell and PMIC thermal / voltage boundaries

The following numeric limits are already fixed from the registered manufacturer sources and must not be weakened silently:

| Item | Frozen boundary | Validation use |
|---|---:|---|
| LG INR18650-MJ1 charge operating temperature | **0 to 45 °C** | V4 charging must remain inside this range |
| LG INR18650-MJ1 discharge operating temperature | **-20 to 60 °C** | V5/V6/V7/V8/V9/V10/V12 battery operation must remain inside this range |
| LG INR18650-MJ1 maximum charge voltage | **4.20 ±0.05 V** | V4 |
| LG INR18650-MJ1 manufacturer discharge end voltage | **2.50 V** | hard lower boundary; V10 uses a higher product cutoff |
| MP2636 recommended operating junction temperature | **-40 to +125 °C** | calculated/estimated junction temperature must remain <=125 °C during PASS runs |
| MP2636 thermal shutdown | approximately **150 °C**, recovery approximately **120 °C** | protective behavior only; entering thermal shutdown is a FAIL, not an acceptable operating point |

For the selected post-regulator, 3.3 V regulator, inductor, fuse/protection element and any other thermally stressed part, IHAP-55 must add the manufacturer maximum operating/rated temperature and the test-point-to-junction/hotspot interpretation to the thermal acceptance table **before** V4 or V6 can pass. If a measured temperature plus documented measurement/model uncertainty can exceed a registered component limit, the run is FAIL.

### Frozen low-voltage product policy

For the first reference implementation:

- normal battery-backed operation must initiate cutoff at **2.70 V ±0.05 V** measured at BATT under the defined low-current validation condition;
- deliberate continued operation below **2.50 V** is prohibited;
- battery-backed restart after low-voltage cutoff requires **BATT >=3.00 V ±0.05 V**, or restoration of valid USB input;
- the resulting nominal voltage hysteresis is **0.30 V** and must not produce repeated cutoff/restart oscillation;
- IHAP-55 may supersede these values only through an explicit reviewed design change supported by the accepted MJ1 specification and converter operating requirements.

## Required instrumentation

Minimum instrumentation for ordinary bring-up:

- digital multimeter for voltage, continuity, resistance and steady-state current;
- serial/host logging sufficient to detect ESP32-C3 reboot/brownout/re-enumeration;
- timer/timestamps for endurance testing;
- calibrated or characterized temperature measurement suitable for the frozen thermal acceptance table;
- resistor substitution / switching fixture capable of simulating the frozen NTC network's normal, hot, cold, open and short conditions;
- current-limited bench source or equivalent bounded battery simulator for cell-side protection and reverse-blocking verification without intentionally hard-shorting or reverse-driving the actual Li-ion cell;
- source-current measurement capable of resolving the combined node + charger input current around the configured input-current limit.

Additional instrumentation is **mandatory for the frozen >=1.0 A transient/headroom requirement**:

- an electronic load or MOSFET fixture capable of repeatable **baseline↔1.0 A** transitions at the 5 V product SYS bus;
- a reference **10–90% current-transition time <=100 µs** on both rising and falling edges, unless final load characterization demonstrates a faster edge that must then be used;
- an oscilloscope or equivalent acquisition instrument with sufficient bandwidth to capture sub-millisecond rail excursions; **>=20 MHz analog bandwidth** is the reference minimum unless the final regulator validation method demonstrates an equivalent or stronger capture capability;
- a low-inductance probing arrangement at the product 5 V SYS test point.

A generic USB display power meter is not an acceptable substitute for the mandatory transient capture.

## Physical test sequence — IHAP-55

### V1 — Unpowered PCB inspection

- verify polarity, continuity and absence of unintended shorts;
- inspect battery connector/holder polarity;
- verify reverse-battery blocking or mechanical keying implementation;
- verify the cell-side over-current interruption element is physically/electrically upstream of the BAT-net fault paths it is intended to cover;
- verify USB-C CC and input-protection population;
- verify MP2636 / post-regulator / 3.3 V regulator / inductor / sense-network population against BOM;
- verify NTC path and test points;
- verify the thermal acceptance table is complete for every dissipative power component before powered thermal tests.

### V2 — USB-C normal-source bring-up, no battery

- apply the accepted 5 V USB-C source;
- confirm VIN and the intermediate pass-through node;
- confirm **regulated 5 V product SYS**, not merely the MP2636 pass-through node;
- steady-state 5 V SYS PASS band: **4.75–5.25 V**, unless the selected downstream load requires tighter limits;
- confirm 3.3 V rail;
- verify the node can boot without a battery;
- record steady-state current and temperature;
- verify no unintended voltage appears on disconnected battery terminals beyond the expected charger behavior.

### V3 — Received cell / holder inspection

- confirm received LG MJ1 markings and condition;
- confirm non-destructive fit/contact pressure in the owned holder;
- verify polarity labeling;
- confirm the final reverse-insertion control cannot be bypassed during ordinary installation/service;
- confirm the cell-side protection path remains in-circuit during ordinary installation/service;
- record open-circuit cell voltage before first connection.

### V4 — Controlled charging, combined-input-limit and mandatory NTC fault validation

Charge-behavior checks:

- verify ~1 A target charge current within the tolerance frozen in the schematic/PMIC configuration;
- verify cell terminal voltage remains within the accepted **4.20 ±0.05 V** maximum-charge envelope;
- verify charge termination / auto-recharge behavior as observable;
- operate the representative node while charging and verify system-load priority;
- measure total USB input current while the node operates and the charger requests maximum permitted charge current;
- force the source/load combination toward the configured ILIM and verify charging current is reduced before product SYS collapses;
- PASS only if measured input current does not exceed the frozen worst-case ILIM and **does not exceed 1.50 A** for the reference source, accounting for instrument uncertainty;
- record cell, MP2636, inductor and post-regulator temperatures.

Thermal PASS criteria during charging:

- measured cell temperature remains **0–45 °C**;
- MP2636 estimated/calculated junction temperature remains **<=125 °C**;
- no selected component exceeds its frozen manufacturer-derived limit in the thermal acceptance table;
- thermal shutdown, charge cycling caused by overheating, discoloration, odor, deformation or uncontrolled temperature rise is FAIL.

**NTC validation is mandatory, not optional.** Use a resistor/switching fixture derived from the frozen NTC schematic and PMIC thresholds. Exercise at minimum:

1. valid/normal NTC equivalent;
2. cold out-of-window equivalent;
3. hot out-of-window equivalent;
4. NTC open-circuit;
5. NTC short-circuit.

PASS criteria:

- valid/normal equivalent permits charging when all other charge preconditions are valid;
- both hot and cold out-of-window equivalents inhibit charging;
- NTC open and short are fail-bounded and must inhibit charging, either directly through the PMIC TS behavior or through an explicitly reviewed equivalent control;
- the product 5 V SYS remains stable while each NTC fault is asserted;
- restoring the valid/normal NTC equivalent produces deterministic recovery without charge on/off oscillation;
- actual resistor values, measured TS voltage/state and observed charge-current response are recorded.

If the selected NTC topology cannot make open and short fail-bounded, the schematic does **not** satisfy this contract and must be revised before acceptance.

### V5 — Battery mode / product 5 V regulation

Across representative battery voltages:

- verify intermediate boost behavior;
- verify product 5 V SYS remains **4.75–5.25 V steady-state**;
- verify 3.3 V rail stability;
- exercise ESP32 Wi-Fi, LD2410C, OLED and selected environmental/reed interface;
- record brownout/reset evidence;
- keep the MJ1 within **-20 to 60 °C** during discharge operation and within all component limits in the thermal acceptance table.

### V6 — Mandatory 0.5 A continuous load / thermal test

With USB input and separately with battery backup at representative battery voltages:

- apply **0.5 A continuous** at the regulated 5 V product SYS bus in addition to, or using an equivalent controlled replacement for, the node load;
- maintain the test until the monitored temperatures have reached a stable plateau or the defined test-duration limit in IHAP-55;
- PASS only if product SYS remains **4.75–5.25 V**, no protection oscillation/reset/brownout occurs, and all thermal limits remain satisfied;
- battery-mode cell temperature must remain **-20 to 60 °C**;
- MP2636 estimated/calculated junction temperature must remain **<=125 °C**;
- each selected regulator/inductor/protection component must remain within its frozen manufacturer-derived limit;
- any thermal shutdown is FAIL;
- record temperatures, ambient temperature, battery voltage, load and duration.

### V7 — Mandatory 1.0 A bidirectional load-step / headroom test

This test is **not optional**.

- establish a repeatable baseline load representative of the node or approximately 0.1–0.15 A;
- transition **baseline ->1.0 A** and **1.0 A -> baseline**;
- each current edge must have a measured 10–90% transition time **<=100 µs**, unless final measured node transients require a faster reference edge;
- capture the 5 V SYS waveform and load-current waveform at the PCB test point with the required oscilloscope/acquisition setup;
- repeat in normal USB mode and battery mode at representative high, mid and low accepted battery voltages;
- log ESP32 reset/brownout state during both edges.

PASS criteria:

- no uncontrolled rail collapse or protection oscillation;
- no ESP32 reset/brownout attributable to either load edge;
- steady-state after each transition returns to **4.75–5.25 V**;
- captured transient does not fall below **4.5 V** or rise above **5.5 V**;
- the rail returns to the 4.75–5.25 V steady-state band within **2 ms** after each load transition;
- no frozen component/cell thermal limit is exceeded;
- if any selected downstream component requires a tighter transient limit, the tighter component limit supersedes these generic acceptance numbers.

The waveforms, measured current-edge rise/fall times, battery voltage and probe point are mandatory evidence.

### V8 — USB loss / backup transfer across accepted battery range

Execute the transfer at all of these battery conditions using a battery simulator or controlled cell state:

- **high:** 4.10 V ±0.10 V;
- **mid:** 3.60 V ±0.10 V;
- **low:** 2.80 V ±0.05 V, i.e. above the frozen 2.70 V cutoff but close to the low end of accepted backup operation.

At each battery condition, repeat with the representative node load and with a controlled higher load up to the validated continuous envelope where practical:

- start with normal USB operation;
- remove normal USB input;
- verify automatic transition to battery-backed regulated 5 V;
- verify no prohibited backfeed toward USB;
- capture product 5 V SYS during the transfer with suitable bandwidth instrumentation;
- record whether any ESP32 reset/brownout occurs;
- verify all thermal and rail limits;
- **PASS target: no-reset transfer at every required battery condition**.

### V9 — Normal-source restoration across accepted battery range

At the same high/mid/low battery conditions used in V8:

- restore valid USB input;
- verify deterministic return to normal source;
- verify charging resumes as designed where the cell state permits charging;
- verify no source oscillation or reset loop;
- verify no backfeed;
- capture product 5 V SYS during restoration;
- verify all rail/thermal limits and record reset/brownout state.

### V10 — Numeric low-voltage cutoff / recovery behavior

Use a current-limited battery simulator or controlled discharge fixture so the threshold can be exercised repeatably without intentionally deep-discharging the actual cell.

PASS criteria:

- battery-backed operation cuts off at **2.70 V ±0.05 V** under the frozen validation load/measurement condition;
- product behavior never intentionally sustains MJ1 discharge below **2.50 V**;
- after low-voltage cutoff, battery-backed restart does not occur until **BATT >=3.00 V ±0.05 V** or valid USB input is restored;
- no repeated cutoff/restart oscillation occurs while BATT is between the cutoff and recovery thresholds;
- the actual cutoff voltage, recovery voltage, hysteresis, rail/reset behavior and load condition are recorded.

### V11 — Mandatory quantitative load characterization transferred from prior ADRs

The following measurements remain mandatory even though execution ownership moved from IHAP-49 to IHAP-55:

- ESP32-C3 final implementation: 3.3 V rail current in representative idle/Wi-Fi-active conditions and observable peak/transient behavior with appropriate instrumentation;
- LD2410C: quantitative 5 V current contribution on the final wiring/interface;
- OLED: active-display current, blank/sleep current where supported, and a documented sleep/power policy based on the measured values;
- DHT11 standard profile and BME280 precision profile: quantitative current contribution under the selected sampling policy;
- MC-38/reed input: quantitative closed-loop current contribution for the final pull/network chosen by IHAP-50/implemented on the custom board;
- complete node: normal-source input current, 5 V product SYS current, 3.3 V rail current and brownout/reset evidence under representative operation.

These measurements satisfy the still-valid quantitative power obligations originally assigned to IHAP-49 by **ADR-0001, ADR-0002, ADR-0003, ADR-0004 and ADR-0005**. ADR-0007 transfers execution ownership to IHAP-55; it does not waive the evidence.

### V12 — Backup endurance

- fully charge the accepted cell;
- run the complete reference node on battery under representative workload;
- log start/end, periodic cell/SYS readings, temperatures, resets and functional state;
- stop at the frozen low-voltage cutoff;
- record measured runtime.

Only V12 may support a measured backup-autonomy statement for the tested board/cell/configuration.

### V13 — Mandatory cell-side over-current protection verification

This test verifies R-012 / RT-R012-01 without intentionally shorting the actual MJ1 cell.

Precondition:

- the schematic/BOM identifies the cell-side fuse/electronic protection element, its location, current/time threshold or trip curve, and the worst-case legitimate charge/discharge/transient envelope used to size it.

Verification method:

- use a current-limited bench source, protected battery simulator, sacrificial protection sample, or other bounded fixture representing the BAT source;
- apply a controlled over-current condition on the protected downstream BAT path sufficient to exercise the frozen protection threshold without exceeding the fixture/component limits;
- verify the protection element interrupts/limits the current within the frozen design threshold/time;
- verify normal operation can be restored according to the selected protection technology (replace fuse, reset protection switch, or equivalent);
- confirm the PMIC SYS/boost current limit is **not** the only element covering this upstream BAT fault path.

PASS criteria:

- the protected BAT path is interrupted/limited as designed;
- measured trip/limit behavior is consistent with the frozen component specification and design rationale;
- no intentional hard short is applied across the actual Li-ion cell;
- post-test inspection reveals no damage that invalidates the tested PCB/protection sample.

### V14 — Mandatory combined source-current-limit / system-load-priority verification

This test isolates the input-current-limit requirement from ordinary V4 charging observations.

- use a regulated 5 V source capable of current readback/current limiting and configure the board with the frozen ILIM setting;
- connect a battery simulator/cell state that causes the charger to request near-maximum programmed charge current;
- operate the representative complete node, including Wi-Fi/radar/display activity;
- increase controlled SYS load as needed to approach the source limit without exceeding the validated board envelope;
- measure total USB input current, charge current and product SYS voltage.

PASS criteria:

- total measured USB input current remains **<=1.50 A** and <= the frozen worst-case ILIM, including instrument uncertainty;
- as system load increases, charging current is reduced before product SYS leaves **4.75–5.25 V**;
- no source oscillation, reset/brownout or repeated charger enable/disable loop occurs;
- measured source current, charge current, SYS load and rail voltage are recorded together.

### V15 — Mandatory functional reverse-polarity verification when electrical blocking is selected

If the final design uses **mechanical keying only**, V15 electrical reverse-drive is not applicable and V1/V3 must prove ordinary insertion cannot physically reverse the cell. If any **electrical reverse-battery blocking/protection** is relied upon, V15 is mandatory.

- disconnect the real MJ1 cell;
- use a current-limited battery simulator set to **4.20 V** with a **10 mA maximum current limit**;
- connect the simulator to the battery input with reversed polarity through the normal service interface;
- observe input current, BAT-protected node, intermediate SYS, product 5 V SYS and 3.3 V rails.

PASS criteria for the electrical-blocking path:

- steady reversed-source current is **<=1 mA** after settling, unless the selected protection component datasheet specifies a lower limit that then governs;
- product 5 V SYS and 3.3 V rails do not start from the reversed source and remain **<=0.3 V**;
- no component heats abnormally or enters destructive conduction;
- after returning to correct polarity, normal operation is restored without damage;
- the real Li-ion cell is never intentionally reverse-connected for this verification.

## Risk-to-test map

| Canonical risk / exposure | Primary validation evidence |
|---|---|
| R-012 battery over-charge / charge control | V4 |
| R-012 NTC hot/cold/open/short | V4 |
| R-012 input-current / charging priority interaction | V4 + V14 |
| R-012 over-discharge / recovery | V10 |
| R-012 reverse insertion | V1 + V3 + V15 when electrical blocking is used |
| R-012 cell-side over-current | V13 |
| R-012/R-013 thermal overstress | V4 + V5 + V6 + V7 + V8 + V9 against frozen thermal table |
| R-013 regulated product rail | V2 + V5 + V6 |
| R-013 1 A transient / brownout | V7 both edges |
| R-013 USB loss / backfeed | V8 high/mid/low battery conditions |
| R-013 source restoration / oscillation / backfeed | V9 high/mid/low battery conditions |
| R-013 reference-source input-current limit / system priority | V14 |
| R-013 final-node quantitative loads | V11 |
| R-013 measured backup runtime | V12 |

## Acceptance boundary

Physical PASS results support only the tested custom-board revision and conditions. They do not establish certification, fire safety, commercial readiness or universal cell/board equivalence.

**IHAP-49 may remain closed because ADR-0007 explicitly transfers these still-mandatory implementation measurements to IHAP-55.** IHAP-57 keeps R-012/R-013 treatment effectiveness open until the evidence above exists. Any downstream evidence that contradicts the accepted architecture contract must reopen/supersede ADR-0007 rather than silently weakening tests.
