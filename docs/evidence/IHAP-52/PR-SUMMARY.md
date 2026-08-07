# IHAP-52 Pull Request Summary

## Scope

This change defines the HomeEdge MVP central-node hardware profile without accepting a specific runtime, operating system distribution, database, container topology or AI model.

## Proposed decision

- vendor-neutral central-node hardware contract;
- Raspberry Pi 4 Model B >=4 GB as the first reference/validation candidate;
- existing Raspberry Pi 4 Model B 8 GB as the first physical validation specimen;
- 64 GB A2 microSD reference storage;
- Wi-Fi required, Ethernet optional;
- Linux-exposed graphics/compute-device baseline for future AI direction, without claiming AI acceleration;
- heatsinks and/or fan optional but recommended;
- Raspberry Pi 5 treated as a newer compatible/recommended candidate until equivalent HomeEdge/community evidence exists;
- ARM64 and x86_64 replacement paths preserved.

## Evidence and validation

The branch includes:

- ADR-0003 in `Proposed` status;
- workload/resource assumption table;
- manufacturer-backed alternative comparison;
- acquisition-vs-replication cost boundary;
- reproducible physical/resource validation plan;
- Python standard-library validation harness;
- specialist pre-PR review summary.

The harness performs profile checks, Wi-Fi checks, storage integrity smoke testing, bounded CPU/thermal stress observation and Raspberry Pi undervoltage/throttling observation.

## Evidence boundary

Physical Raspberry Pi 4 validation has not yet been executed for this PR. Therefore:

- Raspberry Pi 4 is not yet labelled `Community validated`;
- ADR-0003 remains `Proposed`;
- final workload sufficiency remains `[UNVALIDATED]`;
- 64 GB microSD endurance/retention sufficiency remains `[UNVALIDATED]`;
- future AI model/runtime and GPU/NPU acceleration remain `[UNVALIDATED]`;
- Docker, Alpine Linux, database, Kafka and orchestration remain outside IHAP-52.

## Review status

Pre-PR specialist review found no remaining `BLOCKER` or `MAJOR` issue. Two evidence-precision findings were corrected on the same branch:

1. thermal acceptance wording no longer invents a CPU-temperature threshold from ambient operating specifications;
2. storage smoke testing now verifies deterministic write/read SHA-256 integrity in addition to byte counts and cleanup.

## Next gate

The Project Owner runs the committed harness on the Raspberry Pi 4 reference specimen. Sanitized evidence and any fixes remain on this same branch and PR before ADR acceptance or final Jira review transition.
