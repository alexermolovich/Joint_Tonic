# Rank Reward Candidates by Rollout Evidence

Select a trained candidate using held-out task behavior, not the numerical scale of its training reward. Make missing evidence and observed safety violations explicit before ranking.

## Contract

success and safety_violation Boolean (K,N), valid Boolean same shape; 1<=K<=128, 0<=N<=4096, <=1e6 entries. Each row is one candidate policy evaluated on the same declared task distribution; a trial can succeed and violate safety simultaneously. min_trials built-in int [1,4096]; max_violation_rate scalar [0,1]. Return dict count int64(K,), success_rate and violation_rate float64(K,) NaN if zero count, eligible bool(K,) count>=min AND violation_rate<=max; order int64(E,) containing eligible candidate indices sorted descending success_rate, ascending violation_rate, descending count, ascending index; selected Python int first ordered index or -1. Missing observations cannot become failures or successes. This ranking uses independent rollout labels, never the candidate's training reward, and is an original operational policy, not Eureka's exact search implementation.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Reward contributions and independent progress/success metrics are dimensionless and already normalized. Observations are recorded rollout steps; paired comparisons share seed identity by column. No coordinate transform or simulator execution is implicit. Original bounded reward-design diagnostic or arithmetic teaching language. It does not reproduce language-model search, policy training or real-robot transfer.

## Example 1

success [[True,False],[True,True]], violations all False, valid all True, min_trials 2,max_rate 0 -> rates [.5,1], order [1,0], selected 1.

## Example 2

Same success but candidate 1 violations [True,False], max_rate 0 -> candidate 1 ineligible; order [0], selected 0.
