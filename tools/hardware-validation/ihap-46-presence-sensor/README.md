# IHAP-46 — Presence Sensor Physical Validation

This package executes reproducible physical tests on the owned LD2410C specimen and, when an identified PIR specimen is available, performs a controlled comparison.

The test does not rely on an informal observation that the sensor “seems to work.” Every run records the physical specimen, room geometry, mounting position, operator action, duration, ground truth, received data, reset history, and invalidating events.

The guided runtime prints the required action on screen, creates ground-truth markers automatically, and generates the evidence package.

<!--
AI_AGENT_METADATA:
  issue: IHAP-46
  artifact_role: reproducible_physical_test_harness
  human_entrypoint: README.md
  detailed_human_procedure: docs/operator-test-procedure.md
  runtime_entrypoint: host/guided_run.py
  numerical_test_plan: config/test-plan.json
  operator_action_source: config/operator-actions.json
  default_environment_source: config/default-environment.json
  physical_specimen_evidence: ../../../docs/evidence/IHAP-46/README.md
  raw_runs_default_location: runs/
  production_event_boundary: presence_detected_boolean_only
  detailed_radar_fields: laboratory_evidence_only
  decisions_allowed_here: none

HIDDEN_AGENT_RULES:
  - Do not treat harness creation or one successful run as sensor acceptance.
  - Do not create or accept an ADR from raw observations without Project Owner decision.
  - Do not move detailed radar telemetry into the MVP event contract.
  - Do not commit raw runs by default; publish only reviewed, sanitized evidence.
  - New practical risks remain observations until the Project Owner approves risk-record work.
  - IHAP-49 owns quantitative power evidence.
  - IHAP-50 owns final wiring.
  - IHAP-51 owns enclosure and production placement constraints.
-->

## Owned LD2410C specimen

The Project Owner supplied component-side and antenna-side photographs of one owned specimen.

The visible markings identify:

- module label `HLK-LD2410C`;
- PCB revision `V1.1`;
- antenna-side pin labels `TX`, `RX`, `OUT`, `GND`, `VCC`.

The sanitized photographs, provenance, checksums, supported observations, and limitations are recorded in [`docs/evidence/IHAP-46/`](../../../docs/evidence/IHAP-46/README.md).

The photographs identify the physical labels of this specimen. They do not validate signal voltage, power behavior, UART operation, detection quality, or suitability for the MVP.

## Default physical environment

The default experiment profile is stored in [`config/default-environment.json`](config/default-environment.json).

It defines:

- square room: **5.00 m × 5.00 m**;
- door: **near one corner** of the mounting wall;
- sensor height: **2.00 m above the floor**;
- sensor position: **attached to the wall immediately above the door opening**;
- sensor orientation: **board parallel to the wall, antenna side facing into the room**.

The runtime displays these values before the run. Pressing Enter accepts a default. Typing another value records a correction in the evidence.

The profile also defines relative reference points:

- 1.00 m inside the doorway on the sensor centreline;
- geometric room centre;
- 0.50 m from the wall opposite the door on the sensor centreline;
- a lateral path through the room centre;
- a fixed seated point at the room centre unless corrected.

Exact door width, offset from the nearest corner, ceiling height, furniture layout, adjacent-space geometry, and moving objects remain run-specific and must be corrected in the metadata when known.

## Breadboard wiring for the first validation

Disconnect USB power before changing the wiring.

Use the labels printed on the photographed antenna side to identify the pins. The initial validation uses receive-only UART:

```text
LD2410C VCC -> ESP32-C3 5 V
LD2410C GND -> ESP32-C3 GND
LD2410C TX  -> ESP32-C3 GPIO5
```

Do not connect these pins during the first run:

```text
ESP32-C3 TX -> LD2410C RX
LD2410C OUT -> ESP32-C3 GPIO
PIR OUT     -> ESP32-C3 GPIO
```

The shared ground is mandatory. The photographed pin labels do not establish logic-level safety. RX, OUT, and PIR paths remain disabled until their levels are verified.

## Clone the pull request

```bash
git clone https://github.com/pianic2/homeedge-ai-platform.git
cd homeedge-ai-platform
git fetch origin pull/25/head:ihap-46-validation
git switch ihap-46-validation
cd tools/hardware-validation/ihap-46-presence-sensor
```

Confirm the checked-out commit before testing:

```bash
git status
git rev-parse HEAD
```

Record the commit SHA with the run evidence.

## Build and flash the firmware

Use ESP-IDF **6.0.1** for the reference run. A different ESP-IDF 6.x version is a test deviation and must be recorded.

Activate ESP-IDF, then run:

```bash
cd firmware
idf.py set-target esp32c3
idf.py menuconfig
idf.py build
idf.py -p /dev/ttyACM0 flash
cd ..
```

The default firmware configuration reads LD2410C UART on ESP32-C3 GPIO5 at 256000 baud and emits newline-delimited JSON on the USB serial console at 115200 baud.

## Prepare the host runtime

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r host/requirements.txt
python -m unittest discover -s tests -v
```

Preview the default environment and operator actions without opening the serial port:

```bash
python host/guided_run.py --dry-run
```

Preview only the initial smoke scenarios:

```bash
python host/guided_run.py \
  --dry-run \
  --scenario ROOM_EMPTY_BASELINE \
  --scenario ENTER_ROOM \
  --scenario SEATED_STILL \
  --scenario EXIT_CLEAR
```

## Execute the first real smoke run

Mount the sensor in the documented default position before starting the room scenarios.

```bash
python host/guided_run.py \
  --port /dev/ttyACM0 \
  --run-id IHAP46-LD2410C-SMOKE-01 \
  --sensor ld2410c_uart \
  --scenario ROOM_EMPTY_BASELINE \
  --scenario ENTER_ROOM \
  --scenario SEATED_STILL \
  --scenario EXIT_CLEAR
```

The runtime:

1. displays the default room and mounting profile;
2. accepts or corrects the effective values;
3. records operator, sensor, board, and room identifiers;
4. starts the reset-tolerant serial collector;
5. requires a valid firmware and UART pre-flight;
6. prints the exact action for each repetition;
7. waits for operator readiness;
8. starts a five-second countdown;
9. records scenario start and end automatically;
10. repeats the current action and remaining time on screen;
11. records anomaly notes;
12. generates machine-readable results and a human-readable report.

A second terminal is not required.

## Override defaults

Each value can be changed interactively or on the command line:

```bash
python host/guided_run.py \
  --port /dev/ttyACM0 \
  --run-id IHAP46-LD2410C-CORRECTED-01 \
  --sensor ld2410c_uart \
  --room-width-m 4.80 \
  --room-depth-m 5.10 \
  --door-location "0.40 m from the west corner" \
  --mount-height-cm 198 \
  --mount-position "wall-mounted 5 cm above the door frame" \
  --mount-orientation "board parallel to wall, antenna side facing into room"
```

A separate environment file can be selected with:

```bash
--environment path/to/environment.json
```

Every effective value is saved with the run.

## Execute the complete required matrix

After the smoke run has valid evidence and no blocking electrical or firmware defect:

```bash
python host/guided_run.py \
  --port /dev/ttyACM0 \
  --run-id IHAP46-LD2410C-FULL-01 \
  --sensor ld2410c_uart
```

Optional boundary and interference scenarios are added with:

```bash
--include-optional
```

The digital-output consistency scenario requires both:

```bash
--sensor ld2410c_uart
--sensor ld2410c_out
```

Do not enable `ld2410c_out` until the output logic level is verified.

## Evidence produced by each run

Each run is stored under `runs/<RUN-ID>/`:

```text
run.json                    operator, specimens, environment, and snapshots
effective-environment.json  exact room, door, mounting, and reference points
effective-test-plan.json    exact scenarios, repetitions, and thresholds
serial.log                  complete console stream
records.jsonl               parsed device records with host timestamps
marks.jsonl                 automatic ground truth and operator annotations
capture-events.jsonl        serial connection, reset, and reconnection history
results.json                machine-readable evaluation
report.html                 self-contained human-readable report
```

Do not edit a completed run. Execute a new run ID after any correction, wiring change, firmware change, mounting change, or invalid attempt.

Raw logs remain local by default. Repository evidence contains reviewed manifests, sanitized images, aggregated results, graphs, limitations, and traceability to the exact commit.

## Practical risk discovery

Physical validation may expose risks that are not visible from datasheets or static review, including:

- incorrect or ambiguous physical pin interpretation;
- unstable breadboard or jumper connections;
- reset or USB re-enumeration failures;
- false presence from the corridor, open door, wall, curtain, or fan;
- missed substantially stationary presence;
- excessive clear latency after exit;
- inconsistent UART and digital-output behavior;
- sensitivity to mounting height, orientation, furniture, or room geometry;
- configuration loss after reboot;
- unexplained invalid frames or data gaps.

Record each observation in the run annotations and report. An observation becomes a proposed project risk only after review against the existing risk catalogue and explicit Project Owner authorization.

## Boundaries

This package does not:

- select LD2410C or PIR;
- accept an ADR;
- validate quantitative power behavior;
- freeze production wiring or enclosure design;
- change the production event contract;
- authorize identity, tracking, behavioral history, alarm, intrusion-detection, safety, or security-grade claims.

The production semantic remains the local non-identifying boolean `presence_detected` state `[UNVALIDATED]`.
