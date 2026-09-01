# IHAP-46 — Reviewed Physical Run Checkpoint

**Issue:** [IHAP-46](https://niccolopiazzi01.atlassian.net/browse/IHAP-46)
**PR:** [#25](https://github.com/pianic2/homeedge-ai-platform/pull/25)
**Evidence scope:** reviewed aggregates from local raw archives; raw radar telemetry remains local

## Validity classification

| Run | Classification | Decision use |
|---|---|---|
| `IHAP46-LD2410C-EMPTY-01` | Invalid sensor scenario / valid harness-defect evidence | Confirms the UART path and USB reconnect behavior; not an empty-room result |
| `IHAP46-LD2410C-EMPTY-02` | Valid — PASS | Controlled empty-room evidence |
| `IHAP46-LD2410C-ENTER-01` | Partially valid | Six repetitions have a fresh clear pre-start state; superseded for the entry gate by strict `ENTER-02` |
| `IHAP46-LD2410C-ENTER-02` | Valid strict acquisition — FAIL 7/10 against the original onset threshold | Moving-person detection and operational-onset limitation |
| `IHAP46-LD2410C-STILL-02` | Valid — PASS | Stationary-presence retention on the owned specimen |
| `IHAP46-LD2410C-EXIT-03` | Valid procedure-defect evidence; release threshold unclassifiable | Eventual clear observed, but the operator delayed departure after `START NOW` |
| `IHAP46-LD2410C-EXIT-04` | Two valid repetitions — FAIL against the operational release threshold; one repetition excluded | Characterizes release after a normal exit and door close |
| `IHAP46-LD2410C-ADJ-CLOSED-01` | Valid — PASS | Adjacent corridor path with the door closed |
| `IHAP46-LD2410C-ADJ-OPEN-01` | Valid — PASS | Same adjacent corridor path with the door open about 30 degrees |

## `EMPTY-02`

- controlled duration: 300.007 s;
- samples: 3,001;
- presence samples: 0;
- presence ratio: 0.000;
- permitted maximum: 0.020;
- invalid radar frames: 0;
- warnings: none;
- nominal and median cadence: 100 ms.

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

## `STILL-02`

- archive SHA-256: `357f0d606e871e617d2616bd3b16004e616b2140e2ef80dea3f0f4e7d0dd91a0`;
- controlled interval: 300.008 s;
- interval samples: 3,000;
- presence samples: 3,000;
- presence ratio: 1.000;
- valid UART samples in the complete run: 5,392;
- invalid radar frames: 0;
- fresh occupied precondition age: 97 ms;
- median cadence: 100 ms; maximum interval gap: 134 ms;
- raw reanalysis: PASS, coherent with the published aggregate, no warning.

This demonstrates stationary-presence retention for the tested person, setup
and owned specimen. It does not create an occupancy or population-wide
guarantee.

## `EXIT-03` and corrected `EXIT-04`

`EXIT-03` archive SHA-256:
`d0c033e31f0848a38001d28c5383e88df15856410be003a38a18850b9a4afa5c`.
The recorded clear values were 29,982 ms, 23,245 ms and 32,814 ms, but the
operator reported delaying departure for several seconds after the countdown
and start marker. Those values are not classified as sensor latency or as
threshold failures. The run is retained only as procedure-defect evidence and
proof that eventual clear occurred.

The instructions and automated checks were corrected before `EXIT-04` so that
`START NOW` explicitly defines the operational timing origin and the operator
must leave immediately.

`EXIT-04` archive SHA-256:
`f026245914f815e24eb0cbea490a9e9b6c32b0bca3567d35973b1bfd14ad0c61`.
All three occupied preconditions passed, no invalid UART frames were observed,
and raw reanalysis matched the aggregates.

| Repetition | First clear from `START NOW` | Presence ratio | Classification |
|---:|---:|---:|---|
| 1 | 17,736 ms | 0.375 | Excluded: operator re-entered with about five seconds remaining |
| 2 | 18,506 ms | 0.307 | Valid — FAIL |
| 3 | 18,754 ms | 0.312 | Valid — FAIL |

The operational gate was at most 10,000 ms to first clear and at most 0.250
presence ratio. The operator confirmed that repetitions 2 and 3 began with an
immediate departure at `START NOW`; normal exit and door closing took about
5–7 seconds. The machine has no separate door-closure marker, so that estimate
is not subtracted from the measured values. Both clean repetitions consistently
fail the original operational gate while still demonstrating eventual release.
No threshold is rewritten and no additional repetition is required for the
technology decision.

## Adjacent-space runs

### `ADJ-CLOSED-01`

- archive SHA-256: `3f35a623ca318a04d3d0fee8d293335e2ae7bc4dc52a981650ed2b69d5ce3ddb`;
- controlled interval: 120.009 s;
- samples: 1,200;
- presence samples: 0;
- presence ratio: 0.000;
- invalid radar frames: 0;
- median cadence: 100 ms;
- fresh clear precondition and coherent raw reanalysis;
- operator path: external corridor parallel to the door wall, 0.5–2 m from the
  threshold, approximately 3 m back and forth; door closed.

### `ADJ-OPEN-01`

- archive SHA-256: `cab63edffcdf52898c89ccc00d78980f7150b5d3b21bb184ed6569483694073a`;
- controlled interval: 120.010 s;
- samples: 1,200;
- presence samples: 0;
- presence ratio: 0.000;
- invalid radar frames: 0;
- median cadence: 100 ms; maximum interval gap: 120 ms;
- fresh clear precondition and coherent raw reanalysis, with no warning;
- operator path: the same external corridor path of approximately 3 m; door
  fully open to about 30 degrees; the threshold was never crossed.

Both adjacent-space scenarios pass for the exact tested setup, path and owned
specimen. They do not prove universal immunity through walls, doorways or other
placements.

## Decision coverage

| Question | Reviewed evidence |
|---|---|
| Moving presence | Demonstrated; all ten strict entries were eventually detected, with 7/10 meeting the original operational-onset threshold |
| Stationary presence | Demonstrated for 300 seconds with 3,000/3,000 presence samples |
| Empty-room baseline | Demonstrated once for 300 seconds with zero presence samples |
| Empty-room release after exit | Eventual release demonstrated; two clean repetitions consistently failed the original 10-second operational threshold |
| Adjacent-space behavior | No detection in either 120-second tested corridor path, with the door closed and open about 30 degrees |
| UART acquisition stability | Zero invalid radar frames in the accepted intervals and coherent raw reanalysis |
| GPIO OUT behavior | Not required for the current receive-only UART decision path |
| PIR physical comparison | No identified comparison specimen; technology comparison remains source-based |

The lean physical campaign is complete. Additional repetitions would not change
the current decision: the evidence demonstrates the intended stationary fit and
characterizes the onset/release limitations without creating an occupancy
guarantee.

No run authorizes identity, person count, coordinates, trajectory, behavioral
history, persistent raw radar data, occupancy guarantee, alarm, antifurto,
intrusion-detection, safety or protection claims.
