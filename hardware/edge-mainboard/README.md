# HomeEdge Edge Mainboard — IHAP-55

**EDA baseline:** KiCad 10.0.6 stable  
**Status:** initialized; schematic source not yet frozen

This directory is the canonical PCB source workspace for IHAP-55.

Planned source set:

```text
hardware/edge-mainboard/
  homeedge-edge-mainboard.kicad_pro
  homeedge-edge-mainboard.kicad_sch
  homeedge-edge-mainboard.kicad_pcb
  libraries/
  fabrication/        # generated only after DRC/DFM and Project Owner fabrication gate
```

## Current design gates

The workspace is intentionally initialized **before** creating a schematic that would silently freeze unreviewed component values.

Current architecture candidate is documented in:

- `docs/architecture/ihap-55-mainboard-architecture.md`
- `docs/evidence/IHAP-55/source-register.md`

Before first schematic freeze:

1. complete MP2636 + post-regulator electrical calculations;
2. complete 3.3 V regulator calculations;
3. freeze USB-C CC/data/protection implementation;
4. verify ESP32-C3-MINI-1-N4X pin availability against the Accepted IHAP-50 map;
5. measure/identify actual module-side I2C/DHT pull-ups;
6. separate Accepted power requirements from Proposed IHAP-56 controls;
7. retain all exact MPN and footprint evidence in the IHAP-55 source register.

## Governance

- one task = one branch = one PR;
- branch: `ihap-55-integrated-modular-edge-pcb`;
- no fabrication/procurement without explicit Project Owner authorization;
- generated Gerber/drill/fabrication files are not evidence of physical correctness;
- final board behavior remains `[UNVALIDATED]` until bring-up and physical validation;
- no audio circuitry, connector or allocation is permitted in the reference MVP.