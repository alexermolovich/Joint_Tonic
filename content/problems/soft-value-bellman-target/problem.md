# Compute an Entropy-Regularized Bellman Target

One-step critic targets combine immediate reward with a value estimate of the next physical state. True task termination removes the future term; an administrative rollout limit does not necessarily end the task.

## Contract

rewards and next_values are real (B,T), 1<=B<=64, 1<=T<=1024; terminated and valid are Boolean arrays of the same shape. gamma is a scalar in [0,1]. Return a new float64(B,T) array: reward+gamma*(not terminated)*next_value at valid entries, exact0 otherwise. next_values is already a soft value for original SAC or an expectile value for IQL; do not subtract entropy again. A time-limit truncation has terminated=False and uses the final observation before reset. All invalid numeric entries raise even under a false mask. No gradients through targets are computed.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Reward and value share fixed reward units; log densities and entropy are in natural-log units; normalized action coordinates are dimensionless. One aligned transition per record; true termination differs from time-limit truncation. No physical simulator runs. Original bounded component using supplied policy/value data. No online learning, external model weights or full-paper benchmark reproduction.


## Example 1

rewards=[[1,1]], next_values=[[4,4]], terminated=[[False,True]], both valid, gamma=.5 returns [[3,1]].

## Example 2

A valid truncated transition with reward1, next value4, terminated=False returns3; masking that record invalid returns0.
