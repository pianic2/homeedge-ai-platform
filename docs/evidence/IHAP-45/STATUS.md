# IHAP-45 Qualification Status

**Updated:** 2026-07-16  
**Decision state:** no final sensor selection  
**Current gate:** controlled environmental run passed; Project Owner decision pending

## Visible execution history

| Stage | Result | Evidence classification | What it established |
|---|---|---|---|
| Initial parallel preflight | `FAIL` | observed from local run; raw log retained locally | all three sensors produced valid concurrent samples, but startup metadata was missed by the first collector implementation |
| USB-resilient preflight | `FAIL` | observed from local run; raw log retained locally | collector survived ESP32-C3 native-USB reset, but one-shot boot/probe records were emitted before Linux re-enumeration completed |
| Delayed-start resilient preflight | `FAIL` | observed from local run; raw log retained locally | BME280 identity was captured as address `0x76`, chip ID `0x60`, humidity supported; a real brownout caused an unexpected reboot and correctly failed the gate |
| Staged functional-stability isolation | `PASS` reported by Project Owner | operator report; sanitized machine summaries may be exported locally | the staged follow-up configurations passed and the Project Owner authorized the full environmental run |
| Controlled environmental comparison `IHAP45-RUN-01` | `PASS` | reviewed sanitized Markdown and JSON summaries | the committed 12-phase protocol completed with one boot, one successful BME280 probe, 5,771 sample records and no validation errors |

Failed trials remain part of the engineering history. They are not hidden or rewritten as passes. Their raw acquisition files stay local; this page records their purpose, result and the corrective action taken.

## Corrective actions made visible

1. The host collector was changed to survive ESP32-C3 USB disconnect and re-enumeration.
2. Validation-harness startup was delayed so `harness_boot` and `sensor_probe` become observable after reset.
3. The preflight retained the multiple-boot failure rule and exposed the brownout rather than weakening acceptance criteria.
4. A staged functional-stability diagnostic was introduced to isolate board-only and incremental sensor configurations.
5. Repository evidence publication was restricted to generated aggregate summaries; raw telemetry remains ignored locally.
6. A self-contained aggregate-only HTML publisher was added so reviewers can inspect visual evidence without publishing the original Plotly per-sample payload.

## Qualified specimen identity

The owned purple module is qualified for this task as:

```text
sensor_id: BME280-OWNED-01
I2C address: 0x76
chip ID: 0x60
detected type: BME280
humidity supported: true
```

This claim applies only to the tested owned specimen. It does not establish seller-lot reproducibility or characterize every similarly labelled breakout.

## Controlled run result

| Check | Result |
|---|---:|
| Validation status | `PASSED` |
| Comparison scope | `relative_only` |
| Sample records | 5,771 |
| Boot records | 1 |
| Probe records | 1 |
| Independent reference observations | 0 |
| DHT11 valid samples | 1,923 / 1,923 — 100% |
| DHT22 valid samples | 1,922 / 1,924 — 99.90% |
| BME280 valid samples | 1,924 / 1,924 — 100% |
| DHT22 observed errors | 2 `NO_RESPONSE` |
| Validation errors | none |

Every required phase exceeded its minimum duration. No absolute-accuracy claim is supported because no independent reference observation was recorded.

## Review boundary

The successful run supports review of relative stability, completeness, latency, response estimates, aggregate disagreement and the tested specimen identity. It does not establish:

- absolute accuracy;
- calibration;
- universal behavior for every unit in each sensor family;
- final enclosure or placement fitness;
- quantitative power-system capability;
- pressure-channel requirements.

`PO-45-01` and `PO-45-02` remain open until the Project Owner reviews the sanitized environmental evidence and explicitly selects the MVP reference and fallback sensor.
