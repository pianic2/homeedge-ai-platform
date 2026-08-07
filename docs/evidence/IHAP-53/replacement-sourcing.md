# IHAP-53 Replacement Sourcing Snapshot

**Checked:** 2026-08-07  
**Purpose:** evidence that the reference 0.96-inch 128×64 I2C OLED profile can be replicated independently of the owned specimen

Prices are dated market snapshots, not purchasing guarantees.

| Source | Example | Snapshot price | Relevant profile evidence | Status |
|---|---|---:|---|---|
| Homotix (Italy) | 0.96-inch 128×64 I2C OLED, SSD1306 | €4.27 incl. displayed retail pricing context | 128×64, SSD1306, I2C, 3–5 V supply, 3.3/5 V I/O compatibility | Candidate replacement source |
| OpenELAB | 0.96-inch 128×64 I2C OLED, SSD1306 | €8.02 incl. VAT | 0.96-inch, 128×64, SSD1306, I2C | Candidate replacement source |
| GoldenMorning | GME12864-11/12/13 family | Quote-based / no public unit price used | 0.96-inch, 128×64, I2C, SSD1306; `-12` blue | Primary family-identification source |

Sources:

- <https://www.homotix.it/vendita/display-oled/display-oled-128x64-096-pollici-i2c-bianco>
- <https://openelab.io/it/products/096incholedssd1306display>
- <https://goldenmorninglcd.com/oled-display-module/0.96-inch-128x64-ssd1306-gme12864-11/>

## Interpretation

The BOM must not use the owned specimen's sunk cost as `€0` replication cost. After ADR acceptance, IHAP-17 should record:

1. the generic required profile;
2. the tested reference implementation;
3. a dated current replacement-price source.

Mechanical envelope and exact interchangeability remain subject to IHAP-51 and the replacement-profile constraints in ADR-0003.
