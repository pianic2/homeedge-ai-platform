# IHAP-49 — Source Register

## Canonical project sources

- ADR-0001 — ESP32-C3 edge compute profile; board-level quantitative power delegated to IHAP-49 / later custom-board implementation.
- ADR-0002 — DHT11 standard indoor / BME280 precision profile; alternatives rather than simultaneous reference loads.
- ADR-0003 — passive wired reed contact; final pull-network implementation coordinated with IHAP-50.
- ADR-0004 — local 0.96-inch-class 128×64 I2C OLED; exact owned-module current remains unvalidated.
- ADR-0005 — HLK-LD2410C-class local boolean presence sensing.
- IHAP-45 evidence — a real integrated brownout/re-enumeration occurred during an initial preflight; power implementation therefore retains explicit brownout/reset validation.
- IHAP-55 — Integrated Modular Edge PCB — Custom Mainboard Design and Prototype; implementation/validation consumer of ADR-0007.

## Primary component sources

### ESP32-C3

- Espressif ESP32-C3 Series Datasheet — supply domain and Wi-Fi current envelope.

### Presence radar

- Hi-Link HLK-LD2410C official product/manual — 5 V supply, approximately 79 mA operating current and >200 mA source-capability requirement.

### Environmental sensors

- Aosong/ASAIR DHT11 documentation — measurement/standby current order of magnitude.
- Bosch BME280 datasheet — microamp-class bare-sensor current at low-rate sampling.

### Selected cell

- LG INR18650-MJ1 product specification — model-level capacity, charging/discharge boundaries and operating envelope.
- NKON LG INR18650-MJ1 listing, EAN/GTIN `8438493099829` — selected seller/procurement identity used by the Project Owner.

Owner-provided order-decision values:

- 10 cells product subtotal EUR 19.90;
- shipping EUR 6.33;
- planned landed total EUR 26.23.

Purchase completion/received-lot conformance are not implied until explicitly confirmed and inspected.

### Owned charger characterization

- 4056-family reference datasheets — family-level interpretation only; they do not establish the exact vendor/protection thresholds of the owned specimen.
- Physical specimen evidence — `4056E` charger marking, `8205A` dual MOSFET and separate protection-controller IC observed.
- `IHAP49-CHARGER-C0-C1-01/run-record.md` — actual bench evidence.

### Preferred custom-board PMIC

- Monolithic Power Systems `MP2636` official product page and datasheet — Active 3 A switch-mode single-cell charger with system power-path management and system boost.
- Relevant official characteristics used by IHAP-49:
  - 4.5–6 V operating input;
  - system power-path / system-load priority;
  - programmable input-current limit and input-voltage regulation;
  - up to 3 A programmable charge current;
  - selectable 4.2/4.3/4.35 V battery-full voltage;
  - NTC battery-temperature input;
  - programmable boost SYS voltage from 4.2 V to 6 V;
  - programmable boost current limit;
  - pass-through OCP/OVP;
  - boost short-circuit/OVP;
  - battery-current monitor output.

- Mouser Europe `MP2636GR-P` price/availability snapshot checked 2026-09-07:
  - in stock at time checked;
  - approximately EUR 3.67 qty 1;
  - approximately EUR 2.78 qty 10;
  - approximately EUR 2.55 qty 25.

These are dated planning prices, not purchasing guarantees.

### Cost-down PMIC alternative

- ETA Semiconductor `ETA9740` official datasheet — bidirectional single-inductor switching charger / 5 V boost, automatic mode switching, up to 3 A charge and 2.4 A discharge class.
- LCSC `ETA9740E8A` snapshot checked 2026-09-07:
  - in stock at time checked;
  - approximately USD 0.26 at qty 5.

ETA9740 remains a future cost-down candidate rather than first-reference selection because the current architecture prioritizes explicit NTC monitoring and separated input/SYS behavior for revision 1.

## Evidence-quality rule

Primary manufacturer documentation establishes component-level capabilities and constraints. Seller/distributor pages establish dated procurement/availability evidence. Neither replaces physical validation of the fabricated custom board.

Planning load/current/autonomy arithmetic is not a runtime measurement. Physical charge, rail, source-transfer, thermal and endurance claims remain IHAP-55 evidence.
