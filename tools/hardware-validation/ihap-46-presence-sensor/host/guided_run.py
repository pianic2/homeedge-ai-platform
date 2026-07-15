#!/usr/bin/env python3
"""Human-guided execution of reproducible IHAP-46 physical tests."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import signal
import subprocess
import sys
import time
from typing import Any, Mapping, Sequence

import ihap46

DEFAULT_ACTIONS = Path("config/operator-actions.json")
SENSOR_CHOICES = tuple(ihap46.SENSOR_PATHS)


def load_actions(path: Path, plan: Mapping[str, Any]) -> dict[str, Any]:
    payload = ihap46.load_json(path)
    if not isinstance(payload, dict):
        raise ihap46.HarnessError("Operator actions root must be an object")
    if payload.get("schema_version") != ihap46.SCHEMA_VERSION:
        raise ihap46.HarnessError(
            f"Operator actions schema_version must be {ihap46.SCHEMA_VERSION}"
        )
    actions = payload.get("actions")
    if not isinstance(actions, dict):
        raise ihap46.HarnessError("Operator actions must contain an actions object")

    missing: list[str] = []
    invalid: list[str] = []
    for scenario in plan["scenarios"]:
        scenario_id = str(scenario["id"])
        action = actions.get(scenario_id)
        if not isinstance(action, dict):
            missing.append(scenario_id)
            continue
        if not isinstance(action.get("purpose"), str) or not action["purpose"].strip():
            invalid.append(f"{scenario_id}.purpose")
        for field in ("setup", "during_capture", "invalid_if"):
            value = action.get(field)
            if not isinstance(value, list) or not value or not all(
                isinstance(item, str) and item.strip() for item in value
            ):
                invalid.append(f"{scenario_id}.{field}")
        required = action.get("required_sensor_channels", [])
        if not isinstance(required, list) or not all(
            item in SENSOR_CHOICES for item in required
        ):
            invalid.append(f"{scenario_id}.required_sensor_channels")
    if missing:
        raise ihap46.HarnessError(
            "Missing operator actions for scenarios: " + ", ".join(sorted(missing))
        )
    if invalid:
        raise ihap46.HarnessError(
            "Invalid operator action fields: " + ", ".join(sorted(invalid))
        )
    return payload


def select_scenarios(
    plan: Mapping[str, Any], requested: Sequence[str], include_optional: bool
) -> list[dict[str, Any]]:
    index = ihap46.scenario_index(plan)
    if requested:
        unknown = sorted(set(requested) - set(index))
        if unknown:
            raise ihap46.HarnessError("Unknown scenarios: " + ", ".join(unknown))
        return [index[item] for item in requested]
    if include_optional:
        return [dict(item) for item in plan["scenarios"]]
    return [dict(item) for item in plan["scenarios"] if item.get("required", True)]


def filter_scenarios_for_sensors(
    scenarios: Sequence[Mapping[str, Any]],
    actions: Mapping[str, Any],
    sensors: Sequence[str],
    explicitly_requested: Sequence[str],
) -> list[dict[str, Any]]:
    available = set(sensors)
    explicit = set(explicitly_requested)
    selected: list[dict[str, Any]] = []
    for scenario in scenarios:
        scenario_id = str(scenario["id"])
        required = set(
            actions["actions"][scenario_id].get("required_sensor_channels", [])
        )
        missing = sorted(required - available)
        if not missing:
            selected.append(dict(scenario))
        elif scenario_id in explicit:
            raise ihap46.HarnessError(
                f"Scenario {scenario_id} requires sensor channels: "
                + ", ".join(sorted(required))
            )
        else:
            print(
                f"[SCENARIO] {scenario_id} saltato; canali mancanti: "
                + ", ".join(missing)
            )
    return selected


def build_effective_plan(
    plan: Mapping[str, Any], scenarios: Sequence[Mapping[str, Any]], sensors: Sequence[str]
) -> dict[str, Any]:
    selected_sensors = set(sensors)
    effective = copy.deepcopy(dict(plan))
    effective_scenarios: list[dict[str, Any]] = []
    for source in scenarios:
        scenario = copy.deepcopy(dict(source))
        scenario["expected"] = {
            sensor_id: rule
            for sensor_id, rule in scenario["expected"].items()
            if sensor_id in selected_sensors
        }
        if not scenario["expected"]:
            raise ihap46.HarnessError(
                f"Scenario {scenario['id']} has no expectation for selected sensors"
            )
        effective_scenarios.append(scenario)
    effective["scenarios"] = effective_scenarios
    effective["selected_sensor_channels"] = list(sensors)
    return effective


def format_duration(seconds: float) -> str:
    minutes, remaining = divmod(max(0, int(round(seconds))), 60)
    return f"{minutes:02d}:{remaining:02d}"


def scenario_card(
    scenario: Mapping[str, Any], action: Mapping[str, Any], repetition: int
) -> str:
    setup = "\n".join(f"  {i}. {item}" for i, item in enumerate(action["setup"], 1))
    during = "\n".join(
        f"  {i}. {item}" for i, item in enumerate(action["during_capture"], 1)
    )
    invalid = "\n".join(f"  - {item}" for item in action["invalid_if"])
    return (
        "\n"
        + "=" * 76
        + f"\nTEST: {scenario['id']} — {scenario['title']}\n"
        + f"Ripetizione: {repetition}/{scenario['repetitions']}\n"
        + f"Durata registrata: {format_duration(float(scenario['duration_s']))}\n"
        + f"Stato reale atteso: {scenario['ground_truth']}\n"
        + f"Porta: {scenario['door_state']}\n\n"
        + f"Perché eseguiamo questo test\n  {action['purpose']}\n\n"
        + f"Preparazione prima di iniziare\n{setup}\n\n"
        + f"Azioni durante la registrazione\n{during}\n\n"
        + f"Il tentativo non è valido se\n{invalid}\n"
        + "=" * 76
    )


def collect_operator_metadata(args: argparse.Namespace) -> dict[str, Any]:
    def ask(label: str, current: str | None) -> str:
        value = current or input(f"{label}: ").strip()
        if not value:
            raise ihap46.HarnessError(f"Required operator metadata missing: {label}")
        return value

    if args.mount_height_cm is None:
        raw = input("Altezza del sensore dal pavimento, in cm: ").strip()
        try:
            height = float(raw)
        except ValueError as exc:
            raise ihap46.HarnessError("Mount height must be numeric") from exc
    else:
        height = args.mount_height_cm
    if height <= 0:
        raise ihap46.HarnessError("Mount height must be greater than zero")

    return {
        "operator": ask("Nome operatore", args.operator),
        "sensor_specimen_id": ask("ID del sensore fisico", args.sensor_id),
        "board_specimen_id": ask("ID della board ESP32-C3", args.board_id),
        "room_id": ask("Identificativo della stanza", args.room_id),
        "mount_height_cm": height,
        "mount_orientation": ask(
            "Orientamento del sensore (es. parete nord verso sud)",
            args.mount_orientation,
        ),
        "mount_position": ask("Posizione del sensore nella stanza", args.mount_position),
        "room_notes": args.room_notes
        or input("Note su stanza, porte, pareti e oggetti mobili: ").strip(),
    }


def append_marker(
    run_dir: Path,
    scenario: Mapping[str, Any],
    repetition: int,
    phase: str,
    note: str,
) -> None:
    ihap46.append_jsonl(
        run_dir / "marks.jsonl",
        {
            "schema_version": ihap46.SCHEMA_VERSION,
            "record_type": "ground_truth_marker",
            "run_id": run_dir.name,
            "at": ihap46.isoformat_utc(),
            "at_epoch_ms": ihap46.epoch_ms(),
            "scenario_id": scenario["id"],
            "repetition": repetition,
            "phase": phase,
            "ground_truth": scenario["ground_truth"],
            "door_state": scenario["door_state"],
            "note": note,
        },
    )


def wait_for_capture_start(run_dir: Path, process: subprocess.Popen[Any]) -> None:
    deadline = time.monotonic() + 15
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise ihap46.HarnessError("Serial collector stopped before creating the run")
        if (run_dir / "run.json").exists():
            return
        time.sleep(0.2)
    raise ihap46.HarnessError("Serial collector did not create the run directory")


def preflight(
    run_dir: Path,
    process: subprocess.Popen[Any],
    timeout_s: float,
    sensors: Sequence[str],
) -> None:
    print("\nPRE-FLIGHT")
    print("Non iniziare ancora l'azione dello scenario.")
    print("Quando il dispositivo è collegato, premi una sola volta RST sulla board.")
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise ihap46.HarnessError("Serial collector stopped during pre-flight")
        records = list(ihap46.iter_jsonl(run_dir / "records.jsonl"))
        sources = [item.get("source", {}) for item in records]
        boot = any(
            isinstance(item, Mapping) and item.get("record_type") == "boot"
            for item in sources
        )
        samples = [
            item
            for item in sources
            if isinstance(item, Mapping) and item.get("record_type") == "sample"
        ]
        uart_ok = any(
            bool(ihap46.get_nested(item, ("ld2410c", "uart_frame_valid")))
            for item in samples
        )
        if boot and samples and (uart_ok or "ld2410c_uart" not in sensors):
            print("[PRE-FLIGHT] PASS — firmware e canali selezionati disponibili")
            return
        time.sleep(0.5)
    raise ihap46.HarnessError(
        "Pre-flight failed; inspect serial.log and verify reset, wiring and selected channels"
    )


def run_interval(
    run_dir: Path,
    scenario: Mapping[str, Any],
    action: Mapping[str, Any],
    repetition: int,
    reminder_seconds: float,
) -> None:
    print(scenario_card(scenario, action, repetition))
    input("Completa la preparazione e premi Invio. ")
    for remaining in range(5, 0, -1):
        print(f"Inizio registrazione tra {remaining}...")
        time.sleep(1)

    append_marker(run_dir, scenario, repetition, "start", "guided runtime marker")
    duration = float(scenario["duration_s"])
    deadline = time.monotonic() + duration
    next_reminder = 0.0
    print("[REGISTRAZIONE] IN CORSO")
    print("[AZIONE] " + " ".join(action["during_capture"]))
    while time.monotonic() < deadline:
        now = time.monotonic()
        if now >= next_reminder:
            print(
                f"[REGISTRAZIONE] {format_duration(deadline - now)} rimanenti — "
                + action["during_capture"][0]
            )
            next_reminder = now + reminder_seconds
        time.sleep(min(0.5, max(0.0, deadline - time.monotonic())))
    append_marker(run_dir, scenario, repetition, "end", "guided runtime marker")
    print("[REGISTRAZIONE] COMPLETATA")
    note = input("Annota eventuali anomalie oppure premi Invio: ").strip()
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


def stop_collector(process: subprocess.Popen[Any]) -> None:
    if process.poll() is not None:
        return
    process.send_signal(signal.SIGINT)
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        process.terminate()
        process.wait(timeout=5)


def print_dry_run(
    scenarios: Sequence[Mapping[str, Any]], actions: Mapping[str, Any]
) -> None:
    print("IHAP-46 — ANTEPRIMA DELLA PROCEDURA")
    print("Nessuna porta seriale viene aperta e nessun dato viene registrato.")
    for scenario in scenarios:
        action = actions["actions"][scenario["id"]]
        for repetition in range(1, int(scenario["repetitions"]) + 1):
            print(scenario_card(scenario, action, repetition))


def command_run(args: argparse.Namespace) -> None:
    plan = ihap46.require_valid_plan(args.plan)
    actions = load_actions(args.actions, plan)
    sensors = args.sensor or ["ld2410c_uart"]
    scenarios = select_scenarios(plan, args.scenario, args.include_optional)
    scenarios = filter_scenarios_for_sensors(
        scenarios, actions, sensors, args.scenario
    )
    if not scenarios:
        raise ihap46.HarnessError("No executable scenarios remain")
    effective_plan = build_effective_plan(plan, scenarios, sensors)

    if args.dry_run:
        print_dry_run(scenarios, actions)
        return

    metadata = collect_operator_metadata(args)
    pending_dir = args.runs_dir / ".pending"
    pending_dir.mkdir(parents=True, exist_ok=True)
    pending_plan = pending_dir / f"{args.run_id}-effective-test-plan.json"
    ihap46.write_json(pending_plan, effective_plan)

    command = [
        sys.executable,
        str(Path(__file__).with_name("ihap46.py")),
        "capture",
        "--port",
        args.port,
        "--run-id",
        args.run_id,
        "--plan",
        str(pending_plan),
        "--runs-dir",
        str(args.runs_dir),
        "--baud",
        str(args.baud),
        "--reconnect-seconds",
        str(args.reconnect_seconds),
    ]
    process = subprocess.Popen(command, stdout=subprocess.DEVNULL)
    run_dir = args.runs_dir / args.run_id
    try:
        wait_for_capture_start(run_dir, process)
        effective_plan_path = run_dir / "effective-test-plan.json"
        ihap46.write_json(effective_plan_path, effective_plan)
        run_metadata = ihap46.load_json(run_dir / "run.json")
        run_metadata.update(
            {
                "selected_sensor_channels": sensors,
                "operator_metadata": metadata,
                "plan_path": str(effective_plan_path),
                "plan_snapshot": effective_plan,
                "operator_actions_snapshot": actions,
                "scope": "physical laboratory evidence",
            }
        )
        ihap46.write_json(run_dir / "run.json", run_metadata)
        pending_plan.unlink(missing_ok=True)

        print("\nIHAP-46 — ESECUZIONE GUIDATA")
        print(f"Run: {args.run_id}")
        print(f"Canali valutati: {', '.join(sensors)}")
        preflight(run_dir, process, args.preflight_seconds, sensors)
        for scenario in scenarios:
            action = actions["actions"][scenario["id"]]
            for repetition in range(1, int(scenario["repetitions"]) + 1):
                run_interval(
                    run_dir,
                    scenario,
                    action,
                    repetition,
                    args.reminder_seconds,
                )
    except KeyboardInterrupt:
        ihap46.append_jsonl(
            run_dir / "marks.jsonl",
            {
                "schema_version": ihap46.SCHEMA_VERSION,
                "record_type": "operator_annotation",
                "run_id": args.run_id,
                "at": ihap46.isoformat_utc(),
                "at_epoch_ms": ihap46.epoch_ms(),
                "phase": "point",
                "note": "run aborted by operator",
            },
        )
        raise ihap46.HarnessError("Run interrotta dall'operatore")
    finally:
        stop_collector(process)
        pending_plan.unlink(missing_ok=True)

    results = ihap46.analyze_run(run_dir, run_dir / "effective-test-plan.json")
    ihap46.write_json(run_dir / "results.json", results)
    ihap46.render_report(results, run_dir / "report.html")
    print("\nRUN COMPLETATA")
    print(f"Risultati: {run_dir / 'results.json'}")
    print(f"Report umano: {run_dir / 'report.html'}")
    print("Non modificare questa run; per una correzione usa un nuovo run-id.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Execute reproducible IHAP-46 tests with on-screen instructions."
    )
    parser.add_argument("--port")
    parser.add_argument("--run-id")
    parser.add_argument("--plan", type=Path, default=Path("config/test-plan.json"))
    parser.add_argument("--actions", type=Path, default=DEFAULT_ACTIONS)
    parser.add_argument("--runs-dir", type=Path, default=Path("runs"))
    parser.add_argument("--baud", type=int, default=ihap46.DEFAULT_BAUD)
    parser.add_argument("--sensor", action="append", choices=SENSOR_CHOICES)
    parser.add_argument("--scenario", action="append", default=[])
    parser.add_argument("--include-optional", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--preflight-seconds", type=float, default=30.0)
    parser.add_argument("--reconnect-seconds", type=float, default=1.0)
    parser.add_argument("--reminder-seconds", type=float, default=15.0)
    parser.add_argument("--operator")
    parser.add_argument("--sensor-id")
    parser.add_argument("--board-id")
    parser.add_argument("--room-id")
    parser.add_argument("--mount-height-cm", type=float)
    parser.add_argument("--mount-orientation")
    parser.add_argument("--mount-position")
    parser.add_argument("--room-notes")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.dry_run:
        if not args.port:
            parser.error("--port is required unless --dry-run is used")
        if not args.run_id:
            parser.error("--run-id is required unless --dry-run is used")
    try:
        command_run(args)
    except ihap46.HarnessError as exc:
        print(f"IHAP-46 ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
