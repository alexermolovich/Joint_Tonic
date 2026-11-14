# Construct Motion Discriminator Features

A motion discriminator should recognize coordinated movement regardless of where the character stands or which way it faces. Express root velocities and endpoints in each state's own heading frame, then preserve the order of current and successor features.

## Contract

Root positions, root linear velocities and root angular velocities are real `(B, 2, 3)` arrays. `root_yaw` is real `(B, 2)`. `joint_rotations` is real `(B, 2, J, 3, 3)`, `joint_velocities` is real `(B, 2, J, 3)`, and `endpoints` is real `(B, 2, E, 3)`. Bounds are `1 <= B <= 64`, `1 <= J <= 32`, `1 <= E <= 8`. Transition index 0 is current; 1 is successor.

The world is right-handed with +y up. Local +x is the heading direction. Yaw is in `[-pi, pi]` radians and defines the local-to-world matrix `Ry = [[cos(yaw), 0, sin(yaw)], [0, 1, 0], [-sin(yaw), 0, cos(yaw)]]`. Positions are meters, root linear velocities meters/second, and angular velocities radians/second. Joint rotations are parent-local proper rotation matrices: validate orthogonality and determinant one with absolute tolerance `1e-6`, zero relative tolerance. Joint velocities are already parent-local.

For each state, concatenate these feature blocks in order:

1. `Ry.T @ root_velocity` (3 entries).
2. `Ry.T @ root_angular_velocity` (3 entries).
3. For each joint in order, its rotation's first column followed by its second column (6J entries).
4. Joint velocities flattened in joint/axis order (3J entries).
5. `Ry.T @ (endpoint - root_position)` for each endpoint in order (3E entries).

Return a fresh float64 `(B, 2F)` array, where `F = 6 + 9J + 3E`, containing current features followed by successor features. Each state uses its own root origin and heading. Do not include root height or clip phase, normalize features, or train a discriminator. The six-dimensional rotation ordering is an explicit teaching convention consistent with a normal/tangent representation; released checkpoint compatibility is not claimed.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Positions use meters, time seconds, angular quantities radians and rad/s; phase and reward are dimensionless. Exact per-input units appear in the contract. Synchronized motion states or phases are supplied. World coordinates are right-handed with +y up where used; local joint frames are relative to parents. Original bounded component using synthetic motion. No retargeting, discriminator or feedback policy is trained; no physical safety or full-paper reproduction claim.

## Example 1

With one identity joint, zero velocities, one endpoint [1, 0, 0], root at the origin and yaw 0, a state feature is [0,0,0, 0,0,0, 1,0,0,0,1,0, 0,0,0, 1,0,0]. Identical current and successor states repeat this 18-entry vector.

## Example 2

At yaw pi/2, world root velocity [0, 0, -1] becomes local [1, 0, 0]. Translating root and endpoints by the same world vector leaves relative endpoint features unchanged.
