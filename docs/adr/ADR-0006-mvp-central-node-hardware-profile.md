# ADR-0006 — MVP Central Node Hardware Profile

**Status:** Accepted  
**Date:** 2026-09-02  
**Accepted:** 2026-09-05  
**Last evidence update:** 2026-09-05  
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
  - Raspberry Pi OS Lite 64-bit is the first Pi 4 reference image, not a universal Linux dependency.
  - Alpine Linux remains a future compatible candidate until separately validated.
  - Do not accept Docker, database, orchestration, Kafka or a final AI runtime through this ADR.
  - GPU/graphics exposure is not a current MVP hardware acceptance requirement.
  - Keep [UNVALIDATED] on final workload sufficiency, storage endurance/retention and AI acceleration until project evidence exists.
  - Do not promote A2 from recommendation to mandatory without evidence that A1 fails the HomeEdge validation envelope.
  - Do not weaken Raspberry Pi 4 power requirements because a lower-current supply merely boots the board.
  - The tested Pi 4 reference enclosure requires the fan-enabled cooling configuration that passed the bounded run; this is not a universal active-cooling requirement for equivalent hardware.
  - Accepted status is authorized by explicit Project Owner approval on 2026-09-05 after physical-evidence review.
-->

---

## 1. Context

HomeEdge separates low-cost ESP32-C3 room/door edge nodes from a local central node. The central node is intended to host future local ingestion/backend/read-model responsibilities while preserving a local-first deployment boundary.

The hardware decision needs two layers:

1. a vendor-neutral minimum profile that future Infrastructure-as-Code can target without Raspberry Pi application lock-in;
2. one reproducible physical reference that the project can validate now.

The owned validation specimen is a Raspberry Pi 4 Model B Rev 1.4 with 8 GB RAM and a nominal 32 GB A1 microSD.

IHAP-52 originally drafted this decision as ADR-0003. While the branch remained open, current `main` accepted ADR-0003, ADR-0004 and ADR-0005 for other decisions. IHAP-52 is therefore correctly ADR-0006; accepted ADRs are not renumbered.

---

## 2. Decision

```text
HomeEdge defines the central node through a vendor-neutral 64-bit Linux hardware profile.

The first reference implementation is Raspberry Pi 4 Model B with at least 4 GB RAM, nominal >=32 GB persistent storage and Wi-Fi connectivity.

The first validated specimen is the owned Raspberry Pi 4 Model B 8 GB using a nominal 32 GB A1 microSD, Raspberry Pi OS Lite 64-bit, a 5.1 V / 3 A PSU and the tested case/heatsink with fan enabled.

A1 or A2 microSD application class is accepted for the bounded hardware validation. A2 is recommended for new purchases/reference replication.

For the bounded Pi 4 validation, a good-quality approximately 5 V supply rated at least 2.5 A is required; 5.1 V / 3 A remains the recommended reference supply.

Equivalent ARM64/AArch64 or x86_64 hardware may satisfy the ADR when it meets the same minimum profile and passes equivalent validation. Active cooling is not universally required, but the tested Pi 4 reference enclosure must use the fan-enabled configuration that passed physical validation.

Raspberry Pi OS Lite 64-bit is the first reference image. Alpine Linux remains a compatible lightweight candidate pending separate validation.
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
| Cooling | must complete the bounded hardware run without thermal/frequency/throttle failure | No universal active-cooling requirement |
| Enclosure | safe handling and adequate ventilation | No IP/fire/safety certification claim |
| GPIO | not required | Central-node application must not depend on Raspberry Pi GPIO |
| Operating system | supported 64-bit Linux | Pi OS Lite is the first reference image only |
| GPU / accelerator | not mandatory for current MVP | AI acceleration remains `[UNVALIDATED]` |

### 2.2 Raspberry Pi 4 reference implementation

| Component | Reference decision |
|---|---|
| Compute | Raspberry Pi 4 Model B |
| Minimum RAM | 4 GB |
| Validated specimen | Raspberry Pi 4 Model B Rev 1.4, 8 GB |
| Storage | nominal 32 GB microSD; A1 or A2 accepted |
| Validated storage | owned nominal 32 GB A1 microSD |
| Required network | on-board Wi-Fi |
| Optional network | Gigabit Ethernet |
| Power | approximately 5 V, >=2.5 A for bounded low-USB-load validation; 5.1 V / 3 A recommended |
| Validated PSU | 5.1 V / 3 A |
| Cooling | exact configuration must pass bounded stress without Pi throttle/temperature flags |
| Validated cooling | case + heatsink + **fan enabled** |
| Rejected cooling | same case + heatsink with **fan absent** for the tested 300-second stress envelope |
| Reference OS | Raspberry Pi OS Lite 64-bit |

The validated fan requirement applies to this tested Raspberry Pi 4 enclosure/reference setup. Equivalent cooling is acceptable on other hardware when the same acceptance gates pass.

### 2.3 Storage policy

Raspberry Pi's current official microSD products are A2, while Raspberry Pi has also recommended A1-class cards for application workloads. IHAP-52 therefore does not invent an A2-only requirement.

The owned A1 card passed the deterministic write/read/SHA-256 integrity gate in the successful physical run. Final endurance and retention remain `[UNVALIDATED]`.

### 2.4 Power policy

Raspberry Pi documents 5 V / 3 A as the normal Pi 4 input requirement and notes that a good-quality 2.5 A supply can be used when downstream USB peripheral load remains below 500 mA.

IHAP-52 therefore uses 2.5 A only as the bounded low-peripheral validation floor and retains 5.1 V / 3 A as the recommended replication reference. The initial 5 V / 1.55 A supply was correctly rejected before stress execution.

### 2.5 Reference OS

The operator selects Raspberry Pi OS Lite 64-bit through Raspberry Pi Imager and the harness records the actual runtime OS/kernel. The successful run reported `Debian GNU/Linux 13 (trixie)`, consistent with the current Raspberry Pi OS Lite base.

Alpine Linux remains a compatible future candidate and requires separate reproducibility validation before reference promotion.

### 2.6 Support tiers

| Tier | Meaning |
|---|---|
| Minimum compliant | Meets the hardware/OS-family contract; no runtime guarantee implied |
| Compatible candidate | Documented specifications appear compliant; HomeEdge physical/runtime evidence incomplete |
| Community validated | Reproducible HomeEdge validation run passes reviewed gates |
| Recommended reference | Community-validated profile recommended for reproduction/onboarding |

The fan-enabled Raspberry Pi 4 reference configuration has passing reviewed physical evidence and is the accepted HomeEdge reference implementation for this ADR. Equivalent hardware remains eligible through the vendor-neutral minimum profile and equivalent validation gates.

---

## 3. Physical Validation Evidence

### 3.1 Initial pre-flight

The first pre-flight confirmed Pi 4 identity, ARM64, 4 CPUs, ~8.2 GB RAM, ~30.8 GB root filesystem, Wi-Fi, clean repository state and clean `vcgencmd` history.

It also exposed:

- A1 card rather than A2: policy corrected to A1/A2 accepted;
- 5 V / 1.55 A PSU: rejected as under-rated for the acceptance stress run.

### 3.2 Passive-cooling full run — FAIL

Run: `pi4b-20260905T111348Z`

Configuration: Pi 4 Rev 1.4 / 8 GB / A1 / 5.1 V 3 A / case / heatsink / **no fan**.

Key results:

- architecture/resource/network/repository gates: PASS;
- storage integrity: PASS;
- stress workers: PASS;
- boot stability: PASS;
- no OOM pattern: PASS;
- maximum observed CPU temperature: **84.724 °C**;
- Pi throttle/undervoltage gate: **FAIL**;
- overall: **FAIL**.

Disposition: passive cooling in this reference enclosure is rejected for the 300-second bounded stress envelope.

### 3.3 Fan-enabled full run — PASS

Run: `pi4b-20260905T112848Z`

Configuration: same Pi 4 reference platform, A1 storage and 5.1 V / 3 A PSU, with **fan installed/enabled**.

Key results:

- all architecture/resource/network/repository gates: PASS;
- storage integrity: PASS;
- stress workers: PASS;
- boot stability: PASS;
- no OOM pattern: PASS;
- no Pi undervoltage: PASS;
- no Pi frequency cap/throttling: PASS;
- no Pi soft-temperature limit: PASS;
- maximum observed CPU temperature: **64.757 °C**;
- post-run throttle word: **`0x0 (none)`**;
- overall: **PASS**.

This establishes a reproducible physical PASS for the bounded IHAP-52 hardware/resource envelope.

It does **not** prove final HomeEdge service workload sufficiency, database/container behavior, storage retention/endurance or AI performance.

---

## 4. Alternatives Considered

| Alternative | Outcome | Reason |
|---|---|---|
| Raspberry Pi 4 Model B >=4 GB | Accepted reference with passing physical evidence | Available specimen, mature Linux support, no new board purchase required |
| Raspberry Pi 5 >=4 GB | Compatible newer candidate | More headroom; no HomeEdge physical evidence yet |
| Raspberry Pi 3 Model B+ | Not recommended | 1 GB RAM below minimum |
| Raspberry Pi Zero 2 W | Rejected for central node | 512 MB RAM below minimum |
| x86_64 mini-PC / thin client | Compatible candidate | Good CPU/RAM/storage options; model variability requires validation |
| Reused x86_64 laptop/desktop | Compatible candidate | Valid reuse path; reproducibility/power/support vary |
| Cloud-only runtime | Rejected as central-node replacement | Conflicts with local-first central-node boundary |
| Raspberry Pi OS Lite 64-bit | First reference OS | Official headless Pi path with minimal overhead |
| Alpine Linux aarch64 | Compatible distro candidate | Separate persistence/install reproducibility validation required |
| 32 GB A1 microSD | Validated media | Passed bounded storage integrity and full hardware run |
| 32 GB A2 microSD | Recommended replication media | Current official Raspberry Pi cards are A2; better random-I/O characteristics |

---

## 5. Consequences

### Positive

- Hardware requirements remain vendor-neutral.
- Existing Pi 4 and A1 storage are sufficient for the bounded hardware reference validation.
- A2 remains a recommendation rather than an artificial blocker.
- The first physical reference has a reproducible PASS configuration.
- Equivalent ARM64/x86_64 replacements remain possible.
- No GPIO/GPU dependency is introduced.

### Negative / trade-offs

- The tested Pi 4 enclosure requires active fan cooling for this stress envelope.
- 32 GB has limited capacity headroom; endurance/retention remain unknown.
- A1 may have lower random-I/O performance than A2 outside this bounded test.
- Supporting ARM64 and x86_64 increases future IaC/build validation scope.
- A hardware PASS does not prove final service workload sufficiency.

### Operational

- Use the committed guided harness for reproduction.
- Record exact storage, PSU, enclosure and cooling configuration.
- For the validated Pi 4 reference enclosure, enable the fan.
- A passing hardware run does not authorize Docker/database/AI claims.

---

## 6. Related Risks and Treatments

| Risk / exposure | Treatment | Remaining exposure |
|---|---|---|
| Power instability / undervoltage | PSU rating pre-flight + `vcgencmd` pre/during/post gates | Long-term PSU reliability remains outside bounded run |
| Thermal throttling | live temperature/throttle sampling + fan-enabled validated reference | Long-duration/production thermal envelope remains outside IHAP-52 |
| Storage corruption | deterministic write/read/SHA-256 smoke test | microSD endurance/retention remains `[UNVALIDATED]` |
| Resource instability | bounded CPU stress, worker/boot/OOM checks | final application workload remains `[UNVALIDATED]` |
| Vendor lock-in | ARM64/x86_64 equivalent-device contract; no Pi GPIO dependency | future IaC must preserve portability |

No residual application/runtime risk is accepted by this ADR.

---

## 7. Follow-up Work

| Item | Tracking |
|---|---|
| ADR-0006 accepted by Project Owner on 2026-09-05 | IHAP-52 |
| Propagate accepted central-node BOM/cost profile | IHAP-17 / IHAP-43 |
| Validate Pi 5 / x86_64 references when useful | Future hardware validation |
| Validate Alpine Linux as alternate reference distro | Future infrastructure/runtime validation |
| Implement portable IaC | Future infrastructure task |
| Benchmark final services/storage/write rate | Future runtime tasks |
| Select/benchmark AI runtime/accelerator only if approved | Future AI task |

---

## 8. Evidence Links

| Evidence | Link |
|---|---|
| Jira issue | [IHAP-52](https://niccolopiazzi01.atlassian.net/browse/IHAP-52) |
| Pull request | [PR #30](https://github.com/pianic2/homeedge-ai-platform/pull/30) |
| Evidence index | [IHAP-52 evidence](../evidence/IHAP-52/README.md) |
| Passive-cooling FAIL | [pi4b-20260905T111348Z](../evidence/IHAP-52/summaries/pi4b-20260905T111348Z-summary.md) |
| Fan-enabled PASS | [pi4b-20260905T112848Z](../evidence/IHAP-52/summaries/pi4b-20260905T112848Z-summary.md) |
| Hardware comparison | [Central-node comparison](../evidence/IHAP-52/central-node-hardware-comparison.md) |
| Validation runbook | [Central-node validation runbook](../evidence/IHAP-52/central-node-validation-plan.md) |
| Quick commands | [Quick test commands](../../tools/hardware-validation/ihap-52-central-node/QUICKSTART.md) |
| Validation harness | [IHAP-52 harness](../../tools/hardware-validation/ihap-52-central-node/README.md) |
| Raspberry Pi 4 specifications | https://www.raspberrypi.com/products/raspberry-pi-4-model-b/specifications/ |
| Raspberry Pi official setup | https://www.raspberrypi.com/documentation/computers/getting-started.html |
| Raspberry Pi OS images | https://www.raspberrypi.com/software/operating-systems/ |
| Raspberry Pi SD cards | https://www.raspberrypi.com/documentation/accessories/sd-cards.html |
| Raspberry Pi thermal/frequency management | https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#frequency-management-and-thermal-control |
| Alpine Raspberry Pi documentation | https://wiki.alpinelinux.org/wiki/Raspberry_Pi |

---

## 9. Review Notes

```text
[x] ADR numbering reconciled against current main.
[x] Accepted ADR-0003/0004/0005 remain untouched.
[x] Vendor-neutral ARM64/x86_64 portability preserved.
[x] Nominal >=32 GB storage baseline preserved.
[x] A1 or A2 accepted; A2 recommended for new purchases/reference replication.
[x] Raspberry Pi OS Lite 64-bit retained as first reference image.
[x] PSU policy validated; 5.1 V / 3 A reference run passed.
[x] Passive no-fan reference enclosure rejected by physical evidence.
[x] Fan-enabled reference enclosure passed full bounded validation.
[x] Successful run: 64.757 °C maximum, post-run throttled=0x0, all reported gates PASS.
[x] Docker, database, orchestration, Kafka and final AI runtime remain separate decisions.
[x] Workload sufficiency, storage endurance/retention and AI acceleration remain [UNVALIDATED].
[x] Physical Raspberry Pi 4 validation evidence has passed technical review.
[x] Project Owner explicitly accepted ADR-0006 on 2026-09-05.
```
