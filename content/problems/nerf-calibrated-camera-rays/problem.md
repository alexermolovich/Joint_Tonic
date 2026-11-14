# Generate Calibrated Camera Rays

Implement `camera_rays(pixels: np.ndarray, intrinsics: np.ndarray, camera_to_world: np.ndarray) -> tuple[np.ndarray, np.ndarray]`.

Turn supplied continuous pixel coordinates into world-space unit rays.
`pixels` is (N,2), 0<=N<=4096, ordered (u,v) in pixels; values may lie outside an image. `intrinsics` is (3,3), exactly [[fx,0,cx],[0,fy,cy],[0,0,1]], fx,fy>=1e-6. `camera_to_world` is (4,4): last row [0,0,0,1], rotation R satisfies R.T@R≈I and det(R)≈1 with absolute tolerance 1e-8, translation t in meters. Camera axes are x right,y down,z forward; world axes are caller-declared right-handed axes. Return origins (N,3), each t, and normalized world directions (N,3). Use d_c=[(u-cx)/fx,(v-cy)/fy,1]; rotate with R then normalize. No pixel-center offset is added: callers supply their chosen centers. No distortion, NDC conversion, scene normalization, or ray sampling occurs.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. With identity intrinsics/pose, pixels `[[0,0],[1,0]]` yield origins `[[0,0,0],[0,0,0]]`, directions `[[0,0,1],[1/√2,0,1/√2]]`.
2. With fx=fy=2,cx=cy=1, pixel `[[1,1]]` and identity rotation plus translation `[3,0,2]`, the ray starts `[3,0,2]` and points `[0,0,1]`. Translation changes origin, never direction.

## Source and scope

[Primary source](https://arxiv.org/abs/2003.08934). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
