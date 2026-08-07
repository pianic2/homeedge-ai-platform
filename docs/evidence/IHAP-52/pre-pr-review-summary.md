# IHAP-52 — Specialist Pre-PR Review Summary

**Review target:** `ihap-52-central-node-hardware-decision`  
**Base:** `main` at `d5e0b5648a2362385014241d50b950a1e8286417`  
**Review stage:** pre-PR, before physical Raspberry Pi validation  
**Decision authority:** advisory reviewers only; Project Owner retains ADR acceptance, Jira transition and merge authority.

## Severity model

`BLOCKER` > `MAJOR` > `MINOR` > `NOTE`

## Review result

No open `BLOCKER` or `MAJOR` finding remains after the pre-PR corrections recorded below.

Physical Raspberry Pi 4 evidence is intentionally still pending. Therefore:

- ADR-0003 remains `Proposed`;
- Raspberry Pi 4 remains the approved reference/validation candidate, not yet `Community validated`;
- IHAP-52 must not be treated as complete;
- final workload sufficiency, microSD endurance and AI acceleration remain `[UNVALIDATED]`.

## Architecture Regression Reviewer

**Result:** PASS with NOTE

Checks:

- central-node hardware remains separate from ESP32-C3 edge-node decisions;
- target `services/*` directories are not used as runtime/resource evidence;
- Docker, Alpine Linux, database, Kafka, orchestration and final deployment topology are not accepted by ADR-0003;
- cloud-only runtime is not substituted for the local central-node boundary;
- ARM64 and x86_64 remain permitted to avoid unnecessary Raspberry Pi vendor lock-in;
- GPIO is explicitly not a central-node requirement.

**NOTE:** Future Infrastructure-as-Code portability is recorded as an architectural constraint only. No IaC implementation is claimed by IHAP-52.

## Hardware Compatibility Reviewer

**Result:** PASS with NOTE

Checks:

- Raspberry Pi 4 manufacturer capabilities are separated from HomeEdge measured evidence;
- Pi 4 >=4 GB, 64 GB A2 microSD and Wi-Fi match the Project Owner decision;
- Ethernet remains optional;
- PSU requirement is separated into a vendor-neutral stable-supply contract plus Raspberry Pi 4 reference guidance;
- fan/heatsinks remain optional but recommended, not falsely required by an unmeasured workload;
- Pi 5 remains a newer compatible/recommended candidate without a false HomeEdge validation claim;
- Pi 3 B+ and Zero 2 W are closed proportionately because their documented RAM falls below the accepted minimum;
- x86_64 mini-PC and reused-computer paths remain available when the minimum profile is met.

**NOTE:** The Linux graphics/compute-device requirement establishes only hardware presence. VideoCore VI AI suitability remains `[UNVALIDATED]` and must be handled by later AI/runtime work.

## Testing & Evidence Reviewer

**Result:** PASS after one MINOR correction; physical evidence gate pending

### Closed MINOR — thermal acceptance wording

Initial validation-plan wording risked deriving a CPU-temperature acceptance threshold from manufacturer operating-temperature material. The plan was corrected so that the automated gate relies on observable stability/current throttling state, while temperature samples are reviewed together with ambient conditions, enclosure and cooling configuration.

### Closed MINOR — storage integrity check

The storage smoke test initially verified byte counts and cleanup only. The harness now computes deterministic write/read SHA-256 values and requires a matching hash in addition to equal byte counts and temporary-file removal.

### Remaining evidence boundary

The harness itself has been software-sanity checked, but the required physical Raspberry Pi 4 run has not yet been executed by the Project Owner. This is not a documentation defect; it is the planned evidence gate before community-validation/ADR acceptance.

## Security & Privacy Reviewer

**Result:** PASS with NOTE

Checks:

- the harness does not require Internet connectivity;
- Wi-Fi credentials and SSID are not collected;
- assigned IP addresses are reduced to presence/family evidence rather than written verbatim;
- hostname and username are not intentionally collected;
- optional ping is restricted by documentation to an authorized local host;
- raw run output remains ignored/local until review and sanitization;
- no security-appliance, hardened, high-availability or certified claim is introduced.

**NOTE:** `lsblk` may expose local storage model metadata. Raw output must therefore remain subject to the documented pre-publication review.

## Cost Governance Reviewer

**Result:** PASS with NOTE

Checks:

- already-owned Raspberry Pi 4 8 GB is recorded as `unknown/pre-owned`, not EUR 0;
- acquisition context is separated from contributor replication cost;
- current prices are explicitly dated snapshots rather than guarantees;
- cooling/enclosure package cost is not frozen before a reproducible package is selected;
- final BOM propagation is deferred to IHAP-17/IHAP-43 after Project Owner acceptance.

**NOTE:** The Raspberry Pi 4 4 GB supplier snapshot currently used for cost context was unavailable/out-of-stock when checked. Price and availability must be refreshed before final IHAP-17 propagation.

## Source of Truth Guardian

**Result:** PASS

Checks:

- ADR, comparison, assumptions, validation plan and harness live in GitHub;
- Jira records the active workflow state and Project Owner decision evidence;
- no long-form technical decision has been duplicated into Confluence;
- ADR-0003 is registered in the canonical ADR index;
- `[UNVALIDATED]` markers are preserved on unproven runtime/resource/AI/endurance claims;
- Confluence update is appropriately deferred until a stakeholder summary/link is useful.

## ADR Conformance Reviewer

**Result:** PASS with NOTE

Checks:

- one stable architecture-significant decision is recorded: central-node hardware profile plus its reference/equivalence contract;
- ADR follows the canonical Context / Decision / Alternatives / Consequences / Risks / Follow-up / Evidence / Review structure;
- status is `Proposed`;
- Project Owner decisions were recorded in Jira before the proposal;
- no reviewer is treated as an acceptance authority;
- physical evidence and explicit final Project Owner acceptance remain unchecked.

**NOTE:** PR links are `Pending` until the single IHAP-52 PR is created. They must be backfilled on the same branch immediately after PR creation.

## Pre-PR conclusion

The branch is suitable for a **draft PR** and Project Owner hardware validation.

The next acceptance gate is not more planning. It is execution of the committed IHAP-52 harness on the Raspberry Pi 4 reference specimen, followed by evidence sanitization/review. No workflow move to final review or ADR acceptance is justified before that evidence exists.
