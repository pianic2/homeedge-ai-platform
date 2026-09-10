# IHAP-50 — Interconnect Evidence

**Issue:** IHAP-50  
**Status:** execution checkpoint — static design review complete; integrated gate ready for physical execution  
**Branch:** `ihap-50-interconnect-prototype-assembly`  
**PR:** #36

## Purpose

This evidence index records the sources, review findings and evidence boundary used to derive the IHAP-50 interconnect specification. It does not claim that the final custom PCB or integrated node has already been physically validated.

## Canonical outputs

- [`docs/architecture/ihap-50-interconnect-prototype-assembly.md`](../../architecture/ihap-50-interconnect-prototype-assembly.md)
- [`docs/architecture/ihap-50-connection-matrix.json`](../../architecture/ihap-50-connection-matrix.json)
- [`tools/hardware-validation/ihap-50-interconnect/README.md`](../../../tools/hardware-validation/ihap-50-interconnect/README.md)

## Accepted source inputs

| Input | State consumed | IHAP-50 use |
|---|---|---|
| ADR-0001 — MVP Edge Compute Platform | Accepted | ESP32-C3 GPIO/recovery baseline, eight safe application GPIO and spare ADC-capable requirement |
| ADR-0002 — Environmental Sensor Profiles | Accepted | DHT11 and BME280 profile interfaces |
| ADR-0003 — MVP Door State Sensor | Accepted | reed-contact topology and semantic limitations |
| ADR-0004 — Local Status Display | Accepted | 3.3 V I2C OLED profile and BME280 bus-sharing direction |
| ADR-0005 — MVP Presence Sensor | Accepted | LD2410C 5 V/UART direction and boolean-only product boundary |
| IHAP-48 audio disposition | accepted closure | zero audio interconnect allocation |
| ADR-0007 — Edge Power Subsystem | Accepted 2026-09-07 baseline | SYS_5V/SYS_3V3 domains and custom-PCB direction |
| IHAP-56 / PR #35 | remediation merged | Accepted-vs-Proposed separation; later Proposed controls remain Proposed |

## Primary-source review

Espressif ESP32-C3 documentation was used to verify the mapping rather than inheriting assumptions from validation-fixture pinouts.

Relevant static constraints:

- GPIO2, GPIO8 and GPIO9 are strapping pins and remain outside the reference application mapping;
- GPIO20/GPIO21 are kept available for UART0/recovery when practical;
- external JTAG functions overlap GPIO4/GPIO5/GPIO6/GPIO7, while the reference design retains native USB Serial/JTAG/recovery and prioritizes application I/O on the mapped pins;
- ADC-capable pins on ESP32-C3 are GPIO0 through GPIO5; GPIO5 provides ADC2_CH0;
- GPIO10 is a valid digital application candidate but **not** ADC-capable;
- peripheral signals such as I2C can be routed through the GPIO matrix, allowing the shared I2C bus to move to GPIO6/GPIO7.

Accepted module evidence also confirms:

- OLED address `0x3C` and BME280 address `0x76` do not collide;
- earlier IHAP-46 LD2410C validation used receive-only UART at 256000 baud;
- the accepted reed topology is HIGH when open and LOW when closed, with broken wire indistinguishable from open;
- audio remains outside the reference MVP.

## Static review history

### SR-50-01 — incorrect ADC capability in initial draft

**Severity before remediation:** MAJOR  
**Status:** REMEDIATED

Initial PR #36 draft mapping incorrectly labelled `GPIO10` as `SPARE_ADC_CAPABLE`. Official ESP32-C3 ADC mapping shows GPIO10 is not an ADC input. Leaving that mapping would have violated ADR-0001's requirement to preserve one spare ADC-capable GPIO.

Remediation applied before any integrated test or PCB handoff:

```text
GPIO0  RADAR_RX_FROM_LD2410C_TX
GPIO1  RADAR_TX_TO_LD2410C_RX_SERVICE_ONLY
GPIO3  DOOR_SENSE
GPIO4  ENV_DHT_DATA
GPIO5  SPARE_ADC_CAPABLE (ADC2_CH0)
GPIO6  I2C_SDA
GPIO7  I2C_SCL
GPIO10 SPARE_DIGITAL
```

The machine-readable matrix was bumped to schema version `1.1` and the human-readable specification contains the same corrected allocation.

### SR-50-02 — validation harness configured service TX despite receive-only baseline

**Severity before remediation:** MAJOR  
**Status:** REMEDIATED

The first integrated-harness implementation passed GPIO1 to `uart_set_pin()` as the UART TX pin even though the specification classifies that net as service-only and disabled by default. No product requirement or Accepted evidence required the harness to drive LD2410C RX.

Remediation commit `1efab860c404ee4bc30222f068fb0ad0ac5945c0` changed the harness to:

- configure UART1 RX only on GPIO0;
- pass `UART_PIN_NO_CHANGE` for TX;
- keep GPIO1 only as a physical/reference contract reservation;
- emit `radar_tx_service_configured=false` in the boot evidence record;
- make the host evaluator fail if service TX is unexpectedly enabled.

This keeps the IHAP-50 physical gate aligned with the receive-only LD2410C path already demonstrated by IHAP-46 and prevents an unreviewed configuration/control surface from being introduced merely by the test harness.

### Static no-regression observations after remediation

1. No strapping pin is allocated.
2. GPIO20/GPIO21 remain free for UART0/recovery when practical.
3. One real ADC-capable spare is preserved on GPIO5.
4. A second digital margin pin remains available on GPIO10.
5. Radar UART no longer collides with the shared I2C bus.
6. GPIO1 service TX is physically reserved but not configured by the validation firmware.
7. OLED+BME280 can share I2C without address collision in the accepted evidence set.
8. DHT11 and BME280 are tested as alternative environmental profiles rather than as an artificial simultaneous requirement.
9. Breadboard and loose Dupont wiring remain development/validation-only.
10. Generic `PH2.0` remains prototype inventory until exact mating parts and footprint are frozen in IHAP-55.
11. Audio remains zero-allocation.
12. Proposed IHAP-56 controls remain Proposed; this task does not upgrade them.

## Integrated gate implementation

The physical gate lives under:

```text
tools/hardware-validation/ihap-50-interconnect/
```

It contains:

- ESP-IDF validation firmware;
- a pure host-side evaluator;
- unit tests for standard/precision profiles and regression conditions;
- a guided serial runner;
- local-only `runs/` storage protected by `.gitignore`;
- one human runbook with exact wiring and commands.

The firmware emits structured JSON boot and sample records. The host runner records the exact git commit, validates the profile-specific expectations, guides the MC-38 open/closed/disconnected phases, records operator OLED/polarity confirmation, and produces local summary JSON/Markdown without automatically publishing raw serial telemetry.

The evaluator logic was exercised locally against seven synthetic scenarios covering both valid profiles plus ADC mapping, service-TX, BME identity, radar-frame and door-state regressions. This is host logic evidence only; it does not replace the required ESP-IDF build or physical run.

## Integrated evidence still required

Two lean physical runs remain:

1. `IHAP50-STANDARD-01` — OLED + LD2410C + MC-38 + DHT11; includes the door open/closed/disconnected phases.
2. `IHAP50-PRECISION-01` — OLED + LD2410C + BME280 on shared I2C; DHT11 disconnected; door phases are not duplicated.

Together they cover:

- boot/reset/flashing/recovery with selected peripherals attached;
- OLED+BME280 coexistence on GPIO6/GPIO7;
- DHT11 on GPIO4 while OLED and radar remain active;
- LD2410C receive UART on GPIO0 at 256000 baud while other interfaces operate;
- MC-38 HIGH/LOW mapping plus disconnected-wire observation on GPIO3;
- practical availability/usability of GPIO5 as ADC-capable spare and GPIO10 as digital spare on the exact implementation;
- connector pin-order and polarity review.

Exact final PCB I2C/DHT pull-up population remains an IHAP-55 schematic/BOM freeze item because breakout-module pull-ups must be reconciled against the final board rather than inferred from the prototype. Quantitative rail, load-step, battery, source-transfer and thermal evidence also remains IHAP-55 / ADR-0007 scope. Proposed IHAP-56 strengthening is not silently treated as Accepted.

## Claim boundary

Current evidence supports a **reviewed proposed interconnect design with a ready physical validation harness**, not a validated custom PCB. Final simultaneous behavior, exact connector SKU compatibility, final enclosure harness lengths and production maturity remain `[UNVALIDATED]` until their owning gates complete.
