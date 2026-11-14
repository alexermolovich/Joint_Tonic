# Sample a Balanced Multi-Dataset Mixture

## Intuition

Large datasets should not automatically dominate every mixed batch. Separate the probability of choosing a dataset from the probability of choosing an example within it.

## Mathematical mechanism

For dataset weights w_g, define $p_g=w_g/\sum_jw_j$ and cumulative $C_g=\sum_{j\leq g}p_j$. Selection uses $$g=\min\{j:C_j>u\},\qquad i=\lfloor v n_g\rfloor.$$ Here n_g is dataset size and u,v lie in [0,1). This gives each example probability p_g/n_g; zero-weight datasets have an empty probability interval.

## Visual computation trace

| Dataset | Size | Weight | CDF interval |
|---|---|---|---|
| 0 | 2 | 1 | [0,0.25) |
| 1 | 4 | 3 | [0.25,1) |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

sizes=[2,4], weights=[1,3], uniforms=[[0,0.9],[0.25,0.5]] returns dataset_ids=[0,1], local_indices=[1,2]. The CDF boundary belongs to the next dataset.

## Why this matters on a robot

Multiplying weights by dataset size changes the intended mixture. CDF boundary mistakes can accidentally draw a zero-weight source. Version the ordered dataset inventory and weights, and monitor realized counts to detect pipeline drift.

## Physical contract and limits

Counts, weights and fractions are dimensionless; dataset action interfaces remain distinct. Independent draws with replacement; selected local indices are not time coordinates. Original weighted mixture sampler motivated by OXE. Weights are explicit caller policy, not inferred from dataset size or asserted as the paper’s exact proportions.

Source: [primary paper](https://arxiv.org/abs/2310.08864). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.

Build the cumulative distribution over positive-weight datasets only, keeping their original indices; force its last value to exactly 1. This prevents floating-point roundoff from selecting a trailing zero-weight source.
