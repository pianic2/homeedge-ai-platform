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
# Nominal 64 GB media usually exposes <64 GiB. This gate targets usable capacity.
MIN_STORAGE_BYTES = 58_000_000_000


def command(args: list[str], timeout: int = 10) -> dict[str, Any]:
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=timeout, check=False)
        return {"available": True, "returncode": p.returncode, "stdout": p.stdout.strip(), "stderr": p.stderr.strip()}
    except FileNotFoundError:
        return {"available": False, "returncode": None, "stdout": "", "stderr": "command not found"}
    except subprocess.TimeoutExpired:
        return {"available": True, "returncode": None, "stdout": "", "stderr": "timeout"}


def read_text(path: str | Path) -> str | None:
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace").strip("\x00\n ")
    except OSError:
        return None


def meminfo() -> dict[str, int]:
    values: dict[str, int] = {}
    raw = read_text("/proc/meminfo")
    if not raw:
        return values
    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, rest = line.split(":", 1)
        fields = rest.strip().split()
        if not fields:
            continue
        try:
            value = int(fields[0])
        except ValueError:
            continue
        if len(fields) > 1 and fields[1].lower() == "kb":
            value *= 1024
        values[key] = value
    return values


def temperature_c() -> float | None:
    for path in ("/sys/class/thermal/thermal_zone0/temp", "/sys/class/hwmon/hwmon0/temp1_input"):
        raw = read_text(path)
        if raw is None:
            continue
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
    decoded = None if value is None else {
        "current_undervoltage": bool(value & (1 << 0)),
        "current_frequency_capped": bool(value & (1 << 1)),
        "current_throttled": bool(value & (1 << 2)),
        "current_soft_temp_limit": bool(value & (1 << 3)),
        "historical_undervoltage": bool(value & (1 << 16)),
        "historical_frequency_capped": bool(value & (1 << 17)),
        "historical_throttled": bool(value & (1 << 18)),
        "historical_soft_temp_limit": bool(value & (1 << 19)),
    }
    return {"raw": result, "value": value, "decoded": decoded}


def wifi_interfaces() -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    root = Path("/sys/class/net")
    if not root.exists():
        return result
    for iface in sorted(root.iterdir()):
        if not (iface / "wireless").exists():
            continue
        addr = command(["ip", "-j", "addr", "show", "dev", iface.name])
        has_ip = False
        families: set[str] = set()
        if addr["available"] and addr["returncode"] == 0 and addr["stdout"]:
            try:
                for item in json.loads(addr["stdout"]):
                    for info in item.get("addr_info", []):
                        family = info.get("family")
                        local = info.get("local", "")
                        if family in {"inet", "inet6"} and local and not local.startswith("fe80:"):
                            has_ip = True
                            families.add(family)
            except json.JSONDecodeError:
                pass
        result.append({
            "name": iface.name,
            "operstate": read_text(iface / "operstate"),
            "has_ip": has_ip,
            "families": sorted(families),
        })
    return result


def graphics_devices() -> list[str]:
    dri = Path("/dev/dri")
    return [] if not dri.exists() else sorted(p.name for p in dri.iterdir() if p.name.startswith(("card", "render")))


def os_release() -> dict[str, str]:
    result: dict[str, str] = {}
    raw = read_text("/etc/os-release")
    if not raw:
        return result
    for line in raw.splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key in {"NAME", "ID", "VERSION", "VERSION_ID"}:
            result[key] = value.strip('"')
    return result


def root_storage() -> dict[str, Any]:
    usage = shutil.disk_usage("/")
    return {
        "filesystem_total_bytes": usage.total,
        "filesystem_used_bytes": usage.used,
        "filesystem_free_bytes": usage.free,
        "lsblk": command(["lsblk", "-J", "-b", "-o", "NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS,MODEL"]),
    }


def local_ping(host: str | None) -> dict[str, Any] | None:
    return None if not host else command(["ping", "-c", "3", "-W", "2", host], timeout=10)


def storage_smoke(output_dir: Path, size_mib: int) -> dict[str, Any]:
    size_bytes = size_mib * 1024 * 1024
    block = hashlib.sha256(b"IHAP-52-storage-smoke").digest() * 4096
    target = output_dir / ".storage-smoke.bin"
    written = 0
    write_hash = hashlib.sha256()
    started = time.monotonic()
    with target.open("wb", buffering=0) as fh:
        while written < size_bytes:
            chunk = block[: min(len(block), size_bytes - written)]
            fh.write(chunk)
            write_hash.update(chunk)
            written += len(chunk)
        os.fsync(fh.fileno())
    write_seconds = time.monotonic() - started

    read = 0
    read_hash = hashlib.sha256()
    started = time.monotonic()
    with target.open("rb", buffering=0) as fh:
        while chunk := fh.read(1024 * 1024):
            read_hash.update(chunk)
            read += len(chunk)
    read_seconds = time.monotonic() - started
    target.unlink(missing_ok=True)

    write_sha = write_hash.hexdigest()
    read_sha = read_hash.hexdigest()
    return {
        "requested_mib": size_mib,
        "bytes_written": written,
        "bytes_read": read,
        "write_seconds": round(write_seconds, 4),
        "read_seconds": round(read_seconds, 4),
        "write_mib_s": round((written / 1048576) / write_seconds, 2) if write_seconds else None,
        "read_mib_s": round((read / 1048576) / read_seconds, 2) if read_seconds else None,
        "write_sha256": write_sha,
        "read_sha256": read_sha,
        "hash_match": write_sha == read_sha,
        "temporary_file_removed": not target.exists(),
    }


def cpu_worker(stop_at: float) -> None:
    seed = b"homeedge-ihap-52-central-node"
    digest = seed
    while time.monotonic() < stop_at:
        digest = hashlib.sha256(digest + seed).digest()


def cpu_stress(seconds: int, workers: int, sample_seconds: int = 5) -> dict[str, Any]:
    stop_at = time.monotonic() + seconds
    processes = [mp.Process(target=cpu_worker, args=(stop_at,)) for _ in range(workers)]
    for process in processes:
        process.start()

    samples: list[dict[str, Any]] = []
    while any(process.is_alive() for process in processes):
        remaining = max(0.0, stop_at - time.monotonic())
        samples.append({
            "elapsed_seconds": round(seconds - remaining, 2),
            "temperature_c": temperature_c(),
            "loadavg": list(os.getloadavg()) if hasattr(os, "getloadavg") else None,
            "mem_available_bytes": meminfo().get("MemAvailable"),
        })
        if remaining <= 0:
            break
        time.sleep(min(sample_seconds, remaining))

    for process in processes:
        process.join(timeout=5)
    return {
        "duration_seconds": seconds,
        "workers": workers,
        "samples": samples,
        "worker_exitcodes": [process.exitcode for process in processes],
    }


def evaluate(payload: dict[str, Any]) -> dict[str, Any]:
    arch = payload["system"]["architecture"].lower()
    cpus = payload["system"]["logical_cpus"] or 0
    ram = payload["system"]["memory_before"].get("MemTotal", 0)
    storage = payload["storage"]["filesystem_total_bytes"]
    wifi = payload["network"]["wifi_interfaces"]
    graphics = payload["system"]["graphics_devices"]
    smoke = payload["storage_smoke"]
    exitcodes = payload["stress"]["worker_exitcodes"]
    throttle = payload["raspberry_pi"]["throttled_after"]["decoded"]

    checks: dict[str, dict[str, Any]] = {
        "architecture": {"pass": arch in {"aarch64", "arm64", "x86_64", "amd64"}, "observed": arch},
        "logical_cpus": {"pass": cpus >= MIN_LOGICAL_CPUS, "observed": cpus, "minimum": MIN_LOGICAL_CPUS},
        "ram": {"pass": ram >= MIN_RAM_BYTES, "observed_bytes": ram, "minimum_bytes": MIN_RAM_BYTES},
        "storage": {"pass": storage >= MIN_STORAGE_BYTES, "observed_bytes": storage, "minimum_bytes": MIN_STORAGE_BYTES},
        "wifi": {"pass": any(i["operstate"] == "up" and i["has_ip"] for i in wifi), "observed_interfaces": wifi},
        "graphics_compute_device": {"pass": bool(graphics), "observed": graphics, "note": "Presence only; AI acceleration remains UNVALIDATED."},
        "storage_smoke": {"pass": smoke["bytes_written"] == smoke["bytes_read"] and smoke["hash_match"] and smoke["temporary_file_removed"], "observed": {"hash_match": smoke["hash_match"]}},
        "stress_workers": {"pass": all(code == 0 for code in exitcodes), "observed": exitcodes},
    }
    if throttle is None:
        checks["raspberry_pi_current_undervoltage"] = {"pass": None, "observed": None, "note": "vcgencmd unavailable or non-Raspberry Pi"}
        checks["raspberry_pi_current_throttling"] = {"pass": None, "observed": None, "note": "vcgencmd unavailable or non-Raspberry Pi"}
    else:
        checks["raspberry_pi_current_undervoltage"] = {"pass": not throttle["current_undervoltage"], "observed": throttle["current_undervoltage"]}
        checks["raspberry_pi_current_throttling"] = {"pass": not throttle["current_throttled"], "observed": throttle["current_throttled"]}

    applicable = [item["pass"] for item in checks.values() if item["pass"] is not None]
    return {"checks": checks, "overall_pass": all(applicable)}


def markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# IHAP-52 Central Node Validation Summary", "",
        f"- Generated at (UTC): `{payload['generated_at_utc']}`",
        f"- Model: `{payload['system'].get('raspberry_model') or 'not reported'}`",
        f"- Architecture: `{payload['system']['architecture']}`",
        f"- Logical CPUs: `{payload['system']['logical_cpus']}`",
        f"- RAM bytes: `{payload['system']['memory_before'].get('MemTotal')}`",
        f"- Root filesystem bytes: `{payload['storage']['filesystem_total_bytes']}`",
        f"- Automated gate: `{'PASS' if payload['evaluation']['overall_pass'] else 'FAIL'}`", "",
        "## Automated checks", "", "| Check | Result |", "|---|---|",
    ]
    for name, check in payload["evaluation"]["checks"].items():
        result = "N/A" if check["pass"] is None else ("PASS" if check["pass"] else "FAIL")
        lines.append(f"| `{name}` | {result} |")
    lines += [
        "", "## Evidence boundaries", "",
        "- Bounded hardware/resource smoke test only; final application workload remains `[UNVALIDATED]`.",
        "- microSD endurance remains `[UNVALIDATED]`.",
        "- future AI runtime/model and GPU/NPU acceleration remain `[UNVALIDATED]`.",
        "- Docker, Alpine Linux, database and orchestration are outside this run.",
        "- Review raw output before publication.", "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="IHAP-52 central-node hardware validation harness")
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--stress-seconds", type=int, default=300)
    parser.add_argument("--storage-mib", type=int, default=128)
    parser.add_argument("--wifi-host", help="Optional authorized local host to ping")
    args = parser.parse_args()
    if args.stress_seconds < 10:
        parser.error("--stress-seconds must be at least 10")
    if not 16 <= args.storage_mib <= 1024:
        parser.error("--storage-mib must be between 16 and 1024")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {
        "schema_version": 1,
        "generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "system": {
            "raspberry_model": read_text("/proc/device-tree/model"),
            "architecture": platform.machine(),
            "logical_cpus": os.cpu_count(),
            "kernel": platform.release(),
            "os_release": os_release(),
            "memory_before": meminfo(),
            "graphics_devices": graphics_devices(),
        },
        "network": {"wifi_interfaces": wifi_interfaces(), "optional_local_ping": local_ping(args.wifi_host)},
        "storage": root_storage(),
        "raspberry_pi": {"throttled_before": throttled()},
    }
    payload["storage_smoke"] = storage_smoke(args.output_dir, args.storage_mib)
    payload["stress"] = cpu_stress(args.stress_seconds, os.cpu_count() or 1)
    payload["raspberry_pi"]["throttled_after"] = throttled()
    payload["system"]["memory_after"] = meminfo()
    payload["system"]["temperature_after_c"] = temperature_c()
    payload["evaluation"] = evaluate(payload)
    payload["evidence_boundaries"] = {
        "final_workload_sufficiency": "UNVALIDATED",
        "storage_endurance": "UNVALIDATED",
        "ai_runtime_model": "UNVALIDATED",
        "gpu_npu_ai_acceleration": "UNVALIDATED",
        "docker_alpine_database_orchestration": "OUT_OF_SCOPE",
    }

    (args.output_dir / "validation.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (args.output_dir / "validation.md").write_text(markdown(payload), encoding="utf-8")
    print(f"Wrote {args.output_dir / 'validation.json'}")
    print(f"Wrote {args.output_dir / 'validation.md'}")
    print("Automated gate:", "PASS" if payload["evaluation"]["overall_pass"] else "FAIL")
    return 0 if payload["evaluation"]["overall_pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
