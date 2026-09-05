# IHAP-49 — Cost Governance Notes

**Status:** component selection incomplete; replication total not yet valid

## Owned inventory evidence

The project already owns:

- USB-C 4056E-family charger/protection boards;
- single-cell 18650 holders with leads.

Historical ownership does not make either component acceptable for the reference implementation.

The owned holder is currently **not accepted as the reference holder** because the user-measured maximum width is approximately 18 mm and compatibility with the eventual exact cell is not demonstrated.

The owned charger/protection board remains a **candidate** because the exact protection-controller identity and quantitative trip thresholds are not yet verified.

## Replication-cost rule

The final power-subsystem replication cost must include every required component needed to reproduce the accepted architecture, including as applicable:

- regulated 5 V USB-C source/cable if part of the reference kit;
- exact backup cell;
- compatible holder;
- charger/protection board;
- DC/DC converter;
- source-selection/isolation components;
- switch;
- fuse/protection/polarity components;
- connectors and wiring attributable to the power subsystem.

A low individual part price must not be used to characterize the subsystem as inexpensive before this complete cost is known.

## Current disposition

Definitive BOM lines and replication totals are intentionally deferred until the exact implementation is selected and Project Owner acceptance is obtained. Existing IHAP-17 work remains informative but must not be treated as the final current architecture total.
