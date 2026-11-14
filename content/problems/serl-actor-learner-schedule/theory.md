# Schedule Actor-Learner Updates

## Intuition

The learner should not consume an unbounded update budget merely because it runs faster than robot collection. Track owed updates exactly, cap work per scheduling tick, and carry the remainder forward.

## Mathematical mechanism

Let D_t be cumulative new transitions, warmup W, and integer ratio numerator a and denominator b. The allowed cumulative update target is $$U_t^*=\left\lfloor\frac{a\max(D_t-W,0)}{b}\right\rfloor.$$ With completed count U_prev and per-tick cap C, emit $$u_t=\min(C, U_t^*-U_{prev}),\qquad U_t=U_{prev}+u_t,\qquad B_t=U_t^*-U_t.$$ Data counts never decrease, so backlog is nonnegative. Publish the latest U_t when its integer quotient by the publication interval increases. This models update accounting; it does not predict computation time or guarantee network delivery.

## Visual computation trace

| Tick | New records | Target updates | Emitted | Backlog |
|---|---|---|---|---|
| 0 | 2 | 4 | 3 | 1 |
| 1 | 0 | 4 | 1 | 0 |
| 2 | 1 | 6 | 2 | 0 |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

With new transitions `[2, 0, 1]`, warmup `0`, ratio `2/1`, cap `3` and publication interval `2`, return updates `[3, 1, 2]`, completed `[3, 4, 6]`, backlog `[1, 0, 0]`, published_version `[3, 4, 6]` and publish `[True, True, True]`.

## Why this matters on a robot

Robot observations arrive at a slower and less regular pace than optimizer calls. Ignoring accumulated update debt changes the update-to-data ratio; dropping backlog during a tick with no new observations makes the schedule depend on collection timing.

## Physical contract and limits

Normalized observation/action coordinates and reward probabilities are dimensionless. Interaction/reset durations use seconds. Counters and indices are exact integers. Transitions follow the caller-declared fixed control period within each recorded episode; no implicit clock or coordinate conversion. Scheduler ticks are accounting events, not a promised wall-clock cadence. Original bounded operational component motivated by SERL/HIL-SERL. It does not reproduce the entire learner, authorize physical robot execution or establish deployment safety.

Source: [primary paper](https://arxiv.org/abs/2401.16013). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
