# IHAP-49 — Source Register

## Canonical project sources

- ADR-0001 — MVP edge compute platform; quantitative final-board power work transferred by ADR-0007 to IHAP-55.
- ADR-0002 — DHT11 standard / BME280 precision profile; quantitative current work transferred to IHAP-55.
- ADR-0003 — passive wired reed contact; final pull network under IHAP-50; quantitative closed-loop current transferred to IHAP-55.
- ADR-0004 — accepted local OLED; display-current/sleep-policy measurement transferred to IHAP-55.
- ADR-0005 — LD2410C presence sensing; quantitative current/rail/autonomy contribution transferred to IHAP-55.
- ADR-0006 — MVP central-node hardware profile.
- ADR-0007 — accepted edge power architecture: regulated 5 V USB-C normal source, LG INR18650-MJ1 backup-only cell, custom modular PCB direction, MP2636GR-P preferred charger/power-path/battery-boost candidate plus mandatory regulated 5 V post-stage or reviewed equivalent.

## Primary component sources used for planning / validation contract

### LG INR18650-MJ1

Checked: **2026-09-08**.

Manufacturer specification mirrors used for model-level limits:

- LG Chem `PRODUCT SPECIFICATION — Lithium Ion INR18650 MJ1 3500mAh`, Date **2014-08-22**, Rev. **1**: `https://files.batteryjunction.com/frontend/files/lg/datasheet/LG-MJ1-Datasheet.pdf`
- LG Chem `PRODUCT SPECIFICATION — Lithium Ion INR18650 MJ1 3500mAh`, Date **2016-06-30**, Rev. **1**, hosted by selected seller NKON: `https://www.nkon.nl/en/amfile/file/download/file/499/product/5626/`
- NKON selected listing identity: EAN/GTIN `8438493099829`.

Limits used by the IHAP-49 validation contract:

- nominal voltage 3.635 V in LG specification;
- max charge voltage **4.20 ±0.05 V**;
- manufacturer discharge end voltage **2.50 V**;
- max discharge current 10 A in the registered product specification;
- operating temperature: **charge 0–45 °C; discharge -20–60 °C**;
- selected seller/listing dimensions remain procurement evidence; received-cell identity/condition/fit remain `[UNVALIDATED]` until inspection.

The first-reference product cutoff **2.70 ±0.05 V** and recovery **>=3.00 ±0.05 V** are project-level conservative controls above the manufacturer 2.50 V discharge end voltage; they are not represented as LG manufacturer requirements.

### MP2636

Checked: **2026-09-08**.

- MPS product page: `https://www.monolithicpower.com/en/mp2636.html`
- MPS datasheet: `https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/Datasheet/lang/en/sku/MP2636/`
- Datasheet identifier/revision: **MP2636 Rev.1.02, 2018-12-21**.

Relevant manufacturer statements used:

- single-cell switch-mode charger with system power-path management;
- input-current limit / input-voltage regulation;
- selectable 4.2 V / 4.3 V / 4.35 V charge voltage;
- NTC battery-temperature input;
- reverse boost operation from battery;
- **IN-to-SYS pass-through path while valid input is present**;
- programmable SYS voltage applies in boost mode, so MP2636 alone is not proof of regulated 5.0 V USB-powered product SYS;
- recommended operating junction temperature **-40 to +125 °C**;
- thermal shutdown occurs at approximately **150 °C** and normal operation resumes around **120 °C**; entering thermal shutdown is a validation FAIL, not an allowed normal operating condition.

### Other accepted-load sources

- Espressif ESP32-C3 Series Datasheet — supply domain and Wi-Fi current envelope.
- Hi-Link HLK-LD2410C official product/manual — 5 V supply, approximately 79 mA operating current and >200 mA source-capability requirement.
- Aosong/ASAIR DHT11 documentation — operating/standby current order of magnitude.
- Bosch BME280 datasheet — microamp-class bare-sensor average current at low-rate environmental sampling.

### ETA9740 — comparison only

Checked: **2026-09-07**.

- ETA Semiconductor datasheet: `https://www.eta-semi.com/wp-content/uploads/2022/03/ETA9740_V1.1.pdf`
- Revision: **ETA9740 V1.1**.
- Disposition: future cost-down alternative only.

### Owned 4056E module evidence boundary

4056-family documentation is used only to bound the already-owned charger module. The owned `4056E + 8205A` board is not the final reference implementation and its unresolved RPROG/protection-controller identity is not used to justify the custom-board design.

## Procurement evidence boundary

The Project Owner selected a planned NKON order of 10 × LG INR18650-MJ1 at EUR 19.90 product subtotal plus EUR 6.33 shipping, planned total EUR 26.23. Purchase completion and received-lot conformance remain pending until explicitly confirmed and inspected.

No TPS61023, TPS2116 or additional charger/boost/mux breakout purchase is required solely to emulate the final custom PCB architecture.

## Evidence-quality / thermal rule

Primary manufacturer documentation defines component-level constraints. Before V4/V6 physical validation, IHAP-55 must register manufacturer numeric operating/rated temperature limits for the exact post-regulator, 3.3 V regulator, inductor and protection components and define how measured test-point temperature maps to the applicable device limit. A rail-stable run that exceeds a registered temperature limit is FAIL.

Seller evidence establishes procurement identity but does not replace inspection of received cells. Physical custom-board charging, regulated-rail, thermal, source-limit, bidirectional load-step, high/mid/low transfer and endurance claims remain `[UNVALIDATED]` until IHAP-55 tests the fabricated implementation.
