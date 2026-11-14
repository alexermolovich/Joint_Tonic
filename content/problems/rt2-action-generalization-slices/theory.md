# Monitor Invalid Actions and Semantic Generalization Slices

## Intuition

An overall success percentage can hide a policy that emits malformed commands on unfamiliar instructions. Report validity and task success on the same denominator for every declared evaluation slice.

## Mathematical mechanism

For slice s with index set I_s, count 

$$n_s=|I_s|$$

, invalid rate $r_s=\sum_{i\in I_s}(1-v_i)/n_s$, and success rate $p_s=\sum_{i\in I_s}v_iy_i/n_s$. Here v and y are Boolean validity and success flags. An empty I_s has no estimated rate, represented by NaN rather than a misleading zero.

## Visual computation trace

| Slice | Attempts | Invalid | Valid successes | Rates |
|---|---|---|---|---|
| 0 | 2 | 1 | 1 | invalid0.5,success0.5 |
| 1 | 0 | 0 | 0 | unknown / NaN |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

valid=[True,False], success=[True,True], slice_ids=[0,0], num_slices=2 returns count=[2,0], invalid_rate=[0.5,NaN], success_rate=[0.5,NaN]. The invalid row is not a success.

## Why this matters on a robot

Dropping invalid commands before computing success inflates the metric. Empty slices indicate missing coverage and should block decisions that require evidence there; NaN is not a passing score. Semantic labels must be fixed before examining model results.

## Physical contract and limits

Rates are dimensionless attempt fractions; semantic slice IDs preserve external evaluation labels. Each row is one evaluated attempt, not a timestep; attempts may come from different episodes. Original monitoring component inspired by RT-2 semantic-generalization evaluation. It computes supplied slice metrics and does not infer semantic novelty from images or claim paper-level success.

Source: [primary paper](https://arxiv.org/abs/2307.15818). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
