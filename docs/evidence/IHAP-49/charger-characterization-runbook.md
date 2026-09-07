# IHAP-49 — 4056E Charger/Protection Characterization Runbook

**Status:** executable staged runbook; exact charger/protection qualification incomplete

## Purpose

Characterize the owned USB-C 4056E-family charger/protection board before connecting the selected LG INR18650-MJ1 cell.

This runbook intentionally begins with an **unpowered-only stage** that can be executed while the cell order is pending. No battery and no USB source are required for Stage C0.

The `4056E` marking is treated as a family-level clue only. Reference 4056E datasheets are used to interpret the PROG-resistor relationship, but they do not prove the exact silicon manufacturer or protection-controller thresholds of the owned board.

## Safety / stop rules

For Stage C0:

- USB-C **disconnected**;
- no battery/cell installed;
- no load connected to `OUT+ / OUT-`;
- do not short adjacent SMD pads with the probes;
- do not attempt destructive short-circuit, reverse-polarity or live-current tests;
- if a measurement requires significant force or unstable probe contact, stop and repeat with better access rather than scraping component metallization.

## Equipment

- digital multimeter with resistance/continuity mode;
- owned 4056E charger/protection board;
- macro photo or magnification sufficient to see PCB designators.

## Stage C0 — Charge-current programming resistor

### C0.1 Board state

Confirm and record:

```text
USB-C disconnected: YES / NO
Battery connected:  NO
OUT load connected: NO
Board visibly damaged: YES / NO
```

If any power source or cell is connected, **STOP**.

### C0.2 Identify R3

Using the existing board orientation with USB-C at the top and `B+/B-` pads at the bottom, locate the resistor marked by PCB designator **`R3`**, immediately to the left of charger IC `U1`.

Current photographic evidence indicates that R3 is the candidate resistor connected to the `PROG` function of the 4056E-family charger. The electrical measurement below is required before that relationship is used quantitatively.

### C0.3 Measure R3 resistance

1. Set the multimeter to resistance mode.
2. With the board completely unpowered, place one probe on each metallic end of **R3**.
3. Keep both probes clear of neighboring pads.
4. Wait for the reading to stabilize.
5. Record the value in ohms/kilohms.
6. Reverse the probe positions and repeat once.

Record:

| Measurement | Result |
|---|---:|
| R3 pass 1 | TBD |
| R3 pass 2, probes reversed | TBD |
| Difference materially significant? | TBD |

If the two readings differ materially or wander, record the behavior rather than forcing an interpretation; in-circuit parallel paths or poor probe contact may require a continuity-trace follow-up.

### C0.4 Planning interpretation only

A reference HKT4056E datasheet for an IC carrying the `4056E` marking identifies pin 2 as `PROG`, states that charge current is set by a resistor from PROG to GND, and gives these reference examples:

| RPROG | Reference programmed current |
|---:|---:|
| 12 kΩ | 100 mA |
| 4 kΩ | 300 mA |
| 2 kΩ | 600 mA |
| 1.5 kΩ | 800 mA |
| 1.2 kΩ | 1000 mA |

This table is **family-reference evidence, not a measured charge-current result for the owned specimen**.

For the selected LG INR18650-MJ1, the eventual programmed current must remain inside the accepted cell charging envelope and must later be verified physically during the controlled charging test. No cell shall be connected based only on this arithmetic.

## Stage C0 PASS / HOLD boundary

**PASS for characterization** means:

- board was unpowered throughout;
- R3 was located without ambiguity;
- two stable resistance readings were recorded and are mutually consistent enough to form a planning hypothesis.

A C0 PASS does **not** qualify the charger, protection stage, cell, current, float voltage or thermal behavior.

**HOLD** if:

- R3 cannot be identified confidently;
- resistance is unstable/unreadable;
- visual damage is present;
- any board/source/cell condition differs from this runbook.

## Next stages after C0

After R3 is characterized and the exact cell is received:

1. received-cell identity/condition and holder-fit inspection;
2. controlled charger input/charge-current/terminal-voltage test;
3. protection/cutoff characterization within safe non-destructive limits;
4. 1S→5 V converter validation;
5. integrated source switchover and backup-endurance testing.

Do not skip directly from C0 to a full integrated battery run.
