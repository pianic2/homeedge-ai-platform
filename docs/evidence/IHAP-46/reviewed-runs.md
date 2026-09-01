# IHAP-46 — Reviewed Physical Run Checkpoint

**Issue:** [IHAP-46](https://niccolopiazzi01.atlassian.net/browse/IHAP-46)
**PR:** [#25](https://github.com/pianic2/homeedge-ai-platform/pull/25)
**Evidence scope:** reviewed aggregates from local raw archives; raw radar telemetry remains local

## Validity classification

| Run | Classification | Decision use |
|---|---|---|
| `IHAP46-LD2410C-EMPTY-01` | Invalid sensor scenario / valid harness-defect evidence | Confirms the UART path and USB reconnect behavior; not an empty-room result |
| `IHAP46-LD2410C-EMPTY-02` | Valid | Controlled empty-room evidence |
| `IHAP46-LD2410C-ENTER-01` | Partially valid | Six repetitions have a fresh clear pre-start state; superseded for the entry gate by strict `ENTER-02` |
| `IHAP46-LD2410C-ENTER-02` | Valid strict acquisition; threshold result FAIL 7/10 | Moving-person detection and operational-onset evidence |

## `EMPTY-02`

- controlled duration: 300.007 s;
- samples: 3,001;
- presence samples: 0;
- presence ratio: 0.000;
- permitted maximum: 0.020;
- invalid radar frames: 0;
- warnings: none;
- nominal and median cadence: 100 ms;
- the only material gap was associated with the intentional pre-flight reset and USB re-enumeration.

This supports one controlled observation on the owned specimen. It is not a
population-wide reliability or false-positive guarantee.

## Strict `ENTER-02`

- archive SHA-256: `87b077dafa7767b72053e77ea4f416aa0fc39fd6251edb7a11ef46f4ab9ec07c`;
- valid UART samples: 6,535;
- invalid radar frames: 0;
- ten clear-state gates started and passed;
- every repetition had a fresh `presence=false` sample before the start marker;
- presence ratio range: 0.917–0.993;
- median operational onset: 1,129 ms;
- threshold result: 7/10 repetitions at or below 2,000 ms;
- threshold failures: repetitions 2, 3 and 10 at 2,421 ms, 2,356 ms and 2,590 ms.

The onset value begins at the operator start marker and includes reaction and
travel into the sensing area. It is not isolated radar-processing latency. The
three threshold failures remain real evidence; the threshold is not rewritten
and the run is not converted to PASS.

## Decision coverage

| Question | Current evidence |
|---|---|
| Moving presence | Demonstrated on the owned specimen; strict run eventually detected all ten entries |
| Empty-room baseline | Demonstrated once for 300 seconds |
| UART acquisition stability | Demonstrated across the reviewed runs with zero invalid radar frames in the accepted intervals |
| Stationary presence | `[UNVALIDATED]` — one lean scenario remains |
| Empty-room release after exit | `[UNVALIDATED]` — three automatically measured repetitions remain |
| Adjacent-space behavior | `[UNVALIDATED]` — one closed-door and one open-door scenario remain |
| GPIO OUT behavior | Not required for the current receive-only UART decision path |
| PIR physical comparison | No identified comparison specimen; technology comparison remains source-based |

No run authorizes identity, person count, coordinates, trajectory, behavioral
history, persistent raw radar data, occupancy guarantee, alarm, antifurto,
intrusion-detection, safety or protection claims.
