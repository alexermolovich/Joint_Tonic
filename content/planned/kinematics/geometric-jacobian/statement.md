# Build a Geometric Jacobian from Joint Axes

**Status: planned.** Determine how each joint's motion changes the tool's instantaneous linear and angular velocity.

## Contract

Inputs are finite joint origins `origins (N,3)` in meters, unit joint axes `axes (N,3)`, joint types `R` or `P`, and tool origin `p_tool (3,)`. Every vector is expressed in the same right-handed base frame at one configuration. `N>=1`.

Return a new float64 geometric Jacobian `J (6,N)`, with **linear velocity rows first**, angular velocity rows last. For revolute joints, joint rates use rad/s; for prismatic joints they use m/s. The resulting twist is base-frame `[vx,vy,vz,wx,wy,wz]`.

A revolute column uses its axis cross its lever arm for the linear part and the axis for the angular part. A prismatic column uses its axis for linear motion and zero angular motion.

Reject unknown types, mismatched shapes, nonfinite values, and axes whose norm differs from one by more than `1e-7`. Do not silently renormalize. Return geometry only; no inverse or joint command is requested.

See [examples](examples.md), [theory](theory.md), and [hints](hints.md).
