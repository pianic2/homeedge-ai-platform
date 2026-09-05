# IHAP-52 — Central Node Validation Runbook

## Purpose

This is the canonical operator procedure for the Raspberry Pi 4 reference validation. It is deliberately short: the harness performs the checks, storage smoke test, stress phase and evidence generation.

A PASS validates only the bounded IHAP-52 hardware envelope. Final HomeEdge workload capacity, microSD endurance/retention, container/database behavior and AI acceleration remain `[UNVALIDATED]`.

## Reference configuration

- Raspberry Pi 4 Model B, >=4 GB RAM;
- nominal 32 GB or larger microSD;
- application class **A1 or A2** accepted for this bounded test;
- A2 recommended for new purchases/reference replication;
- Raspberry Pi OS Lite 64-bit installed with Raspberry Pi Imager;
- Wi-Fi active;
- approximately 5 V PSU rated **>=2.5 A** for the low-USB-load bounded run;
- **5.1 V / 3 A recommended** reference PSU;
- exact case/heatsink/fan configuration recorded.

Raspberry Pi documents 5 V / 3 A as the normal Pi 4 input requirement and allows a good-quality 2.5 A supply when downstream USB devices consume less than 500 mA. A supply below 2.5 A is not accepted for the IHAP-52 stress run.

## 1. Prepare Raspberry Pi OS Lite

Use Raspberry Pi Imager and the official setup guidance:

- https://www.raspberrypi.com/documentation/computers/getting-started.html
- https://www.raspberrypi.com/software/operating-systems/

Select **Raspberry Pi OS Lite 64-bit**, configure Wi-Fi and SSH, then boot the Raspberry Pi.

Current Raspberry Pi OS is Debian-based. A runtime identification such as `Debian GNU/Linux 13 (trixie)` is compatible with a correctly installed current Raspberry Pi OS Lite 64-bit image.

Install only the validation prerequisites:

```bash
sudo apt update
sudo apt install -y git python3 iproute2 util-linux
```

A full OS upgrade is not required solely for IHAP-52.

## 2. Pull the canonical task branch

```bash
cd ~
git clone https://github.com/pianic2/homeedge-ai-platform.git 2>/dev/null || true
cd ~/homeedge-ai-platform
git fetch origin
git checkout ihap-52-central-node-hardware-decision
git pull --ff-only origin ihap-52-central-node-hardware-decision
```

Do not edit the harness locally. A harness fix belongs on this same IHAP-52 branch/PR before a new attempt.

## 3. Run the harness self-test

```bash
python3 -m unittest discover \
  -s tools/hardware-validation/ihap-52-central-node/tests \
  -p 'test_*.py' -v
```

Proceed only when the suite reports `OK`.

## 4. Run pre-flight only

```bash
python3 tools/hardware-validation/ihap-52-central-node/validate_central_node.py --guided --dry-run
```

The harness asks only for facts Linux cannot prove directly:

- microSD application class: `A1`, `A2`, `other` or `unknown`;
- Raspberry Pi OS Lite 64-bit Imager selection confirmation;
- optional card model;
- PSU electrical rating, for example `5.1V 3A`;
- case;
- heatsink/fan;
- approximate ambient temperature.

The pre-flight automatically checks:

- Raspberry Pi 4 identity;
- ARM64 architecture;
- >=4 logical CPUs;
- >=4 GB RAM;
- >=28 GB root filesystem capacity for nominal 32 GB media;
- active Wi-Fi with an IP address;
- repository commit recorded and clean worktree;
- `vcgencmd` availability;
- no current or historical Pi undervoltage/throttling flags;
- microSD class A1/A2;
- Raspberry Pi OS Lite 64-bit operator confirmation;
- parseable/supported PSU rating.

Do **not** run the stress phase after a `PRE-FLIGHT FAIL`.

## 5. Run the canonical physical validation

Only after `PRE-FLIGHT PASS`:

```bash
python3 tools/hardware-validation/ihap-52-central-node/validate_central_node.py --guided
```

The default workload is:

- 128 MiB deterministic storage write/read test with SHA-256 comparison;
- 300 seconds CPU stress;
- temperature samples when the kernel exposes them;
- worker exit validation;
- boot-ID stability check;
- OOM observation when readable;
- post-stress `vcgencmd` power/throttle validation.

The harness creates a unique run directory automatically and never overwrites a previous run.

## 6. Read the result

```bash
RUN_DIR=$(find tools/hardware-validation/ihap-52-central-node/runs \
  -mindepth 1 -maxdepth 1 -type d | sort | tail -n1)

cat "$RUN_DIR/validation.md"
python3 -m json.tool "$RUN_DIR/validation.json" >/dev/null && echo 'JSON OK'
```

A valid candidate PASS requires `Overall gate: PASS`.

A `not reported` maximum CPU temperature is expected on a `--dry-run`, because the stress phase did not run.

## Failure rule

Keep every failed attempt as local evidence. Do not rerun into the same directory and do not weaken a gate just to obtain PASS.

Use these primary classifications:

- `CONFIGURATION`
- `PSU_UNDERVOLTAGE`
- `WIFI`
- `THERMAL`
- `STORAGE`
- `MINIMUM_PROFILE`
- `HARNESS_DEFECT`
- `HARDWARE_OR_WORKLOAD_BLOCKER`

The 2026-09-05 first physical pre-flight is classified as **configuration/profile discovery**, not a hardware rejection: the owned A1 microSD is now accepted by the corrected profile, while the observed 5 V / 1.55 A PSU is below the accepted Pi 4 validation envelope and must be replaced before stress testing.

## Publication/privacy

Raw run directories remain local by default. Before publishing a sanitized summary, ensure it contains no hostname, username, SSID, private IP, MAC address or credentials.

Promotion to `Community validated` / `Recommended reference` requires a clean physical PASS, evidence review and explicit Project Owner acceptance of ADR-0006.
