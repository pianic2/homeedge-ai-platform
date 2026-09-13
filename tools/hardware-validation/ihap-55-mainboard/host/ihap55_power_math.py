#!/usr/bin/env python3
"""Revision-A component equations and bounded design arithmetic, not simulation."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
CONTRACT = ROOT / "hardware/edge-mainboard/schematic-contract.json"


def feedback(vref: float, top: float, bottom: float) -> float:
    return vref * (1 + top / bottom)


def feedback_corners(vref_low: float, vref_high: float, top: float,
                     bottom: float, resistor_tolerance: float) -> tuple[float, float]:
    t = resistor_tolerance / 100
    return (
        feedback(vref_low, top * (1 - t), bottom * (1 + t)),
        feedback(vref_high, top * (1 + t), bottom * (1 - t)),
    )


def main() -> None:
    c = json.loads(CONTRACT.read_text())
    mp = c["power"]["charger"]
    tps = c["power"]["post_5v"]
    tlv = c["power"]["reg_3v3"]
    f5, f3 = tps["feedback"], tlv["feedback"]
    adc = c["health_monitor"]["channels"]["AIN0"]["divider"]
    top, bottom = adc["top_ohm"], adc["bottom_ohm"]
    adc_input_impedance = 6_000_000  # TI TLA2024 typical at +/-4.096 V FSR
    loaded_bottom = 1 / (1 / bottom + 1 / adc_input_impedance)
    nominal_ratio = bottom / (top + bottom)
    loaded_ratio = loaded_bottom / (top + loaded_bottom)
    result = {
        "schema": "ihap55.power-math.v1",
        "classification": "static calculation; conditional assumptions are not physical validation",
        "mp2636": {
            "charge_current_nominal_a": 2400 / (mp["riset_kohm"] * mp["rsense_mohm"]),
            "boost_sys_nominal_v": feedback(mp["boost_feedback"]["vref_v"],
                                            mp["boost_feedback"]["r_top_kohm"],
                                            mp["boost_feedback"]["r_bottom_kohm"]),
            "input_limit_candidate_30k1_nominal_a": 43.3 / 30.1 - 0.05,
            "input_limit_30k1_status": "candidate only; min/max and USB power budget unresolved",
            "boost_rolim_sensitivity": {
                "220k8_nominal_a": 2400 * 0.92 / (220.8 * 20),
                "110k4_nominal_a": 2400 * 0.92 / (110.4 * 20),
                "90k3_nominal_a": 2400 * 0.92 / (90.3 * 20),
                "status": "220k8 rejected against product target; 110k4 and 90k3 candidates only",
            },
        },
        "tps63802": {
            "sys5_nominal_v": feedback(f5["vref_nom_v"], f5["r_top_kohm"],
                                       f5["r_bottom_kohm"]),
            "feedback_only_corner_v": feedback_corners(
                f5["vref_nom_v"] * (1 - f5["vref_tol_pct"] / 100),
                f5["vref_nom_v"] * (1 + f5["vref_tol_pct"] / 100),
                f5["r_top_kohm"], f5["r_bottom_kohm"], f5["tolerance_pct"]),
            "output_power_0p5a_w": 5 * 0.5,
            "loss_if_90pct_efficiency_w": 5 * 0.5 * (1 / 0.90 - 1),
            "efficiency_note": "90% is a sensitivity assumption, not a guaranteed datasheet limit",
        },
        "tlv62568": {
            "sys3_nominal_v": feedback(0.6, f3["r_top_kohm"], f3["r_bottom_kohm"]),
            "feedback_only_corner_v": feedback_corners(
                f3["vref_range_v"][0], f3["vref_range_v"][1],
                f3["r_top_kohm"], f3["r_bottom_kohm"], f3["tolerance_pct"]),
            "output_power_0p5a_w": 3.3 * 0.5,
            "loss_if_90pct_efficiency_w": 3.3 * 0.5 * (1 / 0.90 - 1),
        },
        "tla2024": {
            "divider_nominal_ratio": nominal_ratio,
            "divider_loaded_ratio_typical": loaded_ratio,
            "divider_loading_error_pct_typical": 100 * (loaded_ratio / nominal_ratio - 1),
            "rail_lsb_v_at_4p096_fsr": 2 * 4.096 / 2048,
            "ain_at_vbus_5p25_v": 5.25 * nominal_ratio,
            "unpowered_ain_absolute_max_v": 0.3,
            "unpowered_input_status": "FAIL: VBUS divider drives AIN above VDD+0.3 V when VDD=0",
        },
        "i2c": {
            "assumed_bus_capacitance_pf": 200,
            "rise_4k7_200pf_us": 0.8473 * 4700 * 200e-12 * 1e6,
            "rise_10k_200pf_us": 0.8473 * 10000 * 200e-12 * 1e6,
            "capacitance_status": "assumption pending actual module and cable measurement",
        },
        "dht": {
            "effective_4k7_module_plus_5k1_board_ohm": 1 / (1 / 4700 + 1 / 5100),
            "board_pullup_status": "DNP pending module measurement",
        },
    }
    assert abs(result["mp2636"]["charge_current_nominal_a"] - 1) < 1e-9
    assert abs(result["mp2636"]["boost_rolim_sensitivity"]["220k8_nominal_a"] - 0.5) < 1e-9
    assert abs(result["mp2636"]["boost_rolim_sensitivity"]["110k4_nominal_a"] - 1.0) < 1e-9
    assert 1.2 < result["mp2636"]["boost_rolim_sensitivity"]["90k3_nominal_a"] < 1.3
    assert abs(result["tps63802"]["sys5_nominal_v"] - 5) < 1e-9
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
