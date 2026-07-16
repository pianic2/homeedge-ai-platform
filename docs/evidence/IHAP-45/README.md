# IHAP-45 — Environmental Sensor Comparative Evidence

**Issue:** [IHAP-45](https://niccolopiazzi01.atlassian.net/browse/IHAP-45)  
**Evidence status:** normalized controlled run accepted; decision recorded in ADR-0002  
**Validation harness:** [`tools/hardware-validation/ihap-45-environmental-sensors/`](../../../tools/hardware-validation/ihap-45-environmental-sensors/)

This directory is the durable, public evidence index for the owned DHT11, DHT22 and BME280 comparative qualification.

## Publication model

The repository publishes:

- the validation protocol and implementation;
- the visible history of failed trials and corrective actions;
- reviewed aggregate Markdown and JSON summaries;
- a self-contained aggregate-only HTML presentation;
- explicit limitations, decision boundaries and unsupported claims.

The repository does not publish:

- serial logs;
- individual samples;
- phase-marker or reference-observation streams;
- per-sample CSV files;
- workstation paths or serial-port history;
- the original Plotly `report.html`, because it embeds the underlying sample series.

See [`PUBLICATION-POLICY.md`](PUBLICATION-POLICY.md) for the binding evidence-classification rules.

## Evidence structure

```text
IHAP-45/
├── README.md
├── STATUS.md
├── PUBLICATION-POLICY.md
├── .gitignore
└── summaries/
    ├── README.md
    ├── stability-*.summary.json
    ├── stability-*.summary.md
    ├── environmental-IHAP45-RUN-01.summary.json
    ├── environmental-IHAP45-RUN-01.summary.md
    └── environmental-IHAP45-RUN-01.summary.html
```

Only files produced after normalization, regeneration and Project Owner review are admissible.

## Accepted controlled run

The original `IHAP45-RUN-01` completed every required phase but its first publication exposed pre-reset contamination through completeness values above 100%. The original local run was preserved and a derived run retained structured and serial evidence from the first captured `harness_boot` onward.

The regenerated publication reports:

- plan: `IHAP45-QUALIFICATION-01`;
- comparison scope: `relative_only`;
- measurement channels: temperature and relative humidity only;
- sample records: 5,769;
- boot records: 1;
- probe records: 1;
- validation errors: none;
- independent reference observations: 0;
- DHT11: 1,923/1,923 valid, 100% completeness;
- DHT22: 1,921/1,923 valid, 100% completeness, two `NO_RESPONSE` errors;
- BME280: 1,923/1,923 valid, 100% completeness.

The evidence is available as:

- [human-readable summary](summaries/environmental-IHAP45-RUN-01.summary.md);
- [machine-readable aggregate summary](summaries/environmental-IHAP45-RUN-01.summary.json);
- [aggregate-only visual report](summaries/environmental-IHAP45-RUN-01.summary.html).

## Qualified owned BME280

The owned purple breakout was directly identified as:

```text
sensor_id: BME280-OWNED-01
I2C address: 0x76
chip ID: 0x60
detected type: BME280
humidity supported: true
status: OK
```

This identity applies only to the tested specimen.

## Supported decision claims

The evidence and Project Owner review support:

- DHT11 as the default standard-indoor profile for cost-optimized domestic room nodes with slow, gradual changes;
- BME280 as the precision and extended-environment profile for outdoor nodes, controlled rooms, wider excursions or tighter operational thresholds;
- BME280 as an optional procurement fallback when DHT11 is unavailable and increased cost is acceptable;
- DHT22 not selected because it added cost, produced two communication failures and did not establish a decisive profile advantage;
- broad thresholds, filtering and hysteresis for DHT11-based room automation;
- temperature and relative humidity as the only accepted measurement channels for this decision.

The canonical decision is [`ADR-0002`](../../adr/ADR-0002-environmental-sensor-profiles.md).

## Claims not supported

The evidence does not establish:

- absolute accuracy or calibration, because no independent reference was recorded;
- universal behavior of every DHT11, DHT22 or BME280 unit;
- seller-lot reproducibility;
- final enclosure or placement fitness;
- quantitative power consumption, regulator capability or autonomy;
- production, precision, medical, safety or certification maturity;
- any MVP pressure-channel requirement.

Placement and enclosure effects remain active under [`R-011`](../../risks/records/R-011-environmental-sensor-placement-bias.md). The proposed treatment is not implemented or verified by this evidence package.
