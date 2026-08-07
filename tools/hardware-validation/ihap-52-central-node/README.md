# IHAP-52 Central Node Hardware Validation Harness

## Scope

This harness collects reproducible hardware/resource evidence for the HomeEdge central-node profile without installing Docker, Alpine Linux, a database or an AI framework.

It validates only a bounded hardware smoke-test envelope:

- architecture and CPU concurrency;
- physical RAM capacity;
- local storage capacity and a bounded write/read smoke test;
- required Wi-Fi interface availability;
- Linux graphics/render-device exposure;
- Raspberry Pi temperature/throttling observations when supported;
- bounded CPU stress stability.

It does **not** prove final application performance, microSD endurance or AI acceleration.

## Requirements

- 64-bit Linux;
- Python 3.10+ recommended;
- standard Linux utilities (`ip`, `lsblk`, optional `ping`);
- on Raspberry Pi, `vcgencmd` is used when available.

No third-party Python packages are required.

## Run

From the repository root:

```bash
python3 tools/hardware-validation/ihap-52-central-node/validate_central_node.py \
  --output-dir tools/hardware-validation/ihap-52-central-node/runs/pi4b-reference-01 \
  --stress-seconds 300 \
  --storage-mib 128
```

Optional authorized local reachability check:

```bash
python3 tools/hardware-validation/ihap-52-central-node/validate_central_node.py \
  --output-dir tools/hardware-validation/ihap-52-central-node/runs/pi4b-reference-01 \
  --stress-seconds 300 \
  --storage-mib 128 \
  --wifi-host 192.168.1.2
```

Do not use a public Internet target merely to make the test pass. The central-node decision is local-first and public connectivity is not a hardware requirement.

## Default automated minimum gates

| Gate | Threshold |
|---|---|
| Architecture | `aarch64` / `arm64` / `x86_64` / `amd64` |
| Logical CPUs | >=4 |
| Physical RAM | >=4,000,000,000 bytes |
| Root filesystem capacity | >=58,000,000,000 bytes, allowing normal formatted capacity of nominal 64 GB media |
| Wi-Fi | at least one detected wireless interface that is up and has a non-link-local IP address |
| Graphics/compute exposure | at least one `/dev/dri/card*` or `/dev/dri/render*` device |
| Storage smoke | requested bytes written/read and temporary file removed |
| Stress workers | all workers exit successfully |
| Raspberry Pi current undervoltage | no current undervoltage flag when `vcgencmd` is available |
| Raspberry Pi current throttling | no current throttling flag when `vcgencmd` is available |

The storage threshold is intentionally expressed in bytes rather than `64 GiB`: consumer storage labelled 64 GB exposes less than 64 GiB after decimal/binary conversion and filesystem formatting.

## Outputs

Each run writes:

```text
runs/<run-id>/
├── validation.json
└── validation.md
```

The local `runs/` directory is ignored by Git.

## Manual evidence that software cannot prove

Record separately before publication:

- exact board and RAM variant;
- storage manufacturer/model and confirmation of A2 marking;
- PSU manufacturer/model/rating;
- enclosure;
- installed heatsinks;
- installed fan;
- approximate ambient temperature.

## Privacy / publication boundary

Raw output may contain device model, kernel/OS details and command output such as block-device models. Wi-Fi SSIDs, MAC addresses, private IPs, hostnames and usernames are deliberately not written by the harness, but all output must still be reviewed before publication.

Publish only a sanitized summary under `docs/evidence/IHAP-52/summaries/` after Project Owner review.

## Exit codes

- `0`: all applicable automated gates passed;
- `2`: at least one applicable automated gate failed;
- argparse errors use the standard non-zero Python argparse exit code.

A failed gate is evidence to investigate, not an automatic rejection of Raspberry Pi 4.
