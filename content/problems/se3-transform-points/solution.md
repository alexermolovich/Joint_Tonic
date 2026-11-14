# Solution: rotate rows, then translate

Convert both inputs to float64 arrays and reject invalid shapes or nonfinite numbers. Check the homogeneous bottom row and proper rotation constraints before doing geometry. Once validated, extract `R=T[:3,:3]` and `t=T[:3,3]`.

```python
result = points @ R.T + t
```

This is the transposed form of the column-vector equation. It supports `(3,)`, `(N,3)`, and `(0,3)` without a special loop or reshaping branch. Matrix multiplication and addition allocate new storage.

The numerical part uses O(N) work and O(N) result memory. Validation also examines O(N) point values. A correct alternative may append homogeneous ones and multiply by the 4x4 matrix, but it allocates an unnecessary fourth coordinate for every point.

To debug a failing sign or axis case, test the origin and each basis vector separately. The origin should become `t`; each transformed basis displacement relative to `t` should equal a column of `R`. For a recorded pipeline, retain the calibration and frame convention with the evaluator version.
