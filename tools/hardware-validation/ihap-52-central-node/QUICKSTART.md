# IHAP-52 — Quick Test Commands

## 1. Reference setup

Use Raspberry Pi Imager and install the current **Raspberry Pi OS Lite 64-bit** image. Configure Wi-Fi and SSH in Imager.

Official guide:

https://www.raspberrypi.com/documentation/computers/getting-started.html

For the Raspberry Pi 4 reference run:

- 32 GB or larger microSD;
- application class **A1 or A2** is accepted for the bounded IHAP-52 validation; A2 remains the recommended new-purchase/reference class;
- Raspberry Pi 4 supported ~5 V supply;
- **5.1 V / 3 A is recommended**;
- a good-quality **2.5 A** supply is the minimum accepted by this bounded test when USB peripheral load is low;
- a supply below 2.5 A is not accepted for the reference stress run;
- cooling/enclosure configuration must be recorded exactly.

On the Pi:

```bash
sudo apt update
sudo apt install -y git python3 iproute2 util-linux
```

Do not run a full OS upgrade only for IHAP-52 unless you independently need it. The harness records the actual OS/kernel under test.

## 2. Get the exact task branch

```bash
cd ~
git clone https://github.com/pianic2/homeedge-ai-platform.git 2>/dev/null || true
cd ~/homeedge-ai-platform
git fetch origin
git checkout ihap-52-central-node-hardware-decision
git pull --ff-only origin ihap-52-central-node-hardware-decision
```

## 3. Harness self-test

```bash
python3 -m unittest discover \
  -s tools/hardware-validation/ihap-52-central-node/tests \
  -p 'test_*.py' -v
```

Expected: all tests `OK`.

## 4. Pre-flight only

```bash
python3 tools/hardware-validation/ihap-52-central-node/validate_central_node.py --guided --dry-run
```

When prompted for the microSD application class, enter `A1` or `A2` exactly as printed on the card.

If the PSU is below the accepted Pi 4 reference threshold, stop here and replace the PSU before running the stress phase.

The harness prints every pre-flight gate individually as `[PASS]` or `[FAIL]`.

## 5. Canonical validation — one command

Only after `PRE-FLIGHT PASS`:

```bash
python3 tools/hardware-validation/ihap-52-central-node/validate_central_node.py --guided
```

Default physical workload:

- 128 MiB deterministic storage smoke test;
- 300 seconds CPU stress;
- automatic power/throttle/stability gates.

### Live console progress

The harness prints the active phase and progress with flushed console output. During a normal run you will see messages similar to:

```text
[IHAP-52] PHASE 3/5: storage integrity smoke test (128 MiB)
[IHAP-52] STORAGE write: 25% (32/128 MiB)
[IHAP-52] STORAGE write: 50% (64/128 MiB)
[IHAP-52] STORAGE: rilettura e verifica SHA-256...
[IHAP-52] STORAGE: PASS; write=... read=... hash_match=True
[IHAP-52] PHASE 4/5: CPU stress (300s, 4 worker)
[IHAP-52] STRESS  33% | elapsed=  100s | remaining=  200s | temp=...C | load1=... | mem_avail=... MiB | throttle=0x0 (none)
[IHAP-52] STRESS  67% | elapsed=  200s | remaining=  100s | temp=...C | load1=... | mem_avail=... MiB | throttle=0x0 (none)
[IHAP-52] PHASE 5/5: post-flight power/throttle, boot stability e OOM checks
[IHAP-52] POST-FLIGHT throttle=0x0 (none)
[IHAP-52] POST-FLIGHT GATES
  [PASS] storage_integrity
  [PASS] stress_workers
  [PASS] no_pi_undervoltage
  [PASS] no_pi_frequency_cap_or_throttle
  [PASS] no_pi_soft_temperature_limit
  ...
[IHAP-52] FINAL RESULT: PASS
```

Stress progress is emitted approximately every **5 seconds** and includes:

- percentage completed;
- elapsed and remaining seconds;
- CPU temperature when readable;
- 1-minute load average;
- available RAM;
- decoded Raspberry Pi `vcgencmd get_throttled` state.

These console messages are observational only. They do not modify the test duration or acceptance envelope.

The command prints the evidence directory when it finishes.

## 6. Read the result

```bash
RUN_DIR=$(find tools/hardware-validation/ihap-52-central-node/runs \
  -mindepth 1 -maxdepth 1 -type d | sort | tail -n1)

cat "$RUN_DIR/validation.md"
python3 -m json.tool "$RUN_DIR/validation.json" >/dev/null && echo 'JSON OK'
```

Expected final result: `Overall gate: PASS`.

## 7. If a run fails on Raspberry Pi throttle/power

Before rebooting, capture the current/historical firmware flags:

```bash
vcgencmd get_throttled
vcgencmd measure_temp
```

The revised harness separates:

- `no_pi_undervoltage` — supply-voltage events;
- `no_pi_frequency_cap_or_throttle` — frequency-cap/throttle events, including thermal throttling;
- `no_pi_soft_temperature_limit` — generic soft-temperature flag when exposed.

Raspberry Pi documentation states that between approximately **80 °C and 85 °C** the Arm cores are progressively throttled. A bounded run that reaches this regime and records frequency-cap/throttle flags does not reject the Pi 4 itself; it rejects that exact tested cooling/enclosure configuration.

### Thermal rerun path

If the previous run reached the thermal-throttling regime:

1. improve airflow / install the intended case fan or otherwise change cooling;
2. record the new cooling configuration exactly;
3. reboot before the next acceptance run, because historical `vcgencmd` flags would otherwise contaminate pre-flight;
4. after reboot verify:

```bash
vcgencmd get_throttled
```

Expected clean boot state:

```text
throttled=0x0
```

5. pull the latest IHAP-52 branch;
6. rerun the host self-test;
7. run `--guided --dry-run`;
8. only after `PRE-FLIGHT PASS`, run the full `--guided` test.

## 8. Interpretation notes

Current Raspberry Pi OS Lite 64-bit is Debian-based. A summary such as `Debian GNU/Linux 13 (trixie)` is therefore not, by itself, an OS failure when the operator has confirmed Raspberry Pi OS Lite 64-bit was selected in Raspberry Pi Imager.

A `not reported` maximum CPU temperature in a `--dry-run` is expected because the stress phase did not execute.
