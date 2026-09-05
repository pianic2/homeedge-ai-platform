# IHAP-49 — Proposed Power Tree

**Status:** Proposed; exact components and transfer implementation pending

```text
Normal source
regulated 5 V USB-C
        |
        +------------------------------+
        |                              |
        |                              v
        |                         source-selection /
        |                         isolation stage
        |                              |
        |                              v
        |                       regulated 5 V node bus
        |                              |
        |                 +------------+-------------+
        |                 |                          |
        |                 v                          v
        |             LD2410C                  ESP32-C3 board
        |               5 V                       5 V input
        |                                             |
        |                                             v
        |                                      onboard 3.3 V
        |                                             |
        |                                +------------+-------------+
        |                                |            |             |
        |                                v            v             v
        |                           DHT11/BME280     OLED      reed network
        |
        +--> charging input to 4056E-family charger/protection board
                                      |
                                      +--> B+/B- --> 1S Li-ion cell
                                      |
                                      +--> OUT+/OUT-
                                              |
                                              v
                                       1S -> regulated 5 V
                                           converter
                                              |
                                              +------> source-selection /
                                                      isolation stage
```

## Architectural requirements

- The normal source is regulated 5 V USB-C.
- The battery path is backup only.
- The battery path must be converted to a regulated 5 V node domain because the accepted LD2410C reference uses 5 V.
- The final source-selection/isolation stage must prevent prohibited backfeed between the normal 5 V source and backup path.
- A generic 4056E/TP4056-family charger module is not treated as a complete load-sharing or UPS controller.
- Until an explicit power-path implementation is selected and validated, charging while operating from the battery path is prohibited.
- The final physical wiring/connectors remain coordinated with IHAP-50.
- Battery accessibility, retention, reverse-insertion mitigation and thermal spacing remain coordinated with IHAP-51.

## Transfer behavior

Whether loss of the normal source must be electrically seamless or may cause one controlled node reboot is not yet accepted. The selected source-selection implementation and downstream runtime/event-integrity constraints must decide this before final ADR acceptance.
