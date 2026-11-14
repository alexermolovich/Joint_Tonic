# Integrate Differential-Drive Wheel Odometry

**Status: planned.** Estimate a mobile robot's new planar pose from the signed travel of its two driven wheels.

## Contract

Input pose is finite `[x,y,theta]`: meters in a fixed right-handed world frame and heading radians counterclockwise from world +x. Robot +x points forward; +y points left. Inputs `left_travel` and `right_travel` are signed distances in meters during the same interval; positive means rolling forward. Track width `b` is finite and strictly positive.

Assume ideal no-slip differential drive and constant wheel-velocity ratio over the interval. Return a new pose after integrating the resulting constant twist exactly. Normalize returned heading into `[-pi,pi)`. Straight travel is the continuous zero-turn limit; use a numerically stable formulation near zero.

Reject bad shapes, nonfinite/complex values, or nonpositive track width. The interval's duration is unnecessary because the inputs are travel, not rates. Do not estimate uncertainty, correct slip, or fuse other sensors.

See [examples](examples.md), [theory](theory.md), and [hints](hints.md).
