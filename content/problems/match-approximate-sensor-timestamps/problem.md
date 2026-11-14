# Match Approximate Sensor Timestamps

Associate each query with its nearest reference timestamp within a fixed tolerance.

```python
def match_timestamps(reference, queries, tolerance):
```

## Contract

Reference times are strictly increasing; either vector may be empty. Tolerance is a nonnegative scalar. Match each query independently; reference reuse is allowed. Nearest-time ties choose the lower index. Return -1 if the absolute offset exceeds tolerance. Queries need not be sorted.

**Shapes and outputs:** reference (N,), queries (M,); output int64 (M,).

**Units:** times: seconds, tolerance: seconds. **Time:** One common monotonic clock in seconds.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `reference=[0,1,2], queries=[0.1,0.5,1.9], tolerance=0.2` → `[0,-1,2]`. The middle sample is too far from both neighbors.
2. `reference=[0,2], queries=[1,0,2], tolerance=1` → `[0,0,1]`. The exact midpoint uses the earlier reference.
