# IHAP-52 — Central Node Validation Runbook

## Purpose

Canonical operator procedure for the first HomeEdge central-node hardware validation.

The procedure intentionally minimizes operator work. All checks that can be established by software are executed by the harness. The operator supplies only physical facts that the operating system cannot prove.

Reference configuration:

- Raspberry Pi 4 Model B >=4 GB; first specimen: owned 8 GB board;
- 32 GB A2 microSD;
- Raspberry Pi OS Lite 64-bit;
- Wi-Fi required; Ethernet optional;
- manufacturer-supported USB-C PSU;
- tested enclosure/cooling recorded exactly.

A PASS proves only this bounded hardware/resource smoke-test envelope. Final service capacity, microSD endurance/retention, Docker/container behavior, database behavior and AI acceleration remain `[UNVALIDATED]`.

---

## 1. Install Raspberry Pi OS Lite 64-bit

Use the current Raspberry Pi Imager and official headless guidance:

- https://www.raspberrypi.com/documentation/computers/getting-started.html
- https://www.raspberrypi.com/software/operating-systems/

In Imager:

1. select Raspberry Pi 4;
2. select the current Raspberry Pi OS Lite 64-bit image;
3. select the 32 GB A2 card;
4. configure a non-default user/credential;
5. configure Wi-Fi and wireless country;
6. enable SSH;
7. write and verify the image.

Do not hard-code a Raspberry Pi OS release number into the validation. The harness records the actual OS under test so later reproductions remain comparable when the official image changes.

Raspberry Pi's current documentation recommends Lite for headless setups and supports Wi-Fi/SSH customisation through Imager. The 32 GB decision is a HomeEdge storage baseline; OS installation size does not prove final HomeEdge retention or card endurance.

Alpine Linux remains a future compatible candidate and is not part of this acceptance run:

https://wiki.alpinelinux.org/wiki/Raspberry_Pi

---

## 2. First boot and minimal prerequisites

Boot using the exact PSU/case/cooling configuration to be validated and connect over Wi-Fi/SSH.

Install only the prerequisites needed by the committed harness:

```bash
sudo apt update
sudo apt install -y git python3 iproute2 util-linux
```

A full `apt full-upgrade` is **not** an IHAP-52 test prerequisite. Avoid spending time changing the software baseline merely to run a hardware gate. The exact installed OS/kernel is evidence.

Verify Raspberry Pi diagnostics once:

```bash
command -v vcgencmd
vcgencmd get_throttled
```

For the Pi 4 reference profile `vcgencmd` is mandatory. The guided harness also checks it automatically.

---

## 3. Retrieve the exact IHAP-52 branch

```bash
cd ~
git clone https://github.com/pianic2/homeedge-ai-platform.git 2>/dev/null || true
cd ~/homeedge-ai-platform
git fetch origin
git checkout ihap-52-central-node-hardware-decision
git pull --ff-only origin ihap-52-central-node-hardware-decision
```

The harness records the tested Git commit and rejects a dirty worktree. Do not edit validation code locally before a run.

---

## 4. Fast pre-flight

Recommended before the full test:

```bash
python3 tools/hardware-validation/ihap-52-central-node/validate_central_node.py --guided --dry-run
```

The guided prompts request only:

- A2 marking confirmation;
- confirmation that Raspberry Pi OS Lite 64-bit was selected in Imager;
- microSD model when known;
- PSU/rating;
- case;
- heatsink/fan;
- optional approximate ambient temperature.

The script automatically checks board identity, architecture, CPU, RAM, root capacity, Wi-Fi, repository state and Raspberry Pi power/throttle diagnostics. A mandatory failure stops before storage/stress work.

For the reference Pi 4 run, `get_throttled=0x0` is required before stress. Existing historical throttle/undervoltage/frequency-cap/soft-temperature bits make the run ambiguous, so reboot with the intended PSU/cooling configuration and repeat the pre-flight. If the history immediately reappears, investigate the hardware/power condition.

---

## 5. Canonical physical validation

Run exactly:

```bash
python3 tools/hardware-validation/ihap-52-central-node/validate_central_node.py --guided
```

Defaults:

- unique run ID generated automatically;
- 128 MiB deterministic write/read/hash storage test;
- 300-second bounded CPU stress;
- up to 8 workers, with Pi 4 naturally using its four logical CPUs;
- automatic boot-identity and OOM observation;
- automatic post-stress `vcgencmd` gate;
- automatic Markdown/JSON evidence.

Do not change PSU, network path, storage, case or cooling while the stress phase is active.

Expected duration after prompts is approximately five minutes plus storage I/O, not hours.

---

## 6. Automated PASS gates

A canonical Pi 4 run is PASS only if every mandatory check is true:

| Gate | Condition |
|---|---|
| Reference board | Raspberry Pi 4 Model B |
| Architecture | ARM64/AArch64 |
| CPU | >=4 logical processors |
| RAM | >=4,000,000,000 bytes |
| Root capacity | >=28,000,000,000 bytes |
| Wi-Fi | wireless interface `up` with non-link-local address |
| Repository | commit recorded; worktree clean |
| Physical evidence | A2 + Raspberry Pi OS Lite 64-bit confirmed; PSU rating recorded |
| Pi pre-flight | `vcgencmd` available; throttle/power history clean |
| Storage | exact requested bytes; SHA-256 write/read match; temp file removed |
| CPU stress | every worker exits `0` |
| Boot stability | boot ID unchanged |
| OOM | no OOM signature when kernel log is readable |
| Pi post-flight | no current/historical undervoltage, throttle, frequency-cap or soft-temp flags |

CPU temperature is recorded as evidence but no invented HomeEdge temperature threshold is imposed. Graphics/render-device exposure is also recorded but is not an MVP hardware acceptance gate because GPU acceleration is outside the current MVP requirement.

---

## 7. Evidence

Every attempt receives a new directory; existing runs are never overwritten:

```text
tools/hardware-validation/ihap-52-central-node/runs/<generated-run-id>/
├── operator-notes.md
├── validation.json
└── validation.md
```

Read the latest result:

```bash
RUN_DIR=$(find tools/hardware-validation/ihap-52-central-node/runs -mindepth 1 -maxdepth 1 -type d | sort | tail -n1)
cat "$RUN_DIR/validation.md"
python3 -m json.tool "$RUN_DIR/validation.json" >/dev/null && echo 'JSON OK'
```

Raw run directories stay local and are ignored by Git.

---

## 8. Failure classification

Use the first applicable category:

- `CONFIGURATION` — wrong OS/setup/repository state;
- `PSU_UNDERVOLTAGE` — Raspberry Pi power diagnostics fail;
- `WIFI` — required wireless path unavailable;
- `THERMAL` — repeatable thermal throttling/soft-limit evidence;
- `STORAGE` — capacity or write/read integrity failure;
- `MINIMUM_PROFILE` — board/CPU/RAM/storage profile mismatch;
- `HARNESS_DEFECT` — validation logic is wrong;
- `HARDWARE_OR_WORKLOAD_BLOCKER` — reproducible bounded-test failure not explained by setup/tooling.

A failed run is retained. Do not rerun into the same directory.

---

## 9. Harness regression tests

Before or after hardware execution, validate the decision engine without a Raspberry Pi:

```bash
python3 -m unittest discover \
  -s tools/hardware-validation/ihap-52-central-node/tests \
  -p 'test_*.py' -v
```

These tests must stay green whenever the harness is changed.

---

## 10. Privacy and publication

The harness does not intentionally persist SSID, Wi-Fi credentials, hostname, username, MAC address or private IP. Review local evidence before publishing a sanitized summary.

The profile may move to `Community validated` / `Recommended reference` only after:

1. canonical guided run PASS;
2. evidence integrity/privacy review;
3. required specialist review;
4. Project Owner acceptance of ADR-0006.

Until then the Raspberry Pi 4 remains the reference/validation candidate and workload/endurance claims remain `[UNVALIDATED]`.
