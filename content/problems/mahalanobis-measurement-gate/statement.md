# Gate Measurements with Mahalanobis Distance

Accept sensor innovations using their squared covariance-normalized distance.

```python
def gate_measurements(residuals, covariance, threshold):
```

## Contract

Covariance is symmetric within atol=1e-10; symmetrize it and require all eigenvalues >1e-10. Threshold is a nonnegative scalar. Distances are squared Mahalanobis distances. Accept equality at the threshold. Empty batches (0,D) are valid; D must be 1..32. No chi-square threshold selection is performed.

**Shapes and outputs:** residuals(N,D), covariance(D,D), scalar threshold -> (float64 distances(N,), bool accepted(N,)); 1<=D<=32.

**Units:** residuals: sensor units, covariance: products of sensor units, threshold: dimensionless squared distance. **Time:** All residuals use the same measurement model and covariance at a common evaluation interval.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `residuals=[[2,0],[0,2]], covariance=diag([4,1]), threshold=1` → distances `[1,4]`, accepted `[True,False]`.
2. `residuals=[[0]], covariance=[[2]], threshold=0` → `([0],[True])`.

Covariance numerical convention: after symmetrization, accepted eigenvalues in [-1e-10,0) are projected to zero before filtering. Eigenvalues below -1e-10 are rejected. Strictly positive observation/gating covariance still requires eigenvalues >1e-10.
