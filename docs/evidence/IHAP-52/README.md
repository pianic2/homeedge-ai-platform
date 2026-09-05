# IHAP-52 — Central Node Hardware Evidence

## Current state

- Jira: `IHAP-52`
- ADR: `ADR-0006 — MVP Central Node Hardware Profile`
- ADR status: `Accepted` (Project Owner approval 2026-09-05)
- PR: `#30` — open; **not merged**
- reference implementation: Raspberry Pi 4 Model B >=4 GB
- validated specimen: owned Raspberry Pi 4 Model B Rev 1.4, 8 GB
- storage baseline: nominal **32 GB microSD; A1 or A2 accepted**
- A2: recommended for new purchases/reference replication
- reference OS: **Raspberry Pi OS Lite 64-bit**
- Wi-Fi required; Ethernet optional
- reference PSU: **5.1 V / 3 A recommended**; >=2.5 A accepted only for the bounded low-USB-load Pi 4 validation
- validated reference cooling: **case + heatsink + fan enabled**
- latest full bounded physical run: **PASS** (`pi4b-20260905T112848Z`)

`ADR-0006` replaces the stale branch-local ADR-0003 number only. Current `main` already uses ADR-0003, ADR-0004 and ADR-0005 for accepted door/display/presence decisions.

## Evidence timeline — 2026-09-05

### 1. Initial pre-flight

The first guided pre-flight established the board/OS/resource baseline but did not start stress because the operator evidence exposed two issues:

- owned microSD was **A1**, while the harness incorrectly required A2;
- tested PSU was **5 V / 1.55 A**, below the Raspberry Pi 4 validation power envelope.

Observed automated PASS evidence included Raspberry Pi 4 Model B Rev 1.4, `aarch64`, 4 logical CPUs, ~8.2 GB RAM, ~30.8 GB root filesystem, Wi-Fi, clean repository state and clean pre-run `vcgencmd` diagnostics.

Disposition:

- A1/A2 policy corrected: A1 or A2 accepted, A2 recommended for new purchases;
- 5 V / 1.55 A rejected for the stress phase;
- no Raspberry Pi hardware rejection.

### 2. First full bounded run — passive cooling FAIL

Sanitized evidence:

- [`summaries/pi4b-20260905T111348Z-summary.md`](summaries/pi4b-20260905T111348Z-summary.md)

Configuration:

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
- stress workers: PASS;
- boot stability: PASS;
- no OOM pattern: PASS;
- maximum CPU temperature: **84.724 °C**;
- combined Pi throttle/undervoltage gate: **FAIL**;
- overall: **FAIL**.

Disposition: the tested passive configuration (`case + heatsink, no fan`) is rejected for the current 300-second bounded reference stress envelope. This run does not reject Pi 4, A1 storage, Raspberry Pi OS Lite 64-bit, the 5.1 V / 3 A PSU or storage/resource stability.

### 3. Second full bounded run — fan cooling PASS

Sanitized evidence:

- [`summaries/pi4b-20260905T112848Z-summary.md`](summaries/pi4b-20260905T112848Z-summary.md)

Configuration remained the same reference platform, storage and PSU, with the cooling configuration changed to **case + heatsink + fan enabled**.

Result:

- all architecture/resource/network/repository gates: PASS;
- A1 application-class policy: PASS;
- Raspberry Pi OS Lite 64-bit confirmation: PASS;
- PSU policy: PASS;
- storage integrity: PASS;
- stress workers: PASS;
- boot stability: PASS;
- no OOM pattern: PASS;
- no Pi undervoltage: PASS;
- no Pi frequency cap/throttling: PASS;
- no Pi soft-temperature limit: PASS;
- maximum CPU temperature: **64.757 °C**;
- post-run Pi throttle word: **`0x0 (none)`**;
- overall: **PASS**.

Disposition: **the fan-enabled cooling configuration is validated for the tested Raspberry Pi 4 reference enclosure and bounded 300-second stress envelope**. This does not create a universal active-cooling requirement for all equivalent hardware; an equivalent cooling solution may qualify when it passes the same gates.

## Decision/evidence boundary

| Claim | State |
|---|---|
| Pi 4 documented CPU/RAM/network/I/O capabilities | manufacturer fact |
| >=4 GB RAM | accepted HomeEdge minimum-profile decision |
| nominal 32 GB microSD | accepted HomeEdge first reference capacity decision |
| A1/A2 accepted for bounded validation | **Accepted**; A1 has passing physical evidence |
| A2 preferred for new purchase/reference replication | recommendation |
| Wi-Fi required | accepted HomeEdge profile decision |
| Pi OS Lite 64-bit first reference image | accepted HomeEdge reference decision |
| passive `case + heatsink, no fan` configuration | **rejected** for bounded reference stress by `pi4b-20260905T111348Z` |
| `case + heatsink + fan enabled` reference configuration | **validated** by `pi4b-20260905T112848Z` |
| Raspberry Pi 4 reference hardware/resource envelope | **PASS; ADR-0006 Accepted 2026-09-05** |
| final HomeEdge workload sufficiency | `[UNVALIDATED]` |
| microSD endurance / final retention | `[UNVALIDATED]` |
| GPU/AI acceleration | `[UNVALIDATED]`; not an MVP hardware gate |
| Alpine Linux HomeEdge validation | not established |

## Validation model

Host regression suite:

```bash
python3 -m unittest discover \
  -s tools/hardware-validation/ihap-52-central-node/tests \
  -p 'test_*.py' -v
```

Pre-flight:

```bash
python3 tools/hardware-validation/ihap-52-central-node/validate_central_node.py --guided --dry-run
```

Canonical physical run:

```bash
python3 tools/hardware-validation/ihap-52-central-node/validate_central_node.py --guided
```

The harness performs automated profile, Wi-Fi, repository-integrity, Raspberry Pi power/throttle, storage-integrity, CPU-stress, boot-stability and post-flight gates. Only physical attributes unavailable to Linux are prompted.

## Reference replication profile

| Item | Reference | Requirement |
|---|---|---|
| Compute | Raspberry Pi 4 Model B | reference implementation |
| RAM | >=4 GB | mandatory |
| Storage capacity | nominal >=32 GB | mandatory |
| microSD application class | A1 or A2 | accepted; A2 recommended for new purchase |
| Wi-Fi | on-board wireless | mandatory |
| Ethernet | Gigabit Ethernet | optional |
| PSU | approximately 5 V, >=2.5 A for bounded low-USB-load run; 5.1 V / 3 A recommended | mandatory stable supply |
| Cooling | tested reference uses heatsink + active fan | equivalent cooling acceptable only after passing same gates |
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
- `summaries/pi4b-20260905T111348Z-summary.md` — passive-cooling full run; FAIL.
- `summaries/pi4b-20260905T112848Z-summary.md` — fan-cooled full run; PASS.
- `../../adr/ADR-0006-mvp-central-node-hardware-profile.md` — **Accepted ADR**.
- `../../../tools/hardware-validation/ihap-52-central-node/` — harness, quick-start and host regression tests.

## Publication boundary

Raw run outputs remain local by default. Review and sanitize derived evidence before publication. No SSID, credential, private IP, MAC, hostname or username is required for public evidence.
