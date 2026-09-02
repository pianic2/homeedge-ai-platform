# IHAP-52 Central Node Hardware Validation Harness

## Goal

Validate the bounded HomeEdge central-node hardware profile with the same operating model used for the mature IHAP-46/IHAP-47 hardware campaigns: one guided entrypoint, automatic gates, deterministic evidence, no manual command-by-command interpretation.

Reference profile:

- Raspberry Pi 4 Model B;
- >=4 GB RAM;
- 32 GB A2 microSD;
- Raspberry Pi OS Lite 64-bit;
- Wi-Fi required;
- Ethernet optional;
- manufacturer-supported USB-C PSU;
- cooling/enclosure recorded exactly as tested.

This validates hardware/resource stability only. Final HomeEdge workload sufficiency, microSD endurance/retention, Docker/container behavior and AI acceleration remain `[UNVALIDATED]`.

## Fast path

After installing Raspberry Pi OS Lite 64-bit and cloning/checking out the IHAP-52 branch:

```bash
cd ~/homeedge-ai-platform
python3 tools/hardware-validation/ihap-52-central-node/validate_central_node.py --guided
```

That command:

1. creates a unique run directory automatically;
2. asks only for physical facts Linux cannot prove (A2 marking, PSU, case/cooling, OS image selected);
3. records board, RAM, OS, kernel-facing hardware, repository commit and Wi-Fi state automatically;
4. rejects stale/dirty repository state before the stress phase;
5. requires a clean Raspberry Pi `vcgencmd get_throttled` baseline;
6. performs the deterministic storage write/read/hash smoke test;
7. runs the bounded 300-second CPU stress gate;
8. checks worker exits, boot identity, OOM evidence when readable, and Raspberry Pi throttling/undervoltage state;
9. writes `operator-notes.md`, `validation.json` and `validation.md`;
10. exits `0` on PASS or `2` on a validation failure.

Normal operator time after OS preparation is approximately the five-minute stress window plus a few prompts. No manual pre-flight or post-flight command list is required.

## Pre-flight only

Before committing to the five-minute run:

```bash
python3 tools/hardware-validation/ihap-52-central-node/validate_central_node.py --guided --dry-run
```

This performs the automatic mandatory pre-flight only and does not execute the storage write test or CPU stress.

## Harness self-tests

Run on any normal development machine; Raspberry Pi hardware is not required:

```bash
python3 -m unittest discover \
  -s tools/hardware-validation/ihap-52-central-node/tests \
  -p 'test_*.py' -v
```

These tests cover the pass/fail engine, Raspberry Pi-specific diagnostics, manual evidence gates, storage-integrity rejection, throttle-history rejection, equivalent-device behavior and non-overwriting run IDs.

## Mandatory automated gates

| Gate | Reference PASS condition |
|---|---|
| Architecture | 64-bit ARM64 for Pi 4 reference; ARM64/x86_64 for equivalent profile |
| Board | Raspberry Pi 4 Model B for `pi4-reference` |
| CPU | >=4 logical processors |
| RAM | >=4,000,000,000 bytes |
| Root filesystem | >=28,000,000,000 bytes for nominal 32 GB media |
| Wi-Fi | wireless interface `up` with a non-link-local address |
| Repository | tested commit recorded and worktree clean |
| A2 / OS selection | confirmed by operator in guided mode |
| PSU | rating recorded by operator |
| Pi diagnostics | `vcgencmd` available and no current/historical throttle/undervoltage flags before the run |
| Storage smoke | exact byte count and deterministic SHA-256 write/read match; temp file removed |
| Stress | all workers exit successfully |
| Stability | boot identity unchanged; no OOM pattern when kernel log is readable |
| Post-stress Pi health | no current/historical throttle/undervoltage/frequency-cap/soft-temp flags |

Graphics/render-device exposure is recorded as evidence but is **not** an MVP hardware gate. The current HomeEdge MVP does not require GPU acceleration.

## Outputs

Each attempt gets a new directory automatically:

```text
tools/hardware-validation/ihap-52-central-node/runs/pi4b-YYYYMMDDTHHMMSSZ/
├── operator-notes.md
├── validation.json
└── validation.md
```

`runs/` is ignored by Git. Never overwrite a failed run.

## Failure handling

If the guided command stops at pre-flight, fix the reported condition first. Common causes:

- A2 or Raspberry Pi OS Lite 64-bit not confirmed;
- worktree contains local edits;
- Wi-Fi is not up;
- wrong board/architecture;
- `vcgencmd` is unavailable;
- `get_throttled` already reports historical/current power or thermal flags.

For a dirty throttle history, reboot once with the intended PSU/cooling configuration and run the pre-flight again. A history that reappears immediately is evidence to investigate, not something to suppress.

## Privacy

The harness intentionally avoids recording SSID, passwords, private IPs, MAC addresses, hostname or username. Raw run evidence remains local until reviewed and sanitized.

## Canonical operator procedure

See [`docs/evidence/IHAP-52/central-node-validation-plan.md`](../../../docs/evidence/IHAP-52/central-node-validation-plan.md).

Official Raspberry Pi headless setup guidance:

- https://www.raspberrypi.com/documentation/computers/getting-started.html
- https://www.raspberrypi.com/software/operating-systems/
