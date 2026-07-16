# IHAP-47 — Reproducible MC-38 Physical Test Protocol

**Issue:** [IHAP-47](https://niccolopiazzi01.atlassian.net/browse/IHAP-47)  
**Protocol state:** Ready for Project Owner execution  
**Physical execution state:** Not started  
**Scope:** qualify owned wired magnetic contacts for binary door-state telemetry only

## 1. Objective

Determine, for identified owned specimens and a controlled geometry:

- magnet-near and magnet-far electrical behavior;
- unambiguous reed-form interpretation;
- observed pull-in and drop-out distances;
- alignment sensitivity;
- raw transition behavior and bounce;
- repeated-cycle consistency;
- disconnected-wire and short-to-ground behavior;
- whether the internal pull-up is sufficient for the temporary bench setup.

The protocol does not validate final wiring, power consumption, autonomy, enclosure, mounting adhesive, access control, tamper detection or alarm behavior.

## 2. Required Equipment

Minimum:

- two owned MC-38 / DC-38 contact-and-magnet pairs when available;
- ESP32-C3 board accepted by ADR-0001;
- PC USB data cable;
- digital multimeter with continuity or resistance mode;
- breadboard or secure temporary terminals;
- jumper wires;
- metric ruler with 1 mm resolution, preferably a caliper;
- non-ferromagnetic alignment surface;
- camera or phone for evidence photographs.

Optional:

- 10 kOhm external pull-up resistor for comparison;
- logic analyzer or oscilloscope for independent bounce timing;
- removable tape for the measurement fixture.

The optional instruments improve evidence quality but do not authorize power, rail or alarm-grade claims.

## 3. Specimen Identification

Assign stable local identifiers before testing:

- `MC38-A`;
- `MC38-B`.

Do not use seller claims as specimen facts.

Record for each specimen:

- visible text and markings;
- sensor-body dimensions;
- magnet-body dimensions;
- cable length;
- visible cable or housing differences;
- whether the sensor and magnet were supplied as a pair.

Take the photographs listed in the evidence manifest before electrical testing.

## 4. Safety and Scope Checks

- Disconnect the ESP32-C3 before using continuity or resistance mode.
- Do not apply mains voltage or an external contact load.
- Use ESP32-C3 3.3 V GPIO logic only.
- Do not measure current, rail regulation or battery autonomy in this task.
- Do not mount the sensor permanently.
- Do not interpret any result as security, alarm, antifurto, access-control, intrusion-detection or tamper evidence.

## 5. Test A — Passive Continuity and Reed Form

### Procedure

For each specimen:

1. Disconnect it from all electronics.
2. Place the multimeter across the two contact wires.
3. Keep the paired magnet at least 100 mm away.
4. Record resistance or continuity as `open`, `closed` or `unstable`.
5. Bring the magnet into direct, repeatable side-by-side alignment without forcing the housings together.
6. Record resistance or continuity again.
7. Repeat the far/near cycle ten times.
8. Reverse magnet orientation and repeat two cycles as an observation only.

### Interpretation

Use component terminology, not door-installation shorthand:

| Magnet far | Magnet near | Inferred behavior |
|---|---|---|
| Open | Closed | Form A / normally open relative to magnetic actuation |
| Closed | Open | Form B / normally closed relative to magnetic actuation |
| Other or unstable | Other or unstable | Do not classify; stop and investigate |

### Pass gate

- all ten cycles for a specimen produce the same far and near states;
- at least one specimen can be classified unambiguously;
- disagreement between specimens is reported, not averaged away.

A commercial listing that calls a sensor `NC` does not override the observed reed-form test.

## 6. Test B — Pull-In and Drop-Out Distance

### Fixture

- Keep sensor and magnet long axes parallel.
- Fix the sensor.
- Move only the magnet along a marked straight line.
- Define `0 mm` as the closest repeatable non-forced housing position.
- Use the same reference faces for all repetitions.
- Keep ferromagnetic objects away from the fixture.

### Procedure

For each specimen:

1. Start with the magnet far enough that the electrical circuit is in the magnet-far state.
2. Move the magnet toward the sensor slowly.
3. Record the distance at the first stable transition: `pull_in_mm`.
4. Continue to the near position.
5. Move the magnet away slowly.
6. Record the distance at the first stable release: `drop_out_mm`.
7. Repeat ten times.

### Reporting

Report:

- minimum;
- maximum;
- median;
- all individual values;
- measurement tool resolution;
- fixture photograph;
- any hesitation or unstable zone.

Do not report a universal MC-38 operating gap. The result applies only to the tested specimen and geometry.

## 7. Test C — Alignment Sensitivity

Test at a conservative near distance derived from Test B, not at the observed transition threshold.

For each specimen, move the magnet while retaining parallel orientation:

- lateral offset in 1 mm increments;
- vertical offset in 1 mm increments;
- optional rotation observations at 15 degree increments.

Record the last stable position and the first unstable or released position.

This test informs IHAP-51. It does not choose the final mounting margin.

## 8. Test D — Bench GPIO Mapping

Temporary wiring:

```text
ESP32-C3 GPIO6 ---- contact ---- GND
        |
        +---- internal pull-up enabled by test firmware
```

GPIO6 is a test-harness default inherited from historical prototype evidence. It is not the final IHAP-50 pin decision.

### Procedure

1. Flash the IHAP-47 harness.
2. Start the local capture script.
3. Send `snapshot` with magnet far.
4. Send `snapshot` with magnet near.
5. Confirm:
   - open electrical circuit -> raw level `1`;
   - closed electrical circuit -> raw level `0`.
6. Repeat for both specimens.

### Stop condition

Stop if the GPIO is floating, unstable or does not match the passive continuity result.

## 9. Test E — Raw Transition and Bounce Capture

The harness records raw level transitions during a bounded capture window. It does not claim oscilloscope-grade timing.

For each specimen and direction:

1. Send `begin BOUNCE_OPEN_TO_CLOSED MC38-A`.
2. Move the magnet once from the stable far position to the stable near position.
3. Wait one second.
4. Send `end`.
5. Repeat ten times.
6. Repeat ten times for `BOUNCE_CLOSED_TO_OPEN`.

Record:

- raw transition count;
- timestamp of each transition;
- total interval from first to final transition;
- final stable level;
- whether buffer overflow occurred.

When a logic analyzer is available, capture the same transition independently and state the instrument and sampling rate.

### Debounce decision rule

Do not predeclare a production interval. After the observations:

- report the maximum observed transition interval;
- propose a stable-state debounce interval with explicit engineering margin;
- keep the proposed interval `[UNVALIDATED]` until the repeated-cycle test passes with it.

The historical three-read majority method is not accepted automatically.

## 10. Test F — Repeated Cycle Consistency

For each specimen:

1. Use the observed conservative near and far positions.
2. Execute 50 complete near/far cycles.
3. Capture one stable snapshot after every movement.
4. Record expected and observed raw levels.
5. Do not discard failed or ambiguous cycles.

Minimum decision input:

- cycle count;
- mismatches;
- unstable readings;
- missed transitions;
- repeated transitions after debounce simulation.

A zero-mismatch result supports the tested session only. It does not establish production reliability.

## 11. Test G — Failure-Mode Observations

With the ESP32-C3 and capture running, record these controlled cases:

| Case | Expected electrical result under pull-up topology |
|---|---|
| Contact circuit open | `HIGH` |
| One contact conductor disconnected | `HIGH` |
| Magnet removed or far | Depends on Test A; expected open circuit for the historical candidate topology |
| Contact conductors shorted together / GPIO connected to GND | `LOW` |
| Boot with contact circuit open | Internal state must remain uninitialized until first stable sample, then `HIGH` |
| Boot with contact circuit closed | Internal state must remain uninitialized until first stable sample, then `LOW` |

Use only low-voltage bench wiring. Never short a supply rail.

Required conclusion:

> Under a simple two-wire pull-up topology, a legitimate open circuit and several fault conditions are electrically indistinguishable.

If the Project Owner requires fault distinction, stop. A supervised loop is a scope and architecture change.

## 12. Test H — Internal Pull-Up Adequacy

The ESP32-C3 datasheet describes the internal pull-up as weak and gives a typical value around 45 kOhm. The exact value varies and the final cable is not selected.

For the temporary bench wiring:

1. run the repeated-cycle test with internal pull-up only;
2. note any unstable raw levels;
3. optionally repeat with a 10 kOhm external pull-up to 3.3 V;
4. label the external resistor test as a comparison, not the final circuit.

No final pull decision is made by this protocol. IHAP-50 owns the integrated circuit after cable and connector constraints are known. IHAP-49 owns the quantitative closed-loop current impact.

## 13. Local Data Files

The capture workflow creates local files under `output/<session-id>/`:

- `serial.log` — complete local serial capture;
- `records.jsonl` — parsed firmware records;
- `operator-observations.jsonl` — manual observations entered by the operator;
- `session.json` — local execution metadata;
- `summary.json` — sanitized machine-readable summary;
- `report.html` — standalone human-readable report.

Repository policy:

- do not commit `serial.log`;
- do not commit raw `records.jsonl`;
- review and sanitize `summary.json` and `report.html` before publication;
- remove MAC addresses, private paths and unrelated logs;
- commit only evidence required to support the decision.

## 14. Result Review Gate

The physical handoff is complete only when:

```text
[ ] At least one specimen has repeatable magnet-far and magnet-near behavior.
[ ] Preferably two owned specimens were compared.
[ ] Reed form is reported from observation, not seller wording.
[ ] Pull-in and drop-out distributions are recorded.
[ ] Alignment geometry and measurement resolution are recorded.
[ ] Raw transition captures exist in both directions.
[ ] Repeated-cycle mismatches are reported without filtering.
[ ] Disconnect and short-to-ground observations are recorded.
[ ] Open-door and open-circuit ambiguity is explicitly accepted or escalated.
[ ] No tamper, alarm, access-control or reliability claim is introduced.
[ ] Raw logs remain local and only sanitized summaries are proposed for GitHub.
```

## 15. Mandatory Stop Conditions

Stop and request a decision when:

- specimens disagree on reed behavior;
- a specimen is unstable at a conservative near position;
- the activation envelope is impractical for the expected door geometry;
- the harness buffer overflows repeatedly;
- the contact produces unexplained transitions without movement;
- the internal pull-up is unstable and an external circuit must be frozen;
- a `FAULT`, `UNKNOWN` or tamper state is requested in the external contract;
- wire supervision is requested;
- an alternative sensor technology becomes necessary;
- final power, wiring or mounting work would be pulled into IHAP-47.
