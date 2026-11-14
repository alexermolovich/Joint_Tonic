# Compute a Differential-Drive Rollout

Integrate piecewise-constant wheel rates into an exact planar differential-drive pose sequence.

```python
def differential_drive_rollout(initial_pose, wheel_rates, dt, radius, track):
```

## Contract

dt, wheel radius and wheel-center track width are positive scalars. First output is the initial pose with yaw wrapped into [-pi,pi). Each rate row is held constant for dt. Use exact circular-arc integration; zero angular velocity must reduce continuously to straight motion. Every returned yaw is wrapped into [-pi,pi). Empty rate arrays (0,2) return one initial pose.

**Shapes and outputs:** initial_pose(3,), wheel_rates(T,2), dt/radius/track scalar -> float64(T+1,3).

**Units:** pose: x,y metres; yaw radians, wheel_rates: left,right radians/second, dt: seconds, radius,track: metres. **Time:** One common monotonic clock in seconds.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `initial_pose=[0,0,0], wheel_rates=[[1,1],[1,1]], dt=1, radius=1, track=2` → `[[0,0,0],[1,0,0],[2,0,0]]`.
2. Same parameters with one rate row `[[0,2]]` → final `[sin(1),1-cos(1),1]`, approximately `[0.84147098,0.45969769,1]`.

dt, radius and track must each be at least 1e-9 in their declared units; smaller values raise ValueError.
