# Build a Pre-Grasp Pose Along the Tool Axis

**Status: planned; no runnable implementation yet.**

A grasp predictor supplies a target gripper pose. Construct a pre-grasp pose that starts a given distance away along the gripper's negative approach axis while preserving the target orientation.

## Contract

Planned function: pregrasp_pose(T_world_grasp, distance).

The finite proper SE(3) transform maps grasp-frame coordinates into world coordinates; translation is meters. The gripper approaches its target by moving in its own positive z direction. Distance is a finite nonnegative scalar in meters.

Return a new proper world-from-pregrasp transform with the same rotation and translation shifted by minus distance times the world-space grasp z-axis. Validate the rotation/bottom row using the same tolerances as the live SE(3) problem. Reject malformed transforms, negative distance, and nonfinite inputs. Zero distance returns an independent copy of the target transform.

## Scope and assessment

The result is a candidate pose, not a proof of a reachable or collision-free approach. Wrist-to-tool calibration and grasp width belong to separate interfaces. Grade rotated tools, zero offset, preserved orientation, distance, and frame direction. Read [examples.md](examples.md). This folder is planned and not runnable.

