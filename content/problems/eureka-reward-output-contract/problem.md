# Validate a Reward Function Contract

A reward callback needs a measurable interface before it can guide learning. Diagnose nonfinite values, excessive scale and inconsistent component totals without silently repairing the output.

## Contract

rewards real array-like (B,), components real (B,C), valid Boolean (B,), 0<=B<=4096, 1<=C<=32. Unlike ordinary finite numeric inputs, rewards/components may contain NaN/Inf: these are evidence to diagnose, not an exception. Require floating or integer real dtype (not bool/object/complex); all finite magnitudes <=1e6. reward_bound finite scalar [0,1e6], atol [0,1]. Components are already weighted dimensionless contributions, expected to sum to reward. Return dict finite bool(B): reward and all components finite; bounded bool(B): finite AND abs(reward)<=bound AND every abs(component)<=bound; consistent bool(B): finite AND abs(reward-sum(components))<=atol; accepted bool(B): valid AND finite AND bounded AND consistent; all_valid_accepted Python bool all accepted on valid rows (vacuously True with no valid rows); invalid_count Python int number of valid rejected rows. Diagnose even invalid-mask rows but exclude them from acceptance and aggregate count. No executable code is accepted; this checks captured reward-function outputs, not semantic task alignment.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, follow the stated nonfinite-evidence exception, with finite absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Reward contributions and independent progress/success metrics are dimensionless and already normalized. Observations are recorded rollout steps; paired comparisons share seed identity by column. No coordinate transform or simulator execution is implicit. Original bounded reward-design diagnostic or arithmetic teaching language. It does not reproduce language-model search, policy training or real-robot transfer.

## Example 1

rewards [3], components [[1,2]], valid [True], bound 3, atol 0 -> all flags True, invalid_count 0.

## Example 2

rewards [3,NaN], components [[1,1],[0,0]], valid [True,False], bound 3, atol 0 -> consistent [False,False], accepted [False,False], invalid_count 1.
