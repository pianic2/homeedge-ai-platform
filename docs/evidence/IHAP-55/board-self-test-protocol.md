# IHAP-55 board self-test protocol

**Transport:** ESP32-C3 native USB Serial/JTAG, JSON Lines.  
**Schema:** `ihap55.board.v1`.

Request:

```json
{"cmd":"self_test","profile":"standard","schema":"ihap55.board.v1"}
```

Final firmware response must contain one terminal `board_self_test` record with: profile; booleans for USB console, health ADC, OLED, radar, door level, ADC/digital spare and service-TX-disabled; DHT11/BME280 profile checks; and rail readings `VBUS_IN`, `BATT`, `SYS_5V`, `SYS_3V3` from the TLA2024.

The validation firmware accepts the documented three-field request in `cmd`, `profile`, `schema` order, with optional JSON whitespace. Malformed requests or extra fields produce `board_command_error`, never a passing `board_self_test`. The host evaluator requires the matching schema/profile, firmware `pass: true`, every required boolean, all four finite numeric rails and their diagnostic windows; missing readings fail closed.

PRECISION requires BME280 at `0x76` with chip ID `0x60`; STANDARD requires DHT11.

Run:

```bash
python3 tools/hardware-validation/ihap-55-mainboard/host/ihap55_board_test.py \
  --port /dev/ttyACM0 --profile standard \
  --out docs/evidence/IHAP-55/runs/IHAP55-BOARD-01.json
```

The host fails closed. Programmatic ADC rail readings are diagnostic evidence only; Accepted power tests still require calibrated DMM/oscilloscope/load/thermal evidence for transient, load, transfer and thermal behavior.

`IHAP55-BOARD-01` is a **future physical gate**: use only a fabricated and approved board with verified connector and battery polarity, flash the built `ihap55_mainboard_harness.bin` over native USB, identify its new `/dev/ttyACM*` port after reset, run the command above for the installed STANDARD profile (or `--profile precision` for BME280), retain the JSON output, and separately execute calibrated voltage/load/transfer checks from ADR-0007. A firmware build alone does not complete this run.
