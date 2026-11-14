## Example 1

Use one environment, two timestamps, and one foot: `foot_positions=[[[[0.,0.,0.2]],[[0.,0.,0.05]]]]`, zero terrain heights, all swing/observed masks true, `terrain_ids=[0]`, `minimum_clearance=[0.1,0.1]`, and `num_terrains=2`.

Return `clearance=[[[0.2],[0.05]]]`, `counts=[2,0]`, `mean_clearance=[0.125,NaN]`, `min_clearance=[0.05,NaN]`, and `violation_rate=[0.5,NaN]`. Terrain 1 has no evidence.

## Example 2

Change foot z coordinates to `[0.1,-0.2]`, mark only the first sample as swing, keep both observed, and use one terrain with threshold `0.1` m. Return `clearance=[[[0.1],[NaN]]]`, `counts=[1]`, mean and minimum `[0.1]`, and violation rate `[0.]`. Equality passes; the stance row is excluded.
