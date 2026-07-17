#!/usr/bin/env python3
"""Human-guided execution of reproducible IHAP-46 physical tests."""

from __future__ import annotations

import argparse
import copy
from pathlib import Path
import signal
import subprocess
import sys
import time
from typing import Any, Mapping, Sequence

import ihap46

DEFAULT_ACTIONS = Path("config/operator-actions.json")
DEFAULT_ENVIRONMENT = Path("config/default-environment.json")
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


def load_environment(path: Path) -> dict[str, Any]:
    payload = ihap46.load_json(path)
    if not isinstance(payload, dict):
        raise ihap46.HarnessError("Environment profile root must be an object")
    if payload.get("schema_version") != ihap46.SCHEMA_VERSION:
        raise ihap46.HarnessError(
            f"Environment schema_version must be {ihap46.SCHEMA_VERSION}"
        )

    profile_id = payload.get("profile_id")
    defaults = payload.get("defaults")
    positions = payload.get("reference_test_positions")
    if not isinstance(profile_id, str) or not profile_id.strip():
        raise ihap46.HarnessError("Environment profile_id must be a non-empty string")
    if not isinstance(defaults, dict):
        raise ihap46.HarnessError("Environment profile must contain defaults")
    if not isinstance(positions, dict):
        raise ihap46.HarnessError(
            "Environment profile must contain reference_test_positions"
        )

    required_text = (
        "room_id",
        "room_shape",
        "door_location",
        "mount_position",
        "mount_orientation",
        "room_notes",
    )
    required_numbers = ("room_width_m", "room_depth_m", "mount_height_cm")
    invalid: list[str] = []
    for field in required_text:
        value = defaults.get(field)
        if not isinstance(value, str) or not value.strip():
            invalid.append(f"defaults.{field}")
    for field in required_numbers:
        value = defaults.get(field)
        if not isinstance(value, (int, float)) or float(value) <= 0:
            invalid.append(f"defaults.{field}")
    for field, value in positions.items():
        if not isinstance(field, str) or not isinstance(value, str) or not value.strip():
            invalid.append(f"reference_test_positions.{field}")

    if invalid:
        raise ihap46.HarnessError(
            "Invalid environment fields: " + ", ".join(sorted(invalid))
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
                f"[SCENARIO] {scenario_id} skipped; missing channels: "
                + ", ".join(missing)
            )
    return selected


def build_effective_plan(
    plan: Mapping[str, Any],
    scenarios: Sequence[Mapping[str, Any]],
    sensors: Sequence[str],
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
        + f"Repetition: {repetition}/{scenario['repetitions']}\n"
        + f"Recorded duration: {format_duration(float(scenario['duration_s']))}\n"
        + f"Expected ground truth: {scenario['ground_truth']}\n"
        + f"Door state: {scenario['door_state']}\n\n"
        + f"Test purpose\n  {action['purpose']}\n\n"
        + f"Setup before recording\n{setup}\n\n"
        + f"Actions during recording\n{during}\n\n"
        + f"Invalidate this attempt if\n{invalid}\n"
        + "=" * 76
    )


def effective_environment(
    environment: Mapping[str, Any], args: argparse.Namespace
) -> dict[str, Any]:
    defaults = dict(environment["defaults"])
    overrides = {
        "room_id": args.room_id,
        "room_width_m": args.room_width_m,
        "room_depth_m": args.room_depth_m,
        "door_location": args.door_location,
        "mount_height_cm": args.mount_height_cm,
        "mount_orientation": args.mount_orientation,
        "mount_position": args.mount_position,
        "room_notes": args.room_notes,
    }
    for field, value in overrides.items():
        if value is not None:
            defaults[field] = value

    return {
        "schema_version": environment["schema_version"],
        "issue": environment.get("issue", "IHAP-46"),
        "profile_id": environment["profile_id"],
        "description": environment.get("description"),
        "values": defaults,
        "reference_test_positions": copy.deepcopy(
            environment["reference_test_positions"]
        ),
        "override_rule": environment.get("override_rule"),
    }


def environment_summary(environment: Mapping[str, Any]) -> str:
    values = environment["values"]
    positions = environment["reference_test_positions"]
    position_lines = "\n".join(
        f"  - {name}: {description}" for name, description in positions.items()
    )
    return (
        "\nREFERENCE PHYSICAL SETUP\n"
        f"  Profile: {environment['profile_id']}\n"
        f"  Room: {values['room_width_m']:.2f} m x "
        f"{values['room_depth_m']:.2f} m ({values['room_shape']})\n"
        f"  Door: {values['door_location']}\n"
        f"  Sensor height: {values['mount_height_cm'] / 100:.2f} m\n"
        f"  Sensor position: {values['mount_position']}\n"
        f"  Sensor orientation: {values['mount_orientation']}\n"
        "  Reference points:\n"
        f"{position_lines}\n"
    )


def collect_operator_metadata(
    args: argparse.Namespace, environment: Mapping[str, Any]
) -> dict[str, Any]:
    values = environment["values"]

    def ask_required(label: str, current: str | None) -> str:
        value = current or input(f"{label}: ").strip()
        if not value:
            raise ihap46.HarnessError(f"Required operator metadata missing: {label}")
        return value

    def ask_default(label: str, current: Any) -> str:
        raw = input(f"{label} [{current}]: ").strip()
        return raw or str(current)

    def ask_float_default(label: str, current: float) -> float:
        raw = input(f"{label} [{current}]: ").strip()
        if not raw:
            return float(current)
        try:
            value = float(raw)
        except ValueError as exc:
            raise ihap46.HarnessError(f"{label} must be numeric") from exc
        if value <= 0:
            raise ihap46.HarnessError(f"{label} must be greater than zero")
        return value

    room_width_m = ask_float_default("Room width in metres", values["room_width_m"])
    room_depth_m = ask_float_default("Room depth in metres", values["room_depth_m"])
    mount_height_cm = ask_float_default(
        "Sensor height above floor in centimetres", values["mount_height_cm"]
    )

    return {
        "operator": ask_required("Operator name", args.operator),
        "sensor_specimen_id": ask_required(
            "Physical sensor specimen ID", args.sensor_id
        ),
        "board_specimen_id": ask_required(
            "ESP32-C3 board specimen ID", args.board_id
        ),
        "environment_profile_id": environment["profile_id"],
        "room_id": ask_default("Room ID", values["room_id"]),
        "room_shape": values["room_shape"],
        "room_width_m": room_width_m,
        "room_depth_m": room_depth_m,
        "door_location": ask_default("Door location", values["door_location"]),
        "mount_height_cm": mount_height_cm,
        "mount_orientation": ask_default(
            "Sensor orientation", values["mount_orientation"]
        ),
        "mount_position": ask_default("Sensor position", values["mount_position"]),
        "room_notes": ask_default(
            "Room and adjacent-space notes", values["room_notes"]
        ),
        "reference_test_positions": copy.deepcopy(
            environment["reference_test_positions"]
        ),
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
            raise ihap46.HarnessError(
                "Serial collector stopped before creating the run"
            )
        if (run_dir / "run.json").exists():
            return
        time.sleep(0.2)
    raise ihap46.HarnessError("Serial collector did not create the run directory")


def preflight_snapshot(
    run_dir: Path, started_at_ms: int, sensors: Sequence[str]
) -> dict[str, Any]:
    """Return pre-flight diagnostics using evidence created after the gate starts."""

    records = [
        item
        for item in ihap46.iter_jsonl(run_dir / "records.jsonl")
        if int(item.get("received_at_epoch_ms", 0)) >= started_at_ms
    ]
    sources = [item.get("source", {}) for item in records]
    boot_count = sum(
        1
        for item in sources
        if isinstance(item, Mapping) and item.get("record_type") == "boot"
    )
    samples = [
        item
        for item in sources
        if isinstance(item, Mapping) and item.get("record_type") == "sample"
    ]
    valid_uart_count = sum(
        1
        for item in samples
        if bool(ihap46.get_nested(item, ("ld2410c", "uart_frame_valid")))
    )

    events = sorted(
        (
            item
            for item in ihap46.iter_jsonl(run_dir / "capture-events.jsonl")
            if int(item.get("at_epoch_ms", 0)) >= started_at_ms
        ),
        key=lambda item: int(item.get("at_epoch_ms", 0)),
    )
    disconnected = False
    reconnected_after_disconnect = False
    for event in events:
        if event.get("event") == "serial_disconnected":
            disconnected = True
        elif event.get("event") == "serial_connected" and disconnected:
            reconnected_after_disconnect = True

    reset_observed = boot_count > 0 or reconnected_after_disconnect
    selected_channels_ready = bool(samples) and (
        "ld2410c_uart" not in sensors or valid_uart_count > 0
    )
    return {
        "schema_version": ihap46.SCHEMA_VERSION,
        "issue": "IHAP-46",
        "started_at_epoch_ms": started_at_ms,
        "fresh_record_count": len(records),
        "fresh_sample_count": len(samples),
        "fresh_boot_count": boot_count,
        "fresh_valid_uart_count": valid_uart_count,
        "serial_disconnect_observed": disconnected,
        "serial_reconnect_after_disconnect": reconnected_after_disconnect,
        "reset_observed": reset_observed,
        "selected_channels_ready": selected_channels_ready,
        "status": "PASS" if reset_observed and selected_channels_ready else "WAIT",
    }


def preflight(
    run_dir: Path,
    process: subprocess.Popen[Any],
    timeout_s: float,
    sensors: Sequence[str],
) -> None:
    print("\nPRE-FLIGHT")
    print("Do not start the scenario action yet.")
    print("With the device connected, press the ESP32-C3 RST button once.")
    print(
        "The reset may be observed either as a boot record or as a USB "
        "disconnect/reconnect sequence."
    )

    started_at_ms = ihap46.epoch_ms()
    ihap46.record_capture_event(
        run_dir,
        "guided_preflight_started",
        selected_channels=list(sensors),
    )
    deadline = time.monotonic() + timeout_s
    next_diagnostic = 0.0
    snapshot: dict[str, Any] = {}

    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise ihap46.HarnessError("Serial collector stopped during pre-flight")

        snapshot = preflight_snapshot(run_dir, started_at_ms, sensors)
        if snapshot["status"] == "PASS":
            snapshot["completed_at"] = ihap46.isoformat_utc()
            ihap46.write_json(run_dir / "preflight.json", snapshot)
            ihap46.record_capture_event(
                run_dir,
                "guided_preflight_passed",
                boot_records=snapshot["fresh_boot_count"],
                valid_uart_samples=snapshot["fresh_valid_uart_count"],
                reconnect=snapshot["serial_reconnect_after_disconnect"],
            )
            print(
                "[PRE-FLIGHT] PASS — fresh samples received and reset/reconnect "
                "evidence observed"
            )
            return

        now = time.monotonic()
        if now >= next_diagnostic:
            print(
                "[PRE-FLIGHT] waiting — "
                f"samples={snapshot['fresh_sample_count']}, "
                f"valid_uart={snapshot['fresh_valid_uart_count']}, "
                f"boot={snapshot['fresh_boot_count']}, "
                f"reconnect={snapshot['serial_reconnect_after_disconnect']}"
            )
            next_diagnostic = now + 2.0
        time.sleep(0.25)

    snapshot = preflight_snapshot(run_dir, started_at_ms, sensors)
    snapshot["status"] = "FAIL"
    snapshot["completed_at"] = ihap46.isoformat_utc()
    snapshot["failure_reason"] = (
        "No combination of fresh selected-channel samples and reset evidence "
        "was observed before timeout."
    )
    ihap46.write_json(run_dir / "preflight.json", snapshot)
    ihap46.record_capture_event(
        run_dir,
        "guided_preflight_failed",
        fresh_samples=snapshot["fresh_sample_count"],
        valid_uart_samples=snapshot["fresh_valid_uart_count"],
        boot_records=snapshot["fresh_boot_count"],
        reconnect=snapshot["serial_reconnect_after_disconnect"],
    )
    raise ihap46.HarnessError(
        "Pre-flight failed; inspect preflight.json, serial.log, records.jsonl, "
        "and capture-events.jsonl"
    )


def run_interval(
    run_dir: Path,
    scenario: Mapping[str, Any],
    action: Mapping[str, Any],
    repetition: int,
    reminder_seconds: float,
) -> None:
    print(scenario_card(scenario, action, repetition))
    input("Complete the setup, move to the required start position, and press Enter. ")
    for remaining in range(5, 0, -1):
        print(f"Recording starts in {remaining}...")
        time.sleep(1)

    append_marker(run_dir, scenario, repetition, "start", "guided runtime marker")
    duration = float(scenario["duration_s"])
    deadline = time.monotonic() + duration
    next_reminder = 0.0
    print("[RECORDING] IN PROGRESS")
    print("[ACTION] " + " ".join(action["during_capture"]))
    while time.monotonic() < deadline:
        now = time.monotonic()
        if now >= next_reminder:
            print(
                f"[RECORDING] {format_duration(deadline - now)} remaining — "
                + action["during_capture"][0]
            )
            next_reminder = now + reminder_seconds
        time.sleep(min(0.5, max(0.0, deadline - time.monotonic())))

    append_marker(run_dir, scenario, repetition, "end", "guided runtime marker")
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
    scenarios: Sequence[Mapping[str, Any]],
    actions: Mapping[str, Any],
    environment: Mapping[str, Any],
) -> None:
    print("IHAP-46 — PROCEDURE PREVIEW")
    print("No serial port is opened and no evidence is recorded.")
    print(environment_summary(environment))
    for scenario in scenarios:
        action = actions["actions"][scenario["id"]]
        for repetition in range(1, int(scenario["repetitions"]) + 1):
            print(scenario_card(scenario, action, repetition))


def command_run(args: argparse.Namespace) -> None:
    plan = ihap46.require_valid_plan(args.plan)
    actions = load_actions(args.actions, plan)
    environment_source = load_environment(args.environment)
    environment = effective_environment(environment_source, args)
    sensors = args.sensor or ["ld2410c_uart"]
    scenarios = select_scenarios(plan, args.scenario, args.include_optional)
    scenarios = filter_scenarios_for_sensors(
        scenarios, actions, sensors, args.scenario
    )
    if not scenarios:
        raise ihap46.HarnessError("No executable scenarios remain")
    effective_plan = build_effective_plan(plan, scenarios, sensors)

    if args.dry_run:
        print_dry_run(scenarios, actions, environment)
        return

    print(environment_summary(environment))
    print(
        "Press Enter to accept each displayed default, or type a corrected value. "
        "The effective values are stored with the run."
    )
    metadata = collect_operator_metadata(args, environment)
    environment["values"].update(
        {
            "room_id": metadata["room_id"],
            "room_width_m": metadata["room_width_m"],
            "room_depth_m": metadata["room_depth_m"],
            "door_location": metadata["door_location"],
            "mount_height_cm": metadata["mount_height_cm"],
            "mount_orientation": metadata["mount_orientation"],
            "mount_position": metadata["mount_position"],
            "room_notes": metadata["room_notes"],
        }
    )

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
        effective_environment_path = run_dir / "effective-environment.json"
        ihap46.write_json(effective_plan_path, effective_plan)
        ihap46.write_json(effective_environment_path, environment)

        run_metadata = ihap46.load_json(run_dir / "run.json")
        run_metadata.update(
            {
                "selected_sensor_channels": sensors,
                "operator_metadata": metadata,
                "plan_path": str(effective_plan_path),
                "plan_snapshot": effective_plan,
                "environment_path": str(effective_environment_path),
                "environment_snapshot": environment,
                "operator_actions_snapshot": actions,
                "scope": "physical laboratory evidence",
            }
        )
        ihap46.write_json(run_dir / "run.json", run_metadata)
        pending_plan.unlink(missing_ok=True)

        print("\nIHAP-46 — GUIDED PHYSICAL VALIDATION")
        print(f"Run: {args.run_id}")
        print(f"Evaluated channels: {', '.join(sensors)}")
        print(environment_summary(environment))
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
        raise ihap46.HarnessError("Run aborted by operator")
    finally:
        stop_collector(process)
        pending_plan.unlink(missing_ok=True)

    results = ihap46.analyze_run(
        run_dir, run_dir / "effective-test-plan.json"
    )
    ihap46.write_json(run_dir / "results.json", results)
    ihap46.render_report(results, run_dir / "report.html")
    print("\nRUN COMPLETE")
    print(f"Machine-readable results: {run_dir / 'results.json'}")
    print(f"Human-readable report: {run_dir / 'report.html'}")
    print("Do not edit this run. Use a new run ID for any correction or repeat.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Execute reproducible IHAP-46 tests with on-screen instructions."
    )
    parser.add_argument("--port")
    parser.add_argument("--run-id")
    parser.add_argument("--plan", type=Path, default=Path("config/test-plan.json"))
    parser.add_argument("--actions", type=Path, default=DEFAULT_ACTIONS)
    parser.add_argument("--environment", type=Path, default=DEFAULT_ENVIRONMENT)
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
    parser.add_argument("--room-width-m", type=float)
    parser.add_argument("--room-depth-m", type=float)
    parser.add_argument("--door-location")
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
