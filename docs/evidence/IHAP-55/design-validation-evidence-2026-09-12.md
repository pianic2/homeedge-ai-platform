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
