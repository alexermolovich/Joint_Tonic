# Evaluate a Relocalization Candidate

Implement `relocalization_coverage(keypoints, landmark_ids, inliers, image_size, grid_size, min_landmarks, min_cells)`.

Evaluate relocalization candidates using distinct geometric landmarks and image coverage.

`keypoints (N,2)` is float64 `(x,y)` pixels, `0<=N<=4096`, within the closed center domain `[0,width-1] x [0,height-1]`. `landmark_ids (K,N)` is int64, `1<=K<=128`, entries -1 (unmatched) or 0..1_000_000_000. `inliers (K,N)` is bool; every True must refer to a nonnegative landmark ID. `image_size` is int64 `[height,width]`, each 1..4096; `grid_size` int64 `[rows,columns]`, each 1..64. `min_landmarks` is a Python int in 1..4096; `min_cells` a Python int in 1..grid_rows*grid_columns.

For each candidate, keep only its geometrically inlier feature observations. Deduplicate landmark IDs by retaining the lowest feature index for each ID. Count distinct landmark representatives and the grid cells occupied by THESE representatives. Cell indices are `row=floor(y*grid_rows/height)`, `column=floor(x*grid_columns/width)`.

Return int64 `unique_landmarks (K,)`, int64 `covered_cells (K,)`, bool `eligible (K,)` requiring both counts >=their thresholds, int64 `order (E,)` sorted by descending unique-landmark count, descending cell count and ascending candidate index, and Python int `best` first eligible or -1. No evidence yields zero counts and no eligible candidate. This is an original operational gate over supplied geometric inliers, not place recognition, pose estimation or a full ORB-SLAM2 relocalizer.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Keypoints `[[0.,0.],[3.,3.]]` in a `[4,4]` image and `[2,2]` grid, candidate landmark IDs `[[7,7]]`, both geometric inliers: unique_landmarks=1 and covered_cells=1. Only feature index 0 represents landmark 7.
2. Change IDs to `[[7,8]]`: both counts become 2. With min_landmarks=2 and min_cells=2 this candidate becomes eligible; the duplicated-ID candidate does not.

## Source and scope

[Primary source](https://arxiv.org/abs/1610.06475). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
