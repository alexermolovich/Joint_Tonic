# Worked examples

1. Keypoints `[[0.,0.],[3.,3.]]` in a `[4,4]` image and `[2,2]` grid, candidate landmark IDs `[[7,7]]`, both geometric inliers: unique_landmarks=1 and covered_cells=1. Only feature index 0 represents landmark 7.
2. Change IDs to `[[7,8]]`: both counts become 2. With min_landmarks=2 and min_cells=2 this candidate becomes eligible; the duplicated-ID candidate does not.
