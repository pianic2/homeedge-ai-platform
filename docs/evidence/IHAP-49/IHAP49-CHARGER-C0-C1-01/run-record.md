# IHAP-49 — Charger Characterization Run C0/C1-01

**Task:** IHAP-49  
**Branch:** `ihap-49-edge-power-subsystem-decision`  
**PR:** #34  
**Date:** 2026-09-07  
**Operator:** Project Owner  
**Board:** owned USB-C 4056E-family charger/protection module

## C0 — R3 / PROG-resistor in-circuit characterization

Board state reported by operator:

- USB source disconnected during resistance measurement;
- battery absent;
- output load absent;
- multimeter manual resistance range: 2 kΩ.

Measured directly across R3 in-circuit:

| Measurement | Reading |
|---|---:|
| R3 pass 1 | 0.814 kΩ |
| R3 pass 2, probes reversed | 0.345 kΩ |

### C0 disposition

**HOLD / INCONCLUSIVE.**

The large polarity-dependent difference is not consistent with treating the in-circuit reading as the standalone resistance of R3. Parallel semiconductor paths through the charger circuitry can influence the multimeter reading. Neither 814 Ω nor 345 Ω is accepted as `RPROG`, and no charge-current value is inferred from these readings.

No desoldering is required at this stage. Actual charge current will be measured later with the selected cell under a controlled charging test.

## C1 — Charger input / unloaded-node sanity

### Attempt A — USB-C to USB-C fast-charge source

Initial attempt used a USB-C-to-USB-C cable and a fast-charge-capable USB-C source. No usable input voltage was observed at the board power input. Early measurements taken from a small USB-C connector contact were discarded because the point was not VBUS.

Disposition: **unsupported / not validated for this board**. The result is consistent with the board not presenting the USB-C sink configuration required for a compliant USB-C source to enable VBUS, but exact CC implementation is not independently traced. No generic claim is made beyond the tested source/cable combination.

### Attempt B — legacy 5 V USB-A source to USB-C cable

Operator changed to an older regulated source rated **5 V / 1.55 A** using a **USB-A-to-USB-C** cable.

Measured with no battery and no output load:

| Measurement | Result |
|---|---:|
| VIN, large board input pads | **4.95 V** |
| B+ to B- | **4.19 V** |
| OUT+ to OUT- | **4.18 V** |

### C1 disposition

**PASS for legacy 5 V input sanity only.**

The owned charger board powers correctly from the tested 5 V / 1.55 A USB-A source through a USB-A-to-USB-C cable. The approximately 4.18–4.19 V unloaded readings on B/OUT are recorded as open-circuit behavior only; they do **not** validate float voltage, charge regulation, charge current, termination, protection thresholds, or suitability for an attached LG INR18650-MJ1 cell.

## Requirements / consequences

1. The charger input reference must not assume generic USB-C-to-USB-C compatibility.
2. Until a different result is demonstrated, the owned charger module shall be treated as requiring a known 5 V source/cable arrangement equivalent to the tested USB-A-to-USB-C legacy supply path.
3. The normal edge-node 5 V USB-C operating source remains a separate subsystem requirement; this result applies specifically to the owned charger module input behavior.
4. Battery connection remains prohibited until received-cell identity/condition, holder fit, and the controlled charging procedure are ready.

## Remaining charger validation

- received LG INR18650-MJ1 identity and condition;
- holder fit/contact-pressure check;
- actual charge current;
- terminal/float voltage with cell attached;
- charge-complete/termination behavior;
- charger/protection thermal behavior;
- low-voltage/protection behavior within safe non-destructive limits.

No safety, certification, USB-C compliance, production-readiness, or autonomy claim is supported by this run.
