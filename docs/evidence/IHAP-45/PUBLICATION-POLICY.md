# IHAP-45 Summary-Only Evidence Publication Policy

## Purpose

IHAP-45 must be reviewable without publishing raw hardware telemetry. The repository therefore exposes the test protocol, acceptance rules, failures, corrective actions and aggregate outcomes while retaining reproducible acquisition streams only on the Project Owner's workstation.

## Data classification

| Class | Examples | Repository policy |
|---|---|---|
| Public engineering method | wiring, commands, phase definitions, validators, source code | commit |
| Public aggregate evidence | pass/fail status, counts, completeness, aggregate statistics, pairwise deltas, response estimates, declared limitations | commit after review |
| Public aggregate visualization | self-contained HTML generated only from the reviewed public summary JSON | commit after review |
| Local reproducible telemetry | serial logs, individual samples, phase-marker streams, reference-observation streams, per-sample CSV, interactive reports embedding samples | do not commit |
| Potentially identifying workstation data | absolute paths, serial-port history, usernames, host metadata | do not commit |
| Visual evidence | photographs and screenshots | commit only after explicit sanitization and Project Owner review |

## Safety controls

1. `runs/` is ignored by Git.
2. `docs/evidence/IHAP-45/.gitignore` blocks common raw-evidence filenames, the original sample-embedding `report.html` and unsanitized HEIC files.
3. The summary publisher reads local runs but writes new files from an allow-list of aggregate fields.
4. The aggregate HTML publisher reads only an already-generated public `*.summary.json`; it does not read `runs/`, JSONL, serial logs or per-sample CSV files.
5. Publishers do not copy source files and do not embed raw JSONL lines.
6. Validation errors and warnings are preserved in published summaries.
7. A failed run may be summarized for transparency but cannot be presented as accepted evidence.
8. Raw evidence is not required to remain indefinitely; the Project Owner controls local retention.

## Reproducibility model

Reproduction relies on the committed firmware, host tools, test plan and instructions. An independent operator can execute the same protocol and generate a new local run. Repository summaries demonstrate what the Project Owner observed without turning the original raw stream into a permanent public artefact.

The public HTML is a presentation layer over the companion JSON summary. Reviewers must treat the JSON summary as the machine-readable source for the HTML and can regenerate the page deterministically with the committed publisher.

## Admissible environmental summary fields

The generated environmental summary and aggregate-only HTML may include:

- run and plan identifiers;
- validation pass/fail status;
- errors and warnings;
- boot and probe counts;
- aggregate phase durations;
- sample counts, completeness and valid percentages;
- aggregate temperature and humidity statistics;
- aggregate read latency;
- aggregate pairwise differences;
- response-time estimates;
- aggregate reference metrics when an independent reference exists;
- explicit evidence boundaries and unsupported claims;
- charts derived exclusively from per-phase or whole-run aggregate values.

They must not include:

- individual samples;
- exact serial lines;
- host paths or serial-port identifiers;
- source timestamps for individual observations;
- raw reference observations;
- pressure measurements or pressure fields;
- embedded interactive plots containing the underlying sample stream;
- JavaScript datasets reconstructed from timestamped or batch-level observations.

## Required filenames

The original local report remains named `report.html` and is intentionally ignored. A publishable page must use the generated form:

```text
environmental-<run-id>.summary.html
```

and must be produced by:

```bash
python host/ihap45_publish_html.py \
  --summary ../../../docs/evidence/IHAP-45/summaries/environmental-<run-id>.summary.json
```

## Review requirement

Before committing generated evidence, the Project Owner must inspect the Markdown, JSON and aggregate-only HTML outputs, confirm that the status is accurate and verify with `git diff --cached` that no raw files are staged.
