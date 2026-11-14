---
schema_version: 1
slug: compose-frame-transforms
title: Compose and Invert Coordinate Transforms
status: planned
difficulty: Medium
domain: Frames and units
prerequisites: [se3-transform-points]
paper_applications: [2022-bevformer, 2016-orb-slam-2]
assessment: "Frame-compatible composition, inverse round trips, rigid-transform validation."
simulator: "Optional MuJoCo frame overlay; numerical grading is authoritative."
units: "Translations meters; rotations dimensionless."
frames: [world, base, camera]
fixture_license: CC0-1.0
---

# Planning metadata

This is a planned robotics concept exercise, not a runnable problem. It teaches how multiple rigid calibrations compose before paper-specific perception or mapping.

Primary context: [Modern Robotics frame transforms](https://modernrobotics.northwestern.edu/nu-gm-book-resource/3-3-1-homogeneous-transformation-matrices/). Paper applications: [BEVFormer](../../../../research/papers/vision-vlm-3d/2022-bevformer.md) and [ORB-SLAM2](../../../../research/papers/geometry-calibration-slam/2016-orb-slam-2.md). These are prerequisite connections, not reproductions.

Planned assessment uses synthetic right-handed transforms, composition order, inverse translation, mismatched frame labels, and round trips with numerical tolerance `1e-7`. Runtime and evaluator versions must be pinned before implementation.
