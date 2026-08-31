#!/usr/bin/env python3
"""Interactive operator guide for the IHAP-45 controlled environmental phases."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any, Callable, Sequence

import ihap45

PHASE_INSTRUCTIONS = {
    "warmup": "Leave all three sensors co-located and undisturbed under stable room conditions.",
    "baseline": "Maintain stable room conditions; do not touch, breathe on or move the sensors.",
    "humidity_ramp_up": "Introduce the separated humidity source safely. No direct water, mist or steam may contact electronics.",
    "humidity_high_plateau": "Maintain the higher-humidity condition without direct airflow or condensation.",
    "humidity_recovery": "Remove the humidity source and allow the sensors to recover toward ambient conditions.",
    "humidity_low_plateau": "Maintain the lower-humidity condition using a separated dry source; do not place loose material on electronics.",
    "humidity_final_recovery": "Remove the dry source and allow the setup to return toward ambient conditions.",
    "temperature_ramp_up": "Introduce a separated sealed warm mass. Do not use flame, a heat gun or direct hot airflow.",
    "temperature_high_plateau": "Maintain the warmer condition within every sensor's declared operating range.",
    "temperature_recovery": "Remove the warm mass and allow the setup to recover toward ambient conditions.",
    "temperature_low_plateau": "Introduce a separated sealed cold mass. Stop immediately if condensation appears.",
    "final_recovery": "Remove the cold mass and allow the setup to recover under stable room conditions.",
}


def mark_phase(run_dir: Path, phase: str, note: str, plan: dict[str, Any]) -> None:
    allowed = {str(item["name"]) for item in plan.get("phases", [])}
    if phase not in allowed:
        raise ihap45.HarnessError(f"phase {phase!r} is not declared by the test plan")
    paths = ihap45.run_paths(run_dir)
    metadata = ihap45.load_json(paths["metadata"])
    ihap45.atomic_write_text(paths["phase"], phase + "\n")
    ihap45.append_jsonl(
        paths["markers"],
        {
            "record_type": "phase_marker",
            "schema_version": ihap45.SCHEMA_VERSION,
            "run_id": metadata["run_id"],
            "host_timestamp_utc": ihap45.utc_now(),
            "phase": phase,
            "note": note,
        },
    )


def format_duration(seconds: float) -> str:
    minutes, remaining = divmod(int(seconds), 60)
    if minutes and remaining:
        return f"{minutes}m {remaining}s"
    if minutes:
        return f"{minutes}m"
    return f"{remaining}s"


def countdown(
    seconds: float,
    *,
    sleep_fn: Callable[[float], None] = time.sleep,
    monotonic_fn: Callable[[], float] = time.monotonic,
    output: Callable[[str], None] = print,
) -> float:
    started = monotonic_fn()
    deadline = started + seconds
    while True:
        remaining = deadline - monotonic_fn()
        if remaining <= 0:
            break
        output(f"  remaining: {format_duration(remaining)}")
        sleep_fn(min(60.0, remaining))
    actual = monotonic_fn() - started
    output(f"  minimum duration completed: {format_duration(actual)}")
    return actual


def run_guide(
    run_dir: Path,
    plan_path: Path,
    *,
    input_fn: Callable[[str], str] = input,
    sleep_fn: Callable[[float], None] = time.sleep,
    monotonic_fn: Callable[[], float] = time.monotonic,
    output: Callable[[str], None] = print,
) -> bool:
    plan = ihap45.load_json(plan_path)
    paths = ihap45.run_paths(run_dir)
    metadata = ihap45.load_json(paths["metadata"])
    phases = list(plan.get("phases", []))
    if not phases:
        raise ihap45.HarnessError("test plan contains no phases")

    execution: list[dict[str, Any]] = []
    summary_path = run_dir / "phase-guide-summary.json"
    total_minimum = sum(float(phase.get("minimum_seconds", 0)) for phase in phases)

    output(f"IHAP-45 controlled phase guide for {metadata['run_id']}")
    output(f"Minimum timed duration: {format_duration(total_minimum)}")
    output("The serial capture must remain running in the first terminal.")
    output("Type STOP at any prompt to abort without relabelling the next phase.")

    completed = False
    try:
        for index, phase_config in enumerate(phases, start=1):
            phase = str(phase_config["name"])
            minimum_seconds = float(phase_config.get("minimum_seconds", 0))
            instruction = PHASE_INSTRUCTIONS.get(phase, "Apply and maintain the condition described by the approved test plan.")
            output("")
            output(f"[{index}/{len(phases)}] {phase} — minimum {format_duration(minimum_seconds)}")
            output(instruction)
            answer = input_fn("Press ENTER when the condition is ready, or type STOP: ").strip()
            if answer.upper() == "STOP":
                output("Guide aborted by operator before the phase marker was written.")
                return False

            note = f"Operator confirmed phase condition. {instruction}"
            mark_phase(run_dir, phase, note, plan)
            started_at = ihap45.utc_now()
            actual_seconds = countdown(
                minimum_seconds,
                sleep_fn=sleep_fn,
                monotonic_fn=monotonic_fn,
                output=output,
            )
            execution.append(
                {
                    "phase": phase,
                    "minimum_seconds": minimum_seconds,
                    "actual_guide_seconds": actual_seconds,
                    "started_at_utc": started_at,
                    "completed_at_utc": ihap45.utc_now(),
                }
            )
            summary_path.write_text(
                json.dumps(
                    {
                        "run_id": metadata["run_id"],
                        "status": "in_progress",
                        "minimum_total_seconds": total_minimum,
                        "phases": execution,
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
        completed = True
        return True
    finally:
        summary_path.write_text(
            json.dumps(
                {
                    "run_id": metadata["run_id"],
                    "status": "completed" if completed else "aborted",
                    "minimum_total_seconds": total_minimum,
                    "phases": execution,
                    "raw_data_policy": "local_only",
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        if completed:
            output("")
            output("All minimum phase durations completed.")
            output("Leave final recovery stable for one additional sample batch, then stop capture with Ctrl+C in terminal 1.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--plan", default="config/test-plan.json")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        completed = run_guide(Path(args.run_dir), Path(args.plan))
    except (ihap45.HarnessError, KeyboardInterrupt) as exc:
        print(f"IHAP-45 PHASE GUIDE ERROR: {exc}", file=sys.stderr)
        return 2
    return 0 if completed else 2


if __name__ == "__main__":
    raise SystemExit(main())
