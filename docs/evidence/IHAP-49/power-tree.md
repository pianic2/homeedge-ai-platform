# IHAP-49 — Power Tree

**Status:** Accepted PR #34 architecture baseline + Proposed IHAP-56 protection/validation overlay

## Accepted power tree — 2026-09-07 baseline

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
       accepted reverse-insertion control
       - electrical blocking/protection OR
       - mechanically keyed interface/enclosure
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

## Accepted architectural requirements

- USB-C 5 V is the normal/priority source.
- One LG INR18650-MJ1 is retained only as backup.
- Final reference direction is a **single custom core PCB**, not separate charger + boost + mux breakouts.
- Preferred charger/power-path/battery-boost PMIC candidate: `MP2636GR-P`.
- **MP2636 input pass-through is an intermediate node, not the regulated product 5 V rail.**
- A downstream 5 V regulation stage, or explicitly reviewed equivalent topology, is required so valid USB input and battery operation feed the same regulated 5.0 V product bus.
- Product 5 V SYS steady-state validation band: **4.75–5.25 V** unless a downstream part requires tighter limits.
- Minimum product SYS design capability: **>=0.5 A continuous across the accepted battery range and valid USB-input range** and **>=1.0 A transient/headroom**.
- USB reference source: 5 V with at least 1.5 A available/advertised.
- Charging target: 4.2 V CV, ~1.0 A nominal charge current.
- Charging while operating is allowed only through the integrated system power-path implementation and remains subject to physical validation.
- USB-to-battery transfer must be automatic and backfeed into upstream USB is prohibited.
- No-reset source transfer is the reference target and remains `[UNVALIDATED]`.
- Battery-temperature monitoring is required.
- Reverse insertion must be prevented by electrical blocking/protection or a mechanically keyed interface/enclosure; procedure/labels are supplementary only.
- Low-voltage behavior must not intentionally violate the accepted cell boundary.

## Proposed IHAP-56 overlay — pending Project Owner approval

The following details were added after PR #34 and are **Proposed**, not part of the accepted baseline until explicitly approved:

```text
LG INR18650-MJ1
      |
      v
PROPOSED source-side over-current boundary
- must sit ahead of every holder/service conductor
  that RT-R012-01 claims as protected
- any conductor before the interruption element remains
  explicit residual exposure until separately controlled/verified
      |
      v
accepted reverse-insertion control / PMIC BAT path
```

Also Proposed:

- mandatory NTC hot/cold/open/short functional verification;
- numeric thermal PASS/FAIL criteria plus a justified MP2636 junction-temperature/derating method;
- worst-case ILIM <=1.50 A + V14 combined-load verification;
- component-derived 3.3 V steady/transient PASS criteria;
- bidirectional <=100 µs V7 strengthening;
- high/mid/valid-low V8/V9 strengthening, with low BATT margin above cutoff and zero restoration-attributable reset for proposed no-reset effectiveness;
- quantified backfeed criteria for open and attached-unpowered upstream USB conditions;
- numeric 2.70/3.00 V low-voltage policy;
- V15-A/V15-B bounded electrical reverse-blocking verification with USB absent and present;
- ADR-0003/reed-current ownership transfer to IHAP-55.

RT-R012-01 and RT-R013-01 remain Proposed. This diagram must not be used to imply those later controls are already approved, implemented or verified. `ihap-56-closure-matrix.md` is the state router.

## Modular boundary

The custom board integrates stable core power/compute functions while keeping placement-sensitive or serviceable components off-board:

- LD2410C: external module;
- MC-38: field-mounted contact;
- OLED: external/front-panel module;
- DHT11/BME280: replaceable environmental module/profile;
- 18650 holder/cell: mechanically serviceable.

IHAP-50 defines the final connector/signal matrix. IHAP-55 consumes the accepted baseline after the IHAP-56 gate is resolved; Proposed overlay items require explicit approval first. IHAP-51 consumes the final PCB outline and serviceability constraints.
