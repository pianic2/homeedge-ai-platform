# IHAP-45 — Environmental Sensor Comparative Evidence

**Issue:** [IHAP-45](https://niccolopiazzi01.atlassian.net/browse/IHAP-45)  
**Evidence status:** controlled environmental qualification passed; decision pending  
**Validation harness:** [`tools/hardware-validation/ihap-45-environmental-sensors/`](../../../tools/hardware-validation/ihap-45-environmental-sensors/)

This directory is the durable, public evidence index for the owned DHT11, DHT22 and BME280 comparative qualification.

## Publication model

The repository publishes:

- the validation protocol and implementation;
- the visible history of failed trials and corrective actions;
- aggregate Markdown and JSON summaries;
- an optional self-contained aggregate-only HTML presentation;
- explicit limitations and unsupported claims.

The repository does not publish:

- serial logs;
- individual samples;
- phase-marker or reference-observation streams;
- per-sample CSV files;
- workstation paths or serial-port history;
- the original Plotly `report.html`, because it embeds the underlying sample series.

See [`PUBLICATION-POLICY.md`](PUBLICATION-POLICY.md) for the binding evidence-classification rules.

## Current evidence structure

```text
IHAP-45/
├── README.md
├── STATUS.md
├── PUBLICATION-POLICY.md
├── .gitignore
└── summaries/
    ├── README.md
    ├── stability-<run-id>.summary.json
    ├── stability-<run-id>.summary.md
    ├── environmental-IHAP45-RUN-01.summary.json
    ├── environmental-IHAP45-RUN-01.summary.md
    └── environmental-IHAP45-RUN-01.summary.html
```

Only files that actually exist after local generation and Project Owner review should be committed.

## Controlled run outcome

`IHAP45-RUN-01` passed the committed qualification protocol:

- plan: `IHAP45-QUALIFICATION-01`;
- comparison scope: `relative_only`;
- measurement channels: temperature and relative humidity only;
- sample records: 5,771;
- boot records: 1;
- probe records: 1;
- validation errors: none;
- independent reference observations: 0.

Validity by owned specimen:

| Sensor | Valid samples | Valid rate | Observed communication errors |
|---|---:|---:|---|
| `DHT11-OWNED-01` | 1,923 / 1,923 | 100% | none |
| `DHT22-OWNED-01` | 1,922 / 1,924 | 99.90% | 2 `NO_RESPONSE` |
| `BME280-OWNED-01` | 1,924 / 1,924 | 100% | none |

Every required phase exceeded its minimum duration.

## Qualified owned BME280

The owned purple breakout was directly identified during the accepted run as:

```text
sensor_id: BME280-OWNED-01
I2C address: 0x76
chip ID: 0x60
detected type: BME280
humidity supported: true
status: OK
```

This identity applies only to the tested specimen.

## Claims supported

The accepted evidence supports claims about:

- successful build, flash and execution of the validation harness on the tested ESP32-C3 setup;
- direct BME280 identification and humidity support for the owned purple module;
- parallel acquisition from the three owned sensors;
- observed sample completeness and communication errors;
- relative disagreement, stability, read latency and response estimates in the executed placement;
- completion of the controlled phase protocol without validation errors.

## Claims not supported

The evidence does not establish:

- absolute accuracy or calibration, because no independent reference was recorded;
- universal behavior of every DHT11, DHT22 or BME280 unit;
- seller-lot reproducibility;
- final enclosure or placement fitness;
- quantitative power consumption, regulator capability or autonomy;
- production, precision, medical, safety or certification maturity;
- any MVP pressure-channel requirement.

## Decision state

No final sensor selection is encoded in this evidence index. `PO-45-01` and `PO-45-02` remain open until the Project Owner reviews the sanitized comparative results and explicitly selects the reference and fallback sensor.
