# Build Advantage-Weighted Action Weights

Offline policy fitting can prefer logged actions that look better than the state-value baseline. Exponential advantage weights make that preference explicit, while a declared cap keeps one high estimate from dominating the supervised update.

## Contract

q_targets and values are real(B,T),1<=B<=64,1<=T<=1024; valid is Boolean of the same shape. beta is a scalar in[0,100]; max_weight is in[1,1e6]. Return a new float64(B,T) array min(exp(beta*(Q-V)),max_weight) at valid entries and0elsewhere. Cap the exponent at log(max_weight) before exponentiation to avoid overflow. Negative exponents may underflow to zero. Do not normalize across examples; beta0 gives weight1 at every valid entry.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Reward and value share fixed reward units; log densities and entropy are in natural-log units; normalized action coordinates are dimensionless. One aligned transition per record; true termination differs from time-limit truncation. No physical simulator runs. Original bounded component using supplied policy/value data. No online learning, external model weights or full-paper benchmark reproduction.


## Example 1

Q=[[0,1,100]], V=zeros, all valid, beta1,max_weight2 returns[[1,2,2]].

## Example 2

beta0 with validity[[True,False]] returns[[1,0]], regardless of finite Q/V values.
