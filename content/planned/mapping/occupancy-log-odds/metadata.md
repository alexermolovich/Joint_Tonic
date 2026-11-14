---
schema_version: 1
slug: occupancy-log-odds
title: "Update Occupancy Belief from Range Evidence"
status: planned
difficulty: Medium
domain: mapping
prerequisites: ["compose-frame-transforms"]
paper_applications: ["2022-bevformer"]
assessment: "Additive evidence, explicit prior correction, probability conversion, and saturation bounds"
simulator: none
units: "dimensionless probability and log odds; map cell size: meters"
frames: ["map"]
fixture_license: CC0-1.0
---

# Authoring status

This is a planned robotics-concept lesson. It is not runnable and is not counted among the first ten implemented problems. Examples are hand-verifiable teaching cases; reference code, hidden tests, runtime limits, and an immutable evaluator version are required before publication.

## Paper connection

Paper IDs above identify applications to study after the foundation. They do not claim these papers use the exact reduced teaching contract. Resolve their paired cards under `research/papers/` before implementation.

Primary application context: [BEVFormer](https://arxiv.org/abs/2203.17270). This is a classical occupancy-belief foundation. BEVFormer is a later comparison in spatial representations and is not asserted to use this log-odds rule.

