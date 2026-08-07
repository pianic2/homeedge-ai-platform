#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import multiprocessing as mp
import os
import platform
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any

MIN_LOGICAL_CPUS = 4
MIN_RAM_BYTES = 4_000_000_000
# A nominal 32 GB microSD exposes less usable filesystem capacity after
# decimal/binary conversion, partitioning and formatting.
MIN_STORAGE_BYTES = 28_000_000_000


def command(args: list[str], timeout: int = 10) -> dict[str, Any]:
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=timeout, check=False)
        return {"available": True, "returncode": p.returncode, "stdout": p.stdout.strip(), "stderr": p.stderr.strip()}
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
    result: dict[str, int] = {}
    raw = read_text(Path("/proc/meminfo")) or ""
    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields = value.strip().split()
        if not fields:
            continue
        try:
            parsed = int(fields[0])
        except ValueError:
            continue
        if len(fields) > 1 and fields[1].lower() == "kb":
            parsed *= 1024
        result[key] = parsed
    return result


def os_release() -> dict[str, str]:
    result: dict[str, str] = {}
    raw = read_text(Path("/etc/os-release")) or ""
    for line in raw.splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key in {"NAME", "VERSION", "VERSION_ID", "ID", "PRETTY_NAME"}:
            result[key] = value.strip('"')
    return result


def cpu_temperature() -> float | None:
    for path in [Path("/sys/class/thermal/thermal_zone0/temp"), Path("/sys/class/hwmon/hwmon0/temp1_input")]:
        raw = read_text(path)
        if raw:
            try:
                value = float(raw)
                return value / 1000.0 if value > 1000 else value
            except ValueError:
                pass
    return None


def throttled() -> dict[str, Any]:
    result = command(["vcgencmd", "get_throttled"])
    value = None
    if result["available"] and result["returncode"] == 0 and "=" in result["stdout"]:
        try:
            value = int(result["stdout"].split("=", 1)[1], 16)
        except ValueError:
            pass
    return {"value": value, "raw": result}


def wifi_interfaces() -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    root = Path("/sys/class/net")
    if not root.exists():
        return output
    for iface in sorted(root.iterdir()):
        if not (iface / "wireless").exists():
            continue
        addr = command(["ip", "-j", "addr", "show", "dev", iface.name])
        has_ip = False
        if addr["available"] and addr["returncode"] == 0 and addr["stdout"]:
            try:
                for item in json.loads(addr["stdout"]):
                    for info in item.get("addr_info", []):
                        local = info.get("local", "")
                        if info.get("family") in {"inet", "inet6"} and local and not local.startswith("fe80:"):
                            has_ip = True
            except json.JSONDecodeError:
                pass
        output.append({"name": iface.name, "operstate": read_text(iface / "operstate"), "has_ip": has_ip})
    return output


def graphics_devices() -> list[str]:
    root = Path("/dev/dri")
    return sorted(p.name for p in root.iterdir() if p.name.startswith(("card", "render"))) if root.exists() else []


def storage_smoke(output_dir: Path, size_mib: int) -> dict[str, Any]:
    target = output_dir / ".storage-smoke.bin"
    requested = size_mib * 1024 * 1024
    block = hashlib.sha256(b"IHAP-52-storage-smoke").digest() * 4096
    write_hash = hashlib.sha256()
    written = 0
    started = time.monotonic()
    with target.open("wb", buffering=0) as fh:
        while written < requested:
            chunk = block[: min(len(block), requested - written)]
            fh.write(chunk)
            write_hash.update(chunk)
            written += len(chunk)
        os.fsync(fh.fileno())
    write_seconds = time.monotonic() - started

    read_hash = hashlib.sha256()
    read_bytes = 0
    started = time.monotonic()
    with target.open("rb", buffering=0) as fh:
        while True:
            chunk = fh.read(1024 * 1024)
            if not chunk:
                break
            read_hash.update(chunk)
            read_bytes += len(chunk)
    read_seconds = time.monotonic() - started
    target.unlink(missing_ok=True)
    return {
        "bytes_written": written,
        "bytes_read": read_bytes,
        "write_sha256": write_hash.hexdigest(),
        "read_sha256": read_hash.hexdigest(),
        "hash_match": write_hash.digest() == read_hash.digest(),
        "write_seconds": round(write_seconds, 4),
        "read_seconds": round(read_seconds, 4),
        "temporary_file_removed": not target.exists(),
    }


def worker(stop_at: float) -> None:
    value = b"homeedge-ihap-52"
    while time.monotonic() < stop_at:
        value = hashlib.sha256(value).digest()


def stress(seconds: int, workers: int) -> dict[str, Any]:
    stop_at = time.monotonic() + seconds
    procs = [mp.Process(target=worker, args=(stop_at,)) for _ in range(workers)]
    for p in procs:
        p.start()
    samples: list[dict[str, Any]] = []
    while any(p.is_alive() for p in procs):
        memory = meminfo()
        samples.append({
            "temperature_c": cpu_temperature(),
            "loadavg": list(os.getloadavg()) if hasattr(os, "getloadavg") else None,
            "mem_available_bytes": memory.get("MemAvailable"),
        })
        remaining = stop_at - time.monotonic()
        if remaining <= 0:
            break
        time.sleep(min(5, remaining))
    for p in procs:
        p.join(timeout=5)
    return {"duration_seconds": seconds, "workers": workers, "samples": samples, "worker_exitcodes": [p.exitcode for p in procs]}


def main() -> int:
    parser = argparse.ArgumentParser(description="IHAP-52 central-node hardware validation")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--stress-seconds", type=int, default=300)
    parser.add_argument("--storage-mib", type=int, default=128)
    parser.add_argument("--wifi-host", default=None)
    args = parser.parse_args()
    if args.stress_seconds < 10:
        parser.error("--stress-seconds must be >=10")
    if not 16 <= args.storage_mib <= 1024:
        parser.error("--storage-mib must be between 16 and 1024")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    before_throttle = throttled()
    usage = shutil.disk_usage("/")
    cpu_count = os.cpu_count() or 0
    payload: dict[str, Any] = {
        "schema_version": 2,
        "generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "system": {
            "raspberry_model": read_text(Path("/proc/device-tree/model")),
            "architecture": platform.machine(),
            "logical_cpus": cpu_count,
            "memory": meminfo(),
            "os_release": os_release(),
            "graphics_devices": graphics_devices(),
        },
        "storage": {"filesystem_total_bytes": usage.total, "filesystem_free_bytes": usage.free, "lsblk": command(["lsblk", "-J", "-b", "-o", "NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS,MODEL"])},
        "network": {"wifi_interfaces": wifi_interfaces(), "optional_local_ping": command(["ping", "-c", "3", "-W", "2", args.wifi_host]) if args.wifi_host else None},
        "raspberry_pi": {"throttled_before": before_throttle},
    }
    payload["storage_smoke"] = storage_smoke(args.output_dir, args.storage_mib)
    payload["stress"] = stress(args.stress_seconds, cpu_count)
    payload["raspberry_pi"]["throttled_after"] = throttled()

    wifi_ok = any(i["operstate"] == "up" and i["has_ip"] for i in payload["network"]["wifi_interfaces"])
    after = payload["raspberry_pi"]["throttled_after"]["value"]
    checks = {
        "architecture": platform.machine().lower() in {"aarch64", "arm64", "x86_64", "amd64"},
        "logical_cpus": cpu_count >= MIN_LOGICAL_CPUS,
        "ram": payload["system"]["memory"].get("MemTotal", 0) >= MIN_RAM_BYTES,
        "storage": usage.total >= MIN_STORAGE_BYTES,
        "wifi": wifi_ok,
        "graphics_compute_device": bool(payload["system"]["graphics_devices"]),
        "storage_integrity": payload["storage_smoke"]["hash_match"] and payload["storage_smoke"]["temporary_file_removed"],
        "stress_workers": all(code == 0 for code in payload["stress"]["worker_exitcodes"]),
        "current_undervoltage": None if after is None else (after & 0x1) == 0,
        "current_throttling": None if after is None else (after & 0x4) == 0,
    }
    mandatory = [value for value in checks.values() if value is not None]
    payload["evaluation"] = {"checks": checks, "overall_pass": all(mandatory)}

    json_path = args.output_dir / "validation.json"
    md_path = args.output_dir / "validation.md"
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(
        "# IHAP-52 Central Node Validation Summary\n\n"
        f"- Model: `{payload['system']['raspberry_model'] or 'not reported'}`\n"
        f"- OS: `{payload['system']['os_release'].get('PRETTY_NAME', 'not reported')}`\n"
        f"- Architecture: `{payload['system']['architecture']}`\n"
        f"- CPUs: `{cpu_count}`\n"
        f"- RAM bytes: `{payload['system']['memory'].get('MemTotal')}`\n"
        f"- Root filesystem bytes: `{usage.total}`\n"
        f"- Overall automated gate: `{'PASS' if payload['evaluation']['overall_pass'] else 'FAIL'}`\n\n"
        "Final application workload, microSD endurance and AI acceleration remain `[UNVALIDATED]`.\n",
        encoding="utf-8",
    )
    return 0 if payload["evaluation"]["overall_pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
