# IHAP-49 — Final Review Checklist

**Status:** Project Owner accepted ADR-0007 / PR #34 on 2026-09-07

## Architecture decision

- [x] Normal source frozen: regulated 5 V USB-C.
- [x] Battery role frozen: 1S rechargeable backup only.
- [x] Multi-day standalone operation explicitly excluded from MVP requirement.
- [x] Exact reference cell selected: LG INR18650-MJ1 / EAN 8438493099829.
- [x] Cost-first rule recorded after minimum technical/provenance gates.
- [x] Final hardware direction frozen: one modular custom core PCB.
- [x] Preferred first integrated PMIC direction frozen: MP2636GR-P.
- [x] ETA9740 retained as future cost-down alternative.

## Electrical contract

- [x] USB-C 5 V only; no PD requirement.
- [x] Correct Type-C sink termination required.
- [x] Reference input >=1.5 A available/advertised.
- [x] 4.2 V battery CV target frozen.
- [x] ~1.0 A nominal charge target frozen.
- [x] NTC battery-temperature monitoring required.
- [x] 5.0 V SYS target frozen.
- [x] >=0.5 A continuous and >=1.0 A transient/headroom target frozen.
- [x] Automatic USB-priority battery takeover required.
- [x] Backfeed into upstream USB prohibited.
- [x] No-reset transfer defined as target; remains `[UNVALIDATED]` until IHAP-55.
- [x] System-level protection required for unprotected MJ1.
- [x] Reverse-cell risk explicit.

## Owned hardware evidence

- [x] 4056E charger marking observed.
- [x] 8205A dual MOSFET observed.
- [x] Separate protection controller observed; exact identity remains `[UNVALIDATED]`.
- [x] R3 in-circuit measurement recorded as inconclusive rather than forced.
- [x] Legacy 5 V USB-A-to-C input sanity recorded.
- [x] USB-C-to-USB-C limitation recorded.
- [x] Owned 4056E breakout explicitly rejected as final reference implementation.
- [x] Existing holder retained as candidate; final fit handed downstream.

## Procurement / cost

- [x] LG MJ1 purchase remains justified because cell persists in final design.
- [x] No new holder purchase required now.
- [x] TPS61023/TPS2116 breakout purchases removed from final-architecture plan.
- [x] Additional redundant charger/boost/mux purchases require a specific blocker.
- [x] MP2636 current supplier price snapshot recorded as planning evidence.
- [x] Final board-level replication cost explicitly deferred to IHAP-55 BOM/fabrication evidence.

## Architecture regression

- [x] ESP32-C3 compute decision preserved.
- [x] LD2410C remains on 5 V and externally modular.
- [x] DHT11/BME280 profile distinction preserved.
- [x] Passive reed decision preserved.
- [x] Local OLED decision preserved.
- [x] Audio remains excluded.
- [x] IHAP-50 owns connection matrix.
- [x] IHAP-55 owns custom PCB implementation/validation.
- [x] IHAP-51 owns enclosure/mounting/serviceability.

## Evidence / claim boundary

- [x] Autonomy arithmetic remains `[UNVALIDATED]` until measured downstream.
- [x] No `safe`, `certified`, `fire-safe`, `compliant`, `production-ready` or equivalent unsupported claim.
- [x] Physical charge/thermal/switchover/runtime tests remain mandatory in IHAP-55.
- [x] Downstream physical evidence may supersede ADR-0007 rather than silently weaken requirements.

## Final approval

- [x] Project Owner explicitly accepted ADR-0007 on 2026-09-07.
- [x] Project Owner explicitly approved PR #34 on 2026-09-07.
- [x] Merge authorized.
- [x] Jira IHAP-49 completion authorized after successful merge.
