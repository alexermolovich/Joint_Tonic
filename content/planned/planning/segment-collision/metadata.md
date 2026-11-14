---
schema_version: 1
slug: segment-collision
title: "Check a Motion Segment Against Inflated Obstacles"
status: planned
difficulty: Medium
domain: planning
prerequisites: ["grid-shortest-path"]
paper_applications: ["2018-motion-planning-networks"]
assessment: "Closed-box segment intersection, conservative clearance, first hit and zero-length motion"
simulator: none
units: "positions, obstacle extents, clearance: meters; segment parameter: dimensionless"
frames: ["world-2d"]
fixture_license: CC0-1.0
---

# Authoring status

This is a planned robotics-concept lesson. It is not runnable and is not counted among the first ten implemented problems. Examples are hand-verifiable teaching cases; reference code, hidden tests, runtime limits, and an immutable evaluator version are required before publication.

## Paper connection

Paper IDs above identify applications to study after the foundation. They do not claim these papers use the exact reduced teaching contract. Resolve their paired cards under `research/papers/` before implementation.

Primary application context: [Motion Planning Networks](https://arxiv.org/abs/1806.05767). This geometry checker is a reusable planning foundation; it is not a claim about the paper's exact collision implementation.

