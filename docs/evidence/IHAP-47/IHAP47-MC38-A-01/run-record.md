# IHAP-47 MC38-A Guided Validation Run Record

## Run identity

- Evidence ID: `IHAP47-MC38-A-01`
- Source session: `20260901T113516Z`
- Specimen: `MC38-A`
- Execution mode: guided low-touch
- Date: 2026-09-01
- Firmware sampling period: `250 us`
- Stable-state window: `150 ms`
- Requested complete cycles: `20`
- Raw `serial.log` and `records.jsonl`: preserved locally, not committed
- Project Owner decision: **Accepted — 2026-09-01**

## Sanitization review

The supplied generated artifacts were reviewed before publication.

- no MAC address is present in the publication summary;
- no serial-port path is present;
- no absolute local file-system path is present;
- no account, order, address or private-room information is present;
- raw serial/device logs remain local;
- the generated HTML report is retained locally because it duplicates the reviewed summary and is not required for the decision gate.

Two later Project Owner photographs were also reviewed: no EXIF metadata or visible sensitive/account/device-identifier information was found. They support visible specimen form only; they do not establish supplier or manufacturer identity.

## Electrical mapping

| Condition | Observed raw level | Electrical state | Result |
|---|---:|---|---|
| Magnet FAR | `1` | open | PASS |
| Magnet NEAR | `0` | closed | PASS |

For the tested specimen this is consistent with Form A / normally-open behavior relative to magnetic actuation.

This statement applies only to `MC38-A`; it does not override or generalize seller terminology for other products sold as MC-38/DC-38.

## Automated repeated-cycle gate

- complete cycles: **20/20**;
- stable movements: **40/40**;
- mismatches: **0**;
- buffer overflows: **0**;
- movements with more than one observed raw transition: **0/40**;
- maximum observed multi-transition span: **0 us** because no multiple transition was observed;
- gate result: **PASS**.

The raw sampling period was `250 us`. Therefore the supported claim is limited to: no additional transition was observed at that harness sampling resolution. This is not an oscilloscope-grade proof that physical contact bounce cannot occur.

## Failure-mode gate

| Controlled case | Observed raw level | Result |
|---|---:|---|
| One contact conductor disconnected while a closed contact was expected | `1` | PASS |
| GPIO6 connected to GND in the low-voltage bench check | `0` | PASS |

Required architectural conclusion:

> Under the tested simple two-wire pull-up topology, a legitimate open electrical contact and an interrupted conductor are electrically indistinguishable.

No tamper, supervised-loop or fault-distinction capability is claimed.

## Internal pull-up bench observation

The internal ESP32-C3 pull-up was stable for the complete guided run:

- deterministic FAR/NEAR mapping;
- 40/40 stable movements;
- zero unexplained mismatches;
- zero overflow;
- no instability preventing the stable-state gate.

Result: **PASS for the temporary bench setup only**.

The final pull network remains IHAP-50 scope. Quantitative current impact remains IHAP-49 scope.

## Decision review

The physical evidence supports the IHAP-47 sensor-technology decision gate:

- passive wired reed-contact operation: PASS;
- tested owned specimen deterministic: PASS;
- repeated operation sufficient for MVP selection evidence: PASS;
- failure-mode limitation explicitly demonstrated: PASS;
- temporary bench topology stable: PASS.

Overall evidence classification: **PASS — observed owned specimen**.

The Project Owner explicitly accepted ADR-0003 on **2026-09-01**, accepting passive wired two-conductor magnetic reed-contact technology for MVP binary door-state telemetry and `MC38-A` as the tested local reference specimen.

## Explicit claim boundary

This run does **not** establish:

- universal MC-38/DC-38 characteristics;
- cross-lot or replacement equivalence;
- production or industrial reliability;
- final mounting gap or alignment tolerance;
- final GPIO, debounce, cable, connector, ESD/protection or pull resistor;
- power/autonomy;
- alarm, antifurto, intrusion-detection, access-control, tamper, safety or certification capability.

Mounting geometry belongs to IHAP-51. Integrated electrical design belongs to IHAP-50. Power impact belongs to IHAP-49.
