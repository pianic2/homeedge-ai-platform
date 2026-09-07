# IHAP-49 — Proposed Power Tree

**Status:** Proposed architecture contract; custom-board implementation delegated to IHAP-55

```text
NORMAL SOURCE
USB-C 5 V
   |
   v
Type-C sink termination + input protection
   |
   v
+------------------------------------------------+
| Integrated custom-board power subsystem        |
|                                                |
|  1S switch-mode charger                        |
|  + system power-path management                |
|  + input current limiting                      |
|  + battery-temperature monitoring              |
|  + battery-to-SYS boost                        |
|                                                |
|  Preferred first implementation: MP2636GR-P    |
+------------------+-----------------------------+
                   |                    |
                   |                    +----> LG INR18650-MJ1
                   |                              1S backup cell
                   |                              in serviceable holder
                   v
             regulated 5 V SYS
                   |
          +--------+--------------------+
          |                             |
          v                             v
      LD2410C                    regulated 3.3 V
      external                         |
      module                  +--------+---------+----------+
                              |        |         |          |
                              v        v         v          v
                           ESP32-C3   OLED   DHT11/BME280  reed network
```

## Architectural requirements

- USB-C 5 V is the normal/priority source.
- One LG INR18650-MJ1 is retained only as backup.
- The final reference product uses a **single custom core PCB**, not separate charger + boost + mux breakout boards.
- Preferred first integrated PMIC direction: `MP2636GR-P`.
- Boost-mode SYS target: 5.0 V.
- Minimum 5 V SYS design capability: >=0.5 A continuous, >=1.0 A transient/headroom target.
- USB reference source: 5 V with at least 1.5 A available/advertised.
- Charging target: 4.2 V CV, ~1.0 A nominal charge current.
- Charging while operating is allowed only through the integrated system power-path implementation and remains subject to physical validation.
- USB-to-battery transfer must be automatic and must prohibit backfeed into the upstream USB source.
- No-reset source transfer is the reference target and remains `[UNVALIDATED]` until IHAP-55 bring-up.
- Battery-temperature monitoring is required in the integrated board.
- The unprotected cell requires system-level low-voltage/over-current/reverse-insertion treatment.

## Modular boundary

The custom board should integrate stable core functions while keeping placement-sensitive or serviceable components off-board:

- LD2410C: external module;
- MC-38: field-mounted contact;
- OLED: external/front-panel module;
- DHT11/BME280: replaceable environmental module/profile;
- 18650 holder/cell: mechanically serviceable.

IHAP-50 defines the final connector/signal matrix. IHAP-55 turns that matrix and this power tree into the schematic/PCB. IHAP-51 consumes the final PCB outline and serviceability constraints.
