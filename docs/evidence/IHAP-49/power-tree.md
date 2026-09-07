# IHAP-49 — Accepted Power Tree

**Status:** Accepted architecture contract; custom-board implementation and physical validation delegated to IHAP-55

```text
NORMAL SOURCE
USB-C 5 V
   |
   v
Type-C sink termination + input protection
   |
   v
+---------------------------------------------------------+
| Charger / power-path / battery-boost stage              |
|                                                         |
| Preferred PMIC candidate: MP2636GR-P                    |
| - 1S switch-mode charging                               |
| - system-load priority / power-path management          |
| - input current limiting                                |
| - NTC battery-temperature monitoring                    |
| - battery-to-intermediate-SYS boost                     |
+-----------------------+---------------------------------+
                        ^
                        |
              BATTERY BACKUP PATH
              LG INR18650-MJ1, 1S
                        |
                 serviceable holder
                        |
          cell-side protection boundary
          - over-current interruption REQUIRED
          - reverse blocking OR mechanically keyed
            interface REQUIRED
                        |
                        +-----------------------> PMIC BAT

PMIC output
   |
   v
intermediate SYS / USB-pass-through-or-battery-boost node
   |
   v
5 V post-regulation stage
(buck-boost or reviewed equivalent covering the complete
intermediate range)
   |
   v
regulated 5.0 V PRODUCT SYS
   |
   +--------------------------+-----------------------------+
   |                          |                             |
   v                          v                             v
LD2410C                 regulated 3.3 V              5 V test point
external                      |
module              +---------+-----------+-----------+-----------+
                    |         |           |           |           |
                    v         v           v           v           v
                 ESP32-C3    OLED   DHT11/BME280  reed network  3.3 V TP
```

## Architectural requirements

- USB-C 5 V is the normal/priority source.
- One LG INR18650-MJ1 is retained only as backup.
- The final reference product uses a **single custom core PCB**, not separate charger + boost + mux breakout boards.
- Preferred charger/power-path/battery-boost PMIC candidate: `MP2636GR-P`.
- **MP2636 input pass-through is an intermediate node, not the regulated product 5 V rail.**
- A downstream 5 V regulation stage, or an explicitly reviewed equivalent topology, is mandatory so both valid USB input and battery operation feed the same regulated 5.0 V product bus.
- Product 5 V SYS steady-state validation band: **4.75–5.25 V**, unless a selected downstream part requires tighter limits.
- Minimum product 5 V SYS design capability: **>=0.5 A continuous** and **>=1.0 A transient/headroom**.
- USB reference source: 5 V with at least 1.5 A available/advertised.
- Charging target: 4.2 V CV, ~1.0 A nominal charge current.
- Charging while operating is allowed only through the integrated system power-path implementation and remains subject to physical validation.
- USB-to-battery transfer must be automatic and must prohibit backfeed into the upstream USB source.
- No-reset source transfer is the reference target and remains `[UNVALIDATED]` until IHAP-55 bring-up.
- Battery-temperature monitoring is mandatory and its hot/cold/open/short behavior must be functionally verified.
- Because the MJ1 is unprotected, **cell-side over-current interruption is mandatory upstream of PMIC-output protection coverage**. A holder/BAT-net short must not rely solely on SYS/boost current limiting.
- Reverse insertion must be prevented by electrical blocking/protection or a mechanically keyed interface/enclosure. Procedure/labels are supplementary only.
- Low-voltage cutoff/recovery must keep intentional discharge within the accepted cell boundary.

## Modular boundary

The custom board integrates stable core power/compute functions while keeping placement-sensitive or serviceable components off-board:

- LD2410C: external module;
- MC-38: field-mounted contact;
- OLED: external/front-panel module;
- DHT11/BME280: replaceable environmental module/profile;
- 18650 holder/cell: mechanically serviceable, subject to the protection/keying requirements above.

IHAP-50 defines the final connector/signal matrix. IHAP-55 turns that matrix and this accepted power tree into the schematic/PCB and executes the mandatory validation contract. IHAP-51 consumes the final PCB outline and serviceability constraints.
