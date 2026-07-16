# IHAP-47 — Door State Sensor Evidence

**Issue:** [IHAP-47](https://niccolopiazzi01.atlassian.net/browse/IHAP-47)  
**Decision document:** [`ADR-0002`](../../adr/ADR-0002-mvp-door-state-sensor.md)  
**Evidence owner:** Project Owner  
**Package state:** Prepared for physical execution  
**Repository purpose:** durable summaries, sanitized photographs, structured results and reproducible procedures

<!--
AI_AGENT_METADATA:
  document_type: hardware_evidence_manifest
  issue: IHAP-47
  evidence_scope: owned_mc38_or_dc38_door_contact_specimens
  physical_test_executed: false
  raw_serial_logs_committed: false
  raw_device_identifiers_committed: false
  result_claims_validated: false
  test_protocol: docs/evidence/IHAP-47/test-protocol.md
  validation_harness: tools/hardware-validation/ihap-47-door-state-sensor/
  unvalidated_claim_marker: "[UNVALIDATED]"

HIDDEN_ANTI_REGRESSION_RULES:
  - Do not add a result row before the corresponding artifact exists.
  - Do not commit raw serial logs, device MAC addresses, local paths, private order details or unsanitized domestic photographs.
  - Historical prototype evidence supports feasibility only; it does not qualify the current specimen.
  - Photographs prove visible facts about the photographed specimen only.
  - Physical measurements apply only to the tested specimens and geometry.
  - Preserve [UNVALIDATED] for exact NO/NC behavior, gap, alignment, bounce, replacement reproducibility and final electrical interface until reviewed evidence exists.
-->

## 1. Evidence State

No IHAP-47 physical result has been executed or accepted yet.

The package currently contains:

- the evidence classification rules;
- a summary of historical prototype evidence;
- the controlled physical test protocol;
- the validation harness and local report generator;
- empty result placeholders that must not be interpreted as test evidence.

The owned contact remains a **qualification candidate**. Its exact reed form, activation envelope, bounce behavior and specimen consistency remain `[UNVALIDATED]`.

## 2. Evidence Classification

Every claim must use one of these evidence classes.

| Class | Meaning | Allowed use |
|---|---|---|
| `manufacturer-declared` | Statement from an official manufacturer document for an identified part | Supports that exact identified part and documented conditions only |
| `observed-owned-specimen` | Direct observation or measurement on an identified owned specimen | Supports only the tested specimen, setup and procedure |
| `historical-prototype` | Earlier firmware, logs or photographs not produced under the current protocol | Feasibility and test-design input only |
| `inventory-evidence` | Purchase record, pack quantity, photograph or owner declaration | Supports ownership and historical acquisition only |
| `current-market-evidence` | Dated current listing or distributor record | Supports availability and price only at the recorded date |
| `assumption` | Working hypothesis used to design a test | Must not be stated as a result |
| `[UNVALIDATED]` | Claim not yet backed by sufficient evidence | Must remain visibly marked |

## 3. Historical Prototype Evidence

The Project Owner supplied two private historical artifacts:

- `room-env-node-v06-ld2410c-mc38.c`;
- `monitor.log`.

They are not committed to this repository. The raw log contains unrelated prototype output and device-specific information. Only the minimum non-sensitive summary is recorded here.

| Evidence ID | Classification | Supported observation | Limitation |
|---|---|---|---|
| E-IHAP47-H01 | historical-prototype | Earlier ESP32-C3 firmware configured GPIO6 as an input with the internal pull-up and connected the contact to ground. | GPIO6 is not the final pin decision. The exact board, cable and contact specimen are not established by this summary. |
| E-IHAP47-H02 | historical-prototype | Earlier firmware interpreted a closed electrical contact as `LOW` and an open electrical circuit as `HIGH`. | This is a software convention and observed topology, not proof of the commercial NO/NC designation. |
| E-IHAP47-H03 | historical-prototype | Earlier firmware took three samples approximately 1.2 ms apart and used the majority level. | The method was not a controlled bounce characterization and is not accepted as the final debounce strategy. |
| E-IHAP47-H04 | historical-prototype | Earlier serial telemetry contained both logical open and logical closed states. | It proves only that a transition was observed during that session. It does not prove gap, alignment, reliability or fault detection. |

Historical artifacts must never be presented as evidence that the current physical protocol passed.

## 4. Inventory Evidence

The Project Owner previously reported ownership of ten MC-38 contacts acquired for a total of EUR 5.75, equivalent to EUR 0.575 per contact before assigning wiring and mounting cost.

This is currently an owner-declared historical inventory statement. Receipt, seller, exact listing, lot correspondence, current availability and current replacement price remain `[UNVALIDATED]`.

Future sanitized inventory evidence may be added as:

| Evidence ID | Planned file | Purpose | State |
|---|---|---|---|
| E-IHAP47-I01 | `inventory-pack.jpg` | Show the owned pack and visible labels | Pending |
| E-IHAP47-I02 | `purchase-record-redacted.jpg` | Support historical quantity and price without exposing private data | Pending |

## 5. Physical Evidence Register

Do not mark an item present until the file has been added and its checksum recorded.

| Evidence ID | Planned artifact | Supports | State | SHA-256 |
|---|---|---|---|---|
| E-IHAP47-P01 | `mc38-a-sensor.jpg` | Specimen A visible housing, cable and markings | Pending | — |
| E-IHAP47-P02 | `mc38-a-magnet.jpg` | Specimen A paired magnet | Pending | — |
| E-IHAP47-P03 | `mc38-b-sensor.jpg` | Specimen B visible housing, cable and markings | Pending | — |
| E-IHAP47-P04 | `specimen-comparison.jpg` | Visible comparison between tested specimens | Pending | — |
| E-IHAP47-P05 | `continuity-magnet-far.jpg` | Multimeter setup with magnet outside activation range | Pending | — |
| E-IHAP47-P06 | `continuity-magnet-near.jpg` | Multimeter setup with magnet in the closed-door candidate position | Pending | — |
| E-IHAP47-P07 | `alignment-fixture.jpg` | Measurement geometry used for gap and offset tests | Pending | — |
| E-IHAP47-R01 | `results.json` | Structured physical and electrical observations | Pending | — |
| E-IHAP47-R02 | `summary.json` | Sanitized generated summary | Pending | — |
| E-IHAP47-R03 | `report.html` | Human-readable standalone report | Pending | — |

`serial.log` and `records.jsonl` are intentionally local-only working files and must not be added to this register.

## 6. Supported Claims Before Physical Test

The prepared material supports only these statements:

- a passive two-wire magnetic contact is technically compatible with an ESP32-C3 digital input;
- an earlier prototype used a contact-to-ground topology with the internal pull-up;
- the current test protocol is reproducible and produces structured local evidence;
- the generic MC-38 candidate has not yet been physically qualified under IHAP-47.

## 7. Claims Not Supported Before Physical Test

The package does not currently prove:

- whether the owned contact is Form A/NO, Form B/NC or another arrangement;
- the exact distance at which it operates or releases;
- acceptable lateral or vertical misalignment;
- contact bounce duration;
- cycle reliability;
- adequacy of the ESP32-C3 internal pull-up for the final cable;
- a final external pull resistance;
- distinction between door open and cable disconnected;
- tamper detection;
- current market availability or replacement cost;
- equivalence of other products sold as `MC-38` or `DC-38`;
- production, security, alarm, antifurto, access-control, intrusion-detection, safety or certification maturity.

## 8. Publication and Sanitization Rules

Before committing any photograph or generated result:

1. crop unrelated surroundings;
2. remove EXIF metadata;
3. remove addresses, order numbers, account data and seller-account details;
4. omit ESP32 MAC addresses and unique device identifiers;
5. remove absolute local file-system paths;
6. confirm no private room layout or domestic detail is visible beyond the controlled fixture;
7. do not add, remove or reconstruct hardware details generatively;
8. calculate SHA-256 over the final sanitized repository file;
9. state what the artifact supports and what it does not support.

## 9. Execution Entry Point

Follow:

1. [`test-protocol.md`](test-protocol.md);
2. [`tools/hardware-validation/ihap-47-door-state-sensor/README.md`](../../../tools/hardware-validation/ihap-47-door-state-sensor/README.md).

Stop and request a Project Owner decision if the procedure reveals inconsistent specimens, unstable states, a need for supervised wiring, a new event state or a different sensor technology.
