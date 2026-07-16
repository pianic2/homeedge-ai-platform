#!/usr/bin/env python3
"""Generate self-contained aggregate-only HTML evidence from an IHAP-45 public summary."""

from __future__ import annotations

import argparse
import html
import json
import math
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence


FORBIDDEN_KEYS = {
    "batch_id",
    "host_timestamp_utc",
    "uptime_ms",
    "serial_port",
    "serial_port_history",
    "pressure",
    "pressure_pa",
    "pressure_hpa",
}
SENSOR_ORDER = ["DHT11-OWNED-01", "DHT22-OWNED-01", "BME280-OWNED-01"]
SENSOR_COLORS = {
    "DHT11-OWNED-01": "#1473e6",
    "DHT22-OWNED-01": "#e24a8d",
    "BME280-OWNED-01": "#23a36d",
}
PHASE_ORDER = [
    "baseline",
    "humidity_high_plateau",
    "humidity_low_plateau",
    "temperature_high_plateau",
    "temperature_low_plateau",
    "final_recovery",
]


class HtmlPublicationError(RuntimeError):
    """Raised when a summary is not safe or complete enough for HTML publication."""


def load_summary(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise HtmlPublicationError(f"missing summary: {path}") from exc
    except json.JSONDecodeError as exc:
        raise HtmlPublicationError(f"invalid JSON summary: {exc}") from exc
    if not isinstance(value, dict):
        raise HtmlPublicationError("summary root must be a JSON object")
    if value.get("evidence_type") != "environmental_comparison_summary":
        raise HtmlPublicationError("expected environmental_comparison_summary evidence")
    if value.get("publication_schema_version") != "1.0.0":
        raise HtmlPublicationError("unsupported publication schema version")
    findings = find_forbidden_keys(value)
    if findings:
        raise HtmlPublicationError(f"summary contains forbidden raw or pressure keys: {findings}")
    return value


def find_forbidden_keys(value: Any, path: str = "$") -> list[str]:
    findings: list[str] = []
    if isinstance(value, Mapping):
        for key, nested in value.items():
            key_text = str(key)
            if key_text in FORBIDDEN_KEYS:
                findings.append(f"{path}.{key_text}")
            findings.extend(find_forbidden_keys(nested, f"{path}.{key_text}"))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            findings.extend(find_forbidden_keys(nested, f"{path}[{index}]"))
    return findings


def esc(value: Any) -> str:
    return html.escape("n/a" if value is None else str(value), quote=True)


def number(value: Any, digits: int = 2) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, int):
        return f"{value:,}"
    if isinstance(value, float):
        if not math.isfinite(value):
            return "n/a"
        return f"{value:,.{digits}f}"
    return esc(value)


def metric(metrics: Mapping[str, Any] | None, key: str) -> Any:
    return None if metrics is None else metrics.get(key)


def sensor_metrics(summary: Mapping[str, Any]) -> Mapping[str, Any]:
    return ((summary.get("results") or {}).get("per_sensor") or {})


def phase_duration_rows(summary: Mapping[str, Any]) -> str:
    durations = ((summary.get("validation") or {}).get("phase_durations_seconds") or {})
    entries = [(str(name), float(seconds)) for name, seconds in durations.items() if name != "unclassified"]
    maximum = max((seconds for _, seconds in entries), default=1.0)
    rows: list[str] = []
    for name, seconds in entries:
        width = max(1.0, seconds / maximum * 100.0)
        rows.append(
            f'<div class="phase-row"><code>{esc(name)}</code><div class="bar-track">'
            f'<div class="bar" style="width:{width:.2f}%"></div></div><strong>{seconds / 60.0:.1f} min</strong></div>'
        )
    return "\n".join(rows)


def aggregate_sensor_rows(summary: Mapping[str, Any]) -> str:
    rows: list[str] = []
    metrics_by_sensor = sensor_metrics(summary)
    for sensor_id in SENSOR_ORDER:
        metrics = metrics_by_sensor.get(sensor_id) or {}
        temp = metrics.get("temperature_c") or {}
        humidity = metrics.get("humidity_percent") or {}
        latency = metrics.get("read_duration_us") or {}
        errors = metrics.get("error_counts") or {}
        rows.append(
            "<tr>"
            f"<td><span class=\"sensor-dot\" style=\"background:{SENSOR_COLORS[sensor_id]}\"></span><code>{esc(sensor_id)}</code></td>"
            f"<td>{number(metrics.get('valid_records'), 0)} / {number(metrics.get('records'), 0)}</td>"
            f"<td>{number(metrics.get('valid_percent'))}%</td>"
            f"<td>{number(temp.get('mean'), 3)}</td>"
            f"<td>{number(temp.get('stddev'), 3)}</td>"
            f"<td>{number(humidity.get('mean'), 3)}</td>"
            f"<td>{number(humidity.get('stddev'), 3)}</td>"
            f"<td>{number(latency.get('median'), 1)}</td>"
            f"<td><code>{esc(json.dumps(errors, sort_keys=True))}</code></td>"
            "</tr>"
        )
    return "\n".join(rows)


def polyline_points(values: Sequence[float | None], width: int, height: int, padding: int = 24) -> str:
    finite = [value for value in values if value is not None and math.isfinite(value)]
    if not finite:
        return ""
    lower = min(finite)
    upper = max(finite)
    span = upper - lower or 1.0
    denominator = max(1, len(values) - 1)
    points: list[str] = []
    for index, value in enumerate(values):
        if value is None or not math.isfinite(value):
            continue
        x = padding + index * (width - 2 * padding) / denominator
        y = height - padding - (value - lower) * (height - 2 * padding) / span
        points.append(f"{x:.1f},{y:.1f}")
    return " ".join(points)


def aggregate_svg(summary: Mapping[str, Any], field: str, title: str, unit: str) -> str:
    width, height = 920, 310
    metrics_by_sensor = sensor_metrics(summary)
    all_values: list[float] = []
    series: dict[str, list[float | None]] = {}
    for sensor_id in SENSOR_ORDER:
        per_phase = (metrics_by_sensor.get(sensor_id) or {}).get("per_phase") or {}
        values: list[float | None] = []
        for phase in PHASE_ORDER:
            raw = ((per_phase.get(phase) or {}).get(field) or {}).get("mean")
            value = float(raw) if isinstance(raw, (int, float)) and math.isfinite(float(raw)) else None
            values.append(value)
            if value is not None:
                all_values.append(value)
        series[sensor_id] = values
    if not all_values:
        return f"<section class=\"panel\"><h2>{esc(title)}</h2><p>No aggregate values available.</p></section>"
    lower, upper = min(all_values), max(all_values)
    lines: list[str] = []
    dots: list[str] = []
    labels: list[str] = []
    for sensor_id, values in series.items():
        points = polyline_points(values, width, height)
        if points:
            lines.append(
                f'<polyline points="{points}" fill="none" stroke="{SENSOR_COLORS[sensor_id]}" '
                'stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/>'
            )
        denominator = max(1, len(values) - 1)
        span = upper - lower or 1.0
        for index, value in enumerate(values):
            if value is None:
                continue
            x = 24 + index * (width - 48) / denominator
            y = height - 24 - (value - lower) * (height - 48) / span
            dots.append(
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{SENSOR_COLORS[sensor_id]}">'
                f'<title>{esc(sensor_id)} — {esc(PHASE_ORDER[index])}: {value:.3f} {esc(unit)}</title></circle>'
            )
    denominator = max(1, len(PHASE_ORDER) - 1)
    for index, phase in enumerate(PHASE_ORDER):
        x = 24 + index * (width - 48) / denominator
        short = phase.replace("temperature_", "temp_").replace("humidity_", "rh_").replace("_plateau", "")
        labels.append(f'<text x="{x:.1f}" y="302" text-anchor="middle" class="axis-label">{esc(short)}</text>')
    legend = "".join(
        f'<span><i style="background:{SENSOR_COLORS[sensor]}"></i>{esc(sensor)}</span>' for sensor in SENSOR_ORDER
    )
    return f"""
<section class="panel">
  <div class="chart-heading"><div><h2>{esc(title)}</h2><p>Per-phase means; aggregate values only.</p></div><div class="legend">{legend}</div></div>
  <div class="chart-wrap"><svg viewBox="0 0 {width} {height}" role="img" aria-label="{esc(title)}">
    <line x1="24" y1="24" x2="24" y2="286" class="grid-line"/>
    <line x1="24" y1="286" x2="896" y2="286" class="grid-line"/>
    {''.join(lines)}{''.join(dots)}{''.join(labels)}
  </svg></div>
  <p class="range">Observed aggregate range: {lower:.3f}–{upper:.3f} {esc(unit)}</p>
</section>
"""


def pairwise_rows(summary: Mapping[str, Any]) -> str:
    rows: list[str] = []
    pairs = ((summary.get("results") or {}).get("pairwise") or {})
    for pair, metrics in pairs.items():
        temp = metrics.get("temperature_delta_c") or {}
        humidity = metrics.get("humidity_delta_percent") or {}
        rows.append(
            "<tr>"
            f"<td><code>{esc(pair)}</code></td>"
            f"<td>{number(metrics.get('matched_batches'), 0)}</td>"
            f"<td>{number(temp.get('mean'), 3)}</td>"
            f"<td>{number(temp.get('median'), 3)}</td>"
            f"<td>{number(humidity.get('mean'), 3)}</td>"
            f"<td>{number(humidity.get('median'), 3)}</td>"
            "</tr>"
        )
    return "\n".join(rows) or '<tr><td colspan="6">No pairwise aggregates available.</td></tr>'


def render(summary: Mapping[str, Any]) -> str:
    validation = summary.get("validation") or {}
    probe = summary.get("qualified_bme280") or {}
    limitations = summary.get("limitations") or []
    status = str(summary.get("status", "unknown")).upper()
    status_class = "pass" if status == "PASSED" else "fail"
    scope_warning = (
        "Relative comparison only. No independent reference was recorded, so absolute accuracy remains unvalidated."
        if summary.get("comparison_scope") == "relative_only"
        else "Independent reference aggregates are available; review the companion JSON for error metrics."
    )
    limitations_html = "".join(f"<li>{esc(item)}</li>" for item in limitations)
    errors = validation.get("errors") or []
    warnings = validation.get("warnings") or []
    messages = "".join(f'<li class="error">{esc(item)}</li>' for item in errors) + "".join(
        f'<li class="warning">{esc(item)}</li>' for item in warnings
    )
    if not messages:
        messages = "<li>No validation errors or warnings.</li>"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>IHAP-45 Aggregate Evidence — {esc(summary.get('run_id'))}</title>
<style>
:root {{ color-scheme: light dark; --bg:#07111f; --panel:#101e31; --text:#eef6ff; --muted:#a9bed3; --line:#2b4664; --accent:#64d8ff; --ok:#3ddc97; --warn:#ffc857; --bad:#ff6b6b; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; font-family:Inter,ui-sans-serif,system-ui,sans-serif; background:radial-gradient(circle at top right,#19375a 0,#07111f 42%); color:var(--text); }}
main {{ max-width:1320px; margin:auto; padding:32px 22px 72px; }}
.hero,.panel,.card {{ background:rgba(16,30,49,.94); border:1px solid var(--line); border-radius:20px; box-shadow:0 18px 50px rgba(0,0,0,.24); }}
.hero {{ padding:32px; display:grid; gap:24px; grid-template-columns:1.5fr .8fr; align-items:center; }}
h1 {{ margin:.2rem 0 .7rem; font-size:clamp(2rem,5vw,4.8rem); line-height:.95; }}
h2 {{ margin:0 0 8px; }}
p {{ color:var(--muted); line-height:1.55; }}
.eyebrow {{ text-transform:uppercase; letter-spacing:.14em; color:var(--accent); font-weight:800; font-size:.78rem; }}
.status {{ justify-self:end; padding:18px 24px; border-radius:999px; font-weight:900; letter-spacing:.1em; font-size:1.35rem; }}
.status.pass {{ color:#042317; background:var(--ok); }} .status.fail {{ color:white; background:var(--bad); }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:16px; margin:20px 0; }}
.card {{ padding:20px; }} .card strong {{ display:block; font-size:2rem; margin-top:5px; }}
.panel {{ padding:24px; margin-top:20px; overflow:hidden; }}
.notice {{ border-left:6px solid var(--warn); }}
table {{ width:100%; border-collapse:collapse; min-width:860px; }} th,td {{ padding:12px 10px; border-bottom:1px solid var(--line); text-align:right; }} th:first-child,td:first-child {{ text-align:left; }}
.table-wrap,.chart-wrap {{ overflow:auto; }}
.sensor-dot {{ display:inline-block; width:10px; height:10px; border-radius:50%; margin-right:8px; }}
.phase-row {{ display:grid; grid-template-columns:minmax(210px,1fr) 4fr 90px; gap:12px; align-items:center; margin:12px 0; }}
.bar-track {{ height:14px; background:#07111f; border-radius:999px; overflow:hidden; }} .bar {{ height:100%; background:linear-gradient(90deg,#64d8ff,#3ddc97); border-radius:999px; }}
.chart-heading {{ display:flex; justify-content:space-between; gap:20px; align-items:flex-start; flex-wrap:wrap; }}
.legend {{ display:flex; gap:12px; flex-wrap:wrap; font-size:.78rem; }} .legend span {{ display:flex; align-items:center; gap:6px; }} .legend i {{ width:12px; height:12px; border-radius:50%; }}
svg {{ width:100%; min-width:760px; height:auto; }} .grid-line {{ stroke:var(--line); stroke-width:1; }} .axis-label {{ fill:var(--muted); font-size:12px; }}
.range,footer {{ font-size:.85rem; }} ul {{ color:var(--muted); line-height:1.6; }} .warning {{ color:var(--warn); }} .error {{ color:var(--bad); }}
code {{ font-family:ui-monospace,SFMono-Regular,Menlo,monospace; }}
footer {{ margin-top:28px; color:var(--muted); text-align:center; }}
@media(max-width:760px) {{ .hero {{ grid-template-columns:1fr; }} .status {{ justify-self:start; }} .phase-row {{ grid-template-columns:1fr; }} }}
</style>
</head>
<body><main>
<section class="hero">
  <div><div class="eyebrow">IHAP-45 · Aggregate evidence</div><h1>Environmental sensor comparison</h1>
  <p>Run <code>{esc(summary.get('run_id'))}</code> · Plan <code>{esc(summary.get('plan_id'))}</code> · temperature and relative humidity only</p></div>
  <div class="status {status_class}">{esc(status)}</div>
</section>
<section class="grid">
  <article class="card"><span>Sample records</span><strong>{number(validation.get('sample_records'),0)}</strong></article>
  <article class="card"><span>Boot records</span><strong>{number(validation.get('boot_records'),0)}</strong></article>
  <article class="card"><span>BME280 chip</span><strong>{esc(probe.get('chip_id'))}</strong></article>
  <article class="card"><span>BME280 address</span><strong>{esc(probe.get('i2c_address'))}</strong></article>
</section>
<section class="panel notice"><h2>Evidence boundary</h2><p>{esc(scope_warning)}</p><p>This page contains aggregate statistics only. It embeds no serial log, timestamped observation, batch record, workstation path or per-sample series.</p></section>
<section class="panel"><h2>Validation messages</h2><ul>{messages}</ul></section>
<section class="panel"><h2>Phase coverage</h2>{phase_duration_rows(summary)}</section>
{aggregate_svg(summary, 'temperature_c', 'Temperature by stable phase', '°C')}
{aggregate_svg(summary, 'humidity_percent', 'Relative humidity by stable phase', '% RH')}
<section class="panel"><h2>Aggregate sensor results</h2><div class="table-wrap"><table><thead><tr><th>Sensor</th><th>Valid</th><th>Valid %</th><th>Mean °C</th><th>SD °C</th><th>Mean RH %</th><th>SD RH</th><th>Median µs</th><th>Errors</th></tr></thead><tbody>{aggregate_sensor_rows(summary)}</tbody></table></div></section>
<section class="panel"><h2>Pairwise aggregate differences</h2><div class="table-wrap"><table><thead><tr><th>Comparison</th><th>Matched batches</th><th>Mean Δ °C</th><th>Median Δ °C</th><th>Mean Δ RH</th><th>Median Δ RH</th></tr></thead><tbody>{pairwise_rows(summary)}</tbody></table></div></section>
<section class="panel"><h2>Limitations</h2><ul>{limitations_html}</ul></section>
<footer>Generated from <code>{esc(summary.get('publication_schema_version'))}</code> allow-listed aggregate evidence. Review the companion JSON and Markdown summaries for machine-readable provenance.</footer>
</main></body></html>"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary", required=True, help="path to environmental-*.summary.json")
    parser.add_argument("--output", help="output HTML path; defaults beside the summary")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    summary_path = Path(args.summary)
    output_path = Path(args.output) if args.output else summary_path.with_suffix(".html")
    try:
        summary = load_summary(summary_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(render(summary), encoding="utf-8")
    except (HtmlPublicationError, OSError, ValueError, TypeError) as exc:
        print(f"IHAP-45 HTML PUBLICATION ERROR: {exc}", file=sys.stderr)
        return 2
    print(f"Aggregate-only HTML evidence: {output_path}")
    print("No raw serial or per-sample telemetry was copied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
