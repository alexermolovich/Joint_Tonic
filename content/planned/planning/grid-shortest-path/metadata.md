---
schema_version: 1
slug: grid-shortest-path
title: "Plan a Shortest Route on an Occupancy Grid"
status: planned
difficulty: Medium
domain: planning
prerequisites: ["occupancy-log-odds"]
paper_applications: ["2018-motion-planning-networks"]
assessment: "Collision-free four-neighbor path, optimal cost, deterministic tie policy, and unreachable status"
simulator: none
units: "cell size: meters; path cost: meters"
frames: ["map-grid"]
fixture_license: CC0-1.0
---

# Authoring status

This is a planned robotics-concept lesson. It is not runnable and is not counted among the first ten implemented problems. Examples are hand-verifiable teaching cases; reference code, hidden tests, runtime limits, and an immutable evaluator version are required before publication.

## Paper connection

Paper IDs above identify applications to study after the foundation. They do not claim these papers use the exact reduced teaching contract. Resolve their paired cards under `research/papers/` before implementation.

Primary application context: [Motion Planning Networks](https://arxiv.org/abs/1806.05767). The grid planner is a transparent search baseline. A later paper component must preserve explicit feasibility and evaluation contracts.

