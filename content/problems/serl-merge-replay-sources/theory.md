# Merge Online and Demonstration Replay

## Intuition

Replay sources may contain the same transition, especially after demonstrations are also copied into an online buffer. Preserve one immutable transition identity and report both sources instead of duplicating or overwriting evidence.

## Mathematical mechanism

Let a transition be $\tau_i=(o_i, a_i, r_i, o_i^{next}, d_i)$ under globally unique ID i. Union the two ID sets. If i appears in both, require exact equality of every transition field after the documented dtype conversion. Its source mask is $$s_i=\mathbf1[i\in D_{online}]+2\mathbf1[i\in D_{demo}].$$ Thus source masks 1, 2, 3 mean online only, demonstration only, or identical in both. Sort the output by ID and gather every field through the same ordering. The source mask is storage lineage; it is not an action-autonomy label.

## Visual computation trace

| ID | Online | Demonstration | Output origin |
|---|---|---|---|
| 1 | absent | present | 2 |
| 2 | present | absent | 1 |
| 5 | same transition | same transition | 3 |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

Use one-dimensional observations/actions. Online has ID `2`, observation `[0]`, action `[0.2]`, reward `1`, next observation `[1]`, terminated `False`. Demonstration has ID `1`, observation `[3]`, action `[0.1]`, reward `2`, next observation `[4]`, terminated `True`. Output IDs `[1, 2]`, observations `[[3], [0]]`, actions `[[0.1], [0.2]]`, rewards `[2, 1]`, next observations `[[4], [1]]`, terminated `[True, False]` and origin `[2, 1]`.

## Why this matters on a robot

A human correction can exist in both demonstration and online storage. Counting it twice changes the effective training distribution; resolving a conflicting action silently destroys evidence about what the robot actually executed.

## Physical contract and limits

Normalized observation/action coordinates and reward probabilities are dimensionless. Interaction/reset durations use seconds. Counters and indices are exact integers. Transitions follow the caller-declared fixed control period within each recorded episode; no implicit clock or coordinate conversion. Scheduler ticks are accounting events, not a promised wall-clock cadence. Original bounded operational component motivated by SERL/HIL-SERL. It does not reproduce the entire learner, authorize physical robot execution or establish deployment safety.

Source: [primary paper](https://arxiv.org/abs/2401.16013). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
