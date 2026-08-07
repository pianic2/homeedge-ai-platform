# IHAP-52 — Central Node Validation Plan

## Goal

Produce reproducible evidence that the first Raspberry Pi 4 Model B specimen satisfies the accepted minimum hardware profile and can sustain a bounded synthetic central-node workload without obvious resource, Wi-Fi, storage or thermal blockers.

This validation does **not** certify the final HomeEdge application workload because the backend, database, container topology and AI runtime are not yet implemented. Those remain `[UNVALIDATED]`.

## Validation specimen

Expected first specimen:

- Raspberry Pi 4 Model B;
- 8 GB RAM physically installed;
- 64 GB A2 microSD for the MVP reference storage configuration;
- Wi-Fi enabled and connected to the local network;
- manufacturer-supported USB-C power supply, preferably official 15 W / 5.1 V 3 A class;
- enclosure/cooling configuration recorded exactly as tested.

The 8 GB specimen may demonstrate compliance with the >=4 GB minimum but cannot by itself prove that a physical 4 GB board has identical workload headroom. The runtime workload test should therefore record actual peak memory use and preserve the 4 GB sufficiency claim as `[UNVALIDATED]` if the evidence is not strong enough.

## Test principles

1. No Internet connectivity is required.
2. No private SSID, password, private IP, hostname or username should be published.
3. No Docker, Alpine Linux, database or AI framework is installed or accepted by this test.
4. The harness uses Python standard-library functionality and Linux system files/commands only.
5. The synthetic load is intentionally bounded and is not a benchmark competition.
6. Raw evidence stays local until reviewed and sanitized.
7. A passing run supports the hardware-profile decision only within the declared test envelope.

## Required checks

### Gate A — Hardware identity and minimum profile

Pass when all mandatory checks succeed:

- architecture is `aarch64`, `arm64` or `x86_64`;
- at least 4 logical processors are visible;
- at least 4 GB physical RAM is reported;
- root storage device/filesystem corresponds to approximately a nominal 64 GB or larger device;
- at least one Wi-Fi interface exists and is operational;
- a Linux graphics/compute render device is exposed when available through `/dev/dri` or equivalent detected evidence;
- Raspberry Pi model identity is recorded when `/proc/device-tree/model` exists.

The graphics check confirms platform exposure only. AI acceleration remains `[UNVALIDATED]`.

### Gate B — Power/undervoltage observation

On Raspberry Pi, record `vcgencmd get_throttled` before and after the stress phase when `vcgencmd` is available.

A run is not acceptable as clean power evidence if current undervoltage/throttling flags are observed. Historical flags must be reported and reviewed rather than silently ignored.

The PSU model/rating must also be recorded manually because software cannot prove which external supply is attached.

### Gate C — Wi-Fi

Pass when:

- a wireless interface is detected;
- the interface is up;
- an IPv4 or IPv6 address is assigned.

Optional local reachability may be tested with `--wifi-host <local-address>`. The harness must not require a public Internet host.

### Gate D — Storage smoke test

The harness writes a bounded temporary file, flushes it to storage, reads it back, compares deterministic write/read hashes and removes it.

Default size: 128 MiB.

Record:

- bytes written/read;
- elapsed write/read time;
- calculated sequential throughput;
- matching write/read hashes;
- whether the temporary file was removed.

This is only a functional/performance smoke test. It does not prove microSD endurance.

### Gate E — CPU/thermal stress

Default stress duration: 300 seconds.

The harness creates CPU-bound worker processes equal to the detected logical CPU count and samples:

- CPU temperature when available;
- load average;
- memory availability;
- Raspberry Pi throttling flags when available.

Pass criteria for the first project run:

- harness completes without crash or forced reboot;
- no current undervoltage flag is reported at the end of the run;
- no current thermal-throttling condition is reported by Raspberry Pi firmware at the end of the run;
- the temperature series is successfully recorded when the platform exposes it;
- no out-of-memory condition is observed.

Temperature samples must be reviewed together with the recorded ambient conditions, enclosure and cooling configuration. IHAP-52 does not invent a CPU-temperature acceptance threshold from an ambient operating-range specification. Historical throttling or thermal-limit flags are evidence to review even when no current flag remains.

This is a smoke/stability gate, not a production thermal qualification.

### Gate F — Memory/headroom observation

Record total and available memory before, during and after stress.

The test does not allocate most of the system RAM because the goal is not to damage stability. Instead, the evidence must state whether measured synthetic workload memory remains comfortably below the 4 GB minimum.

If future backend/AI tasks consume materially more memory, the minimum must be revalidated.

### Gate G — AI readiness

No AI runtime is installed by IHAP-52.

Record only:

- CPU architecture and core count;
- RAM capacity;
- detected graphics/render device;
- optional USB 3 / PCIe capability from documented board profile.

Outcome must remain:

`future small-model AI workload and acceleration path: [UNVALIDATED]`

## Manual configuration record

Before the run, record locally:

| Field | Required |
|---|---|
| Board/model | Yes |
| RAM variant | Yes |
| Storage manufacturer/model/capacity | Yes |
| A2 marking confirmed | Yes for reference acceptance |
| PSU manufacturer/model/rating | Yes |
| Case | Yes |
| Heatsinks installed | Yes/No |
| Fan installed | Yes/No |
| Ambient temperature estimate | Recommended |
| OS and kernel | Automatically captured |

Do not publish Wi-Fi credentials, SSID, MAC address, hostname, username or private IP addresses.

## Commands

From repository root on the central-node candidate:

```bash
python3 tools/hardware-validation/ihap-52-central-node/validate_central_node.py \
  --output-dir tools/hardware-validation/ihap-52-central-node/runs/pi4b-reference-01 \
  --stress-seconds 300 \
  --storage-mib 128
```

Optional local network check:

```bash
python3 tools/hardware-validation/ihap-52-central-node/validate_central_node.py \
  --output-dir tools/hardware-validation/ihap-52-central-node/runs/pi4b-reference-01 \
  --wifi-host 192.168.1.2
```

`--wifi-host` must point to a host the operator is authorized to probe on the local network.

## Expected local outputs

```text
tools/hardware-validation/ihap-52-central-node/runs/<run-id>/
├── validation.json
└── validation.md
```

The harness-local `runs/` directory is ignored by Git. These raw outputs must be reviewed before repository publication.

## Public evidence promotion

After the Project Owner runs the test:

1. inspect the JSON/Markdown for private local metadata;
2. remove/redact network identifiers;
3. verify pass/fail statements against the raw run;
4. publish a summary under `docs/evidence/IHAP-52/summaries/`;
5. run the required specialist reviews;
6. only after a passing evidence review may Raspberry Pi 4 be labelled `Community validated` and the ADR be considered for `Accepted` status.

## Failure handling

A failed gate does not automatically reject Raspberry Pi 4.

Classify the failure first:

- configuration failure;
- PSU/undervoltage issue;
- Wi-Fi setup issue;
- thermal/cooling issue;
- storage issue;
- minimum-profile mismatch;
- harness defect;
- genuine hardware/workload blocker.

Corrective fixes remain on the same IHAP-52 branch/PR. No replacement branch or PR is created.
