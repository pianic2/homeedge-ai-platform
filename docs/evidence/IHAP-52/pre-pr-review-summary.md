# IHAP-52 — Specialist Pre-Physical-Run Review Summary

**Task:** IHAP-52  
**PR:** #30  
**Decision:** ADR-0006 — MVP Central Node Hardware Profile (`Proposed`)  
**Review stage:** after ADR/main reconciliation and validation-harness automation remediation; before physical Pi 4 run.

## Result

No known documentation or harness-design blocker remains before the physical reference run.

The physical run itself is still mandatory, therefore Raspberry Pi 4 is not yet `Community validated` and ADR-0006 must remain `Proposed`.

## Reconciled baseline

```text
Raspberry Pi 4 Model B
>=4 GB RAM
owned 8 GB specimen for first run
32 GB A2 microSD
Raspberry Pi OS Lite 64-bit
Wi-Fi required
Ethernet optional
stable supported USB-C PSU
fan/heatsink optional but recorded exactly
```

## Architecture Regression Review

PASS.

- ADR number no longer collides with accepted ADR-0003/0004/0005 on current `main`.
- Pi 4 remains a reference implementation, not a vendor lock-in.
- ARM64/x86_64 equivalent-device path remains explicit.
- GPU/graphics exposure is no longer an artificial current-MVP acceptance requirement.
- Docker, database, orchestration, Kafka and final AI runtime remain separate `[UNVALIDATED]` work.

## Hardware Compatibility Review

PASS pending physical evidence.

- board, RAM, storage, Wi-Fi and PSU gates are explicit;
- `vcgencmd` is mandatory for the Pi 4 reference path rather than silently ignored;
- pre-existing/current Raspberry Pi power/throttle flags prevent an ambiguous PASS;
- final thermal behavior remains evidence-based rather than tied to an invented CPU-temperature threshold.

## Testing & Evidence Review

PASS for harness design; physical run pending.

The operator path has been reduced from a long manual command sequence to one guided command. Manual input is limited to physical characteristics not observable by Linux.

Automated host-side regression suite: **9/9 PASS** during remediation development.

Coverage includes:

- valid Pi 4 pre-flight;
- mandatory `vcgencmd` handling;
- historical throttle rejection;
- A2/manual gate enforcement;
- equivalent x86_64 behavior;
- graphics exposure as observation rather than MVP gate;
- storage hash mismatch rejection;
- post-stress throttle rejection;
- non-overwriting run IDs.

## Source of Truth Review

PASS.

- GitHub remains canonical for ADR/runbook/harness/evidence;
- Jira remains workflow/decision/evidence-link coordination;
- Confluence remains stakeholder summary/navigation;
- no accepted ADR is modified or renumbered.

## Cost/effort review

PASS.

The canonical validation no longer requires an unnecessary full system upgrade. After OS imaging/first boot, normal operator test time is approximately five minutes of automated stress plus short guided prompts.

## Remaining gate

Run on the owned Raspberry Pi 4 8 GB + 32 GB A2 specimen:

```bash
python3 tools/hardware-validation/ihap-52-central-node/validate_central_node.py --guided
```

Then review and sanitize the generated evidence before Project Owner ADR acceptance.
