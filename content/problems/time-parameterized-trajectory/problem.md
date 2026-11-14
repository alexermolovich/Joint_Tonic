# Interpolate a Time-Parameterized Trajectory

Sample a piecewise-linear joint trajectory and its segment velocity at requested times.

```python
def sample_trajectory(times, positions, queries):
```

## Contract

T>=2, D>=1. Times must be strictly increasing. Queries may be unsorted or empty but must lie in [times[0],times[-1]]. Interpolate linearly. At an interior knot return the velocity of the segment to its right; at the final knot use the last segment. No angular wrapping, extrapolation, or smoothing.

**Shapes and outputs:** times(T,), positions(T,D), queries(M,) -> float64 position(M,D), velocity(M,D).

**Units:** times,queries: seconds, positions: radians, velocity: radians/second. **Time:** One common monotonic clock in seconds.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `times=[0,1,3], positions=[[0],[2],[4]], queries=[0.5,1,3]` → positions `[[1],[2],[4]]`, velocities `[[2],[1],[1]]`.
2. `times=[0,2], positions=[[0,2],[4,0]], queries=[2,0]` → positions `[[4,0],[0,2]]`, velocities `[[2,-1],[2,-1]]`.

Adjacent knot intervals must be at least 1e-9 seconds; smaller intervals raise ValueError.
