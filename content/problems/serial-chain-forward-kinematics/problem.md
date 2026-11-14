# Compute Forward Kinematics for a Serial Chain

Compute every joint endpoint and the tool pose of a planar serial chain.

```python
def planar_forward_kinematics(lengths, q):
```

## Contract

Lengths must be positive; angles are relative to the preceding link and may lie outside [-pi,pi]. Base origin is [0,0] with identity orientation. Rotate each link by its joint angle before translating along that rotated link by its length. Return the base and all distal endpoints, plus the homogeneous planar transform mapping tool coordinates into the base frame. No joint limits, collisions, or dynamics.

**Shapes and outputs:** lengths(N,), q(N,), 1<=N<=1000 -> float64 origins(N+1,2), tool_pose(3,3).

**Units:** lengths: metres, q: radians. **Time:** All joint values are one simultaneous static configuration.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `lengths=[1,0.5], q=[pi/2,-pi/2]` → origins `[[0,0],[0,1],[0.5,1]]`, tool pose `[[1,0,0.5],[0,1,1],[0,0,1]]` up to roundoff.
2. `lengths=[2], q=[0]` → origins `[[0,0],[2,0]]`, tool pose `[[1,0,2],[0,1,0],[0,0,1]]`.
