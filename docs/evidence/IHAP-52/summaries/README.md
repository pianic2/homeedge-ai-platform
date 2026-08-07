# IHAP-52 Sanitized Validation Summaries

This directory is reserved for reviewed aggregate summaries generated from Project Owner/community central-node validation runs.

Raw harness output under `tools/hardware-validation/ihap-52-central-node/runs/` remains local and ignored by Git.

A public summary may be added only after checking that it does not expose Wi-Fi credentials, SSIDs, MAC addresses, private IP addresses, hostnames, usernames or unnecessary local paths.

A summary may report:

- device family/model;
- architecture, logical CPU count and RAM capacity;
- storage capacity/profile and integrity-smoke result;
- Wi-Fi gate pass/fail without private addressing;
- temperature aggregates and throttling/undervoltage flags;
- stress duration and worker result;
- overall automated gate;
- manual PSU/cooling/enclosure configuration;
- explicit `[UNVALIDATED]` boundaries.

A passing summary supports only the declared IHAP-52 validation envelope. It does not prove production readiness, final application sizing, microSD endurance or AI acceleration.
