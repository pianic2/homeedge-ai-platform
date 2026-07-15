# IHAP-45 — Environmental Sensor Comparative Evidence

**Issue:** [IHAP-45](https://niccolopiazzi01.atlassian.net/browse/IHAP-45)  
**Evidence status:** preparation only; physical execution pending  
**Validation harness:** [`tools/hardware-validation/ihap-45-environmental-sensors/`](../../../tools/hardware-validation/ihap-45-environmental-sensors/)

This directory is the durable evidence destination for the parallel DHT11, DHT22 and owned BME/BMP280-breakout qualification.

At this preparation stage:

- test tooling is being prepared;
- no result is accepted;
- no sensor is selected as reference or fallback;
- the owned purple breakout remains an unidentified `BME/BMP280` candidate until chip-ID and humidity checks complete;
- pressure remains outside scope and is not emitted by the harness;
- physical execution, result files and sanitized photographs remain pending.

Expected evidence after the Project Owner executes the test:

```text
IHAP-45/
├── README.md
├── photos/
├── manifests/
├── raw/
│   ├── serial.log
│   ├── samples.jsonl
│   ├── markers.jsonl
│   ├── reference.jsonl
│   └── run-metadata.json
├── results/
│   ├── comparison.csv
│   ├── summary.json
│   └── report.html
└── checksums.sha256
```

## Claims currently supported

- the Project Owner owns three photographed breakout candidates visually compatible with DHT11, DHT22/AM2302 and a `BME/BMP280`-labelled board;
- a breadboard and an ESP32-C3 SuperMini-compatible board have been prepared for wiring;
- these observations concern the photographed specimens only.

## Claims not yet supported

- successful firmware build or flashing;
- safe electrical behavior of the breakout interfaces;
- BME280 identity;
- observed I2C address;
- working humidity acquisition from the purple board;
- relative or absolute sensor performance;
- calibration, accuracy, repeatability or placement fitness;
- production, precision, medical, safety or certification maturity.

All such claims remain `[UNVALIDATED]` until the corresponding evidence is committed and reviewed.
