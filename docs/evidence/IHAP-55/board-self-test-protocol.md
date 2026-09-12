# IHAP-55 board self-test protocol

**Transport:** ESP32-C3 native USB Serial/JTAG, JSON Lines.  
**Schema:** `ihap55.board.v1`.

Request:

```json
{"cmd":"self_test","profile":"standard","schema":"ihap55.board.v1"}
```

Final firmware response must contain one terminal `board_self_test` record with: profile; booleans for USB console, health ADC, OLED, radar, door level, ADC/digital spare and service-TX-disabled; DHT11/BME280 profile checks; and rail readings `VBUS_IN`, `BATT`, `SYS_5V`, `SYS_3V3` from the TLA2024.

PRECISION requires BME280 at `0x76` with chip ID `0x60`; STANDARD requires DHT11.

Run:

```bash
python3 tools/hardware-validation/ihap-55-mainboard/host/ihap55_board_test.py \
  --port /dev/ttyACM0 --profile standard \
  --out docs/evidence/IHAP-55/runs/IHAP55-BOARD-01.json
```

The host fails closed. Programmatic ADC rail readings are diagnostic evidence only; Accepted power tests still require calibrated DMM/oscilloscope/load/thermal evidence for transient, load, transfer and thermal behavior.
