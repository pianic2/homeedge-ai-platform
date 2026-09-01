# IHAP-45 Controlled 115-Minute Environmental Runbook

## Gate status

The full run may begin only after the staged functional-stability gate has passed with the complete three-sensor configuration. The Project Owner reported that gate as passed.

Raw telemetry remains local under `runs/`. Only generated aggregate summaries are eligible for repository publication.

## Safety boundary

- Power the ESP32-C3 from one direct PC USB port without a hub.
- Keep the qualified 3.3 V wiring and common ground unchanged.
- Keep the ESP32-C3 outside the environmental enclosure when practical.
- Use separated sealed warm/cold masses and separated humidity/dry sources.
- Do not apply water, mist, steam, flame, a heat gun or direct hot/cold airflow.
- Stop immediately if condensation, unstable wiring, unexpected heating, brownout or repeated USB reset occurs.
- Do not describe the setup as a calibrated chamber unless independent calibration evidence exists.

## Before starting

```bash
cd tools/hardware-validation/ihap-45-environmental-sensors

git pull --ff-only origin test/ihap-45-environmental-sensor-validation
python -m unittest discover -s host/tests -v
```

Confirm that no other process owns the serial port:

```bash
fuser /dev/ttyACM0 || true
```

Do not run `idf.py monitor` during capture.

## Terminal 1 — resilient capture

Use a fresh run ID. The canonical first complete run is:

```bash
python host/ihap45_resilient.py capture \
  --port /dev/ttyACM0 \
  --run-id IHAP45-RUN-01 \
  --plan config/test-plan.json
```

After the collector prints `Connected`, press `RST` exactly once.

Do not start phase timing until the terminal shows all of the following:

```text
"record_type":"harness_boot"
"record_type":"sensor_probe"
"chip_id":"0x60"
"detected_type":"BME280"
"humidity_supported":true
"status":"OK"
```

and one complete batch containing DHT11, DHT22 and BME280 samples.

Hard stop conditions:

- `Brownout detector was triggered`;
- a second `harness_boot`;
- repeated USB reconnect after the first boot;
- missing or rejected BME280 probe;
- condensation or unsafe environmental manipulation;
- wiring movement or loss of sensor co-location that makes phases incomparable.

## Terminal 2 — interactive phase guide

```bash
python host/ihap45_phase_guide.py \
  --run-dir runs/IHAP45-RUN-01 \
  --plan config/test-plan.json
```

The guide requires explicit operator confirmation before each phase, writes the phase marker, and times the minimum duration.

| Phase | Minimum | Operator condition |
|---|---:|---|
| `warmup` | 15 min | stable room condition, undisturbed |
| `baseline` | 10 min | stable room baseline |
| `humidity_ramp_up` | 5 min | introduce separated humidity source |
| `humidity_high_plateau` | 10 min | maintain higher humidity without condensation |
| `humidity_recovery` | 10 min | remove humidity source and recover |
| `humidity_low_plateau` | 10 min | maintain separated lower-humidity condition |
| `humidity_final_recovery` | 10 min | remove dry source and recover |
| `temperature_ramp_up` | 5 min | introduce separated sealed warm mass |
| `temperature_high_plateau` | 10 min | maintain warmer condition |
| `temperature_recovery` | 10 min | remove warm mass and recover |
| `temperature_low_plateau` | 10 min | introduce separated sealed cold mass; watch for condensation |
| `final_recovery` | 10 min | remove cold mass and recover |

Minimum total timed duration: **115 minutes**.

The guide may take longer because the operator must safely establish each next condition before confirming it. Longer phases are acceptable; shorter phases are not.

## End of acquisition

After the guide reports completion, leave the final recovery condition stable for at least one additional complete sample batch. Then stop Terminal 1 with `Ctrl+C`.

Do not delete the local run even if validation fails. Failed runs are diagnostic evidence.

## Strict local gate

```bash
python host/ihap45_final_gate.py \
  --run-dir runs/IHAP45-RUN-01 \
  --plan config/test-plan.json
```

The gate requires:

- exactly one boot record;
- zero brownout messages;
- a successful BME280 `0x60` probe;
- every required phase and duration;
- minimum sample completeness and valid-record thresholds;
- no pressure fields.

Do not publish a failed run as accepted evidence.

## Local analysis

When the strict gate passes:

```bash
python host/ihap45.py analyze \
  --run-dir runs/IHAP45-RUN-01 \
  --plan config/test-plan.json
```

The generated CSV, JSON and interactive HTML remain inside the ignored `runs/` directory. They are for local analysis and Project Owner review only.

## Summary-only publication

Generate repository-safe summaries for every available stability run:

```bash
for run_id in \
  IHAP45-STABILITY-S1 \
  IHAP45-STABILITY-S2 \
  IHAP45-STABILITY-S3 \
  IHAP45-STABILITY-S4
do
  if [ -d "runs/$run_id" ]; then
    python host/ihap45_publish.py stability \
      --run-dir "runs/$run_id" \
      --output-dir ../../../docs/evidence/IHAP-45/summaries
  fi
done
```

Generate the environmental summary:

```bash
python host/ihap45_publish.py environmental \
  --run-dir runs/IHAP45-RUN-01 \
  --plan config/test-plan.json \
  --output-dir ../../../docs/evidence/IHAP-45/summaries
```

The publisher creates only:

```text
*.summary.json
*.summary.md
```

It does not copy serial logs, samples, phase streams, reference streams, per-sample CSV files, workstation paths or interactive reports.

## Mandatory review before commit

```bash
git status --short
git diff -- docs/evidence/IHAP-45
git check-ignore -v \
  runs/IHAP45-RUN-01/raw/serial.log \
  runs/IHAP45-RUN-01/raw/samples.jsonl
```

Stage only reviewed summary and documentation files:

```bash
git add docs/evidence/IHAP-45

git diff --cached --name-only
git diff --cached
```

The staged file list must not include `runs/`, `.log`, raw JSONL, `comparison.csv` or `report.html`.

## Decision boundary

Completion of this run does not automatically select the sensor. The Project Owner must review the sanitized results and decide `PO-45-01` and `PO-45-02` before the single ADR is drafted.
