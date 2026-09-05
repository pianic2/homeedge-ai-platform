# IHAP-52 Central Node Hardware Validation Harness

## Goal

Validate the bounded HomeEdge central-node hardware profile with the same operating model used for the mature IHAP-46/IHAP-47 hardware campaigns: one guided entrypoint, automatic gates, deterministic evidence, no manual command-by-command interpretation.

Reference profile:

- Raspberry Pi 4 Model B;
- >=4 GB RAM;
- nominal 32 GB or larger microSD;
- application class **A1 or A2** accepted;
- A2 recommended for new purchases/reference replication;
- Raspberry Pi OS Lite 64-bit;
- Wi-Fi required;
- Ethernet optional;
- approximately 5 V PSU rated >=2.5 A for the bounded low-USB-load run;
- 5.1 V / 3 A recommended reference PSU;
- cooling/enclosure recorded exactly as tested.

This validates hardware/resource stability only. Final HomeEdge workload sufficiency, microSD endurance/retention, Docker/container behavior and AI acceleration remain `[UNVALIDATED]`.

## Fast path

### 1. Self-test

```bash
python3 -m unittest discover \
  -s tools/hardware-validation/ihap-52-central-node/tests \
  -p 'test_*.py' -v
```

### 2. Pre-flight only

```bash
python3 tools/hardware-validation/ihap-52-central-node/validate_central_node.py --guided --dry-run
```

The operator supplies only facts Linux cannot prove directly: microSD application class, Raspberry Pi OS Lite 64-bit Imager selection, optional card model, PSU rating, case/cooling and ambient temperature.

For the Pi 4 reference profile, `A1` and `A2` are accepted application classes. A2 remains the recommended replication class.

The PSU rating is an actual gate. Raspberry Pi documents 5 V / 3 A as the normal Pi 4 requirement and permits a good-quality 2.5 A supply where downstream USB load remains below 500 mA. IHAP-52 therefore accepts >=2.5 A only for this bounded low-peripheral run and recommends 5.1 V / 3 A for reference replication.

A 5 V / 1.55 A supply is below the accepted validation envelope and must not proceed to the stress phase.

### 3. Canonical physical run

Only after `PRE-FLIGHT PASS`:

```bash
python3 tools/hardware-validation/ihap-52-central-node/validate_central_node.py --guided
```

Default workload:

- 128 MiB deterministic storage write/read test with SHA-256 comparison;
- 300 seconds CPU stress;
- automatic worker, boot, OOM and `vcgencmd` post-run gates.

## Automatic pre-flight gates

- supported 64-bit architecture;
- >=4 logical CPUs;
- >=4 GB RAM;
- root filesystem capacity compatible with nominal 32 GB media;
- active Wi-Fi with an IP address;
- repository commit recorded and clean worktree;
- Pi 4 model/ARM64 for the reference profile;
- `vcgencmd` available;
- no current or historical Pi undervoltage/throttling flags;
- microSD application class A1/A2;
- Raspberry Pi OS Lite 64-bit operator confirmation;
- parseable and supported PSU rating.

GPU/render exposure is collected as observation only and is not an MVP PASS gate.

## Outputs

```text
runs/<run-id>/
├── operator-notes.md
├── validation.json
└── validation.md
```

Every run gets a unique directory. Previous attempts are never overwritten.

## Current Raspberry Pi OS note

Current Raspberry Pi OS Lite 64-bit is Debian-based. Seeing `Debian GNU/Linux 13 (trixie)` in `/etc/os-release` is compatible with the current Raspberry Pi OS Lite release when the operator confirms the Imager selection.

A `--dry-run` does not execute CPU stress, so `Max observed CPU temperature: not reported` is expected there.

## Privacy

Raw runs remain local and ignored by Git. Before publishing any sanitized summary, remove hostname, username, SSID, private IP, MAC address and credentials.

## Exit codes

- `0`: all applicable mandatory gates passed;
- `2`: at least one mandatory gate failed;
- other non-zero: execution/configuration error.

See [`QUICKSTART.md`](QUICKSTART.md) for the shortest operator command sequence and [`docs/evidence/IHAP-52/central-node-validation-plan.md`](../../../docs/evidence/IHAP-52/central-node-validation-plan.md) for the canonical runbook.
