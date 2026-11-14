# Apply Tanh Action Log-Probability Correction

Squashing a Gaussian sample into an action interval changes its probability density. Correcting the Jacobian keeps the actor likelihood consistent with the bounded actions actually given to the critic.

## Contract

pre_tanh is real (B,D), 1<=B<=128, 1<=D<=64, magnitude<=100. base_logprob is real(B,), the already summed Gaussian log density. action_scale is real(D,) in[1e-6,1000]. Return a dict actions:float64(B,D)=scale*tanh(u), log_prob:float64(B,)=base-sum(log(scale)+log(1-tanh(u)^2)). Compute the log Jacobian stably as 2*(log(2)-u-logaddexp(0,-2*u)), including when rounded tanh equals1. All actions and scales use dimensionless normalized controller coordinates; physical unit conversion is outside this function. No offsets, sampling or Gaussian probability computation.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Reward and value share fixed reward units; log densities and entropy are in natural-log units; normalized action coordinates are dimensionless. One aligned transition per record; true termination differs from time-limit truncation. No physical simulator runs. Original bounded component using supplied policy/value data. No online learning, external model weights or full-paper benchmark reproduction.


## Example 1

u=[[0,0]], base=[-2], scale=[2,3] returns zero actions and log_prob[-2-log(6)].

## Example 2

u=[[20]], base=[-1], scale=[1] gives a finite corrected log probability approximately37.61370564.
