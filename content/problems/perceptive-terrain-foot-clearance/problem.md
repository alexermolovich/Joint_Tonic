# Evaluate Foot Clearance Across Terrain Slices

Foot height becomes useful only relative to the nearby support surface. Compare observed swing feet against that surface, then retain separate terrain slices so easy ground cannot hide clearance failures elsewhere.

## Contract

Implement `terrain_clearance_report(foot_positions, terrain_height, swing, observed, terrain_ids, minimum_clearance, num_terrains)`.

`foot_positions` has shape `(B,T,F,3)`, where `0 <= B <= 128`, `1 <= T <= 256`, and `1 <= F <= 4`. `terrain_height` has shape `(B,T,F)`. Both use meters in one right-handed world frame with z up, have absolute values at most 10,000, and describe matched timestamps. Each height is a supplied support-surface estimate directly under that foot; no interpolation is required.

`swing` and `observed` are Boolean `(B,T,F)` masks. A sample is eligible only when both are true. `num_terrains` is a built-in Python integer `K` in `[1,64]`; `terrain_ids` is an integer `(B,)` array with values in `[0,K-1]`. Each environment retains one terrain ID throughout the window. `minimum_clearance` has shape `(K,)`, with values in `[0,1]` meters.

Clearance is `foot_positions[...,2] - terrain_height`. Return a dictionary with `clearance` (float64 `(B,T,F)`, NaN outside eligible samples), `counts` (int64 `(K,)`), and `mean_clearance`, `min_clearance`, and `violation_rate` (float64 `(K,)`). The latter three fields are NaN for terrain slices without eligible samples. A violation occurs strictly below that terrain's minimum; equality passes. Negative clearance remains negative and counts as a violation.

Aggregate eligible foot/time samples equally, rather than averaging episodes or weighting elapsed duration. Stance and unobserved samples are excluded. This original diagnostic is not a collision detector or proof of safe walking; terrain-height error directly biases its result.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Example 1

Use one environment, two timestamps, and one foot: `foot_positions=[[[[0.,0.,0.2]],[[0.,0.,0.05]]]]`, zero terrain heights, all swing/observed masks true, `terrain_ids=[0]`, `minimum_clearance=[0.1,0.1]`, and `num_terrains=2`.

Return `clearance=[[[0.2],[0.05]]]`, `counts=[2,0]`, `mean_clearance=[0.125,NaN]`, `min_clearance=[0.05,NaN]`, and `violation_rate=[0.5,NaN]`. Terrain 1 has no evidence.

## Example 2

Change foot z coordinates to `[0.1,-0.2]`, mark only the first sample as swing, keep both observed, and use one terrain with threshold `0.1` m. Return `clearance=[[[0.1],[NaN]]]`, `counts=[1]`, mean and minimum `[0.1]`, and violation rate `[0.]`. Equality passes; the stance row is excluded.
