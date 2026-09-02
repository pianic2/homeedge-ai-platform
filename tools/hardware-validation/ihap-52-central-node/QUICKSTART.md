# IHAP-52 — Quick Test Commands

## 1. One-time Raspberry Pi preparation

Use Raspberry Pi Imager and install the current **Raspberry Pi OS Lite 64-bit** image. Configure Wi-Fi and SSH in Imager.

Official guide:

https://www.raspberrypi.com/documentation/computers/getting-started.html

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

## 3. Optional pre-flight

```bash
python3 tools/hardware-validation/ihap-52-central-node/validate_central_node.py --guided --dry-run
```

If this is PASS, proceed.

## 4. Canonical validation — one command

```bash
python3 tools/hardware-validation/ihap-52-central-node/validate_central_node.py --guided
```

Default physical workload:

- 128 MiB deterministic storage smoke test;
- 300 seconds CPU stress;
- automatic power/throttle/stability gates.

The command prints the evidence directory when it finishes.

## 5. Read the result

```bash
RUN_DIR=$(find tools/hardware-validation/ihap-52-central-node/runs -mindepth 1 -maxdepth 1 -type d | sort | tail -n1)
cat "$RUN_DIR/validation.md"
python3 -m json.tool "$RUN_DIR/validation.json" >/dev/null && echo 'JSON OK'
```

Expected final result: `Overall gate: PASS`.

## 6. Harness self-test — no Raspberry Pi required

```bash
python3 -m unittest discover \
  -s tools/hardware-validation/ihap-52-central-node/tests \
  -p 'test_*.py' -v
```

Expected: all tests `OK`.
