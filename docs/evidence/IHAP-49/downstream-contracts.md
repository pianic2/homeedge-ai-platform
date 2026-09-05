# IHAP-49 — Downstream Contracts

## IHAP-50 — Interconnect and Prototype Assembly

IHAP-50 must preserve:

- one regulated 5 V node domain serving LD2410C and the ESP32-C3 board input;
- the accepted 3.3 V peripheral domain downstream of the ESP32-C3 board where validated;
- normal 5 V USB-C source plus backup-source isolation/switchover as defined by the final IHAP-49 ADR;
- explicit prevention of unintended backfeed;
- final reed pull-network current must be included in the integrated power budget if an external network is selected.

IHAP-50 does not re-decide battery chemistry or charger topology.

## IHAP-51 — Edge Enclosure and Mounting

IHAP-51 must preserve:

- battery retention and cell-access rules;
- polarity/reverse-insertion mitigation required by IHAP-49;
- separation/access appropriate to charger input, battery and power switch;
- thermal and mechanical constraints from the selected cell/charger/converter;
- no enclosure wording that converts tested prototype evidence into a certification or fire-safety claim.

IHAP-51 does not re-decide the power architecture.

## IHAP-17 — Cost Governance / BOM

IHAP-17 may receive definitive power BOM lines only after Project Owner acceptance of the exact IHAP-49 implementation. Historical owned inventory remains distinct from replication cost.

## IHAP-43 — Hardware Decision Baseline

IHAP-43 receives the final accepted power-subsystem disposition after IHAP-49 is accepted. Until then, the ADR remains Proposed and no dependent task may treat exact battery/holder/converter details as frozen.

## Runtime / event integrity

IHAP-49 does not redefine runtime or event contracts. However, the final architecture must state whether normal-source loss can cause a controlled reboot or whether seamless transfer is required. Downstream runtime validation must account for the accepted behavior so that resets do not silently create duplicate/corrupt event semantics.
