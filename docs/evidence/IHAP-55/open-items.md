# IHAP-55 open technical items — 2026-09-12

All below remain inside IHAP-55 / PR #37. `RT-R012-01` and `RT-R013-01` remain Proposed/Pending Evidence; none is promoted by this list.

| Priority | Item | Evidence / next resolution |
|---|---|---|
| Blocker to schematic freeze | TLA2024 direct divider can violate AIN ≤ VDD+0.3 V while SYS_3V3 is off | `power-calculations.md`; design and verify supply-off-safe isolation and update ADC scaling |
| Blocker to power-stage freeze | MP2636 PWIN, REG, ILIM, OLIM, MODE, NTC, input and SYS effective capacitors, inductor and thermal margin not fully frozen | Manufacturer Rev.1.02 equations; calculate with exact protection/thermistor/inductor MPNs |
| Blocker to battery implementation | Accepted reverse-cell prevention and cell-temperature sensing not implemented | ADR-0007; select and verify electrical or mechanical prevention and real NTC path |
| Blocker to input implementation | USB VBUS fuse/TVS/protection MPN, connector pad mapping and no-backfeed path not frozen | USB-C/MP2636 datasheet and source-transfer analysis |
| Blocker to regulator qualification | TI PSpice models produced nonphysical ngspice outputs; 0.5 A continuous and 1 A transient/thermal/efficiency not shown | `simulation-summary.md`; validate wrappers in supported simulator or correct compatibility with plausible waveforms |
| Blocker to EDA gate | Native schematic/PCB now load, but ERC and schematic-parity/footprint mapping are not clean | KiCad 10.0.6 native schematic load PASS; ERC executed with 0 errors and 1 warning. PCB native load PASS; DRC executed with 0 geometric violations and 84 parity/footprint findings. Generic ESP32 contract symbol and preliminary placement footprints remain non-fabrication mapping aids. No false ERC/DRC PASS. |
| Physical characterization | OLED/BME280/DHT11 module pull-ups, cabling capacitance and effective I2C/DHT pull-up | Measure owned modules before populating board resistors; DNP footprints retained |
| Mechanical interlock | Preliminary envelope/holes/connectors/antenna keepout then IHAP-51 review before final layout freeze | No preliminary PCB gate yet; Espressif antenna guidance applies |
| Production detail | Exact passive/protection MPNs, DC-bias/Isat/Irms and DFM/assembly review | No BOM/fabrication release until complete |
| Physical validation | `IHAP55-BOARD-01`, calibrated V1–V12, USB/battery transfer, load, RF and thermal tests | Requires authorized fabricated board; all `[UNVALIDATED]` now |

Project Owner decisions are **not requested yet**: technical prerequisites are incomplete. Later gates remain core/module partition review as documented, IHAP-51 feedback, procurement/fabrication authorization, any Accepted-decision change or formal risk acceptance, and final reference-implementation declaration.
