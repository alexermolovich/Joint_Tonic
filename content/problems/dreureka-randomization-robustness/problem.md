# Compare Robustness Across Randomization Settings

A physics setting can appear stronger merely because it was tested on easier rollout seeds. Compare the same observed seed columns when measuring degradation against a baseline.

## Contract

success and valid Boolean (G,N), 1<=G<=128, 0<=N<=4096, <=1e6 entries. Rows are fixed physical parameter settings and columns are the same recorded rollout seeds. Parameter values/units are provided by the surrounding experiment; this function only compares dimensionless outcomes without changing physics. baseline_index built-in int [0,G), min_pairs built-in int [1,4096]. Return dict counts int64(G,), success_rate float64(G,) using all valid trials (NaN none), paired_counts int64(G,), paired_delta float64(G,) mean(success_g-success_baseline) over jointly valid same-seed trials (NaN none), comparable bool(G,) paired_count>=min_pairs; worst_index Python int lowest paired_delta among comparable rows with tie lowest index, or -1. Baseline compared with itself gives delta0 where observed. Pairing avoids confounding different seed subsets; no confidence interval or complete reward-aware prior construction is claimed.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Reward contributions and independent progress/success metrics are dimensionless and already normalized. Observations are recorded rollout steps; paired comparisons share seed identity by column. No coordinate transform or simulator execution is implicit. Original bounded reward-design diagnostic or arithmetic teaching language. It does not reproduce language-model search, policy training or real-robot transfer.

## Example 1

success [[True,False],[False,False]], all valid, baseline 0,min_pairs 2 -> success_rate [.5,0], paired_delta [0,-.5], worst_index 1.

## Example 2

Same successes with row1 valid [False,True] -> rate 0, paired_delta 0, paired_count 1; with min_pairs 2 row1 not comparable and worst_index 0.
