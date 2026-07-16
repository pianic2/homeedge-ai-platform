#!/usr/bin/env python3
"""Build a sanitized summary and standalone HTML report for an IHAP-47 session."""

from __future__ import annotations

import argparse
import html
import json
import math
import statistics
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    if not path.exists():
        return records

    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
        if not isinstance(value, dict):
            raise ValueError(f"{path}:{line_number}: expected JSON object")
        records.append(value)
    return records


def numeric(values: Iterable[Any]) -> list[float]:
    result: list[float] = []
    for value in values:
        if isinstance(value, bool):
            continue
        if isinstance(value, (int, float)) and math.isfinite(float(value)):
            result.append(float(value))
    return result


def stats(values: list[float]) -> dict[str, float | int | None]:
    if not values:
        return {"count": 0, "min": None, "median": None, "max": None}
    return {
        "count": len(values),
        "min": min(values),
        "median": statistics.median(values),
        "max": max(values),
    }


def capture_summaries(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None

    for record in records:
        record_type = record.get("record_type")

        if record_type == "capture_started":
            if current is not None:
                current["incomplete"] = True
                summaries.append(current)
            current = {
                "test_id": str(record.get("test_id", "UNSET")),
                "specimen_id": str(record.get("specimen_id", "UNSET")),
                "initial_level": record.get("initial_level"),
                "sample_period_us": record.get("sample_period_us"),
                "transitions": [],
                "incomplete": True,
            }
            continue

        if record_type == "raw_transition":
            if current is not None:
                current["transitions"].append(record)
            continue

        if record_type == "capture_ended":
            if current is None:
                current = {
                    "test_id": str(record.get("test_id", "UNSET")),
                    "specimen_id": str(record.get("specimen_id", "UNSET")),
                    "transitions": [],
                }

            edge_records = sorted(
                current.get("transitions", []), key=lambda item: item.get("sequence", 0)
            )
            offsets = numeric(item.get("offset_us") for item in edge_records)
            bounce_span_us = None
            if len(offsets) >= 2:
                bounce_span_us = max(offsets) - min(offsets)
            elif len(offsets) == 1:
                bounce_span_us = 0.0

            current.update(
                {
                    "test_id": str(record.get("test_id", current.get("test_id", "UNSET"))),
                    "specimen_id": str(
                        record.get("specimen_id", current.get("specimen_id", "UNSET"))
                    ),
                    "duration_us": record.get("duration_us"),
                    "sample_period_us": record.get(
                        "sample_period_us", current.get("sample_period_us")
                    ),
                    "initial_level": record.get(
                        "initial_level", current.get("initial_level")
                    ),
                    "final_level": record.get("final_level"),
                    "transition_count": record.get(
                        "transition_count", len(edge_records)
                    ),
                    "bounce_span_us": bounce_span_us,
                    "buffer_overflow": bool(record.get("buffer_overflow", False)),
                    "transitions": edge_records,
                    "incomplete": False,
                }
            )
            summaries.append(current)
            current = None

    if current is not None:
        current["incomplete"] = True
        current.setdefault("duration_us", None)
        current.setdefault("final_level", None)
        current.setdefault("transition_count", len(current.get("transitions", [])))
        current.setdefault("bounce_span_us", None)
        current.setdefault("buffer_overflow", False)
        summaries.append(current)

    return summaries


def observation_summary(observations: list[dict[str, Any]]) -> dict[str, Any]:
    gap_groups: dict[str, list[float]] = defaultdict(list)
    continuity: list[dict[str, Any]] = []
    cycle_results: list[dict[str, Any]] = []

    for observation in observations:
        test = observation.get("test")
        if test == "gap":
            direction = str(observation.get("direction", "unspecified"))
            values = numeric([observation.get("distance_mm")])
            gap_groups[direction].extend(values)
        elif test == "continuity":
            continuity.append(observation)
        elif test == "cycle":
            cycle_results.append(observation)

    return {
        "continuity": continuity,
        "gap_mm": {name: stats(values) for name, values in sorted(gap_groups.items())},
        "cycle_observations": cycle_results,
    }


def build_summary(
    session_dir: Path,
    records: list[dict[str, Any]],
    observations: list[dict[str, Any]],
) -> dict[str, Any]:
    captures = capture_summaries(records)
    overflow_count = sum(1 for item in captures if item["buffer_overflow"])
    bounce_values = numeric(item.get("bounce_span_us") for item in captures)

    return {
        "schema_version": "1.0.0",
        "issue": "IHAP-47",
        "generated_at_utc": utc_now(),
        "source_session": session_dir.name,
        "evidence_class": "observed-owned-specimen-pending-review",
        "physical_results_validated": False,
        "raw_logs_included": False,
        "records_count": len(records),
        "operator_observations_count": len(observations),
        "capture_count": len(captures),
        "captures_with_buffer_overflow": overflow_count,
        "bounce_span_us": stats(bounce_values),
        "observations": observation_summary(observations),
        "captures": captures,
        "limitations": [
            "The report is generated from a test harness, not production firmware.",
            "Firmware timestamps are not independent oscilloscope-grade measurements.",
            "Open circuit does not distinguish door open from disconnected wire or failed-open contact.",
            "Results apply only to the recorded specimens, setup and session.",
            "Project Owner review is required before any ADR status change.",
        ],
    }


def format_value(value: Any) -> str:
    if value is None:
        return "—"
    if isinstance(value, float):
        return f"{value:.3f}".rstrip("0").rstrip(".")
    return str(value)


def render_table(headers: list[str], rows: list[list[Any]]) -> str:
    head = "".join(f"<th>{html.escape(header)}</th>" for header in headers)
    body = "".join(
        "<tr>" + "".join(f"<td>{html.escape(format_value(cell))}</td>" for cell in row) + "</tr>"
        for row in rows
    )
    return f"<div class='table-wrap'><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>"


def build_html(summary: dict[str, Any]) -> str:
    capture_rows = [
        [
            item["test_id"],
            item["specimen_id"],
            item["initial_level"],
            item["final_level"],
            item["transition_count"],
            item["bounce_span_us"],
            "YES" if item["buffer_overflow"] else "NO",
        ]
        for item in summary["captures"]
    ]

    continuity_rows = [
        [
            item.get("specimen_id"),
            item.get("magnet_position"),
            item.get("circuit"),
            item.get("iteration"),
            item.get("notes"),
        ]
        for item in summary["observations"]["continuity"]
    ]

    gap_rows = [
        [name, values["count"], values["min"], values["median"], values["max"]]
        for name, values in summary["observations"]["gap_mm"].items()
    ]

    embedded = json.dumps(summary, separators=(",", ":")).replace("</", "<\\/")
    limitations = "".join(f"<li>{html.escape(item)}</li>" for item in summary["limitations"])

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>IHAP-47 Door State Sensor Test Report</title>
<style>
:root {{ color-scheme: light dark; --bg:#f4f6fb; --surface:#ffffff; --text:#172033; --muted:#5f6b7a; --line:#d9e0ea; --accent:#284b9b; --warn:#a85a00; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#11151c; --surface:#1a202b; --text:#edf2f8; --muted:#aab4c3; --line:#303a49; --accent:#9bb8ff; --warn:#ffbd73; }} }}
* {{ box-sizing:border-box; }} body {{ margin:0; font:15px/1.55 system-ui,sans-serif; background:var(--bg); color:var(--text); }}
main {{ width:min(1180px,calc(100% - 32px)); margin:32px auto 64px; }}
h1,h2 {{ line-height:1.2; }} .lede {{ color:var(--muted); max-width:80ch; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:12px; margin:24px 0; }}
.card,section {{ background:var(--surface); border:1px solid var(--line); border-radius:14px; padding:18px; }}
.card strong {{ display:block; font-size:28px; }} .card span {{ color:var(--muted); }}
section {{ margin-top:18px; }} .warning {{ border-left:5px solid var(--warn); }}
.table-wrap {{ overflow:auto; }} table {{ border-collapse:collapse; width:100%; }} th,td {{ border-bottom:1px solid var(--line); padding:9px; text-align:left; white-space:nowrap; }} th {{ color:var(--muted); }}
canvas {{ width:100%; height:280px; border:1px solid var(--line); border-radius:10px; }}
code {{ background:color-mix(in srgb,var(--surface),var(--line) 35%); padding:2px 5px; border-radius:5px; }}
</style>
</head>
<body><main>
<h1>IHAP-47 — Door State Sensor Test Report</h1>
<p class="lede">Generated from local structured records. Status remains pending Project Owner review. This report is telemetry evidence only and is not alarm, access-control, intrusion-detection, antifurto, tamper or reliability certification.</p>
<div class="grid">
<div class="card"><strong>{summary['capture_count']}</strong><span>bounded captures</span></div>
<div class="card"><strong>{summary['records_count']}</strong><span>firmware records</span></div>
<div class="card"><strong>{summary['operator_observations_count']}</strong><span>operator observations</span></div>
<div class="card"><strong>{summary['captures_with_buffer_overflow']}</strong><span>buffer overflows</span></div>
</div>
<section class="warning"><h2>Decision boundary</h2><p><strong>Physical results validated:</strong> {str(summary['physical_results_validated']).lower()}.</p><p>Open electrical circuit remains indistinguishable from several physical and wiring failure modes.</p></section>
<section><h2>Capture summary</h2>{render_table(['Test','Specimen','Initial','Final','Transitions','Observed span (us)','Overflow'], capture_rows)}</section>
<section><h2>Transition spans</h2><canvas id="bounce-chart" width="1000" height="280"></canvas></section>
<section><h2>Passive continuity observations</h2>{render_table(['Specimen','Magnet position','Circuit','Iteration','Notes'], continuity_rows)}</section>
<section><h2>Gap observations</h2>{render_table(['Direction','Count','Minimum mm','Median mm','Maximum mm'], gap_rows)}</section>
<section><h2>Limitations</h2><ul>{limitations}</ul></section>
<section><h2>Embedded data</h2><p>The sanitized summary used by this report is embedded below for auditability.</p><details><summary>Show JSON</summary><pre id="json"></pre></details></section>
</main>
<script id="report-data" type="application/json">{embedded}</script>
<script>
const data=JSON.parse(document.getElementById('report-data').textContent);
document.getElementById('json').textContent=JSON.stringify(data,null,2);
const canvas=document.getElementById('bounce-chart'); const ctx=canvas.getContext('2d');
const items=data.captures.filter(x=>Number.isFinite(x.bounce_span_us));
const max=Math.max(1,...items.map(x=>x.bounce_span_us)); const pad=48; const w=canvas.width-pad*2; const h=canvas.height-pad*2;
ctx.font='14px system-ui'; ctx.fillStyle=getComputedStyle(document.documentElement).getPropertyValue('--text');
ctx.strokeStyle=getComputedStyle(document.documentElement).getPropertyValue('--line'); ctx.beginPath(); ctx.moveTo(pad,pad); ctx.lineTo(pad,pad+h); ctx.lineTo(pad+w,pad+h); ctx.stroke();
items.forEach((item,i)=>{{ const barW=Math.max(8,w/Math.max(1,items.length)-8); const x=pad+i*(w/Math.max(1,items.length))+4; const barH=(item.bounce_span_us/max)*h; ctx.fillStyle=getComputedStyle(document.documentElement).getPropertyValue('--accent'); ctx.fillRect(x,pad+h-barH,barW,barH); ctx.save(); ctx.translate(x+barW/2,pad+h+8); ctx.rotate(-0.5); ctx.textAlign='right'; ctx.fillStyle=getComputedStyle(document.documentElement).getPropertyValue('--text'); ctx.fillText(item.test_id,0,0); ctx.restore(); }});
ctx.fillStyle=getComputedStyle(document.documentElement).getPropertyValue('--muted'); ctx.fillText('Observed transition span (us)',pad,20);
</script></body></html>"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("session_dir", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    session_dir = args.session_dir
    records = read_jsonl(session_dir / "records.jsonl")
    observations = read_jsonl(session_dir / "operator-observations.jsonl")

    summary = build_summary(session_dir, records, observations)
    (session_dir / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    (session_dir / "report.html").write_text(build_html(summary), encoding="utf-8")

    print(f"Generated: {session_dir / 'summary.json'}")
    print(f"Generated: {session_dir / 'report.html'}")
    print("Review and sanitize before copying any generated file into docs/evidence/IHAP-47/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
