# IHAP-52 — Specialist Review Summary

**Task:** IHAP-52  
**PR:** #30  
**Decision:** ADR-0006 — MVP Central Node Hardware Profile (`Proposed`)  
**Review stage:** after ADR/main reconciliation, harness automation remediation and first physical pre-flight; before the full Pi 4 stress run.

## Result

No known Raspberry Pi architecture blocker has been found. The first physical pre-flight produced useful evidence but correctly stopped before stress because the tested PSU was below the accepted Pi 4 power envelope.

The full physical run is still mandatory. Raspberry Pi 4 is therefore not yet `Community validated` and ADR-0006 remains `Proposed`.

## Reconciled baseline

```text
Raspberry Pi 4 Model B
>=4 GB RAM
owned 8 GB specimen for first run
nominal 32 GB microSD
A1 or A2 accepted; A2 recommended for new purchases
Raspberry Pi OS Lite 64-bit
Wi-Fi required
Ethernet optional
~5 V PSU >=2.5 A for bounded low-USB-load validation
5.1 V / 3 A recommended reference PSU
fan/heatsink optional but recorded exactly
```

## First physical pre-flight — 2026-09-05

PASS observations:

- Raspberry Pi 4 Model B Rev 1.4;
- `aarch64`;
- 4 logical CPUs;
- 8,199,639,040 bytes RAM;
- 30,825,431,040-byte root filesystem;
- Wi-Fi PASS;
- repository commit recorded and worktree clean;
- `vcgencmd` available;
- current/historical pre-run power/throttle state clean;
- Raspberry Pi OS Lite 64-bit Imager selection confirmed;
- runtime base OS Debian GNU/Linux 13 (trixie), consistent with current Raspberry Pi OS.

Physical discovery:

- microSD is A1;
- case installed;
- heatsink installed;
- fan not installed;
- approximate ambient temperature 28 °C;
- PSU label 5 V / 1.55 A.

Disposition:

- A1 is accepted by the revised proposed storage profile; A2 remains recommended for replication/new purchase;
- 5 V / 1.55 A is below the accepted Pi 4 validation supply floor and must be replaced before stress;
- no Raspberry Pi rejection is justified by this pre-flight.

## Architecture Regression Review

PASS.

- ADR number no longer collides with accepted ADR-0003/0004/0005 on current `main`.
- Pi 4 remains a reference implementation, not a vendor lock-in.
- ARM64/x86_64 equivalent-device path remains explicit.
- GPU/graphics exposure is not an artificial current-MVP acceptance requirement.
- Docker, database, orchestration, Kafka and final AI runtime remain separate `[UNVALIDATED]` work.

## Hardware Compatibility Review

PASS for the observed board/profile; power remediation required before stress.

- board, RAM, storage capacity and Wi-Fi meet the current proposed profile;
- A1/A2 storage class handling is explicit;
- `vcgencmd` is mandatory for the Pi 4 reference path;
- pre-existing/current Raspberry Pi power/throttle flags prevent an ambiguous PASS;
- PSU rating is now a real pre-flight gate rather than a documentation-only field;
- final thermal behavior remains evidence-based rather than tied to an invented CPU-temperature threshold.

## Testing & Evidence Review

The operator path remains one guided entrypoint with a pre-flight mode and a full physical mode. Manual input is limited to characteristics Linux cannot establish reliably.

The host-side suite has been expanded from the earlier 9-case remediation baseline to include explicit A1/A2 handling and PSU-rating regression cases, including rejection of the observed 5 V / 1.55 A supply.

Canonical host suite:

```bash
python3 -m unittest discover \
  -s tools/hardware-validation/ihap-52-central-node/tests \
  -p 'test_*.py' -v
```

The current suite must report `OK` on the pulled branch before the next physical run. No CI status is claimed where GitHub exposes no workflow check.

## Source of Truth Review

PASS.

- GitHub remains canonical for ADR/runbook/harness/evidence;
- Jira remains workflow/decision/evidence-link coordination;
- Confluence remains stakeholder summary/navigation;
- no accepted ADR is modified or renumbered.

## Cost/effort review

PASS.

No reflash is required. Once a compliant PSU is available, the remaining operator work is the host self-test, a short guided dry-run and approximately five minutes of automated stress.

## Remaining gate

With the current branch pulled and a compliant supply connected:

```bash
python3 -m unittest discover \
  -s tools/hardware-validation/ihap-52-central-node/tests \
  -p 'test_*.py' -v

python3 tools/hardware-validation/ihap-52-central-node/validate_central_node.py --guided --dry-run

python3 tools/hardware-validation/ihap-52-central-node/validate_central_node.py --guided
```

Then review and sanitize the generated evidence before Project Owner ADR acceptance.
