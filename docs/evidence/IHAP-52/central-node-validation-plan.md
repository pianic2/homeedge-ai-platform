# IHAP-52 — Central Node Validation Plan

## Goal

Produce reproducible evidence that the first Raspberry Pi 4 Model B specimen satisfies the accepted minimum hardware profile and can sustain a bounded synthetic central-node workload without obvious resource, Wi-Fi, storage or thermal blockers.

This validation does **not** certify the final HomeEdge application workload. Backend, database, container topology and AI runtime remain `[UNVALIDATED]`.

## Validation specimen

Expected first specimen:

- Raspberry Pi 4 Model B;
- 8 GB RAM physically installed;
- **32 GB A2 microSD** for the MVP reference storage configuration;
- **Raspberry Pi OS Lite 64-bit**;
- Wi-Fi enabled and connected to the local network;
- manufacturer-supported USB-C power supply, preferably official 15 W / 5.1 V 3 A class;
- enclosure/cooling configuration recorded exactly as tested.

The 8 GB specimen demonstrates compliance with the >=4 GB minimum but does not by itself prove identical workload headroom on a physical 4 GB board.

## OS installation prerequisite

Install the reference OS using Raspberry Pi's official instructions:

https://www.raspberrypi.com/documentation/computers/getting-started.html#install-an-operating-system

Use Raspberry Pi Imager and select **Raspberry Pi OS Lite (64-bit)**. For the headless setup, configure Wi-Fi and enable SSH before first boot. Raspberry Pi's official documentation recommends Lite for headless systems.

Alpine Linux remains an alternate candidate and is not used for the first acceptance run. Official Alpine Raspberry Pi guide:

https://wiki.alpinelinux.org/wiki/Raspberry_Pi

## Test principles

1. No Internet connectivity is required by the validation harness.
2. No private SSID/password/private IP/hostname/username is published.
3. No Docker, database or AI framework is installed by this test.
4. The harness uses Python standard-library functionality and Linux system files/commands only.
5. Raw evidence stays local until reviewed and sanitized.
6. A passing run supports only the declared hardware/OS validation envelope.

## Gate A — Hardware and OS identity

Pass when:

- architecture is `aarch64`, `arm64` or `x86_64`;
- at least 4 logical processors are visible;
- at least 4 GB physical RAM is reported;
- root storage corresponds to approximately a nominal 32 GB or larger device;
- at least one Wi-Fi interface exists and is operational;
- a Linux graphics/compute render device is exposed when available;
- Raspberry Pi model identity is recorded when available;
- OS release/architecture evidence matches the selected 64-bit reference image.

The harness cannot reliably prove that a Debian-family image is the Lite variant, so the exact Raspberry Pi Imager selection is recorded manually.

## Gate B — Power / undervoltage

On Raspberry Pi, record `vcgencmd get_throttled` before and after stress when available. Current undervoltage/throttling flags make the run unacceptable as clean power evidence. PSU model/rating is recorded manually.

## Gate C — Wi-Fi

Pass when a wireless interface is detected, is up and has a non-link-local IP address. Optional local reachability may be tested with `--wifi-host <authorized-local-address>`.

## Gate D — Storage smoke

Write a bounded temporary file, flush, read back, compare deterministic hashes and remove it. Default size: 128 MiB.

This checks basic functionality/integrity only. It does not prove microSD endurance or final retention sufficiency.

## Gate E — CPU / thermal stress

Default duration: 300 seconds. Use CPU-bound workers equal to detected logical CPU count and sample temperature, load and memory.

Pass criteria:

- no crash or forced reboot;
- no current undervoltage at end;
- no current thermal-throttling condition reported by Raspberry Pi firmware at end;
- thermal observations are retained for review;
- no out-of-memory condition is observed.

## Gate F — Memory/headroom observation

Record total/available memory before, during and after stress. Future backend/AI workloads must revalidate the 4 GB minimum if their measured footprint materially changes the envelope.

## Gate G — AI readiness

No AI runtime is installed. Record only CPU architecture/core count, RAM and graphics/render-device exposure. Outcome remains:

`future small-model AI workload and acceleration path: [UNVALIDATED]`

## Manual configuration record

| Field | Required |
|---|---|
| Board/model | Yes |
| RAM variant | Yes |
| Storage manufacturer/model/capacity | Yes |
| A2 marking confirmed | Yes |
| OS image | Raspberry Pi OS Lite 64-bit |
| Official install procedure followed | Yes |
| PSU manufacturer/model/rating | Yes |
| Case | Yes |
| Heatsinks installed | Yes/No |
| Fan installed | Yes/No |
| Ambient temperature estimate | Recommended |

## Command

```bash
python3 tools/hardware-validation/ihap-52-central-node/validate_central_node.py \
  --output-dir tools/hardware-validation/ihap-52-central-node/runs/pi4b-reference-01 \
  --stress-seconds 300 \
  --storage-mib 128
```

Expected outputs:

```text
tools/hardware-validation/ihap-52-central-node/runs/<run-id>/
├── validation.json
└── validation.md
```

The `runs/` directory is ignored by Git. Review and sanitize outputs before publication.

## Promotion rule

Only after a passing evidence review may Raspberry Pi 4 + Raspberry Pi OS Lite 64-bit be labelled `Community validated` / `Recommended reference` and ADR-0003 be considered for acceptance.
