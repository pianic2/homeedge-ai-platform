# IHAP-55 preliminary PCB review — 2026-09-21

**PCB NATIVE LOAD: PASS.** KiCad `pcb render` successfully parsed `hardware/edge-mainboard/homeedge-edge-mainboard.kicad_pcb` and produced `/tmp/ihap55-pcb.png`.

The native preliminary baseline contains a 100×70 mm candidate outline, four mounting-hole candidates, USB-C edge placement, ESP32 placement with antenna-edge/15 mm enclosure-clearance annotation, power-stage placement, peripheral/service edge zone, and preliminary service access marking. It is not a final placement/layout freeze or fabrication release.

**DRC: NOT PASS.** KiCad DRC executed with `--severity-all --exit-code-violations --schematic-parity`: 0 geometric violations, 0 unconnected pads, and 84 schematic-parity/footprint mapping findings. The findings are real: bootstrap placement footprints lack final pads/connector footprint mapping and the schematic contains contract/testpoint symbols not yet represented as final PCB footprints. Exact output is `drc-report.txt`.
