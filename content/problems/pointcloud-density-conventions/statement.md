# Validate Point-Cloud Density and Coordinate Conventions

Implement `audit_cloud(points: np.ndarray, unit: str, frame: str, expected_frame: str, voxel_size: float) -> dict`.

Report declared coordinate compatibility and spatial sampling density without guessing a frame from geometry.
`points` is float64 (N,3), 0<=N<=4096. `unit` is exactly "m", "cm", or "mm"; frame and expected_frame are nonempty ASCII identifiers of at most 32 characters using letters/digits/underscore. `voxel_size` is a built-in int/float (not bool), finite in [1e-4,1000], in meters. Convert to meters using the declared unit. Quantize each axis by floor(position_m/voxel_size), anchored at the declared frame origin, including negatives. Return exactly {"frame_matches":bool,"occupied_voxels":int,"points_per_voxel":float,"extent_m":float64(3,)}. Density is N/number_of_occupied_voxels (0 for empty); extent is coordinatewise max-minus-min (zeros for empty). Duplicate points count toward density. Unit conversion changes scale but does not rotate/translate or repair a frame mismatch. No target density threshold or physical surface area is inferred.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Points `[[0,0,0],[50,0,0],[100,0,0]]`, unit="cm", matching frame="base", voxel_size=1 m occupy 2 voxels, density 1.5 points/voxel, extent `[1,0,0]` m.
2. Points `[[-0.01,0,0],[0,0,0]]` in meters with voxel_size=1 occupy 2 voxels because floor(-0.01)=-1. Frame "camera" versus expected "base" reports False without modifying the coordinates.

## Source and scope

[Primary source](https://arxiv.org/abs/1612.00593). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
