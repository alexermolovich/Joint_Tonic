# Solve Closed-Form IK for a Planar Two-Link Arm

**Status: planned.** Choose shoulder and elbow angles that place a planar tool at a target point.

## Contract

Inputs: two finite positive link lengths `L1,L2` in meters and finite base-frame target `[x,y]`. Both joints rotate about +z. Angles are relative to their preceding link, following the forward-kinematics lesson.

Return a record with `reachable`, `angles`, and `singular`. For reachable targets, `angles=[q1,q2]` uses the branch `q2 in [0,pi]`; normalize q1 into `[-pi,pi)`. Mark singular when `abs(sin(q2))<=1e-9`. For unreachable targets return `reachable=False, angles=None, singular=False`.

Reachability requires distance between `abs(L1-L2)` and `L1+L2`. Values outside this annulus by more than `1e-9 m` are unreachable; within the tolerance, clamp the derived cosine to `[-1,1]`. If both lengths are equal and the target is the origin, choose `[0,pi]` by convention.

Reject invalid lengths, shape, nonfinite or complex data. No joint limits, obstacles, desired tool orientation, or motion continuity are imposed.

Read [examples](examples.md), [theory](theory.md), and [hints](hints.md).
