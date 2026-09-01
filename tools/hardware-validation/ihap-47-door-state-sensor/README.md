# IHAP-47 Door State Sensor Validation Harness

This tool validates an owned passive wired magnetic contact for **binary electrical door-state telemetry only**.

It is a **test harness**, not production room-node firmware.

## Default workflow: low-touch guided run

The normal operator path is now intentionally simple:

1. connect the ESP32-C3 and contact;
2. start one command;
3. place the magnet FAR / NEAR when prompted;
4. during the cycle test, only move the magnet back and forth;
5. perform two explicit failure-mode setup changes;
6. keep the generated raw evidence locally.

No manual JSON entry is required.

From the harness root:

```bash
python scripts/guided_run.py \
  --port /dev/ttyACM0 \
  --specimen MC38-A
```

Default cycle count is 20 complete cycles. The runner:

- verifies FAR=`1` and NEAR=`0`;
- opens a bounded raw capture for every physical movement;
- waits for a stable target state automatically;
- counts complete cycles and mismatches;
- records raw transition counts at the firmware sampling resolution;
- records buffer overflow status;
- checks disconnected-conductor and GPIO-to-GND behavior;
- derives temporary internal-pull-up adequacy for the bench setup;
- writes `guided-result.json`;
- preserves `serial.log`, `records.jsonl`, and generated session metadata locally;
- invokes `build_report.py` after a successful run.

The operator should not type `snapshot`, `begin`, `end`, or `@observe` during the guided workflow.

## Scope

The harness supports:

- raw GPIO mapping;
- bounded high-frequency transition capture;
- automatic cycle counting;
- stable-state validation;
- disconnected-wire ambiguity observation;
- local raw evidence preservation;
- sanitized summary/report generation.

It does not:

- decide the final production GPIO;
- choose the final pull resistor;
- distinguish door open from a disconnected wire;
- implement tamper detection;
- validate mounting geometry;
- validate enclosure or cable routing;
- measure rail voltage, current or autonomy;
- make alarm, security or access-control claims.

## Responsibility split

IHAP-47 only decides whether the owned passive wired reed-contact technology is suitable for MVP binary telemetry.

- **IHAP-50** owns final GPIO, pull network, debounce and integrated electrical behavior.
- **IHAP-51** owns mounting geometry, operating gap, alignment margin and cable routing.
- **IHAP-49** owns power impact.
- **IHAP-17** owns final BOM registration.

Repeated millimetre-by-millimetre gap/alignment measurements are therefore not a blocking IHAP-47 gate.

## Directory layout

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
│   ├── guided_run.py
│   ├── build_report.py
│   └── capture_serial.py
└── output/
    └── .gitignore
```

## Bench wiring

```text
ESP32-C3 GPIO6 ---- passive contact ---- GND
```

The firmware enables the ESP32-C3 internal pull-up.

Expected electrical levels:

- open circuit -> `1`;
- closed circuit -> `0`.

GPIO6 is test-only. IHAP-50 owns the final pin mapping.

## Prerequisites

- ESP-IDF 6.x environment;
- Python 3.11 or newer;
- `pyserial` from `requirements.txt`;
- ESP32-C3 connected over USB;
- flashed IHAP-47 harness firmware.

## Build and flash

From `firmware/`:

```bash
idf.py set-target esp32c3
idf.py build
idf.py -p /dev/ttyACM0 flash
```

Use the actual serial port on the machine.

Do not run `idf.py monitor` while a host validation script owns the serial port.

## Guided run outputs

A guided session is created under:

```text
output/<session-id>/
```

It contains at least:

- `serial.log` — complete raw serial capture;
- `records.jsonl` — parsed firmware records;
- `operator-observations.jsonl` — observations written automatically by the runner;
- `session.json` — execution metadata;
- `guided-result.json` — machine-readable guided-run result;
- `summary.json` — generated sanitized summary after a successful run;
- `report.html` — standalone human-readable report after a successful run.

## Raw evidence rule

`output/` is ignored by Git.

Never commit raw `serial.log` or `records.jsonl`.

Before publishing selected evidence:

1. preserve the complete session directory locally;
2. inspect generated outputs;
3. remove unique identifiers, private paths and unrelated logs from publishable artifacts;
4. publish only reviewed evidence needed to support IHAP-47;
5. keep claims limited to the tested owned specimen and setup.

## Advanced/manual mode

`scripts/capture_serial.py` remains available for diagnostics and exceptional investigation.

It is **not** the default validation path and manual `@observe` JSON entry is not required for normal IHAP-47 execution.

Firmware commands remain available for troubleshooting:

```text
help
status
snapshot
begin <test_id> <specimen_id>
end
set-sample-us <250-10000>
```

## Decision boundary

A successful guided run can support these conclusions only:

- the tested owned specimen has repeatable FAR/NEAR electrical behavior;
- the temporary GPIO/pull-up bench topology reads the expected binary states;
- observed raw transition behavior is captured at the configured firmware sampling resolution;
- repeated stable movements complete without unexplained mismatch or buffer overflow;
- a disconnected conductor is electrically indistinguishable from an open contact in the simple two-wire topology.

It does **not** establish universal MC-38 behavior, production reliability, tamper detection, intrusion detection, alarm suitability or access-control suitability.
