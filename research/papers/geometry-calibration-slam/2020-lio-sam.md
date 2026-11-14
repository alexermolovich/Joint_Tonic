---
schema_version: 1
paper_id: 2020-lio-sam
title: 'LIO-SAM: Tightly-coupled Lidar Inertial Odometry via Smoothing and Mapping'
authors:
  - 'Shan, Tixiao'
  - 'Englot, Brendan'
  - 'Meyers, Drew'
  - 'Wang, Wei'
  - 'Ratti, Carlo'
  - 'Rus, Daniela'
year: 2020
venue_or_status: >-
  Author-deposited arXiv manuscript; final venue not asserted by this
  acquisition card.
primary_url: 'https://arxiv.org/abs/2007.00258'
pdf_url: 'https://arxiv.org/pdf/2007.00258'
local_pdf: ./2020-lio-sam.pdf
sha256: 8ad11438fc0849de88b1604932f8bfd2732aee640aaf5fb41974b34f555c86f6
bytes: 4368703
pages: 8
topics:
  - geometry-calibration-slam
  - lio-sam
modalities:
  - camera
  - imu
  - lidar
  - poses
track_role: supporting
open_access_status: open-access-preprint
redistribution_note: Research copy only; verify the source license before redistribution.
execution_flow:
  title: Core execution flow
  description: >-
    Follow the data through the mechanism. Training objectives and inference
    behavior are distinguished in the linked explanations.
  nodes:
    - id: stage-1
      title: Deskew lidar measurements
      detail: Move points captured at different times into one scan frame.
      column: 0
      row: 0
      section: Deskew lidar measurements
      problem_slugs:
        - interpolate-pose-slerp
        - trace-perception-frame-graph
        - deskew-lidar-points
      planned_problems: []
    - id: stage-2
      title: Align local scan features
      detail: Match edge and surface features against a local map.
      column: 1
      row: 0
      section: Align local scan features
      problem_slugs:
        - lidar-feature-residuals
      planned_problems: []
    - id: stage-3
      title: Smooth sensor factors
      detail: 'Combine inertial, lidar, GPS, and loop constraints when available.'
      column: 2
      row: 0
      section: Smooth sensor factors
      problem_slugs: []
      planned_problems:
        - Assemble an IMU-Lidar Pose Constraint
        - Reject Inconsistent Loop Closures
  edges:
    - from: stage-1
      to: stage-2
      label: deskewed scan
    - from: stage-2
      to: stage-3
      label: relative pose factors
---

## Core paper explanation

LIO-SAM couples lidar and IMU through factor-graph smoothing. IMU preintegration supplies motion estimates for scan deskewing and initialization, while lidar alignment constrains drift and helps estimate inertial biases.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Deskew lidar measurements

For point $p^{L_t}$ captured at time $t$, its reference-scan coordinates are
$$p^{L_0}=T_{WL_0}^{-1}T_{WL_t}p^{L_t}.$$
Transforms include lidar–IMU extrinsics. A scan is not instantaneous; per-point timestamps and motion interpolation determine whether deskewing is meaningful.


**Prerequisite practice:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). These supporting skills do not complete this model stage.

**Implement these components:** [Deskew a Lidar Scan with Motion Estimates](/problems/deskew-lidar-points). Each exercise states its bounded numerical and frame conventions; it does not reproduce the complete estimator.

Use homogeneous points $p^{L_t}\in\mathbb R^4$ with final coordinate one. Each $T_{WL_t}\in\mathbb R^{4\times4}$ maps the lidar frame at capture time $t$ into the common world frame; translations and the first three point entries are in meters. If the lidar moves one meter along world x between the reference time and capture, with identity rotations, a captured point $(2,0,0,1)$ becomes $(3,0,0,1)$ in the reference lidar frame. Reversing the relative transform would incorrectly return x equal to one.

[Interpolate a Pose with SLERP](/problems/interpolate-pose-slerp) and [Trace Frames Through a Robot Perception Graph](/problems/trace-perception-frame-graph) expose interpolation and transform-direction prerequisites. The interpolation exercise is a bounded geometric model, not a substitute for LIO-SAM's inertial motion estimation, bias handling, or scan registration.


### Align local scan features

A surface residual is $r=n^\top(Rp+t-q)$, with $n$ a unit normal and distances in meters. Edge features use distance-to-line geometry. Local keyframe maps bound registration work and reduce dependence on a monolithic global point cloud.




**Implement these components:** [Compute Point-to-Line and Point-to-Plane Scan Residuals](/problems/lidar-feature-residuals). Each exercise states its bounded numerical and frame conventions; it does not reproduce the complete estimator.

### Smooth sensor factors

The graph solves $\min_X\sum_k\|r_k(X)\|_{\Sigma_k^{-1}}^2$ with appropriate robust treatment. $X$ includes pose, velocity, and biases for inertial estimation. Lidar correction improves motion and bias estimates, which then improve later scan deskewing.


**Planned component problems:** Assemble an IMU-Lidar Pose Constraint; Reject Inconsistent Loop Closures. These remain unreviewed implementation ideas without runnable exercises.

## Implement the components

- **Related implementation skill:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). This isolates a supporting mechanism, not this paper's complete method.

**Runnable components and remaining ideas:**

- [Deskew a Lidar Scan with Motion Estimates](/problems/deskew-lidar-points) — runnable bounded component.
- [Compute Point-to-Line and Point-to-Plane Scan Residuals](/problems/lidar-feature-residuals) — runnable bounded component.
- Assemble an IMU-Lidar Pose Constraint.
- Reject Inconsistent Loop Closures.

[Browse the planned curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md). Planned titles require a reviewed contract and evaluator before becoming runnable.

## Why this matters on a robot

Coupling is valuable during rapid motion or short visual outages. Feature-poor geometry, timing errors, and a wrong lidar–IMU transform can make the estimator confidently wrong.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2007.00258) · [Open-access manuscript](https://arxiv.org/pdf/2007.00258)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
