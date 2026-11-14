---
schema_version: 1
paper_id: 2021-fast-lio-2
title: 'FAST-LIO2: Fast Direct LiDAR-inertial Odometry'
authors:
  - 'Xu, Wei'
  - 'Cai, Yixi'
  - 'He, Dongjiao'
  - 'Lin, Jiarong'
  - 'Zhang, Fu'
year: 2021
venue_or_status: >-
  Author-deposited arXiv manuscript; final venue not asserted by this
  acquisition card.
primary_url: 'https://arxiv.org/abs/2107.06829'
pdf_url: 'https://arxiv.org/pdf/2107.06829'
local_pdf: ./2021-fast-lio-2.pdf
sha256: ba5072e06e75dec5222bcb528143f3aa3238d6f6692bac1e22a9fe1bc55a15dd
bytes: 13481318
pages: 19
topics:
  - geometry-calibration-slam
  - fast-lio-2
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
      title: Propagate the inertial state
      detail: 'Predict pose, velocity, biases, and covariance.'
      column: 0
      row: 0
      section: Propagate the inertial state
      problem_slugs: []
      planned_problems:
        - Propagate an Error-State IMU Mean and Covariance
    - id: stage-2
      title: Iterate point-to-map updates
      detail: Use raw-point geometric residuals without a feature-extraction stage.
      column: 1
      row: 0
      section: Iterate point-to-map updates
      problem_slugs:
        - associate-local-map-planes
        - lidar-feature-residuals
      planned_problems: []
    - id: stage-3
      title: Maintain the local map
      detail: Update an incremental spatial index.
      column: 2
      row: 0
      section: Maintain the local map
      problem_slugs:
        - incremental-voxel-local-map
      planned_problems: []
  edges:
    - from: stage-1
      to: stage-2
      label: predicted state
    - from: stage-2
      to: stage-3
      label: corrected scan pose
---

## Core paper explanation

FAST-LIO2 registers raw lidar points directly to a map using a tightly coupled iterated Kalman filter. An incremental k-d tree supports fast nearest-neighbor lookup, map insertion, deletion, and local-map maintenance.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Propagate the inertial state

For state estimate $x$ and IMU input $u$, propagation is $x^-_{k+1}=f(x_k,u_k,\Delta t)$. The error covariance follows
$$P^-=FPF^\top+GQG^\top,$$
where $F,G$ are linearized transition/noise Jacobians and $Q$ the discretized process-noise covariance. Rotation updates use manifold operations.




**Planned component problems:** Propagate an Error-State IMU Mean and Covariance. These remain unreviewed implementation ideas without runnable exercises.

### Iterate point-to-map updates

For local map plane $(n,q)$ and lidar point $p$, $r=n^\top(Rp+t-q)$. A local linear update uses
$$K=PH^\top(HPH^\top+R_z)^{-1}.$$
$H$ is the residual Jacobian and $R_z$ measurement covariance. The actual iterated manifold filter relinearizes and uses an efficient state-dimension formulation; this equation is the Kalman measurement-update core.


**Implement these components:** [Associate Scan Points with Local Map Planes](/problems/associate-local-map-planes) · [Compute Point-to-Line and Point-to-Plane Scan Residuals](/problems/lidar-feature-residuals). Each exercise states its bounded numerical and frame conventions; it does not reproduce the complete estimator.

### Maintain the local map

The ikd-Tree supports adding transformed points, deleting points outside the local region, and downsampling. Map resolution trades geometric detail against computation. Timestamped deskewing and lidar–IMU extrinsics remain necessary even though handcrafted feature extraction is removed. The linked local-map exercise makes the update decisions deterministic: transform the scan, prune an inclusive world-aligned box, and retain the center-nearest point per world-origin voxel with stable identity ties. It is a bounded batch teaching model, not an ikd-Tree implementation or its performance claim.


**Implement these components:** [Update an Incremental Local Map](/problems/incremental-voxel-local-map). Each linked exercise declares its bounded numerical and physical contract; these are not full estimator reproductions.

## Implement the components

- **Related implementation skill:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). This isolates a supporting mechanism, not this paper's complete method.

**Runnable components and remaining ideas:**

- Propagate an Error-State IMU Mean and Covariance.
- [Associate Scan Points with Local Map Planes](/problems/associate-local-map-planes) — runnable bounded component.
- [Compute Point-to-Line and Point-to-Plane Scan Residuals](/problems/lidar-feature-residuals) — runnable bounded component.
- [Update an Incremental Local Map](/problems/incremental-voxel-local-map) — runnable bounded component.

[Browse the planned curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md). Planned titles require a reviewed contract and evaluator before becoming runnable.

## Why this matters on a robot

Direct registration accommodates varied lidar scan patterns. Large planar or sparse scenes can leave some motion directions weakly observable; fast computation does not eliminate geometric degeneracy.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2107.06829) · [Open-access manuscript](https://arxiv.org/pdf/2107.06829)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
