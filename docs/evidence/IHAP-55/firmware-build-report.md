# IHAP-55 firmware build evidence — 2026-09-12

Input baseline HEAD `f5c94a2429f27e88161305896eb5fb85566dd636` plus the firmware changes now committed as `fc5a591`. Tool: ESP-IDF v6.0.1, target `esp32c3`, 4 MB flash setting, native USB Serial/JTAG console.

Commands executed in `tools/hardware-validation/ihap-55-mainboard/firmware/`:

```bash
source /home/optimus/.espressif/v6.0.1/esp-idf/export.sh
idf.py set-target esp32c3
idf.py build
```

Final `set-target` exit **0**; final `build` exit **0** after the strict command parser was added. Build output: `build/ihap55_mainboard_harness.bin`, 0x2f2b0 bytes, 82% free in the 1 MiB app partition. SHA-256: `ec8a64470fe3e4f7530396b94b21ac02013639e6a880701db5c58ea989aa0c10`. Generated build/sdkconfig are ignored by Git.

Reviewer rerun on 2026-09-13: `idf.py build` exit **0** with no source changes to firmware since `fc5a591`; the generated app descriptor identified the then-current worktree as `30569eb-dirty`, so the new binary hash is `f3b068ca9f683904bfab1e8e34f54803bccae7cb03ca96ffa9fda91e3df3671e` while size remains 0x2f2b0. Binary hashes are tied to the exact Git-derived app descriptor, not a stable firmware-source-only fingerprint.

The first build failed with `-Werror=misleading-indentation` in the pre-existing compact `health_adc.c`; it was reformatted and rebuilt successfully. IHAP-55 now initializes the TLA2024 on I2C, reads all four channels on command, includes rail validity in a terminal JSON `board_self_test`, preserves the IHAP-50 integrated sample stream, and serializes DHT access between tasks. Host evaluator tests passed 12/12 after fail-closed checks were tightened.

**PASS — firmware build only.** USB command reception, real ADC accuracy, sensor/connector function and GPIO electrical behavior on a fabricated mainboard remain `[UNVALIDATED]`. The firmware's rail thresholds are diagnostic, not calibrated proof of the accepted power contract.
