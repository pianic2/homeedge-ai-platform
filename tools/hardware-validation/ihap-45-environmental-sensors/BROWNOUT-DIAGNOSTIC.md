# IHAP-45 Functional Brownout Isolation

This procedure isolates the functional reset observed while the three owned environmental sensors were running in parallel.

It does **not** characterize current draw, rail voltage, regulator capacity or autonomy. Quantitative power work remains outside IHAP-45. The only gate here is whether the ESP32-C3 validation setup can complete a fixed interval without a brownout, unexpected USB disconnect or reboot.

## Observed trigger

The initial resilient preflight captured:

- one valid `harness_boot`;
- one successful BME280 probe at I2C address `0x76`, chip ID `0x60`;
- valid DHT11, DHT22 and BME280 samples;
- `Brownout detector was triggered` after approximately 50 seconds;
- USB disconnect/re-enumeration;
- a second `harness_boot`.

This is a blocking functional-stability failure. The preflight validator must not be weakened to accept it.

## Before each run

1. Stop every serial monitor, `idf.py monitor`, terminal program or previous capture process.
2. Use one PC USB port directly, without a hub.
3. Keep the same USB cable for all staged runs.
4. Verify that no jumper bridges `5V` and `3.3V`.
5. Verify one common ground and firm breadboard contacts.
6. Do not change more than one hardware variable between runs.
7. Use a new run ID every time.

## Diagnostic command

After the command prints `Connected`, press `RST` exactly once. The five-minute qualification window starts only when the first `harness_boot` is captured.

```bash
python host/ihap45_stability.py \
  --port /dev/ttyACM0 \
  --label "CONFIGURATION_LABEL" \
  --run-id "RUN_ID" \
  --duration-seconds 300
```

A passing run requires:

- exactly one `harness_boot` after the operator reset;
- zero `Brownout detector was triggered` lines;
- zero USB disconnects after the qualification window starts;
- the complete five-minute window.

The diagnostic may warn about missing sensor samples during board-only isolation; that warning is expected and does not fail the board-only run.

## Isolation sequence

Run in this order and stop at the first failure.

### S1 — Board only

Disconnect VCC, GND and signal wires from all three sensor modules. Leave only the ESP32-C3 connected to the PC.

```bash
python host/ihap45_stability.py \
  --port /dev/ttyACM0 \
  --label "S1-board-only" \
  --run-id IHAP45-STABILITY-S1 \
  --duration-seconds 300
```

Interpretation:

- failure: suspect USB cable/port, ESP32-C3 board, breadboard contact or board power path;
- pass: reconnect the BME280 and continue.

### S2 — Board plus BME280

Connect only BME280 `VIN`, `GND`, `SDA` and `SCL` using the qualified 3.3 V wiring.

```bash
python host/ihap45_stability.py \
  --port /dev/ttyACM0 \
  --label "S2-board-bme280" \
  --run-id IHAP45-STABILITY-S2 \
  --duration-seconds 300
```

### S3 — Board plus BME280 and DHT22

Add DHT22 power, ground and data. Keep DHT11 disconnected.

```bash
python host/ihap45_stability.py \
  --port /dev/ttyACM0 \
  --label "S3-board-bme280-dht22" \
  --run-id IHAP45-STABILITY-S3 \
  --duration-seconds 300
```

### S4 — All three sensors

Reconnect the DHT11 and restore the full validation harness.

```bash
python host/ihap45_stability.py \
  --port /dev/ttyACM0 \
  --label "S4-all-three-sensors" \
  --run-id IHAP45-STABILITY-S4 \
  --duration-seconds 300
```

## Evidence generated

Each run contains:

```text
runs/<RUN_ID>/
├── raw/
│   ├── serial.log
│   └── samples.jsonl
├── run-metadata.json
└── stability-summary.json
```

Preserve failed runs. They are diagnostic evidence, not disposable output.

## Full-test gate

Do not start `IHAP45-RUN-01` or any controlled temperature/humidity phase until S4 passes for the full five-minute interval. A longer integrated functional-stability check may then be required before the 115-minute environmental test.
