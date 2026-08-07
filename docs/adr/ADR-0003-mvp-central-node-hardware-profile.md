# ADR-0003 — MVP Central Node Hardware Profile

**Status:** Proposed  
**Date:** 2026-08-07  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Jira:** IHAP-52  
**PR:** [PR #30](https://github.com/pianic2/homeedge-ai-platform/pull/30)  
**Supersedes:** None  
**Superseded by:** None

<!--
AI_AGENT_METADATA:
  document_type: architecture_decision_record
  approval_authority: project_owner
  source_of_truth: github_versioned_repository_documentation
  jira_role: evidence_links_only
  confluence_role: stakeholder_navigation_only
  unvalidated_claim_marker: "[UNVALIDATED]"

HIDDEN_ANTI_REGRESSION_RULES:
  - Keep this ADR limited to the central-node hardware profile, reference implementation and compatibility contract.
  - Raspberry Pi 4 Model B is a reference implementation, not a vendor lock-in requirement.
  - Raspberry Pi OS Lite 64-bit is the first reference/validation OS for the Pi 4 profile, not a universal Linux requirement.
  - Alpine Linux remains a compatible candidate until separately validated for HomeEdge.
  - Do not accept Docker, a database, container orchestration, Kafka or a specific AI runtime/model through this ADR.
  - Do not claim GPU/NPU acceleration until a future runtime/model is selected and measured.
  - Keep [UNVALIDATED] on workload sufficiency, AI acceleration, storage endurance and thermal sufficiency until project evidence exists.
  - Do not mark this ADR Accepted without explicit Project Owner approval after required evidence review.
-->

---

## 1. Context

HomeEdge separates ESP32-C3 edge nodes from a local central node. The central node is expected to receive local telemetry, support future backend/read-model responsibilities, retain local operational data and provide a foundation for later small-model AI workloads.

The repository service directories remain target boundaries rather than runtime evidence, so final CPU, RAM, storage retention and AI performance remain `[UNVALIDATED]`.

The hardware decision therefore defines:

1. a vendor-neutral minimum profile that future Infrastructure-as-Code can target;
2. a reproducible Raspberry Pi 4 reference implementation that the project can physically validate;
3. a reference OS image for the first hardware-validation path without making that distro a universal architecture dependency.

The Project Owner has an existing Raspberry Pi 4 Model B with 8 GB RAM and currently has a 32 GB A2 microSD available for the MVP validation.

---

## 2. Decision

```text
HomeEdge will define the central node through a vendor-neutral minimum hardware profile and keep future Infrastructure-as-Code portable across compliant 64-bit Linux machines.

The first reference and project-validation platform is Raspberry Pi 4 Model B with at least 4 GB RAM, a 32 GB A2 microSD card and Wi-Fi connectivity.

Raspberry Pi OS Lite 64-bit is the reference OS for the first Raspberry Pi 4 MVP validation and installation path.

Raspberry Pi 5 is a recommended newer compatible candidate for new purchases, but it is not community-validated until equivalent project/community evidence exists.

Alpine Linux remains a compatible lightweight distro candidate and may be validated later; it is not required for IHAP-52 acceptance.
```

### 2.1 Minimum compliant central-node profile

| Dimension | Minimum requirement | Validation boundary |
|---|---|---|
| CPU architecture | 64-bit `arm64/aarch64` or `x86_64` Linux-capable platform | Final application/runtime compatibility remains `[UNVALIDATED]` |
| CPU concurrency | At least 4 logical processors | Final workload sufficiency remains `[UNVALIDATED]` |
| RAM | At least 4 GB | Required baseline for backend and future small-model AI direction; actual sufficiency remains `[UNVALIDATED]` |
| Local storage | At least a nominal 32 GB persistent device | Retention/endurance remain `[UNVALIDATED]` |
| Networking | Wi-Fi required and supported by Linux | Ethernet optional |
| Graphics / compute device | Linux-exposed integrated/discrete graphics or compute device | Presence does not prove AI acceleration |
| External accelerator path | Not mandatory | USB/PCIe or equivalent expansion desirable where available |
| Power | Manufacturer-supported regulated supply sized for device/peripherals | Board-specific voltage/current rules apply |
| Cooling | No universal active-cooling requirement | Heatsinks and/or fan optional but recommended; thermal sufficiency must be measured |
| Enclosure | Safe handling and adequate ventilation | No industrial/IP/safety certification claim |
| GPIO | Not required | Central-node application must not depend on Raspberry Pi GPIO |
| Operating system | Supported 64-bit Linux | Raspberry Pi OS Lite 64-bit is the first reference image, not a universal requirement |

### 2.2 Raspberry Pi 4 reference implementation

| Component | Reference decision |
|---|---|
| Compute | Raspberry Pi 4 Model B |
| Minimum RAM | 4 GB |
| First validation specimen | Existing Raspberry Pi 4 Model B, 8 GB RAM |
| Storage | 32 GB A2 microSD |
| Required network | On-board dual-band Wi-Fi |
| Optional network | Gigabit Ethernet |
| Power | Raspberry Pi-supported 5 V USB-C supply; official 15 W / 5.1 V 3 A class preferred |
| Cooling | Optional but recommended heatsinks and/or fan |
| Enclosure | Ventilated non-industrial Raspberry Pi-compatible case recommended |
| Reference OS | Raspberry Pi OS Lite 64-bit |

Raspberry Pi documents Raspberry Pi 4 as a 64-bit quad-core Cortex-A72 platform with 4 GB and 8 GB RAM variants, dual-band Wi-Fi, Gigabit Ethernet, USB 3.0, microSD storage and VideoCore VI graphics. These are manufacturer capabilities, not HomeEdge workload measurements.

### 2.3 Reference OS installation

The first validation image must be installed using Raspberry Pi's official instructions:

- official setup/install documentation: https://www.raspberrypi.com/documentation/computers/getting-started.html#install-an-operating-system
- use Raspberry Pi Imager to select **Raspberry Pi OS Lite (64-bit)**, configure Wi-Fi and enable SSH for a headless deployment before first boot.

Raspberry Pi's documentation recommends Raspberry Pi OS Lite for headless systems and lists 8 GB as sufficient to get started with Lite. The HomeEdge 32 GB A2 baseline therefore provides additional initial capacity, while final retention/endurance remain `[UNVALIDATED]`.

Alpine Linux is not rejected. Official Alpine Raspberry Pi documentation is retained as the alternative lightweight distro reference:

- https://wiki.alpinelinux.org/wiki/Raspberry_Pi

Alpine uses different installation/persistence modes and therefore requires its own reproducibility validation before it can replace the reference image.

### 2.4 Support tiers

| Tier | Meaning |
|---|---|
| Minimum compliant | Meets the hardware/OS-family contract; no runtime guarantee implied |
| Compatible candidate | Specifications appear compliant but HomeEdge validation is incomplete |
| Community validated | Reproducible HomeEdge validation run passes reviewed gates |
| Recommended reference | Community-validated profile recommended for reproduction/onboarding |

At proposal time, Raspberry Pi 4 Model B with Raspberry Pi OS Lite 64-bit is the approved first validation/reference candidate. Raspberry Pi 5 is a compatible newer candidate. Alpine Linux is a compatible distro candidate, not yet the reference runtime image.

---

## 3. Alternatives Considered

| Alternative | Outcome | Reason |
|---|---|---|
| Raspberry Pi 4 Model B >=4 GB | Proposed reference | Available specimen, adequate documented hardware, Wi-Fi, USB 3, mature Linux support; project workload evidence still required |
| Raspberry Pi 5 >=4 GB | Compatible / recommended new-purchase candidate | Newer/faster platform with more headroom; not yet HomeEdge-validated |
| Raspberry Pi 3 Model B+ | Not recommended | 1 GB RAM is below the 4 GB minimum |
| Raspberry Pi Zero 2 W | Rejected for central node | 512 MB RAM and limited I/O are below the minimum |
| x86_64 mini-PC / thin client | Compatible candidate | Strong CPU/RAM/storage options but model variability requires per-profile validation |
| Reused x86_64 laptop/desktop | Compatible candidate | Useful reuse path; reproducibility/power/hardware support vary |
| Cloud-only runtime | Rejected as MVP central-node replacement | Removes local node boundary and introduces WAN dependency |
| Raspberry Pi OS Lite 64-bit | Reference OS | Minimal official headless path, straightforward Imager installation and strong Pi hardware integration |
| Alpine Linux aarch64 | Compatible distro candidate | Very lightweight and Pi-supported, but persistence/install-mode choices add validation variance for the first MVP |

---

## 4. Consequences

### Positive

- Requirements remain vendor-neutral while the project has one reproducible first reference.
- The available Pi 4 and 32 GB A2 card can be tested immediately without unnecessary procurement.
- Raspberry Pi OS Lite reduces background desktop overhead and follows the official headless setup path.
- Contributors may later use Pi 5, x86_64 or Alpine when equivalent evidence exists.
- Support labels distinguish compatibility from actual validation.
- Wi-Fi is guaranteed while Ethernet remains optional.

### Negative / Trade-offs

- 32 GB is a smaller storage baseline and makes retention/write-volume validation more important.
- microSD endurance remains workload-dependent and `[UNVALIDATED]`.
- Selecting Raspberry Pi OS Lite as the first reference image does not prove Alpine compatibility or portability by itself.
- Supporting ARM64 and x86_64 increases the future IaC/test matrix.
- Pi 4 graphics do not by themselves prove useful AI acceleration.

### Neutral / Operational

- Raspberry Pi OS Lite is a reference implementation choice; future IaC must avoid unnecessary distro-specific application coupling.
- Alpine Linux can later become validated without changing the central-node hardware contract if it satisfies the same runtime requirements.
- USB SSD/NVMe/eMMC remain compatible alternatives when future evidence justifies them.

---

## 5. Related Risks and Treatments

| Risk | Treatment | Effect | Remaining exposure |
|---|---|---|---|
| None | IHAP-52 validation plan | Leaves unresolved pending evidence | Workload sufficiency, microSD endurance, thermal margin, Wi-Fi behavior and AI acceleration remain `[UNVALIDATED]` |

---

## 6. Follow-up Work

| Item | Tracking |
|---|---|
| Install Raspberry Pi OS Lite 64-bit using official Raspberry Pi Imager guidance | IHAP-52 |
| Execute Pi 4 physical validation and publish reviewed summary | IHAP-52 |
| Promote Pi 4 profile after evidence passes | IHAP-52 Project Owner review |
| Validate Pi 5 when specimen/community evidence becomes available | Future IHAP work |
| Validate Alpine Linux as alternate lightweight central-node distro | Future infrastructure/runtime validation |
| Implement portable IaC without Raspberry Pi-only application dependencies | Future infrastructure task |
| Select/benchmark small-model AI runtime and optional accelerator path | Future AI task |
| Propagate accepted BOM quantities/cost snapshots | IHAP-17 / IHAP-43 after acceptance |

---

## 7. Evidence Links

| Evidence | Link |
|---|---|
| Jira issue | [IHAP-52](https://niccolopiazzi01.atlassian.net/browse/IHAP-52) |
| Pull request | [PR #30](https://github.com/pianic2/homeedge-ai-platform/pull/30) |
| Evidence index | [IHAP-52 evidence](../evidence/IHAP-52/README.md) |
| Hardware comparison | [Central-node comparison](../evidence/IHAP-52/central-node-hardware-comparison.md) |
| Validation plan | [Central-node validation plan](../evidence/IHAP-52/central-node-validation-plan.md) |
| Validation harness | [IHAP-52 harness](../../tools/hardware-validation/ihap-52-central-node/README.md) |
| Raspberry Pi official OS installation | https://www.raspberrypi.com/documentation/computers/getting-started.html#install-an-operating-system |
| Alpine Raspberry Pi documentation | https://wiki.alpinelinux.org/wiki/Raspberry_Pi |
| Related ADRs | [ADR-0001](ADR-0001-mvp-edge-compute-platform.md) |

---

## 8. Review Notes

```text
[x] Vendor-neutral hardware/IaC portability is preserved.
[x] 32 GB A2 is the MVP reference storage baseline.
[x] Raspberry Pi OS Lite 64-bit is the first reference/validation image.
[x] Alpine Linux remains a compatible candidate rather than an implicitly accepted runtime.
[x] Docker, database, orchestration, Kafka and final AI runtime remain separate decisions.
[x] Raspberry Pi 5 is not labelled community-validated without evidence.
[x] AI acceleration, storage endurance, final workload and thermal sufficiency remain [UNVALIDATED].
[x] Official OS installation links are recorded.
[ ] Physical Raspberry Pi 4 validation evidence has passed review.
[ ] Project Owner has explicitly accepted this ADR.
```
