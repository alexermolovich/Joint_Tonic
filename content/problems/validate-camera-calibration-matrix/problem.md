# Validate a Camera Calibration Matrix

Check a pinhole intrinsic matrix against an explicit image-size and principal-point policy.

```python
def validate_camera_matrix(K, width, height):
```

## Contract

width,height must be built-in or NumPy integers in [1,100000], not bool. K must be finite real (3,3); malformed shapes/types raise ValueError. For well-formed K return True exactly when fx=K[0,0]>0, fy=K[1,1]>0, 0<=cx=K[0,2]<width, 0<=cy=K[1,2]<height, and K[1,0],K[2,0],K[2,1] are within 1e-9 of zero and K[2,2] within 1e-9 of one. Skew K[0,1] is unrestricted within numeric bounds. A well-formed matrix that violates these calibration conditions returns False, not an exception.

**Shapes and outputs:** K(3,3), integer width,height -> Python bool.

**Units:** K: focal lengths,skew,principal point in pixels; homogeneous bottom row dimensionless, width,height: pixels. **Time:** Matrix and image dimensions refer to the same calibrated image stream.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `K=[[500,0,320],[0,510,240],[0,0,1]], width=640, height=480` → `True`.
2. Same K with width=320 → `False` because cx equals the excluded right boundary.
