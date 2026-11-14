# Validate an Offline Dataset Split

## Intuition

A robot episode can contain many correlated transitions. Keeping its records within one data split avoids evaluating on the same rollout used for fitting; including source identity prevents unrelated datasets with matching local episode numbers from colliding.

## Mathematical mechanism

Let $e_i=(source_i,episode_i)$ and split $s_i\in\{0,1,2\}$. For each identity e define $$S_e=\{s_i:e_i=e\},\qquad leak(e)=\mathbf1[|S_e|>1].$$ Counts sum records, not distinct episodes. The validity report also requires evidence in all declared splits. This original audit supports offline learning but does not guarantee statistical independence or prevent duplicated content under different IDs.

## Visual computation trace

| Source | Episode | Split | Identity collision? |
|---|---|---|---|
| 0 | 1 | train | same as next row |
| 0 | 1 | validation | leakage |
| 1 | 1 | test | distinct source |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

episodes[1,1,2], sources[0,0,0], splits[0,1,2] returns counts[1,1,1], leakage_pairs[[0,1]], no missing splits, validFalse.

## Why this matters on a robot

A robot learning pipeline depends on correct action likelihoods, terminal flags and dataset identity. A numerically small loss cannot repair incorrect replay semantics or absent action coverage.

## Physical contract and limits

Reward and value share fixed reward units; log densities and entropy are in natural-log units; normalized action coordinates are dimensionless. One aligned transition per record; true termination differs from time-limit truncation. No physical simulator runs. Original bounded component using supplied policy/value data. No online learning, external model weights or full-paper benchmark reproduction.

Source: [primary paper](https://arxiv.org/abs/2110.06169). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
