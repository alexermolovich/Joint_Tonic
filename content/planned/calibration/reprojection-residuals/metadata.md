---
schema_version: 1
slug: reprojection-residuals
title: Measure Camera Reprojection Residuals
status: planned
difficulty: Easy
domain: Camera calibration
prerequisites: [project-camera-points, compose-frame-transforms]
paper_applications: [2016-orb-slam-2, 2017-vins-mono, 2022-bevformer]
assessment: "Observed-minus-predicted residuals, valid-depth mask, per-point pixel RMSE."
simulator: "2D observed/predicted pixel overlay; no simulator required."
units: "3D points meters; residuals and RMSE pixels."
frames: [camera_optical, image]
fixture_license: CC0-1.0
---

# Planning metadata

Planned, not runnable. Build a diagnostic component rather than a full camera-calibration optimizer.

Primary model reference: [OpenCV calibration](https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html). Paper applications: [ORB-SLAM2](../../../../research/papers/geometry-calibration-slam/2016-orb-slam-2.md), [VINS-Mono](../../../../research/papers/geometry-calibration-slam/2017-vins-mono.md), and [BEVFormer](../../../../research/papers/vision-vlm-3d/2022-bevformer.md).

Assess residual sign, correct focal/principal-point use, invalid-depth exclusion, an empty-valid-set result, and the distinction between per-coordinate and per-point error. All fixtures are synthetic.
