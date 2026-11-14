# Interpolate a Pose with SLERP

Interpolate translation linearly and orientation along the shortest quaternion arc.

```python
def interpolate_pose(p0, q0, p1, q1, fraction):
```

## Contract

Both quaternions must be nonzero and are normalized with max-component scaling. Fraction lies in [0,1]. Negate normalized q1 if dot(q0,q1)<0 to choose the shorter arc; exactly zero dot is not negated. For adjusted dot>0.9995 use normalized linear quaternion interpolation; otherwise use SLERP. Normalize the final quaternion. Preserve the q0-aligned sign convention, so the returned endpoint quaternion may equal -normalized(q1).

**Shapes and outputs:** positions(3,), quaternions(4,), scalar fraction -> (float64 position(3,), quaternion(4,)).

**Units:** positions: metres, quaternions,fraction: dimensionless. **Time:** fraction parametrizes two synchronized endpoint poses; no timestamp extrapolation.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `p0=[0,0,0], q0=[1,0,0,0], p1=[2,0,0], q1=[0,0,0,1], fraction=0.5` → position `[1,0,0]`, quaternion `[sqrt(0.5),0,0,sqrt(0.5)]`.
2. Same positions, `q0=[2,0,0,0], q1=[-3,0,0,0], fraction=0.5` → position `[1,0,0]`, quaternion `[1,0,0,0]`; opposite signs describe the same orientation.

Quaternion coordinate order is scalar-first (w,x,y,z); both orientations and positions use the same right-handed reference frame.
