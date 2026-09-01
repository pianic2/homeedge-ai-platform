#!/usr/bin/env python3
"""Build a sanitized IHAP-47 summary and standalone HTML report.

The report consumes the local guided result when present so the operator never
has to re-enter cycle or failure-mode data manually.
"""

from __future__ import annotations

import argparse
import html
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected JSON object")
    return value


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    if not path.exists():
        return result
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"{path}:{line_number}: expected JSON object")
        result.append(value)
    return result


def capture_summaries(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    captures: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None

    for record in records:
        kind = record.get("record_type")
        if kind == "capture_started":
            current = {
                "test_id": record.get("test_id"),
                "specimen_id": record.get("specimen_id"),
                "initial_level": record.get("initial_level"),
                "sample_period_us": record.get("sample_period_us"),
                "transitions": [],
            }
        elif kind == "raw_transition" and current is not None:
            current["transitions"].append(record)
        elif kind == "capture_ended":
            if current is None:
                current = {
                    "test_id": record.get("test_id"),
                    "specimen_id": record.get("specimen_id"),
                    "initial_level": record.get("initial_level"),
                    "sample_period_us": record.get("sample_period_us"),
                    "transitions": [],
                }
            offsets = [
                int(item["offset_us"])
                for item in current["transitions"]
                if isinstance(item.get("offset_us"), (int, float))
            ]
            span = max(offsets) - min(offsets) if len(offsets) >= 2 else 0
            captures.append(
                {
                    "test_id": record.get("test_id", current.get("test_id")),
                    "specimen_id": record.get("specimen_id", current.get("specimen_id")),
                    "initial_level": record.get(
                        "initial_level", current.get("initial_level")
                    ),
                    "final_level": record.get("final_level"),
                    "transition_count": record.get(
                        "transition_count", len(current["transitions"])
                    ),
                    "raw_transition_span_us": span,
                    "sample_period_us": record.get(
                        "sample_period_us", current.get("sample_period_us")
                    ),
                    "buffer_overflow": bool(record.get("buffer_overflow", False)),
                }
            )
            current = None

    return captures


def compact_cycle_test(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        return {}
    keys = (
        "complete_cycles",
        "stable_movements",
        "mismatches",
        "buffer_overflows",
        "movements_with_multiple_raw_transitions",
        "max_raw_transition_span_us",
        "sample_period_us",
        "stable_window_ms",
        "pass",
    )
    return {key: value.get(key) for key in keys if key in value}


def build_summary(session_dir: Path) -> dict[str, Any]:
    records = read_jsonl(session_dir / "records.jsonl")
    observations = read_jsonl(session_dir / "operator-observations.jsonl")
    guided = read_json(session_dir / "guided-result.json")
    session = read_json(session_dir / "session.json")

    captures = capture_summaries(records)
    summary: dict[str, Any] = {
        "schema_version": "1.1.0",
        "issue": "IHAP-47",
        "generated_at_utc": utc_now(),
        "source_session": session_dir.name,
        "evidence_class": "observed-owned-specimen-pending-review",
        "physical_results_validated": False,
        "raw_logs_included": False,
        "records_count": len(records),
        "operator_observations_count": len(observations),
        "capture_count": len(captures),
        "captures_with_buffer_overflow": sum(
            1 for item in captures if item["buffer_overflow"]
        ),
        "captures": captures,
        "limitations": [
            "The report is generated from a test harness, not production firmware.",
            "Firmware timestamps are not independent oscilloscope-grade measurements.",
            "Open circuit does not distinguish door open from disconnected wire or failed-open contact.",
            "Results apply only to the recorded specimen, setup and session.",
            "Project Owner review is required before any ADR status change.",
        ],
    }

    if session:
        summary["execution_mode"] = session.get("mode")
        summary["specimen_id"] = session.get("specimen_id")
        summary["requested_cycles"] = session.get("requested_cycles")

    if guided:
        summary["mapping"] = guided.get("mapping", {})
        summary["cycle_test"] = compact_cycle_test(guided.get("cycle_test"))
        summary["failure_modes"] = guided.get("failure_modes", {})
        summary["pull_up_bench_adequate"] = guided.get(
            "pull_up_bench_adequate", False
        )
        summary["decision_gate_pass"] = guided.get("decision_gate_pass", False)

    return summary


def esc(value: Any) -> str:
    if value is None:
        return "—"
    if isinstance(value, bool):
        return "true" if value else "false"
    return html.escape(str(value))


def build_html(summary: dict[str, Any]) -> str:
    mapping = summary.get("mapping", {})
    cycles = summary.get("cycle_test", {})
    failure = summary.get("failure_modes", {})

    capture_rows = "".join(
        "<tr>"
        f"<td>{esc(item.get('test_id'))}</td>"
        f"<td>{esc(item.get('initial_level'))}</td>"
        f"<td>{esc(item.get('final_level'))}</td>"
        f"<td>{esc(item.get('transition_count'))}</td>"
        f"<td>{esc(item.get('raw_transition_span_us'))}</td>"
        f"<td>{esc(item.get('buffer_overflow'))}</td>"
        "</tr>"
        for item in summary.get("captures", [])
    )

    embedded = json.dumps(summary, separators=(",", ":")).replace("</", "<\\/")
    limitations = "".join(
        f"<li>{html.escape(item)}</li>" for item in summary["limitations"]
    )

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>IHAP-47 Guided Validation Report</title>
<style>
body{{font:15px/1.5 system-ui,sans-serif;max-width:1100px;margin:32px auto;padding:0 16px}}
section{{margin:20px 0;padding:16px;border:1px solid #aaa;border-radius:10px}}
table{{border-collapse:collapse;width:100%}}th,td{{padding:7px;border-bottom:1px solid #bbb;text-align:left}}
.pass{{font-weight:700}}code,pre{{white-space:pre-wrap;overflow-wrap:anywhere}}
</style>
</head>
<body>
<h1>IHAP-47 — Guided Door Contact Validation</h1>
<p>This is telemetry evidence only. It is not alarm, tamper, access-control,
intrusion-detection, antifurto, safety or reliability certification.</p>

<section>
<h2>Decision gate</h2>
<p class="pass">{'PASS' if summary.get('decision_gate_pass') else 'PENDING/FAIL'}</p>
<p>Physical results validated by Project Owner: {esc(summary.get('physical_results_validated'))}</p>
</section>

<section>
<h2>Electrical mapping</h2>
<ul>
<li>FAR raw level: {esc(mapping.get('far_level'))}</li>
<li>NEAR raw level: {esc(mapping.get('near_level'))}</li>
</ul>
</section>

<section>
<h2>Automated cycle gate</h2>
<ul>
<li>Complete cycles: {esc(cycles.get('complete_cycles'))}</li>
<li>Stable movements: {esc(cycles.get('stable_movements'))}</li>
<li>Mismatches: {esc(cycles.get('mismatches'))}</li>
<li>Buffer overflows: {esc(cycles.get('buffer_overflows'))}</li>
<li>Movements with multiple raw transitions: {esc(cycles.get('movements_with_multiple_raw_transitions'))}</li>
<li>Maximum observed multi-transition span (us): {esc(cycles.get('max_raw_transition_span_us'))}</li>
<li>Sampling period (us): {esc(cycles.get('sample_period_us'))}</li>
</ul>
</section>

<section>
<h2>Failure-mode gate</h2>
<ul>
<li>Disconnected conductor raw level: {esc(failure.get('disconnected_conductor_level'))}</li>
<li>GPIO-to-GND raw level: {esc(failure.get('gpio_to_ground_level'))}</li>
<li>Failure-mode gate pass: {esc(failure.get('pass'))}</li>
<li>Internal pull-up bench adequate: {esc(summary.get('pull_up_bench_adequate'))}</li>
</ul>
<p>Open contact and interrupted conductor remain electrically indistinguishable
under the simple two-wire pull-up topology.</p>
</section>

<section>
<h2>Raw capture audit</h2>
<table>
<thead><tr><th>Test</th><th>Initial</th><th>Final</th><th>Transitions</th><th>Span us</th><th>Overflow</th></tr></thead>
<tbody>{capture_rows}</tbody>
</table>
</section>

<section>
<h2>Limitations</h2>
<ul>{limitations}</ul>
</section>

<details><summary>Embedded sanitized JSON</summary><pre id="json"></pre></details>
<script id="data" type="application/json">{embedded}</script>
<script>document.getElementById('json').textContent=JSON.stringify(JSON.parse(document.getElementById('data').textContent),null,2);</script>
</body></html>
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("session_dir", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summary = build_summary(args.session_dir)
    (args.session_dir / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    (args.session_dir / "report.html").write_text(
        build_html(summary), encoding="utf-8"
    )

    print(f"Generated: {args.session_dir / 'summary.json'}")
    print(f"Generated: {args.session_dir / 'report.html'}")
    print("Review and sanitize before publishing decision evidence.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
