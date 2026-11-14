# Project BEV Reference Points into Calibrated Cameras

Implement `project_bev(points: np.ndarray, ego_to_camera: np.ndarray, intrinsics: np.ndarray) -> tuple[np.ndarray, np.ndarray]`.

Project ego-frame reference points into every camera without clipping image bounds.
`points` (N,3), 0<=N<=4096, meters in ego x-forward,y-left,z-up. `ego_to_camera` (C,4,4), 1<=C<=16, rigid transforms mapping ego to optical x-right,y-down,z-forward. Validate R.T@R≈I, det(R)≈1 at absolute tolerance 1e-8 and exact homogeneous last row. `intrinsics` (C,3,3), exact pinhole form [[fx,0,cx],[0,fy,cy],[0,0,1]], fx,fy>=1e-6. Return `(uv, depth)` float64 shapes (C,N,2),(C,N). Depth is camera z in meters. For z>1e-6 return u=fx*x/z+cx,v=fy*y/z+cy. For z<=1e-6 return exact [0,0] sentinel while retaining signed depth. Visibility is a separate problem; a [0,0] pixel is not itself invalid. Inputs are synchronized and undistorted.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. For one identity camera, K=I, points `[[2,4,2],[0,0,-1]]` give uv `[[[1,2],[0,0]]]` and depth `[[2,-1]]`.
2. Add a second camera translated +1 meter along optical x. Point `[0,0,2]` projects to `[0,0]` in camera 0 and `[0.5,0]` in camera 1; both depths are 2 meters.

## Source and scope

[Primary source](https://arxiv.org/abs/2203.17270). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
