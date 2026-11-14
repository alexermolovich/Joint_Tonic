---
schema_version: 1
slug: differential-drive-odometry
title: Integrate Differential-Drive Wheel Odometry
status: planned
difficulty: Medium
domain: State estimation
prerequisites: [compose-frame-transforms, interpolate-joint-state]
paper_applications: [2016-orb-slam-2, 2019-vins-fusion]
assessment: "Exact constant-twist arc, straight limit, in-place rotation, heading convention."
simulator: "MuJoCo planar mobile base and trajectory overlay."
units: "Wheel travel and track width meters; heading radians."
frames: [world, robot_base, left_wheel, right_wheel]
fixture_license: CC0-1.0
---

# Planning metadata

Planned, not runnable. This component integrates ideal wheel travel; visual SLAM and sensor fusion may later compare or constrain that estimate. It is not a claimed wheel-odometry component from a specific paper.

Read the [ORB-SLAM2 context](../../../../research/papers/geometry-calibration-slam/2016-orb-slam-2.md) and the robot geometry conventions before creating sensor-fusion extensions.

Assessment checks equal wheel travel, reverse motion, curved arcs, pure rotation, starting heading, and the near-zero-turn limit. Synthetic fixtures assume no slip and one constant-twist interval.
