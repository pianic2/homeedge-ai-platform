# IHAP-55 revision-A power calculations — 2026-09-12

Reproduce with `python3 tools/hardware-validation/ihap-55-mainboard/host/ihap55_power_math.py` (exit 0 on 2026-09-12). These are **static calculations**, not regulator qualification. Primary sources: [MPS MP2636 Rev.1.02](https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/Datasheet/lang/EN/sku/MP2636/document_id/1443/), [TI TPS63802 Rev.D](https://www.ti.com/lit/ds/symlink/tps63802.pdf), [TI TLV62568 Rev.B](https://www.ti.com/lit/ds/symlink/tlv62568.pdf), [TI TLA2024 SBAS846](https://www.ti.com/lit/ds/symlink/tla2024.pdf), [NXP I2C UM10204](https://www.nxp.com/docs/en/user-guide/UM10204.pdf), [Espressif ESP32-C3 layout guidance](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c3/pcb-layout-design.html).

## Verified arithmetic

| Network | Equation and candidate | Static result | Limit of claim |
|---|---|---:|---|
| MP2636 charge | `2400/(120 kΩ × 20 mΩ)` | 1.000 A nominal | sense/ISET tolerance and charge thermal foldback pending |
| MP2636 battery boost | `1.2 × (1+33.2/10)` | 5.184 V nominal MP_SYS | valid-input MP_SYS remains pass-through, not regulated 5 V |
| MP2636 input limit candidate | `43.3/30.1−0.05` | 1.389 A nominal | candidate resistor only; limit tolerance and source budget pending |
| TPS63802 feedback | `0.5 × (1+900/100)` | 5.000 V nominal | FB ±1%, resistors ±0.1% => 4.941–5.059 V feedback-only; dynamic/line/load excluded |
| TLV62568 feedback | `0.6 × (1+453/100)` | 3.318 V nominal | FB 0.588–0.612 V, resistors ±0.1% => 3.246–3.390 V feedback-only |
| TLA2024 divider | `47/(47+47)` | 0.5 nominal | at ±4.096 V FSR, 6 MΩ typical input impedance loads it to 0.49805 (−0.390%); rail LSB 4 mV |
| I2C rise time example | `0.8473 × Rp × 200 pF` | 0.796 µs at 4.7 kΩ; 1.695 µs at 10 kΩ | 200 pF assumed, modules/cables unmeasured; Standard-mode 1 µs maximum must be checked |
| DHT parallel pull-ups example | `4.7 kΩ || 5.1 kΩ` | 2.446 kΩ | board resistor stays DNP until owned module is measured |

TPS63802 reference passives are 0.47 µH, 10 µF input and two 22 µF output for 5 V; TI lists 5.4 A rated Coilcraft `XFL4015-471ME` in its characterization circuit. TLV62568 candidate passives are 2.2 µH, 4.7 µF input, 22 µF output and 6.8 pF feed-forward. Exact capacitor effective capacitance at DC bias, inductor Isat/Irms, PCB copper heat spreading, current limit at minimum Vin, startup and load-step margins are **not yet proven**. At 0.5 A, SYS_5V supplies 2.5 W; if efficiency were 90%, converter loss would be 0.278 W. That efficiency is a sensitivity assumption, not a guaranteed thermal result. The same assumption at 3.3 V/0.5 A gives 0.183 W TLV loss.

## Design issue requiring remediation before schematic freeze

At 5.25 V VBUS, a 47 kΩ/47 kΩ divider presents 2.625 V to AIN0. TLA2024 recommended analog input is GND..VDD and absolute maximum is VDD+0.3 V. With SYS_3V3 unpowered during startup/fault/partial supply, the direct divider violates this bound. The same analysis applies to any monitored rail remaining live while the ADC supply is down. **FAIL — current passive divider topology is not approved for capture without supply sequencing or input isolation.** A validated switched divider / protection implementation must be selected and checked for measurement error. The nominal 47 kΩ ratio and firmware scaling may then need updating.

MP2636 NTC requires a real cell thermistor and divider calculated from the actual thermistor curve. The MPS example `NCP18XH103` with RT1 6.65 kΩ and RT2 25.5 kΩ covers its example 0–50 °C window; it is not evidence that the owned LG cell/holder has this NTC. The published 10 kΩ/10 kΩ no-NTC bypass is **not** acceptable under ADR-0007's battery-temperature requirement. Reverse-cell electrical/mechanical prevention, VBUS protection, MP2636 PWIN/REG/OLIM population, SYS capacitor effective ≥44 µF, thermal and low-battery behavior remain unresolved.

The 1.389 A input-limit candidate leaves less than the nominal 1.5 A reference source advertisement. USB-C Rp advertising must be respected; board input loading cannot be inferred from connector current rating. MP2636 prioritizes system load over charging, but charge reduction at simultaneous 5 V load and 1 A charge target is not yet quantitatively established. No current number here qualifies the accepted ≥0.5 A continuous or ≥1.0 A transient rail target.

USB-C 5 V sink candidate uses one 5.1 kΩ Rd on each of CC1 and CC2; 5.1 kΩ at 1% spans 5.049–5.151 kΩ. The [USB Type-C specification](https://www.usb.org/sites/default/files/USB%20Type-C%20Spec%20R2.0%20-%20August%202019.pdf) requires Rd on both CC pins and source-current advertisement recognition. The Accepted reference is a source advertising at least 1.5 A, but the board has no frozen CC-current detection/limiting circuit yet. USBLC6-2SC6 covers the data lines only; VBUS fuse/TVS and polarity/backfeed implementation remain open. D+/D− series value and the exact USB4105-GF-A pad/pin mapping must be checked against the manufacturer drawing before capture.
