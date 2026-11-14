---
schema_version: 1
slug: pid-anti-windup
title: "Take a PID Step with Conditional Anti-Windup"
status: planned
difficulty: Medium
domain: control
prerequisites: ["interpolate-joint-state"]
paper_applications: ["2023-diffusion-policy"]
assessment: "Discrete-time derivative, candidate integral, actuator clamp and directional anti-windup rule"
simulator: mujoco-optional
units: "error: joint radians; time: seconds; output: declared actuator command units"
frames: ["joint"]
fixture_license: CC0-1.0
---

# Authoring status

This is a planned robotics-concept lesson. It is not runnable and is not counted among the first ten implemented problems. Examples are hand-verifiable teaching cases; reference code, hidden tests, runtime limits, and an immutable evaluator version are required before publication.

## Paper connection

Paper IDs above identify applications to study after the foundation. They do not claim these papers use the exact reduced teaching contract. Resolve their paired cards under `research/papers/` before implementation.

Primary application context: [Diffusion Policy](https://arxiv.org/abs/2303.04137). A low-level controller can execute a learned target, but this PID contract is an independent foundation and not the paper's control specification.

