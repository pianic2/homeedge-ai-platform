# IHAP-49 — Power Subsystem Validation Plan / IHAP-55 Handoff

**Status:** architecture validation complete enough for ADR review; physical implementation validation delegated to IHAP-55

## Objective

Define the tests required to prove that the **custom PCB implementation** satisfies ADR-0007:

- regulated 5 V USB-C as the normal source;
- LG INR18650-MJ1 1S battery as backup only;
- integrated charger + system power path + battery-to-5 V boost;
- automatic source transfer without prohibited backfeed;
- controlled battery charging and low-voltage behavior;
- sufficient 5 V / 3.3 V headroom for the reference node.

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
- custom-PCB power contract and preferred integrated PMIC direction frozen.

The unresolved exact RPROG/protection-controller behavior of the owned 4056E module is **not a closure blocker** because that module is not selected for the final reference PCB.

## Reference implementation preconditions for IHAP-55

Before physical bring-up, IHAP-55 must freeze:

- MP2636GR-P schematic implementation or an explicitly reviewed superseding PMIC;
- 4.2 V charge-voltage selection;
- ~1.0 A nominal charge-current setting;
- 5.0 V boost/SYS setting;
- >=0.5 A continuous / >=1.0 A transient SYS design envelope;
- USB-C CC/input-protection implementation;
- 3.3 V regulator;
- NTC network;
- battery reverse-polarity strategy;
- holder connector/polarity;
- input-current-limit profile for the reference 5 V >=1.5 A source;
- automatic MODE/source-transfer logic;
- test points for VIN, BATT, SYS 5 V and 3.3 V.

## Minimum instrumentation

- digital multimeter for voltage, continuity, resistance and steady-state current;
- serial/host logging sufficient to detect ESP32-C3 reboot/brownout/re-enumeration;
- timer/timestamps for endurance testing;
- temperature measurement suitable for comparative bench observation.

A generic USB power meter is not mandatory. If an unexplained transient remains, escalate to suitable higher-bandwidth instrumentation instead of inventing a transient claim from slow average measurements.

## Physical test sequence — IHAP-55

### V1 — Unpowered PCB inspection

- verify polarity, continuity and absence of unintended shorts;
- inspect battery connector/holder polarity;
- verify USB-C CC and input-protection population;
- verify MP2636 / regulator / inductor / sense-network population against BOM;
- verify NTC path and test points.

### V2 — USB-C normal-source bring-up, no battery

- apply the accepted 5 V USB-C source;
- confirm VIN and 5 V SYS;
- confirm 3.3 V rail;
- verify the node can boot without a battery;
- record steady-state current and abnormal heating;
- verify no unintended voltage appears on disconnected battery terminals beyond the expected charger behavior.

### V3 — Received cell / holder inspection

- confirm received LG MJ1 markings and condition;
- confirm non-destructive fit/contact pressure in the owned holder;
- verify polarity labeling and reverse-insertion mitigation;
- record open-circuit cell voltage before first connection.

### V4 — Controlled charging

- verify ~1 A target charge current within accepted tolerance;
- verify cell terminal voltage approaches but does not exceed the accepted 4.2 V charging envelope;
- verify charge termination / auto-recharge behavior as observable;
- verify system-load priority while the node operates;
- observe battery/PMIC/inductor temperature behavior;
- verify NTC fault behavior non-destructively where practical.

### V5 — Battery boost / SYS regulation

Across representative battery voltages:

- verify 5 V SYS remains within the frozen tolerance;
- verify 3.3 V rail stability;
- exercise ESP32 Wi-Fi, LD2410C, OLED and selected environmental/reed interface;
- record brownout/reset evidence;
- verify load-headroom target with a controlled test load where practical.

### V6 — USB loss / backup transfer

- start with normal USB operation and valid charged backup;
- remove normal USB input;
- verify automatic transition to battery-backed 5 V;
- verify no prohibited backfeed toward USB;
- record whether any ESP32 reset/brownout occurs;
- **PASS target: no-reset transfer**.

### V7 — Normal-source restoration

- restore valid USB input;
- verify deterministic return to normal source;
- verify charging resumes as designed;
- verify no source oscillation or reset loop;
- verify no backfeed.

### V8 — Low-voltage / recovery behavior

Within safe non-destructive limits:

- verify battery discharge does not intentionally continue below the accepted cell boundary;
- verify any graceful low-battery warning/shutdown behavior;
- verify recovery after normal USB source returns;
- do not perform destructive short/reverse tests merely to claim protection.

### V9 — Backup endurance

- fully charge the accepted cell;
- run the complete reference node on battery under representative workload;
- log start/end, periodic cell/SYS readings, resets and functional state;
- stop at the accepted low-voltage endpoint;
- record measured runtime.

Only V9 may support a measured backup-autonomy statement for the tested board/cell/configuration.

## Acceptance boundary

Physical PASS results support only the tested custom-board revision and conditions. They do not establish certification, fire safety, commercial readiness or universal cell/board equivalence.

**IHAP-49 can be accepted before V1–V9 are executed because it is the architecture-decision task; IHAP-55 is the explicit implementation/validation task.** Any downstream evidence that contradicts this contract must reopen/supersede ADR-0007 rather than silently weakening tests.
