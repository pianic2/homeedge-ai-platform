# IHAP-45 — Environmental Sensor Comparative Evidence

**Issue:** [IHAP-45](https://niccolopiazzi01.atlassian.net/browse/IHAP-45)  
**Evidence status:** controlled run completed; normalized publication pending  
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

Only files produced after normalization, regeneration and Project Owner review are admissible.

## Controlled run state

`IHAP45-RUN-01` completed every required phase and its first generated summary reported:

- plan: `IHAP45-QUALIFICATION-01`;
- comparison scope: `relative_only`;
- measurement channels: temperature and relative humidity only;
- sample records: 5,771;
- boot records: 1;
- probe records: 1;
- validation errors: none;
- independent reference observations: 0.

The same summary also reported `100.052%` completeness for DHT22 and BME280. Completeness cannot exceed 100%. This exposed a collector-boundary defect: samples emitted by the already-running firmware before the operator reset were retained before the first captured `harness_boot`.

The original run remains preserved locally. It does not need to be repeated. A derived run must be created with `host/ihap45_normalize_run.py`, retaining only evidence from the first captured boot onward. Validation, analysis and publication are then rerun on the derived directory.

## Qualified owned BME280

The owned purple breakout was directly identified during the run as:

```text
sensor_id: BME280-OWNED-01
I2C address: 0x76
chip ID: 0x60
detected type: BME280
humidity supported: true
status: OK
```

This identity applies only to the tested specimen and is unaffected by removal of pre-reset samples because the probe follows the retained boot boundary.

## Claims currently supported

The evidence already supports:

- successful build, flash and execution of the validation harness on the tested ESP32-C3 setup;
- direct BME280 identification and humidity support for the owned purple module;
- completion of all controlled environmental phases;
- existence of sufficient local evidence to regenerate a normalized comparison without repeating the two-hour test;
- transparent detection and correction of an evidence-boundary defect.

## Claims pending normalized republication

The following aggregate claims remain provisional until regenerated summaries pass review:

- final sample counts and completeness;
- final whole-run and per-phase means;
- final pairwise differences;
- final response-time estimates;
- accepted relative stability and communication-error rates;
- final reference and fallback selection.

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

No final sensor selection is encoded in this evidence index. `PO-45-01` and `PO-45-02` remain open until the normalized comparative summaries and aggregate-only HTML are reviewed by the Project Owner.
