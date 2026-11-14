# Enforce Velocity and Acceleration Limits

Generate joint commands by projecting requested velocities into velocity and acceleration limits.

```python
def limit_joint_commands(initial_position, initial_velocity, targets, dt, max_velocity, max_acceleration):
```

## Contract

D>=1. dt is positive scalar; per-joint velocity and acceleration limits are positive. Initial velocity must satisfy its limits. At each step compute desired_velocity=(target-current_position)/dt. Clip to intersection [-max_velocity,max_velocity] and [previous_velocity-max_acceleration*dt,previous_velocity+max_acceleration*dt], then advance position by clipped_velocity*dt. Empty targets (0,D) produce empty outputs. Targets need not be reached; no joint position or collision constraints are enforced.

**Shapes and outputs:** initial_position/velocity(D,), targets(T,D), max_velocity/acceleration(D,) -> float64 positions(T,D), velocities(T,D).

**Units:** positions,targets: radians, velocities: radians/second, acceleration: radians/second², dt: seconds. **Time:** Each target is requested at the end of one fixed positive dt interval.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `initial_position=[0], initial_velocity=[0], targets=[[10],[10],[10]], dt=1, max_velocity=[2], max_acceleration=[1]` → positions `[[1],[3],[5]]`, velocities `[[1],[2],[2]]`.
2. `initial_position=[0], initial_velocity=[2], targets=[[-10]], dt=1, max_velocity=[2], max_acceleration=[1]` → position `[[1]]`, velocity `[[1]]`; braking cannot reverse velocity instantly.

dt must be at least 1e-9 seconds; smaller values raise ValueError.
