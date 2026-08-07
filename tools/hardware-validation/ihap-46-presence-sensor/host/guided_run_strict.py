#!/usr/bin/env python3
"""Strict IHAP-46 guided runner with repeat-level onset integrity gates.

This entrypoint layers additional physical-test integrity checks over
``guided_run.py`` without changing firmware, scenario thresholds, or the raw
evidence contract.
"""

from __future__ import annotations

import copy
from pathlib import Path
import time
from typing import Any, Mapping, Sequence

import guided_run as base
import ihap46

CLEAR_STABLE_SECONDS = 3.0
CLEAR_TIMEOUT_SECONDS = 90.0
OCCUPIED_STABLE_SECONDS = 3.0
OCCUPIED_TIMEOUT_SECONDS = 90.0
LATEST_SAMPLE_MAX_AGE_MS = 1_000

_ORIGINAL_ANALYZE_RUN = ihap46.analyze_run


def onset_sensor_ids(scenario: Mapping[str, Any]) -> tuple[str, ...]:
    """Return selected channels whose scenario rules evaluate onset latency."""

    expected = scenario.get("expected", {})
    if not isinstance(expected, Mapping):
        return ()
    return tuple(
        str(sensor_id)
        for sensor_id, rule in expected.items()
        if isinstance(rule, Mapping) and "max_onset_ms" in rule
    )


def selected_transition_sensor_ids(
    run_dir: Path,
    scenario: Mapping[str, Any],
    transition: str,
) -> tuple[str, ...]:
    """Return selected channels relevant to the scenario transition."""

    expected_transition = scenario.get("expected_transition")
    if expected_transition is not None:
        if expected_transition != transition:
            return ()
    elif transition == "empty_to_occupied":
        # Backward-compatible fallback for pre-transition plan fixtures.
        return onset_sensor_ids(scenario)
    else:
        return ()

    expected = scenario.get("expected", {})
    if not isinstance(expected, Mapping):
        return ()
    expected_ids = {str(sensor_id) for sensor_id in expected}
    try:
        run = ihap46.load_json(run_dir / "run.json")
    except ihap46.HarnessError:
        run = {}
    selected = run.get("selected_sensor_channels") if isinstance(run, Mapping) else None
    if not isinstance(selected, list):
        selected = list(expected_ids)
    return tuple(str(sensor_id) for sensor_id in selected if str(sensor_id) in expected_ids)


def clear_start_snapshot(
    run_dir: Path,
    sensor_ids: Sequence[str],
    started_at_ms: int,
    required_stable_ms: int,
    *,
    now_ms: int | None = None,
) -> dict[str, Any]:
    """Evaluate whether selected channels are freshly and continuously clear."""

    usable: list[tuple[int, dict[str, bool]]] = []
    for record in ihap46.iter_jsonl(run_dir / "records.jsonl"):
        received_ms = int(record.get("received_at_epoch_ms", 0))
        if received_ms < started_at_ms:
            continue
        source = record.get("source")
        if not isinstance(source, Mapping) or source.get("record_type") != "sample":
            continue
        states = {
            sensor_id: ihap46.normalize_sensor_value(source, sensor_id)
            for sensor_id in sensor_ids
        }
        if all(isinstance(value, bool) for value in states.values()):
            usable.append(
                (
                    received_ms,
                    {sensor_id: bool(value) for sensor_id, value in states.items()},
                )
            )

    current_ms = ihap46.epoch_ms() if now_ms is None else int(now_ms)
    if not usable:
        return {
            "status": "WAIT",
            "sample_count": 0,
            "latest_sample_age_ms": None,
            "latest_states": {},
            "stable_clear_ms": 0,
        }

    latest_ms, latest_states = usable[-1]
    latest_sample_age_ms = max(0, current_ms - latest_ms)
    stable_clear_ms = 0
    if all(value is False for value in latest_states.values()):
        clear_start_ms = latest_ms
        for sample_ms, states in reversed(usable):
            if not all(value is False for value in states.values()):
                break
            clear_start_ms = sample_ms
        stable_clear_ms = latest_ms - clear_start_ms

    fresh = latest_sample_age_ms <= LATEST_SAMPLE_MAX_AGE_MS
    return {
        "status": (
            "PASS"
            if fresh and stable_clear_ms >= required_stable_ms
            else "WAIT"
        ),
        "sample_count": len(usable),
        "latest_sample_age_ms": latest_sample_age_ms,
        "latest_states": latest_states,
        "stable_clear_ms": stable_clear_ms,
    }


def occupied_start_snapshot(
    run_dir: Path,
    sensor_ids: Sequence[str],
    started_at_ms: int,
    required_stable_ms: int,
    *,
    now_ms: int | None = None,
) -> dict[str, Any]:
    """Evaluate whether selected channels are freshly and continuously occupied."""

    usable: list[tuple[int, dict[str, bool]]] = []
    for record in ihap46.iter_jsonl(run_dir / "records.jsonl"):
        received_ms = int(record.get("received_at_epoch_ms", 0))
        if received_ms < started_at_ms:
            continue
        source = record.get("source")
        if not isinstance(source, Mapping) or source.get("record_type") != "sample":
            continue
        states = {
            sensor_id: ihap46.normalize_sensor_value(source, sensor_id)
            for sensor_id in sensor_ids
        }
        if all(isinstance(value, bool) for value in states.values()):
            usable.append((received_ms, {sensor_id: bool(value) for sensor_id, value in states.items()}))

    current_ms = ihap46.epoch_ms() if now_ms is None else int(now_ms)
    if not usable:
        return {
            "status": "WAIT",
            "sample_count": 0,
            "latest_sample_age_ms": None,
            "latest_states": {},
            "stable_occupied_ms": 0,
        }

    latest_ms, latest_states = usable[-1]
    latest_sample_age_ms = max(0, current_ms - latest_ms)
    stable_occupied_ms = 0
    if all(value is True for value in latest_states.values()):
        occupied_start_ms = latest_ms
        for sample_ms, states in reversed(usable):
            if not all(value is True for value in states.values()):
                break
            occupied_start_ms = sample_ms
        stable_occupied_ms = latest_ms - occupied_start_ms

    fresh = latest_sample_age_ms <= LATEST_SAMPLE_MAX_AGE_MS
    return {
        "status": (
            "PASS"
            if fresh and stable_occupied_ms >= required_stable_ms
            else "WAIT"
        ),
        "sample_count": len(usable),
        "latest_sample_age_ms": latest_sample_age_ms,
        "latest_states": latest_states,
        "stable_occupied_ms": stable_occupied_ms,
    }


def wait_for_clear_start(
    run_dir: Path,
    scenario: Mapping[str, Any],
    repetition: int,
    sensor_ids: Sequence[str],
    *,
    stable_seconds: float = CLEAR_STABLE_SECONDS,
    timeout_seconds: float = CLEAR_TIMEOUT_SECONDS,
) -> dict[str, Any]:
    """Block an onset repetition until every selected channel is stably clear."""

    required_stable_ms = int(stable_seconds * 1_000)
    started_at_ms = ihap46.epoch_ms()
    deadline = time.monotonic() + timeout_seconds
    next_diagnostic = 0.0

    ihap46.record_capture_event(
        run_dir,
        "onset_clear_gate_started",
        scenario_id=scenario["id"],
        repetition=repetition,
        sensor_channels=list(sensor_ids),
        required_stable_ms=required_stable_ms,
        timeout_ms=int(timeout_seconds * 1_000),
    )
    print(
        "[START GATE] Remain outside the sensing area and substantially still. "
        f"Waiting for {stable_seconds:.1f} seconds of continuous clear state."
    )

    snapshot: dict[str, Any] = {}
    while time.monotonic() < deadline:
        snapshot = clear_start_snapshot(
            run_dir,
            sensor_ids,
            started_at_ms,
            required_stable_ms,
        )
        if snapshot["status"] == "PASS":
            ihap46.record_capture_event(
                run_dir,
                "onset_clear_gate_passed",
                scenario_id=scenario["id"],
                repetition=repetition,
                sensor_channels=list(sensor_ids),
                stable_clear_ms=snapshot["stable_clear_ms"],
                latest_states=snapshot["latest_states"],
            )
            print(
                "[START GATE] PASS — selected channels are freshly and "
                "continuously clear"
            )
            return snapshot

        now = time.monotonic()
        if now >= next_diagnostic:
            states = snapshot.get("latest_states") or "no fresh sample"
            print(
                "[START GATE] waiting — "
                f"states={states}, "
                f"stable_clear_ms={snapshot.get('stable_clear_ms', 0)}, "
                f"sample_age_ms={snapshot.get('latest_sample_age_ms')}"
            )
            next_diagnostic = now + 2.0
        time.sleep(0.1)

    ihap46.record_capture_event(
        run_dir,
        "onset_clear_gate_failed",
        scenario_id=scenario["id"],
        repetition=repetition,
        sensor_channels=list(sensor_ids),
        latest_states=snapshot.get("latest_states", {}),
        stable_clear_ms=snapshot.get("stable_clear_ms", 0),
    )
    raise ihap46.HarnessError(
        "Onset start gate timed out before the selected channels were stably "
        "clear. Preserve the run and inspect adjacent-area detection or clear "
        "latency before repeating."
    )


def wait_for_occupied_start(
    run_dir: Path,
    scenario: Mapping[str, Any],
    repetition: int,
    sensor_ids: Sequence[str],
    *,
    stable_seconds: float = OCCUPIED_STABLE_SECONDS,
    timeout_seconds: float = OCCUPIED_TIMEOUT_SECONDS,
) -> dict[str, Any]:
    """Block an offset repetition until every selected channel is stably occupied."""

    required_stable_ms = int(stable_seconds * 1_000)
    started_at_ms = ihap46.epoch_ms()
    deadline = time.monotonic() + timeout_seconds
    next_diagnostic = 0.0

    ihap46.record_capture_event(
        run_dir,
        "offset_occupied_gate_started",
        scenario_id=scenario["id"],
        repetition=repetition,
        sensor_channels=list(sensor_ids),
        required_stable_ms=required_stable_ms,
        timeout_ms=int(timeout_seconds * 1_000),
    )
    print(
        "[START GATE] Remain at the documented occupied point. "
        f"Waiting for {stable_seconds:.1f} seconds of continuous occupied state."
    )

    snapshot: dict[str, Any] = {}
    while time.monotonic() < deadline:
        snapshot = occupied_start_snapshot(
            run_dir, sensor_ids, started_at_ms, required_stable_ms
        )
        if snapshot["status"] == "PASS":
            ihap46.record_capture_event(
                run_dir,
                "offset_occupied_gate_passed",
                scenario_id=scenario["id"],
                repetition=repetition,
                sensor_channels=list(sensor_ids),
                stable_occupied_ms=snapshot["stable_occupied_ms"],
                latest_states=snapshot["latest_states"],
            )
            print(
                "[START GATE] PASS — selected channels are freshly and "
                "continuously occupied"
            )
            return snapshot

        now = time.monotonic()
        if now >= next_diagnostic:
            print(
                "[START GATE] waiting — "
                f"states={snapshot.get('latest_states') or 'no fresh sample'}, "
                f"stable_occupied_ms={snapshot.get('stable_occupied_ms', 0)}, "
                f"sample_age_ms={snapshot.get('latest_sample_age_ms')}"
            )
            next_diagnostic = now + 2.0
        time.sleep(0.1)

    ihap46.record_capture_event(
        run_dir,
        "offset_occupied_gate_failed",
        scenario_id=scenario["id"],
        repetition=repetition,
        sensor_channels=list(sensor_ids),
        latest_states=snapshot.get("latest_states", {}),
        stable_occupied_ms=snapshot.get("stable_occupied_ms", 0),
    )
    raise ihap46.HarnessError(
        "Offset start gate timed out before the selected channels were stably "
        "occupied. Preserve the run and inspect the occupied precondition."
    )


def countdown_finished_clear(
    run_dir: Path,
    sensor_ids: Sequence[str],
) -> bool:
    """Confirm that no selected channel became present during the countdown."""

    now_ms = ihap46.epoch_ms()
    snapshot = clear_start_snapshot(
        run_dir,
        sensor_ids,
        now_ms - LATEST_SAMPLE_MAX_AGE_MS,
        0,
        now_ms=now_ms,
    )
    return snapshot["status"] == "PASS" and all(
        value is False for value in snapshot["latest_states"].values()
    )


def countdown_finished_occupied(
    run_dir: Path,
    sensor_ids: Sequence[str],
) -> bool:
    """Confirm that all selected channels remain present during the countdown."""

    now_ms = ihap46.epoch_ms()
    snapshot = occupied_start_snapshot(
        run_dir,
        sensor_ids,
        now_ms - LATEST_SAMPLE_MAX_AGE_MS,
        0,
        now_ms=now_ms,
    )
    return snapshot["status"] == "PASS" and all(
        value is True for value in snapshot["latest_states"].values()
    )


def strict_run_interval(
    run_dir: Path,
    scenario: Mapping[str, Any],
    action: Mapping[str, Any],
    repetition: int,
    reminder_seconds: float,
) -> None:
    """Run one interval, enforcing a clear precondition for onset scenarios."""

    print(base.scenario_card(scenario, action, repetition))
    input("Complete the setup, move to the required start position, and press Enter. ")

    onset_channels = selected_transition_sensor_ids(
        run_dir, scenario, "empty_to_occupied"
    )
    offset_channels = selected_transition_sensor_ids(
        run_dir, scenario, "occupied_to_empty"
    )
    while True:
        if onset_channels:
            wait_for_clear_start(
                run_dir,
                scenario,
                repetition,
                onset_channels,
            )
        if offset_channels:
            wait_for_occupied_start(
                run_dir,
                scenario,
                repetition,
                offset_channels,
            )

        for remaining in range(5, 0, -1):
            print(f"Recording starts in {remaining}...")
            time.sleep(1)

        countdown_valid = True
        if onset_channels:
            countdown_valid = countdown_finished_clear(run_dir, onset_channels)
        if offset_channels:
            countdown_valid = countdown_valid and countdown_finished_occupied(
                run_dir, offset_channels
            )
        if not onset_channels and not offset_channels:
            countdown_valid = True
        if countdown_valid:
            break

        transition_prefix = "onset" if onset_channels else "offset"
        ihap46.record_capture_event(
            run_dir,
            f"{transition_prefix}_countdown_restarted",
            scenario_id=scenario["id"],
            repetition=repetition,
            sensor_channels=list(onset_channels or offset_channels),
            reason=(
                "presence returned before the start marker"
                if onset_channels
                else "presence cleared before the start marker"
            ),
        )
        if onset_channels:
            print(
                "[START GATE] Presence returned during the countdown. "
                "The marker was not created; restarting the clear-state gate."
            )
        else:
            print(
                "[START GATE] Presence cleared during the countdown. "
                "The marker was not created; restarting the occupied-state gate."
            )

    base.append_marker(
        run_dir,
        scenario,
        repetition,
        "start",
        "strict guided runtime marker",
    )
    duration = float(scenario["duration_s"])
    deadline = time.monotonic() + duration
    next_reminder = 0.0
    print("[RECORDING] IN PROGRESS")
    print("[ACTION] " + " ".join(action["during_capture"]))

    while time.monotonic() < deadline:
        now = time.monotonic()
        if now >= next_reminder:
            print(
                f"[RECORDING] {base.format_duration(deadline - now)} remaining — "
                + action["during_capture"][0]
            )
            next_reminder = now + reminder_seconds
        time.sleep(min(0.5, max(0.0, deadline - time.monotonic())))

    base.append_marker(
        run_dir,
        scenario,
        repetition,
        "end",
        "strict guided runtime marker",
    )
    print("[RECORDING] COMPLETE")
    note = input(
        "Record any anomaly or invalidating event, or press Enter for none: "
    ).strip()
    if note:
        ihap46.append_jsonl(
            run_dir / "marks.jsonl",
            {
                "schema_version": ihap46.SCHEMA_VERSION,
                "record_type": "operator_annotation",
                "run_id": run_dir.name,
                "at": ihap46.isoformat_utc(),
                "at_epoch_ms": ihap46.epoch_ms(),
                "scenario_id": scenario["id"],
                "repetition": repetition,
                "phase": "point",
                "note": note,
            },
        )


def latest_pre_start_value(
    records: Sequence[Mapping[str, Any]],
    start_ms: int,
    sensor_id: str,
) -> tuple[bool | None, int | None]:
    """Return the latest normalized value immediately before a marker."""

    for record in reversed(records):
        received_ms = int(record.get("received_at_epoch_ms", 0))
        if received_ms >= start_ms:
            continue
        age_ms = start_ms - received_ms
        if age_ms > LATEST_SAMPLE_MAX_AGE_MS:
            return None, None
        source = record.get("source")
        if not isinstance(source, Mapping) or source.get("record_type") != "sample":
            continue
        value = ihap46.normalize_sensor_value(source, sensor_id)
        if isinstance(value, bool):
            return value, age_ms
    return None, None


def apply_onset_integrity(
    results: Mapping[str, Any],
    records: Sequence[Mapping[str, Any]],
    plan: Mapping[str, Any],
) -> dict[str, Any]:
    """Reject latency metrics without a fresh clear pre-start observation."""

    updated = copy.deepcopy(dict(results))
    scenarios = ihap46.scenario_index(plan)
    ordered_records = sorted(
        records,
        key=lambda record: int(record.get("received_at_epoch_ms", 0)),
    )
    invalid_count = 0

    for interval in updated.get("intervals", []):
        scenario = scenarios.get(str(interval.get("scenario_id")), {})
        expected = scenario.get("expected", {})
        for sensor_id, metrics in interval.get("sensors", {}).items():
            rule = expected.get(sensor_id, {}) if isinstance(expected, Mapping) else {}
            if not isinstance(rule, Mapping) or "max_onset_ms" not in rule:
                continue

            pre_start_value, sample_age_ms = latest_pre_start_value(
                ordered_records,
                int(interval["start_epoch_ms"]),
                sensor_id,
            )
            metrics["pre_start_presence"] = pre_start_value
            metrics["pre_start_sample_age_ms"] = sample_age_ms
            metrics["onset_integrity"] = (
                "PASS" if pre_start_value is False else "FAIL"
            )

            if pre_start_value is False:
                continue

            invalid_count += 1
            raw_latency = metrics.get("first_true_latency_ms")
            metrics["raw_first_true_latency_ms"] = raw_latency
            metrics["first_true_latency_ms"] = None
            reason = (
                "onset invalid: sensor was already present immediately before "
                "the interval start"
                if pre_start_value is True
                else "onset invalid: no fresh pre-start sensor sample"
            )
            failures = list(metrics.get("failures", []))
            if reason not in failures:
                failures.append(reason)
            metrics["failures"] = failures
            metrics["status"] = "FAIL"

        sensors = interval.get("sensors", {})
        interval["status"] = (
            "PASS"
            if sensors and all(item.get("status") == "PASS" for item in sensors.values())
            else "FAIL"
        )

    updated["summary"] = ihap46.summarize_results(updated.get("intervals", []))
    warnings = list(updated.get("warnings", []))
    if invalid_count:
        warnings.append(
            f"Rejected {invalid_count} onset interval(s) without a fresh clear "
            "pre-start observation"
        )
    updated["warnings"] = warnings
    return updated


def strict_analyze_run(run_dir: Path, plan_path: Path) -> dict[str, Any]:
    """Run canonical analysis and then enforce onset precondition integrity."""

    results = _ORIGINAL_ANALYZE_RUN(run_dir, plan_path)
    records = list(ihap46.iter_jsonl(run_dir / "records.jsonl"))
    plan = ihap46.require_valid_plan(plan_path)
    return apply_onset_integrity(results, records, plan)


def main(argv: Sequence[str] | None = None) -> int:
    """Execute the existing guided CLI with strict interval hooks installed."""

    base.run_interval = strict_run_interval
    ihap46.analyze_run = strict_analyze_run
    return base.main(argv)


if __name__ == "__main__":
    raise SystemExit(main())
