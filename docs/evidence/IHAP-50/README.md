# IHAP-50 — Interconnect Evidence

**Issue:** IHAP-50  
**Status:** execution checkpoint — physical/integrated gate pending  
**Branch:** `ihap-50-interconnect-prototype-assembly`

## Purpose

This evidence index records the sources and review boundary used to derive the IHAP-50 interconnect specification. It does not claim that the final custom PCB or integrated node has already been physically validated.

## Canonical outputs

- [`docs/architecture/ihap-50-interconnect-prototype-assembly.md`](../../architecture/ihap-50-interconnect-prototype-assembly.md)
- [`docs/architecture/ihap-50-connection-matrix.json`](../../architecture/ihap-50-connection-matrix.json)

## Accepted source inputs

| Input | State consumed | IHAP-50 use |
|---|---|---|
| ADR-0001 — MVP Edge Compute Platform | Accepted | ESP32-C3 GPIO/recovery baseline and engineering margin |
| ADR-0002 — Environmental Sensor Profiles | Accepted | DHT11 and BME280 profile interfaces |
| ADR-0003 — MVP Door State Sensor | Accepted | reed contact topology and semantic limitations |
| ADR-0004 — Local Status Display | Accepted | 3.3 V I2C OLED profile and BME280 bus-sharing direction |
| ADR-0005 — MVP Presence Sensor | Accepted | LD2410C 5 V / UART direction and boolean-only product boundary |
| IHAP-48 audio disposition | accepted closure | zero audio interconnect allocation |
| ADR-0007 — Edge Power Subsystem | Accepted 2026-09-07 baseline | SYS_5V/SYS_3V3 domains and custom-PCB direction |
| IHAP-56 / PR #35 | remediation merged | Accepted-vs-Proposed separation only; later Proposed controls remain Proposed |

## External primary references reviewed

- Espressif ESP32-C3 Series Datasheet — strapping pins, peripheral/GPIO constraints and recovery interfaces.
- Espressif ESP32-C3 hardware design guidelines — boot/strapping design constraints.
- Bosch Sensortec BME280 datasheet — I2C interface and 3.3 V-compatible supply domain.
- Hi-Link LD2410C documentation — module family interface and power documentation.
- DHT11 family manual evidence — 3.3–5.5 V supply and approximately 5 kOhm data pull-up reference.

## Static review observations

1. `GPIO2`, `GPIO8`, and `GPIO9` must remain outside the reference application mapping because they are ESP32-C3 strapping pins.
2. `GPIO20/21` are intentionally kept available for UART0/recovery when practical.
3. OLED and accepted BME280 specimen addresses (`0x3C` and `0x76`) do not collide.
4. The earlier IHAP-46 validation wiring used LD2410C TX on GPIO5, which would collide with the final shared I2C bus. The IHAP-50 reference mapping therefore moves radar UART to GPIO0/GPIO1 and keeps GPIO5/GPIO6 for I2C.
5. The accepted MC-38 topology requires a deterministic pull-up and must retain the open-contact versus broken-wire ambiguity.
6. Breadboard and loose Dupont wiring are not compatible with the accepted custom-PCB final-reference direction and are classified as development/validation-only.
7. Generic `PH2.0` naming is not sufficient evidence for a controlled connector family; exact mating parts/footprints remain an IHAP-55 BOM freeze item.
8. Audio remains zero-allocation.

## Physical / integrated evidence still required

The lean integrated gate is intentionally limited to evidence that cannot be proven statically:

- boot/reset/recovery with selected peripherals attached;
- OLED+BME280 shared-I2C coexistence;
- DHT11 standard profile while OLED/radar remain active;
- LD2410C UART at 256000 baud on the reference/equivalent final mapping;
- MC-38 HIGH/LOW mapping plus disconnected-wire observation;
- confirmation that GPIO7/GPIO10 are not accidentally consumed by the exact implementation;
- connector pin-order/polarity review;
- measurement/identification of effective I2C and DHT pull-up networks before final PCB population.

Quantitative rail, load-step, battery, source-transfer and thermal evidence remains IHAP-55 / ADR-0007 scope. Proposed IHAP-56 strengthening is not silently treated as Accepted.

## Claim boundary

Current evidence supports a **reviewable proposed interconnect design**, not a validated custom PCB. Final integrated behavior, exact connector SKU compatibility, exact enclosure harness lengths and production maturity remain `[UNVALIDATED]`.
