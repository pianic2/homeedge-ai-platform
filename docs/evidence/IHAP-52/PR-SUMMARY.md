# IHAP-52 Pull Request Summary

## Scope

Defines the vendor-neutral HomeEdge MVP central-node hardware profile and the Raspberry Pi 4 reference-validation path without accepting Docker, a database, orchestration, Kafka or a final AI runtime.

## Proposed decision

- vendor-neutral 64-bit Linux central-node contract;
- Raspberry Pi 4 Model B >=4 GB as first reference/validation candidate;
- existing Raspberry Pi 4 Model B 8 GB as first physical specimen;
- nominal **32 GB microSD** as MVP reference storage capacity;
- **A1 or A2** accepted for the bounded validation; A2 recommended for new purchases/reference replication;
- Wi-Fi required; Ethernet optional;
- Raspberry Pi OS Lite 64-bit as first reference image;
- approximately 5 V PSU rated >=2.5 A for the bounded low-USB-load run; 5.1 V / 3 A recommended reference;
- Raspberry Pi 5 as a newer compatible candidate pending HomeEdge evidence;
- ARM64/x86_64 equivalent-device paths preserved;
- graphics/compute exposure recorded but **not required** by the current MVP hardware gate.

## ADR reconciliation

`main` already contains ADR-0001 through ADR-0005. The IHAP-52 decision is therefore:

**ADR-0006 — MVP Central Node Hardware Profile** (`Proposed`).

No accepted ADR is renumbered or modified by this task.

## Validation automation remediation

Canonical pre-flight:

```bash
python3 tools/hardware-validation/ihap-52-central-node/validate_central_node.py --guided --dry-run
```

Canonical physical run, only after pre-flight PASS:

```bash
python3 tools/hardware-validation/ihap-52-central-node/validate_central_node.py --guided
```

The harness automatically creates a non-overwriting run ID, records repository state, validates board/architecture/CPU/RAM/storage/Wi-Fi, requires Pi `vcgencmd`, checks throttle/power history, validates storage with deterministic SHA-256 write/read, executes a bounded 300-second CPU stress, checks worker/boot/OOM/power state and generates Markdown/JSON evidence.

## First physical pre-flight — 2026-09-05

The first guided pre-flight reached policy evaluation and intentionally stopped before stress.

Observed PASS evidence:

- Raspberry Pi 4 Model B Rev 1.4;
- `aarch64`;
- 4 logical CPUs;
- 8,199,639,040 bytes RAM;
- 30,825,431,040-byte root filesystem;
- Wi-Fi PASS;
- repository commit recorded / clean worktree PASS;
- `vcgencmd` available;
- clean current/historical throttle/undervoltage state;
- Raspberry Pi OS Lite 64-bit selected in Imager;
- runtime base OS Debian GNU/Linux 13 (trixie), consistent with current Raspberry Pi OS.

Physical discovery:

- owned card is **A1**, not A2;
- case installed;
- heatsink installed;
- fan absent;
- approximate ambient temperature 28 °C;
- PSU label **5 V / 1.55 A**.

Disposition:

1. the original A2-only requirement was too restrictive and has been corrected to A1/A2 accepted, A2 recommended;
2. the 5 V / 1.55 A supply is below the accepted Raspberry Pi 4 validation envelope and blocks the stress run;
3. the Raspberry Pi itself is **not rejected** by this pre-flight.

## Harness regression coverage

Host-only tests cover the pass/fail engine without Raspberry Pi hardware. The suite includes explicit regression cases for A1/A2 storage classes and rejection of a 5 V / 1.55 A PSU.

```bash
python3 -m unittest discover \
  -s tools/hardware-validation/ihap-52-central-node/tests \
  -p 'test_*.py' -v
```

## Evidence boundary

The full physical Raspberry Pi 4 stress run is still pending. Until a compliant-PSU run passes and is reviewed:

- Raspberry Pi 4 is not `Community validated`;
- ADR-0006 remains `Proposed`;
- workload sufficiency, microSD endurance/retention and AI acceleration remain `[UNVALIDATED]`.
