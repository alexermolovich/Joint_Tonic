---
schema_version: 1
slug: grasp-approach-frame
title: "Build a Pre-Grasp Pose Along the Tool Axis"
status: planned
difficulty: Easy
domain: manipulation
prerequisites: ["compose-frame-transforms","serial-chain-forward-kinematics"]
paper_applications: ["2017-dex-net-2"]
assessment: "Tool-axis direction, unchanged rotation, positive approach distance and proper SE3 validation"
simulator: mujoco-optional
units: "translation and approach distance: meters; rotation entries: dimensionless"
frames: ["world","grasp"]
fixture_license: CC0-1.0
---

# Authoring status

This is a planned robotics-concept lesson. It is not runnable and is not counted among the first ten implemented problems. Examples are hand-verifiable teaching cases; reference code, hidden tests, runtime limits, and an immutable evaluator version are required before publication.

## Paper connection

Paper IDs above identify applications to study after the foundation. They do not claim these papers use the exact reduced teaching contract. Resolve their paired cards under `research/papers/` before implementation.

Primary application context: [Dex-Net 2.0](https://arxiv.org/abs/1703.09312). The pose construction prepares a grasp execution interface. It does not estimate the paper's analytic grasp quality or reproduce its network.

