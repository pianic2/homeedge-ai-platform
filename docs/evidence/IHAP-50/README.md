# IHAP-50 — Interconnect Evidence

**Issue:** IHAP-50  
**Status:** **ACCEPTED by Project Owner — 2026-09-11**; physical gates complete; PR #36 awaiting Codex review before merge  
**Branch:** `ihap-50-interconnect-prototype-assembly`  
**PR:** #36

## Purpose

This evidence index records the accepted source inputs, review findings, remediations, physical evidence and Project Owner acceptance for the IHAP-50 prototype interconnect baseline. It does **not** claim that the final custom PCB, power subsystem, enclosure integration or production node has been physically validated.

## Canonical outputs

- [`docs/architecture/ihap-50-interconnect-prototype-assembly.md`](../../architecture/ihap-50-interconnect-prototype-assembly.md)
- [`docs/architecture/ihap-50-connection-matrix.json`](../../architecture/ihap-50-connection-matrix.json)
- [`tools/hardware-validation/ihap-50-interconnect/README.md`](../../../tools/hardware-validation/ihap-50-interconnect/README.md)
- [`IHAP50-STANDARD-11-summary.md`](IHAP50-STANDARD-11-summary.md) / [`json`](IHAP50-STANDARD-11-summary.json)
- [`IHAP50-PRECISION-01-summary.md`](IHAP50-PRECISION-01-summary.md) / [`json`](IHAP50-PRECISION-01-summary.json)

Raw serial captures remain local under ignored `runs/` directories and are not committed by default.

## Accepted source inputs

| Input | State consumed | IHAP-50 use |
|---|---|---|
| ADR-0001 — MVP Edge Compute Platform | Accepted | ESP32-C3 GPIO/recovery baseline and spare ADC-capable requirement |
| ADR-0002 — Environmental Sensor Profiles | Accepted | alternative DHT11 / BME280 profile interfaces |
| ADR-0003 — MVP Door State Sensor | Accepted | reed-contact topology and semantic limitation |
| ADR-0004 — Local Status Display | Accepted | 3.3 V I2C OLED and BME280 bus-sharing direction |
| ADR-0005 — MVP Presence Sensor | Accepted | LD2410C 5 V/UART receive direction and boolean-only boundary |
| IHAP-48 audio disposition | Accepted closure | zero audio interconnect allocation |
| ADR-0007 — Edge Power Subsystem | Accepted | SYS_5V/SYS_3V3 domains and custom-PCB direction |
| IHAP-56 / PR #35 | merged remediation | Accepted-vs-Proposed separation; strengthened controls remain Proposed unless separately accepted |

## Accepted IHAP-50 contract

The Project Owner explicitly approved IHAP-50 on **2026-09-11** after successful STANDARD and PRECISION physical gates and final regression review. The following are therefore Accepted IHAP-50 implementation decisions:

- canonical GPIO/net allocation below;
- breadboard and loose Dupont as validation/development-only;
- keyed/polarized low-voltage connector classes as the final-reference direction while exact manufacturer series/SKU/footprint remains IHAP-55 scope;
- MC-38 reference network: 10 kOhm pull-up to `SYS_3V3` + 1 kOhm series resistor to GPIO3, with 100 nF filter footprint DNP by default;
- I2C/DHT board pull-up **footprint requirements and target/candidate values**, while exact final population remains IHAP-55 `[UNVALIDATED]` scope after effective module pull-ups are reconciled;
- STANDARD and PRECISION as alternative environmental profiles;
- ADR disposition: **no new ADR required**.

Acceptance does **not** promote controls that remain explicitly Proposed under IHAP-56.

## Canonical GPIO contract

```text
GPIO0  RADAR_RX_FROM_LD2410C_TX       UART1 RX @ 256000
GPIO1  RADAR_TX_TO_LD2410C_RX         SERVICE-ONLY reservation; disabled by default
GPIO3  DOOR_SENSE
GPIO4  ENV_DHT_DATA
GPIO5  SPARE_ADC_CAPABLE               ADC2_CH0
GPIO6  I2C_SDA
GPIO7  I2C_SCL
GPIO10 SPARE_DIGITAL
```

GPIO2/GPIO8/GPIO9 remain excluded as strapping pins. GPIO20/GPIO21 remain free for recovery/UART0 when practical. Audio receives zero allocation.

## Review/remediation history

### SR-50-01 — incorrect ADC capability — REMEDIATED

The initial draft incorrectly labelled GPIO10 as ADC-capable. The mapping was corrected so GPIO5 provides the required ADC-capable spare and GPIO10 remains digital-only. Human and machine-readable contracts were reconciled before physical validation.

### SR-50-02 — validation UART TX exceeded receive-only baseline — REMEDIATED

The initial harness attached GPIO1 as UART TX even though the accepted LD2410C baseline is receive-only. The harness now configures only GPIO0 RX, leaves GPIO1 as a physical/service reservation and emits `radar_tx_service_configured=false`; the evaluator fails if that contract regresses.

### SR-50-03 — ESP32-C3 target / USB console configuration — REMEDIATED

A physical flash attempt exposed a harness configuration defect: the build invoked `esptool --chip esp32` while the ROM bootloader correctly identified the board as ESP32-C3. Comparison with accepted IHAP-46/IHAP-47 harnesses also showed that IHAP-50 had not pinned the USB Serial/JTAG console used by the collector.

Remediation added `firmware/sdkconfig.defaults` with the ESP32-C3 target and USB Serial/JTAG console configuration. A 3.5 s native-USB re-enumeration guard is retained as defensive validation tooling. The board/ROM USB path was demonstrated healthy during recovery; no hardware failure was inferred from the aborted pre-remediation attempts.

### SR-50-04 — stale serial samples crossed operator phase boundaries — REMEDIATED

The first guided runner could attribute `integrated_sample` records queued while an operator changed the MC-38 condition to the next phase. The runner now:

- aborts immediately on requested/detected profile mismatch;
- clears queued serial input after each operator-confirmed acquisition boundary;
- records only fresh post-confirmation samples;
- displays sequence numbers to make temporal progression visible.

No sensor semantics or thresholds were weakened to obtain PASS.

## Accepted physical evidence

### IHAP50-STANDARD-11 — PASS

Commit under test: `6e1200afe15492c283edc6afd39059b2947b7fae`.

Validated:

- detected STANDARD profile; BME280 absent as required;
- exact canonical pin map;
- GPIO5 ADC-spare and GPIO10 digital-spare pull tests PASS;
- GPIO1 service TX disabled;
- OLED communication stable plus visual startup confirmation;
- DHT11 valid throughout baseline;
- LD2410C fresh with valid frames and zero parsed invalid frames;
- MC-38 OPEN/FAR = `1,1`;
- MC-38 CLOSED/NEAR = `0,0`;
- one MC-38 conductor disconnected = `1,1`;
- OLED and radar remained alive through all door phases;
- evaluator errors: none.

The accepted phase samples were temporally separated by the SR-50-04 acquisition boundaries: OPEN seq 8/9, CLOSED seq 14/15, DISCONNECTED seq 17/18.

### IHAP50-PRECISION-01 — PASS

Commit under test: `6e1200afe15492c283edc6afd39059b2947b7fae`.

Validated:

- detected PRECISION profile;
- BME280 present on shared I2C at `0x76` with identity `0x60`;
- BME280 communication successful across all six accepted baseline samples;
- DHT11 absent (`NO_RESPONSE`) as required by the alternative profile setup;
- OLED remained operational on the shared GPIO6/GPIO7 bus;
- LD2410C remained fresh with valid frames and zero parsed invalid frames;
- exact pin map, spare-pin checks and disabled radar service TX remained valid;
- evaluator errors: none.

Door phases were intentionally not duplicated because STANDARD-11 already supplied accepted MC-38 evidence.

## No-regression review

After remediation, physical execution and PO acceptance:

1. no strapping pin is allocated;
2. GPIO20/GPIO21 remain available for recovery/UART0 when practical;
3. GPIO5 preserves a real ADC-capable spare;
4. GPIO10 preserves digital margin;
5. radar receive UART does not collide with shared I2C;
6. GPIO1 remains service-only and undriven by the validation firmware;
7. OLED and BME280 coexist on I2C without address collision in PRECISION;
8. DHT11 and BME280 remain alternative accepted profiles, not a simultaneous product requirement;
9. MC-38 HIGH/open, LOW/closed and broken-conductor-as-HIGH behavior is physically demonstrated for the **Accepted IHAP-50 reference network**;
10. breadboard and loose Dupont wiring remain validation-only;
11. generic `PH2.0` remains prototype inventory; exact connector manufacturer/series/footprint belongs to IHAP-55;
12. audio remains zero-allocation;
13. controls explicitly remaining Proposed in IHAP-56 remain **Proposed**; IHAP-50 approval does not promote them;
14. branch changes remain confined to IHAP-50 specification, machine-readable matrix, evidence and validation tooling.

## Downstream handoff

The Accepted IHAP-50 contract is sufficient to hand the canonical connection matrix and validated prototype interconnect behavior to:

- **IHAP-55:** schematic/PCB implementation, exact connector/footprint freeze, effective I2C/DHT pull-up population, quantitative rail/load-step/source-transfer/thermal evidence;
- **IHAP-51:** enclosure routing, connector access, harness lengths, keepouts and strain relief;
- **IHAP-17:** final BOM quantities/costs once IHAP-55 freezes exact parts.

## ADR disposition

**Accepted: no new ADR is required for IHAP-50.** The task derives implementation/interconnect details from already Accepted architecture decisions and does not introduce a new cross-cutting architecture choice. The implementation contract and evidence remain in the architecture specification, connection matrix and this evidence index.

## Merge gate

Project Owner acceptance is complete. PR #36 must **not be merged until Codex review has been received and resolved**. Any Codex finding is remediated on this same IHAP-50 branch/PR under the one-task/one-branch/one-PR rule; acceptance is rechecked if a remediation changes the Accepted contract.

## Claim boundary

IHAP-50 evidence supports an **Accepted, physically validated prototype interconnect baseline for the tested STANDARD and PRECISION profiles**. It does not validate the final custom PCB, exact production connector SKU, final enclosure harness lengths, battery/power behavior, certification, production reliability or commercial readiness. Those remain owned by their downstream gates and are `[UNVALIDATED]` here.
