# IHAP-45 Sanitized Summaries

This directory contains generated, reviewed aggregate evidence only.

Current files:

```text
stability-<run-id>.summary.json
stability-<run-id>.summary.md
environmental-IHAP45-RUN-01.summary.json
environmental-IHAP45-RUN-01.summary.md
environmental-IHAP45-RUN-01.summary.html
```

Markdown and JSON summaries are generated from local ignored runs with:

```bash
python host/ihap45_publish.py stability ...
python host/ihap45_publish.py environmental ...
```

The publishable visual page is generated only from the reviewed environmental JSON summary:

```bash
python host/ihap45_publish_html.py \
  --summary ../../../docs/evidence/IHAP-45/summaries/environmental-IHAP45-RUN-01.summary.json
```

The original local `report.html` must not be copied here because its Plotly payload embeds the per-sample series. Only `*.summary.html` produced by the aggregate HTML publisher is admissible.

No raw serial log, individual sample, phase stream, reference stream, per-sample CSV, workstation path or sample-embedding interactive report may be added here.

## Normalization provenance

The first publication of `IHAP45-RUN-01` exposed completeness values above 100%, showing that samples emitted before the operator reset had been retained before the first captured `harness_boot`.

The original local run was preserved. A non-destructive derived run was created with:

```bash
python host/ihap45_normalize_run.py \
  --source-run-dir runs/IHAP45-RUN-01 \
  --output-run-dir runs/IHAP45-RUN-01-NORMALIZED
```

The strict gate, analysis and publishers were rerun against the derived directory. The current committed environmental summaries report exactly 100% completeness for all three sensor streams, one boot, one successful BME280 probe and no validation errors.

## Review boundary

The summaries support relative specimen comparison only. No independent reference observations were recorded, so absolute accuracy and calibration remain `[UNVALIDATED]`.

The architecture decision is recorded separately in [`ADR-0002`](../../../adr/ADR-0002-environmental-sensor-profiles.md); this directory remains evidence, not a competing decision source.
