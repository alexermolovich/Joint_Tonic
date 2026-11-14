# Mix Intervention and Autonomous Replay

## Intuition

Corrective and autonomous transitions answer different questions. Use explicit quotas and recorded priorities to build a reproducible batch while preserving the commands that were executed.

## Mathematical mechanism

For requested batch size B and human fraction eta, allocate $$n_H=\lfloor B\eta+0.5\rfloor,\qquad n_A=B-n_H.$$ Within each source pool, sort by the supplied priority and then original row index; take the required number without replacement. The result concatenates human selections followed by autonomous selections. Priorities are dimensionless values in [0,1); they can be stored random draws, but this operation generates none. Insufficient support raises an error rather than silently changing the recipe.

## Visual computation trace

| Source pool | Candidate priorities | One selected row |
|---|---|---|
| Human rows0,2 | .8,.1 | row2 |
| Autonomous rows1,3 | .4,.2 | row3 |
| Output order | human then autonomous | [2,3] |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

Actions `[[0.1], [0.2], [0.3], [0.4]]`, intervention `[True, False, True, False]`, priorities `[0.8, 0.4, 0.1, 0.2]`, batch size `2` and fraction `0.5` produce indices `[2, 3]`, actions `[[0.3], [0.4]]`, intervention `[True, False]` and counts `[1, 1]`.

## Why this matters on a robot

Rare corrective transitions can disappear in a large autonomous buffer. Explicit source quotas keep their representation reproducible; silently replacing missing corrective records changes the learning recipe and conceals insufficient demonstrations.

## Physical contract and limits

Normalized observation/action coordinates and reward probabilities are dimensionless. Interaction/reset durations use seconds. Counters and indices are exact integers. Transitions follow the caller-declared fixed control period within each recorded episode; no implicit clock or coordinate conversion. Scheduler ticks are accounting events, not a promised wall-clock cadence. Original bounded operational component motivated by SERL/HIL-SERL. It does not reproduce the entire learner, authorize physical robot execution or establish deployment safety.

Source: [primary paper](https://arxiv.org/abs/2410.21845). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
