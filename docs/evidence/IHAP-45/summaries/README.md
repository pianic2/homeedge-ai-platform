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

Current state: the controlled environmental run `IHAP45-RUN-01` passed validation and its reviewed Markdown and JSON summaries are available for publication. The aggregate-only HTML presentation remains to be generated locally from that JSON summary.
