---
schema_version: 1
paper_id: 2020-orb-slam-3
title: >-
  ORB-SLAM3: An Accurate Open-Source Library for Visual, Visual-Inertial and
  Multi-Map SLAM
authors:
  - 'Campos, Carlos'
  - 'Elvira, Richard'
  - 'Rodríguez, Juan J. Gómez'
  - 'Montiel, José M. M.'
  - 'Tardós, Juan D.'
year: 2020
venue_or_status: >-
  Author-deposited arXiv manuscript; final venue not asserted by this
  acquisition card.
primary_url: 'https://arxiv.org/abs/2007.11898'
pdf_url: 'https://arxiv.org/pdf/2007.11898'
local_pdf: ./2020-orb-slam-3.pdf
sha256: 4d119517be7565c9651fbf1e36a330d605b7a534d738558858c96feca7b99156
bytes: 5049669
pages: 18
topics:
  - geometry-calibration-slam
  - orb-slam-3
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
      title: Initialize inertial estimation
      detail: 'Estimate scale, gravity, velocity, and bias with probabilistic priors.'
      column: 0
      row: 0
      section: Initialize inertial estimation
      problem_slugs:
        - visual-inertial-initialization-gate
      planned_problems: []
    - id: stage-2
      title: Track and refine a map
      detail: Optimize feature reprojection and inertial constraints together.
      column: 1
      row: 0
      section: Track and refine a map
      problem_slugs:
        - visual-inertial-keyframe-residual
      planned_problems: []
    - id: stage-3
      title: Reuse and merge maps
      detail: Geometrically verify common places across atlas maps.
      column: 2
      row: 0
      section: Reuse and merge maps
      problem_slugs:
        - aligned-trajectory-position-error
      planned_problems:
        - Merge Consistent Map Transforms
  edges:
    - from: stage-1
      to: stage-2
      label: initialized state
    - from: stage-2
      to: stage-3
      label: keyframe atlas
---

## Core paper explanation

ORB-SLAM3 extends feature-based SLAM with tightly integrated visual-inertial estimation and an atlas of multiple maps. It can start a new map after tracking loss and later merge maps when a verified shared place is found.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Initialize inertial estimation

Maximum-a-posteriori estimation combines likelihood and prior:
$$X^*=\arg\min_X[-\log p(z\mid X)-\log p(X)].$$
Here $z$ includes visual and IMU observations. Metric scale and gravity require sufficiently informative inertial motion; monocular images alone do not identify scale. The linked initializer validates a supplied candidate with a gauge-fixed, whitened/scaled Jacobian rank check, metric scale interval, gravity magnitude and bias norms, and whitened residual RMS. These transparent operational gates are not ORB-SLAM3’s complete MAP initialization procedure or a proof of nonlinear observability.


**Implement these components:** [Validate a Visual-Inertial Initialization](/problems/visual-inertial-initialization-gate). Each linked exercise declares its bounded numerical and physical contract; these are not full estimator reproductions.

### Track and refine a map

Visual residuals are $r_{ij}=u_{ij}-\pi(T_{CW,i}P_j)$, combined with preintegrated IMU residuals in local bundle adjustment. $T_{CW}$ maps world points into the camera frame. Pinhole and fisheye cameras require their corresponding projection functions. The reused visual-inertial exercise is strictly a two-keyframe window: it combines supplied visual pixel residuals with gravity-corrected rotation, velocity and position residuals under diagonal standard deviations. It does not generate reprojections, construct a larger graph, include bias-state residuals, or optimize bundle adjustment.


**Prerequisite practice:** [Project Camera Points into Pixels](/problems/project-camera-points). These supporting skills do not complete this model stage.


**Implement these components:** [Build a Visual-Inertial Residual](/problems/visual-inertial-keyframe-residual). Each linked exercise declares its bounded numerical and physical contract; these are not full estimator reproductions.

### Reuse and merge maps

An atlas stores separate maps until a consistent cross-map alignment is found. A similarity transform $p'=sRp+t$ can express unknown relative scale for monocular maps; established inertial/metric constraints restrict allowable alignment. A recognized image is only a candidate, not sufficient evidence for merging. The linked trajectory exercise fits a proper global rigid or similarity alignment to time-matched position samples and reports Euclidean position RMSE. It does not merge maps, measure orientation error, remove outliers or show that local drift is absent.


**Implement these components:** [Evaluate Trajectory Error After Alignment](/problems/aligned-trajectory-position-error). The exercises state their bounded frame, numerical and diagnostic conventions; they do not reproduce the complete estimator.

**Planned component problems:** Merge Consistent Map Transforms. These remain unreviewed implementation ideas without runnable exercises.

## Implement the components

- **Related implementation skill:** [Project Camera Points into Pixels](/problems/project-camera-points). This isolates a supporting mechanism, not this paper's complete method.
- **Related implementation skill:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). This isolates a supporting mechanism, not this paper's complete method.

**Runnable components and remaining ideas:**

- [Validate a Visual-Inertial Initialization](/problems/visual-inertial-initialization-gate) — runnable bounded component.
- [Build a Visual-Inertial Residual](/problems/visual-inertial-keyframe-residual) — runnable bounded component.
- Merge Consistent Map Transforms.
- [Evaluate Trajectory Error After Alignment](/problems/aligned-trajectory-position-error) — runnable bounded component.

[Browse the planned curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md). Planned titles require a reviewed contract and evaluator before becoming runnable.

## Why this matters on a robot

An atlas supports recovery across repeated visits and temporary tracking failures. False place recognition or inconsistent metric initialization can corrupt multiple sessions, so merge evidence must be inspectable.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2007.11898) · [Open-access manuscript](https://arxiv.org/pdf/2007.11898)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
