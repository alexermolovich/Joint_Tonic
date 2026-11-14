# Stabilize Singular IK with Damped Least Squares

Compute a regularized joint-space correction that remains bounded near singular Jacobians.

```python
def damped_ik_step(jacobian, error, damping):
```

## Contract

Damping is strictly positive. Solve the unique minimizer of ||J*dq-error||²+damping²||dq||². Return dq and predicted residual J@dq-error. Use singular-value filtering or a stable equivalent; avoid forming an inverse. The inputs are normalized coordinates with units/scales already made comparable by the caller. Zero and rank-deficient J are supported.

**Shapes and outputs:** J(M,N), error(M,), scalar damping -> float64 correction(N,), residual(M,); 1<=M,N<=32.

**Units:** jacobian: normalized task coordinate per normalized joint coordinate, error: normalized task coordinates, damping: task/joint scale ratio. **Time:** One static linearized IK iteration, not a physical motion command.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `jacobian=[[1,0],[0,0]], error=[2,3], damping=1` → correction `[1,0]`, residual `[-1,-3]`.
2. `jacobian=[[1,1]], error=[2], damping=1` → correction `[2/3,2/3]`, residual `[-2/3]`.

Damping must be at least 1e-9; smaller values raise ValueError. This lower bound avoids underflow in the squared damping term.
