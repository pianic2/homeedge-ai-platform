# IHAP-45 Pull Request Summary

## Scope

This change completes the environmental-sensor decision for the HomeEdge MVP using reproducible hardware validation and summary-only public evidence.

## Accepted decision

- DHT11 is the default standard-indoor profile.
- BME280 is the precision / extended-environment profile and may also act as a procurement fallback.
- DHT22 is not selected.
- Temperature and relative humidity remain the only accepted measurement channels.
- Absolute accuracy remains `[UNVALIDATED]` because no independent reference instrument was used.

## Evidence

- one normalized 115-minute controlled environmental run;
- 5,769 structured samples;
- one boot and one successful BME280 probe;
- 100% stream completeness for all three sensors;
- DHT11: 1,923/1,923 valid;
- DHT22: 1,921/1,923 valid with two `NO_RESPONSE` errors;
- BME280: 1,923/1,923 valid;
- no validation errors;
- Markdown, JSON and aggregate-only HTML summaries;
- raw serial and per-sample telemetry retained locally only.

## Governance

- ADR-0002 records the stable decision.
- R-011 records placement and enclosure measurement bias.
- RT-R011-01 remains Proposed and requires IHAP-51/IHAP-50 follow-up.
- Generated ESP-IDF `sdkconfig` files are excluded.
- No Jira or Confluence mutation is included in this branch.
