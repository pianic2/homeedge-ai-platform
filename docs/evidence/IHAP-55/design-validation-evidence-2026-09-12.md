# IHAP-55 — Design and simulation evidence — 2026-09-12

## Manufacturer-derived schematic values

### MP2636GR-P

Source: MPS MP2636 datasheet Rev.1.02.

- Manufacturer equation: `ICHG = 2400 / (RISET[kOhm] * RS1[mOhm])`.
- Candidate `RS1=20 mOhm`, `RISET=120 kOhm` -> nominal `ICHG=1.0 A`.
- boost/system output is programmable 4.2..6 V; candidate battery-mode MP_SYS is 5.184 V using 33.2 kOhm / 10 kOhm around the published 1.2 V feedback reference.
- MP2636 SYS requires at least 22 uF close to SYS and the datasheet states total SYS capacitance must not be below 44 uF.
- this does not turn the valid-input pass-through node into regulated product 5 V.

### TPS63802DLAR

Source: TI TPS63802 datasheet Rev.D and TI model package.

- 1.3..5.5 V input; adjustable output up to 5.2 V.
- 0.47 uH reference inductor class.
- 10 uF input capacitor recommendation.
- for VOUT >3.6 V, 2x22 uF output capacitors are recommended.
- feedback reference 0.5 V; low-side feedback resistor <=100 kOhm.
- candidate 900 kOhm / 100 kOhm -> 5.000 V nominal.
- TI publishes an unencrypted PSpice transient package `SLVMCX1C.ZIP`.

### TLV62568DBVR

Source: TI TLV62568 datasheet Rev.B and TI model package.

- 2.5..5.5 V input, 1 A buck.
- standard recommended network for VOUT >=1.8 V includes 2.2 uH + 22 uF.
- feedback formula uses 0.6 V nominal; R2 <=200 kOhm.
- 6.8 pF feed-forward capacitor recommended when R2=100 kOhm.
- candidate 453 kOhm / 100 kOhm -> 3.318 V nominal.
- published feedback range 0.588..0.612 V; with 0.1% resistors divider-only corner is approximately 3.246..3.390 V.
- TI publishes unencrypted PSpice transient package `SLVMBV4B.ZIP`.

### TLA2024IRUGT board-health ADC

Source: TI TLA2024 datasheet.

- Active 12-bit, four-channel delta-sigma ADC with I2C, internal reference/oscillator/PGA.
- 2..5.5 V supply; ~150 uA typical operating current stated by TI.
- ADDR=GND selects I2C address `0x48`.
- selected solely for programmatic board-health telemetry; it does not supersede external calibrated measurements.

## Executed software gate

Executed locally against the revision-A contract before repository publication:

- `ihap55_contract_check.py`: PASS;
- deterministic USB/battery/load sweep: 28/28 PASS;
- unit tests: 8/8 PASS.

These are design-screen results, not physical evidence.

## Required next evidence

- vendor switching simulation for TPS63802 and TLV62568;
- MP2636 exact-model MPSmart run if available;
- exact VBUS protection / reverse-cell / NTC freeze;
- real module pull-up characterization;
- KiCad ERC then PCB DRC/DFM;
- fabricated-board USB self-test plus accepted V1..V12 bench plan.

## 2026-09-13 unfrozen remediation candidates

### TLA2024 supply-off isolation

TI's TMUX1511 is a candidate for the four divided rail paths: its data sheet specifies powered-off high-Z isolation for signal-path voltages up to 3.6 V and fail-safe SEL inputs. The existing worst-case divided input is 2.625 V, below that signal-path ceiling, and the ADC input current is far below the switch's 25 mA channel rating. Candidate mapping is `Sx=rail divider`, `Dx=TLA2024 AINx`, `VDD=SYS_3V3`.

The enable cannot be treated as solved by tying SEL directly to `SYS_3V3`: the switch can turn on while the ADC supply is still near its lower operating range, leaving the ADC's `VDD+0.3 V` absolute input limit to be checked during ramp/down. A candidate gate is TI `TPS3839K33DBZR` (2.93 V nominal reset threshold, active-low push-pull RESET output used as SEL); it holds SEL low until `SYS_3V3` is above the threshold and asserts low again on undervoltage. Threshold tolerance, TMUX timing, ADC clamp current and the 120–350 ms supervisor release delay still require corner analysis. This is not a captured or validated circuit.

### MP2636 candidate population

Using the MPS Rev.1.02 equations, the following values are electrically reproducible candidates: `RISET=120 kOhm` with `RS1=20 mOhm` for 1.0 A nominal charge; `RILIM=30.1 kOhm` for approximately 1.389 A nominal input limit (`43.3/R - 0.05`), retaining nominal source margin. `RILIM=28.0 kOhm` gives approximately 1.50 A only nominally and is sensitivity analysis, not a freeze, because resistor and IC tolerance can exceed the 1.5 A USB-C source advertisement. `PWIN RH=91 kOhm/RL=20 kOhm` gives 0.811 V at the 4.5 V input corner; `REG R3=15 kOhm/R4=5.1 kOhm` is approximately a 4.75 V input-regulation target. `ROLIM=220.8 kOhm` gives only 0.5 A nominal boost output and is rejected against the product contract; `110.4 kOhm` (1.0 A nominal) or `90.3 kOhm` (1.223 A by equation; roughly 1.25 A in the MPS table) require tolerance/thermal/transient verification before selection. The MPS example NCP18XH103 plus `RT1=6.65 kOhm` and `RT2=25.5 kOhm` covers 0–50 °C, but the owned LG cell/holder has no verified thermistor, so this cannot yet be frozen as the battery NTC implementation.

The TMUX/supervisor gate is `[UNVALIDATED]` for the ADC supply transient: TPS3839 specifies 20 µs typical falling propagation, **not a guaranteed maximum**. With a 24 µs sensitivity interval and the candidate 22 µF nominal `SYS_3V3` output capacitor, `ΔV = I·t/C = 0.5 A·24 µs/22 µF ≈ 0.545 V`. The ADC input safety margin at the 2.857 V minimum supervisor threshold is only `2.857 − 2.325 = 0.532 V` for a 2.625 V divided input, so even ideal-capacitor droop exceeds that margin. Effective capacitance after DC-bias derating, ESR, converter response and additional capacitance have not been bounded. This is not a supply-off safety proof.

### Reverse-cell disposition

TI `LM66100` is **rejected as a battery-path candidate**: although its data sheet specifies reverse-polarity protection and reverse-current blocking, it is a single-input/single-output ideal diode and cannot be assumed to pass both the MP2636 charge direction and battery-discharge direction in this topology. It must not be placed in series with `BATT` without a demonstrated bidirectional arrangement.

The minimally defensible reverse-cell options remain (a) a mechanically keyed battery connector/holder that physically prevents reverse insertion, with the exact connector and contact arrangement frozen and inspected, or (b) a bidirectional back-to-back-FET protection stage with a controller whose charge/discharge current paths and fault behavior are explicitly verified. The present non-keyed holder is not closed by labels or procedure, and no electrical option is yet selected.
