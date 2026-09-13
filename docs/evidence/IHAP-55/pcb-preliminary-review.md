# IHAP-55 preliminary PCB review — 2026-09-13

**HOLD — no native PCB file or DRC.** The preliminary mechanical envelope is not yet a safe IHAP-51 handoff because source schematic/ERC and power/protection footprints are absent. Do not infer board dimensions or mounting holes from the architecture sketch.

The eventual IHAP-51 input must include a real board outline, candidate holes, exact USB-C/JST connector coordinates, battery/service zones, BOOT/RESET/test-point access and ESP32-C3-MINI-1 antenna-at-edge keepout. [Espressif layout guidance](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c3/pcb-layout-design.html) recommends the antenna outside the base-board edge where practical and at least 15 mm clearance in the final housing; no copper, parts or routes may invade the applicable antenna keepout. Final placement/layout freeze follows IHAP-51 feedback.

`drc-report.txt` explicitly records the unexecuted DRC gate. No fabrication preview or manufacturing output exists.
