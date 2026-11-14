# Compare Logged and Sampled Action Values

A critic can score sampled actions much higher than logged behavior. Report the two sample means separately so that missing observations cannot masquerade as a reassuring zero gap.

## Contract

`logged_values` is real `(B, L)` and `sampled_values` is real `(B, K)`, with `1 <= B <= 128` and `1 <= L, K <= 256`. Their corresponding validity masks are Boolean arrays of matching shapes. `threshold` is a scalar in `[0, 1_000_000]`.

Return a dictionary containing float64 `(B,)` arrays `logged_mean`, `sample_mean` and `gap`; int64 `(B, 2)` `counts` in logged/sample order; and Boolean `(B,)` `flagged`. Average each pool independently over its valid entries. A mean is NaN when its pool has no observations. The gap is sampled mean minus logged mean, and is NaN unless both exist. Flag exactly the rows where both pools exist and the gap is **strictly greater** than the threshold.

This is a value diagnostic, not the density-corrected CQL penalty or a guarantee of policy quality.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Actions and image intensities are normalized and dimensionless. Q values and rewards use a fixed reward scale; squared losses use squared reward units. All views in a row describe the same transition. No physical simulation or implicit coordinate conversion runs. Original bounded teaching component using supplied arrays; not a reproduction of trained policy performance or the full paper.

## Example 1

Logged values [[1, 3]] and sampled values [[5]], all valid, have means 2 and 5. The gap is 3, counts are [[2, 1]], and threshold 2 produces flagged = [True].

## Example 2

With the same values and threshold 3, equality is not flagged. If the sampled mask is all false, its mean and the gap are NaN, and flagged is false.
