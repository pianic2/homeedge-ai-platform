# IHAP-52 — Specialist Pre-PR Review Summary

**Review target:** `ihap-52-central-node-hardware-decision`  
**Base:** `main` at `d5e0b5648a2362385014241d50b950a1e8286417`  
**Review stage:** draft PR, before physical Raspberry Pi validation  
**Decision authority:** advisory reviewers only; Project Owner retains ADR acceptance, Jira transition and merge authority.

## Review result

No open `BLOCKER` or `MAJOR` finding remains after the pre-PR corrections.

Physical Raspberry Pi 4 evidence is still pending. Therefore:

- ADR-0003 remains `Proposed`;
- Raspberry Pi 4 remains the approved reference/validation candidate, not yet `Community validated`;
- the revised MVP storage baseline is **32 GB A2 microSD**;
- **Raspberry Pi OS Lite 64-bit** is the first reference/validation image;
- Alpine Linux remains a compatible alternative candidate pending separate validation;
- final workload sufficiency, microSD endurance, thermal sufficiency and AI acceleration remain `[UNVALIDATED]`.

## Architecture Regression Reviewer

**Result:** PASS with NOTE

- vendor-neutral ARM64/x86_64 hardware contract remains intact;
- future IaC portability remains an architectural constraint, not an implementation claim;
- Raspberry Pi OS Lite is a reference image, not a universal distro lock-in;
- Alpine Linux remains compatible-candidate scope;
- Docker, database, Kafka, orchestration and final AI runtime are not accepted by ADR-0003.

## Hardware Compatibility Reviewer

**Result:** PASS with NOTE

- Pi 4 >=4 GB, 32 GB A2 and Wi-Fi match the revised Project Owner baseline;
- Ethernet remains optional;
- stable manufacturer-supported PSU remains required;
- fan/heatsinks remain optional but recommended;
- Pi 5 remains a newer compatible/recommended candidate without false HomeEdge validation;
- x86_64 equivalent-device paths remain available.

## Testing & Evidence Reviewer

**Result:** PASS after corrections; physical evidence pending

Closed corrections:

- thermal acceptance now relies on observable stability/current-throttling evidence rather than an invented project temperature threshold;
- storage smoke now verifies deterministic write/read SHA-256 integrity;
- storage capacity gate is aligned to nominal 32 GB media and allows partition/format overhead;
- OS identity is captured while the exact Raspberry Pi OS Lite selection is recorded manually because software cannot reliably distinguish every image variant;
- **validation reproducibility gap:** the original `central-node-validation-plan.md` described gates and principles but did not provide a complete operator procedure. It has been replaced by a canonical end-to-end runbook covering OS preparation, Imager settings, first boot, updates, prerequisites, repository checkout, immutable run IDs, manual configuration capture, pre-flight commands, canonical harness invocation, exit-code handling, evidence verification, PASS/FAIL gates, post-run checks, failure classification and privacy review.

The runbook now defines that:

- every attempt has a unique run ID;
- a started run is never overwritten by a retry;
- physical configuration is recorded before stress begins;
- the exact branch commit is recorded;
- mandatory pre-flight failures stop the run;
- failed attempts remain evidence rather than being overwritten;
- a future operator can follow the same ordered procedure from blank microSD to reviewed local evidence.

The next mandatory gate is execution on the physical Raspberry Pi 4 reference specimen.

## Security & Privacy Reviewer

**Result:** PASS with NOTE

- Internet access is not required by the harness itself;
- Wi-Fi secrets/SSID are not intentionally collected by the harness;
- operator notes explicitly prohibit credentials and local network identifiers;
- raw evidence remains local until reviewed;
- no hardened/security-appliance claim is introduced.

## Cost Governance Reviewer

**Result:** PASS with NOTE

- already-owned Pi 4 and 32 GB A2 card are availability evidence, not zero-cost replication assumptions;
- replication prices must be refreshed when IHAP-17 is unblocked and BOM propagation occurs.

## Source of Truth Guardian

**Result:** PASS

- GitHub contains ADR/evidence/harness/runbook;
- Jira tracks workflow and Project Owner decisions;
- Confluence remains link/summary-only;
- `[UNVALIDATED]` markers remain on unsupported claims.

## ADR Conformance Reviewer

**Result:** PASS with NOTE

- ADR-0003 remains `Proposed`;
- PR #30 is linked;
- official Raspberry Pi OS installation documentation and Alpine alternative documentation are linked;
- final Project Owner acceptance remains intentionally unchecked.

## Conclusion

The draft PR is ready for the revised physical validation configuration:

```text
Raspberry Pi 4 Model B
>=4 GB RAM
32 GB A2 microSD
Raspberry Pi OS Lite 64-bit
Wi-Fi required
Ethernet optional
fan/heatsinks optional but recommended
```

The validation procedure is now an executable, repeatable operator runbook rather than a high-level checklist. No move to final review or ADR acceptance is justified until the physical run is complete.
