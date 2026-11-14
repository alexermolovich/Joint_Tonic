# Interpolate a Time-Parameterized Joint Trajectory

**Status: planned; no runnable implementation yet.**

A planner sends joint waypoints at irregular future times, while a controller requests a command on its own clock. Interpolate the desired joint vector and its interval velocity at one query time.

## Contract

Planned function: sample_trajectory(times, positions, query_time).

Times has K≥2 finite strictly increasing entries in seconds. Positions is finite (K,D) with D≥1, in radians for unwrapped joint coordinates. Query time is finite and uses the same clock. Return a new (D,) desired position and (D,) velocity.

Inside an interval, interpolate linearly and report its constant slope. At an interior knot, choose the interval immediately to its right. Before or at the first time, hold the first position with zero velocity. At or after the last time, hold the last position with zero velocity. No extrapolation or shortest-angle wrapping is permitted.

## Assessment plan

Check irregular intervals, multi-joint vectors, exact knots, endpoint holding, invalid time order, and input immutability. Read [examples.md](examples.md). This simple planned sampler does not guarantee acceleration continuity or actuator feasibility.

