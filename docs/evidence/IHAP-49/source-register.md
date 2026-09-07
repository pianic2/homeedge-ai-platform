# IHAP-49 — Source Register

## Canonical project sources

- ADR-0001 — MVP edge compute platform: ESP32-C3 reference family; quantitative final-board power work is explicitly transferred by ADR-0007 to IHAP-55.
- ADR-0002 — Environmental sensor profiles: DHT11 standard indoor; BME280 precision/extended profile; alternatives rather than simultaneous reference loads. Quantitative final-board current work is transferred by ADR-0007 to IHAP-55.
- ADR-0003 — MVP door state sensor: passive wired reed contact; final pull network coordinated with IHAP-50.
- ADR-0004 — Local status display: accepted 0.96-inch-class 128×64 I2C monochrome OLED; display-current/sleep-policy measurement is transferred by ADR-0007 to IHAP-55.
- ADR-0005 — MVP presence sensor: LD2410C-class local boolean presence sensing; quantitative final-board rail/current/autonomy work is transferred by ADR-0007 to IHAP-55.
- ADR-0006 — MVP central-node hardware profile.
- ADR-0007 — Edge power subsystem: accepted 2026-09-07; normal regulated 5 V USB-C source, LG INR18650-MJ1 backup-only cell, custom modular PCB direction with MP2636GR-P as preferred charger/power-path/battery-boost PMIC candidate plus mandatory regulated 5 V post-stage or reviewed equivalent topology.

## Primary component sources used for planning / design contract

- Espressif ESP32-C3 Series Datasheet — supply domain and Wi-Fi current envelope.
- Hi-Link HLK-LD2410C official product/manual — 5 V supply, approximately 79 mA operating current and >200 mA source-capability requirement.
- Aosong/ASAIR DHT11 documentation — operating/standby current order of magnitude.
- Bosch BME280 datasheet — microamp-class bare-sensor average current at low-rate environmental sampling.
- LG Chem INR18650-MJ1 product specification — model-level capacity, charge/discharge and operating-envelope evidence.
- NKON LG INR18650-MJ1 listing, EAN/GTIN `8438493099829` — selected procurement identity; seller evidence records 3.6 V nominal, 3500 mAh typical / 3400 mAh minimum, 10 A discharge capability and approximately 18.2 mm × 65 mm dimensions.

### MP2636 — durable manufacturer references

Checked: **2026-09-07**.

- MPS product page: `https://www.monolithicpower.com/en/mp2636.html`
- MPS datasheet endpoint: `https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/Datasheet/lang/en/sku/MP2636/`
- Datasheet identifier/revision used for the decision: **MP2636 Rev.1.02, 2018-12-21**.
- Relevant manufacturer statements used by IHAP-49:
  - single-cell switch-mode charger with system power-path management;
  - input-current limit / input-voltage regulation;
  - selectable 4.2 V / 4.3 V / 4.35 V charge voltage;
  - NTC battery-temperature input;
  - reverse boost operation from battery;
  - **IN-to-SYS pass-through path while valid input is present**;
  - programmable SYS voltage belongs to boost mode, so MP2636 alone is not treated as proof of a regulated 5.0 V product rail in USB-powered mode.

### ETA9740 — durable manufacturer reference

Checked: **2026-09-07**.

- ETA Semiconductor datasheet: `https://www.eta-semi.com/wp-content/uploads/2022/03/ETA9740_V1.1.pdf`
- Datasheet identifier/revision used for comparison: **ETA9740 V1.1**.
- Disposition: future cost-down alternative only; not the first-reference implementation.

### Owned 4056E module evidence boundary

- 4056-family charger documentation is used only to bound the already-owned charger module.
- The owned `4056E + 8205A` board is not the final reference implementation and its unresolved RPROG/protection-controller identity is not used to justify the custom-board design.

## Procurement evidence boundary

The Project Owner selected a planned NKON order of 10 × LG INR18650-MJ1 at EUR 19.90 product subtotal plus EUR 6.33 shipping, planned total EUR 26.23. Purchase completion and received-lot conformance remain pending until explicitly confirmed and inspected.

No TPS61023, TPS2116 or additional charger/boost/mux breakout purchase is required solely to emulate the final custom PCB architecture.

## Evidence-quality rule

Primary manufacturer documentation defines component-level constraints. Seller evidence establishes listing/procurement identity but does not replace inspection of received cells. Physical custom-board charging, regulated-rail, thermal, 1 A load-step, transfer and endurance claims remain `[UNVALIDATED]` until IHAP-55 tests the fabricated implementation.
