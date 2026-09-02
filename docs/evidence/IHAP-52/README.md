# IHAP-52 — Central Node Hardware Evidence

## Current state

- Jira: `IHAP-52`
- ADR: `ADR-0006 — MVP Central Node Hardware Profile`
- ADR status: `Proposed`
- PR: `#30`
- reference candidate: Raspberry Pi 4 Model B >=4 GB
- first specimen: owned Raspberry Pi 4 Model B 8 GB
- storage baseline: **32 GB A2 microSD**
- reference OS: **Raspberry Pi OS Lite 64-bit**
- Wi-Fi required; Ethernet optional
- physical run: pending

`ADR-0006` replaces the stale branch-local ADR-0003 number only. Current `main` already uses ADR-0003, ADR-0004 and ADR-0005 for accepted door/display/presence decisions.

## Decision/evidence boundary

| Claim | State |
|---|---|
| Pi 4 documented CPU/RAM/network/I/O capabilities | manufacturer fact |
| >=4 GB RAM | HomeEdge minimum-profile decision |
| 32 GB A2 microSD | HomeEdge first reference storage decision |
| Wi-Fi required | HomeEdge profile decision |
| Pi OS Lite 64-bit first reference image | HomeEdge reference-validation decision |
| Pi 4 final HomeEdge workload sufficiency | `[UNVALIDATED]` |
| microSD endurance / final retention | `[UNVALIDATED]` |
| GPU/AI acceleration | `[UNVALIDATED]`; not an MVP hardware gate |
| Alpine Linux HomeEdge validation | not established |

## Validation model

The operator does **not** manually execute a long checklist. The canonical path is:

```bash
python3 tools/hardware-validation/ihap-52-central-node/validate_central_node.py --guided
```

The harness performs automated profile, Wi-Fi, repository-integrity, Raspberry Pi power/throttle, storage-integrity, CPU-stress, boot-stability and post-flight gates. Only physical attributes unavailable to Linux are prompted.

Quick commands:

- [`tools/hardware-validation/ihap-52-central-node/QUICKSTART.md`](../../../tools/hardware-validation/ihap-52-central-node/QUICKSTART.md)
- [`central-node-validation-plan.md`](central-node-validation-plan.md)

## Harness regression tests

```bash
python3 -m unittest discover \
  -s tools/hardware-validation/ihap-52-central-node/tests \
  -p 'test_*.py' -v
```

The remediation suite contains host-only tests so harness changes can be validated without spending physical test time.

## Workload/resource assumptions

| Dimension | Current assumption | Status |
|---|---|---|
| Initial physically validated edge nodes | 1 generic room/door node | known baseline |
| Maximum MVP edge-node count | not fixed | `[UNVALIDATED]` |
| Edge-to-central transport | HTTP/JSON direction | product direction |
| Telemetry | temperature, humidity, local non-identifying presence, door state | MVP scope |
| Event rate / payload size | not measured | `[UNVALIDATED]` |
| Retention / log volume | not decided/measured | `[UNVALIDATED]` |
| Backend/container count | not implemented | `[UNVALIDATED]` |
| Database | not decided | `[UNVALIDATED]` |
| AI workload | future direction only | `[UNVALIDATED]` |

## Reference replication profile

| Item | Reference | Requirement |
|---|---|---|
| Compute | Raspberry Pi 4 Model B | reference implementation |
| RAM | >=4 GB | mandatory |
| Storage | 32 GB A2 microSD | first reference baseline |
| Wi-Fi | on-board wireless | mandatory |
| Ethernet | Gigabit Ethernet | optional |
| PSU | supported USB-C PSU; official 5.1 V / 3 A class preferred | mandatory stable supply |
| Cooling | heatsink and/or fan | optional; exact tested setup recorded |
| Enclosure | ventilated case or explicit bench setup | record exact setup |
| OS | Raspberry Pi OS Lite 64-bit | first reference image |
| GPU/accelerator | none required | optional future capability |

## Official sources

- Raspberry Pi headless/getting started: https://www.raspberrypi.com/documentation/computers/getting-started.html
- Raspberry Pi OS images: https://www.raspberrypi.com/software/operating-systems/
- Raspberry Pi 4 specifications: https://www.raspberrypi.com/products/raspberry-pi-4-model-b/specifications/
- Raspberry Pi 5 specifications: https://www.raspberrypi.com/products/raspberry-pi-5/
- Alpine Raspberry Pi documentation: https://wiki.alpinelinux.org/wiki/Raspberry_Pi

Do not freeze a Raspberry Pi OS image-size number into the architecture decision. Capture the actual version under test and keep final HomeEdge storage/endurance claims evidence-based.

## Files

- `central-node-hardware-comparison.md` — alternative comparison/equivalence rules.
- `central-node-validation-plan.md` — canonical physical runbook.
- `PR-SUMMARY.md` — PR-level decision/remediation summary.
- `pre-pr-review-summary.md` — specialist pre-physical-run review.
- `../../adr/ADR-0006-mvp-central-node-hardware-profile.md` — Proposed ADR.
- `../../../tools/hardware-validation/ihap-52-central-node/` — harness, quick-start and host regression tests.

## Publication boundary

Raw run outputs remain local by default. Review and sanitize derived evidence before publication. No SSID, credential, private IP, MAC, hostname or username is required for public evidence.
