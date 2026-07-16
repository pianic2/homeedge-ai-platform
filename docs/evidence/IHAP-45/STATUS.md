# IHAP-45 Qualification Status

**Updated:** 2026-07-16  
**Decision state:** no final sensor selection  
**Current gate:** controlled run completed; first-boot normalization and republication pending

## Visible execution history

| Stage | Result | Evidence classification | What it established |
|---|---|---|---|
| Initial parallel preflight | `FAIL` | observed from local run; raw log retained locally | all three sensors produced valid concurrent samples, but startup metadata was missed by the first collector implementation |
| USB-resilient preflight | `FAIL` | observed from local run; raw log retained locally | collector survived ESP32-C3 native-USB reset, but one-shot boot/probe records were emitted before Linux re-enumeration completed |
| Delayed-start resilient preflight | `FAIL` | observed from local run; raw log retained locally | BME280 identity was captured as address `0x76`, chip ID `0x60`, humidity supported; a real brownout caused an unexpected reboot and correctly failed the gate |
| Staged functional-stability isolation | `PASS` reported by Project Owner | operator report; sanitized machine summaries may be exported locally | the staged follow-up configurations passed and the Project Owner authorized the full environmental run |
| Controlled environmental comparison `IHAP45-RUN-01` | `PROVISIONAL PASS` | generated summaries require normalization and regeneration | all required phases completed with one captured boot and no validation errors, but pre-reset records caused impossible completeness values above 100% |

Failed trials and evidence-quality defects remain part of the engineering history. They are not hidden or rewritten as passes. Raw acquisition files stay local; this page records their purpose, result and corrective action.

## Corrective actions made visible

1. The host collector was changed to survive ESP32-C3 USB disconnect and re-enumeration.
2. Validation-harness startup was delayed so `harness_boot` and `sensor_probe` become observable after reset.
3. The preflight retained the multiple-boot failure rule and exposed the brownout rather than weakening acceptance criteria.
4. A staged functional-stability diagnostic was introduced to isolate board-only and incremental sensor configurations.
5. Repository evidence publication was restricted to generated aggregate summaries; raw telemetry remains ignored locally.
6. A self-contained aggregate-only HTML publisher was added so reviewers can inspect visual evidence without publishing the original Plotly per-sample payload.
7. A non-destructive normalizer was added after the first generated summary exposed pre-reset sample contamination through completeness values above 100%.

## Qualified specimen identity

The owned purple module is qualified for this task as:

```text
sensor_id: BME280-OWNED-01
I2C address: 0x76
chip ID: 0x60
detected type: BME280
humidity supported: true
```

This claim applies only to the tested specimen. It does not establish seller-lot reproducibility or characterize every similarly labelled breakout.

## Provisional controlled-run result

The first generated summary reported:

| Check | Provisional value |
|---|---:|
| Validation status | `PASSED` |
| Comparison scope | `relative_only` |
| Sample records | 5,771 |
| Boot records | 1 |
| Probe records | 1 |
| Independent reference observations | 0 |
| DHT11 valid samples | 1,923 / 1,923 |
| DHT22 valid samples | 1,922 / 1,924 |
| BME280 valid samples | 1,924 / 1,924 |
| Validation errors | none |

However, DHT22 and BME280 completeness were reported as `100.052%`. Completeness above 100% is invalid and indicates that the resilient collector retained one or more samples emitted by the already-running firmware before the operator reset and first captured `harness_boot`.

The original two-hour run remains preserved and does not need to be repeated. A derived local run must retain structured evidence and serial content from the first captured `harness_boot` onward. Validation, analysis and publication must then be rerun against that derived directory.

## Acceptance after normalization

The controlled run becomes accepted evidence only when the normalized derived run demonstrates:

- the first structured record is `harness_boot`;
- exactly one boot is present;
- no brownout occurs after that boot;
- the successful BME280 probe is retained;
- no duplicate sensor/batch record is present;
- all required phases still meet minimum durations;
- completeness is within `0..100%`;
- validation and the strict final gate pass;
- regenerated Markdown, JSON and aggregate-only HTML summaries are reviewed.

## Review boundary

The successful normalized run may support review of relative stability, completeness, latency, response estimates, aggregate disagreement and tested specimen identity. It will not establish:

- absolute accuracy;
- calibration;
- universal behavior for every unit in each sensor family;
- final enclosure or placement fitness;
- quantitative power-system capability;
- pressure-channel requirements.

`PO-45-01` and `PO-45-02` remain open until the normalized sanitized evidence is reviewed by the Project Owner.
