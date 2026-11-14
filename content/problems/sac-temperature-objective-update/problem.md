# Update a Temperature Objective (later SAC extension)

The entropy temperature should increase when the sampled policy is less random than the declared target and decrease when it is more random. Updating log temperature preserves positivity, while explicit clipping bounds this teaching update.

## Contract

log_alpha is a scalar in[-20,5]. log_probabilities is real(B,K),1<=B<=128,1<=K<=256,range[-100,100]; valid is Boolean with at least one true entry. target_entropy is a scalar in[-100,100], the desired expected differential entropy in nats (it may be negative). learning_rate is in[0,1]. Set alpha=exp(log_alpha), loss=-alpha*mean_valid(log_probability+target_entropy). Return a dict loss:float, gradient:float derivative with respect to original log_alpha (equal to loss), log_alpha:float updated by clip(original-learning_rate*gradient,-20,5), alpha:float exp(updated). Log densities are held fixed. This exact exponential dual objective differs from the common log-alpha surrogate; cite the later SAC Algorithms and Applications extension.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Reward and value share fixed reward units; log densities and entropy are in natural-log units; normalized action coordinates are dimensionless. One aligned transition per record; true termination differs from time-limit truncation. No physical simulator runs. Original bounded component using supplied policy/value data. No online learning, external model weights or full-paper benchmark reproduction.


## Example 1

log_alpha0, logp[[-2]], validTrue, target_entropy1, learning_rate.1 returns loss1, gradient1, log_alpha-.1, alpha=exp(-.1).

## Example 2

Changing logp to[[0]] gives loss/gradient-1 and new log_alpha.1.
