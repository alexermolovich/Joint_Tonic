# Solution: mask depth before dividing

Validate points and the constrained pinhole intrinsic matrix. Allocate a `(N,2)` float64 array filled with NaNs, and copy the z column into `depths`. Compute `front=depths>1e-8`; only those rows participate in perspective division.

```python
pixels[front, 0] = K[0,0] * points[front,0] / depths[front] + K[0,2]
pixels[front, 1] = K[1,1] * points[front,1] / depths[front] + K[1,2]
```

Combine `front` with four half-open bounds comparisons for the boolean mask. NaN comparisons are false, but retaining `front` explicitly communicates the intended contract. Do not clip pixels: a point outside the image must retain its true coordinate for debugging and later geometry.

The algorithm uses O(N) work and output memory. A loop over points is unnecessary. An inverse-intrinsics or homogeneous-matrix approach can be useful elsewhere, but the direct formula makes this task's units and depth policy easy to verify.
