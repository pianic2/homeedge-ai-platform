# IHAP-45 Qualification Status

**Updated:** 2026-07-16  
**Decision state:** accepted by Project Owner and recorded in ADR-0002  
**Current gate:** normalized controlled run accepted; PR review pending

## Visible execution history

| Stage | Result | Evidence classification | What it established |
|---|---|---|---|
| Initial parallel preflight | `FAIL` | local raw run retained | all three sensors produced valid concurrent samples, but startup metadata was missed by the first collector implementation |
| USB-resilient preflight | `FAIL` | local raw run retained | collector survived ESP32-C3 native-USB reset, but one-shot boot/probe records were emitted before Linux re-enumeration completed |
| Delayed-start resilient preflight | `FAIL` | local raw run retained | BME280 identity was captured as address `0x76`, chip ID `0x60`, humidity supported; a real brownout caused an unexpected reboot and correctly failed the gate |
| Staged functional-stability isolation | `PASS` | sanitized aggregate summaries | board-only and incremental sensor configurations completed the qualification window without brownout or unexpected reboot |
| Original controlled environmental comparison | `PROVISIONAL PASS` | local source retained; superseded publication | every phase completed, but pre-reset samples caused impossible completeness values above 100% |
| First-boot normalization | `PASS` | non-destructive derived run | removed pre-reset contamination while preserving the original local run and retaining exactly one boot |
| Normalized controlled environmental comparison | `PASS` | reviewed Markdown, JSON and aggregate-only HTML | 5,769 samples; all sensors at 100% completeness; no validation errors; relative-only comparison |
| Environmental sensor profile decision | `ACCEPTED` | ADR-0002 | DHT11 standard indoor profile; BME280 precision / extended-environment profile; DHT22 not selected |

Failed trials and evidence-quality defects remain visible engineering history. They are not rewritten as passes. Raw acquisition files remain local; the repository contains the reproducible method and reviewed aggregate evidence only.

## Corrective actions made visible

1. The host collector was changed to survive ESP32-C3 USB disconnect and re-enumeration.
2. Validation-harness startup was delayed so `harness_boot` and `sensor_probe` become observable after reset.
3. The preflight retained the multiple-boot failure rule and exposed the brownout rather than weakening acceptance criteria.
4. A staged functional-stability diagnostic isolated board-only and incremental sensor configurations.
5. Repository evidence publication was restricted to generated aggregate summaries; raw telemetry remains ignored locally.
6. A self-contained aggregate-only HTML publisher was added so visual evidence does not publish the original Plotly per-sample payload.
7. A non-destructive normalizer removed pre-reset records after the first summary exposed completeness values above 100%.
8. Generated ESP-IDF `sdkconfig` files were removed from version control; `sdkconfig.defaults` remains the intentional configuration source.

## Accepted normalized result

| Check | Result |
|---|---:|
| Validation status | `PASSED` |
| Comparison scope | `relative_only` |
| Sample records | 5,769 |
| Boot records | 1 |
| Probe records | 1 |
| Independent reference observations | 0 |
| DHT11 completeness | 100% |
| DHT11 valid samples | 1,923 / 1,923 |
| DHT22 completeness | 100% |
| DHT22 valid samples | 1,921 / 1,923 |
| DHT22 errors | 2 × `NO_RESPONSE` |
| BME280 completeness | 100% |
| BME280 valid samples | 1,923 / 1,923 |
| Validation errors | none |

## Qualified specimen identity

```text
sensor_id: BME280-OWNED-01
I2C address: 0x76
chip ID: 0x60
detected type: BME280
humidity supported: true
```

This identity applies only to the tested owned specimen. It does not establish seller-lot reproducibility or characterize every similarly labelled breakout.

## Accepted decision

- **Standard indoor profile:** DHT11 for cost-optimized domestic rooms with slow, gradual environmental changes and broad comfort-oriented thresholds.
- **Precision / extended-environment profile:** BME280 for outdoor nodes, controlled rooms, wider excursions, tighter operational thresholds or finer observation requirements.
- **DHT22:** not selected because it added cost, produced two communication failures and did not establish a decisive profile advantage.
- **Procurement fallback:** BME280 may replace DHT11 when availability requires it and the increased cost is acceptable, but this is secondary to its specialized profile role.

The decision is canonical in [`ADR-0002`](../../adr/ADR-0002-environmental-sensor-profiles.md).

## Review boundary

The evidence supports relative stability, completeness, latency, response estimates, aggregate disagreement and tested specimen identity. It does not establish:

- absolute accuracy or calibration;
- universal behavior for every unit in each sensor family;
- final enclosure or placement fitness;
- quantitative power-system capability;
- pressure-channel requirements;
- production, precision, medical, safety or certification maturity.

Placement and enclosure exposure remains active under [`R-011`](../../risks/records/R-011-environmental-sensor-placement-bias.md) with `RT-R011-01` in `Proposed` state.
