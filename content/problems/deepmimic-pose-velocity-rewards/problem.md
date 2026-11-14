# Compute Pose and Velocity Imitation Rewards

Motion imitation should compare physical orientations, not quaternion storage signs. Penalize squared angular disagreement and velocity disagreement separately, with scale factors that turn each error into a bounded reward.

## Contract

`rotations` and `reference_rotations` are real `(B, J, 4)`; `velocities` and `reference_velocities` are real `(B, J, 3)`, with `1 <= B <= 128` and `1 <= J <= 32`. Rotations are scalar-first `(w, x, y, z)` parent-local joint quaternions. Require norms within `1e-6` of one and then normalize. Angular velocities are in radians/second in corresponding parent-local frames; no frame conversion is implicit.

For each joint, angle error is `2*arccos(clip(abs(dot(q, q_reference)), 0, 1))` radians. Return `angle_error` as float64 `(B, J)`, `pose` as float64 `(B,)` equal to `exp(-2*sum(angle_error**2, axis=1))`, and `velocity` as float64 `(B,)` equal to `exp(-0.1*sum((velocity-reference_velocity)**2, over joints and axes))`, in a dictionary.

The coefficients carry reciprocal squared units so rewards are dimensionless. This isolates DeepMimic's pose and velocity terms. Do not add end-effector or center-of-mass terms, or claim this is the complete imitation reward.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Positions use meters, time seconds, angular quantities radians and rad/s; phase and reward are dimensionless. Exact per-input units appear in the contract. Synchronized motion states or phases are supplied. World coordinates are right-handed with +y up where used; local joint frames are relative to parents. Original bounded component using synthetic motion. No retargeting, discriminator or feedback policy is trained; no physical safety or full-paper reproduction claim.

## Example 1

Identical identity rotations and angular velocities yield pose reward [1], velocity reward [1] and angle_error [[0]] for one state and joint.

## Example 2

One joint with a 180-degree mismatch yields angle error pi and pose reward exp(-2*pi**2). A velocity difference [1, 0, 0] rad/s yields exp(-0.1). Negating a quaternion alone causes zero orientation error.
