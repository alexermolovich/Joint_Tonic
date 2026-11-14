# Apply Radial and Tangential Lens Distortion

Apply a five-coefficient radial/tangential lens model to normalized image-plane points.

```python
def distort_normalized_points(points, coefficients):
```

## Contract

Coefficient order is [k1,k2,p1,p2,k3]. Points must have absolute coordinates <=10; coefficients absolute values <=1. Empty points (0,2) are valid. Apply the Brown-Conrady polynomial written in Theory. No inverse distortion, camera intrinsics, pixel clipping, or fisheye model.

**Shapes and outputs:** points(N,2), coefficients(5,) -> fresh float64(N,2).

**Units:** points: dimensionless x=X/Z,y=Y/Z, coefficients: dimensionless. **Time:** One fixed calibration snapshot applies to all points.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `points=[[1,0],[0,1]], coefficients=[0.1,0,0,0,0]` → `[[1.1,0],[0,1.1]]`.
2. `points=[[1,0]], coefficients=[0,0,0.1,0.2,0]` → `[[1.6,0.1]]`.
