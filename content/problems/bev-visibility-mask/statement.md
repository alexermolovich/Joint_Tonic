# Mask Out-of-View and Behind-Camera Samples

Implement `bev_visibility(uv: np.ndarray, depth: np.ndarray, image_sizes: np.ndarray) -> np.ndarray`.

Build a per-camera visibility mask from projections and signed optical depth.
`uv` (C,N,2) float64 stores continuous (u,v) pixels, `depth` (C,N) float64 stores meters, and `image_sizes` (C,2) int64 stores (height,width), each 1..100000. 1<=C<=16,0<=N<=4096. Return bool (C,N), true exactly when depth>1e-6, 0<=u<width, and 0<=v<height. Upper bounds are exclusive. No occlusion test or rounding is performed. Inputs are finite; invalid sentinels must retain nonpositive depth. All cameras and points refer to one synchronized instant.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. uv=`[[[0,0],[4,2],[3.9,2.9]]]`, depth=`[[1,1,1]]`, sizes=`[[3,4]]` returns `[[True,False,True]]`.
2. Three points all at pixel (1,1), depths `[-1,1e-6,2e-6]`, size (2,2), return `[False,False,True]`.

## Source and scope

[Primary source](https://arxiv.org/abs/2203.17270). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
