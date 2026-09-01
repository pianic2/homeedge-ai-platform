# IHAP-47 — Door State Sensor Evidence

**Issue:** [IHAP-47](https://niccolopiazzi01.atlassian.net/browse/IHAP-47)  
**Decision document:** [`ADR-0003`](../../adr/ADR-0003-mvp-door-state-sensor.md)  
**Evidence owner:** Project Owner  
**Package state:** Physical execution complete; evidence reviewed; ADR accepted  
**Default runner:** [`guided_run.py`](../../../tools/hardware-validation/ihap-47-door-state-sensor/scripts/guided_run.py)

<!--
AI_AGENT_METADATA:
  document_type: hardware_evidence_manifest
  issue: IHAP-47
  evidence_scope: owned_mc38_door_contact_specimen
  physical_test_executed: true
  reviewed_evidence_id: IHAP47-MC38-A-01
  tested_specimen: MC38-A
  physical_gate: PASS
  project_owner_decision: accepted_2026-09-01
  raw_serial_logs_committed: false
  raw_device_identifiers_committed: false
  acquisition_evidence_level: E1
  acquisition_supplier: Mega Semiconductor CO., Ltd.
  acquisition_date: 2026-06-18
  acquisition_pack: 10_pairs
  acquisition_total_eur: 7.19
  normalized_unit_price_eur_per_pair: 0.7190
  shipping_eur: 0.00
  test_protocol: docs/evidence/IHAP-47/test-protocol.md
  validation_harness: tools/hardware-validation/ihap-47-door-state-sensor/
  unvalidated_claim_marker: "[UNVALIDATED]"

HIDDEN_ANTI_REGRESSION_RULES:
  - Treat IHAP47-MC38-A-01 as evidence for MC38-A only.
  - Do not infer universal MC-38/DC-38 specifications or replacement equivalence.
  - Do not commit serial.log, records.jsonl, MAC addresses, serial-port paths or local absolute paths.
  - Do not introduce alarm, tamper, intrusion, access-control, safety or certification claims.
  - Final GPIO, pull network, cable and debounce remain IHAP-50.
  - Final mounting geometry remains IHAP-51.
  - Quantitative power impact remains IHAP-49.
  - Acquisition supplier/price evidence does not establish a controlled manufacturer part number.
-->

## 1. Reviewed Physical Result

Canonical reviewed evidence:

- [`IHAP47-MC38-A-01/run-record.md`](IHAP47-MC38-A-01/run-record.md)
- [`IHAP47-MC38-A-01/summary.json`](IHAP47-MC38-A-01/summary.json)

Source local session: `20260901T113516Z`.

Result for owned specimen `MC38-A`:

| Gate | Result |
|---|---|
| FAR electrical mapping | PASS — raw `1`, electrical open |
| NEAR electrical mapping | PASS — raw `0`, electrical closed |
| Automated repeated cycles | PASS — 20/20 complete cycles, 40/40 stable movements |
| Mismatches | `0` |
| Buffer overflows | `0` |
| Movements with >1 observed raw transition | `0/40` at `250 us` sampling |
| One conductor disconnected | raw `1` |
| GPIO6 to GND bench check | raw `0` |
| Internal pull-up adequacy | PASS for this temporary bench session |
| Overall IHAP-47 physical decision gate | **PASS** |
| Project Owner decision | **Accepted — 2026-09-01** |

The observed FAR/NEAR behavior is consistent with **Form A / normally open relative to magnetic actuation** for `MC38-A`.

## 2. Evidence Classification

The reviewed result is `observed-owned-specimen`.

It supports the tested specimen, setup and session only. It does not establish a controlled manufacturer part number, lot equivalence, universal MC-38/DC-38 behavior, production reliability or replacement reproducibility.

Historical prototype evidence remains feasibility-only.

## 3. Decision-Relevant Limitation

The failure-mode test demonstrated:

> Under the tested simple two-wire pull-up topology, a legitimate open electrical contact and an interrupted conductor are electrically indistinguishable.

Therefore this topology provides binary electrical telemetry only. It does not provide wire supervision, tamper detection or a fault-distinct state.

## 4. Raw Evidence Preservation

The guided runner produced local raw evidence including:

- `serial.log`;
- `records.jsonl`;
- runner-generated observations;
- session metadata;
- generated report artifacts.

`serial.log` and `records.jsonl` remain local until IHAP-47 closure. They are intentionally not committed.

The generated HTML report was reviewed but is not published because the reviewed run record and compact summary contain the decision-relevant evidence without duplicating 40 capture rows.

## 5. Published Evidence Register

| Evidence ID | Artifact | Supports | State | SHA-256 |
|---|---|---|---|---|
| E-IHAP47-R01 | `IHAP47-MC38-A-01/run-record.md` | Human-readable reviewed physical run and claim boundary | Reviewed | `711ffa5ab799c31af1910d22deec273679608bbe1629f583d8373ae52aceaa04` |
| E-IHAP47-R02 | `IHAP47-MC38-A-01/summary.json` | Machine-readable reviewed decision summary | Reviewed | `63fcad134fe0c97b2ee1247f4678f77c3635a7f2d28f3eea6f187146c12a4b5d` |

### 5.1 Published photograph evidence

The Project Owner supplied two photographs on 2026-09-01. Sanitization review found no EXIF metadata and no visible account, order, address, device identifier or sensitive private-room information. Repository copies were verified after publication; their SHA-256 values match the reviewed source files.

| Evidence ID | Repository artifact | Supports | State | SHA-256 |
|---|---|---|---|---|
| E-IHAP47-P01 | [`IHAP47-MC38-A-01/photo-overview.jpg`](IHAP47-MC38-A-01/photo-overview.jpg) | Visible owned sensor/magnet pair and wired sensor housing | Reviewed / Published | `c52db2c54c42e8f82ea034b63360c70103963365c196129d0e8035babc23d4dd` |
| E-IHAP47-P02 | [`IHAP47-MC38-A-01/photo-mounting.jpg`](IHAP47-MC38-A-01/photo-mounting.jpg) | Visible sensor housing, paired magnet and mounting openings/geometry | Reviewed / Published | `7739c9b5ab223a8d959d84329c51ddd3ccdfae87085337fa8363446f6ae2ca0d` |

The photographs do **not** prove supplier, manufacturer, commercial listing, exact reed internals or replacement equivalence. No readable controlled manufacturer marking is established by these images.

## 6. Inventory and Procurement Context

The strongest available acquisition evidence is the E1 order evidence already recorded under IHAP-17. It supersedes an earlier owner-declared historical price used in an older IHAP-47 draft.

| Field | Verified acquisition evidence |
|---|---|
| Item | MC-38 magnetic contacts |
| Supplier | **Mega Semiconductor CO., Ltd.** |
| Order state/date | Closed order, **2026-06-18** |
| Purchased quantity | **1 pack / 10 pairs** |
| Total product price | **EUR 7.19** |
| Normalized acquisition price | **EUR 0.7190 per pair** |
| Shipping | **EUR 0.00** |
| BOM acquisition evidence level | **E1** |
| Reference MVP quantity | **1 pair** |

The earlier owner-declared value `EUR 5.75 / EUR 0.575 per contact` is not used as the canonical BOM value because the dated closed-order evidence above is stronger and directly traceable.

Still `[UNVALIDATED]`:

- controlled manufacturer and manufacturer part number;
- current replacement-market price and availability;
- cross-lot or cross-seller equivalence;
- whether another product marketed as `MC-38` or `DC-38` behaves identically.

These gaps do not block use of the already-owned tested local specimen. A controlled fallback SKU is needed only if replacement reproducibility becomes a project requirement.

## 7. Claims Supported After Review and Acceptance

The evidence supports:

- passive two-wire reed-contact behavior on the tested specimen;
- deterministic FAR=open/raw `1` and NEAR=closed/raw `0` mapping;
- 20 complete near/far cycles without stable-state mismatch;
- no additional transition observed in 40 movements at the `250 us` harness sampling resolution;
- explicit open-circuit/disconnected-wire ambiguity;
- temporary internal pull-up adequacy for this bench run;
- suitability of passive wired magnetic reed-contact technology for MVP binary door-state telemetry;
- `MC38-A` as the accepted tested local reference specimen;
- one reference-MVP BOM pair with E1 historical acquisition price evidence of EUR 0.7190/pair.

## 8. Claims Not Supported

The package does not support:

- universal activation distance or alignment tolerance;
- universal MC-38/DC-38 NO/NC behavior;
- replacement or cross-lot equivalence;
- industrial or production reliability;
- oscilloscope-grade bounce characterization;
- final GPIO, pull resistor, cable, connector or protection circuit;
- final mounting geometry;
- power/autonomy;
- tamper, alarm, antifurto, intrusion-detection, access-control, safety or certification maturity.

## 9. Downstream Ownership

- **IHAP-50:** final GPIO, pull network, cable/interface behavior and production debounce.
- **IHAP-49:** quantitative power/current impact.
- **IHAP-51:** mounting gap, alignment margin, attachment and enclosure integration.
- **IHAP-17 / IHAP-43:** propagate the accepted component decision into the canonical BOM/baseline; controlled replacement evidence only if required.

## 10. Execution Entry Point

The normal procedure is the lean automated workflow in [`test-protocol.md`](test-protocol.md) using `scripts/guided_run.py`.

Manual JSON entry is diagnostic-only and must not be reintroduced as the default operator workflow.
