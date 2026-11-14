# Normalize Batched Advantages

Different rollout batches can have very different advantage scales. Centering and rescaling the valid batch keeps the update scale interpretable, while the mask prevents padding or missing transitions from changing its statistics.

## Contract

Implement `normalize_advantages(advantages, valid, epsilon)`. advantages is real (B,T), 1<=B<=64, 1<=T<=1024; valid is Boolean with the same shape. epsilon is a scalar in [1e-12,1]. Compute one global valid-entry mean and population variance (denominator count), then (advantage-mean)/sqrt(variance+epsilon), with invalid outputs exactly zero. Return a dict normalized:float64(B,T), mean:Python float, std:Python float equal to sqrt(variance+epsilon), count:Python int. With no valid samples use mean=0, variance=0, std=sqrt(epsilon), and zero normalized output. Do not normalize separately per row or use sample variance.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Log densities and ratios are dimensionless; advantage/value/return terms use the caller-fixed reward units. Ordered transition indices at a fixed caller-declared control interval; terminal events differ from time limits. Original bounded PPO component. Normalization, boundary handling and diagnostic conventions are explicitly supplied; this does not train a complete locomotion policy.


## Example 1

advantages[[1,3]],valid[[True,True]],epsilon1 gives mean2,var1,stdsqrt2,normalized[-1/sqrt2,1/sqrt2].

## Example 2

advantages[[4,99]],valid[[True,False]],epsilon1 gives mean4,std1,count1 and zeros.
