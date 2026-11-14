# Compute the Clipped Policy Surrogate

PPO compares the new policy with the policy that collected each action. The clipped objective limits an overly optimistic improvement, and the sign of the advantage determines which probability change should be limited.

## Contract

Implement `clipped_surrogate(new_logp, old_logp, advantages, valid, epsilon)`. Each numeric input has shape (B,T), 1<=B<=64 and 1<=T<=1024. Log densities are in [-100,100], including positive continuous densities, and abs(new_logp-old_logp)<=40 at every entry. Advantages have magnitude <=1e6. valid is Boolean (B,T); epsilon is a scalar in [0,1]. Set ratio=exp(new-old), then take the minimum of ratio*advantage and clip(ratio,1-epsilon,1+epsilon)*advantage. Return a dict with terms:float64(B,T), exact zero at invalid slots; objective:Python float, the mean term over valid slots; loss:Python float, negative objective. With no valid slots all outputs are zero.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Log densities and ratios are dimensionless; advantage/value/return terms use the caller-fixed reward units. Ordered transition indices at a fixed caller-declared control interval; terminal events differ from time limits. Original bounded PPO component. Normalization, boundary handling and diagnostic conventions are explicitly supplied; this does not train a complete locomotion policy.


## Example 1

Positive advantage1 ratio1.5 epsilon.2 clips objective to1.2; negative advantage-1 ratio1.5 gives-1.5, not-1.2.

## Example 2

All-False valid mask returns objective/loss0 and zero terms.
