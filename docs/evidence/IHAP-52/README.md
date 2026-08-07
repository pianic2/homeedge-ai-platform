# IHAP-52 — Central Node Hardware Evidence

## Purpose

This directory contains reviewable evidence for the HomeEdge MVP central-node hardware decision. It separates manufacturer facts, Project Owner decisions, assumptions and future measured evidence.

No document in this directory proves production readiness, reliability, storage endurance, thermal sufficiency or AI acceleration unless a reproducible validation result explicitly supports that claim.

## Decision status

- Jira: `IHAP-52`
- ADR: `ADR-0003 — MVP Central Node Hardware Profile`
- ADR status: `Proposed`
- Project Owner reference candidate: Raspberry Pi 4 Model B, >=4 GB RAM
- First validation specimen: existing Raspberry Pi 4 Model B, 8 GB RAM
- Reference storage: 64 GB A2 microSD
- Required network: Wi-Fi
- Ethernet: optional
- Cooling: fan and/or heatsinks optional but recommended
- Raspberry Pi 5: newer compatible/recommended candidate; not HomeEdge-validated yet

## Evidence classification

| Claim | Classification | Evidence / boundary |
|---|---|---|
| Raspberry Pi 4 has a 64-bit quad-core Cortex-A72 CPU | Documented fact | Raspberry Pi official specifications |
| Raspberry Pi 4 supports 4 GB and 8 GB RAM variants | Documented fact | Raspberry Pi official specifications |
| Raspberry Pi 4 provides dual-band 802.11ac Wi-Fi and Gigabit Ethernet | Documented fact | Raspberry Pi official specifications |
| Raspberry Pi 4 uses microSD and supports USB 3.0 | Documented fact | Raspberry Pi official specifications |
| Raspberry Pi 4 has VideoCore VI graphics | Documented fact | Raspberry Pi documentation/product material |
| Raspberry Pi 4 official reference power class is 15 W / 5.1 V 3 A | Documented fact | Raspberry Pi official product guidance |
| >=4 GB RAM is the HomeEdge minimum | Project Owner decision | Jira IHAP-52 decision comment |
| 64 GB A2 microSD is the MVP reference storage | Project Owner decision | Jira IHAP-52 decision comment |
| Wi-Fi is required and Ethernet optional | Project Owner decision | Jira IHAP-52 decision comment |
| Fan/heatsinks are optional but recommended | Project Owner decision | Jira IHAP-52 decision comment |
| Raspberry Pi 4 is sufficient for the final HomeEdge workload | `[UNVALIDATED]` | Physical/resource validation required |
| Raspberry Pi 4 GPU accelerates the future AI model/runtime | `[UNVALIDATED]` | Future AI runtime/model benchmark required |
| 64 GB is sufficient for final retention and write endurance | `[UNVALIDATED]` | Retention/write model and runtime evidence required |
| Raspberry Pi 5 is HomeEdge community-validated | False at proposal time | Requires equivalent validation evidence |

## Workload/resource assumption table

The project deliberately avoids false precision. Current product scope supports only a limited set of assumptions.

| Dimension | Current assumption | Status |
|---|---|---|
| Initial physically validated edge nodes | 1 generic room/door node | Known project baseline |
| Maximum MVP edge-node count | Not fixed | `[UNVALIDATED]` |
| Edge-to-central transport | HTTP/JSON direction | Product direction |
| Telemetry | temperature, humidity, local non-identifying presence state, door state | MVP scope |
| Event interval / event rate | Not fixed | `[UNVALIDATED]` |
| Average payload size | Not measured | `[UNVALIDATED]` |
| Events/day | Not derivable yet | `[UNVALIDATED]` |
| Retention | Not decided | `[UNVALIDATED]` |
| Backend process/container count | Not implemented | `[UNVALIDATED]` |
| Database | Not decided | `[UNVALIDATED]` |
| Log volume | Not measured | `[UNVALIDATED]` |
| Storage growth/day | Not measurable yet | `[UNVALIDATED]` |
| AI workload | Small local models are a future direction | `[UNVALIDATED]` |
| GPU/NPU offload | No runtime selected | `[UNVALIDATED]` |
| Kafka | Future / not part of this decision | OUT OF IHAP-52 |

## Support model

### Minimum compliant

A device satisfies the hardware contract when it meets all mandatory requirements in ADR-0003. Compliance is a specification result, not a runtime certification.

### Compatible candidate

A device appears to meet the hardware contract from documented specifications but has no accepted HomeEdge validation run.

### Community validated

A device has a reproducible validation summary generated with the HomeEdge IHAP-52 protocol, reviewed with no blocker/major evidence defects, and explicitly recognized by the Project Owner/community governance process.

### Recommended reference

A community-validated profile recommended for contributor reproduction. Raspberry Pi 4 Model B is the first candidate for this status.

## Reference replication profile

| Item | Reference | Requirement type |
|---|---|---|
| Compute board | Raspberry Pi 4 Model B | Reference implementation |
| RAM | >=4 GB | Mandatory for Pi 4 reference and minimum profile |
| Storage | 64 GB A2 microSD | Reference baseline |
| Wi-Fi | On-board dual-band Wi-Fi | Mandatory |
| Ethernet | On-board Gigabit Ethernet | Optional |
| PSU | Raspberry Pi-supported USB-C supply; official 15 W / 5.1 V 3 A class preferred | Mandatory stable supply / reference preference |
| Cooling | Heatsink and/or fan | Optional, recommended |
| Enclosure | Ventilated non-industrial case | Recommended |
| External AI accelerator | None required for MVP | Optional future extension |

## Acquisition vs replication cost

The existing Raspberry Pi 4 Model B 8 GB is an already-owned validation specimen. Its historical acquisition price is not currently recorded, therefore acquisition cost is `unknown/pre-owned`, not EUR 0.

Current supplier snapshots are dated observations only and must be refreshed before final IHAP-17 propagation.

| Item | Snapshot | Date checked | Source | Governance note |
|---|---:|---|---|---|
| Raspberry Pi 4 Model B 4 GB | EUR 108.58, out of stock on retrieved Melopero regional listing | 2026-08-07 | https://melopero.com/de/shop/boards/pi4/raspberrypi4computermodelb4gbram/ | Availability/price snapshot only; not a purchasing guarantee |
| Raspberry Pi official 64 GB A2 microSD | EUR 21.59 on retrieved Italian listing | 2026-08-07 | https://melopero.com/it/shop/accessories/microsd_hard_disk/raspberry-pi-sd-64/ | Snapshot only |
| Raspberry Pi 4 official PSU 5.1 V / 3 A EU | EUR 8.69 | 2026-08-07 | https://www.melopero.com/it/shop/components/power/raspberrypi4officialpowersupply5dot1v3ablackwitheuplug/ | Snapshot only |

Cooling/enclosure cost is intentionally not frozen here because multiple low-cost kits satisfy the optional/recommended profile. IHAP-17 must use a dated reproducible package price only after ADR acceptance.

## Primary hardware sources

- Raspberry Pi 4 specifications: https://www.raspberrypi.com/products/raspberry-pi-4-model-b/specifications/
- Raspberry Pi 4 product information portal: https://pip.raspberrypi.com/categories/545-raspberry-pi-4-model-b
- Raspberry Pi 5 specifications: https://www.raspberrypi.com/products/raspberry-pi-5/
- Raspberry Pi 3 Model B+ product brief: https://datasheets.raspberrypi.com/rpi3/raspberry-pi-3-b-plus-product-brief.pdf
- Raspberry Pi Zero 2 W: https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/
- Raspberry Pi hardware power documentation: https://www.raspberrypi.com/documentation/computers/raspberry-pi.html

## Files

- `central-node-hardware-comparison.md` — proportionate alternative comparison and equivalence rules.
- `central-node-validation-plan.md` — physical/resource validation protocol and evidence gates.
- `../../adr/ADR-0003-mvp-central-node-hardware-profile.md` — Proposed architectural decision.
- `../../../tools/hardware-validation/ihap-52-central-node/` — reproducible Linux validation harness.

## Publication boundary

Future run outputs may contain hostnames, private IP addresses, SSIDs, usernames, paths or other local metadata. Raw run directories must be reviewed and sanitized before publication. Public evidence should contain the minimum aggregate facts necessary to establish pass/fail and hardware identity without disclosing private network data.
