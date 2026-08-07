# IHAP-53 Local Display Validation Harness

This directory contains the minimal ESP-IDF harness used to validate the owned 0.96-inch display candidate for IHAP-53.

It is **validation tooling**, not final room-node firmware and not the final IHAP-50 pinout.

The harness:

1. probes `0x3C` and `0x3D` on I2C;
2. requires exactly one candidate address;
3. applies an SSD1306 128×64 initialization profile;
4. renders full-on, full-off and checkerboard frames;
5. renders a static `HOMEEDGE` / `IHAP53` text card;
6. enters a five-second heartbeat/update loop for the one-hour stability gate;
7. emits structured serial records for review.

Canonical wiring, operator steps, acceptance criteria and evidence rules are in:

[`docs/evidence/IHAP-53/README.md`](../../../docs/evidence/IHAP-53/README.md)

Build and run:

```bash
cd tools/hardware-validation/ihap-53-local-display/firmware
idf.py set-target esp32c3
idf.py build
idf.py -p /dev/ttyACM0 flash monitor
```

Use the actual serial port when it differs from `/dev/ttyACM0`.
