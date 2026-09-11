# IHAP-55 — Manufacturer and Sourcing Evidence Register

**Checked:** 2026-09-11  
**Status:** design-selection evidence; no procurement authorization

Primary manufacturer documentation governs electrical/mechanical limits. Distributor evidence is used only for dated availability/price observations and does not replace manufacturer specifications.

## SR-55-01 — ESP32-C3 module candidate

**Candidate:** Espressif `ESP32-C3-MINI-1-N4X`.

Manufacturer evidence:

- ESP32-C3-MINI-1 / MINI-1U Datasheet v2.2, 2026-05-06: `https://documentation.espressif.com/esp32-c3-mini-1_datasheet_en.html`
- ESP32-C3 Hardware Design Guidelines: `https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c3/`

Verified manufacturer facts:

- `ESP32-C3-MINI-1-N4X` is listed as **Recommended**;
- 4 MB Quad SPI flash, chip revision v1.1;
- module size 13.2 x 16.6 x 2.4 mm;
- integrated PCB antenna;
- module supply 3.0–3.6 V;
- native USB Serial/JTAG is available on GPIO18/GPIO19;
- module-on-board placement must protect antenna clearance/keepout; Espressif recommends at least 15 mm clearance around the PCB antenna in the final housing.

Dated sourcing observation:

- DigiKey Italy, checked 2026-09-11: unit price EUR 2.79 ex VAT at qty 1; listing showed 0 immediately in stock and 650 expected 2026-09-14.

Availability is therefore acceptable for evaluation but not yet strong enough to call supply risk closed. No order authorized.

## SR-55-02 — Charger / power-path candidate

**Candidate:** Monolithic Power Systems `MP2636GR-P`.

Manufacturer evidence:

- product page: `https://www.monolithicpower.com/en/mp2636.html`
- MP2636 datasheet Rev.1.02: `https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/Datasheet/lang/EN/sku/MP2636/document_id/1443/`

Verified manufacturer facts relevant here:

- Active part number `MP2636GR-P`;
- QFN-30 4 x 4 mm;
- single-cell charger with system power-path management and battery boost;
- 4.5–6 V operating input range;
- programmable input-current limit/input-voltage regulation;
- selectable 4.2/4.3/4.35 V charge voltage;
- NTC input;
- valid-input operation uses the input/system pass-through behavior already captured by ADR-0007;
- boost/current protection features do not by themselves prove the complete Accepted product-level battery/system protection contract.

Dated sourcing observation:

- MPS direct, checked 2026-09-11: product page showed MP2636GR-P/GR-Z in stock, direct qty-1 price USD 3.80, 10-unit price USD 2.87; 50,000 units shown in stock with estimated shipment by 2026-09-15.
- Mouser EU also listed `MP2636GR-P` in stock (1,643 observed) but factory lead time was long; use multiple-source stock checks again at procurement gate.

No order authorized.

## SR-55-03 — 5 V post-regulator candidate

**Candidate:** Texas Instruments `TPS63802DLAR`.

Manufacturer evidence:

- `https://www.ti.com/product/TPS63802`

Verified manufacturer facts:

- Active;
- synchronous buck-boost;
- 1.3–5.5 V input;
- adjustable 1.8–5.2 V output;
- 2 A product-class output rating under datasheet conditions;
- VSON-HR 3 x 2 mm package;
- integrated soft start, load disconnect and forward/backward current limiting.

Dated sourcing observation:

- DigiKey Italy, checked 2026-09-11: `TPS63802DLAR`, EUR 2.42 ex VAT at qty 1; 5,902 units observed in stock in the retrieved listing.

**Design state:** `[UNVALIDATED]` as final 5 V regulator until IHAP-55 proves the full intermediate-SYS range, output-current capability at 5.0 V, transient target, inductor/capacitor sizing, tolerance and thermal margin.

## SR-55-04 — 3.3 V regulator candidate

**Candidate:** Texas Instruments `TLV62568DBVR`.

Manufacturer evidence:

- `https://www.ti.com/product/TLV62568`

Verified manufacturer facts:

- Active;
- synchronous buck;
- 2.5–5.5 V input;
- 1 A output;
- adjustable output;
- SOT-23-5 option;
- -40 to 125 °C junction operating range listed on manufacturer/distributor data.

Dated sourcing observation:

- DigiKey Italy, checked 2026-09-11: EUR 0.27 ex VAT at qty 1; 48,086 units observed in stock.

**Design state:** `[UNVALIDATED]` until feedback/passive sizing, rail tolerance, Wi-Fi peak load and thermal calculations are complete.

## SR-55-05 — USB-C receptacle candidate

**Candidate:** GCT `USB4105-GF-A`.

Manufacturer evidence:

- GCT USB Type-C product selection guide: `https://gct.co/files/productbrochures/gct-usb-type-c-product-selection-guide_web.pdf`
- USB4105 product family/CAD landing: `https://gct.co/connector/USB4105`

Distributor observation:

- DigiKey Italy, checked 2026-09-11: `USB4105-GF-A`, Active, USB 2.0 Type-C receptacle, 16 active contacts / 24 positions including dummy positions, SMT right-angle with through-hole retention, rated 5 A by listing; EUR 0.68 ex VAT at qty 1 and 142,810 units observed in stock.

The connector rating does not set the board input-current policy. Accepted reference source behavior remains governed by ADR-0007.

## SR-55-06 — USB data ESD candidate

**Candidate:** STMicroelectronics `USBLC6-2SC6`.

Manufacturer evidence:

- `https://www.st.com/en/protections-and-emi-filters/usblc6-2.html`

Verified manufacturer facts:

- Active / volume production;
- intended for USB 2.0 high-speed ESD protection;
- two data-line protection;
- SOT23-6L variant available;
- low line capacitance and IEC 61000-4-2 level-4 device protection stated by ST.

**Design state:** candidate for D+/D- only. Complete VBUS/input protection remains `[UNVALIDATED]` and must be frozen separately.

## SR-55-07 — Low-power external module connectors

**Candidate family:** JST PH.

Manufacturer evidence:

- official JST model directory: `https://www.jst-mfg.com/product/index.php?lang=2&series=199`
- JST PH series regional product profile: `https://jst.es/producto/ph-connector/`

Verified family facts:

- 2.0 mm pitch;
- 2 A family rating with AWG24 in JST profile;
- controlled housings include `PHR-2`, `PHR-4`, `PHR-5`;
- controlled board headers include `B2B-PH-K-S`, `B4B-PH-K-S`, `B5B-PH-K-S`;
- crimp contacts include `SPH-002T-P0.5S`.

Availability note:

- distributor stock varies by position and region. Example: DigiKey Italy listing for `B4B-PH-K-S` was inconsistent across crawls (one result zero stock/backorder, another 35k+ stock) at about EUR 0.17–0.18 qty 1. Availability must therefore be rechecked at the procurement gate rather than treated as frozen.

## SR-55-08 — Battery/service connector candidate

**Candidate family:** JST XH.

Manufacturer evidence:

- official JST model directory: `https://www.jst-mfg.com/product/index.php?lang=2&series=277`
- JST XH regional product profile: `https://jst.es/en/producto/xh-connector/`

Verified family facts:

- 2.5 mm pitch;
- 3 A family rating with AWG22 in JST profile;
- board header `B2B-XH-A`;
- housing `XHP-2`;
- contacts include `SXH-001T-P0.6` / `SXH-002T-P0.6` variants.

Wire gauge/contact variant and holder termination remain `[UNVALIDATED]` until actual battery-service harness mechanics are frozen.

## SR-55-09 — EDA baseline

**Selected engineering tool baseline:** KiCad **10.0.6 stable**.

Official evidence:

- release notice, 2026-08-29: `https://www.kicad.org/blog/2026/08/KiCad-10.0.6-Release/`

KiCad 10.0.6 is the current stable bug-fix release observed on 2026-09-11. Nightly/testing builds are not the project baseline.

## Evidence boundary

No dated price above is a purchase authorization or definitive IHAP-17 cost. Prices exclude shipping unless explicitly stated, can change, and must be refreshed at the procurement/BOM gate. Final BOM requires exact passive/inductor/protection MPNs, quantities and fabrication/assembly allocation.