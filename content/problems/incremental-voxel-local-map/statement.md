# Update an Incremental Local Map

Implement `update_local_map(existing, scan, world_from_lidar, center, half_extent, voxel_size)`.

`update_local_map(existing, scan, world_from_lidar, center, half_extent, voxel_size)` existing(M,3)world points,scan(N,3)lidar points,M/N0..16384, abs<=1e4; transformproper withtranslation abs<=1e4;center(3)world meters abs<=1e4;half_extent(3)meters[1e-3,1e4],voxelscalar [1e-3,1000]meters.

Transform scan into world coordinates; merge candidates in existing-then-scan index order.

Keep points in inclusive axis-aligned center±extent.

Voxel key=floor(worldpoint/size),global origin fixed zero,negative coordinates use floor.

Within each occupied voxel retain candidate closest in squared meters to voxel center (key+.5)*size, tie lower merged candidate index.

Return points(V,3),voxel_keys(V,3)int64,source_indices(V)int64(sorted lexicographic voxel keys),removed_existing(M)bool true iff existing point not retained (outside or loses voxel selection).

Candidate identity from concatenation.

Deterministic batch teaching equivalent of pruning/downsampling decisions; no incremental ikd-tree, runtimeclaim or scan deskew.

Example: existing[[.1,0,0],[.4,0,0]],scan[[.6,0,0]],I,center0,extent2,voxel1=>selectexistingindex1 (equal .4/.6 center distances tie earlier),key[0,0,0],removed[True,False].

Example: existing[[-.1,0,0]],scan zero,I,size1=>keys[-1,0,0],[0,0,0] distinct.

Implementation should handle up to 32768 candidates without quadratic pairwise arrays.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool.

Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated.

All malformed types, shapes, ranges, or scalar arguments raise ValueError.

Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias).

CPU only; no implicit batch dimension.

Comparisons use rtol=1e-6 and atol=1e-7.

Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Existing points [[0.1,0,0],[0.4,0,0]], incoming [[0.6,0,0]], identity pose, center [0,0,0], half extents [2,2,2] and voxel size 1 select existing index 1.

Points 0.4 and 0.6 tie around center 0.5, so the earlier candidate wins.

Removed-existing flags are [True,False].
2. Existing [-0.1,0,0] and incoming [0,0,0] belong to voxel keys [-1,0,0] and [0,0,0].

Negative coordinates use floor, not truncation toward zero.

## Source and scope

[Primary source](https://arxiv.org/abs/2107.06829).

This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
