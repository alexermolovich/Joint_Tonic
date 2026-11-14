# Compute an Expectile Regression Loss

An expectile emphasizes one side of a squared residual. In IQL, weighting higher observed action values more strongly can raise the state-value estimate without querying actions absent from the offline dataset.

## Contract

q_targets and values are real(B,T),1<=B<=64,1<=T<=1024; valid is Boolean of the same shape; tau is a scalar in[.001,.999]. Set residual=q_target-value and weight=tau when residual>=0, otherwise1-tau. Return a dict loss:Python float equal to global valid mean(weight*residual^2), per_element:float64(B,T) weighted squared terms exact0invalid, value_gradient:float64(B,T)=-2*weight*residual/valid_count exact0invalid. Empty support returns all zero. Q targets are fixed. This is quadratic expectile regression, not quantile pinball loss.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Reward and value share fixed reward units; log densities and entropy are in natural-log units; normalized action coordinates are dimensionless. One aligned transition per record; true termination differs from time-limit truncation. No physical simulator runs. Original bounded component using supplied policy/value data. No online learning, external model weights or full-paper benchmark reproduction.


## Example 1

Q=[[2,0]], V=[[1,1]], both valid, tau.75 gives loss.5, per_element[[.75,.25]], value_gradient[[-.75,.25]].

## Example 2

All-false validity returns zero loss, terms and gradient regardless of finite residuals.
