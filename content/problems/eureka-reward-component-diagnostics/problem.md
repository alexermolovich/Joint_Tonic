# Aggregate Reward-Component Diagnostics

A reward can be numerically valid yet be dominated by a constant or oversized component. Summarize observed terms and compare their variation with an independent progress signal.

## Contract

components real (B,T,C), task_scores real (B,T), valid Boolean (B,T); 1<=B<=64, 1<=T<=1024, 1<=C<=16, total elements<=1e6, magnitudes<=1e6 including masked entries. Components are already weighted dimensionless rewards; task scores are independent dimensionless progress metrics. Flatten valid (episode,time) observations with equal weight per observation. Return dict count Python int; mean, std, mean_abs, correlation float64(C,). std is population standard deviation, computed with centered scaling to retain tiny nonconstant variation; correlation is Pearson covariance/(population_std_component*population_std_score), NaN if either exact standard deviation is zero. With no valid rows all four vectors NaN. Do not weight episodes equally or infer causal reward quality from correlation.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Reward contributions and independent progress/success metrics are dimensionless and already normalized. Observations are recorded rollout steps; paired comparisons share seed identity by column. No coordinate transform or simulator execution is implicit. Original bounded reward-design diagnostic or arithmetic teaching language. It does not reproduce language-model search, policy training or real-robot transfer.

## Example 1

components [[[1,2],[3,2]]], scores [[0,1]], all valid -> mean [2,2], std [1,0], mean_abs [2,2], correlation [1,NaN], count 2.

## Example 2

Same values with validity [[False,True]] -> mean [3,2], std [0,0], mean_abs [3,2], correlations NaN, count 1.
