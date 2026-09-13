# IHAP-55 simulation strategy

The board uses three complementary validation layers.

## 1 — deterministic corner screening

```bash
python3 tools/hardware-validation/ihap-55-mainboard/host/ihap55_contract_check.py
python3 tools/hardware-validation/ihap-55-mainboard/host/ihap55_sim.py
python3 -m unittest discover -s tools/hardware-validation/ihap-55-mainboard/host/tests -v
```

This checks preserved contracts, feedback networks, source/load corners and Accepted steady rail bounds. It deliberately does not pretend to model switching waveforms.

## 2 — vendor switching models

TI publishes the `TPS63802 Unencrypted PSpice Transient Model Package (Rev. C)` (`SLVMCX1C.ZIP`) and the `TLV62568 PSpice Unencrypted Transient Model (Rev. B)` (`SLVMBV4B.ZIP`). KiCad uses ngspice and can load external unencrypted PSpice subcircuits.

Target TPS63802 runs: startup at MP_SYS min/nominal/max; 0.1->0.5 A step; 0.1->1.0 A headroom step; buck/buck-boost/boost transition; undershoot/overshoot/recovery.

Target TLV62568 runs: 5 V startup; 50->250 mA and 50->500 mA steps; tolerance corners; undershoot/overshoot.

Vendor files are not redistributed in this repository. Put locally downloaded files under `simulation/vendor-models/` and bind them to the corresponding KiCad symbols.

The exact TI package URLs, SHA-256 checksums and internal `.LIB` paths are pinned in `vendor-model-manifest.json`. Run `python3 fetch_vendor_models.py` to download and verify them into `vendor-models/`. From this directory, with ngspice 44.2 and PSpice compatibility enabled by `.spiceinit`, run:

```bash
ngspice -b -o tps63802-startup-step.log tps63802-startup-step.cir
ngspice -b -o tlv62568-startup-step.log tlv62568-startup-step.cir
```

The transient netlists are vendor-model experiments, not complete power-path simulation. A process exit alone is not a PASS: inspect measured rail values against the circuit's expected steady and transient envelopes. A package-extracted ngspice also needs its matching XSPICE code-model libraries loaded; the normal Debian installation does this from `spinit`.

The 2026-09-12 ngspice 44.2 experiments did **not** qualify either regulator model: TPS63802 returned a negative output with exit 0, TLV62568 returned a negative output with exit 0 in the initial run and the startup retry did not finish in a practical time. See `docs/evidence/IHAP-55/simulation-summary.md`. Treat these netlists as diagnostic starting points until a supported model integration produces plausible measured waveforms.

## 3 — MP2636/full-system

MPS documents MPSmart as its SIMetrix/SIMPLIS environment and states that most MPS IC models are SIMPLIS models. Use an exact MP2636 model there if exposed by the installed MPS model library. Otherwise the repository retains a bounded system behavioral model plus mandatory physical validation rather than inventing a switching model.

Physical V1–V12 validation from the IHAP-49 plan remains mandatory after fabrication.

## Evidence boundary

Simulation validates the modeled circuit, not assembly, real parasitics, connector polarity, battery safety, RF, actual thermal behavior or transfer performance. Those remain `[UNVALIDATED]` until measured.
