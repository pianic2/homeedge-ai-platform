# IHAP-49 — Power Architecture Alternatives

**Status:** Proposed comparison supporting ADR review

| Alternative | MVP disposition | Rationale |
|---|---|---|
| Regulated 5 V USB-C only | Rejected as the complete subsystem | Simple and lowest-risk normal supply, but Project Owner requires local backup for blackout/cable-input failure. Retained as the **normal source**, not as the whole architecture. |
| Protected 18650 + charger/regulator | Viable alternative | Reduces reliance on external protection, but protected-cell dimensional envelope may complicate holder compatibility and duplicates some protection if the selected charger board already provides a verified protection stage. Exact cell/holder evidence would still be required. |
| Unprotected branded 18650 + verified charger/protection + regulator | Preferred implementation direction, not yet accepted | Matches the owned 4056E-family charger/protection-board topology and avoids redundant protection components, but only if exact protection thresholds, cell compatibility, holder fit and failure behavior are validated. |
| Unprotected cell + separate BMS/protection unrelated to charger | Not preferred | Adds components, interfaces and failure modes without a demonstrated MVP need if the owned charger/protection stage can be qualified. |
| LiPo pouch | Rejected for current reference direction | Does not eliminate the need for charging, protection, regulation, thermal/mechanical constraints or source switchover; introduces a different mechanical/handling profile without a current product requirement that justifies it. |
| Replaceable primary cells | Rejected | Poor fit for a continuously powered 5 V radar/Wi-Fi node and creates repeated-consumable handling without solving the regulated 5 V domain cleanly. |
| Rechargeable battery as primary continuous supply | Rejected | Planning budget shows a single 3.5 Ah-class 1S cell is an hours-scale source, not a multi-day reference supply. The Project Owner has selected wired 5 V as normal supply and battery only as backup. |

## Decision summary

The selected architecture class is therefore **normal regulated 5 V USB-C + rechargeable 1S battery backup**. Exact cell, holder, charger/protection qualification, boost converter and source-selection/isolation components remain implementation decisions to close before ADR acceptance.
