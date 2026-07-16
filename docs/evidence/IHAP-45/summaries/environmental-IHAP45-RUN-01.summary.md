# IHAP-45 Environmental Comparison Summary — IHAP45-RUN-01

**Status:** `PASSED`  
**Plan:** `IHAP45-QUALIFICATION-01`  
**Comparison scope:** `relative_only`  
**Published channels:** temperature and relative humidity only

## Harness identity

| Field | Value |
|---|---|
| Firmware | `ihap-45-environmental-sensor-harness` |
| ESP-IDF | `v6.0.1` |
| Sample interval | 5000 ms |
| BME280 address | `0x76` |
| BME280 chip ID | `0x60` |
| Humidity supported | true |

## Validation

| Check | Value |
|---|---:|
| Sample records | 5769 |
| Boot records | 1 |
| Probe records | 1 |
| Independent reference observations | 0 |

### Errors

- none

### Warnings

- no independent reference observations; absolute accuracy metrics are not available

## Phase coverage

| Phase | Observed duration (s) |
|---|---:|
| `unclassified` | 65.0 |
| `warmup` | 1509.9 |
| `baseline` | 845.0 |
| `humidity_ramp_up` | 330.0 |
| `humidity_high_plateau` | 815.0 |
| `humidity_recovery` | 640.0 |
| `humidity_low_plateau` | 1050.0 |
| `humidity_final_recovery` | 720.0 |
| `temperature_ramp_up` | 355.0 |
| `temperature_high_plateau` | 630.0 |
| `temperature_recovery` | 900.0 |
| `temperature_low_plateau` | 630.0 |
| `final_recovery` | 1120.0 |

## Aggregate sensor results

| Sensor | Valid | Valid % | Mean °C | SD °C | Mean RH % | SD RH | Median read µs |
|---|---:|---:|---:|---:|---:|---:|---:|
| DHT11-OWNED-01 | 1923/1923 | 100.00% | 30.929 | 4.196 | 48.689 | 8.596 | 23977.0 |
| DHT22-OWNED-01 | 1921/1923 | 99.90% | 32.020 | 4.134 | 51.756 | 7.235 | 5762.0 |
| BME280-OWNED-01 | 1923/1923 | 100.00% | 31.045 | 4.427 | 46.523 | 8.872 | 11152.0 |

## Evidence boundary

No serial log, individual sample, marker stream, reference-observation stream, per-sample CSV, workstation path or embedded interactive telemetry is included. Pairwise aggregates, per-phase aggregates, response estimates and optional aggregate reference metrics remain available in the companion JSON summary.

A `PASSED` summary establishes only that the committed protocol and thresholds were met by the owned specimens in the executed setup. It does not establish universal sensor-family behavior, final enclosure fitness, calibrated accuracy without an independent reference, or power-system characterization.
