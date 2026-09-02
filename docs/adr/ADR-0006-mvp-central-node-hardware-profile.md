# ADR-0006 — MVP Central Node Hardware Profile

**Status:** Proposed  
**Date:** 2026-09-02  
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
  - Keep this ADR limited to central-node hardware profile, reference implementation and portability contract.
  - Raspberry Pi 4 Model B is a reference implementation, not a vendor lock-in requirement.
  - Raspberry Pi OS Lite 64-bit is the first Pi 4 validation image, not a universal Linux dependency.
  - Alpine Linux remains a future compatible candidate until separately validated.
  - Do not accept Docker, database, orchestration, Kafka or a final AI runtime through this ADR.
  - GPU/graphics exposure may be recorded but is not a current MVP hardware acceptance requirement.
  - Keep [UNVALIDATED] on workload sufficiency, storage endurance/retention and AI acceleration until project evidence exists.
  - Do not mark Accepted without explicit Project Owner approval after the physical evidence review.
-->

---

## 1. Context

HomeEdge separates low-cost ESP32-C3 room/door edge nodes from a local central node. The central node is intended to host future local ingestion/backend/read-model responsibilities while preserving a local-first deployment boundary.

The repository's service directories and future AI direction are target architecture, not runtime evidence. CPU/RAM headroom, final storage retention, container behavior, database behavior and AI performance therefore remain `[UNVALIDATED]`.

The hardware decision needs two layers:

1. a vendor-neutral minimum profile that future Infrastructure-as-Code can target without Raspberry Pi application lock-in;
2. one reproducible physical reference that the project can validate now.

The Project Owner has an existing Raspberry Pi 4 Model B with 8 GB RAM and a 32 GB A2 microSD available for the MVP validation.

This ADR was originally drafted as ADR-0003 on the IHAP-52 branch. While that branch remained open, current `main` accepted ADR-0003 (door sensor), ADR-0004 (local display) and ADR-0005 (presence sensor). IHAP-52 is therefore correctly renumbered to **ADR-0006**. Accepted ADRs are not renumbered.

---

## 2. Decision

```text
HomeEdge defines the central node through a vendor-neutral 64-bit Linux hardware profile.

The first reference and physical-validation platform is Raspberry Pi 4 Model B with at least 4 GB RAM, a 32 GB A2 microSD card and Wi-Fi connectivity.

The owned Raspberry Pi 4 Model B 8 GB is the first validation specimen.

Raspberry Pi OS Lite 64-bit is the first reference/validation image for the Pi 4 profile.

Raspberry Pi 5 and compliant x86_64 machines remain compatible candidates. Alpine Linux remains a compatible lightweight distro candidate pending separate validation.
```

### 2.1 Minimum compliant profile

| Dimension | Minimum requirement | Boundary |
|---|---|---|
| CPU architecture | 64-bit ARM64/AArch64 or x86_64 Linux-capable platform | Application/runtime compatibility remains `[UNVALIDATED]` |
| CPU concurrency | >=4 logical processors | Final workload sufficiency remains `[UNVALIDATED]` |
| RAM | >=4 GB | Final workload sufficiency remains `[UNVALIDATED]` |
| Local storage | nominal >=32 GB persistent storage | Retention/endurance remain `[UNVALIDATED]` |
| Networking | Wi-Fi supported under Linux | Ethernet optional |
| Power | manufacturer-supported regulated supply sized for the device/peripherals | Device-specific rules apply |
| Cooling | adequate for the validated bounded workload | No universal active-cooling requirement |
| Enclosure | safe handling and adequate ventilation | No IP/fire/safety certification claim |
| GPIO | not required | Central-node application must not depend on Raspberry Pi GPIO |
| Operating system | supported 64-bit Linux | Pi OS Lite is the first reference image only |
| GPU / accelerator | not mandatory for current MVP | Exposure may be recorded; AI acceleration remains `[UNVALIDATED]` |

### 2.2 Raspberry Pi 4 reference implementation

| Component | Reference decision |
|---|---|
| Compute | Raspberry Pi 4 Model B |
| Minimum RAM | 4 GB |
| First specimen | existing Raspberry Pi 4 Model B 8 GB |
| Storage | 32 GB A2 microSD |
| Required network | on-board Wi-Fi |
| Optional network | Gigabit Ethernet |
| Power | Raspberry Pi-supported USB-C supply; official 5.1 V / 3 A class preferred |
| Cooling | optional heatsinks and/or fan; record exact tested configuration |
| Enclosure | ventilated non-industrial Pi-compatible case or explicit open-bench setup |
| Reference OS | Raspberry Pi OS Lite 64-bit |

Raspberry Pi 4's documented hardware capabilities are manufacturer facts; they do not prove HomeEdge workload sufficiency.

### 2.3 Reference OS and installation

Use Raspberry Pi's current official headless setup path and Raspberry Pi Imager:

- https://www.raspberrypi.com/documentation/computers/getting-started.html
- https://www.raspberrypi.com/software/operating-systems/

The operator selects the current Raspberry Pi OS Lite 64-bit image, configures Wi-Fi/SSH in Imager, and the validation harness records the actual runtime OS/kernel under test. The ADR deliberately avoids hard-coding a Raspberry Pi OS release number or image-size assumption that can become stale.

Alpine Linux remains a compatible future candidate:

- https://wiki.alpinelinux.org/wiki/Raspberry_Pi

Its installation/persistence model requires a separate reproducibility validation before reference promotion.

### 2.4 Support tiers

| Tier | Meaning |
|---|---|
| Minimum compliant | Meets the hardware/OS-family contract; no runtime guarantee implied |
| Compatible candidate | Documented specifications appear compliant; HomeEdge physical/runtime evidence incomplete |
| Community validated | Reproducible HomeEdge validation run passes reviewed gates |
| Recommended reference | Community-validated profile recommended for reproduction/onboarding |

At `Proposed` status, Raspberry Pi 4 is the **reference/validation candidate**, not yet Community validated.

---

## 3. Alternatives Considered

| Alternative | Outcome | Reason |
|---|---|---|
| Raspberry Pi 4 Model B >=4 GB | Proposed reference | Available specimen, mature Linux support, Wi-Fi/USB/Ethernet, no new purchase required for first validation |
| Raspberry Pi 5 >=4 GB | Compatible / newer candidate | More headroom, but no HomeEdge validation evidence yet |
| Raspberry Pi 3 Model B+ | Not recommended | 1 GB RAM below the HomeEdge minimum |
| Raspberry Pi Zero 2 W | Rejected for central node | 512 MB RAM below minimum and limited I/O/headroom |
| x86_64 mini-PC / thin client | Compatible candidate | Good CPU/RAM/storage options but model variability requires profile validation |
| Reused x86_64 laptop/desktop | Compatible candidate | Reuse path is valid; reproducibility/power/support vary |
| Cloud-only runtime | Rejected as central-node replacement | Conflicts with local-first central-node boundary and introduces WAN dependency |
| Raspberry Pi OS Lite 64-bit | First reference OS | Official headless Pi path with minimal desktop overhead |
| Alpine Linux aarch64 | Compatible distro candidate | Lightweight, but persistence/install choices require separate validation |

---

## 4. Consequences

### Positive

- Hardware requirements remain vendor-neutral.
- The existing Pi 4 and 32 GB A2 card can be validated without procurement.
- The first physical campaign is short and reproducible.
- Equivalent ARM64/x86_64 replacements remain possible.
- Application architecture is not coupled to Raspberry Pi GPIO or GPU.

### Negative / Trade-offs

- 32 GB has limited headroom compared with larger media; final retention/endurance remain unknown.
- Supporting ARM64 and x86_64 increases future IaC/build validation scope.
- Raspberry Pi OS Lite validates one reference path, not Alpine or every Linux distro.
- A Pi 4 hardware PASS does not prove the future HomeEdge service workload.

### Operational

- The physical campaign uses the committed IHAP-52 guided harness.
- A passing hardware run does not authorize Docker/database/AI claims.
- Storage, power, cooling and Wi-Fi conditions must be recorded exactly for reproducibility.

---

## 5. Related Risks and Treatments

| Risk / exposure | Treatment | Remaining exposure |
|---|---|---|
| Power instability / throttling | Mandatory `vcgencmd` pre/post gates in IHAP-52 harness | Long-term PSU reliability remains outside the bounded run |
| Storage corruption | Deterministic write/read/SHA-256 smoke test | microSD endurance/retention remains `[UNVALIDATED]` |
| Resource instability | bounded CPU stress, worker/boot/OOM checks | final application workload remains `[UNVALIDATED]` |
| Vendor lock-in | ARM64/x86_64 equivalent-device contract; no Pi GPIO dependency | future IaC must preserve portability |

No residual risk is accepted by this ADR.

---

## 6. Follow-up Work

| Item | Tracking |
|---|---|
| Run Pi 4 guided physical validation and review evidence | IHAP-52 |
| Accept/reject ADR after physical evidence | IHAP-52 Project Owner |
| Propagate accepted central-node BOM/cost profile | IHAP-17 / IHAP-43 |
| Validate Pi 5 / x86_64 references when useful | Future hardware validation |
| Validate Alpine Linux as alternate reference distro | Future infrastructure/runtime validation |
| Implement portable IaC | Future infrastructure task |
| Benchmark final services/storage/write rate | Future runtime tasks |
| Select/benchmark AI runtime/accelerator only if approved | Future AI task |

---

## 7. Evidence Links

| Evidence | Link |
|---|---|
| Jira issue | [IHAP-52](https://niccolopiazzi01.atlassian.net/browse/IHAP-52) |
| Pull request | [PR #30](https://github.com/pianic2/homeedge-ai-platform/pull/30) |
| Evidence index | [IHAP-52 evidence](../evidence/IHAP-52/README.md) |
| Hardware comparison | [Central-node comparison](../evidence/IHAP-52/central-node-hardware-comparison.md) |
| Validation runbook | [Central-node validation runbook](../evidence/IHAP-52/central-node-validation-plan.md) |
| Quick commands | [Quick test commands](../../tools/hardware-validation/ihap-52-central-node/QUICKSTART.md) |
| Validation harness | [IHAP-52 harness](../../tools/hardware-validation/ihap-52-central-node/README.md) |
| Raspberry Pi official setup | https://www.raspberrypi.com/documentation/computers/getting-started.html |
| Raspberry Pi OS images | https://www.raspberrypi.com/software/operating-systems/ |
| Alpine Raspberry Pi documentation | https://wiki.alpinelinux.org/wiki/Raspberry_Pi |
| Related edge-compute ADR | [ADR-0001](ADR-0001-mvp-edge-compute-platform.md) |

---

## 8. Review Notes

```text
[x] ADR number reconciled against current main: ADR-0006.
[x] Accepted ADR-0003/0004/0005 remain untouched.
[x] Vendor-neutral ARM64/x86_64 portability preserved.
[x] 32 GB A2 is the MVP reference storage baseline.
[x] Raspberry Pi OS Lite 64-bit is the first reference/validation image.
[x] Alpine Linux remains a compatible candidate.
[x] Docker, database, orchestration, Kafka and final AI runtime remain separate decisions.
[x] GPU/graphics exposure is not a current MVP acceptance gate.
[x] Validation harness has automated pre-flight/stress/post-flight gates and host regression tests.
[x] Workload sufficiency, storage endurance/retention and AI acceleration remain [UNVALIDATED].
[ ] Physical Raspberry Pi 4 validation evidence has passed review.
[ ] Project Owner has explicitly accepted this ADR.
```
