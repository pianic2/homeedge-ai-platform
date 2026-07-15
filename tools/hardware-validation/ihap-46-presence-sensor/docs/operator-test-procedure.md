# Reproducible Operator Procedure — IHAP-46

## Objective

This procedure enables another operator to repeat the same physical test on the documented LD2410C specimen or on a separately identified comparison specimen.

A usable run preserves both device data and the context required to interpret it: specimen identity, room geometry, door position, sensor mounting, operator action, duration, repetition, ground truth, and anomalies.

## 1. Identify the physical specimens

Assign stable identifiers before flashing:

- presence sensor, for example `LD2410C-HLK-V1.1-OWNED-01`;
- ESP32-C3 board, for example `ESP32C3-SM-OWNED-01`;
- room, default `ROOM-5X5-DOOR-CORNER-01`;
- PIR comparison specimen, when used.

The owned LD2410C photographs are registered in [`docs/evidence/IHAP-46/`](../../../../docs/evidence/IHAP-46/README.md).

The photographs identify one visible `HLK-LD2410C` `V1.1` specimen and the labels `TX RX OUT GND VCC`. They do not validate voltage levels or runtime behavior.

## 2. Apply or correct the default environment

The reference profile is [`config/default-environment.json`](../config/default-environment.json).

Default geometry:

- room shape: square;
- room width: 5.00 m;
- room depth: 5.00 m;
- door: near one corner of the mounting wall;
- sensor height: 2.00 m above the floor;
- sensor position: wall-mounted immediately above the door opening;
- sensor orientation: board parallel to the wall, antenna side facing into the room.

Reference positions:

- door-inside point: 1.00 m inside the room on the sensor centreline;
- room centre: 2.50 m from each wall;
- far point: 0.50 m from the wall opposite the door on the sensor centreline;
- lateral path: through the room centre, 0.50 m from each side wall at its endpoints;
- seated point: room centre unless another fixed point is recorded.

Before the run, correct any known deviation:

- exact door width;
- exact door offset from the nearest corner;
- ceiling height;
- furniture layout;
- adjacent corridor or room geometry;
- curtains, fans, pets, robots, or other moving objects;
- sensor offset from the door frame;
- sensor tilt or rotation.

The effective values are saved in `effective-environment.json`.

## 3. Mount the sensor

Mount the sensor before executing room scenarios.

The reference mounting condition is:

1. attach the module to the wall immediately above the door;
2. set the sensor centre to 2.00 m above the floor;
3. keep the board plane parallel to the wall;
4. face the antenna side into the room;
5. prevent the board, breadboard, or jumper wires from moving during the run;
6. route wires so that door movement cannot pull the circuit.

Photograph the installed test assembly if the mounting is not already documented. Remove private or identifying background content before repository publication.

A mounting change requires a new run ID.

## 4. Wire the receive-only breadboard circuit

Disconnect USB power before wiring.

Identify the pin labels from the antenna side of the owned module:

```text
TX  RX  OUT  GND  VCC
```

Connect only:

```text
LD2410C VCC -> ESP32-C3 5 V
LD2410C GND -> ESP32-C3 GND
LD2410C TX  -> ESP32-C3 GPIO5
```

Leave disconnected:

```text
LD2410C RX
LD2410C OUT
PIR OUT
```

The first run does not require radar configuration writes or the digital output.

Before power-on, verify:

- VCC is not connected to a GPIO;
- GND is shared;
- module TX reaches ESP32-C3 GPIO5;
- no loose conductor bridges adjacent breadboard rows;
- the board is powered only through the intended PC USB connection.

## 5. Check out the exact pull request revision

```bash
git clone https://github.com/pianic2/homeedge-ai-platform.git
cd homeedge-ai-platform
git fetch origin pull/25/head:ihap-46-validation
git switch ihap-46-validation
git rev-parse HEAD
cd tools/hardware-validation/ihap-46-presence-sensor
```

Record the printed commit SHA.

## 6. Build and flash

Use ESP-IDF 6.0.1 for the reference run.

```bash
cd firmware
idf.py set-target esp32c3
idf.py menuconfig
idf.py build
idf.py -p /dev/ttyACM0 flash
cd ..
```

Do not change the default LD2410C GPIO or UART settings for the first run.

A build error, flash error, boot loop, or unexpected reset is evidence. Preserve the complete terminal output before making a correction.

## 7. Prepare and verify the host tools

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r host/requirements.txt
python -m unittest discover -s tests -v
python host/guided_run.py --dry-run
```

The preview must display:

- the 5.00 m × 5.00 m default room;
- door near one corner;
- 2.00 m wall mounting above the door;
- antenna side facing into the room;
- scenario purpose;
- operator setup;
- action during recording;
- duration and repetitions;
- invalidation conditions.

## 8. Execute the smoke run

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

Enter stable operator, sensor, and board IDs.

Press Enter to accept each physical default. Type a correction when the real setup differs.

The pre-flight requires:

- one parsed harness boot record;
- sample records;
- at least one fresh valid LD2410C UART frame.

Do not start a scenario action before the runtime countdown.

## 9. Rules during every scenario

- Execute one controlled action only.
- Keep mounting, wiring, firmware, furniture, and path unchanged.
- Reuse the same speed, endpoints, and posture across repetitions.
- Keep uninvolved people outside the controlled area.
- Record unintended movement, an opened door, power loss, reset, wire movement, or sensor movement.
- Treat the attempt as invalid when any listed invalidation condition occurs.
- Use a new run ID after any material configuration change.
- Do not edit generated evidence files.

## 10. Required operator actions

| Scenario | Operator action | Ground truth |
|---|---|---|
| `ROOM_EMPTY_BASELINE` | Leave the room and avoid the doorway and adjacent wall | Empty room |
| `ENTER_ROOM` | Enter at normal pace and reach the fixed door-inside point | Empty to occupied |
| `MOVING_LATERAL` | Walk between the fixed lateral endpoints | Moving person |
| `MOVING_APPROACH` | Walk between the far and near points | Moving person |
| `SEATED_STILL` | Remain seated without deliberate large movement | Substantially still person |
| `MICRO_MOVEMENT` | Type or turn pages while seated | Small human movement |
| `EXIT_CLEAR` | Leave, close the door, and remain away | Occupied to empty |
| `ADJACENT_DOOR_CLOSED` | Walk along the fixed external path with the door closed | Empty room, adjacent activity |
| `ADJACENT_DOOR_OPEN` | Walk outside without crossing the threshold | Empty room, open door |
| `WALL_MOVEMENT` | Walk behind one documented adjacent wall | Empty room, movement beyond wall |
| `NON_HUMAN_INTERFERENCE` | Activate one documented moving object | Empty room |
| `REBOOT_PERSISTENCE` | Perform one declared reset while continuing the action | Scenario-specific |
| `DIGITAL_UART_CONSISTENCY` | Alternate clearly occupied and empty periods | Alternating state |

The runtime reads the detailed instructions from `config/operator-actions.json` and prints them before every repetition.

## 11. Execution order

### Stage A — electrical and data path

- build;
- flash;
- pre-flight;
- `ROOM_EMPTY_BASELINE`;
- `ENTER_ROOM`;
- `EXIT_CLEAR`.

Stop and inspect evidence after any boot failure, invalid UART frame pattern, repeated disconnect, or unexplained reset.

### Stage B — presence behavior

- `MOVING_LATERAL`;
- `MOVING_APPROACH`;
- `SEATED_STILL`;
- `MICRO_MOVEMENT`.

### Stage C — room boundaries

- `ADJACENT_DOOR_CLOSED`;
- `ADJACENT_DOOR_OPEN`;
- `WALL_MOVEMENT`, when physically applicable.

### Stage D — robustness and interfaces

- `NON_HUMAN_INTERFERENCE`, when physically applicable;
- `REBOOT_PERSISTENCE`;
- `DIGITAL_UART_CONSISTENCY`, only after output-level verification.

## 12. Evidence acceptance gate

A run is usable as technical evidence only when:

- pre-flight passed;
- exact specimen IDs are present;
- room and mounting values are present;
- the effective environment file exists;
- every completed interval has automatic start and end markers;
- anomalies and invalid attempts are recorded;
- the exact test plan is stored;
- `results.json` and `report.html` are generated without manual data correction;
- the firmware commit SHA is recorded.

A run does not independently establish MVP suitability. The decision requires comparison across scenarios, repetitions, practical limitations, alternatives, and relevant risks.

## 13. Practical risk observations

Record practical findings without immediately creating new risk records.

Examples:

- a pin label is easy to misread after mounting;
- jumper movement causes intermittent frames;
- reset causes a serial-port change;
- corridor movement causes internal presence;
- a seated person is cleared too early;
- an empty room remains occupied too long;
- a wall or moving curtain creates false presence;
- the reference mounting position creates blind areas;
- firmware or sensor configuration is lost after reboot.

After the run, compare each observation with the existing risk catalogue, especially R-004. Create or modify a risk record only after explicit Project Owner authorization.

## 14. Repository evidence boundary

Raw run data remains local by default.

A reviewed repository evidence package may include:

- run manifest;
- effective environment;
- sanitized technical photographs;
- aggregate results;
- charts;
- observed limitations;
- practical risk candidates;
- exact firmware and test-plan commit.

Do not publish personal data, radio identifiers, detailed home layout beyond what is technically necessary, or unreviewed raw logs.
