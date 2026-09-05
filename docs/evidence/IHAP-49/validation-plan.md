# IHAP-49 — Power Subsystem Validation Plan

**Status:** Proposed test plan; Project Owner review pending

## Objective

Validate a dual-source reference power subsystem in which regulated 5 V USB-C is the normal operating source and a rechargeable single-cell battery path is used only as backup for blackout or cable/input interruption.

The validation must show electrical compatibility and controlled recovery. It must not turn component arithmetic into safety, certification or autonomy claims.

## Preconditions

The following must be frozen before the corresponding physical tests begin:

- exact reference cell SKU and provenance;
- exact holder;
- owned 4056E charger/protection board specimen;
- exact 1S-to-5 V converter;
- normal/backup source-selection or switchover circuit;
- power switch and polarity-control strategy;
- normal 5 V USB-C source profile and cable;
- final IHAP-50 interconnect mapping where required for the integrated fixture.

## Instrumentation

Minimum planned instrumentation:

- digital multimeter capable of DC voltage, resistance/continuity and DC current measurements;
- serial/host logging sufficient to detect ESP32-C3 reboot/brownout/re-enumeration;
- timer/log timestamps for controlled discharge testing.

A generic USB power meter is not a requirement. If the integrated system exhibits unexplained transient failures that cannot be bounded with datasheet constraints and functional brownout/reset evidence, the test plan must escalate to higher-bandwidth measurement rather than claim transient behavior from a slow display meter.

## Test sequence

### 1. Unpowered inspection

- verify terminal mapping and polarity;
- verify continuity and absence of unintended shorts;
- inspect holder fit and contact pressure;
- record cell orientation and reverse-insertion mitigation;
- verify `B+/B-` versus `OUT+/OUT-` wiring on the charger/protection board.

### 2. Normal 5 V USB-C operation

With the complete reference load connected:

- verify node boots from the normal source;
- record 5 V rail and 3.3 V rail;
- measure representative integrated input current;
- exercise Wi-Fi activity, LD2410C sensing, OLED update and environmental/reed inputs;
- record any brownout, reboot, USB re-enumeration or functional loss.

### 3. Battery-path regulation

Across representative battery voltages allowed by the selected cell/protection architecture:

- verify regulated 5 V output remains inside the final accepted tolerance;
- verify 3.3 V rail remains stable through the board regulator;
- exercise the complete reference load;
- record converter thermal behavior qualitatively and quantitatively where feasible without making certification claims.

### 4. Normal-source interruption / backup takeover

- start from stable normal USB-C operation with a valid charged backup cell;
- interrupt normal 5 V source in a controlled manner;
- record whether the node remains powered, resets, browns out or loses state;
- record 5 V and 3.3 V behavior observable with available instrumentation;
- verify presence sensing and basic node operation after takeover.

A seamless no-reset transfer is not assumed. If the selected architecture intentionally permits a controlled reboot on source loss, that behavior must be explicit in the ADR and downstream runtime expectations.

### 5. Normal-source restoration

- restore normal USB-C power;
- verify deterministic source recovery;
- verify no prohibited backfeed into the charger, battery or external source;
- verify node operational recovery and absence of repeated reset loops.

### 6. Charging behavior

Until an explicit load-sharing/power-path implementation is selected and validated, **charging while the node is operating from the battery path is prohibited**.

Validate:

- charger input voltage;
- charge current for the selected cell and RPROG configuration;
- terminal voltage behavior;
- charge-complete indication/termination behavior as observable;
- post-charge battery voltage;
- absence of abnormal heating under the tested conditions.

### 7. Protection/failure cases

Within safe bench limits and without deliberately exceeding component ratings:

- validate low-voltage cutoff/recovery behavior where supported by the selected protection architecture;
- validate reverse-polarity prevention/mitigation strategy by inspection and non-destructive tests;
- validate that normal-source removal/restoration cannot create an obvious backfeed path;
- verify that a disconnected/open battery does not cause uncontrolled node behavior;
- verify controlled node recovery after power-cycle.

### 8. Backup endurance

After exact hardware and normal load behavior are stable:

- fully charge the selected cell using the accepted procedure;
- operate the complete reference node on backup battery under a representative workload;
- log start time, periodic rail/battery measurements, resets and functional status;
- stop at the defined protection/cutoff or accepted endpoint;
- record measured runtime.

Only this controlled run may support an MVP backup-autonomy statement for the tested specimen/configuration.

## Pass boundary

A PASS supports only the tested reference implementation and conditions. It does not prove universal cell/module equivalence, certification, fire safety, production readiness or deployment suitability outside the documented envelope.
