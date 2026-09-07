# IHAP-49 — Source Register

## Canonical project sources

- ADR-0001 — MVP edge compute platform: ESP32-C3 reference family; quantitative board power delegated to IHAP-49.
- ADR-0002 — Environmental sensor profiles: DHT11 standard indoor; BME280 precision/extended profile; they are alternatives rather than simultaneous reference loads.
- ADR-0003 — MVP door state sensor: passive wired reed contact; final pull network coordinated with IHAP-50 and quantitative impact with IHAP-49.
- ADR-0004 — Local status display: accepted 0.96-inch-class 128×64 I2C monochrome OLED; exact owned-module current remains unvalidated.
- ADR-0005 — MVP presence sensor: LD2410C-class local boolean presence sensing.
- IHAP-45 evidence: integrated environmental fixture experienced a real brownout/re-enumeration in an initial preflight before staged stability passes; IHAP-49 therefore retains an integrated brownout check.

## Primary component sources used for planning

- Espressif ESP32-C3 Series Datasheet — supply domain and Wi-Fi current envelope.
- Hi-Link HLK-LD2410C official product/manual — 5 V supply, approximately 79 mA operating current and >200 mA source-capability requirement.
- Aosong/ASAIR DHT11 documentation — operating/standby current order of magnitude.
- Bosch BME280 datasheet — microamp-class bare-sensor average current at low-rate environmental sampling.
- Top Power / 4056-family charger documentation — single-cell CC/CV charger behavior; charger IC evidence does not establish complete system power-path/load-sharing behavior.
- LG Chem INR18650-MJ1 product specification — model-level capacity, charge/discharge and operating-envelope evidence used to bound the selected cell candidate.
- NKON LG INR18650-MJ1 listing, EAN/GTIN `8438493099829` — current seller/procurement identity used by the Project Owner; listing states LG model INR18650-MJ1, 18650 flat-top unprotected Li-ion, 3.6 V nominal, 3500 mAh typical / 3400 mAh minimum, 10 A discharge capability, approximately 18.2 mm diameter × 65 mm height.

## Procurement evidence boundary

The Project Owner selected a planned NKON order of 10 × LG INR18650-MJ1 at EUR 19.90 product subtotal plus EUR 6.33 shipping, planned total EUR 26.23. These values are owner-provided order-decision evidence. Purchase completion and received-lot conformance remain pending until explicitly confirmed and inspected.

## Evidence-quality rule

Primary manufacturer documentation defines component-level constraints. Seller evidence establishes the selected listing/procurement identity but does not replace inspection of the received cells. Neither source replaces measurement of the owned SuperMini-compatible board, OLED breakout, generic charger/protection module, complete 5 V distribution or final battery-backup path.
