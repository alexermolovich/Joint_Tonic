# One Kalman Filter Measurement Update

Fuse a linear sensor measurement using a stable Kalman gain and Joseph covariance update.

```python
def kalman_update(x, P, z, H, R):
```

## Contract

Covariances must be symmetric within absolute tolerance 1e-10 and positive semidefinite (eigenvalues >=-1e-10); use their symmetrized values. R must additionally be strictly positive definite with eigenvalues >1e-10. Return updated float64 state and Joseph-form covariance, symmetrized. H maps the state to expected sensor readings; no bias term. Both state and measurement dimensions are between 1 and 32. Solve linear systems; an explicit inverse is unnecessary.

**Shapes and outputs:** x(n,), P(n,n), z(m,), H(m,n), R(m,m), 1<=n,m<=32 -> (mean(n,), covariance(n,n)).

**Units:** x: state units, z: sensor units, P: products of state units, R: products of sensor units. **Time:** Prior and measurement represent the same timestamp.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `x=[0], P=[[1]], z=[2], H=[[1]], R=[[1]]` → `([1],[[0.5]])`.
2. `x=[3], P=[[0]], z=[10], H=[[1]], R=[[2]]` → `([3],[[0]])`; an exactly known prior receives zero gain.

Covariance numerical convention: after symmetrization, accepted eigenvalues in [-1e-10,0) are projected to zero before filtering. Eigenvalues below -1e-10 are rejected. Strictly positive observation/gating covariance still requires eigenvalues >1e-10.
