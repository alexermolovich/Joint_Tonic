---
schema_version: 1
slug: planar-two-link-ik
title: Solve Closed-Form IK for a Planar Two-Link Arm
status: planned
difficulty: Medium
domain: Kinematics
prerequisites: [serial-chain-forward-kinematics]
paper_applications: [2022-ik-geo, 2023-curobo]
assessment: "Reachability, declared elbow branch, FK residual and singular boundaries."
simulator: "MuJoCo target and two-link arm sidecar."
units: "Lengths and targets meters; returned angles radians."
frames: [base, shoulder, elbow, tool]
fixture_license: CC0-1.0
---

# Planning metadata

Planned, not runnable. Return one explicitly chosen geometric branch rather than implying a unique solution for every robot.

Paper applications: [IK-Geo](../../../../research/papers/planning-control-ik/2022-ik-geo.md) and [cuRobo](../../../../research/papers/planning-control-ik/2023-curobo.md). This basic planar geometry does not reproduce either method.

Assess forward-kinematics consistency, workspace annulus, positive-elbow branch, zero/full extension, roundoff clipping only within `1e-9`, and the equal-length origin convention.
