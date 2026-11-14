# Detect Training-Serving Transform Skew

**Local Python exercise · content version 1.0.0.**

Run the same captured observations through training and serving preprocessing. Identify output cells that no longer agree.

## Function contract

~~~python
import numpy as np

def transform_skew(train: np.ndarray, serve: np.ndarray,
                   feature_names: list[str], atol: np.ndarray,
                   rtol: float = 0.0) -> list[tuple[int, str]]:
    ...
~~~

Both matrices must be CPU NumPy arrays with dtype float64, ndim 2, and identical shape (N,D). Row i represents the same observation and timestamp on both sides; columns share units and coordinate frames. The caller provides that alignment and schema. This function does not join timestamps or infer physical metadata.

feature_names is a list of D unique ASCII IDs matching [a-z][a-z0-9_-]{0,63}, in column order. atol is a float64 array with shape (D,), measured in each column's units. rtol is a finite built-in int/float, excluding bool, in [0,1]. All values are finite, with absolute matrix entries at most 1e100 and atol entries in [0,1e100].

A cell fails exactly when:

$$
|\mathrm{serve}_{ij}-\mathrm{train}_{ij}| >
\mathrm{atol}_j+\mathrm{rtol}\,|\mathrm{train}_{ij}|.
$$

Equality passes. Training is the reference for relative tolerance; the comparison is intentionally asymmetric. Return new Python (row_index, feature_name) tuples ordered by ascending row, then ascending **column index**, not feature-name sorting. No rounding, angle wrapping, unit conversion, broadcasting, or input mutation is allowed.

Limits: 0 ≤ N ≤ 10,000 and 0 ≤ D ≤ 128. Output pairs are compared exactly. This is output parity, not a distribution-shift test.

## Errors and empty inputs

Raise ValueError for wrong array/container types, dtype, dimensions, shape alignment, names, numeric bounds, or limits. Error text is not graded. Shapes (0,D) and (N,0) are valid and return [] after validating all arguments. Torch tensors, float32 arrays, NaNs, and infinities are rejected.

## Worked example 1 — equality is acceptable

~~~python
train = np.array([[1., 0.], [2., 0.5]], dtype=np.float64)
serve = np.array([[1.125, 0.25], [2.5, 0.625]], dtype=np.float64)
feature_names = ["depth_m", "yaw_rad"]
atol = np.array([0.125, 0.125], dtype=np.float64)
rtol = 0.0
# Output: [(0, "yaw_rad"), (1, "depth_m")]
~~~

Depth is camera optical-axis depth in metres; yaw is counterclockwise about world +z in radians. Identical frame conventions are assumed on both paths. Differences equal to 0.125 pass.

## Worked example 2 — zero needs absolute tolerance

~~~python
train = np.array([[8., 0.]], dtype=np.float64)
serve = np.array([[9., 0.25]], dtype=np.float64)
feature_names = ["depth_m", "yaw_rad"]
atol = np.array([0., 0.125], dtype=np.float64)
rtol = 0.125
# Output: [(0, "yaw_rad")]
~~~

Depth difference 1 equals its tolerance 0 + 0.125×8. At zero yaw the relative term contributes zero, so difference 0.25 exceeds tolerance 0.125.

## Runtime budget

CPython 3.12.3 on the isolated local CPU worker, NumPy 2.2.4. Limits: 10 CPU seconds, 18 wall seconds, 4 GiB address space per process, and 64 KiB output. No simulator or network access is required.
