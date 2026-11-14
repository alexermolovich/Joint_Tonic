# Enforce Joint Limits and Collision Constraints in IK

Reject planar IK candidates violating joint limits or link-obstacle clearance, then rank the survivors.

```python
def select_safe_ik_candidate(lengths, candidates, joint_limits, obstacles, target, margin):
```

## Contract

Lengths positive, N<=1000, K<=100. Limits rows [lower,upper] require lower<=upper; boundaries are allowed. Obstacles rows [center_x,center_y,radius] require radius>=0. Margin>=0 inflates each obstacle. A candidate collides if the minimum Euclidean distance from either closed link segment to any center is <=radius+margin; touching counts as collision. Reject candidates outside either joint range without clipping. Among survivors choose smallest Euclidean endpoint-target distance, with exact ties choosing lower input index. Return exactly {"index": Python int,"q":float64(2,),"point":float64(2,),"error":Python float}; return None if none survive. Empty arrays retain (0,2)/(0,3) shapes. Validate all inputs even if an early winner exists.

**Shapes and outputs:** lengths(2,), candidates(N,2), limits(2,2), obstacles(K,3), target(2,), scalar margin -> dict or None.

**Units:** lengths,obstacles,target,margin: metres, candidates,joint_limits: radians. **Time:** Each candidate is a static configuration; paths between candidates are not checked.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `lengths=[1,1], candidates=[[0,0],[pi/2,0]], joint_limits=[[-pi,pi],[-pi,pi]], obstacles=empty((0,3)), target=[2,0], margin=0` selects index0, q `[0,0]`, point `[2,0]`, error0.
2. Add obstacle `[0.5,0,0.1]`. Candidate0 crosses it, so select index1 with point approximately `[0,2]` and error `sqrt(8)`.

Each link length must be at least 1e-9 metres; smaller values raise ValueError.
