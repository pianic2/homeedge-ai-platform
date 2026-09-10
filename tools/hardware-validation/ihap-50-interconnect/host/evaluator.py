from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

EXPECTED_PINS = {
    "radar_rx": 0,
    "radar_tx_service": 1,
    "door": 3,
    "dht": 4,
    "adc_spare": 5,
    "i2c_sda": 6,
    "i2c_scl": 7,
    "digital_spare": 10,
}


@dataclass(frozen=True)
class GateResult:
    passed: bool
    checks: dict[str, bool]
    errors: list[str]


def _ratio(items: Iterable[dict], key: str) -> float:
    values = list(items)
    if not values:
        return 0.0
    return sum(1 for item in values if item.get(key) is True) / len(values)


def evaluate_boot(boot: dict, profile: str) -> GateResult:
    expected_bme = profile == "precision"
    checks = {
        "record_type": boot.get("record_type") == "boot",
        "firmware": boot.get("firmware") == "ihap50-integrated-interconnect-harness",
        "pins": boot.get("pins") == EXPECTED_PINS,
        "adc_spare": boot.get("adc_spare_pull_test") is True,
        "digital_spare": boot.get("digital_spare_pull_test") is True,
        "radar_service_tx_disabled": boot.get("radar_tx_service_configured") is False,
        "profile": boot.get("detected_profile") == profile,
        "bme_presence": boot.get("bme280_present") is expected_bme,
        "oled_visual_transfer": boot.get("oled_visual_transfer_ok") is True,
    }
    errors = [name for name, ok in checks.items() if not ok]
    return GateResult(not errors, checks, errors)


def evaluate_samples(samples: list[dict], profile: str, min_samples: int = 6) -> GateResult:
    checks: dict[str, bool] = {
        "sample_count": len(samples) >= min_samples,
        "oled_reliability": _ratio(samples, "oled_ok") >= 0.80,
        "radar_freshness": _ratio(samples, "radar_fresh") >= 0.75,
    }

    if samples:
        final = samples[-1]
        valid_frames = int(final.get("radar_valid_frames", 0) or 0)
        invalid_frames = int(final.get("radar_invalid_frames", 0) or 0)
        checks["radar_valid_frames"] = valid_frames > 0
        checks["radar_no_invalid_frames"] = invalid_frames == 0
        checks["profile_consistency"] = all(s.get("profile") == profile for s in samples)
    else:
        checks["radar_valid_frames"] = False
        checks["radar_no_invalid_frames"] = False
        checks["profile_consistency"] = False

    if profile == "standard":
        checks["bme_absent"] = all(s.get("bme280_present") is False for s in samples)
        checks["dht11_reliability"] = _ratio(samples, "dht11_ok") >= 0.75
    elif profile == "precision":
        checks["bme_present"] = all(s.get("bme280_present") is True for s in samples)
        checks["bme280_reliability"] = _ratio(samples, "bme280_ok") >= 0.80
        checks["bme280_identity"] = all(s.get("bme280_chip_id") == "0x60" for s in samples)
    else:
        checks["known_profile"] = False

    errors = [name for name, ok in checks.items() if not ok]
    return GateResult(not errors, checks, errors)


def evaluate_door_phase(samples: list[dict], expected_raw: int, phase: str) -> GateResult:
    checks = {
        f"{phase}_sample_count": len(samples) >= 2,
        f"{phase}_door_raw": len(samples) >= 2
        and all(int(s.get("door_raw", -1)) == expected_raw for s in samples),
        f"{phase}_radar_alive": len(samples) >= 2
        and any(s.get("radar_fresh") is True for s in samples),
        f"{phase}_oled_alive": len(samples) >= 2
        and all(s.get("oled_ok") is True for s in samples),
    }
    errors = [name for name, ok in checks.items() if not ok]
    return GateResult(not errors, checks, errors)


def combine(*results: GateResult) -> GateResult:
    checks: dict[str, bool] = {}
    errors: list[str] = []
    for result in results:
        checks.update(result.checks)
        errors.extend(result.errors)
    return GateResult(not errors, checks, errors)
