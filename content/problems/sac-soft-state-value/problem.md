# Compute an Entropy-Regularized State Value

A stochastic robot policy values both task reward and action entropy. Estimate its soft state value from sampled actions, while keeping the number of usable samples visible instead of interpreting an empty row as strong evidence.

## Contract

q_values and log_probabilities are real (B,K), 1<=B<=128, 1<=K<=256; valid is Boolean of the same shape. Log densities lie in [-100,100], including positive continuous densities. alpha is a scalar in [0,100]. Return a dict values:float64(B,), counts:int64(B,). Each value is the valid sample mean of Q-alpha*log_probability in that row; a row with no valid action samples returns value0/count0. Do not softmax over Q or add probability weights: the supplied samples already follow the policy.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Reward and value share fixed reward units; log densities and entropy are in natural-log units; normalized action coordinates are dimensionless. One aligned transition per record; true termination differs from time-limit truncation. No physical simulator runs. Original bounded component using supplied policy/value data. No online learning, external model weights or full-paper benchmark reproduction.


## Example 1

Q=[[2,4]], log probabilities=[[-1,-2]], both valid, alpha=.5 returns values[3.75], counts[2].

## Example 2

With both entries invalid, the same arrays return values[0], counts[0].
