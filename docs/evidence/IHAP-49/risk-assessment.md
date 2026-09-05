# IHAP-49 — Preliminary Power Risk Assessment

**Status:** Proposed; residual risks remain open pending exact component selection and validation

| Risk | Severity | Current control / decision | Residual state |
|---|---|---|---|
| Normal 5 V source loss | High | Battery retained as backup source | Transfer behavior `[UNVALIDATED]` |
| Backfeed between normal and backup source | High | Explicit source-selection/isolation requirement | Topology not yet frozen |
| Battery over-discharge | High | Candidate charger/protection board contains discrete protection stage | Controller identity/thresholds `[UNVALIDATED]` |
| Battery over-charge | High | 4056E-family CC/CV charger board candidate | Exact charge-current configuration and termination behavior `[UNVALIDATED]` |
| Reverse cell insertion | High | Risk identified; owned holder appears not mechanically keyed | Mitigation not yet frozen |
| Converter undervoltage/brownout | High | Regulated 5 V converter required; integrated brownout test mandatory | Converter not yet selected |
| Wi-Fi/current transient causes reset | High | Datasheet envelope + functional reset/brownout logging; escalate instrumentation if needed | Integrated peak `[UNVALIDATED]` |
| Excess temperature | High | Keep component ratings/headroom; observe charging/converter thermal behavior | Exact thermal envelope `[UNVALIDATED]` |
| Holder incompatibility / poor contact | Medium | Owned holder rejected as reference until exact fit demonstrated | New/reference holder not yet selected |
| Unsupported autonomy expectation | Medium | Battery role explicitly limited to backup; planning estimate separated from validation | Measured runtime `[UNVALIDATED]` |
| Cost creep | Medium | Cost complete subsystem, not already-owned individual parts | Exact replication total pending |
| Enclosure access exposes cell/polarity risk | Medium | Constraint forwarded to IHAP-51 | Physical design pending |
| Power reset corrupts/duplicates events | Medium | Transfer/recovery behavior must be explicit; no runtime contract change in IHAP-49 | Downstream runtime validation pending |

## Safety language boundary

The subsystem is a prototype hardware decision under validation. None of these controls authorizes statements such as `safe`, `certified`, `fire-safe`, `compliant`, `production-ready` or equivalent.
