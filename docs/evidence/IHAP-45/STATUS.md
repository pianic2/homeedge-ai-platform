# IHAP-45 Qualification Status

**Updated:** 2026-07-15  
**Decision state:** no final sensor selection  
**Current gate:** ready for the controlled 115-minute environmental run

## Visible execution history

| Stage | Result | Evidence classification | What it established |
|---|---|---|---|
| Initial parallel preflight | `FAIL` | observed from local run; raw log retained locally | all three sensors produced valid concurrent samples, but startup metadata was missed by the first collector implementation |
| USB-resilient preflight | `FAIL` | observed from local run; raw log retained locally | collector survived ESP32-C3 native-USB reset, but one-shot boot/probe records were emitted before Linux re-enumeration completed |
| Delayed-start resilient preflight | `FAIL` | observed from local run; raw log retained locally | BME280 identity was captured as address `0x76`, chip ID `0x60`, humidity supported; a real brownout caused an unexpected reboot and correctly failed the gate |
| Staged functional-stability isolation | `PASS` reported by Project Owner | operator report; sanitized machine summaries pending export | the staged follow-up configurations passed and the Project Owner authorized the full environmental run |
| Controlled environmental comparison | `READY` | not yet executed | 12 required phases, 115 minutes minimum, temperature and humidity only |

Failed trials remain part of the engineering history. They are not hidden or rewritten as passes. Their raw acquisition files stay local; this page records their purpose, result and the corrective action taken.

## Corrective actions made visible

1. The host collector was changed to survive ESP32-C3 USB disconnect and re-enumeration.
2. Validation-harness startup was delayed so `harness_boot` and `sensor_probe` become observable after reset.
3. The preflight retained the multiple-boot failure rule and exposed the brownout rather than weakening acceptance criteria.
4. A staged functional-stability diagnostic was introduced to isolate board-only and incremental sensor configurations.
5. Repository evidence publication was restricted to generated aggregate summaries; raw telemetry remains ignored locally.

## Qualified specimen identity

The owned purple module is now qualified for this task as:

```text
sensor_id: BME280-OWNED-01
I2C address: 0x76
chip ID: 0x60
detected type: BME280
humidity supported: true
```

This claim applies only to the tested owned specimen. It does not establish seller-lot reproducibility or characterize every similarly labelled breakout.

## Full-run acceptance boundary

The controlled run is acceptable only when:

- exactly one post-reset `harness_boot` is present;
- the successful BME280 probe is present;
- all required phases meet their minimum durations;
- each sensor meets minimum valid-sample and completeness thresholds;
- no pressure field is present;
- no unexpected reset or brownout occurs;
- the report clearly states whether comparison is relative-only or includes an independent reference.

`PO-45-01` and `PO-45-02` remain open until the sanitized environmental summary is reviewed by the Project Owner.
