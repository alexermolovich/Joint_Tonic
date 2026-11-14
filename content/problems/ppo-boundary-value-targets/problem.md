# Compute Value Targets Across Episode Boundaries

A robot rollout can end because the task terminates or because collection hits a time limit. These boundaries need different value targets: a real terminal has no future return, while a time limit can bootstrap from the last observation without borrowing rewards from the next reset.

## Contract

Implement `boundary_value_targets(rewards, next_values, terminated, truncated, valid, gamma, lam)`. rewards and next_values are real (B,T), 1<=B<=32, 1<=T<=1024. The three masks are Boolean of that shape. Valid positions must form a prefix in each row, possibly empty. terminated and truncated cannot both be true and must be false at invalid slots. gamma and lam are scalars in [0,1]. next_values refers to the actual next observation before any autoreset. Iterate backward: continuation is target[t+1] only when that next slot is valid and the current transition is neither terminated nor truncated; otherwise continuation is next_values[t]. Set target[t]=reward[t]+gamma*(not terminated[t])*((1-lam)*next_values[t]+lam*continuation). Return new float64(B,T), exact zero invalid. True terminal removes bootstrap; truncation bootstraps but prevents recursion into a reset episode.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Log densities and ratios are dimensionless; advantage/value/return terms use the caller-fixed reward units. Ordered transition indices at a fixed caller-declared control interval; terminal events differ from time limits. Original bounded PPO component. Normalization, boundary handling and diagnostic conventions are explicitly supplied; this does not train a complete locomotion policy.


## Example 1

rewards[[1,2]],nextvalues[[10,20]],no boundaries,allvalid,gamma.5,lam1 gives lasttarget12 and first7.

## Example 2

Mark firststeptruncated gives firsttarget6,last12; mark firstterminated instead gives firsttarget1,last12.
