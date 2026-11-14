---
schema_version: 1
slug: serial-chain-forward-kinematics
title: Compute Forward Kinematics for a Serial Chain
status: planned
difficulty: Medium
domain: Kinematics
prerequisites: [compose-frame-transforms]
paper_applications: [2023-curobo, 2022-ik-geo]
assessment: "Joint/link pose chain, end-effector pose, configuration consistency."
simulator: "MuJoCo planar chain; optional Isaac Sim adapter later."
units: "Link lengths meters; joint angles radians."
frames: [base, link_1, link_n, tool]
fixture_license: CC0-1.0
---

# Planning metadata

Planned, not runnable. Begin with a planar revolute chain whose link convention is explicit; arbitrary 3D robot descriptions are a later extension.

Applications: [cuRobo](../../../../research/papers/planning-control-ik/2023-curobo.md) and [IK-Geo](../../../../research/papers/planning-control-ik/2022-ik-geo.md) need consistent forward-kinematics queries. These references motivate prerequisites only.

Assessment will compare all link endpoints and final orientation, verify lengths, test zero/negative joint angles and a single link, and preserve input arrays. Use deterministic synthetic robot assets and numerical tolerance `1e-7`.
