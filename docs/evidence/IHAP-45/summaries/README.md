# IHAP-45 Sanitized Summaries

This directory contains generated, aggregate evidence only.

Expected files:

```text
stability-<run-id>.summary.json
stability-<run-id>.summary.md
environmental-<run-id>.summary.json
environmental-<run-id>.summary.md
environmental-<run-id>.summary.html
```

Markdown and JSON summaries are generated from local ignored runs with:

```bash
python host/ihap45_publish.py stability ...
python host/ihap45_publish.py environmental ...
```

The publishable visual page is then generated only from the reviewed environmental JSON summary:

```bash
python host/ihap45_publish_html.py \
  --summary ../../../docs/evidence/IHAP-45/summaries/environmental-<run-id>.summary.json
```

The original local `report.html` must not be copied here because its Plotly payload embeds the per-sample series. Only `*.summary.html` produced by the aggregate HTML publisher is admissible.

No raw serial log, individual sample, phase stream, reference stream, per-sample CSV, workstation path or sample-embedding interactive report may be added here.

## Current normalization requirement

The first `IHAP45-RUN-01` summaries exposed completeness values above 100%, showing that pre-reset samples had been retained before the first captured `harness_boot`. Those files are provisional and must not be committed as accepted evidence.

Create a derived local run without altering the original:

```bash
python host/ihap45_normalize_run.py \
  --source-run-dir runs/IHAP45-RUN-01 \
  --output-run-dir runs/IHAP45-RUN-01-NORMALIZED
```

Then run the strict gate, analysis and publishers against `runs/IHAP45-RUN-01-NORMALIZED`. Replace the provisional Markdown and JSON files and generate the aggregate-only HTML from the regenerated JSON.
