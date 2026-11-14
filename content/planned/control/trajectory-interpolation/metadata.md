---
schema_version: 1
slug: trajectory-interpolation
title: "Interpolate a Time-Parameterized Joint Trajectory"
status: planned
difficulty: Easy
domain: control
prerequisites: ["interpolate-joint-state"]
paper_applications: ["2023-aloha-act","2023-diffusion-policy"]
assessment: "Knot selection, linear interpolation, interval velocity and endpoint hold policy"
simulator: mujoco-optional
units: "time: seconds; joints: radians; velocity: radians per second"
frames: ["joint"]
fixture_license: CC0-1.0
---

# Authoring status

This is a planned robotics-concept lesson. It is not runnable and is not counted among the first ten implemented problems. Examples are hand-verifiable teaching cases; reference code, hidden tests, runtime limits, and an immutable evaluator version are required before publication.

## Paper connection

Paper IDs above identify applications to study after the foundation. They do not claim these papers use the exact reduced teaching contract. Resolve their paired cards under `research/papers/` before implementation.

Primary application context: [ACT / ALOHA](https://arxiv.org/abs/2304.13705). Trajectory timing is a prerequisite for interpreting action chunks; this linear sampler is not an ACT reproduction.

