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

## Evidence-quality rule

Primary manufacturer documentation defines component-level constraints. It does not replace measurement of the owned SuperMini-compatible board, OLED breakout, generic charger/protection module, complete 5 V distribution or final battery-backup path.
