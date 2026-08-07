# IHAP-52 — Central Node Validation Runbook

## Purpose

This document is the canonical operator runbook for the first HomeEdge central-node hardware validation.

It is intentionally procedural. An operator should be able to start from an unprepared Raspberry Pi 4 Model B and a 32 GB A2 microSD card, follow the steps in order, and produce the same classes of evidence with the same validation harness and acceptance gates.

The first reference configuration is:

- Raspberry Pi 4 Model B;
- at least 4 GB RAM; the first project specimen has 8 GB;
- 32 GB A2 microSD;
- Raspberry Pi OS Lite 64-bit;
- Wi-Fi connectivity;
- manufacturer-supported USB-C power supply, preferably the official Raspberry Pi 4 15 W / 5.1 V 3 A class;
- enclosure, heatsinks and fan recorded exactly as installed.

A passing run validates only this bounded hardware/OS smoke-test envelope. Final HomeEdge workload capacity, microSD endurance, final retention, Docker/container behavior and AI inference/acceleration remain `[UNVALIDATED]`.

---

## 1. Required material

Before starting, prepare:

- Raspberry Pi 4 Model B with >=4 GB RAM;
- 32 GB or larger A2 microSD;
- supported Raspberry Pi 4 USB-C power supply;
- another computer able to run Raspberry Pi Imager;
- local Wi-Fi credentials;
- a computer on the same local network with an SSH client;
- optional case, heatsinks and fan in the exact configuration you want to test.

Do not change cooling, PSU, storage or enclosure during a run. If one of these changes, start a new run ID.

---

## 2. Install the reference operating system

Use Raspberry Pi's official installation documentation:

https://www.raspberrypi.com/documentation/computers/getting-started.html#install-an-operating-system

Official Raspberry Pi OS image catalogue:

https://www.raspberrypi.com/software/operating-systems/

For the first IHAP-52 validation select:

1. **Device:** Raspberry Pi 4.
2. **Operating system:** Raspberry Pi OS Lite (64-bit).
3. **Storage:** the 32 GB A2 microSD selected for the MVP test.
4. Open the Raspberry Pi Imager OS customisation screen.
5. Set an operator-chosen hostname.
6. Set a non-default username and password or SSH key.
7. Configure the Wi-Fi SSID, password and correct wireless-LAN country.
8. Configure locale/time zone for the operator environment.
9. Enable SSH.
10. Write the image and allow Raspberry Pi Imager to complete its verification.

The official Raspberry Pi documentation recommends Raspberry Pi OS Lite for headless systems and supports configuring networking and remote access in Imager.

For repeatability, record the exact Raspberry Pi OS version observed after first boot. Do not assume that a future operator will receive the same image release from Imager.

### Alpine Linux boundary

Alpine Linux remains a compatible lightweight candidate but is **not** used for the first acceptance run.

Official Alpine Raspberry Pi documentation:

https://wiki.alpinelinux.org/wiki/Raspberry_Pi

A future Alpine validation must use a separate run ID and must record its installation mode because Alpine supports materially different persistence models. It must not be mixed into the Raspberry Pi OS reference run.

---

## 3. Assemble and boot the specimen

1. With power disconnected, insert the prepared microSD.
2. Install the selected case, heatsinks and/or fan.
3. Connect only the peripherals required for the intended central-node configuration.
4. Connect the supported USB-C PSU.
5. Power on the Raspberry Pi.
6. Allow the first boot to complete.
7. Confirm from another computer that the Raspberry Pi appears on the configured Wi-Fi network.

The validation must be performed over Wi-Fi because Wi-Fi is a mandatory part of the accepted central-node profile. Ethernet may be physically present but must not be the only active network path used to satisfy the network gate.

---

## 4. Connect over SSH

From the operator computer:

```bash
ssh <username>@<hostname>.local
```

If `.local` name resolution is unavailable, use the Raspberry Pi's local IP address obtained from the operator's router/network tooling. Do not publish that address in repository evidence.

Confirm that the shell is running on the Raspberry Pi before continuing:

```bash
uname -a
cat /proc/device-tree/model 2>/dev/null || true
```

Expected model text for the reference specimen should identify a Raspberry Pi 4 Model B.

---

## 5. Update the reference OS

Run:

```bash
sudo apt update
sudo apt full-upgrade -y
sudo reboot
```

The SSH connection will close during reboot.

Reconnect:

```bash
ssh <username>@<hostname>.local
```

The purpose of updating before validation is to avoid comparing an unpatched first-boot image with a later reproduction. The exact resulting OS/kernel version is captured by the harness.

---

## 6. Install validation prerequisites

Run:

```bash
sudo apt install -y git python3 iproute2 util-linux iputils-ping
```

Verify:

```bash
python3 --version
git --version
ip -Version
lsblk --version
```

On Raspberry Pi OS also verify that the firmware diagnostic command is available:

```bash
command -v vcgencmd
vcgencmd get_throttled
```

For the Raspberry Pi reference run, `vcgencmd` should be available. If it is not available, **do not silently ignore it**: record the condition and stop before claiming clean Raspberry Pi power/throttling evidence.

A normal clean current state is expected to report a value with no current undervoltage or throttling bits set. Historical bits, if present, must remain visible in the raw evidence and be reviewed.

---

## 7. Retrieve the exact IHAP-52 validation code

Choose a working directory and clone the repository:

```bash
cd ~
git clone https://github.com/pianic2/homeedge-ai-platform.git
cd homeedge-ai-platform
```

Fetch and check out the single IHAP-52 branch:

```bash
git fetch origin
git checkout ihap-52-central-node-hardware-decision
git pull --ff-only origin ihap-52-central-node-hardware-decision
```

Record the exact commit being tested:

```bash
git rev-parse HEAD
```

Do not edit the harness locally before the test. If the harness requires a fix, fix it on the same IHAP-52 branch first and restart the validation from the new commit.

---

## 8. Create a unique local run directory

Use a new run ID for every attempt. For the first reference run:

```bash
export IHAP52_RUN_ID="pi4b-reference-01"
export IHAP52_RUN_DIR="tools/hardware-validation/ihap-52-central-node/runs/${IHAP52_RUN_ID}"
mkdir -p "${IHAP52_RUN_DIR}"
```

The harness-local `runs/` directory is ignored by Git.

Never overwrite a previous attempt. If the run must be repeated, use `pi4b-reference-02`, then `-03`, and so on.

---

## 9. Record manual configuration before testing

Software cannot reliably identify the physical PSU, A2 marking or cooling assembly. Record these before running the harness.

Create:

```bash
nano "${IHAP52_RUN_DIR}/operator-notes.md"
```

Use this exact template:

```text
# IHAP-52 Operator Notes

Run ID: pi4b-reference-01
Board/model: Raspberry Pi 4 Model B
Installed RAM: 8 GB
microSD manufacturer/model: <fill in>
microSD labelled capacity: 32 GB
A2 marking visually confirmed: yes/no
OS selected in Raspberry Pi Imager: Raspberry Pi OS Lite 64-bit
Official Raspberry Pi installation procedure followed: yes/no
PSU manufacturer/model: <fill in>
PSU electrical rating: <fill in>
Case: <fill in / none>
Heatsinks installed: yes/no
Fan installed: yes/no
Approximate ambient temperature: <fill in or unknown>
Operator notes: <optional>
```

Do not put Wi-Fi SSID, Wi-Fi password, private IP, MAC address, hostname, username or other credentials in this file.

The reference run is invalid for final promotion if the A2 marking cannot be confirmed or the actual physical configuration is not recorded.

---

## 10. Perform the pre-flight checks

Run the following commands exactly:

```bash
uname -m
cat /etc/os-release
nproc
free -b
df -B1 /
lsblk -b -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS,MODEL
ip link
vcgencmd get_throttled
```

Check these conditions before the automated stress run:

| Check | Required pre-flight result |
|---|---|
| Architecture | `aarch64` / ARM64 |
| Board | Raspberry Pi 4 Model B |
| Logical CPUs | >=4 |
| Physical RAM | >=4 GB |
| Storage | nominal 32 GB or larger microSD/reference storage |
| OS | Raspberry Pi OS Lite 64-bit selection recorded; runtime architecture is 64-bit |
| Wi-Fi | wireless interface exists and is enabled |
| Power diagnostics | `vcgencmd get_throttled` available |

If one of the mandatory minimum hardware checks fails, **stop**. Do not run the stress phase merely to generate an output file.

If the pre-flight issue is configuration-only, correct it and restart with the same run ID only if no actual validation workload has started. Once the automated harness starts, any retry gets a new run ID.

---

## 11. Run the canonical automated validation

From the repository root run:

```bash
python3 tools/hardware-validation/ihap-52-central-node/validate_central_node.py \
  --output-dir "${IHAP52_RUN_DIR}" \
  --stress-seconds 300 \
  --storage-mib 128
```

Do not use the Raspberry Pi for unrelated work during the 300-second stress phase.

Do not change network connection, PSU, cooling, enclosure or storage while the command is running.

### Optional local Wi-Fi reachability observation

If an authorized stable host exists on the same LAN, a separate run may include:

```bash
python3 tools/hardware-validation/ihap-52-central-node/validate_central_node.py \
  --output-dir "${IHAP52_RUN_DIR}" \
  --stress-seconds 300 \
  --storage-mib 128 \
  --wifi-host <authorized-local-address>
```

Do not use a public Internet host merely to obtain a PASS. Internet connectivity is not an IHAP-52 requirement.

For the canonical first run, the optional ping is not required.

---

## 12. Interpret the command result

The harness exit codes are:

- `0`: every applicable automated mandatory gate passed;
- `2`: at least one applicable automated mandatory gate failed;
- another non-zero code: execution/configuration error that must be investigated before treating the run as evidence.

Immediately after the command finishes run:

```bash
printf 'harness_exit_code=%s\n' "$?"
```

If you need to preserve the exit code reliably, prefer:

```bash
python3 tools/hardware-validation/ihap-52-central-node/validate_central_node.py \
  --output-dir "${IHAP52_RUN_DIR}" \
  --stress-seconds 300 \
  --storage-mib 128
HARNESS_EXIT=$?
printf 'harness_exit_code=%s\n' "${HARNESS_EXIT}"
```

Do not rerun the command into the same directory to turn a failed run into a pass.

---

## 13. Verify the generated evidence

The run directory must contain at least:

```text
tools/hardware-validation/ihap-52-central-node/runs/<run-id>/
├── operator-notes.md
├── validation.json
└── validation.md
```

Verify:

```bash
ls -la "${IHAP52_RUN_DIR}"
python3 -m json.tool "${IHAP52_RUN_DIR}/validation.json" >/dev/null
cat "${IHAP52_RUN_DIR}/validation.md"
```

The JSON syntax check must complete without error.

The Markdown summary must show the automated gate result and the observed system characteristics.

---

## 14. Mandatory PASS / FAIL gates

A run can be considered a candidate PASS only when all applicable mandatory conditions below are satisfied.

| Gate | PASS condition |
|---|---|
| Architecture | 64-bit `aarch64`/`arm64` or accepted x86_64 equivalent |
| CPU | >=4 logical processors |
| RAM | >=4,000,000,000 bytes reported |
| Storage capacity | root filesystem >=28,000,000,000 bytes, accommodating normal nominal-32-GB partition/format overhead |
| Storage integrity | exact bytes written/read and deterministic SHA-256 write/read hashes match |
| Wi-Fi | wireless interface is up and has a non-link-local IP address |
| Graphics/compute exposure | expected Linux graphics/render device is detected for the reference profile |
| CPU stress | every worker exits successfully |
| Current undervoltage | no current undervoltage flag after stress |
| Current throttling | no current throttling flag after stress |
| Stability | no crash, reboot, OOM or operator intervention during the run |
| Manual configuration | board, RAM, A2 storage, PSU, OS and cooling configuration recorded |

Temperature samples are evidence, not a fabricated project threshold. Review them together with ambient conditions, enclosure/cooling and firmware throttling state.

The run does **not** prove microSD write endurance or final application capacity.

---

## 15. Post-run Raspberry Pi checks

After the automated command, run:

```bash
vcgencmd get_throttled
uptime
free -b
df -h /
```

Compare the throttling result with the harness output.

If the system rebooted unexpectedly, became unreachable, reported current undervoltage/throttling, or required manual recovery, classify the run as failed even if partial output files exist.

---

## 16. Failure classification

Do not immediately change the architecture decision after one failed run. First classify the failure.

Use exactly one primary category:

- `CONFIGURATION` — OS/network/package/operator setup error;
- `PSU_UNDERVOLTAGE` — current or repeatable supply problem;
- `WIFI` — required wireless interface/connectivity gate failure;
- `THERMAL` — repeatable throttling/stability problem associated with temperature/cooling;
- `STORAGE` — capacity, write/read or integrity gate failure;
- `MINIMUM_PROFILE` — specimen does not meet accepted CPU/RAM/storage/network requirements;
- `HARNESS_DEFECT` — validation tool itself is incorrect;
- `HARDWARE_OR_WORKLOAD_BLOCKER` — reproducible failure under the bounded test that cannot be explained by setup/tooling.

Record the classification in `operator-notes.md` for failed attempts.

Any harness/documentation fix remains on the same IHAP-52 branch and PR #30. A new validation attempt must use a new run ID.

---

## 17. Privacy review before publication

Raw runs remain local by default.

Before sharing or committing any derived evidence, inspect:

```bash
cat "${IHAP52_RUN_DIR}/operator-notes.md"
cat "${IHAP52_RUN_DIR}/validation.md"
python3 -m json.tool "${IHAP52_RUN_DIR}/validation.json"
```

Remove or redact any unintended:

- username;
- hostname;
- SSID;
- private IP;
- MAC address;
- credential;
- workstation-specific path or identifier not needed for technical review.

Do not edit the raw local evidence solely to hide a failed gate. Preserve the original locally and create a separate sanitized public summary.

---

## 18. Evidence promotion rule

The Raspberry Pi 4 profile may move from `reference/validation candidate` to `Community validated` / `Recommended reference` only when:

1. the physical configuration matches the declared reference profile;
2. the canonical run completes;
3. all mandatory gates pass;
4. raw evidence is reviewed for privacy and integrity;
5. a sanitized summary is added under `docs/evidence/IHAP-52/summaries/`;
6. Testing & Evidence, Hardware Compatibility and remaining required reviews find no open BLOCKER/MAJOR issue;
7. the Project Owner explicitly accepts the resulting ADR.

Until then ADR-0003 remains `Proposed` and IHAP-52 remains `In corso`.

---

## 19. What this validation deliberately does not decide

Even after a PASS, the following remain separate work:

- final HomeEdge service/container topology;
- Docker or another container runtime;
- database technology;
- telemetry retention policy;
- microSD endurance under the final write pattern;
- Alpine Linux as an officially validated HomeEdge reference distro;
- final AI model/runtime;
- VideoCore/GPU/NPU acceleration suitability;
- external AI accelerator selection;
- production/high-availability/security-grade qualification.

Those claims remain `[UNVALIDATED]` unless a later task provides specific evidence.
