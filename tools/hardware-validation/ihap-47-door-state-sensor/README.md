# IHAP-47 Door State Sensor Validation Harness

This tool captures repeatable raw electrical transitions from a passive wired door contact and turns the local session into structured evidence.

It is a **test harness**, not production room-node firmware.

## Scope

The harness supports:

- raw GPIO snapshots;
- bounded high-frequency transition capture;
- operator-labelled test sessions;
- local JSONL and serial-log capture;
- sanitized JSON summary generation;
- standalone HTML report generation.

It does not:

- decide the final sensor;
- distinguish door open from a disconnected wire;
- implement tamper detection;
- define the final GPIO, cable, connector or pull resistor;
- measure rail voltage, current or autonomy;
- validate mounting or enclosure;
- publish raw logs to GitHub.

## Directory Layout

```text
ihap-47-door-state-sensor/
├── README.md
├── requirements.txt
├── firmware/
│   ├── CMakeLists.txt
│   ├── sdkconfig.defaults
│   └── main/
│       ├── CMakeLists.txt
│       └── main.c
├── scripts/
│   ├── build_report.py
│   └── capture_serial.py
└── output/
    └── .gitignore
```

## Bench Wiring

Default test-only wiring:

```text
ESP32-C3 GPIO6 ---- passive contact ---- GND
```

The firmware enables the ESP32-C3 internal pull-up.

Expected electrical levels:

- open circuit -> `1`;
- closed circuit -> `0`.

GPIO6 is inherited from historical prototype evidence and is used only to make the protocol immediately executable. IHAP-50 owns the final pin mapping.

## Prerequisites

- ESP-IDF 6.x environment;
- Python 3.11 or newer;
- `pyserial` from `requirements.txt`;
- ESP32-C3 connected over USB;
- the physical protocol in `docs/evidence/IHAP-47/test-protocol.md`.

## Build and Flash

From `firmware/`:

```bash
idf.py set-target esp32c3
idf.py build
idf.py -p /dev/ttyACM0 flash
```

Use the actual serial port on your machine.

Do not run `idf.py monitor` at the same time as the capture script because only one process can own the serial port.

## Start Local Capture

From the harness root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/capture_serial.py \
  --port /dev/ttyACM0 \
  --baud 115200 \
  --output-root output
```

The script creates a timestamped local session directory.

## Console Commands

Commands sent to firmware:

```text
help
status
snapshot
begin <test_id> <specimen_id>
end
set-sample-us <250-10000>
```

Examples:

```text
snapshot
begin BOUNCE_OPEN_TO_CLOSED MC38-A
end
begin CYCLE_001 MC38-A
end
```

Local-only operator observations are entered into the capture script and are not sent to firmware:

```text
@observe {"specimen_id":"MC38-A","test":"continuity","magnet_position":"far","circuit":"open"}
@observe {"specimen_id":"MC38-A","test":"gap","direction":"pull_in","distance_mm":14.0,"resolution_mm":1.0}
```

The JSON object is appended to `operator-observations.jsonl` with a UTC timestamp.

Type `@quit` to end the local capture session cleanly.

## Firmware Record Model

Firmware emits one compact JSON object per line.

Record types:

- `boot`;
- `status`;
- `snapshot`;
- `capture_started`;
- `raw_transition`;
- `capture_ended`;
- `configuration_changed`;
- `error`.

The firmware reports `raw_level` and `circuit_state`. It does not report a sensor fault and does not claim the physical door state.

## Build the Report

After capture:

```bash
python scripts/build_report.py output/<session-id>
```

Generated files:

- `summary.json`;
- `report.html`.

The HTML is standalone and uses no external CDN.

## Publication Rule

The entire `output/` directory is ignored by Git.

Before publishing selected artifacts:

1. inspect `serial.log` and keep it local;
2. inspect `records.jsonl` and keep it local;
3. remove unique device identifiers and absolute paths;
4. copy only reviewed `summary.json` and `report.html` into `docs/evidence/IHAP-47/`;
5. add photographs only after EXIF removal and cropping;
6. update the evidence manifest with checksums and supported claims.

A generated report is not automatically accepted evidence. It becomes evidence only after source review and Project Owner approval.

## Expected Stop Point

This branch intentionally stops before physical execution.

The next action is the Project Owner running the protocol and returning:

- selected sanitized photographs;
- `summary.json`;
- `report.html`;
- a statement about any stop condition encountered.
