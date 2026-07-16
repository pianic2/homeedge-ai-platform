# Cost Governance and BOM Policy

**Issue:** IHAP-17 — S0-008 — Cost Governance and BOM Policy  
**Project:** [ITS] [EDGE] HomeEdge AI Platform  
**Document type:** Governance / Cost and BOM policy  
**Status:** Sprint 0 draft for review  
**Price snapshot date:** 2026-07-14  
**Source of truth:** This versioned GitHub document is the canonical policy for hardware BOM records, price snapshots, replication-cost reporting, paid-tool and cloud-cost boundaries, and contributor hardware requirements until superseded by a later reviewed change.

<!--
AI_AGENT_METADATA:
  issue: IHAP-17
  document_type: cost_governance_and_bom_policy
  canonical_path: docs/governance/cost-governance-and-bom-policy.md
  source_of_truth: github_versioned_repository_documentation
  source_of_truth_policy: docs/governance/source-of-truth.md
  product_vision: docs/product/product-vision.md
  documentation_strategy: docs/governance/documentation-strategy.md
  risk_model_baseline: docs/risks/risk-model-baseline.md
  task_scope: documentation_governance_only
  runtime_changes_allowed: false
  firmware_changes_allowed: false
  backend_changes_allowed: false
  mobile_changes_allowed: false
  cloud_changes_allowed: false
  purchase_execution_allowed: false
  price_model: dated_snapshot
  shipping_allocation_rule: separate_by_order_never_arbitrary
  current_shipping_total_eur: 0.00
  central_node_reference: raspberry_pi_4_or_equivalent
  central_node_minimum_cpu_cores: 2
  central_node_minimum_ram_gb: 2
  central_node_minimum_storage_gb: 32
  central_node_os_direction: alpine_linux_or_equivalent_unvalidated
  central_node_container_direction: docker_unvalidated
  raw_audio_collection_allowed: false
  project_owner_decision_authority: true
  unvalidated_claim_marker: "[UNVALIDATED]"

HIDDEN_ANTI_REGRESSION_RULES:
  - GitHub remains the source of truth for the cost policy and versioned BOM snapshots.
  - Jira tracks task state, blockers, review state, and evidence links.
  - Confluence may summarize and link but must not duplicate the long-form BOM as a competing source of truth.
  - Price snapshots are dated observations, not live-price guarantees or purchase commitments.
  - Shipping must be recorded separately by order or supplier and must not be distributed arbitrarily across line items.
  - Zero-price, promotional, donated, or already-owned items must not be used as universal replication prices.
  - Physical inclusion in the hardware inventory does not authorize runtime use.
  - The GY-MAX4466 may be costed as physically available, but raw-audio recording, transmission, storage, and stakeholder exposure remain outside the MVP.
  - The 18650, holder, and TP4056 inventory does not prove a validated or safe power architecture.
  - Raspberry Pi 4 is a reference central node, not a universal vendor lock-in requirement.
  - Alpine Linux and Docker are target deployment directions [UNVALIDATED], not implemented runtime evidence.
  - Mac mini M4 is not a contributor requirement and is not part of the replication cost.
  - Preserve [UNVALIDATED] on unproven technical, cost, compatibility, safety, runtime, and maturity claims.
  - Do not introduce production-ready, commercial-ready, security-grade, certified, alarm-grade, antifurto, access-control, intrusion-detection, or safety-critical claims.
-->

---

## 1. Purpose

This policy makes HomeEdge costs inspectable, reproducible, and reviewable without turning documentation into an immediate purchasing action.

It answers five separate questions:

1. What hardware is physically owned or planned?
2. What is required for one edge node?
3. What is required for the central node?
4. What is shared tooling rather than a per-node cost?
5. Which costs are known, missing, optional, future, recurring, or shipping-related?

Core rule:

```text
Record observed prices.
Separate purchase history from replication cost.
Keep shipping separate.
Do not treat a price choice as an architectural decision.
```

---

## 2. Scope and Non-scope

Included:

- hardware inventory and BOM governance;
- dated price snapshots and order evidence;
- pack-price and normalized-unit-price rules;
- edge-node, central-node, shared-tooling, and shipping separation;
- current Project Owner purchase records;
- minimum contributor and central-node hardware boundaries;
- paid-tool and cloud-cost policy;
- explicit evidence gaps and refresh rules.

Excluded:

- purchasing components;
- validating an electrical circuit;
- selecting final GPIO mappings;
- implementing firmware, backend, mobile, infrastructure, cloud, or container runtime;
- approving Alpine Linux or Docker as an accepted architecture decision;
- authorizing raw-audio collection or processing;
- claiming current market availability or guaranteed prices;
- claiming production, commercial, security, safety, alarm, access-control, or certification maturity.

---

## 3. Cost Model

### 3.1 Cost classes

| Class | Meaning | Included in initial platform total |
|---|---|---:|
| `EDGE_REQUIRED` | Required to physically assemble one reference edge node. | Yes |
| `EDGE_INSTALLED_DISABLED` | Physically included, but not enabled in the current MVP runtime boundary. | Yes, in physical build cost only |
| `EDGE_ALTERNATIVE` | Alternative to another component; never counted simultaneously without an explicit configuration. | No |
| `CENTRAL_REQUIRED` | Required for one central-node reference deployment. | Yes |
| `SHARED_TOOLING` | Reusable tools or bulk consumables shared across nodes. | Yes, once |
| `OPTIONAL` | Useful but not required for the minimum reference platform. | No |
| `FUTURE` | Related to later scope and not part of the current MVP total. | No |
| `RECURRING` | Monthly, annual, usage-based, cloud, SaaS, energy, or connectivity cost. | Reported separately |
| `SHIPPING` | Delivery charge recorded by order or supplier. | Added separately, never allocated arbitrarily |

### 3.2 Required totals

```text
EDGE_ACTIVE_MVP_KNOWN_SUBTOTAL
EDGE_PHYSICAL_BUILD_KNOWN_SUBTOTAL
CENTRAL_NODE_KNOWN_SUBTOTAL
SHARED_TOOLING_ACQUISITION_SUBTOTAL
SHIPPING_TOTAL
PLATFORM_INITIAL_REPLICATION_TOTAL
ADDITIONAL_EDGE_NODE_TOTAL
```

A total must be labeled `INCOMPLETE` whenever any required line lacks a verified quantity or price.

### 3.3 Purchase cost versus replication cost

| Measure | Rule |
|---|---|
| Owner acquisition cost | What the Project Owner actually paid, including promotional or zero-price units where documented. |
| Reference replication price | A realistic dated price available to another contributor. Promotional, donated, or zero-price units are excluded unless generally reproducible. |
| Normalized unit price | Pack price divided by usable units in that pack. |
| Used subtotal | Normalized unit price multiplied by the quantity used in the selected configuration. |

---

## 4. Price Evidence Rules

Every priced line should include:

- component and exact variant where known;
- role in the project;
- purchased quantity or pack quantity;
- total product price;
- normalized unit price;
- quantity used in the selected configuration;
- supplier or evidence source;
- purchase date or price-check date;
- tax status when known;
- replication and compatibility notes.

Evidence levels:

| Level | Evidence | Allowed use |
|---|---|---|
| `E1` | Order, invoice, receipt, or supplier page with date. | Owner acquisition and replication evidence. |
| `E2` | Project Owner purchase record without supplier/order date. | Historical inventory baseline; evidence completion required. |
| `E3` | Public supplier price snapshot with date. | Reference replication price only. |
| `E4` | Official manufacturer documentation. | Technical identity or constraints, never purchase price by itself. |

The first inventory batch remains primarily `E2`. The LD2410C, BME280, heat-insert kit, PH2.0 connector kit, and MC-38 entries are supported by Project Owner order screenshots showing supplier, order status, quantity, price, and date; they are treated as `E1` evidence.

### 4.1 Shipping and taxes

```text
Shipping is recorded separately for each order or supplier.
Shipping is never divided across components by an invented allocation formula.
```

The Project Owner confirmed that shipping was free for all components currently recorded.

```text
SHIPPING_TOTAL = €0.00
```

No separate tax or customs charge is visible in the supplied order screenshots. This policy does not infer that tax or customs can never apply to future orders.

---

## 5. Verified Order Evidence — 18 June 2026

The following closed orders were evidenced through Project Owner screenshots supplied on 2026-07-14. Currency is EUR. Shipping was confirmed as free.

| Order line | Supplier | Variant / pack | Purchased quantity | Total product price | Normalized unit price | Shipping | Classification | Evidence |
|---|---|---|---:|---:|---:|---:|---|---|
| LD2410C 24 GHz presence sensor | Camera Module Factory Store | LD2410C module | 2 modules | €8.78 | €4.3900 per module | €0.00 | `EDGE_REQUIRED` | Closed order dated 2026-06-18 |
| BME280 module | Shop1104003965 Store | GY-BME280-5V | 2 modules | €9.10 | €4.5500 per module | €0.00 | `EDGE_ALTERNATIVE` | Closed order dated 2026-06-18 |
| Brass heat-set insert kit | YMAX A Salted Fish Store | M2 / M2.5 / M3, 508 pieces | 1 kit | €7.07 | €0.0139 per insert | €0.00 | `SHARED_TOOLING` | Closed order dated 2026-06-18 |
| PH2.0 connector terminal kit | Professional Sample Kit Store | 230 pieces, 2/3/4/5-pin, 2.0 mm pitch | 1 kit | €2.94 | €0.0128 per piece | €0.00 | `SHARED_TOOLING` | Closed order dated 2026-06-18 |
| MC-38 magnetic contacts | Mega Semiconductor CO., Ltd. | 10 pairs | 1 pack | €7.19 | €0.7190 per pair | €0.00 | `EDGE_REQUIRED` | Closed order dated 2026-06-18 |

```text
VERIFIED_2026_06_18_ORDER_PRODUCT_SUBTOTAL = €35.08
VERIFIED_2026_06_18_ORDER_SHIPPING_TOTAL = €0.00
```

The brass heat-insert order appears in more than one screenshot but is counted once.

---

## 6. Project Owner Inventory Snapshot

The following table combines the earlier Project Owner inventory record with the verified order evidence above. Supplier and original order date remain pending for the rows marked `E2`.

| ID | Component | Brand / variant | Purchased units | Total price | Unit price | Evidence | Current classification |
|---|---|---|---:|---:|---:|---|---|
| INV-001 | OLED display | AOICRIE, white, 128×64 px | 5 | €7.71 | €1.5420 | `E2` | `OPTIONAL` / `FUTURE` |
| INV-002 | Jumper wires | 15 cm | 40 | €2.15 | €0.0538 | `E2` | `SHARED_TOOLING` |
| INV-003 | Heat-shrink tubing | UMLIFE, assorted | 580 | €4.30 | €0.0074 | `E2` | `SHARED_TOOLING` |
| INV-004 | Jumper wires | 20 cm | 120 | €5.86 | €0.0488 | `E2` | `SHARED_TOOLING` |
| INV-005 | DHT11 module | Model not yet recorded | 2 | €1.96 | €0.9800 | `E2` | `EDGE_REQUIRED` |
| INV-006 | GY-MAX4466 audio module | MAX4466-based microphone preamplifier module | 3 | €3.24 | €1.0800 | `E2` | `EDGE_INSTALLED_DISABLED` |
| INV-007 | DHT22 module | Model not yet recorded | 1 | €1.66 | €1.6600 | `E2` | `EDGE_ALTERNATIVE` |
| INV-008 | 5 V street-light LED module | Model not yet recorded | 1 | €1.14 | €1.1400 | `E2` | `FUTURE` / `OPTIONAL` |
| INV-009 | 400-point breadboard | Brand not recorded | 3 | €4.17 | €1.3900 | `E2` | `EDGE_REQUIRED` for prototype |
| INV-010 | TP4056 Type-C charging module | Brand not recorded | 15 | €4.07 | €0.2713 | `E2` | `EDGE_REQUIRED` candidate `[UNVALIDATED]` |
| INV-011 | TP4056 Type-C charging module | AOICRIE | 10 | €0.00 | €0.0000 | `E2` | Owner inventory only |
| INV-012 | Tarp clips | Brand not recorded | 50 | €1.93 | €0.0386 | `E2` | `OPTIONAL` |
| INV-013 | Resistor kit | 600-piece assortment | 600 | €3.17 | €0.0053 | `E2` | `SHARED_TOOLING` |
| INV-014 | 18650 battery holder with leads | Model not recorded | 10 | €3.15 | €0.3150 | `E2` | `EDGE_REQUIRED` candidate `[UNVALIDATED]` |
| INV-015 | Assorted LED kit | UMLIFE, 3 mm / 5 mm | 100 | €1.15 | €0.0115 | `E2` | `SHARED_TOOLING` / `OPTIONAL` |
| INV-016 | ESP32-C3 development board | Exact SuperMini variant not recorded | 2 | €0.00 | €0.0000 | `E2` | Owner inventory only |
| INV-017 | ESP32-C3 development board | Exact SuperMini variant not recorded | 3 | €8.75 | €2.9167 | `E2` | `EDGE_REQUIRED` |
| INV-018 | LD2410C presence sensor | Camera Module Factory Store | 2 | €8.78 | €4.3900 | `E1`, 2026-06-18 | `EDGE_REQUIRED` |
| INV-019 | BME280 module | GY-BME280-5V, Shop1104003965 Store | 2 | €9.10 | €4.5500 | `E1`, 2026-06-18 | `EDGE_ALTERNATIVE` |
| INV-020 | Brass heat-set inserts | M2/M2.5/M3, 508 pieces | 508 | €7.07 | €0.0139 | `E1`, 2026-06-18 | `SHARED_TOOLING` |
| INV-021 | PH2.0 connector terminal kit | 230 pieces | 230 | €2.94 | €0.0128 | `E1`, 2026-06-18 | `SHARED_TOOLING` |
| INV-022 | MC-38 magnetic contacts | 10 pairs | 10 pairs | €7.19 | €0.7190 | `E1`, 2026-06-18 | `EDGE_REQUIRED` |

### 6.1 Inventory acquisition subtotal

```text
OWNER_REPORTED_PRODUCT_ACQUISITION_SUBTOTAL = €89.49
SHIPPING_TOTAL = €0.00
OWNER_REPORTED_ACQUISITION_TOTAL_WITH_SHIPPING = €89.49
```

This subtotal is **not** the platform replication total. It includes bulk inventory, alternatives, optional items, future items, shared tooling, and zero-price promotional rows.

---

## 7. Reference Edge Node BOM

The Project Owner selected the following physical reference configuration:

- ESP32-C3 SuperMini;
- DHT11;
- LD2410C;
- MC-38;
- GY-MAX4466;
- 18650 battery and holder;
- TP4056 Type-C charging module;
- 400-point breadboard;
- jumper wires, PH2.0 connectors, resistors, insulation, mounting, and enclosure materials required for a complete build.

Physical presence and runtime authorization are separate properties.

| Component | Qty | Reference unit price | Known subtotal | Physical state | MVP runtime state | Evidence gap |
|---|---:|---:|---:|---|---|---|
| ESP32-C3 SuperMini development board | 1 | €2.9167 | €2.9167 | Required | Active MVP compute reference | Exact listing and supplier pending. |
| DHT11 module | 1 | €0.9800 | €0.9800 | Required | Active MVP environmental telemetry | Exact listing pending. |
| LD2410C presence radar | 1 | €4.3900 | €4.3900 | Required | Active MVP local non-identifying presence direction `[UNVALIDATED]` | Compatibility and runtime evidence remain pending. |
| MC-38 magnetic contact pair | 1 | €0.7190 | €0.7190 | Required | Active MVP door-state direction `[UNVALIDATED]` | Wiring and runtime evidence remain pending. |
| GY-MAX4466 module | 1 | €1.0800 | €1.0800 | Required by Project Owner physical configuration | Installed and disabled for MVP | Firmware use and derived-signal policy require separate reviewed work. |
| 400-point breadboard | 1 | €1.3900 | €1.3900 | Required for prototype | Physical assembly only | Production assembly approach is future work. |
| TP4056 Type-C charging module | 1 | €0.2713 | €0.2713 | Candidate required `[UNVALIDATED]` | Power subsystem only | Protection variant and full power design pending. |
| 18650 holder with leads | 1 | €0.3150 | €0.3150 | Candidate required `[UNVALIDATED]` | Power subsystem only | Mechanical and electrical validation pending. |
| 18650 cell | 1 | TBD | TBD | Required | Power subsystem only | Chemistry, capacity, protection, supplier, and price pending. |
| Jumper wires and PH2.0 connectors | TBD | Mixed inventory | TBD | Required | Physical assembly only | Validated wiring count and connector types pending. |
| Resistors / passives | TBD | Mixed inventory | TBD | Required when circuit demands them | Physical/electrical support | Values and quantities pending validated circuit. |
| Heat-shrink / insulation | TBD | Mixed inventory | TBD | Required where needed | Physical assembly only | Allocation based on actual build, never arbitrary. |
| Enclosure and mounting materials | 1 set | TBD | TBD | Required for installable replica | Physical assembly only | Design, materials, supplier, and price pending. |

Current known-price edge totals:

```text
EDGE_ACTIVE_MVP_KNOWN_SUBTOTAL = €10.9820
EDGE_PHYSICAL_BUILD_KNOWN_SUBTOTAL = €12.0620
EDGE_COMPLETE_REPLICATION_TOTAL = INCOMPLETE
```

`EDGE_ACTIVE_MVP_KNOWN_SUBTOTAL` excludes the GY-MAX4466 because its runtime use is not authorized in the current MVP. `EDGE_PHYSICAL_BUILD_KNOWN_SUBTOTAL` includes its physical acquisition cost.

### 7.1 Audio boundary

The GY-MAX4466 is costed because it is part of the Project Owner's physical configuration. It does not authorize raw-audio recording, transmission, persistence, recognition, person identification, behavioral profiling, or stakeholder exposure.

Any future non-reversible, local derived signal remains `FUTURE` and `[UNVALIDATED]` until a dedicated privacy, architecture, firmware, and evidence review permits it.

### 7.2 18650 power boundary

The presence of a cell holder and TP4056 module does not prove that the node has a validated charging, protection, regulation, thermal, enclosure, or low-voltage cutoff design.

Before battery operation is represented as validated, a separate technical task must establish exact cell provenance, protected-cell policy, TP4056 variant, regulator topology, current budget, runtime measurements, enclosure behavior, and failure evidence.

IHAP-17 records cost only and does not approve this architecture.

---

## 8. Central Node Reference Profile

The Mac mini M4 is not a universal contributor requirement and is not included in the HomeEdge replication cost.

```text
Raspberry Pi 4 Model B or equivalent
CPU: at least 2 cores
RAM: at least 2 GB
Storage: at least 32 GB
Architecture: supported ARM64 or x86_64
Network: Ethernet or Wi-Fi suitable for the selected deployment
Operating-system direction: Alpine Linux or equivalent [UNVALIDATED]
Container-runtime direction: Docker [UNVALIDATED]
```

Raspberry Pi 4 is a reference profile, not vendor lock-in.

| Central-node line | Qty | Price | Status | Notes |
|---|---:|---:|---|---|
| Raspberry Pi 4 Model B or equivalent SBC / mini-PC | 1 | TBD | `CENTRAL_REQUIRED` | Existing ownership does not replace the replication price. |
| Storage, minimum 32 GB | 1 | TBD | `CENTRAL_REQUIRED` | microSD or compatible storage; endurance requirement remains `[UNVALIDATED]`. |
| Adequate power supply | 1 | TBD | `CENTRAL_REQUIRED` | Must match the selected device. |
| Enclosure | 1 | TBD | `CENTRAL_REQUIRED` | Cooling requirement depends on selected hardware and measured load. |
| Network cable or Wi-Fi provisioning materials | As needed | TBD | `CENTRAL_REQUIRED` when not already available | Do not assume universal ownership. |
| Alpine Linux or equivalent | 1 installation | €0 licence acquisition | Target `[UNVALIDATED]` | Installation and support cost are not proven zero. |
| Docker open-source runtime path | 1 installation | €0 licence acquisition | Target `[UNVALIDATED]` | Images, updates, persistence, and rollback are not implemented by IHAP-17. |

```text
CENTRAL_NODE_KNOWN_SUBTOTAL = INCOMPLETE
```

A separate architecture task or ADR is required before the central-node software and deployment topology becomes accepted technical truth.

---

## 9. Shared Tooling and Consumables

Bulk purchases and reusable tools must not be multiplied by the number of edge nodes.

```text
SHARED_TOOLING_RECORDED_PRODUCT_SUBTOTAL = €28.57
SHARED_TOOLING_COMPLETE_TOTAL = INCOMPLETE
```

The €28.57 subtotal includes jumper wires, heat-shrink tubing, tarp clips, resistor kit, LED kit, heat-set insert kit, and PH2.0 connector kit. It is an acquisition subtotal, not a claim that all listed items are mandatory.

Tools not yet priced include soldering equipment, multimeter, cutters, wire stripper, USB data cable, optional USB-to-serial adapter, terminal tools, fasteners, and enclosure-fabrication tools.

---

## 10. Cloud, Paid Tool, and Recurring Cost Policy

| Cost area | Current decision |
|---|---|
| Paid cloud runtime | Avoided or deferred unless a later task provides necessity, budget, owner, limits, and evidence. |
| Paid SaaS / development tools | Avoided when a sufficient free or open-source path exists; exceptions require explicit justification. |
| Alpine Linux licence | No acquisition licence cost expected; deployment remains `[UNVALIDATED]`. |
| Docker open-source runtime path | No acquisition licence cost expected; deployment remains `[UNVALIDATED]`. |
| Electricity | Recurring operational cost; not yet measured. |
| Internet connectivity | Contributor/environment cost; not assumed universally free. |
| Domain, certificates, backups, monitoring, and hosted storage | Deferred until an implementation task defines the need. |
| Mac mini M4 | Explicitly excluded as a universal contributor requirement. |

A zero licence price must not be described as zero total cost. Setup, maintenance, energy, storage wear, networking, backups, monitoring, and operator time may still create costs.

---

## 11. Replication Summary

| Measure | Current value | Completeness |
|---|---:|---|
| Owner-reported product acquisition subtotal | €89.49 | Complete for all rows currently supplied |
| Shipping total | €0.00 | Project Owner confirmed free shipping for all currently recorded components |
| Known active-MVP edge subtotal | €10.9820 | Partial |
| Known physical edge-build subtotal | €12.0620 | Partial |
| Complete edge-node replication total | TBD | Incomplete: 18650 cell, wiring allocation, passives, enclosure, and mounting unresolved |
| Central-node replication total | TBD | Incomplete: device, storage, power supply, enclosure, and networking unresolved |
| Recorded shared inventory subtotal | €28.57 | Partial acquisition view only |
| Initial platform replication total | TBD | Incomplete |
| Additional edge-node total | TBD | Incomplete |

A complete platform total may be published only after all `EDGE_REQUIRED`, `CENTRAL_REQUIRED`, required shared-tooling, and any applicable tax records are resolved.

---

## 12. Review and Refresh Policy

Review this document when:

- a required component or exact variant changes;
- a component moves between MVP, disabled, optional, future, or alternative status;
- a supplier or pack quantity changes;
- a price snapshot becomes stale or unavailable;
- a promotional or zero-price unit is replaced by a reproducible market price;
- the edge wiring, power, enclosure, or central-node architecture is validated;
- paid cloud, SaaS, storage, monitoring, or recurring costs are proposed;
- a new node type is introduced.

Minimum arithmetic review:

```text
[ ] Pack price ÷ usable units equals normalized unit price.
[ ] Used quantity × normalized unit price equals used subtotal.
[ ] Alternative components are not double-counted.
[ ] Installed-disabled components are excluded from active-MVP cost.
[ ] Future and optional components are excluded from required totals.
[ ] Shared tooling is counted once.
[ ] Shipping is reported separately by order.
[ ] Zero-price promotional items do not become universal replication prices.
[ ] Every incomplete required line keeps the total marked INCOMPLETE.
```

Project Owner approval remains required before a BOM configuration, architecture choice, residual risk, budget commitment, or Jira completion decision becomes final.

---

## 13. Technical Reference Register

These references support component identity or target-platform feasibility. They are not supplier price evidence.

| Subject | Primary reference | Use |
|---|---|---|
| ESP32-C3 family | [Espressif ESP32-C3 Series Datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-c3_datasheet_en.pdf) | MCU family capabilities and electrical reference; the exact SuperMini board remains supplier-specific. |
| MAX4466 component family | [Analog Devices MAX4465–MAX4469 Datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/MAX4465-MAX4469.pdf) | Identifies MAX4466 as a microphone-preamplifier component; the GY module implementation remains supplier-specific. |
| Raspberry Pi 4 | [Raspberry Pi 4 product page](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/) | Reference central-node hardware family and RAM variants. |
| Docker Engine | [Docker Engine installation documentation](https://docs.docker.com/engine/install/) | Target container-runtime documentation; not implementation evidence. |

Exact primary documentation for the purchased DHT11 module, LD2410C board, MC-38 contact, TP4056 board, 18650 cell, OLED board, BME280 board, and other supplier-specific modules must be attached after their exact listings or manufacturer variants are identified.

---

## 14. Related Sources

- `README.md`;
- `docs/README.md`;
- `docs/governance/source-of-truth.md`;
- `docs/governance/documentation-strategy.md`;
- `docs/governance/shift-left-governance-baseline.md`;
- `docs/governance/scrum-governance-dor-dod.md`;
- `docs/governance/governance-lane-review-gate.md`;
- `docs/governance/stakeholder-transparency.md`;
- `docs/governance/stakeholder-report-data-rules.md`;
- `docs/product/product-vision.md`;
- `docs/risks/risk-model-baseline.md`.

If this document conflicts with the Product Vision or source-of-truth policy, the existing canonical source wins until a reviewed GitHub change resolves the conflict.
