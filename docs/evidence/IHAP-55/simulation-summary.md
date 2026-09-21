# IHAP-55 simulation evidence — 2026-09-12

Input baseline HEAD `f5c94a2429f27e88161305896eb5fb85566dd636` plus the IHAP-55 simulation files committed as `8bd0fc8`. The TI archives were fetched from the official URLs and SHA-256 verified by `python3 hardware/edge-mainboard/simulation/fetch_vendor_models.py`; exact hashes and model versions are in `hardware/edge-mainboard/simulation/vendor-model-manifest.json`. Vendor libraries are Git-ignored.

| Gate | Executed command / tool | Exit | Result |
|---|---|---:|---|
| Contract | `python3 tools/hardware-validation/ihap-55-mainboard/host/ihap55_contract_check.py` / Python 3.13.5 | 0 | PASS — contract JSON checks; does not validate a schematic |
| Behavioral | `python3 tools/hardware-validation/ihap-55-mainboard/host/ihap55_sim.py` | 0 | PASS — 28/28 deterministic screening cases; efficiencies and pass-through drops are assumed |
| Static math | `python3 tools/hardware-validation/ihap-55-mainboard/host/ihap55_power_math.py` | 0 | PASS — arithmetic execution; explicitly reports unsafe unpowered ADC input |
| Host tests | `python3 -m unittest discover -s tools/hardware-validation/ihap-55-mainboard/host/tests -v` | 0 | PASS — 12/12 |
| Vendor TPS63802 | ngspice 44.2 with TI `TPS63802_TRANS.LIB`, PSpice compatibility, `tps63802-startup-step.cir` | 0 | **FAIL — model experiment not valid:** final average VOUT = −0.578 V despite 5.184 V input; 441,928 rows, 1048.92 s. A process exit is not a SPICE PASS. |
| Vendor TLV62568 | ngspice 44.2 with TI `TLV62568_TRANS.LIB`, initial 5 V fixed-source transient | 0 | **FAIL — model experiment not valid:** final average VOUT = −0.083 V, not 3.318 V. |
| Vendor TLV62568 retry | rising-source/startup transient with `tlv62568-startup-step.cir` | 143 | **INCOMPLETE:** stopped only the exact ngspice process after >15 minutes without terminal measures. |
| MP2636 | Official exact-model availability reviewed | n/a | No accessible exact vendor switching model obtained; no substitute is called physical switching simulation. |

The TPS and TLV subcircuits are published as unencrypted PSpice packages, but their observed ngspice outputs are nonphysical under the current wrappers/compatibility layer. Pin order was taken from each `.SUBCKT` declaration; the discrepancy requires model integration diagnosis or a supported PSpice/SIMPLIS run. **No vendor switching-SPICE PASS is claimed.** The committed netlists are reproducible starting points, not qualifying results. The local extracted ngspice package required its XSPICE code-model libraries loaded explicitly because it lacked a system-installed `spinit`; a normal package installation loads those libraries automatically. The raw `.log` files remain ignored locally.

Not covered by any valid switching model: USB/battery transfer waveform, 1 A headroom, startup overshoot/undershoot, rail settling, thermal response, efficiency/corner sensitivity, source current limit or cell protection. These remain `[UNVALIDATED]`; the 28/28 behavioral sweep cannot close them.

## Current software-gate rerun — 2026-09-20

Input HEAD: `d070e5aacbeaebc5a7ab6da1edd006adfdf7a238`.

Executed from repository root:

```bash
python3 tools/hardware-validation/ihap-55-mainboard/host/ihap55_contract_check.py
python3 tools/hardware-validation/ihap-55-mainboard/host/ihap55_sim.py
python3 tools/hardware-validation/ihap-55-mainboard/host/ihap55_power_math.py
python3 -m unittest discover -s tools/hardware-validation/ihap-55-mainboard/host/tests -v
```

Results: contract checker exit 0 / PASS; behavioral simulation exit 0 / 28 of 28 PASS; static power arithmetic exit 0 / PASS with the known unpowered-TLA2024 input failure reported; host tests exit 0 / 12 of 12 PASS. These fresh software/static results do not change the SPICE, ERC, DRC or physical-validation classifications above.
