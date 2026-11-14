# Report Policy Update Clip Fractions

A probability ratio outside the clipping interval does not always change PPO’s objective. Separate raw ratio excursions from the signed cases where the clipped branch actually limits improvement, then report a likelihood-based change diagnostic.

## Contract

Implement `policy_clip_metrics(new_logp, old_logp, advantages, valid, epsilon)`. Numeric arrays are real (B,T), 1<=B<=64, 1<=T<=1024; validity is Boolean with the same shape. Log densities lie in [-100,100] and abs(new-old)<=40; epsilon is in [0,1]. Return a dict count:Python int, ratio_clip_fraction:Python float for valid ratios strictly outside [1-epsilon,1+epsilon], active_clip_fraction:Python float for valid entries where (advantage>0 and ratio>1+epsilon) or (advantage<0 and ratio<1-epsilon), and approx_kl:Python float equal to valid mean(exp(delta)-1-delta), delta=new-old. Each numeric result is zero when count=0. Zero advantages never activate objective clipping. Preserve the strict endpoint convention.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Log densities and ratios are dimensionless; advantage/value/return terms use the caller-fixed reward units. Ordered transition indices at a fixed caller-declared control interval; terminal events differ from time limits. Original bounded PPO component. Normalization, boundary handling and diagnostic conventions are explicitly supplied; this does not train a complete locomotion policy.


## Example 1

ratios[1.5,.5],advantages[1,-1],epsilon.2 gives bothfractions1, KLmean((.5-log1.5)+(-.5-log.5))=-.5log(.75).

## Example 2

Same ratios with advantages[-1,1] gives ratiofraction1,activefraction0; large ratio alone does not imply clipping active.
