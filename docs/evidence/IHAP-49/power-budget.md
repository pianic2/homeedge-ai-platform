# IHAP-49 — Planning Power and Backup Autonomy Budget

**Status:** planning model; measurements pending

## Reference load boundary

The reference node load considered by IHAP-49 is:

- ESP32-C3 SuperMini-compatible reference compute board;
- HLK-LD2410C-class presence sensor;
- DHT11 for the standard-indoor profile **or** BME280 for the precision/extended profile, not both as simultaneous reference loads;
- accepted 0.96-inch-class 128×64 monochrome I2C OLED;
- passive reed-contact input network;
- no microphone/audio load in the reference MVP.

## Source data and assumptions

| Load | Voltage domain | Planning current/power | Status / basis |
|---|---:|---:|---|
| LD2410C | 5 V | ~79 mA average = ~0.395 W | Manufacturer-documented typical/average figure. Source-capability requirement >200 mA is not treated as average consumption. |
| ESP32-C3 + owned SuperMini-compatible board | board 5 V input / internal 3.3 V | central assumption ~175 mW input-equivalent | Engineering assumption for planning only. ESP32-C3 chip current varies strongly with Wi-Fi/runtime; board regulator and exact node-average current remain `[UNVALIDATED]`. |
| OLED 0.96-inch-class 128×64 | 3.3 V reference fixture | central assumption ~50 mW | Exact owned-module current remains `[UNVALIDATED]`; estimate represents a modest text/status workload, not full-white worst case. |
| DHT11 | 3.3 V reference fixture | negligible at node scale; ~0.1 mA average planning assumption | Manufacturer standby/measurement figures are sub-mA to ~1 mA class. Exact owned breakout current `[UNVALIDATED]`. |
| BME280 alternative | 3.3 V reference fixture | negligible at node scale | Bare IC is microamp-class at low-rate environmental sampling. Exact owned breakout current `[UNVALIDATED]`. |
| Reed contact + pull network | 3.3 V | negligible to small; depends on final pull strategy | Passive contact. Internal pull-up was functionally stable in IHAP-47; final network belongs to IHAP-50. |
| Miscellaneous/board/protection allowance | mixed | small planning allowance | Not a measured line item. |

## Central planning estimate

A useful central planning point is approximately:

- **5 V-equivalent integrated load:** ~125 mA;
- **5 V load power:** ~0.625 W;
- assumed battery-path DC/DC efficiency: 90%;
- estimated battery-side power during backup: ~0.694 W.

This is not a measured node power figure.

## 3.5 Ah-class 1S cell planning example

For a nominal 3.5 Ah, 3.6 V Li-ion cell:

- nominal energy = 3.5 Ah × 3.6 V = **12.6 Wh**;
- conservative planning-use factor = 90%;
- planning usable energy = **11.34 Wh**;
- estimated central-runtime = 11.34 Wh / 0.694 W = **~16.3 h**.

Before physical measurement, a planning range of approximately **12–20 h** is reasonable for a 3.5 Ah-class cell depending on actual Wi-Fi duty cycle, OLED content, converter efficiency, usable cell energy and cutoff behavior.

## Architectural interpretation

The battery is not selected to support multi-day standalone operation. The Project Owner has decided that normal operation is from regulated 5 V USB-C and that the battery exists only as backup for blackout or cable/input interruption.

The LD2410C dominates the continuous load. At ~79 mA from 5 V it consumes ~0.395 W before converter loss. Therefore optimizing DHT11 versus BME280 has negligible influence on backup endurance, while ESP32-C3 duty cycle, OLED policy and converter efficiency have materially larger influence.

## Validation boundary

No number in this file is an accepted autonomy claim. Acceptance requires an exact cell and power-path implementation plus an integrated current measurement and controlled backup discharge test. Until then:

**backup autonomy = `[UNVALIDATED]`**.
