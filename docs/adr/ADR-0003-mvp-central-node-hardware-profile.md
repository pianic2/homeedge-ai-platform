# ADR-0003 — MVP Central Node Hardware Profile

**Status:** Proposed  
**Date:** 2026-08-07  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Jira:** IHAP-52  
**PR:** Pending  
**Supersedes:** None  
**Superseded by:** None

<!--
AI_AGENT_METADATA:
  document_type: architecture_decision_record
  status_allowed_values:
    - Proposed
    - Accepted
    - Superseded
    - Rejected
  approval_authority: project_owner
  source_of_truth: github_versioned_repository_documentation
  jira_role: evidence_links_only
  confluence_role: stakeholder_navigation_only
  related_risk_model: docs/risks/risk-model-baseline.md
  unvalidated_claim_marker: "[UNVALIDATED]"

HIDDEN_ANTI_REGRESSION_RULES:
  - Keep this ADR limited to the central-node hardware profile, reference implementation and hardware-equivalence contract.
  - Do not accept Docker, Alpine Linux, a database, container orchestration, Kafka, backend implementation topology or a specific AI runtime/model through this ADR.
  - Raspberry Pi 4 Model B is a reference implementation, not a vendor lock-in requirement.
  - Raspberry Pi 5 and other machines are not community-validated merely because their documented specifications satisfy the profile.
  - Do not claim GPU/NPU acceleration for AI until a future runtime/model is selected and measured.
  - Keep [UNVALIDATED] on workload sufficiency, AI acceleration, storage endurance and thermal sufficiency until project evidence exists.
  - Do not mark this ADR Accepted without explicit Project Owner approval after the required evidence review.
-->

---

## 1. Context

HomeEdge separates ESP32-C3 edge nodes from a local central node. The central node is expected to receive local HTTP/JSON telemetry, support device and read-model directions, retain local operational data and logs, and provide a foundation for later small-model AI workloads. The repository currently exposes `services/ingestion/`, `services/device-registry/`, `services/read-model/` and `services/ai-insight/` only as target service boundaries; those folders are not runtime evidence and cannot be used to infer resource consumption.

The hardware decision therefore needs two different contracts:

1. a vendor-neutral minimum profile that future Infrastructure-as-Code can target without binding HomeEdge to Raspberry Pi hardware;
2. a reproducible reference implementation that can be physically validated by the project and later promoted to a community-validated device profile.

Docker, Alpine Linux, deployment topology, database choice, Kafka, container orchestration and the final AI runtime/model remain separate `[UNVALIDATED]` software decisions.

The Project Owner has an existing Raspberry Pi 4 Model B with 8 GB RAM available as the first validation specimen. Existing ownership is availability evidence only; it does not make replication cost zero and is not sufficient by itself to justify the architecture.

---

## 2. Decision

```text
HomeEdge will define the central node through a vendor-neutral minimum hardware profile and will keep future Infrastructure-as-Code portable across compliant Linux machines.

The first reference and project-validation platform is Raspberry Pi 4 Model B with at least 4 GB RAM, a 64 GB A2 microSD card and Wi-Fi connectivity.

Raspberry Pi 5 is a recommended newer compatible candidate for new purchases, but it is not community-validated until equivalent project/community evidence exists.

Only devices that satisfy the minimum profile may be considered compatible. Only devices with reproducible evidence may be labelled community-validated or officially recommended by the project.
```

### 2.1 Minimum compliant central-node profile

| Dimension | Minimum requirement | Validation boundary |
|---|---|---|
| CPU architecture | 64-bit `arm64/aarch64` or `x86_64` Linux-capable platform | Architecture support is a hardware compatibility requirement; application/runtime compatibility remains `[UNVALIDATED]` |
| CPU concurrency | At least 4 logical processors | Resource sufficiency for the final workload remains `[UNVALIDATED]` |
| RAM | At least 4 GB | Required to preserve headroom for backend services and future small-model AI direction; actual workload sufficiency remains `[UNVALIDATED]` |
| Local storage | At least a nominal 64 GB persistent device | Endurance and retention sufficiency remain `[UNVALIDATED]` |
| Networking | Wi-Fi required and supported by Linux | Ethernet is optional |
| Graphics / compute device | A Linux-exposed integrated or discrete graphics/compute device is required | Presence does not prove AI acceleration support; AI offload remains `[UNVALIDATED]` |
| External accelerator path | Not mandatory | USB/PCIe or equivalent expansion is desirable where available for future AI accelerators |
| Power | Manufacturer-supported regulated supply sized for the device and required peripherals | Board-specific voltage/current rules remain part of the device profile |
| Cooling | No universal active-cooling requirement | Heatsinks and/or a fan are optional but recommended where low-cost; thermal sufficiency must be measured |
| Enclosure | Must permit safe handling and adequate ventilation for the chosen device | No IP, industrial, fire-safety or certified-product claim |
| GPIO | Not required | Central-node software must not depend on Raspberry Pi GPIO |

The graphics/compute-device requirement establishes a hardware baseline only. For the Raspberry Pi 4 reference, VideoCore VI is documented hardware, but its suitability for the future HomeEdge AI runtime is `[UNVALIDATED]`. CPU-only small-model inference must remain possible until a later AI decision proves a supported acceleration path.

### 2.2 Reference implementation

| Component | Reference decision |
|---|---|
| Compute | Raspberry Pi 4 Model B |
| Minimum RAM for reference | 4 GB |
| First validation specimen | Existing Raspberry Pi 4 Model B, 8 GB RAM |
| Storage | 64 GB A2 microSD |
| Required network | On-board dual-band Wi-Fi |
| Optional network | Gigabit Ethernet |
| Power | Raspberry Pi-supported 5 V USB-C supply; official 15 W / 5.1 V 3 A class is preferred |
| Cooling | Optional but recommended heatsinks and/or fan |
| Enclosure | Ventilated non-industrial Raspberry Pi-compatible case recommended |

Raspberry Pi documents Raspberry Pi 4 as a 64-bit quad-core Cortex-A72 platform with 4 GB and 8 GB RAM variants, dual-band 802.11ac Wi-Fi, Gigabit Ethernet, USB 3.0, microSD storage, 5 V USB-C power and VideoCore VI graphics. These are documented manufacturer capabilities, not HomeEdge workload measurements.

### 2.3 Support tiers

| Tier | Meaning |
|---|---|
| Minimum compliant | Meets the accepted hardware contract. No project runtime guarantee is implied. |
| Compatible candidate | Documented specifications appear to meet the contract, but HomeEdge validation evidence is incomplete. |
| Community validated | A reproducible HomeEdge validation run exists and passes the accepted evidence gates. |
| Recommended reference | Community-validated hardware the project recommends for reproducibility and contributor onboarding. |

At proposal time, Raspberry Pi 4 Model B is the approved validation/reference candidate. It becomes the first `Community validated` / `Recommended reference` profile only after the physical validation evidence is reviewed. Raspberry Pi 5 is a `Compatible candidate` and may be preferable for a new purchase because it is newer and materially faster, but it must not be described as HomeEdge-validated before a comparable run exists.

---

## 3. Alternatives Considered

| Alternative | Outcome | Reason |
|---|---|---|
| Raspberry Pi 4 Model B >=4 GB | Proposed reference | Available validation specimen, 64-bit quad-core CPU, >=4 GB variants, Wi-Fi, Ethernet, USB 3 and mature Linux support; project workload/thermal/storage evidence still required |
| Raspberry Pi 5 >=4 GB | Compatible / recommended new-purchase candidate | Newer Cortex-A76 platform with greater CPU/GPU and I/O headroom; not yet validated by HomeEdge |
| Raspberry Pi 3 Model B+ | Not recommended | 64-bit quad-core and Wi-Fi are present, but the documented 1 GB RAM is below the accepted minimum |
| Raspberry Pi Zero 2 W | Rejected for central node | 512 MB RAM and limited I/O are below the minimum profile despite 64-bit CPU and Wi-Fi |
| Low-cost x86_64 mini-PC / thin client | Compatible candidate when profile is met | Can provide strong CPU, RAM and internal SSD options; model variability prevents a generic device from being called validated |
| Reused x86_64 laptop/desktop | Compatible candidate when profile is met | Useful reuse path with potentially zero acquisition cost, but reproducibility and power/thermal characteristics vary by unit |
| Cloud-only runtime | Rejected as central-node replacement for MVP | Removes the required local central-node boundary and introduces WAN dependency; cloud remains a separate future architecture option |

---

## 4. Consequences

### Positive

- Hardware requirements are separated from a specific vendor or board generation.
- The available Raspberry Pi 4 can produce real project evidence without requiring an immediate purchase.
- A contributor may buy a Raspberry Pi 5 or use a compliant x86_64 machine without forcing a new architecture decision.
- Support labels distinguish specification compatibility from actual community validation.
- Wi-Fi is guaranteed for the reference/local-node communication model while Ethernet remains optional.
- 4 GB RAM and a graphics/compute-device baseline preserve headroom for future small-model AI work without prematurely accepting a model or runtime.
- 64 GB A2 microSD provides a simple reproducible MVP storage baseline while keeping USB SSD migration possible later.

### Negative / Trade-offs

- Requiring 4 GB RAM, Wi-Fi and a graphics/compute device excludes otherwise capable headless or lower-memory machines.
- A nominal 64 GB microSD requirement is a project baseline rather than measured retention/endurance evidence; storage sufficiency remains `[UNVALIDATED]`.
- Raspberry Pi 4 graphics hardware does not by itself prove useful AI acceleration.
- Supporting both ARM64 and x86_64 increases future build/test matrix scope.
- Optional fan/heatsink recommendations add small replication cost and configuration variance.

### Neutral / Operational

- Raspberry Pi 5 is not rejected; it is intentionally kept as a newer compatible candidate until evidence is contributed.
- USB SSD, NVMe/eMMC and internal SSD remain valid storage alternatives when a device satisfies the minimum capacity and future validation gates.
- Infrastructure-as-Code portability is an architectural constraint for future implementation, not an IaC implementation delivered by IHAP-52.
- The available Raspberry Pi 4 8 GB specimen is over the 4 GB minimum and does not change the minimum requirement.
- Existing ownership and replication price snapshots remain separate cost concepts.

---

## 5. Related Risks and Treatments

No existing canonical Risk Record specifically covers central-node resource sizing, microSD endurance or central-node thermals at the time of this proposal.

| Risk | Treatment | Effect | Remaining exposure |
|---|---|---|---|
| None | IHAP-52 validation plan | Leaves unresolved pending evidence | Workload sufficiency, microSD endurance, thermal margin, Wi-Fi behavior and AI acceleration remain `[UNVALIDATED]` until measured or handled by later tasks |

---

## 6. Follow-up Work

| Item | Tracking |
|---|---|
| Execute Raspberry Pi 4 physical validation and publish reviewed summary evidence | IHAP-52 |
| Promote Raspberry Pi 4 to Community validated / Recommended reference after evidence passes | IHAP-52 Project Owner review |
| Validate Raspberry Pi 5 through the same protocol when a specimen/community run is available | Future IHAP work / community evidence |
| Implement portable Infrastructure-as-Code without Raspberry Pi-only application dependencies | Future infrastructure task |
| Select and benchmark the small-model AI runtime/model and any GPU/NPU/USB accelerator path | Future AI task |
| Define runtime OS/container implementation | Separate runtime/infrastructure decisions |
| Propagate accepted central-node quantities and replication snapshots to the BOM | IHAP-17 / IHAP-43 after acceptance |

---

## 7. Evidence Links

| Evidence | Link |
|---|---|
| Jira issue | [IHAP-52](https://niccolopiazzi01.atlassian.net/browse/IHAP-52) |
| Pull request | Pending |
| Evidence index | [IHAP-52 evidence](../evidence/IHAP-52/README.md) |
| Hardware comparison | [Central-node comparison](../evidence/IHAP-52/central-node-hardware-comparison.md) |
| Validation plan | [Central-node validation plan](../evidence/IHAP-52/central-node-validation-plan.md) |
| Validation harness | [IHAP-52 harness](../../tools/hardware-validation/ihap-52-central-node/README.md) |
| Raspberry Pi 4 official specifications | https://www.raspberrypi.com/products/raspberry-pi-4-model-b/specifications/ |
| Raspberry Pi 5 official specifications | https://www.raspberrypi.com/products/raspberry-pi-5/ |
| Raspberry Pi 3 Model B+ official product brief | https://datasheets.raspberrypi.com/rpi3/raspberry-pi-3-b-plus-product-brief.pdf |
| Raspberry Pi Zero 2 W official specifications | https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/ |
| Related Risk Records | None |
| Related treatments | None |
| Related ADRs | [ADR-0001](ADR-0001-mvp-edge-compute-platform.md) |

---

## 8. Review Notes

```text
[x] One stable architectural decision only: central-node hardware profile and its reference/equivalence contract.
[x] ADR necessity is explicit; IHAP-43 requires an architecture-significant central-node decision.
[x] Related risks and treatments were checked; no matching canonical Risk Record exists at proposal time.
[x] Source-of-truth boundaries are preserved.
[x] MVP boundary is not silently expanded.
[x] Docker, Alpine Linux, database, orchestration, Kafka and final AI runtime remain separate decisions.
[x] Raspberry Pi 4 ownership is not used as the sole architectural justification.
[x] Raspberry Pi 5 is not labelled community-validated without evidence.
[x] AI acceleration remains [UNVALIDATED].
[x] Storage endurance, workload sufficiency and thermal sufficiency remain [UNVALIDATED].
[x] No production-ready, commercial-ready, security-grade, certified, safety-critical, alarm-grade, antifurto, access-control, intrusion-detection, or protection claim is introduced.
[x] Project Owner hardware-profile decisions were recorded in Jira before this Proposed ADR was created.
[ ] Physical Raspberry Pi 4 validation evidence has passed review.
[ ] Project Owner has explicitly accepted this ADR.
```
