# IHAP-49 — Source Register

## Canonical project sources

- ADR-0001 — MVP edge compute platform: ESP32-C3 reference family; quantitative board power delegated to IHAP-49/IHAP-55.
- ADR-0002 — Environmental sensor profiles: DHT11 standard indoor; BME280 precision/extended profile; alternatives rather than simultaneous reference loads.
- ADR-0003 — MVP door state sensor: passive wired reed contact; final pull network coordinated with IHAP-50.
- ADR-0004 — Local status display: accepted 0.96-inch-class 128×64 I2C monochrome OLED.
- ADR-0005 — MVP presence sensor: LD2410C-class local boolean presence sensing.
- ADR-0006 — MVP central-node hardware profile.
- ADR-0007 — Edge power subsystem: accepted 2026-09-07; normal regulated 5 V USB-C source, LG INR18650-MJ1 backup-only cell, custom modular PCB direction with MP2636GR-P as preferred first integrated PMIC.

## Primary component sources used for planning / design contract

- Espressif ESP32-C3 Series Datasheet — supply domain and Wi-Fi current envelope.
- Hi-Link HLK-LD2410C official product/manual — 5 V supply, approximately 79 mA operating current and >200 mA source-capability requirement.
- Aosong/ASAIR DHT11 documentation — operating/standby current order of magnitude.
- Bosch BME280 datasheet — microamp-class bare-sensor average current at low-rate environmental sampling.
- LG Chem INR18650-MJ1 product specification — model-level capacity, charge/discharge and operating-envelope evidence.
- NKON LG INR18650-MJ1 listing, EAN/GTIN `8438493099829` — selected procurement identity; seller evidence records 3.6 V nominal, 3500 mAh typical / 3400 mAh minimum, 10 A discharge capability and approximately 18.2 mm × 65 mm dimensions.
- MPS MP2636 product documentation — integrated 1S charger, system power-path, reverse boost, NTC and programmable SYS/charge behavior supporting the first custom-board direction.
- ETA9740 manufacturer documentation — retained as future cost-down alternative only.
- 4056-family charger documentation — used only to bound the already-owned charger module; the owned 4056E module is not the final reference implementation.

## Procurement evidence boundary

The Project Owner selected a planned NKON order of 10 × LG INR18650-MJ1 at EUR 19.90 product subtotal plus EUR 6.33 shipping, planned total EUR 26.23. Purchase completion and received-lot conformance remain pending until explicitly confirmed and inspected.

No TPS61023, TPS2116 or additional charger/boost/mux breakout purchase is required solely to emulate the final custom PCB architecture.

## Evidence-quality rule

Primary manufacturer documentation defines component-level constraints. Seller evidence establishes listing/procurement identity but does not replace inspection of received cells. Physical custom-board charging, rail, thermal, transfer and endurance claims remain `[UNVALIDATED]` until IHAP-55 tests the fabricated implementation.
