# IHAP-49 — Review Checklist

**Status:** waiting for Project Owner review

## Power Electronics

- [ ] Normal regulated 5 V USB-C source profile frozen.
- [ ] Backup source-selection/isolation topology frozen.
- [ ] No prohibited backfeed path identified.
- [ ] 1S-to-5 V converter has sufficient measured/derived headroom.
- [ ] 5 V and 3.3 V rails measured with integrated reference load.
- [ ] Brownout/reset behavior recorded.

## Battery / Charging

- [ ] Exact cell SKU, chemistry, capacity and provenance frozen.
- [ ] Cell protection policy coherent with charger/protection board.
- [ ] Holder mechanically compatible with exact cell.
- [ ] Charger IC/board configuration and charge current verified.
- [ ] Protection-controller identity/thresholds verified or experimentally bounded.
- [ ] Charging-while-operating rule enforced.
- [ ] Low-voltage cutoff/recovery characterized.
- [ ] Reverse-insertion risk mitigated.

## Validation / Evidence

- [ ] Integrated normal-source run completed.
- [ ] Battery-path regulation run completed.
- [ ] Normal-source interruption/backup takeover tested.
- [ ] Normal-source restoration tested.
- [ ] Controlled backup endurance run completed.
- [ ] Any transient anomaly escalated rather than hidden by average-current measurements.

## Architecture Regression

- [ ] ESP32-C3 reference board remains unchanged.
- [ ] LD2410C remains on the required 5 V domain.
- [ ] DHT11 standard profile / BME280 precision profile distinction preserved.
- [ ] Passive reed decision preserved.
- [ ] Accepted local OLED preserved.
- [ ] No audio load reintroduced.
- [ ] IHAP-50 owns final interconnect implementation.
- [ ] IHAP-51 owns enclosure/mounting implementation.

## Cost Governance

- [ ] Owned historical items are distinguished from reference replication items.
- [ ] Rejected owned holder is not counted as a valid reference part merely because it is already purchased.
- [ ] Current market replication prices captured for cell, holder, converter and any source-selection parts.
- [ ] IHAP-17 definitive BOM update deferred until Project Owner accepts IHAP-49.

## Claim Boundary

- [ ] No use of `safe`, `certified`, `fire-safe`, `compliant`, `production-ready` or equivalent unsupported claims.
- [ ] Autonomy remains `[UNVALIDATED]` until measured.
- [ ] Generic marketplace module similarity is not treated as exact-spec evidence.
