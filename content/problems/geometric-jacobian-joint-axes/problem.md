# Compute a Geometric Jacobian from Joint Axes

Convert base-frame joint axes and origins into a linear-first tool geometric Jacobian.

```python
def geometric_jacobian(origins, axes, joint_types, tool):
```

## Contract

Joint types must be strings "R" or "P". Each axis norm must differ from 1 by at most 1e-7; do not silently renormalize. Top three rows map joint rates to tool-origin linear velocity; bottom three map to angular velocity. Revolute column is concatenate(cross(axis,tool-origin),axis); prismatic column is concatenate(axis,zeros(3)). The types container must be a list or tuple.

**Shapes and outputs:** origins/axes(N,3), joint_types list/tuple(N), tool(3,) -> float64 J(6,N); 1<=N<=1000.

**Units:** origins,tool: metres, axes: dimensionless unit vectors, joint_rates: revolute rad/s; prismatic m/s, twist: linear m/s then angular rad/s. **Time:** All origins and axes describe the same static robot configuration.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `origins=[[0,0,0]], axes=[[0,0,1]], joint_types=["R"], tool=[2,0,0]` → column `[0,2,0,0,0,1]`.
2. Same origin/tool with `axes=[[1,0,0]], joint_types=["P"]` → column `[1,0,0,0,0,0]`.
