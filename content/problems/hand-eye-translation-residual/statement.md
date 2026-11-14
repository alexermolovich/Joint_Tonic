# Solve a Small Hand-Eye Calibration Residual

Solve the translation component of AX=XB with a supplied hand-eye rotation and report per-pair residuals.

```python
def solve_hand_eye_translation(A, B, rotation):
```

## Contract

All transforms must be proper rigid matrices: bottom row [0,0,0,1], rotation orthogonality and determinant +1 within atol=1e-8. Rotation is the fixed, already estimated R_X; this problem does not estimate it. Stack C_i=R_Ai-I and d_i=R_X t_Bi-t_Ai. Solve min_t ||Ct-d||² using np.linalg.lstsq rcond=1e-10. Raise ValueError if its reported rank<3. Return t and (Ct-d).reshape(N,3), including nonzero residuals for noisy/inconsistent data. Do not enforce the rotational AX=XB equation; only the translation residual is solved.

**Shapes and outputs:** A/B(N,4,4), rotation(3,3), 2<=N<=1000 -> translation float64(3,), residuals float64(N,3).

**Units:** translations,residuals: metres, rotations: dimensionless. **Time:** A[i],B[i] are corresponding relative motions from synchronized pose pairs.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. Let both A translations be zero, R_A1=diag(1,-1,-1), R_A2=diag(-1,1,-1), and R_X=I. Use B with the same respective rotations and translations `[0,-4,-6]`, `[-2,0,-6]`. Return t=`[1,2,3]` and zero residuals.
2. Same rotations with every A/B translation zero returns t=`[0,0,0]` and zero residuals. Repeating only the first rotation instead must raise ValueError.
