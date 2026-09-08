# IHAP-49 — Source Register

## Approval boundary

ADR-0007 / PR #34 was accepted by the Project Owner on 2026-09-07. IHAP-56 subsequently added treatment and validation detail that remains **Proposed** until explicitly approved. Manufacturer sources can support the rationale for those proposed controls, but source validity does not itself approve a project treatment or ADR amendment.

## Canonical project sources

- ADR-0001 — MVP edge compute platform; accepted ADR-0007 baseline transfers quantitative final-board power work to IHAP-55.
- ADR-0002 — DHT11 standard / BME280 precision profile; accepted ADR-0007 baseline transfers quantitative current work to IHAP-55.
- ADR-0003 — passive wired reed contact; final pull network under IHAP-50. **IHAP-56 proposes** transferring quantitative closed-loop current work to IHAP-55; that reassignment is not part of the 2026-09-07 ADR-0007 acceptance until explicitly approved or assigned by another accepted decision.
- ADR-0004 — accepted local OLED; accepted ADR-0007 baseline transfers display-current/sleep-policy measurement to IHAP-55.
- ADR-0005 — LD2410C presence sensing; accepted ADR-0007 baseline transfers quantitative current/rail/autonomy contribution to IHAP-55.
- ADR-0006 — MVP central-node hardware profile.
- ADR-0007 — **Accepted baseline**: regulated 5 V USB-C normal source, LG INR18650-MJ1 backup-only cell, custom modular PCB direction, MP2636GR-P preferred charger/power-path/battery-boost candidate plus regulated 5 V post-stage or reviewed equivalent. **Proposed IHAP-56 amendment**: cell-side interruption, mandatory NTC fault-state tests, numeric thermal/low-voltage criteria, V13/V14/V15, strengthened V7/V8/V9 and ADR-0003 ownership extension.

## Primary component sources used for planning / Proposed treatment validation detail

### LG INR18650-MJ1

Checked: **2026-09-08**.

Manufacturer specification mirrors:

- LG Chem `PRODUCT SPECIFICATION — Lithium Ion INR18650 MJ1 3500mAh`, Date **2014-08-22**, Rev. **1**: `https://files.batteryjunction.com/frontend/files/lg/datasheet/LG-MJ1-Datasheet.pdf`
- LG Chem `PRODUCT SPECIFICATION — Lithium Ion INR18650 MJ1 3500mAh`, Date **2016-06-30**, Rev. **1**, hosted by selected seller NKON: `https://www.nkon.nl/en/amfile/file/download/file/499/product/5626/`
- NKON selected listing identity: EAN/GTIN `8438493099829`.

Manufacturer/model-level values used to support the **Proposed** IHAP-56 numeric validation overlay:

- nominal voltage 3.635 V in LG specification;
- max charge voltage **4.20 ±0.05 V**;
- manufacturer discharge end voltage **2.50 V**;
- max discharge current 10 A in the registered product specification;
- operating temperature: **charge 0–45 °C; discharge -20–60 °C**;
- selected seller/listing dimensions remain procurement evidence; received-cell identity/condition/fit remain `[UNVALIDATED]` until inspection.

The proposed first-reference product cutoff **2.70 ±0.05 V** and recovery **>=3.00 ±0.05 V** are project-level conservative treatment values above the manufacturer 2.50 V discharge-end value. They are neither LG requirements nor accepted project criteria until the Project Owner approves the amendment/treatment scope.

### MP2636

Checked: **2026-09-08**.

- MPS product page: `https://www.monolithicpower.com/en/mp2636.html`
- MPS datasheet: `https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/Datasheet/lang/en/sku/MP2636/`
- Datasheet identifier/revision: **MP2636 Rev.1.02, 2018-12-21**.

Relevant manufacturer statements:

- single-cell switch-mode charger with system power-path management;
- input-current limit / input-voltage regulation;
- selectable 4.2 V / 4.3 V / 4.35 V charge voltage;
- NTC battery-temperature input;
- reverse boost operation from battery;
- **IN-to-SYS pass-through path while valid input is present**;
- programmable SYS voltage applies in boost mode, supporting the accepted need for downstream 5 V regulation or reviewed equivalent;
- recommended operating junction temperature **-40 to +125 °C**;
- thermal shutdown approximately **150 °C** and recovery around **120 °C**; treating shutdown as a FAIL criterion belongs to the **Proposed IHAP-56 thermal treatment overlay** until approved.

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

## Evidence-quality / treatment rule

Primary manufacturer documentation defines component-level constraints. Seller evidence establishes procurement identity but does not replace inspection of received cells. Manufacturer limits can justify a proposed control, but **cannot advance RT-R012-01/RT-R013-01 lifecycle or amend Accepted ADR-0007 without explicit Project Owner decision evidence**.

Physical custom-board charging, regulated-rail, thermal, source-limit, dynamic load-step, source-transfer and endurance claims remain `[UNVALIDATED]` until the applicable approved scope is implemented and tested.
