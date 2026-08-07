# IHAP-52 — Central Node Hardware Evidence

## Purpose

This directory contains reviewable evidence for the HomeEdge MVP central-node hardware decision. It separates manufacturer facts, Project Owner decisions, assumptions and measured evidence.

No document here proves production readiness, storage endurance, final workload sufficiency, thermal sufficiency or AI acceleration unless reproducible evidence explicitly supports that claim.

## Current decision status

- Jira: `IHAP-52`
- ADR: `ADR-0003 — MVP Central Node Hardware Profile`
- ADR status: `Proposed`
- First reference candidate: Raspberry Pi 4 Model B, >=4 GB RAM
- First validation specimen: existing Raspberry Pi 4 Model B, 8 GB RAM
- MVP storage baseline: **32 GB A2 microSD**
- Required network: Wi-Fi
- Ethernet: optional
- Cooling: fan and/or heatsinks optional but recommended
- Reference OS for first Pi 4 validation: **Raspberry Pi OS Lite 64-bit**
- Raspberry Pi 5: newer compatible/recommended hardware candidate; not HomeEdge-validated yet
- Alpine Linux: compatible lightweight distro candidate; not the first reference image

## Evidence classification

| Claim | Classification | Boundary |
|---|---|---|
| Pi 4 has 64-bit quad-core Cortex-A72, Wi-Fi, Gigabit Ethernet, USB 3 and VideoCore VI | Documented fact | Raspberry Pi official specifications |
| >=4 GB RAM is the HomeEdge minimum | Project Owner decision | IHAP-52 |
| 32 GB A2 microSD is the first MVP storage baseline | Project Owner decision | IHAP-52 |
| Wi-Fi required / Ethernet optional | Project Owner decision | IHAP-52 |
| Fan/heatsinks optional but recommended | Project Owner decision | IHAP-52 |
| Raspberry Pi OS Lite 64-bit is the first reference/validation OS | Project Owner direction + architecture recommendation | IHAP-52 / ADR-0003 |
| Raspberry Pi OS Lite is suitable for headless setup | Documented fact | Raspberry Pi official documentation |
| Raspberry Pi OS Lite needs only 8 GB to get started | Documented recommendation | Raspberry Pi official documentation |
| Pi 4 is sufficient for final HomeEdge workload | `[UNVALIDATED]` | Physical/resource validation required |
| Pi 4 GPU accelerates future HomeEdge AI | `[UNVALIDATED]` | Future AI runtime/model benchmark required |
| 32 GB is sufficient for final retention/endurance | `[UNVALIDATED]` | Runtime retention/write model required |
| Alpine Linux is HomeEdge-validated | False at proposal time | Requires separate reproducible validation |

## Workload/resource assumptions

| Dimension | Current assumption | Status |
|---|---|---|
| Initial physically validated edge nodes | 1 generic room/door node | Known baseline |
| Maximum MVP edge-node count | Not fixed | `[UNVALIDATED]` |
| Edge-to-central transport | HTTP/JSON direction | Product direction |
| Telemetry | temperature, humidity, local non-identifying presence, door state | MVP scope |
| Event rate / payload size | Not measured | `[UNVALIDATED]` |
| Retention / log volume | Not decided/measured | `[UNVALIDATED]` |
| Backend process/container count | Not implemented | `[UNVALIDATED]` |
| Database | Not decided | `[UNVALIDATED]` |
| AI workload | Small local models are a future direction | `[UNVALIDATED]` |
| GPU/NPU offload | No runtime selected | `[UNVALIDATED]` |

## Support model

### Minimum compliant
A device satisfies the accepted hardware/OS-family contract. This does not imply runtime certification.

### Compatible candidate
Documented specifications appear to satisfy the contract but HomeEdge validation is incomplete.

### Community validated
A reproducible HomeEdge validation run passes the accepted evidence gates and review.

### Recommended reference
A community-validated profile recommended for contributor reproduction.

## Reference replication profile

| Item | Reference | Requirement type |
|---|---|---|
| Compute board | Raspberry Pi 4 Model B | Reference implementation |
| RAM | >=4 GB | Mandatory |
| Storage | 32 GB A2 microSD | MVP reference baseline |
| Wi-Fi | On-board dual-band Wi-Fi | Mandatory |
| Ethernet | On-board Gigabit Ethernet | Optional |
| PSU | Raspberry Pi-supported USB-C supply; official 15 W / 5.1 V 3 A class preferred | Mandatory stable supply / reference preference |
| Cooling | Heatsink and/or fan | Optional, recommended |
| Enclosure | Ventilated non-industrial case | Recommended |
| OS | Raspberry Pi OS Lite 64-bit | First reference image |
| External AI accelerator | None required for MVP | Optional future extension |

## OS installation sources

### Raspberry Pi OS Lite 64-bit — reference

Use the official Raspberry Pi installation guide and Raspberry Pi Imager:

- https://www.raspberrypi.com/documentation/computers/getting-started.html#install-an-operating-system

For headless systems Raspberry Pi recommends Raspberry Pi OS Lite. During Imager setup configure Wi-Fi and enable SSH before first boot.

### Alpine Linux — compatible alternative candidate

Official Alpine Raspberry Pi documentation:

- https://wiki.alpinelinux.org/wiki/Raspberry_Pi

Alpine supports aarch64 Raspberry Pi 4/5, but its diskless/system-disk installation modes introduce a different persistence model. It must therefore be separately validated before becoming a HomeEdge reference image.

## Acquisition vs replication cost

The existing Raspberry Pi 4 Model B 8 GB and 32 GB A2 microSD are already available validation components. Their historical acquisition price is not recorded, therefore acquisition cost is `unknown/pre-owned`, not EUR 0.

Replication prices must be treated as dated snapshots and refreshed when IHAP-17 is unblocked and the accepted central-node BOM is propagated.

## Primary sources

- Raspberry Pi getting started / OS installation: https://www.raspberrypi.com/documentation/computers/getting-started.html
- Raspberry Pi 4 specifications: https://www.raspberrypi.com/products/raspberry-pi-4-model-b/specifications/
- Raspberry Pi 5 specifications: https://www.raspberrypi.com/products/raspberry-pi-5/
- Alpine Raspberry Pi documentation: https://wiki.alpinelinux.org/wiki/Raspberry_Pi

## Files

- `central-node-hardware-comparison.md` — alternative comparison and equivalence rules.
- `central-node-validation-plan.md` — physical/resource validation protocol.
- `pre-pr-review-summary.md` — advisory specialist review outcome.
- `../../adr/ADR-0003-mvp-central-node-hardware-profile.md` — Proposed ADR.
- `../../../tools/hardware-validation/ihap-52-central-node/` — reproducible validation harness.

## Publication boundary

Raw run outputs may contain local device/network metadata. Review and sanitize them before publication. Public evidence should expose only the minimum facts needed to establish the tested configuration and pass/fail result.
