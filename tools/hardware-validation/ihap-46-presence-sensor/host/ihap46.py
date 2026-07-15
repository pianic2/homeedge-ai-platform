#!/usr/bin/env python3
"""IHAP-46 presence-sensor validation harness.

This host utility captures newline-delimited JSON emitted by the ESP-IDF
laboratory firmware, records manual ground-truth markers, evaluates the
configured scenario matrix and produces machine-readable and human-readable
reports.

It is deliberately test-only. Detailed radar telemetry handled here is
laboratory evidence and is not an MVP production event contract.
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import html
import json
import os
from pathlib import Path
import statistics
import sys
import time
from typing import Any, Iterable, Iterator, Mapping, Sequence

SCHEMA_VERSION = "1.0.0"
DEFAULT_BAUD = 115200
DEFAULT_RUNS_DIR = Path("runs")
SENSOR_PATHS: dict[str, tuple[str, ...]] = {
    "ld2410c_uart": ("ld2410c", "uart_presence"),
    "ld2410c_out": ("ld2410c", "out"),
    "pir_out": ("pir", "out"),
}
GROUND_TRUTH_VALUES = {
    "empty",
    "present_moving",
    "present_stationary",
    "adjacent_activity",
    "unknown",
}
DOOR_VALUES = {"open", "closed", "unknown"}
PHASE_VALUES = {"start", "end", "point"}


class HarnessError(RuntimeError):
    """User-facing validation or capture error."""


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def isoformat_utc(value: dt.datetime | None = None) -> str:
    return (value or utc_now()).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def epoch_ms() -> int:
    return time.time_ns() // 1_000_000


def load_json(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError as exc:
        raise HarnessError(f"File not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise HarnessError(f"Invalid JSON in {path}: {exc}") from exc


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def append_jsonl(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, separators=(",", ":"), sort_keys=True))
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())


def iter_jsonl(path: Path) -> Iterator[dict[str, Any]]:
    if not path.exists():
        return
    with path.open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()
            if not line:
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                raise HarnessError(f"Invalid JSONL in {path}:{line_number}: {exc}") from exc
            if not isinstance(value, dict):
                raise HarnessError(f"Expected object in {path}:{line_number}")
            yield value


def validate_plan(plan: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if plan.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
    if plan.get("issue") != "IHAP-46":
        errors.append("issue must be IHAP-46")
    scenarios = plan.get("scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        errors.append("scenarios must be a non-empty array")
        return errors

    seen: set[str] = set()
    for index, scenario in enumerate(scenarios):
        prefix = f"scenarios[{index}]"
        if not isinstance(scenario, dict):
            errors.append(f"{prefix} must be an object")
            continue
        scenario_id = scenario.get("id")
        if not isinstance(scenario_id, str) or not scenario_id:
            errors.append(f"{prefix}.id must be a non-empty string")
        elif scenario_id in seen:
            errors.append(f"duplicate scenario id: {scenario_id}")
        else:
            seen.add(scenario_id)
        if scenario.get("ground_truth") not in GROUND_TRUTH_VALUES:
            errors.append(f"{prefix}.ground_truth must be one of {sorted(GROUND_TRUTH_VALUES)}")
        if scenario.get("door_state") not in DOOR_VALUES:
            errors.append(f"{prefix}.door_state must be one of {sorted(DOOR_VALUES)}")
        for numeric_field in ("duration_s", "repetitions"):
            value = scenario.get(numeric_field)
            if not isinstance(value, (int, float)) or value <= 0:
                errors.append(f"{prefix}.{numeric_field} must be > 0")
        expected = scenario.get("expected")
        if not isinstance(expected, dict) or not expected:
            errors.append(f"{prefix}.expected must be a non-empty object")
            continue
        for sensor_id, rule in expected.items():
            if sensor_id not in SENSOR_PATHS:
                errors.append(f"{prefix}.expected contains unknown sensor {sensor_id}")
                continue
            if not isinstance(rule, dict):
                errors.append(f"{prefix}.expected.{sensor_id} must be an object")
                continue
            for key in ("min_presence_ratio", "max_presence_ratio"):
                if key in rule:
                    threshold = rule[key]
                    if not isinstance(threshold, (int, float)) or not 0 <= threshold <= 1:
                        errors.append(f"{prefix}.expected.{sensor_id}.{key} must be between 0 and 1")
    return errors


def require_valid_plan(path: Path) -> dict[str, Any]:
    plan = load_json(path)
    if not isinstance(plan, dict):
        raise HarnessError(f"Plan root must be an object: {path}")
    errors = validate_plan(plan)
    if errors:
        raise HarnessError("Invalid test plan:\n- " + "\n- ".join(errors))
    return plan


def scenario_index(plan: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(item["id"]): dict(item) for item in plan["scenarios"]}


def get_nested(mapping: Mapping[str, Any], path: Sequence[str]) -> Any:
    current: Any = mapping
    for key in path:
        if not isinstance(current, Mapping) or key not in current:
            return None
        current = current[key]
    return current


def normalize_sensor_value(source_record: Mapping[str, Any], sensor_id: str) -> bool | None:
    value = get_nested(source_record, SENSOR_PATHS[sensor_id])
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    return None


@dataclasses.dataclass(frozen=True)
class ScenarioInterval:
    scenario_id: str
    repetition: int
    start_ms: int
    end_ms: int
    ground_truth: str
    door_state: str
    note: str


def build_intervals(markers: Iterable[Mapping[str, Any]], plan: Mapping[str, Any]) -> tuple[list[ScenarioInterval], list[str]]:
    scenarios = scenario_index(plan)
    open_intervals: dict[tuple[str, int], Mapping[str, Any]] = {}
    intervals: list[ScenarioInterval] = []
    warnings: list[str] = []

    ordered = sorted(markers, key=lambda item: int(item.get("at_epoch_ms", 0)))
    for marker in ordered:
        scenario_id = str(marker.get("scenario_id", ""))
        repetition = int(marker.get("repetition", 1))
        phase = marker.get("phase")
        key = (scenario_id, repetition)
        if scenario_id not in scenarios:
            warnings.append(f"Unknown scenario marker ignored: {scenario_id}")
            continue
        if phase == "start":
            if key in open_intervals:
                warnings.append(f"Duplicate start marker replaced: {scenario_id} rep {repetition}")
            open_intervals[key] = marker
        elif phase == "end":
            start = open_intervals.pop(key, None)
            if start is None:
                warnings.append(f"End marker without start: {scenario_id} rep {repetition}")
                continue
            start_ms = int(start["at_epoch_ms"])
            end_ms = int(marker["at_epoch_ms"])
            if end_ms <= start_ms:
                warnings.append(f"Non-positive interval ignored: {scenario_id} rep {repetition}")
                continue
            scenario = scenarios[scenario_id]
            intervals.append(ScenarioInterval(
                scenario_id=scenario_id,
                repetition=repetition,
                start_ms=start_ms,
                end_ms=end_ms,
                ground_truth=str(scenario["ground_truth"]),
                door_state=str(scenario["door_state"]),
                note=str(start.get("note") or marker.get("note") or ""),
            ))
        elif phase == "point":
            warnings.append(f"Point marker retained as annotation only: {scenario_id}")
        else:
            warnings.append(f"Invalid marker phase ignored: {phase!r}")

    for scenario_id, repetition in sorted(open_intervals):
        warnings.append(f"Open interval without end: {scenario_id} rep {repetition}")

    intervals.sort(key=lambda item: item.start_ms)
    return intervals, warnings


def records_in_interval(records: Iterable[Mapping[str, Any]], interval: ScenarioInterval) -> list[Mapping[str, Any]]:
    result: list[Mapping[str, Any]] = []
    for record in records:
        received = int(record.get("received_at_epoch_ms", 0))
        source = record.get("source")
        if interval.start_ms <= received <= interval.end_ms and isinstance(source, Mapping):
            if source.get("record_type") == "sample":
                result.append(record)
    return result


def first_true_latency_ms(records: Sequence[Mapping[str, Any]], interval: ScenarioInterval, sensor_id: str) -> int | None:
    for record in records:
        source = record.get("source")
        if not isinstance(source, Mapping):
            continue
        if normalize_sensor_value(source, sensor_id) is True:
            return max(0, int(record["received_at_epoch_ms"]) - interval.start_ms)
    return None


def evaluate_interval(interval: ScenarioInterval, records: Sequence[Mapping[str, Any]], scenario: Mapping[str, Any]) -> dict[str, Any]:
    sensors: dict[str, Any] = {}
    for sensor_id, rule in scenario["expected"].items():
        values: list[bool] = []
        for record in records:
            source = record.get("source")
            if not isinstance(source, Mapping):
                continue
            value = normalize_sensor_value(source, sensor_id)
            if value is not None:
                values.append(value)
        presence_ratio = sum(values) / len(values) if values else None
        failures: list[str] = []
        if presence_ratio is None:
            failures.append("no samples")
        else:
            minimum = rule.get("min_presence_ratio")
            maximum = rule.get("max_presence_ratio")
            if minimum is not None and presence_ratio < float(minimum):
                failures.append(f"presence ratio {presence_ratio:.3f} < {float(minimum):.3f}")
            if maximum is not None and presence_ratio > float(maximum):
                failures.append(f"presence ratio {presence_ratio:.3f} > {float(maximum):.3f}")
        latency = first_true_latency_ms(records, interval, sensor_id)
        max_onset_ms = rule.get("max_onset_ms")
        if max_onset_ms is not None:
            if latency is None:
                failures.append("no positive onset")
            elif latency > int(max_onset_ms):
                failures.append(f"onset {latency} ms > {int(max_onset_ms)} ms")
        sensors[sensor_id] = {
            "sample_count": len(values),
            "presence_count": sum(values),
            "presence_ratio": presence_ratio,
            "first_true_latency_ms": latency,
            "status": "PASS" if not failures else "FAIL",
            "failures": failures,
        }

    return {
        "scenario_id": interval.scenario_id,
        "repetition": interval.repetition,
        "ground_truth": interval.ground_truth,
        "door_state": interval.door_state,
        "start_epoch_ms": interval.start_ms,
        "end_epoch_ms": interval.end_ms,
        "duration_ms": interval.end_ms - interval.start_ms,
        "sample_count": len(records),
        "note": interval.note,
        "sensors": sensors,
        "status": "PASS" if sensors and all(item["status"] == "PASS" for item in sensors.values()) else "FAIL",
    }


def summarize_results(interval_results: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    sensor_rollup: dict[str, dict[str, Any]] = {}
    for result in interval_results:
        for sensor_id, metrics in result.get("sensors", {}).items():
            entry = sensor_rollup.setdefault(sensor_id, {
                "intervals": 0,
                "passed": 0,
                "failed": 0,
                "presence_ratios": [],
                "onset_latencies_ms": [],
            })
            entry["intervals"] += 1
            if metrics["status"] == "PASS":
                entry["passed"] += 1
            else:
                entry["failed"] += 1
            ratio = metrics.get("presence_ratio")
            if isinstance(ratio, (int, float)):
                entry["presence_ratios"].append(float(ratio))
            latency = metrics.get("first_true_latency_ms")
            if isinstance(latency, int):
                entry["onset_latencies_ms"].append(latency)

    for entry in sensor_rollup.values():
        ratios = entry.pop("presence_ratios")
        latencies = entry.pop("onset_latencies_ms")
        entry["mean_presence_ratio"] = statistics.fmean(ratios) if ratios else None
        entry["median_onset_latency_ms"] = statistics.median(latencies) if latencies else None
        entry["status"] = "PASS" if entry["failed"] == 0 and entry["intervals"] else "FAIL"

    return {
        "intervals": len(interval_results),
        "passed": sum(1 for item in interval_results if item["status"] == "PASS"),
        "failed": sum(1 for item in interval_results if item["status"] != "PASS"),
        "sensors": sensor_rollup,
        "status": "PASS" if interval_results and all(item["status"] == "PASS" for item in interval_results) else "FAIL",
    }


def analyze_run(run_dir: Path, plan_path: Path) -> dict[str, Any]:
    plan = require_valid_plan(plan_path)
    records = list(iter_jsonl(run_dir / "records.jsonl"))
    markers = list(iter_jsonl(run_dir / "marks.jsonl"))
    intervals, warnings = build_intervals(markers, plan)
    if not intervals:
        warnings.append("No complete start/end scenario interval exists")
    scenarios = scenario_index(plan)
    interval_results = [
        evaluate_interval(interval, records_in_interval(records, interval), scenarios[interval.scenario_id])
        for interval in intervals
    ]
    return {
        "schema_version": SCHEMA_VERSION,
        "issue": "IHAP-46",
        "run_id": run_dir.name,
        "generated_at": isoformat_utc(),
        "decision_boundary": "laboratory evidence only; no sensor decision or production contract",
        "plan": str(plan_path),
        "record_count": len(records),
        "marker_count": len(markers),
        "warnings": warnings,
        "summary": summarize_results(interval_results),
        "intervals": interval_results,
    }


def json_for_script(payload: Any) -> str:
    return json.dumps(payload, separators=(",", ":")).replace("</", "<\\/")


def render_report(results: Mapping[str, Any], output_path: Path) -> None:
    summary = results["summary"]
    intervals = results["intervals"]
    warning_items = "".join(f"<li>{html.escape(str(item))}</li>" for item in results["warnings"])
    rows: list[str] = []
    for interval in intervals:
        for sensor_id, metrics in interval["sensors"].items():
            ratio = metrics.get("presence_ratio")
            ratio_text = "—" if ratio is None else f"{ratio:.3f}"
            latency = metrics.get("first_true_latency_ms")
            rows.append(
                "<tr>"
                f"<td>{html.escape(interval['scenario_id'])}</td>"
                f"<td>{interval['repetition']}</td>"
                f"<td>{html.escape(sensor_id)}</td>"
                f"<td>{html.escape(interval['ground_truth'])}</td>"
                f"<td>{metrics['sample_count']}</td>"
                f"<td>{ratio_text}</td>"
                f"<td>{'—' if latency is None else latency}</td>"
                f"<td><span class='status {metrics['status'].lower()}'>{metrics['status']}</span></td>"
                f"<td>{html.escape('; '.join(metrics['failures']))}</td>"
                "</tr>"
            )

    report = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>IHAP-46 Presence Sensor Evidence — {html.escape(str(results['run_id']))}</title>
<style>
:root {{ color-scheme: light dark; font-family: Inter, system-ui, sans-serif; }}
body {{ margin: 0; background: #111827; color: #e5e7eb; }}
main {{ max-width: 1200px; margin: auto; padding: 28px; }}
h1,h2 {{ margin-bottom: .4rem; }}
.muted {{ color: #9ca3af; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:12px; margin:20px 0; }}
.card {{ background:#1f2937; border:1px solid #374151; border-radius:12px; padding:16px; }}
.value {{ font-size:1.8rem; font-weight:700; }}
table {{ width:100%; border-collapse:collapse; background:#1f2937; }}
th,td {{ padding:9px; border-bottom:1px solid #374151; text-align:left; vertical-align:top; }}
th {{ position:sticky; top:0; background:#111827; }}
.status {{ font-weight:700; }} .pass {{ color:#34d399; }} .fail {{ color:#f87171; }}
.controls {{ display:flex; gap:12px; flex-wrap:wrap; margin:14px 0; }}
select,input {{ padding:8px; border-radius:8px; border:1px solid #4b5563; background:#111827; color:inherit; }}
canvas {{ width:100%; height:260px; background:#fff; border-radius:10px; }}
code {{ background:#111827; padding:.15rem .35rem; border-radius:4px; }}
</style>
</head>
<body><main>
<h1>IHAP-46 Presence Sensor Evidence</h1>
<p class="muted">Run <code>{html.escape(str(results['run_id']))}</code> — generated {html.escape(str(results['generated_at']))}. Laboratory evidence only: no sensor acceptance, production event contract, alarm-grade or security claim.</p>
<div class="grid">
<div class="card"><div class="muted">Overall</div><div class="value {str(summary['status']).lower()}">{summary['status']}</div></div>
<div class="card"><div class="muted">Intervals</div><div class="value">{summary['intervals']}</div></div>
<div class="card"><div class="muted">Passed</div><div class="value pass">{summary['passed']}</div></div>
<div class="card"><div class="muted">Failed</div><div class="value fail">{summary['failed']}</div></div>
<div class="card"><div class="muted">Records</div><div class="value">{results['record_count']}</div></div>
</div>
<h2>Presence ratio by interval</h2><canvas id="chart" width="1100" height="260"></canvas>
<h2>Results</h2>
<div class="controls"><label>Sensor <select id="sensorFilter"><option value="">all</option></select></label><label>Scenario <input id="scenarioFilter" placeholder="filter"></label></div>
<div style="overflow:auto"><table id="resultsTable"><thead><tr><th>Scenario</th><th>Rep</th><th>Sensor</th><th>Ground truth</th><th>Samples</th><th>Presence ratio</th><th>Onset ms</th><th>Status</th><th>Failures</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
<h2>Warnings</h2><ul>{warning_items or '<li>None</li>'}</ul>
<script id="ihap46-data" type="application/json">{json_for_script(results)}</script>
<script>
const data=JSON.parse(document.getElementById('ihap46-data').textContent);
const sensorFilter=document.getElementById('sensorFilter');
const scenarioFilter=document.getElementById('scenarioFilter');
const rows=[...document.querySelectorAll('#resultsTable tbody tr')];
const sensors=[...new Set(rows.map(r=>r.children[2].textContent))].sort();
sensors.forEach(s=>sensorFilter.add(new Option(s,s)));
function applyFilter(){{const sf=sensorFilter.value;const q=scenarioFilter.value.toLowerCase();rows.forEach(r=>{{r.hidden=(sf&&r.children[2].textContent!==sf)||(q&&!r.children[0].textContent.toLowerCase().includes(q));}})}}
sensorFilter.addEventListener('change',applyFilter);scenarioFilter.addEventListener('input',applyFilter);
const canvas=document.getElementById('chart'),ctx=canvas.getContext('2d');ctx.fillStyle='#fff';ctx.fillRect(0,0,canvas.width,canvas.height);
const points=[];data.intervals.forEach((i,idx)=>Object.entries(i.sensors).forEach(([sensor,m])=>{{if(m.presence_ratio!==null)points.push({{idx,label:i.scenario_id+'#'+i.repetition,sensor,value:m.presence_ratio}})}}));
const palette=['#2563eb','#dc2626','#059669','#7c3aed'];const sensorNames=[...new Set(points.map(p=>p.sensor))];
ctx.strokeStyle='#d1d5db';ctx.fillStyle='#111827';ctx.font='12px sans-serif';for(let y=0;y<=4;y++){{const py=20+y*50;ctx.beginPath();ctx.moveTo(48,py);ctx.lineTo(canvas.width-20,py);ctx.stroke();ctx.fillText((1-y*.25).toFixed(2),8,py+4)}}
const groups=[...new Set(points.map(p=>p.label))];points.forEach(p=>{{const x=60+(groups.indexOf(p.label)+.5)*(canvas.width-90)/Math.max(groups.length,1);const y=220-p.value*200;ctx.fillStyle=palette[sensorNames.indexOf(p.sensor)%palette.length];ctx.beginPath();ctx.arc(x,y,5,0,Math.PI*2);ctx.fill();}});
sensorNames.forEach((s,i)=>{{ctx.fillStyle=palette[i%palette.length];ctx.fillRect(60+i*180,235,12,12);ctx.fillStyle='#111827';ctx.fillText(s,78+i*180,245)}});
</script>
</main></body></html>
"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")


def ensure_run_dir(runs_dir: Path, run_id: str, create: bool = False) -> Path:
    if not run_id or any(char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for char in run_id):
        raise HarnessError("run-id may contain only letters, digits, '-' and '_'")
    run_dir = runs_dir / run_id
    if create:
        run_dir.mkdir(parents=True, exist_ok=False)
    elif not run_dir.is_dir():
        raise HarnessError(f"Run does not exist: {run_dir}")
    return run_dir


def record_capture_event(run_dir: Path, event: str, **details: Any) -> None:
    append_jsonl(run_dir / "capture-events.jsonl", {"at": isoformat_utc(), "at_epoch_ms": epoch_ms(), "event": event, **details})


def decode_json_record(line: str) -> dict[str, Any] | None:
    stripped = line.strip()
    if not stripped.startswith("{"):
        return None
    try:
        value = json.loads(stripped)
    except json.JSONDecodeError:
        return None
    if not isinstance(value, dict) or "record_type" not in value:
        return None
    return value


def capture_serial(*, port: str, baud: int, run_dir: Path, reconnect_seconds: float, duration_seconds: float | None) -> None:
    try:
        import serial  # type: ignore
        from serial import SerialException  # type: ignore
    except ImportError as exc:
        raise HarnessError("pyserial is required: python -m pip install -r host/requirements.txt") from exc

    serial_log_path = run_dir / "serial.log"
    records_path = run_dir / "records.jsonl"
    deadline = time.monotonic() + duration_seconds if duration_seconds else None
    connection = None
    record_capture_event(run_dir, "capture_started", port=port, baud=baud)
    print(f"Capturing {port} at {baud} baud into {run_dir}")
    print(f"Use a second terminal with: python host/ihap46.py mark --run-id {run_dir.name} ...")

    try:
        with serial_log_path.open("a", encoding="utf-8", buffering=1) as serial_log:
            while deadline is None or time.monotonic() < deadline:
                if connection is None:
                    try:
                        connection = serial.Serial(port=port, baudrate=baud, timeout=1.0)
                        connection.reset_input_buffer()
                        record_capture_event(run_dir, "serial_connected", port=port)
                        print(f"Serial connected: {port}")
                    except (SerialException, OSError) as exc:
                        record_capture_event(run_dir, "serial_waiting", port=port, error=str(exc))
                        time.sleep(reconnect_seconds)
                        continue
                try:
                    raw = connection.readline()
                    if not raw:
                        continue
                    received_at = isoformat_utc()
                    received_ms = epoch_ms()
                    line = raw.decode("utf-8", errors="replace").rstrip("\r\n")
                    serial_log.write(line + "\n")
                    print(line)
                    source = decode_json_record(line)
                    if source is not None:
                        append_jsonl(records_path, {
                            "schema_version": SCHEMA_VERSION,
                            "received_at": received_at,
                            "received_at_epoch_ms": received_ms,
                            "source": source,
                        })
                except (SerialException, OSError) as exc:
                    record_capture_event(run_dir, "serial_disconnected", port=port, error=str(exc))
                    print(f"Serial disconnected; waiting for reset/re-enumeration: {exc}", file=sys.stderr)
                    try:
                        connection.close()
                    except Exception:
                        pass
                    connection = None
                    time.sleep(reconnect_seconds)
    except KeyboardInterrupt:
        print("\nCapture stopped by user")
    finally:
        if connection is not None:
            try:
                connection.close()
            except Exception:
                pass
        record_capture_event(run_dir, "capture_stopped", port=port)


def command_validate_plan(args: argparse.Namespace) -> None:
    plan = load_json(args.plan)
    if not isinstance(plan, dict):
        raise HarnessError("Plan root must be an object")
    errors = validate_plan(plan)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise HarnessError("Plan validation failed")
    print(f"Plan valid: {args.plan} ({len(plan['scenarios'])} scenarios)")


def command_list_scenarios(args: argparse.Namespace) -> None:
    plan = require_valid_plan(args.plan)
    for scenario in plan["scenarios"]:
        required = "required" if scenario.get("required", True) else "optional"
        print(f"{scenario['id']}: {scenario['title']} [{scenario['ground_truth']}, {scenario['duration_s']}s x {scenario['repetitions']}, {required}]")


def command_capture(args: argparse.Namespace) -> None:
    plan = require_valid_plan(args.plan)
    run_dir = ensure_run_dir(args.runs_dir, args.run_id, create=True)
    write_json(run_dir / "run.json", {
        "schema_version": SCHEMA_VERSION,
        "issue": "IHAP-46",
        "run_id": args.run_id,
        "created_at": isoformat_utc(),
        "port": args.port,
        "baud": args.baud,
        "plan_path": str(args.plan),
        "plan_snapshot": plan,
        "scope": "laboratory validation only",
    })
    capture_serial(port=args.port, baud=args.baud, run_dir=run_dir, reconnect_seconds=args.reconnect_seconds, duration_seconds=args.duration)


def command_preflight(args: argparse.Namespace) -> None:
    run_id = args.run_id or f"IHAP46-PREFLIGHT-{utc_now().strftime('%Y%m%d-%H%M%S')}"
    run_dir = ensure_run_dir(args.runs_dir, run_id, create=True)
    plan = require_valid_plan(args.plan)
    write_json(run_dir / "run.json", {
        "schema_version": SCHEMA_VERSION,
        "issue": "IHAP-46",
        "run_id": run_id,
        "created_at": isoformat_utc(),
        "port": args.port,
        "baud": args.baud,
        "plan_path": str(args.plan),
        "plan_snapshot": plan,
        "preflight": True,
    })
    capture_serial(port=args.port, baud=args.baud, run_dir=run_dir, reconnect_seconds=args.reconnect_seconds, duration_seconds=args.seconds)
    records = list(iter_jsonl(run_dir / "records.jsonl"))
    sources = [item.get("source", {}) for item in records]
    boot = any(isinstance(item, Mapping) and item.get("record_type") == "boot" for item in sources)
    samples = [item for item in sources if isinstance(item, Mapping) and item.get("record_type") == "sample"]
    valid_uart = any(bool(get_nested(item, ("ld2410c", "uart_frame_valid"))) for item in samples)
    result = {
        "boot_record": boot,
        "sample_records": len(samples),
        "valid_ld2410c_uart_frame": valid_uart,
        "status": "PASS" if boot and samples and valid_uart else "FAIL",
    }
    write_json(run_dir / "preflight.json", result)
    print(json.dumps(result, indent=2))
    if result["status"] != "PASS":
        raise HarnessError("Preflight failed; inspect serial.log and preflight.json")


def command_mark(args: argparse.Namespace) -> None:
    run_dir = ensure_run_dir(args.runs_dir, args.run_id)
    run_metadata = load_json(run_dir / "run.json")
    plan = run_metadata.get("plan_snapshot") if isinstance(run_metadata, dict) else None
    if not isinstance(plan, dict):
        plan = require_valid_plan(args.plan)
    scenarios = scenario_index(plan)
    if args.scenario not in scenarios:
        raise HarnessError(f"Unknown scenario: {args.scenario}")
    marker = {
        "schema_version": SCHEMA_VERSION,
        "record_type": "ground_truth_marker",
        "run_id": args.run_id,
        "at": isoformat_utc(),
        "at_epoch_ms": epoch_ms(),
        "scenario_id": args.scenario,
        "repetition": args.repetition,
        "phase": args.phase,
        "ground_truth": scenarios[args.scenario]["ground_truth"],
        "door_state": args.door or scenarios[args.scenario]["door_state"],
        "note": args.note or "",
    }
    append_jsonl(run_dir / "marks.jsonl", marker)
    print(json.dumps(marker, indent=2))


def command_report(args: argparse.Namespace) -> None:
    run_dir = ensure_run_dir(args.runs_dir, args.run_id)
    run_metadata = load_json(run_dir / "run.json")
    plan_path = args.plan
    if plan_path is None and isinstance(run_metadata, dict):
        candidate = run_metadata.get("plan_path")
        if isinstance(candidate, str):
            plan_path = Path(candidate)
    if plan_path is None:
        raise HarnessError("A plan is required")
    results = analyze_run(run_dir, plan_path)
    results_path = run_dir / "results.json"
    report_path = run_dir / "report.html"
    write_json(results_path, results)
    render_report(results, report_path)
    print(f"Results: {results_path}")
    print(f"Interactive report: {report_path}")
    print(f"Status: {results['summary']['status']}")


def command_selftest(args: argparse.Namespace) -> None:
    plan = require_valid_plan(args.plan)
    run_dir = args.output
    run_dir.mkdir(parents=True, exist_ok=True)
    write_json(run_dir / "run.json", {
        "schema_version": SCHEMA_VERSION,
        "issue": "IHAP-46",
        "run_id": run_dir.name,
        "created_at": isoformat_utc(),
        "plan_path": str(args.plan),
        "plan_snapshot": plan,
        "synthetic": True,
    })
    start = epoch_ms()
    selected = plan["scenarios"][:2]
    for index, scenario in enumerate(selected):
        interval_start = start + index * 12_000
        interval_end = interval_start + 10_000
        append_jsonl(run_dir / "marks.jsonl", {
            "record_type": "ground_truth_marker",
            "at_epoch_ms": interval_start,
            "scenario_id": scenario["id"],
            "repetition": 1,
            "phase": "start",
            "note": "synthetic selftest",
        })
        for offset in range(0, 10_000, 500):
            expected_present = scenario["ground_truth"] not in {"empty", "adjacent_activity"}
            append_jsonl(run_dir / "records.jsonl", {
                "received_at_epoch_ms": interval_start + offset,
                "received_at": isoformat_utc(),
                "source": {
                    "record_type": "sample",
                    "schema_version": SCHEMA_VERSION,
                    "seq": index * 100 + offset // 500,
                    "uptime_ms": offset,
                    "ld2410c": {"uart_frame_valid": True, "uart_presence": expected_present, "out": expected_present},
                    "pir": {"enabled": True, "out": expected_present},
                },
            })
        append_jsonl(run_dir / "marks.jsonl", {
            "record_type": "ground_truth_marker",
            "at_epoch_ms": interval_end,
            "scenario_id": scenario["id"],
            "repetition": 1,
            "phase": "end",
        })
    results = analyze_run(run_dir, args.plan)
    write_json(run_dir / "results.json", results)
    render_report(results, run_dir / "report.html")
    print(f"Selftest generated: {run_dir}")
    if results["summary"]["failed"]:
        raise HarnessError("Synthetic selftest produced failures")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.set_defaults(func=None)
    subparsers = parser.add_subparsers(dest="command")

    validate = subparsers.add_parser("validate-plan", help="validate test-plan JSON")
    validate.add_argument("--plan", type=Path, default=Path("config/test-plan.json"))
    validate.set_defaults(func=command_validate_plan)

    scenarios = subparsers.add_parser("list-scenarios", help="show scenario matrix")
    scenarios.add_argument("--plan", type=Path, default=Path("config/test-plan.json"))
    scenarios.set_defaults(func=command_list_scenarios)

    preflight = subparsers.add_parser("preflight", help="short capture and boot/UART check")
    preflight.add_argument("--port", required=True)
    preflight.add_argument("--baud", type=int, default=DEFAULT_BAUD)
    preflight.add_argument("--seconds", type=float, default=20)
    preflight.add_argument("--run-id")
    preflight.add_argument("--plan", type=Path, default=Path("config/test-plan.json"))
    preflight.add_argument("--runs-dir", type=Path, default=DEFAULT_RUNS_DIR)
    preflight.add_argument("--reconnect-seconds", type=float, default=1.0)
    preflight.set_defaults(func=command_preflight)

    capture = subparsers.add_parser("capture", help="capture serial evidence with auto-reconnect")
    capture.add_argument("--port", required=True)
    capture.add_argument("--run-id", required=True)
    capture.add_argument("--plan", type=Path, default=Path("config/test-plan.json"))
    capture.add_argument("--baud", type=int, default=DEFAULT_BAUD)
    capture.add_argument("--duration", type=float)
    capture.add_argument("--runs-dir", type=Path, default=DEFAULT_RUNS_DIR)
    capture.add_argument("--reconnect-seconds", type=float, default=1.0)
    capture.set_defaults(func=command_capture)

    mark = subparsers.add_parser("mark", help="append a ground-truth scenario marker")
    mark.add_argument("--run-id", required=True)
    mark.add_argument("--scenario", required=True)
    mark.add_argument("--phase", choices=sorted(PHASE_VALUES), required=True)
    mark.add_argument("--repetition", type=int, default=1)
    mark.add_argument("--door", choices=sorted(DOOR_VALUES))
    mark.add_argument("--note")
    mark.add_argument("--plan", type=Path, default=Path("config/test-plan.json"))
    mark.add_argument("--runs-dir", type=Path, default=DEFAULT_RUNS_DIR)
    mark.set_defaults(func=command_mark)

    report = subparsers.add_parser("report", help="produce results.json and report.html")
    report.add_argument("--run-id", required=True)
    report.add_argument("--plan", type=Path)
    report.add_argument("--runs-dir", type=Path, default=DEFAULT_RUNS_DIR)
    report.set_defaults(func=command_report)

    selftest = subparsers.add_parser("selftest", help="generate and evaluate synthetic evidence")
    selftest.add_argument("--plan", type=Path, default=Path("config/test-plan.json"))
    selftest.add_argument("--output", type=Path, default=Path("runs/IHAP46-SELFTEST"))
    selftest.set_defaults(func=command_selftest)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.func is None:
        parser.print_help()
        return 2
    try:
        args.func(args)
    except HarnessError as exc:
        print(f"IHAP-46 ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
