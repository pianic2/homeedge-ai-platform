# IHAP-52 — Central Node Hardware Evidence

## Current state

- Jira: `IHAP-52`
- ADR: `ADR-0006 — MVP Central Node Hardware Profile`
- ADR status: `Proposed`
- PR: `#30`
- reference candidate: Raspberry Pi 4 Model B >=4 GB
- first specimen: owned Raspberry Pi 4 Model B 8 GB
- storage baseline: nominal **32 GB microSD; A1 or A2 accepted**
- A2: recommended for new purchases/reference replication
- reference OS: **Raspberry Pi OS Lite 64-bit**
- Wi-Fi required; Ethernet optional
- reference PSU: 5.1 V / 3 A recommended; >=2.5 A accepted only for the bounded low-USB-load Pi 4 validation
- first full physical stress run: **FAIL on combined Pi throttle/undervoltage gate** with 84.724 °C maximum observed CPU temperature
- next candidate: same platform with improved airflow / fan enabled and clean post-reboot throttle history

`ADR-0006` replaces the stale branch-local ADR-0003 number only. Current `main` already uses ADR-0003, ADR-0004 and ADR-0005 for accepted door/display/presence decisions.

## First physical pre-flight — 2026-09-05

The first guided pre-flight ran successfully up to the policy gates and intentionally did not start the storage/stress phase because pre-flight failed.

Observed automated PASS evidence:

| Gate / observation | Result |
|---|---|
| Raspberry Pi model | Raspberry Pi 4 Model B Rev 1.4 |
| Architecture | `aarch64` |
| Logical CPUs | 4 |
| RAM | 8,199,639,040 bytes reported |
| Root filesystem | 30,825,431,040 bytes |
| Wi-Fi | PASS |
| Repository commit recorded | PASS |
| Repository clean | PASS |
| Pi 4 identity | PASS |
| `vcgencmd` available | PASS |
| Current/historical pre-run throttle/undervoltage | clean / PASS |
| Raspberry Pi OS Lite 64-bit Imager selection | operator confirmed |
| Runtime base OS | Debian GNU/Linux 13 (trixie), expected current Raspberry Pi OS base |

Physical facts discovered:

- the owned 32 GB microSD is **A1**, not A2;
- case installed;
- heatsink installed;
- fan not installed;
- approximate ambient temperature: 28 °C;
- tested PSU label: **5 V / 1.55 A**.

### Pre-flight disposition

The initial A2-only gate was a harness/profile defect: Raspberry Pi has documented A1 as a suitable application class, while current official cards are A2. The profile is therefore corrected to accept **A1 or A2**, with A2 recommended for new purchases.

The 5 V / 1.55 A PSU is a real blocker for the acceptance stress run. Raspberry Pi specifies 5 V / 3 A for Pi 4 and permits a good-quality 2.5 A supply only when downstream USB load remains below 500 mA. IHAP-52 therefore requires >=2.5 A for its bounded low-peripheral validation and recommends 5.1 V / 3 A for replication.

This pre-flight is evidence of configuration/profile discovery, **not** a rejection of Raspberry Pi 4.

## First full bounded run — 2026-09-05

Sanitized evidence:

- [`summaries/pi4b-20260905T111348Z-summary.md`](summaries/pi4b-20260905T111348Z-summary.md)

Configuration under test:

- Raspberry Pi 4 Model B Rev 1.4;
- Raspberry Pi OS Lite 64-bit / Debian GNU/Linux 13 (trixie);
- 32 GB A1 microSD;
- 5.1 V / 3 A PSU;
- case installed;
- heatsink installed;
- **fan absent**;
- approximate ambient temperature 28 °C.

Result:

- architecture/resource/network/repository gates: PASS;
- storage integrity: PASS;
- all stress workers: PASS;
- boot stability: PASS;
- no OOM pattern: PASS;
- PSU manual policy gate: PASS;
- maximum CPU temperature: **84.724 °C**;
- combined `no_pi_throttle_or_undervoltage`: **FAIL**;
- overall gate: **FAIL**.

Raspberry Pi documentation states that the Arm cores are progressively throttled in the 80–85 °C range. The run is therefore strongly consistent with thermal throttling, but the v5 summary did not publish the exact `vcgencmd get_throttled` bitmask. The sanitized record does not claim bit-level confirmation that was not present in the supplied summary.

### Full-run disposition

The run does **not** reject Raspberry Pi 4, A1 storage, Raspberry Pi OS Lite 64-bit, the 5.1 V / 3 A PSU, storage integrity or basic resource stability.

It rejects the tested **passive cooling configuration** (`case + heatsink, no fan`) for the current bounded 300-second stress envelope.

The harness is remediated after this run to:

- sample/decode `vcgencmd get_throttled` during stress;
- display the throttle word live every ~5 seconds;
- separate final gates for undervoltage, frequency-cap/throttle and soft-temperature flags;
- preserve the same overall clean-throttle acceptance requirement.

Before the next acceptance run, improve cooling, reboot to clear historical firmware flags, verify `vcgencmd get_throttled` is `0x0`, pull the updated branch, run the host suite and repeat pre-flight/full validation.

## Decision/evidence boundary

| Claim | State |
|---|---|
| Pi 4 documented CPU/RAM/network/I/O capabilities | manufacturer fact |
| >=4 GB RAM | HomeEdge minimum-profile decision |
| nominal 32 GB microSD | HomeEdge first reference capacity decision |
| A1/A2 accepted for bounded validation | revised proposed profile based on manufacturer guidance + physical evidence |
| A2 preferred for new purchase/reference replication | recommendation |
| Wi-Fi required | HomeEdge profile decision |
| Pi OS Lite 64-bit first reference image | HomeEdge reference-validation decision |
| passive `case + heatsink, no fan` configuration | **rejected for bounded reference stress** by run `pi4b-20260905T111348Z` |
| active-fan cooling reference | pending next physical run |
| Pi 4 final HomeEdge workload sufficiency | `[UNVALIDATED]` |
| microSD endurance / final retention | `[UNVALIDATED]` |
| GPU/AI acceleration | `[UNVALIDATED]`; not an MVP hardware gate |
| Alpine Linux HomeEdge validation | not established |

## Validation model

Self-test:

```bash
python3 -m unittest discover \
  -s tools/hardware-validation/ihap-52-central-node/tests \
  -p 'test_*.py' -v
```

Pre-flight:

```bash
python3 tools/hardware-validation/ihap-52-central-node/validate_central_node.py --guided --dry-run
```

Canonical physical run, only after pre-flight PASS:

```bash
python3 tools/hardware-validation/ihap-52-central-node/validate_central_node.py --guided
```

The harness performs automated profile, Wi-Fi, repository-integrity, Raspberry Pi power/throttle, storage-integrity, CPU-stress, boot-stability and post-flight gates. Only physical attributes unavailable to Linux are prompted.

Quick commands:

- [`tools/hardware-validation/ihap-52-central-node/QUICKSTART.md`](../../../tools/hardware-validation/ihap-52-central-node/QUICKSTART.md)
- [`central-node-validation-plan.md`](central-node-validation-plan.md)

## Reference replication profile

| Item | Reference | Requirement |
|---|---|---|
| Compute | Raspberry Pi 4 Model B | reference implementation |
| RAM | >=4 GB | mandatory |
| Storage capacity | nominal >=32 GB | mandatory |
| microSD application class | A1 or A2 | accepted for bounded run; A2 recommended for new purchase |
| Wi-Fi | on-board wireless | mandatory |
| Ethernet | Gigabit Ethernet | optional |
| PSU | approximately 5 V, >=2.5 A for bounded low-USB-load run; 5.1 V / 3 A recommended | mandatory stable supply |
| Cooling | exact configuration must pass bounded run without Pi throttle flags | passive case+heatsink/no-fan specimen failed; active-fan candidate pending |
| Enclosure | ventilated case or explicit bench setup | record exact setup |
| OS | Raspberry Pi OS Lite 64-bit | first reference image |
| GPU/accelerator | none required | optional future capability |

## Official sources

- Raspberry Pi headless/getting started: https://www.raspberrypi.com/documentation/computers/getting-started.html
- Raspberry Pi OS images: https://www.raspberrypi.com/software/operating-systems/
- Raspberry Pi 4 specifications: https://www.raspberrypi.com/products/raspberry-pi-4-model-b/specifications/
- Raspberry Pi SD cards: https://www.raspberrypi.com/documentation/accessories/sd-cards.html
- Raspberry Pi thermal/frequency management: https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#frequency-management-and-thermal-control
- Alpine Raspberry Pi documentation: https://wiki.alpinelinux.org/wiki/Raspberry_Pi

## Files

- `central-node-hardware-comparison.md` — alternative comparison/equivalence rules.
- `central-node-validation-plan.md` — canonical physical runbook.
- `PR-SUMMARY.md` — PR-level decision/remediation summary.
- `pre-pr-review-summary.md` — specialist review.
- `summaries/pi4b-20260905T111348Z-summary.md` — first full bounded physical run; passive cooling FAIL.
- `../../adr/ADR-0006-mvp-central-node-hardware-profile.md` — Proposed ADR.
- `../../../tools/hardware-validation/ihap-52-central-node/` — harness, quick-start and host regression tests.

## Publication boundary

Raw run outputs remain local by default. Review and sanitize derived evidence before publication. No SSID, credential, private IP, MAC, hostname or username is required for public evidence.
