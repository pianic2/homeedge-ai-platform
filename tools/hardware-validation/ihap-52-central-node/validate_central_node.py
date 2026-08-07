#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any

MIN_LOGICAL_CPUS = 4
MIN_RAM_BYTES = 4_000_000_000
# Nominal 64 GB media normally exposes less than 64 GiB after decimal/binary conversion.
MIN_STORAGE_BYTES = 58_000_000_000


def run_command(args: list[str], timeout: int = 10) -> dict[str, Any]:
    try:
        proc = subprocess.run(args, capture_output=True, text=True, timeout=timeout, check=False)
        return {
            "available": True,
            "returncode": proc.returncode,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
        }
    except FileNotFoundError:
        return {"available": False, "returncode": None, "stdout": "", "stderr": "command not found"}
    except subprocess.TimeoutExpired:
        return {"available": True, "returncode": None, "stdout": "", "stderr": "timeout"}


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8", errors="replace").strip("\x00\n ")
    except OSError:
        return None


def meminfo() -> dict[str, int]:
    data: dict[str, int] = {}
    text = read_text(Path("/proc/meminfo"))
    if not text:
        return data
    for line in text.splitlines():
        if ":" not in line:
            continue
        key, raw = line.split(":", 1)
        fields = raw.strip().split()
        if not fields:
            continue
        try:
            value = int(fields[0])
        except ValueError:
            continue
        if len(fields) > 1 and fields[1].lower() == "kb":
            value *= 1024
        data[key] = value
    return data


def cpu_temperature_c() -> float | None:
    for path in (
        Path("/sys/class/thermal/thermal_zone0/temp"),
        Path("/sys/class/hwmon/hwmon0/temp1_input"),
    ):
        raw = read_text(path)
        if not raw:
            continue
        try:
            value = float(raw)
            return value / 1000.0 if value > 1000 else value
        except ValueError:
            continue
    return None


def raspberry_model() -> str | None:
    return read_text(Path("/proc/device-tree/model"))


def throttled_status() -> dict[str, Any]:
    result = run_command(["vcgencmd", "get_throttled"])
    parsed = None
    if result["available"] and result["returncode"] == 0 and "=" in result["stdout"]:
        raw = result["stdout"].split("=", 1)[1].strip()
        try:
            parsed = int(raw, 16)
        except ValueError:
            parsed = None
    return {"raw": result, "value": parsed}


def wifi_interfaces() -> list[dict[str, Any]]:
    interfaces: list[dict[str, Any]] = []
    net_root = Path("/sys/class/net")
    if not net_root.exists():
        return interfaces
    for iface_path in sorted(net_root.iterdir()):
        if not (iface_path / "wireless").exists():
            continue
        name = iface_path.name
        operstate = read_text(iface_path / "operstate")
        addr = run_command(["ip", "-j", "addr", "show", "dev", name])
        has_ip = False
        families: list[str] = []
        if addr["available"] and addr["returncode"] == 0 and addr["stdout"]:
            try:
                parsed = json.loads(addr["stdout"])
                for item in parsed:
                    for info in item.get("addr_info", []):
                        family = info.get("family")
                        local = info.get("local", "")
                        if family in {"inet", "inet6"} and local and not local.startswith("fe80:"):
                            has_ip = True
                            families.append(family)
            except json.JSONDecodeError:
                pass
        interfaces.append({
            "name": name,
            "operstate": operstate,
            "has_ip": has_ip,
            "families": sorted(set(families)),
        })
    return interfaces


def graphics_devices() -> list[str]:
    dri = Path("/dev/dri")
    if not dri.exists():
        return []
    return sorted(p.name for p in dri.iterdir() if p.name.startswith(("render", "card")))


def root_storage() -> dict[str, Any]:
    usage = shutil.disk_usage("/")
    lsblk = run_command(["lsblk", "-J", "-b", "-o", "NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS,MODEL"])
    return {
        "filesystem_total_bytes": usage.total,
        "filesystem_used_bytes": usage.used,
        "filesystem_free_bytes": usage.free,
        "lsblk": lsblk,
    }


def local_ping(host: str | None) -> dict[str, Any] | None:
    if not host:
        return None
    return run_command(["ping", "-c", "3", "-W", "2", host], timeout=10)


def storage_smoke(output_dir: Path, size_mib: int) -> dict[str, Any]:
    size_bytes = size_mib * 1024 * 1024
    block = hashlib.sha256(b"IHAP-52-storage-smoke").digest() * 4096
    target = output_dir / ".storage-smoke.bin"
    written = 0
    start = time.monotonic()
    with target.open("wb", buffering=0) as fh:
        while written < size_bytes:
            chunk = block[: min(len(block), size_bytes - written)]
            fh.write(chunk)
            written += len(chunk)
        os.fsync(fh.fileno())
    write_elapsed = time.monotonic() - start

    read_bytes = 0
    digest = hashlib.sha256()
    start = time.monotonic()
    with target.open("rb", buffering=0) as fh:
        while True:
            chunk = fh.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
            read_bytes += len(chunk)
    read_elapsed = time.monotonic() - start
    target.unlink(missing_ok=True)
    return {
        "requested_mib": size_mib,
        "bytes_written": written,
        "bytes_read": read_bytes,
        "write_seconds": round(write_elapsed, 4),
        "read_seconds": round(read_elapsed, 4),
        "write_mib_s": round((written / 1024 / 1024) / write_elapsed, 2) if write_elapsed else None,
        "read_mib_s": round((read_bytes / 1024 / 1024) / read_elapsed, 2) if read_elapsed else None,
        "sha256": digest.hexdigest(),
        "temporary_file_removed": not target.exists(),
    }


def worker(stop_at: float) -> None:
    payload = b"homeedge-ihap-52-central-node"
    digest = payload
    while time.monotonic() < stop_at:
        digest = hashlib.sha256(digest + payload).digest()


def cpu_stress(seconds: int, workers: int, sample_seconds: int = 5) -> dict[str, Any]:
    import multiprocessing as mp

    stop_at = time.monotonic() + seconds
    procs = [mp.Process(target=worker, args=(stop_at,)) for _ in range(workers)]
    for proc in procs:
        proc.start()

    samples: list[dict[str, Any]] = []
    while any(proc.is_alive() for proc in procs):
        memory = meminfo()
        samples.append({
            "elapsed_seconds": round(max(0.0, seconds - max(0.0, stop_at - time.monotonic())), 2),
            "temperature_c": cpu_temperature_c(),
            "loadavg": list(os.getloadavg()) if hasattr(os, "getloadavg") else None,
            "mem_available_bytes": memory.get("MemAvailable"),
        })
        remaining = max(0.0, stop_at - time.monotonic())
        if remaining <= 0:
            break
        time.sleep(min(sample_seconds, remaining))

    for proc in procs:
        proc.join(timeout=5)
    return {
        "duration_seconds": seconds,
        "workers": workers,
        "samples": samples,
        "worker_exitcodes": [proc.exitcode for proc in procs],
    }


def sanitize_os_release() -> dict[str, str]:
    result: dict[str, str] = {}
    text = read_text(Path("/etc/os-release"))
    if not text:
        return result
    for line in text.splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key in {"NAME", "VERSION", "VERSION_ID", "ID"}:
            result[key] = value.strip('"')
    return result


def evaluate(payload: dict[str, Any]) -> dict[str, Any]:
    checks: dict[str, dict[str, Any]] = {}
    arch = payload["system"]["architecture"].lower()
    checks["architecture"] = {
        "pass": arch in {"aarch64", "arm64", "x86_64", "amd64"},
        "observed": arch,
    }
    cpu_count = payload["system"]["logical_cpus"] or 0
    checks["logical_cpus"] = {
        "pass": cpu_count >= MIN_LOGICAL_CPUS,
        "observed": cpu_count,
        "minimum": MIN_LOGICAL_CPUS,
    }
    ram = payload["system"]["memory"].get("MemTotal", 0)
    checks["ram"] = {
        "pass": ram >= MIN_RAM_BYTES,
        "observed_bytes": ram,
        "minimum_bytes": MIN_RAM_BYTES,
    }
    storage = payload["storage"]["filesystem_total_bytes"]
    checks["storage"] = {
        "pass": storage >= MIN_STORAGE_BYTES,
        "observed_bytes": storage,
        "minimum_bytes": MIN_STORAGE_BYTES,
    }
    wifi = payload["network"]["wifi_interfaces"]
    wifi_ok = any(i.get("operstate") == "up" and i.get("has_ip") for i in wifi)
    checks["wifi"] = {
        "pass": wifi_ok,
        "observed_interfaces": wifi,
    }
    graphics = payload["system"]["graphics_devices"]
    checks["graphics_compute_device"] = {
        "pass": bool(graphics),
        "observed": graphics,
        "note": "Presence only; AI acceleration remains UNVALIDATED.",
    }
    storage_smoke_ok = (
        payload["storage_smoke"]["bytes_written"] == payload["storage_smoke"]["bytes_read"]
        and payload["storage_smoke"]["temporary_file_removed"]
    )
    checks["storage_smoke"] = {"pass": storage_smoke_ok}
    exitcodes = payload["stress"]["worker_exitcodes"]
    checks["stress_workers"] = {
        "pass": all(code == 0 for code in exitcodes),
        "observed": exitcodes,
    }

    throttle_after = payload["raspberry_pi"]["throttled_after"]["value"]
    if throttle_after is None:
        checks["raspberry_pi_current_undervoltage"] = {
            "pass": None,
            "observed": None,
            "note": "vcgencmd unavailable or non-Raspberry Pi",
        }
        checks["raspberry_pi_current_throttling"] = {
            "pass": None,
            "observed": None,
            "note": "vcgencmd unavailable or non-Raspberry Pi",
        }
    else:
        checks["raspberry_pi_current_undervoltage"] = {
            "pass": (throttle_after & 0x1) == 0,
            "observed": bool(throttle_after & 0x1),
        }
        checks["raspberry_pi_current_throttling"] = {
            "pass": (throttle_after & 0x4) == 0,
            "observed": bool(throttle_after & 0x4),
        }

    mandatory = [check["pass"] for check in checks.values() if check["pass"] is not None]
    return {"checks": checks, "overall_pass": all(mandatory)}


def markdown_summary(payload: dict[str, Any]) -> str:
    lines = [
        "# IHAP-52 Central Node Validation Summary",
        "",
        f"- Generated at (UTC): `{payload['generated_at_utc']}`",
        f"- Model: `{payload['system'].get('raspberry_model') or 'not reported'}`",
        f"- Architecture: `{payload['system']['architecture']}`",
        f"- Logical CPUs: `{payload['system']['logical_cpus']}`",
        f"- RAM bytes: `{payload['system']['memory'].get('MemTotal')}`",
        f"- Root filesystem bytes: `{payload['storage']['filesystem_total_bytes']}`",
        f"- Overall automated gate: `{'PASS' if payload['evaluation']['overall_pass'] else 'FAIL'}`",
        "",
        "## Automated checks",
        "",
        "| Check | Result | Observed |",
        "|---|---|---|",
    ]
    for name, check in payload["evaluation"]["checks"].items():
        result = "N/A" if check["pass"] is None else ("PASS" if check["pass"] else "FAIL")
        observed = check.get(
            "observed",
            check.get("observed_bytes", check.get("observed_interfaces", "")),
        )
        lines.append(f"| `{name}` | {result} | `{str(observed)[:180]}` |")
    lines += [
        "",
        "## Evidence boundaries",
        "",
        "- This run is a bounded hardware/resource smoke test, not final application workload certification.",
        "- microSD endurance remains `[UNVALIDATED]`.",
        "- future AI runtime/model and GPU/NPU acceleration remain `[UNVALIDATED]`.",
        "- Docker, Alpine Linux, database and orchestration are not validated by this run.",
        "- Review raw output for private local metadata before publication.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="IHAP-52 central-node hardware validation harness"
    )
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--stress-seconds", type=int, default=300)
    parser.add_argument("--storage-mib", type=int, default=128)
    parser.add_argument(
        "--wifi-host",
        default=None,
        help="Optional authorized local host to ping",
    )
    args = parser.parse_args()

    if args.stress_seconds < 10:
        parser.error("--stress-seconds must be at least 10")
    if args.storage_mib < 16 or args.storage_mib > 1024:
        parser.error("--storage-mib must be between 16 and 1024")

    output_dir: Path = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    memory_before = meminfo()
    payload: dict[str, Any] = {
        "schema_version": 1,
        "generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "system": {
            "raspberry_model": raspberry_model(),
            "architecture": platform.machine(),
            "logical_cpus": os.cpu_count(),
            "kernel": platform.release(),
            "os_release": sanitize_os_release(),
            "memory": memory_before,
            "graphics_devices": graphics_devices(),
        },
        "network": {
            "wifi_interfaces": wifi_interfaces(),
            "optional_local_ping": local_ping(args.wifi_host),
        },
        "storage": root_storage(),
        "raspberry_pi": {
            "throttled_before": throttled_status(),
        },
    }

    payload["storage_smoke"] = storage_smoke(output_dir, args.storage_mib)
    payload["stress"] = cpu_stress(args.stress_seconds, os.cpu_count() or 1)
    payload["raspberry_pi"]["throttled_after"] = throttled_status()
    payload["system"]["memory_after"] = meminfo()
    payload["system"]["temperature_after_c"] = cpu_temperature_c()
    payload["evaluation"] = evaluate(payload)
    payload["evidence_boundaries"] = {
        "final_workload_sufficiency": "UNVALIDATED",
        "storage_endurance": "UNVALIDATED",
        "ai_runtime_model": "UNVALIDATED",
        "gpu_npu_ai_acceleration": "UNVALIDATED",
        "docker_alpine_database_orchestration": "OUT_OF_SCOPE",
    }

    json_path = output_dir / "validation.json"
    md_path = output_dir / "validation.md"
    json_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    md_path.write_text(markdown_summary(payload), encoding="utf-8")

    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")
    print(
        "Automated gate:",
        "PASS" if payload["evaluation"]["overall_pass"] else "FAIL",
    )
    return 0 if payload["evaluation"]["overall_pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
