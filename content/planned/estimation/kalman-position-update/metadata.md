---
schema_version: 1
slug: kalman-position-update
title: "Fuse a Position Measurement with a Kalman Update"
status: planned
difficulty: Medium
domain: estimation
prerequisites: ["differential-drive-odometry"]
paper_applications: ["2017-vins-mono"]
assessment: "Posterior mean, nonnegative posterior variance, innovation, and gain; measurement-noise limits"
simulator: none
units: "position: meters; variance: square meters"
frames: ["world"]
fixture_license: CC0-1.0
---

# Authoring status

This is a planned robotics-concept lesson. It is not runnable and is not counted among the first ten implemented problems. Examples are hand-verifiable teaching cases; reference code, hidden tests, runtime limits, and an immutable evaluator version are required before publication.

## Paper connection

Paper IDs above identify applications to study after the foundation. They do not claim these papers use the exact reduced teaching contract. Resolve their paired cards under `research/papers/` before implementation.

Primary application context: [VINS-Mono](https://arxiv.org/abs/1708.03852). This scalar identity-observation update is a foundation for interpreting sensor uncertainty, not a reproduction of VINS-Mono's estimator.

