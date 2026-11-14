# Evaluate Offline Policy Support

Offline action support is local to the state where an action was observed. An identical action at another state provides no evidence under this explicitly finite-state diagnostic.

## Contract

`logged_states` is integer `(N,)`, `logged_actions` is real `(N, D)`, `query_states` is integer `(M,)` and `query_actions` is real `(M, D)`. Bounds are `0 <= N <= 1024`, `0 <= M <= 256`, `1 <= D <= 16`. State identifiers lie in `[0, 1_000_000]`; action coordinates lie in `[-1, 1]`. `max_distance` is a scalar in `[0, 10]`.

For each query, find the logged action with the **same discrete state identifier** and minimum Euclidean action distance. Break equal-distance ties by the smallest original logged row index. Return a dictionary containing `nearest_index` (int64 `(M,)`), `distance` (float64 `(M,)`) and `unsupported` (Boolean `(M,)`). Missing state support produces index -1, NaN distance and true unsupported status. Otherwise unsupported is true only when the distance strictly exceeds `max_distance`; equality passes.

This original finite-state diagnostic is not a continuous-state density estimator or a policy performance guarantee.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Actions and image intensities are normalized and dimensionless. Q values and rewards use a fixed reward scale; squared losses use squared reward units. All views in a row describe the same transition. No physical simulation or implicit coordinate conversion runs. Original bounded teaching component using supplied arrays; not a reproduction of trained policy performance or the full paper.

## Example 1

Logged states [0, 0] with actions [[0], [1]] and query state [0] with action [[0.5]] produce nearest index [0] and distance [0.5]. At threshold 0.5, unsupported is false; equal-distance ties choose the first row.

## Example 2

The same query action at state 1 has no matching logged state: nearest index [-1], distance [NaN] and unsupported [True].
