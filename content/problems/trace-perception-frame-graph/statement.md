# Trace Frames Through a Robot Perception Graph

Resolve a rigid transform between two frames in a validated acyclic frame forest.

```python
def resolve_frame_transform(edges, source, target):
```

## Contract

Frame names match ASCII [a-z][a-z0-9_]{0,31}. Each child has at most one parent; reject cycles, self-edges, repeated children, and malformed transforms even in disconnected components. Rigid matrices use atol=1e-8 for orthogonality, determinant +1 and bottom row. Both query names must occur in the graph. Return T_target_source along the unique undirected path, inverting edges when needed. Same known source/target returns identity. Disconnected queries raise ValueError. Edges must be a list of tuples of length3.

**Shapes and outputs:** list of up to128 (parent:str,child:str,T(4,4)) tuples, source/target str -> fresh float64(4,4).

**Units:** translation: metres, rotation: dimensionless. **Time:** Every edge belongs to the same synchronized calibration snapshot; no time interpolation.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. Let T_base_wrist translate `[1,0,0]` and T_wrist_camera translate `[0,2,0]`. Resolving source="camera", target="base" returns translation `[1,2,0]` with identity rotation.
2. Reversing those query frames returns translation `[-1,-2,0]`. A known frame to itself returns identity.
