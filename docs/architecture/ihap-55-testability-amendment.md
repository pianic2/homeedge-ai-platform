# IHAP-55 — Testability Architecture Amendment

**Date:** 2026-09-12  
**Status:** IN PROGRESS design amendment; does not supersede Accepted upstream ADRs

## Decision candidate

Revision A adds a dedicated board-health ADC, `TLA2024IRUGT` (`U6`), on the existing I2C bus.

Purpose: make the final PCB programmatically diagnosable over the ESP32-C3 native USB interface without consuming application GPIO or changing the product sensor/event contract.

Channels:

- AIN0: `VBUS_IN` through 47 kOhm / 47 kOhm divider;
- AIN1: `BATT` through 47 kOhm / 47 kOhm divider;
- AIN2: `SYS_5V` through 47 kOhm / 47 kOhm divider;
- AIN3: `SYS_3V3` through 47 kOhm / 47 kOhm divider.

`ADDR=GND` selects address `0x48`. U6 is powered by `SYS_3V3` and has local 100 nF decoupling.

## Software observability contract

Native USB Serial/JTAG becomes the reference bring-up/test transport. A host command requests a structured self-test; firmware checks the existing IHAP-50 hardware contract and reports TLA2024 rail readings.

The programmatic path covers boot/USB, board-health ADC, OLED, DHT11/BME280 profile, LD2410C receive path, MC-38 door state, spare pins and service-TX-disabled state.

## Boundary

U6 is engineering observability infrastructure, not a new environmental/presence/product sensor and does not create a new user-facing data contract. Rail telemetry used during validation is diagnostic data.

On-board ADC readings cannot prove load-step transients, source-transfer waveform quality, absolute measurement accuracy, thermal behavior, RF behavior or battery safety. Accepted external instrumentation and fabricated-board validation remain mandatory.

No procurement or fabrication is authorized by this amendment.
