# Build Homography-Supervised Descriptor Correspondence Targets

Implement `descriptor_targets(source_centers, target_centers, target_from_source, source_valid, target_valid, tolerance)`.

Create geometric correspondence labels for descriptor-grid centers using a known homography.

`source_centers (N,2)` and `target_centers (M,2)` are float64, `0<=N,M<=512`. They are already expressed in full-resolution `(x,y)` pixels; no stride conversion is implicit. `source_valid (N,)` and `target_valid (M,)` are bool masks. `target_from_source (3,3)` is float64 with absolute entries <=1000 and absolute determinant >=1e-9. It maps source homogeneous pixels into target pixels without automatic scale normalization. `tolerance` is a Python int/float in `[0,100]` target-image pixels.

A projected source is supported only when its absolute homogeneous denominator is strictly >1e-9. A pair is supported if both masks and this projection test pass. Return a dictionary with float64 `distances (N,M)`, Euclidean target-pixel distance for supported pairs and NaN otherwise, and bool `correspondence (N,M)`, True exactly for supported distances <=tolerance. Image bounds are not supplied: masks define valid grid centers. This isolates homography-based labels with a selectable tolerance; it does not implement the descriptor hinge loss or complete training procedure.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Identity warp, source centers `[[0.,0.],[2.,0.]]`, target centers `[[0.,0.],[1.,0.]]`, all valid, tolerance 1: distances `[[0.,1.],[2.,1.]]`, labels `[[True,True],[False,True]]`.
2. With the first source marked invalid, its entire distance row is NaN and its labels are False. The second row is unchanged.

## Source and scope

[Primary source](https://arxiv.org/abs/1712.07629). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
