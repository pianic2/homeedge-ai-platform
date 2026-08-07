# IHAP-52 Central Node Hardware Validation Harness

## Scope

This harness collects reproducible hardware/resource evidence for the HomeEdge central-node profile without installing Docker, a database or an AI framework.

First reference configuration:

- Raspberry Pi 4 Model B;
- >=4 GB RAM;
- **32 GB A2 microSD**;
- **Raspberry Pi OS Lite 64-bit**;
- Wi-Fi required;
- Ethernet optional;
- heatsinks/fan optional but recommended.

It validates only a bounded hardware smoke-test envelope: architecture, CPU concurrency, RAM, local storage, Wi-Fi, graphics/render exposure, Raspberry Pi throttling/temperature observations and bounded CPU stress.

It does **not** prove final application performance, microSD endurance or AI acceleration.

## Install the reference OS first

Use Raspberry Pi's official installation documentation:

https://www.raspberrypi.com/documentation/computers/getting-started.html#install-an-operating-system

Use Raspberry Pi Imager, choose **Raspberry Pi OS Lite (64-bit)**, configure Wi-Fi and enable SSH for headless access before first boot.

Raspberry Pi officially recommends Raspberry Pi OS Lite for headless setups. Alpine Linux remains a compatible future candidate and has separate official installation guidance:

https://wiki.alpinelinux.org/wiki/Raspberry_Pi

## Requirements

- supported 64-bit Linux;
- Python 3.10+ recommended;
- standard Linux utilities (`ip`, `lsblk`, optional `ping`);
- on Raspberry Pi, `vcgencmd` is used when available.

No third-party Python packages are required.

## Run

```bash
python3 tools/hardware-validation/ihap-52-central-node/validate_central_node.py \
  --output-dir tools/hardware-validation/ihap-52-central-node/runs/pi4b-reference-01 \
  --stress-seconds 300 \
  --storage-mib 128
```

## Default automated gates

| Gate | Threshold |
|---|---|
| Architecture | `aarch64` / `arm64` / `x86_64` / `amd64` |
| Logical CPUs | >=4 |
| Physical RAM | >=4,000,000,000 bytes |
| Root filesystem capacity | >=28,000,000,000 bytes, allowing partition/format overhead on nominal 32 GB media |
| Wi-Fi | at least one wireless interface up with a non-link-local IP |
| Graphics/compute exposure | at least one `/dev/dri/card*` or `/dev/dri/render*` device |
| Storage smoke | deterministic write/read hashes match and temp file removed |
| Stress workers | all workers exit successfully |
| Pi current undervoltage | absent when `vcgencmd` is available |
| Pi current throttling | absent when `vcgencmd` is available |

The 28 GB filesystem threshold is a practical gate for a nominal 32 GB card after partitioning/formatting. The manually recorded card capacity and A2 marking remain part of acceptance evidence.

## Outputs

```text
runs/<run-id>/
├── validation.json
└── validation.md
```

The local `runs/` directory is ignored by Git.

## Manual evidence

Record separately:

- exact board/RAM variant;
- storage manufacturer/model, 32 GB capacity and A2 marking;
- Raspberry Pi OS Lite 64-bit selected in Imager;
- PSU manufacturer/model/rating;
- enclosure;
- heatsinks/fan;
- approximate ambient temperature.

## Privacy / publication

Review raw output before publication. Publish only a sanitized summary under `docs/evidence/IHAP-52/summaries/`.

## Exit codes

- `0`: all applicable automated gates passed;
- `2`: at least one applicable automated gate failed.

A failed gate is evidence to investigate, not an automatic rejection of Raspberry Pi 4.
