# Window Proprioceptive History

Adaptation history records what the robot observed and did before the current decision. Left-pad missing history instead of borrowing from another episode or including the current command.

## Contract

`observations` is real `(N, O)`, `actions` is real `(N, A)`, `episode_ids` is integer `(N,)` and `query_indices` is integer `(Q,)`. Bounds are `1 <= N <= 4096`, `1 <= O, A <= 32`, `0 <= Q <= 128`. Episode IDs are nonnegative and nondecreasing; queries lie in `[0, N)`. `history_length` is a built-in Python int in `[1, 64]`. Numeric observation/action magnitudes are at most 100.

Records use a common fixed control period. Observations and commands are normalized dimensionless channels; each command is issued after its same-row observation. For query row t, take H previous candidate rows `[t-H, t)`, retaining only nonnegative rows in the query's episode. Left-pad missing rows with zeros. Never include the query row itself.

Return a dictionary with `history` (float64 `(Q, H, O+A)`, observation channels followed by action channels), `valid` (Boolean `(Q, H)`) and `source_indices` (int64 `(Q, H)`, original row indices or -1 for padding). Preserve query order. Do not interpolate or carry history across episode boundaries.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Normalized observations, extrinsics, actions and latents are dimensionless. Timestamps and ages use seconds. Synchronized fixed-period state/action history; episode and completion boundaries explicit. No implicit frame or clock conversion. Original bounded adaptation teaching component. Frozen encoder and temporal alternatives do not reproduce the complete trained RMA networks or hardware benchmark.

## Example 1

Observations [[1], [2], [3]], actions [[0.1], [0.2], [0.3]], episode IDs [0, 0, 0], query [2] and H=3 produce history [[[0, 0], [1, 0.1], [2, 0.2]]], validity [[False, True, True]] and indices [[-1, 0, 1]].

## Example 2

Changing episode IDs to [0, 0, 1] makes query 2 the first row of a new episode. Its previous-history window is entirely padded.
