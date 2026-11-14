# Label Human Intervention Segments

## Intuition

A human override changes the action that the robot actually experiences. Replay must record that executed command and identify each contiguous intervention without blending across episode resets.

## Mathematical mechanism

For Boolean intervention flag h and same-frame action vectors, $$a_i^{exec}=\begin{cases}a_i^{human}&h_i=1\\a_i^{policy}&h_i=0.\end{cases}$$ A new human segment starts when h_i is true and either i is the first row, h at the preceding row is false, or episode identity changes. Count those starts to assign segment IDs; autonomous rows keep -1. Segment intervals are half-open [start, end), so their difference counts transitions exactly. Intervening does not imply termination.

## Visual computation trace

| Record | Source | Episode | Segment |
|---|---|---|---|
| 0 | policy | 0 | -1 |
| 1 | human | 0 | 0 |
| 2 | human | 0 | 0 |
| 3 | human | 1 | 1 |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

Policy actions `[[0.1], [0.2], [0.3]]`, human actions `[[0.9], [0.8], [0.7]]`, intervention `[False, True, True]` and episodes `[0, 0, 0]` produce executed_actions `[[0.1], [0.8], [0.7]]`, segment_id `[-1, 0, 0]` and segments `[[0, 1, 3]]`.

## Why this matters on a robot

An intervention is a contiguous correction inside one episode. Merging corrections across resets gives a misleading duration and can train on an impossible cross-episode sequence. Execute the recorded human action only on selected intervention rows.

## Physical contract and limits

Normalized observation/action coordinates and reward probabilities are dimensionless. Interaction/reset durations use seconds. Counters and indices are exact integers. Transitions follow the caller-declared fixed control period within each recorded episode; no implicit clock or coordinate conversion. Scheduler ticks are accounting events, not a promised wall-clock cadence. Original bounded operational component motivated by SERL/HIL-SERL. It does not reproduce the entire learner, authorize physical robot execution or establish deployment safety.

Source: [primary paper](https://arxiv.org/abs/2410.21845). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
