---
schema_version: 1
slug: geometric-jacobian
title: Build a Geometric Jacobian from Joint Axes
status: planned
difficulty: Medium
domain: Kinematics
prerequisites: [compose-frame-transforms, serial-chain-forward-kinematics]
paper_applications: [2023-curobo, 2018-rmpflow]
assessment: "Frame-consistent revolute/prismatic columns and small-velocity motion."
simulator: "MuJoCo axis and end-effector velocity overlay."
units: "Origins meters; angular rates rad/s; linear rates m/s."
frames: [base, joint_axes, tool]
fixture_license: CC0-1.0
---

# Planning metadata

Planned, not runnable. The task constructs a geometric Jacobian from already known joint origins and unit axes; it does not differentiate an opaque robot model.

Applications include [cuRobo](../../../../research/papers/planning-control-ik/2023-curobo.md) and control methods using task-space motion. Verify each paper's actual convention before creating a paper-specific extension.

The output stacks linear velocity before angular velocity. Assess mixed joints, off-origin axes, unit-axis validation, zero lever arms, and agreement with a small finite forward-kinematics displacement. Numerical tolerance: `1e-7`.
