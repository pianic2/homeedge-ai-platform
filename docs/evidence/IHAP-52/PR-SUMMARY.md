# IHAP-52 Pull Request Summary

## Scope

Defines the vendor-neutral HomeEdge MVP central-node hardware profile and the Raspberry Pi 4 reference-validation path without accepting Docker, a database, orchestration, Kafka or a final AI runtime.

## Proposed decision

- vendor-neutral 64-bit Linux central-node contract;
- Raspberry Pi 4 Model B >=4 GB as first reference/validation candidate;
- existing Raspberry Pi 4 Model B 8 GB as first physical specimen;
- **32 GB A2 microSD** as MVP reference storage;
- Wi-Fi required; Ethernet optional;
- Raspberry Pi OS Lite 64-bit as first reference image;
- Raspberry Pi 5 as a newer compatible candidate pending HomeEdge evidence;
- ARM64/x86_64 equivalent-device paths preserved;
- graphics/compute exposure recorded but **not required** by the current MVP hardware gate.

## ADR reconciliation

`main` already contains ADR-0001 through ADR-0005. The IHAP-52 decision is therefore renumbered to:

**ADR-0006 — MVP Central Node Hardware Profile** (`Proposed`).

No accepted ADR is renumbered or modified by this task.

## Validation automation remediation

The previous runbook still required too many manual shell checks and the harness treated Raspberry Pi `vcgencmd` as optional even though the reference procedure depended on it.

The revised harness now provides one guided command:

```bash
python3 tools/hardware-validation/ihap-52-central-node/validate_central_node.py --guided
```

It automatically:

- creates a non-overwriting run ID;
- records the tested Git commit and rejects a dirty worktree;
- checks board/architecture/CPU/RAM/storage/Wi-Fi;
- makes Raspberry Pi diagnostics mandatory for the Pi 4 reference profile;
- requires a clean throttle/power history before stress;
- performs deterministic storage integrity testing;
- performs the bounded 300-second CPU stress;
- verifies worker exits and boot identity;
- detects OOM patterns when kernel logging is readable;
- fails on post-stress power/throttle/frequency-cap/soft-temperature flags;
- generates operator notes, JSON evidence and a gate-by-gate Markdown summary.

Only unavoidable physical facts remain guided prompts.

## Harness regression coverage

Host-only unit tests cover the pass/fail engine and can run without Raspberry Pi hardware:

```bash
python3 -m unittest discover \
  -s tools/hardware-validation/ihap-52-central-node/tests \
  -p 'test_*.py' -v
```

Remediation development result: **9/9 PASS**.

## Documentation corrections

- removed stale 64 GB references; canonical storage baseline is 32 GB A2;
- removed stale hard-coded Raspberry Pi OS storage-floor wording;
- removed unnecessary full-OS-upgrade work from the canonical hardware-test path;
- added a short quick-start command sheet;
- clarified that graphics exposure is evidence, not an MVP GPU requirement;
- consolidated pre-flight/post-flight commands into the harness.

## Evidence boundary

Physical Raspberry Pi 4 validation is still pending. Until that run passes and is reviewed:

- Raspberry Pi 4 is not `Community validated`;
- ADR-0006 remains `Proposed`;
- workload sufficiency, microSD endurance/retention and AI acceleration remain `[UNVALIDATED]`.
