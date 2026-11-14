# Combine Competing Task-Space Accelerations

Implement `combine_policies(metrics, accelerations)`.

Combine supplied acceleration policies that already share one normalized coordinate space.

`metrics` is float64 `(K,D,D)`, `accelerations` float64 `(K,D)`, `1<=K<=64`, `1<=D<=16`. Coordinates are dimensionless under a common fixed normalization; accelerations are 1/s², metrics dimensionless. All policies describe the same configuration, time and axes. Policies in different task spaces must first be pulled into the common space.

For every metric use this numerical PSD rule: validate symmetry with atol=1e-10, rtol=0; symmetrize; reject eigenvalues below -1e-10; clip accepted negative eigenvalues to zero and reconstruct. Let M=sum of these effective metrics and f=sum of M[k]@accelerations[k]. Resolve with the symmetric eigendecomposition of M, retaining only eigenvalues strictly greater than `1e-10 * largest_eigenvalue`. Set inverse values of all other eigenvalues to zero. An all-zero M resolves to the zero acceleration and rank 0.

Return a dictionary with fresh float64 `metric (D,D)`, `force (D,)`, `acceleration (D,)`, and Python int `rank` counting retained eigenvalues. There is no additive damping or normalization by K. This operation resolves a bounded weighted composition; it does not construct the RMP tree or ensure stability of arbitrary supplied policies.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Two scalar metrics `[[[1.]],[[3.]]]` and accelerations `[[2.],[-2.]]` yield metric `[[4.]]`, force `[-4.]`, acceleration `[-1.]`, rank `1`.
2. One metric `diag([1.,0.])` and acceleration `[[2.,9.]]` yield force `[2.,0.]`, resolved acceleration `[2.,0.]`, rank `1`. The unweighted direction is set to zero.

## Source and scope

[Primary source](https://arxiv.org/abs/1811.07049). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
