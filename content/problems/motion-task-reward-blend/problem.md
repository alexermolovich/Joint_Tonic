# Combine Motion and Task Rewards

A task score and a motion-quality score measure different properties. Keep their weighted contributions visible while producing the scalar reward used by a controller update.

## Contract

`motion_reward` and `task_reward` are real `(B, T)` arrays in `[0, 1]`, where `1 <= B <= 128` and `1 <= T <= 256`. `valid` is a Boolean array of the same shape. Each weight is a scalar in `[0, 100]`; weights need not sum to one.

Return a dictionary with `motion_contribution`, `task_contribution` and `reward`, each float64 `(B, T)`. Contributions equal the corresponding weight times the input, with exact zero at invalid samples. Reward is their sum. Also return `mean_reward`, a Python float equal to the global mean over valid samples, or zero when none exist.

The caller supplies either a DeepMimic imitation reward or an AMP style reward as the motion component; this function computes neither. Rewards use a common dimensionless convention at synchronized samples. Keep the two contributions visible: a combined reward is not a physical safety certificate.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Positions use meters, time seconds, angular quantities radians and rad/s; phase and reward are dimensionless. Exact per-input units appear in the contract. Synchronized motion states or phases are supplied. World coordinates are right-handed with +y up where used; local joint frames are relative to parents. Original bounded component using synthetic motion. No retargeting, discriminator or feedback policy is trained; no physical safety or full-paper reproduction claim.

## Example 1

Motion reward [[0.8]], task reward [[0.2]], valid [[True]] and weights 0.75 and 0.25 produce contributions [[0.6]] and [[0.05]], reward [[0.65]] and mean_reward 0.65.

## Example 2

Zero weights produce zero contributions and reward. An all-invalid batch produces mean_reward 0 even with nonzero finite reward inputs.
