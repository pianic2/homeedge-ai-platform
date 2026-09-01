# IHAP-47 — Lean Automated MC-38 Physical Test Protocol

**Issue:** [IHAP-47](https://niccolopiazzi01.atlassian.net/browse/IHAP-47)  
**Protocol state:** Ready for Project Owner execution  
**Scope:** qualify an owned passive wired magnetic contact for binary door-state telemetry only

## 1. Principle

IHAP-47 validates a technology decision, not a mounting system or a production electrical design.

The default procedure must therefore minimize operator effort and maximize automatic evidence capture.

Normal execution requires the operator to:

- place the magnet FAR or NEAR when prompted;
- move the magnet back and forth during the automated cycle test;
- perform two explicit failure-mode wiring changes.

The operator does **not** manually type JSON observations, individual `snapshot` commands, cycle identifiers or repeated measurements.

## 2. Decision question

The test answers only:

> Is the tested owned passive wired reed-contact specimen suitable for MVP binary electrical door-state telemetry using the temporary ESP32-C3 bench topology?

It does not validate:

- final mounting geometry;
- universal MC-38 specifications;
- production reliability;
- final GPIO or pull network;
- power consumption or autonomy;
- tamper detection;
- alarm, intrusion-detection, antifurto or access-control behavior.

## 3. Required equipment

Minimum:

- one identified owned contact-and-magnet pair, e.g. `MC38-A`;
- ESP32-C3 board accepted by ADR-0001;
- USB data cable;
- secure temporary wiring;
- PC with ESP-IDF and Python environment.

Optional diagnostic equipment:

- multimeter;
- ruler or caliper;
- logic analyzer or oscilloscope.

Optional instruments may be used to investigate anomalies but are not mandatory decision gates.

## 4. Bench topology

```text
ESP32-C3 GPIO6 ---- passive contact ---- GND
        |
        +---- internal pull-up enabled by test firmware
```

Expected temporary bench mapping:

- electrical open -> raw `1`;
- electrical closed -> raw `0`.

GPIO6 is test-only. IHAP-50 owns the final pin and integrated circuit.

## 5. Default execution

Build and flash from `tools/hardware-validation/ihap-47-door-state-sensor/firmware/` when needed:

```bash
idf.py set-target esp32c3
idf.py build
idf.py -p /dev/ttyACM0 flash
```

Then, from the harness root, run:

```bash
python scripts/guided_run.py \
  --port /dev/ttyACM0 \
  --specimen MC38-A
```

Default execution uses **20 complete near/far cycles**.

No manual JSON entry is part of the normal protocol.

## 6. Gate A — FAR/NEAR electrical mapping

The guided runner requests three setup actions:

1. place magnet FAR, at least approximately 100 mm away;
2. place magnet NEAR and aligned;
3. return magnet FAR before automated cycling.

The runner captures firmware snapshots automatically.

### Pass gate

For the historical candidate topology:

- FAR -> raw `1` / electrical open;
- NEAR -> raw `0` / electrical closed;
- return FAR -> raw `1`.

This supports Form A / normally-open behavior relative to magnetic actuation for the tested specimen.

A seller label such as `NC` does not override observed component behavior.

## 7. Gate B — Automated repeated-cycle and raw-transition test

The runner performs the instrumentation and bookkeeping.

For each complete cycle:

1. it starts a bounded raw capture while the magnet is FAR;
2. it prompts the operator to move the magnet NEAR;
3. it polls firmware state until the target level remains stable for the configured stable window;
4. it ends the bounded capture and records all raw transitions;
5. it immediately starts the reverse bounded capture;
6. it prompts the operator to move the magnet FAR;
7. it waits for a stable FAR state and ends the capture;
8. it increments the cycle automatically.

The operator only moves the magnet when prompted.

Default parameters:

- complete cycles: `20`;
- stable window: `150 ms`;
- host status poll interval: `50 ms`;
- firmware raw sampling period: `250 us`.

### Automatically recorded

For every movement:

- initial level;
- expected target level;
- final level;
- raw transition count;
- raw transition span when multiple transitions occur;
- buffer overflow state;
- pass/fail of the stable movement.

For the complete run:

- completed cycles;
- mismatches;
- buffer overflows;
- number of movements with multiple raw transitions;
- maximum observed raw-transition span.

### Pass gate

- all requested complete cycles finish;
- every stable movement ends at the requested target state;
- no unexplained timeout occurs;
- no buffer overflow occurs.

Multiple raw transitions do not automatically fail the sensor decision. They are retained as bounce evidence and inform IHAP-50 debounce work.

A clean single-transition result means only that no additional transition was observed at the harness sampling resolution.

## 8. Gate C — Failure-mode observation

After automated cycling the runner requests only two controlled setup changes.

### C1 — disconnected conductor

With the contact expected closed, disconnect one contact conductor.

Expected under the simple pull-up topology:

```text
raw level = 1
```

This demonstrates that an open contact and an interrupted conductor are electrically indistinguishable.

### C2 — GPIO to GND bench check

Reconnect the sensor and temporarily connect GPIO6 to GND using only the low-voltage bench wiring.

Expected:

```text
raw level = 0
```

Never short a supply rail.

### Required conclusion

> Under a simple two-wire pull-up topology, a legitimate open circuit and several wiring/fault conditions are electrically indistinguishable.

If fault distinction or wire supervision becomes a requirement, stop: that is an architecture change outside IHAP-47.

## 9. Internal pull-up bench adequacy

No separate repetitive pull-up test is required.

For IHAP-47 the temporary internal pull-up is considered adequate for the bench session when:

- FAR and NEAR mapping are stable;
- all automated cycles complete without unexplained mismatch;
- no spontaneous unstable state prevents the stable-state gate.

The final pull-network decision remains IHAP-50. Quantitative power impact remains IHAP-49.

## 10. Measurements deliberately removed from the blocking gate

Repeated pull-in/drop-out distance and alignment sweeps are **not blocking IHAP-47 evidence**.

Reason:

- operating gap and mounting margin are mechanical integration properties;
- the final enclosure, door geometry and cable route are not frozen here;
- repeated manual millimetre entry does not materially improve the sensor-technology decision.

These measurements belong to **IHAP-51 — mounting/integration** when the actual geometry is available.

A single rough gap or alignment observation may be retained as optional context, but it must not force repeated manual data entry or block the IHAP-47 decision.

## 11. Boot-state and production-debounce checks

Boot initialization semantics, final debounce interval, final GPIO and final pull network are implementation concerns owned by IHAP-50.

IHAP-47 may retain observed raw-transition data for that handoff, but it does not require repeated boot-state execution as a sensor-selection gate.

## 12. Evidence files

The guided runner creates one local session under:

```text
output/<session-id>/
```

Expected files:

- `serial.log` — complete local serial evidence;
- `records.jsonl` — parsed firmware records;
- `operator-observations.jsonl` — runner-generated observations;
- `session.json` — execution metadata;
- `guided-result.json` — machine-readable final guided result;
- `summary.json` — generated summary after successful execution;
- `report.html` — generated human-readable report after successful execution.

### Preservation rule

Do not delete raw session files before the task is closed.

`serial.log` and `records.jsonl` remain local and are not committed to GitHub.

Only reviewed, sanitized, decision-relevant artifacts may be copied into `docs/evidence/IHAP-47/`.

## 13. Stop conditions

Stop and investigate only when:

- FAR/NEAR mapping does not match passive continuity behavior;
- the sensor cannot reach a stable requested state;
- repeated movements produce unexplained mismatches;
- buffer overflow occurs;
- transitions occur persistently without physical movement;
- specimens materially disagree if a second specimen is tested;
- fault distinction, wire supervision or a security state is requested;
- final power, wiring or mounting decisions are being pulled into IHAP-47.

## 14. Result review gate

Physical evidence is sufficient for IHAP-47 review when:

```text
[ ] At least one owned specimen has deterministic FAR/NEAR behavior.
[ ] Automated repeated cycling completed with all mismatches reported.
[ ] Raw transition behavior was captured automatically.
[ ] Buffer overflow status is known.
[ ] Disconnected-conductor ambiguity is demonstrated and accepted or escalated.
[ ] Temporary internal pull-up was stable for the bench session.
[ ] No alarm, tamper, intrusion, access-control or universal reliability claim is introduced.
[ ] Raw logs remain local and preserved until task closure.
```

A second specimen is useful for confidence but is not mandatory unless the first specimen is anomalous or the Project Owner explicitly requires cross-specimen qualification.

## 15. Manual diagnostic mode

`scripts/capture_serial.py` and direct firmware commands remain available for troubleshooting only.

They are not the normal validation workflow. Manual `@observe` JSON entry is not required for a standard IHAP-47 run.
