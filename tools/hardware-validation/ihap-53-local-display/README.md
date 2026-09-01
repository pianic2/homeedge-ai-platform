# IHAP-53 Local Display Validation Harness

This directory contains the minimal ESP-IDF harness used to validate the owned 0.96-inch display candidate for IHAP-53.

It is **validation tooling**, not final room-node firmware and not the final IHAP-50 pinout.

## Human execution entrypoint

Do not execute a physical IHAP-53 run from abbreviated commands in this file.

The complete canonical procedure, including required hardware/software, exact checkout, wiring, ESP-IDF reference version, build/flash, serial-log capture, run IDs, visual observations, 60-minute gate, controlled reboot, evidence filenames and stop conditions is:

[`docs/evidence/IHAP-53/README.md`](../../../docs/evidence/IHAP-53/README.md)

After a run is reviewed, the exact raw-to-published evidence promotion flow is:

[`docs/evidence/IHAP-53/publication-guide.md`](../../../docs/evidence/IHAP-53/publication-guide.md)

The per-run record template is:

[`run-record-template.md`](run-record-template.md)

Raw attempts are stored locally under:

```text
runs/<RUN-ID>/
```

The `runs/` directory is ignored by Git except for its `.gitignore`; raw runs must not be committed by default. Do not remove the ignore rule and do not force-add raw run files.

## Harness behavior

The harness:

1. probes `0x3C` and `0x3D` on I2C;
2. requires exactly one candidate address;
3. applies an SSD1306 128×64 initialization profile;
4. renders full-on, full-off and checkerboard frames;
5. renders a static `HOMEEDGE` / `IHAP53` text card;
6. enters a five-second heartbeat/update loop for the one-hour stability gate;
7. emits structured serial records for review.

## Firmware source

```text
firmware/main/main.c
```

Reference ESP-IDF for the controlled physical run: **v6.0.1**.

For developer-only build verification, after activating ESP-IDF:

```bash
cd tools/hardware-validation/ihap-53-local-display/firmware
idf.py set-target esp32c3
idf.py build
```

For a controlled physical run, return to the canonical evidence/runbook file above so evidence capture is not skipped.