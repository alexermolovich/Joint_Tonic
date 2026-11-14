# Interpolate a Reference Motion Pose

A reference motion is sampled at discrete times, while a controller may request an intermediate pose. Interpolate translation linearly and rotation along its shortest spherical arc, remembering that opposite quaternion signs represent the same orientation.

## Contract

`times` is real `(T,)`, `positions` is real `(T, 3)`, `rotations` is real `(T, J, 4)` and `query_times` is real `(Q,)`. Bounds are `2 <= T <= 1024`, `1 <= J <= 32` and `0 <= Q <= 256`. Timestamps must increase strictly and lie in `[0, 1_000_000]` seconds; queries have the same range. Positions are root translations in meters in a right-handed, y-up world. Each rotation is a scalar-first `(w, x, y, z)` quaternion for a joint relative to its parent. Require its norm within `1e-6` of one, then normalize it.

Clamp each query to the clip endpoints. Choose the lower segment with `searchsorted(times, clamped_query, side="right") - 1`, clipped to `[0, T-2]`; compute its fractional time alpha. Interpolate positions linearly. For each joint, negate the high-end quaternion if its dot product with the low-end quaternion is negative. Use shortest-arc SLERP, except that dot products greater than `0.9995` use normalized linear interpolation. Normalize every output quaternion.

Return a dictionary with `positions` (float64 `(Q, 3)`), `rotations` (float64 `(Q, J, 4)`), `interval` (int64 `(Q,)`) and `alpha` (float64 `(Q,)`). Quaternion endpoint signs follow the segment sign rule; they need not match raw source signs. Empty queries are valid. Do not wrap the clip, synthesize velocities or retarget motion.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Positions use meters, time seconds, angular quantities radians and rad/s; phase and reward are dimensionless. Exact per-input units appear in the contract. Synchronized motion states or phases are supplied. World coordinates are right-handed with +y up where used; local joint frames are relative to parents. Original bounded component using synthetic motion. No retargeting, discriminator or feedback policy is trained; no physical safety or full-paper reproduction claim.

## Example 1

Times [0, 2], root positions [[0, 0, 0], [2, 0, 0]], identity joint quaternions and query [1] yield root position [[1, 0, 0]], identity orientation, interval [0] and alpha [0.5].

## Example 2

An identity quaternion followed by its negative represents no rotation change. The midpoint remains identity after shortest-arc sign handling. A query beyond the final timestamp clamps to alpha 1.
