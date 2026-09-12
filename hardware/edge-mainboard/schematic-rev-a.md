# IHAP-55 — Mainboard schematic revision A

**Date:** 2026-09-12  
**State:** engineering schematic contract — not fabrication-frozen  
**Machine-readable companion:** `schematic-contract.json`

Values marked `TBD` or `[UNVALIDATED]` must not be silently replaced during KiCad capture.

## A — USB-C and native USB

- `J1 = USB4105-GF-A`; VBUS pins -> `VBUS_IN`.
- CC1 -> 5.1 kOhm 1% -> GND; CC2 -> 5.1 kOhm 1% -> GND.
- D-/D+ -> `USBLC6-2SC6` -> optional 22/33 Ohm series footprints -> ESP32-C3 GPIO18/GPIO19.
- `VBUS_IN` -> input protection `[TBD exact MPN]` -> MP2636 IN.
- 5 V Type-C sink only; no PD.

## B — MP2636 charger / power path / battery

`U3 = MP2636GR-P`.

Candidate values derived from manufacturer equations:

- `RS1=20 mOhm`, `RISET=120 kOhm` -> nominal 1.0 A charge target;
- VB HIGH -> 4.2 V cell charge target;
- battery-mode boost feedback: 33.2 kOhm / 10.0 kOhm with 1.2 V reference -> `MP_SYS=5.184 V` nominal;
- SYS capacitance design target >=44 uF effective; VCC bypass 100 nF;
- NTC path present, exact thermistor/divider `[UNVALIDATED]`;
- input-current-limit population remains open until Accepted/Proposed boundary resolution;
- TP BATT and MP_SYS.

MP2636 pass-through is never called product `SYS_5V`.

## C — regulated 5 V

`U4 = TPS63802DLAR`: VIN=MP_SYS, VOUT=SYS_5V.

- L=0.47 uH, saturation-current class >= manufacturer 5.4 A reference class;
- CIN=10 uF; COUT=2x22 uF for VOUT >3.6 V;
- feedback 900 kOhm / 100 kOhm, 0.1%; nominal 5.000 V;
- FB ±1% + resistor ±0.1% divider-only corner: approximately 4.941..5.059 V before line/load/transient effects;
- TP SYS_5V.

## D — regulated 3.3 V

`U5 = TLV62568DBVR`: VIN=SYS_5V, VOUT=SYS_3V3.

- L=2.2 uH, CIN=4.7 uF, COUT=22 uF;
- feedback 453 kOhm / 100 kOhm, 0.1%; feed-forward 6.8 pF;
- nominal 3.318 V;
- published FB 0.588..0.612 V + resistor ±0.1% divider-only corner: approximately 3.246..3.390 V;
- TP SYS_3V3.

## E — ESP32-C3 and service

`U1 = ESP32-C3-MINI-1-N4X`.

- GPIO18 USB D-, GPIO19 USB D+; EN reset network; GPIO9 BOOT only;
- GPIO20/21 recovery/service pads where practical;
- GPIO0 radar RX; GPIO1 radar service TX reservation disabled by firmware default;
- GPIO3 door; GPIO4 DHT; GPIO5 ADC spare; GPIO6 SDA; GPIO7 SCL; GPIO10 spare digital;
- GPIO2/8/9 never application GPIO.

## F — external interfaces

- `J_RADAR`: GND, SYS_5V, RADAR_RX, RADAR_SERVICE_TX.
- `J_OLED`: GND, SYS_3V3, SCL, SDA.
- `J_ENV`: GND, SYS_3V3, DHT_DATA, SCL, SDA.
- `J_DOOR`: GND, DOOR_SENSE.
- `J_BATT`: BATT+, GND; reverse-cell prevention remains mandatory open design work.

Door network: 10 kOhm pull-up + 1 kOhm series + optional 100 nF DNP. I2C/DHT board pull-up footprints stay DNP until real modules are measured.

## G — programmatic board health

`U6 = TLA2024IRUGT`, supplied by SYS_3V3, ADDR=GND -> I2C `0x48`.

Four 47 kOhm / 47 kOhm 1:2 monitor dividers:

- AIN0 VBUS_IN;
- AIN1 BATT;
- AIN2 SYS_5V;
- AIN3 SYS_3V3.

Firmware reports these rails over native USB during `self_test`. This is diagnostic evidence, not a replacement for calibrated DMM/oscilloscope tests.

## Required pre-layout gates

1. freeze exact VBUS protection and reverse-cell prevention;
2. finish NTC/input-current-limit implementation;
3. measure OLED/BME280/DHT11 pull-ups;
4. run deterministic corner simulation and vendor-model simulations;
5. capture contract into KiCad and run ERC;
6. freeze preliminary board envelope and hand it to IHAP-51 before final layout freeze.
