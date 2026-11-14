# One Kalman Filter Predict Step

Propagate a linear robot state estimate and its covariance through one prediction interval.

```python
def kalman_predict(x, P, F, Q):
```

## Contract

No control input is applied. F is any finite square matrix. Return predicted mean F@x and covariance F@P@F.T+Q, symmetrized to remove roundoff. Covariances must be symmetric within absolute tolerance 1e-10 and positive semidefinite (eigenvalues >=-1e-10); use their symmetrized values. n must be between 1 and 32. State components may mix position and velocity when F includes the appropriate seconds factors.

**Shapes and outputs:** x(n,), P/F/Q(n,n), 1<=n<=32 -> (float64(n,),float64(n,n)).

**Units:** x: declared state units, P,Q: products of state units, F: output-state/input-state units. **Time:** F and Q already encode one chosen time interval.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `x=[0,2], P=eye(2), F=[[1,1],[0,1]], Q=diag([0.1,0.2])` → `([2,2], [[2.1,1],[1,1.2]])`.
2. `x=[3], P=[[2]], F=[[1]], Q=[[0]]` → `([3],[[2]])`.

Covariance numerical convention: after symmetrization, accepted eigenvalues in [-1e-10,0) are projected to zero before filtering. Eigenvalues below -1e-10 are rejected. Strictly positive observation/gating covariance still requires eigenvalues >1e-10.
