# IHAP-45 Sanitized Summaries

This directory contains generated, aggregate evidence only.

Expected files:

```text
stability-<run-id>.summary.json
stability-<run-id>.summary.md
environmental-<run-id>.summary.json
environmental-<run-id>.summary.md
```

Files are generated from local ignored runs with:

```bash
python host/ihap45_publish.py stability ...
python host/ihap45_publish.py environmental ...
```

No raw serial log, individual sample, phase stream, reference stream, per-sample CSV, workstation path or interactive report may be added here.

Current state: staged stability trials are reported passed by the Project Owner; generated sanitized files are pending local export. The controlled environmental run is ready but not yet summarized.
