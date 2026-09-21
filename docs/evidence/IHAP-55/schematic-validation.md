# IHAP-55 schematic validation — 2026-09-21

**NATIVE LOAD: PASS.** KiCad 10.0.6 successfully exported a netlist from `hardware/edge-mainboard/homeedge-edge-mainboard.kicad_sch`.

**ERC: NOT PASS.** KiCad executed ERC with `--severity-all --exit-code-violations`; result: 0 errors and 1 warning (`multiple_net_names`, `GND` and `USB_D_MINUS` reported on one generic USB connector item). The exact report is `erc-report.txt`; no exclusion was added.

The native schematic now contains the revision-A interface contract, USB-C sink pins and Rd resistors, ESP32-C3 contract pin map, peripheral/battery connectors, power-stage block marked `UNVALIDATED`, mounting candidates, and service/test access points. It does not claim a frozen power/protection implementation. TLA2024 supply-off isolation, MP2636 protection/NTC/input-limit, reverse-cell prevention, exact VBUS protection, converter passives, and exact module symbol/land mapping remain open.

The generic Connector_Generic symbol used for the ESP32 contract block is an interim native capture aid, not a fabrication-ready ESP32-C3-MINI-1 symbol. No fabrication or final schematic-freeze claim follows.
