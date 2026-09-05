#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import multiprocessing as mp
import os
import platform
import re
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any

MIN_LOGICAL_CPUS = 4
MIN_RAM_BYTES = 4_000_000_000
MIN_STORAGE_BYTES = 28_000_000_000
MIN_PI4_PSU_AMPS = 2.5
DEFAULT_STRESS_SECONDS = 300
DEFAULT_STORAGE_MIB = 128
PROGRESS_INTERVAL_SECONDS = 5

PI_CURRENT_MASK = 0xF
PI_HISTORY_MASK = 0xF0000
PI_UNDERVOLTAGE_MASK = (1 << 0) | (1 << 16)
PI_FREQUENCY_THROTTLE_MASK = (1 << 1) | (1 << 2) | (1 << 17) | (1 << 18)
PI_SOFT_TEMPERATURE_MASK = (1 << 3) | (1 << 19)

PI4_MODEL_TOKEN = "Raspberry Pi 4 Model B"


def log(message: str) -> None:
    print(f"[IHAP-52] {message}", flush=True)


def format_bytes(value: int | None) -> str:
    if value is None:
        return "n/a"
    return f"{value / (1024 ** 2):.0f} MiB"


def print_gate_results(title: str, checks: dict[str, bool]) -> None:
    log(title)
    for name, passed in checks.items():
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}", flush=True)


def command(args: list[str], timeout: int = 10) -> dict[str, Any]:
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=timeout, check=False)
        return {
            "available": True,
            "returncode": p.returncode,
            "stdout": p.stdout.strip(),
            "stderr": p.stderr.strip(),
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
    for path in [
        Path("/sys/class/thermal/thermal_zone0/temp"),
        Path("/sys/class/hwmon/hwmon0/temp1_input"),
    ]:
        raw = read_text(path)
        if raw:
            try:
                value = float(raw)
                return value / 1000.0 if value > 1000 else value
            except ValueError:
                pass
    return None


def parse_throttled(raw: dict[str, Any]) -> int | None:
    if not raw.get("available") or raw.get("returncode") != 0:
        return None
    stdout = str(raw.get("stdout", ""))
    if "=" not in stdout:
        return None
    try:
        return int(stdout.split("=", 1)[1], 16)
    except ValueError:
        return None


def throttled() -> dict[str, Any]:
    raw = command(["vcgencmd", "get_throttled"])
    return {"value": parse_throttled(raw), "raw": raw}


def decode_throttled(value: int | None) -> dict[str, bool | None]:
    if value is None:
        return {
            "current_undervoltage": None,
            "current_frequency_capped": None,
            "current_throttled": None,
            "current_soft_temperature_limit": None,
            "historical_undervoltage": None,
            "historical_frequency_capped": None,
            "historical_throttled": None,
            "historical_soft_temperature_limit": None,
        }
    return {
        "current_undervoltage": bool(value & (1 << 0)),
        "current_frequency_capped": bool(value & (1 << 1)),
        "current_throttled": bool(value & (1 << 2)),
        "current_soft_temperature_limit": bool(value & (1 << 3)),
        "historical_undervoltage": bool(value & (1 << 16)),
        "historical_frequency_capped": bool(value & (1 << 17)),
        "historical_throttled": bool(value & (1 << 18)),
        "historical_soft_temperature_limit": bool(value & (1 << 19)),
    }


def throttle_flags(value: int | None) -> list[str]:
    decoded = decode_throttled(value)
    return [name for name, active in decoded.items() if active is True]


def format_throttle(value: int | None) -> str:
    if value is None:
        return "unavailable"
    flags = throttle_flags(value)
    suffix = ",".join(flags) if flags else "none"
    return f"0x{value:x} ({suffix})"


def parse_psu_rating(text: str) -> dict[str, Any]:
    normalized = text.replace(",", ".")
    voltage_match = re.search(r"(\d+(?:\.\d+)?)\s*V\b", normalized, re.IGNORECASE)
    amps_match = re.search(r"(\d+(?:\.\d+)?)\s*A\b", normalized, re.IGNORECASE)
    if not voltage_match or not amps_match:
        return {
            "parsed": False,
            "volts": None,
            "amps": None,
            "supported_for_pi4_reference": False,
        }
    volts = float(voltage_match.group(1))
    amps = float(amps_match.group(1))
    supported = 4.9 <= volts <= 5.2 and amps >= MIN_PI4_PSU_AMPS
    return {
        "parsed": True,
        "volts": volts,
        "amps": amps,
        "supported_for_pi4_reference": supported,
    }


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
        output.append(
            {
                "name": iface.name,
                "operstate": read_text(iface / "operstate"),
                "has_ip": has_ip,
            }
        )
    return output


def graphics_devices() -> list[str]:
    root = Path("/dev/dri")
    return (
        sorted(p.name for p in root.iterdir() if p.name.startswith(("card", "render")))
        if root.exists()
        else []
    )


def make_run_dir(base: Path) -> Path:
    stamp = time.strftime("pi4b-%Y%m%dT%H%M%SZ", time.gmtime())
    candidate = base / stamp
    index = 1
    while candidate.exists():
        candidate = base / f"{stamp}-{index:02d}"
        index += 1
    return candidate


def storage_smoke(output_dir: Path, size_mib: int) -> dict[str, Any]:
    target = output_dir / ".storage-smoke.bin"
    requested = size_mib * 1024 * 1024
    block = hashlib.sha256(b"IHAP-52-storage-smoke").digest() * 4096
    write_hash = hashlib.sha256()
    written = 0

    log(f"STORAGE: scrittura deterministica di {size_mib} MiB...")
    started = time.monotonic()
    next_report = max(requested // 4, 1)
    with target.open("wb", buffering=0) as fh:
        while written < requested:
            chunk = block[: min(len(block), requested - written)]
            fh.write(chunk)
            write_hash.update(chunk)
            written += len(chunk)
            if written >= next_report or written == requested:
                log(
                    f"STORAGE write: {written * 100 // requested}% "
                    f"({written // (1024 ** 2)}/{size_mib} MiB)"
                )
                next_report += max(requested // 4, 1)
        os.fsync(fh.fileno())
    write_seconds = time.monotonic() - started

    log("STORAGE: rilettura e verifica SHA-256...")
    read_hash = hashlib.sha256()
    read_bytes = 0
    started = time.monotonic()
    next_report = max(requested // 4, 1)
    with target.open("rb", buffering=0) as fh:
        while True:
            chunk = fh.read(1024 * 1024)
            if not chunk:
                break
            read_hash.update(chunk)
            read_bytes += len(chunk)
            if read_bytes >= next_report or read_bytes == requested:
                log(
                    f"STORAGE read: {min(read_bytes * 100 // requested, 100)}% "
                    f"({read_bytes // (1024 ** 2)}/{size_mib} MiB)"
                )
                next_report += max(requested // 4, 1)
    read_seconds = time.monotonic() - started
    target.unlink(missing_ok=True)
    hash_match = write_hash.digest() == read_hash.digest()
    log(
        f"STORAGE: "
        f"{'PASS' if hash_match and written == requested and read_bytes == requested else 'FAIL'}; "
        f"write={write_seconds:.2f}s read={read_seconds:.2f}s hash_match={hash_match}"
    )
    return {
        "bytes_requested": requested,
        "bytes_written": written,
        "bytes_read": read_bytes,
        "write_sha256": write_hash.hexdigest(),
        "read_sha256": read_hash.hexdigest(),
        "hash_match": hash_match,
        "write_seconds": round(write_seconds, 4),
        "read_seconds": round(read_seconds, 4),
        "temporary_file_removed": not target.exists(),
    }


def worker(stop_at: float) -> None:
    value = b"homeedge-ihap-52"
    while time.monotonic() < stop_at:
        value = hashlib.sha256(value).digest()


def stress(seconds: int, workers: int, monitor_pi: bool = False) -> dict[str, Any]:
    started = time.monotonic()
    stop_at = started + seconds
    procs = [mp.Process(target=worker, args=(stop_at,)) for _ in range(workers)]
    log(f"STRESS: avvio {workers} worker CPU per {seconds}s")
    for proc in procs:
        proc.start()

    samples: list[dict[str, Any]] = []
    while any(proc.is_alive() for proc in procs):
        now = time.monotonic()
        elapsed = min(seconds, max(0.0, now - started))
        remaining = max(0.0, stop_at - now)
        memory = meminfo()
        temp = cpu_temperature()
        loadavg = list(os.getloadavg()) if hasattr(os, "getloadavg") else None
        available = memory.get("MemAvailable")

        throttle_sample = throttled() if monitor_pi else {"value": None, "raw": None}
        throttle_value = throttle_sample.get("value")
        throttle_decoded = decode_throttled(throttle_value) if monitor_pi else None

        samples.append(
            {
                "at_monotonic": round(now, 3),
                "elapsed_seconds": round(elapsed, 3),
                "temperature_c": temp,
                "loadavg": loadavg,
                "mem_available_bytes": available,
                "throttled": throttle_sample if monitor_pi else None,
                "throttled_decoded": throttle_decoded,
            }
        )

        percent = min(100, int((elapsed / seconds) * 100)) if seconds else 100
        temp_text = f"{temp:.1f}C" if temp is not None else "n/a"
        load_text = f"{loadavg[0]:.2f}" if loadavg else "n/a"
        throttle_text = f" | throttle={format_throttle(throttle_value)}" if monitor_pi else ""
        log(
            f"STRESS {percent:3d}% | elapsed={elapsed:5.0f}s | remaining={remaining:5.0f}s | "
            f"temp={temp_text} | load1={load_text} | mem_avail={format_bytes(available)}"
            f"{throttle_text}"
        )
        if remaining <= 0:
            break
        time.sleep(min(PROGRESS_INTERVAL_SECONDS, remaining))

    for proc in procs:
        proc.join(timeout=5)
    exitcodes = [proc.exitcode for proc in procs]
    log(f"STRESS: completato; worker exit codes={exitcodes}")
    return {
        "duration_seconds": seconds,
        "workers": workers,
        "samples": samples,
        "worker_exitcodes": exitcodes,
    }


def oom_observation() -> dict[str, Any]:
    raw = command(["dmesg", "--level=err,warn"], timeout=15)
    if not raw["available"] or raw["returncode"] != 0:
        return {"available": False, "oom_pattern_seen": None}
    pattern = re.compile(r"out of memory|oom-kill|killed process", re.IGNORECASE)
    return {
        "available": True,
        "oom_pattern_seen": bool(pattern.search(raw["stdout"])),
    }


def collect_snapshot() -> dict[str, Any]:
    usage = shutil.disk_usage("/")
    cpu_count = os.cpu_count() or 0
    before_throttle = throttled()
    repo_commit = command(["git", "rev-parse", "HEAD"])
    repo_branch = command(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    repo_status = command(["git", "status", "--porcelain"])
    return {
        "repository": {
            "commit": repo_commit,
            "branch": repo_branch,
            "status": repo_status,
        },
        "system": {
            "raspberry_model": read_text(Path("/proc/device-tree/model")),
            "architecture": platform.machine(),
            "logical_cpus": cpu_count,
            "memory": meminfo(),
            "os_release": os_release(),
            "graphics_devices": graphics_devices(),
            "boot_id": read_text(Path("/proc/sys/kernel/random/boot_id")),
            "uptime_seconds": float(
                (read_text(Path("/proc/uptime")) or "0").split()[0]
            ),
        },
        "storage": {
            "filesystem_total_bytes": usage.total,
            "filesystem_free_bytes": usage.free,
            "lsblk": command(
                [
                    "lsblk",
                    "-J",
                    "-b",
                    "-o",
                    "NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS,MODEL",
                ]
            ),
        },
        "network": {"wifi_interfaces": wifi_interfaces()},
        "raspberry_pi": {
            "throttled_before": before_throttle,
            "throttled_before_decoded": decode_throttled(before_throttle["value"]),
        },
    }


def evaluate_preflight(
    snapshot: dict[str, Any],
    profile: str,
    manual: dict[str, Any] | None = None,
) -> dict[str, bool]:
    system = snapshot["system"]
    wifi_ok = any(
        item["operstate"] == "up" and item["has_ip"]
        for item in snapshot["network"]["wifi_interfaces"]
    )
    checks: dict[str, bool] = {
        "architecture": system["architecture"].lower()
        in {"aarch64", "arm64", "x86_64", "amd64"},
        "logical_cpus": system["logical_cpus"] >= MIN_LOGICAL_CPUS,
        "ram": system["memory"].get("MemTotal", 0) >= MIN_RAM_BYTES,
        "storage_capacity": snapshot["storage"]["filesystem_total_bytes"]
        >= MIN_STORAGE_BYTES,
        "wifi": wifi_ok,
        "repository_commit_recorded": snapshot.get("repository", {})
        .get("commit", {})
        .get("returncode")
        == 0,
        "repository_clean": snapshot.get("repository", {})
        .get("status", {})
        .get("returncode")
        == 0
        and snapshot.get("repository", {}).get("status", {}).get("stdout", "")
        == "",
    }
    if profile == "pi4-reference":
        model = system.get("raspberry_model") or ""
        throttle_value = snapshot["raspberry_pi"]["throttled_before"]["value"]
        checks.update(
            {
                "pi4_model": PI4_MODEL_TOKEN in model,
                "pi4_aarch64": system["architecture"].lower()
                in {"aarch64", "arm64"},
                "vcgencmd_available": throttle_value is not None,
                "clean_throttle_history_before_run": throttle_value is not None
                and (throttle_value & (PI_CURRENT_MASK | PI_HISTORY_MASK)) == 0,
            }
        )
        if manual is not None:
            sd_class = str(manual.get("sd_application_class", "")).strip().upper()
            psu = parse_psu_rating(str(manual.get("psu_rating", "")))
            checks["manual_sd_application_class_supported"] = sd_class in {"A1", "A2"}
            checks["manual_rpios_lite64_confirmed"] = (
                manual.get("rpios_lite64_confirmed") is True
            )
            checks["manual_psu_rating_parseable"] = psu["parsed"] is True
            checks["manual_psu_supported_for_pi4"] = (
                psu["supported_for_pi4_reference"] is True
            )
    return checks


def _pi_observed_throttle_values(payload: dict[str, Any]) -> list[int]:
    values: list[int] = []
    after = payload.get("raspberry_pi", {}).get("throttled_after", {}).get("value")
    if isinstance(after, int):
        values.append(after)
    for sample in payload.get("stress", {}).get("samples", []):
        value = (sample.get("throttled") or {}).get("value")
        if isinstance(value, int):
            values.append(value)
    return values


def evaluate_final(payload: dict[str, Any], profile: str) -> dict[str, bool]:
    smoke = payload["storage_smoke"]
    stress_result = payload["stress"]
    after = payload["raspberry_pi"]["throttled_after"]["value"]
    checks: dict[str, bool] = {
        "storage_integrity": smoke["bytes_written"] == smoke["bytes_requested"]
        and smoke["bytes_read"] == smoke["bytes_requested"]
        and smoke["hash_match"]
        and smoke["temporary_file_removed"],
        "stress_workers": bool(stress_result["worker_exitcodes"])
        and all(code == 0 for code in stress_result["worker_exitcodes"]),
        "boot_stability": bool(payload["system"]["boot_id"])
        and payload["system"]["boot_id"] == payload["system_after"]["boot_id"],
    }
    oom = payload.get("oom_observation", {})
    if oom.get("available"):
        checks["no_oom_pattern"] = oom.get("oom_pattern_seen") is False

    if profile == "pi4-reference":
        values = _pi_observed_throttle_values(payload)
        checks["vcgencmd_after_available"] = after is not None
        checks["no_pi_undervoltage"] = bool(values) and all(
            (value & PI_UNDERVOLTAGE_MASK) == 0 for value in values
        )
        checks["no_pi_frequency_cap_or_throttle"] = bool(values) and all(
            (value & PI_FREQUENCY_THROTTLE_MASK) == 0 for value in values
        )
        checks["no_pi_soft_temperature_limit"] = bool(values) and all(
            (value & PI_SOFT_TEMPERATURE_MASK) == 0 for value in values
        )
    return checks


def prompt_yes_no(label: str) -> bool:
    while True:
        value = input(f"{label} [y/n]: ").strip().lower()
        if value in {"y", "yes", "s", "si", "sì"}:
            return True
        if value in {"n", "no"}:
            return False
        print("Rispondi y/n.")


def prompt_sd_application_class() -> str:
    while True:
        value = (
            input("Classe applicativa microSD [A1/A2/other/unknown]: ").strip().upper()
            or "UNKNOWN"
        )
        if value in {"A1", "A2", "OTHER", "UNKNOWN"}:
            return value
        print("Inserisci A1, A2, other oppure unknown.")


def guided_manual_answers() -> dict[str, Any]:
    print(
        "\n[IHAP-52] Servono solo le informazioni fisiche che Linux non può verificare da solo."
    )
    sd_class = prompt_sd_application_class()
    rpios = prompt_yes_no(
        "Hai installato Raspberry Pi OS Lite 64-bit con Raspberry Pi Imager?"
    )
    card_model = input("Marca/modello microSD (invio = unknown): ").strip() or "unknown"
    psu = input("Alimentatore e rating elettrico (es. 5.1V 3A): ").strip()
    while not psu:
        print("Il rating dell'alimentatore è obbligatorio per la evidence.")
        psu = input("Alimentatore e rating elettrico: ").strip()
    psu_eval = parse_psu_rating(psu)
    if psu_eval["parsed"] and not psu_eval["supported_for_pi4_reference"]:
        log(
            f"ATTENZIONE: {psu} non soddisfa il gate Pi 4 del runbook "
            f"(>= {MIN_PI4_PSU_AMPS:.1f} A a circa 5 V)."
        )
    elif not psu_eval["parsed"]:
        log("ATTENZIONE: rating PSU non interpretabile; il pre-flight fallirà.")
    case = input("Case (invio = none): ").strip() or "none"
    heatsink = prompt_yes_no("Heatsink installato?")
    fan = prompt_yes_no("Ventola installata?")
    ambient = (
        input("Temperatura ambiente approssimativa (invio = unknown): ").strip()
        or "unknown"
    )
    return {
        "sd_application_class": sd_class,
        "rpios_lite64_confirmed": rpios,
        "card_model": card_model,
        "psu_rating": psu,
        "case": case,
        "heatsink": heatsink,
        "fan": fan,
        "ambient_temperature": ambient,
    }


def write_operator_notes(
    path: Path,
    manual: dict[str, Any],
    snapshot: dict[str, Any],
    run_id: str,
) -> None:
    system = snapshot["system"]
    path.write_text(
        "# IHAP-52 Operator Notes\n\n"
        f"Run ID: {run_id}\n"
        f"Board/model: {system.get('raspberry_model') or 'not reported'}\n"
        f"Installed RAM bytes: {system['memory'].get('MemTotal')}\n"
        f"microSD manufacturer/model: {manual.get('card_model')}\n"
        f"microSD application class: {manual.get('sd_application_class')}\n"
        f"Raspberry Pi OS Lite 64-bit selected in Imager: "
        f"{'yes' if manual.get('rpios_lite64_confirmed') else 'no'}\n"
        f"Runtime base OS: {system['os_release'].get('PRETTY_NAME', 'not reported')}\n"
        f"PSU/rating: {manual.get('psu_rating')}\n"
        f"Case: {manual.get('case')}\n"
        f"Heatsinks installed: {'yes' if manual.get('heatsink') else 'no'}\n"
        f"Fan installed: {'yes' if manual.get('fan') else 'no'}\n"
        f"Approximate ambient temperature: {manual.get('ambient_temperature')}\n\n"
        "Privacy note: no SSID, password, private IP, MAC address, hostname or username is recorded here.\n",
        encoding="utf-8",
    )


def write_summary(payload: dict[str, Any], output_dir: Path) -> None:
    checks = payload["evaluation"]["checks"]
    rows = "\n".join(
        f"| {name} | {'PASS' if value else 'FAIL'} |"
        for name, value in checks.items()
    )
    temps = [
        s["temperature_c"]
        for s in payload.get("stress", {}).get("samples", [])
        if s.get("temperature_c") is not None
    ]
    max_temp = max(temps) if temps else None
    manual = payload.get("manual_evidence") or {}
    after_value = (
        payload.get("raspberry_pi", {}).get("throttled_after", {}).get("value")
    )

    (output_dir / "validation.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (output_dir / "validation.md").write_text(
        "# IHAP-52 Central Node Validation Summary\n\n"
        f"- Run ID: `{payload['run_id']}`\n"
        f"- Profile: `{payload['profile']}`\n"
        f"- Model: `{payload['system']['raspberry_model'] or 'not reported'}`\n"
        f"- Runtime base OS: "
        f"`{payload['system']['os_release'].get('PRETTY_NAME', 'not reported')}`\n"
        f"- Imager selection: "
        f"`{'Raspberry Pi OS Lite 64-bit (operator confirmed)' if manual.get('rpios_lite64_confirmed') else 'not confirmed'}`\n"
        f"- Architecture: `{payload['system']['architecture']}`\n"
        f"- CPUs: `{payload['system']['logical_cpus']}`\n"
        f"- RAM bytes: `{payload['system']['memory'].get('MemTotal')}`\n"
        f"- Root filesystem bytes: `{payload['storage']['filesystem_total_bytes']}`\n"
        f"- microSD application class: "
        f"`{manual.get('sd_application_class', 'not recorded')}`\n"
        f"- PSU/rating: `{manual.get('psu_rating', 'not recorded')}`\n"
        f"- Max observed CPU temperature: "
        f"`{max_temp if max_temp is not None else 'not reported'}`\n"
        f"- Pi throttle word after run: `{format_throttle(after_value)}`\n"
        f"- Overall gate: "
        f"`{'PASS' if payload['evaluation']['overall_pass'] else 'FAIL'}`\n\n"
        "## Automated gates\n\n| Gate | Result |\n|---|---|\n"
        f"{rows}\n\n"
        "Final application workload, microSD endurance, retention and AI acceleration remain `[UNVALIDATED]`.\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="IHAP-52 central-node hardware validation"
    )
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument(
        "--profile",
        choices=["pi4-reference", "equivalent"],
        default="pi4-reference",
    )
    parser.add_argument("--stress-seconds", type=int, default=DEFAULT_STRESS_SECONDS)
    parser.add_argument("--storage-mib", type=int, default=DEFAULT_STORAGE_MIB)
    parser.add_argument("--wifi-host", default=None)
    parser.add_argument(
        "--guided",
        action="store_true",
        help="prompt only for unavoidable physical evidence",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="run pre-flight only; no storage write or stress",
    )
    args = parser.parse_args()

    if args.stress_seconds < 10:
        parser.error("--stress-seconds must be >=10")
    if not 16 <= args.storage_mib <= 1024:
        parser.error("--storage-mib must be between 16 and 1024")

    base_runs = Path(__file__).resolve().parent / "runs"
    output_dir = args.output_dir or make_run_dir(base_runs)
    if output_dir.exists() and any(output_dir.iterdir()):
        parser.error(
            f"output directory is not empty: {output_dir}; use a new run ID"
        )
    output_dir.mkdir(parents=True, exist_ok=True)
    run_id = output_dir.name

    log(f"RUN START: {run_id} | profile={args.profile} | dry_run={args.dry_run}")
    log("PHASE 1/5: raccolta automatica snapshot hardware/OS/rete/repository")
    snapshot = collect_snapshot()
    log(
        f"Snapshot: model={snapshot['system']['raspberry_model'] or 'n/a'} | "
        f"arch={snapshot['system']['architecture']} | "
        f"cpu={snapshot['system']['logical_cpus']} | "
        f"ram={format_bytes(snapshot['system']['memory'].get('MemTotal'))} | "
        f"throttle_pre={format_throttle(snapshot['raspberry_pi']['throttled_before']['value'])}"
    )

    log("PHASE 2/5: raccolta evidence fisica operatore")
    manual = guided_manual_answers() if args.guided else None
    if manual is not None:
        write_operator_notes(output_dir / "operator-notes.md", manual, snapshot, run_id)

    preflight = evaluate_preflight(snapshot, args.profile, manual)
    print_gate_results("PRE-FLIGHT GATES", preflight)
    payload: dict[str, Any] = {
        "schema_version": 6,
        "generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "run_id": run_id,
        "profile": args.profile,
        **snapshot,
        "manual_evidence": manual,
        "preflight": {"checks": preflight, "pass": all(preflight.values())},
    }

    if args.dry_run or not payload["preflight"]["pass"]:
        payload["evaluation"] = {
            "checks": preflight,
            "overall_pass": all(preflight.values()),
        }
        write_summary(payload, output_dir)
        log(f"PRE-FLIGHT {'PASS' if all(preflight.values()) else 'FAIL'}")
        log(f"Evidence: {output_dir}")
        return 0 if all(preflight.values()) else 2

    log(f"PHASE 3/5: storage integrity smoke test ({args.storage_mib} MiB)")
    payload["storage_smoke"] = storage_smoke(output_dir, args.storage_mib)

    worker_count = min(max(snapshot["system"]["logical_cpus"], 1), 8)
    log(f"PHASE 4/5: CPU stress ({args.stress_seconds}s, {worker_count} worker)")
    payload["stress"] = stress(
        args.stress_seconds,
        worker_count,
        monitor_pi=args.profile == "pi4-reference",
    )

    log("PHASE 5/5: post-flight power/throttle, boot stability e OOM checks")
    payload["raspberry_pi"]["throttled_after"] = throttled()
    payload["raspberry_pi"]["throttled_after_decoded"] = decode_throttled(
        payload["raspberry_pi"]["throttled_after"]["value"]
    )
    log(
        "POST-FLIGHT throttle="
        f"{format_throttle(payload['raspberry_pi']['throttled_after']['value'])}"
    )
    payload["system_after"] = {
        "boot_id": read_text(Path("/proc/sys/kernel/random/boot_id")),
        "uptime_seconds": float(
            (read_text(Path("/proc/uptime")) or "0").split()[0]
        ),
        "memory": meminfo(),
        "temperature_c": cpu_temperature(),
    }
    payload["oom_observation"] = oom_observation()
    if args.wifi_host:
        log(f"Optional LAN ping: {args.wifi_host}")
        payload["network"]["optional_local_ping"] = command(
            ["ping", "-c", "3", "-W", "2", args.wifi_host]
        )

    final_checks = evaluate_final(payload, args.profile)
    print_gate_results("POST-FLIGHT GATES", final_checks)
    all_checks = {**preflight, **final_checks}
    payload["evaluation"] = {
        "checks": all_checks,
        "overall_pass": all(all_checks.values()),
    }
    write_summary(payload, output_dir)
    log(
        f"FINAL RESULT: "
        f"{'PASS' if payload['evaluation']['overall_pass'] else 'FAIL'}"
    )
    log(f"Evidence: {output_dir}")
    return 0 if payload["evaluation"]["overall_pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
