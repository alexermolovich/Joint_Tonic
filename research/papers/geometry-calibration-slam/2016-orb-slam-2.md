---
schema_version: 1
paper_id: 2016-orb-slam-2
title: 'ORB-SLAM2: an Open-Source SLAM System for Monocular, Stereo and RGB-D Cameras'
authors:
  - 'Mur-Artal, Raul'
  - 'Tardos, Juan D.'
year: 2016
venue_or_status: >-
  Author-deposited arXiv manuscript; final venue not asserted by this
  acquisition card.
primary_url: 'https://arxiv.org/abs/1610.06475'
pdf_url: 'https://arxiv.org/pdf/1610.06475'
local_pdf: ./2016-orb-slam-2.pdf
sha256: 2b94552a20378d6dfbe863ba7317d4a86874fe54e43ca8b918abefcbdc64ce24
bytes: 4187799
pages: 9
topics:
  - geometry-calibration-slam
  - orb-slam-2
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
      title: Track visual landmarks
      detail: Associate image keypoints with map points.
      column: 0
      row: 0
      section: Track visual landmarks
      problem_slugs:
        - pose-guided-binary-feature-association
      planned_problems: []
    - id: stage-2
      title: Optimize local geometry
      detail: Refine keyframe poses and landmark positions.
      column: 1
      row: 0
      section: Optimize local geometry
      problem_slugs:
        - reprojection-pose-hypothesis-inliers
      planned_problems: []
    - id: stage-3
      title: Close loops and relocalize
      detail: Recognize previously mapped places and correct drift.
      column: 2
      row: 0
      section: Close loops and relocalize
      problem_slugs:
        - relocalization-landmark-coverage
      planned_problems: []
  edges:
    - from: stage-1
      to: stage-2
      label: feature correspondences
    - from: stage-2
      to: stage-3
      label: keyframe map
---

## Core paper explanation

ORB-SLAM2 combines ORB feature tracking, local mapping, relocalization, and loop closure for monocular, stereo, and RGB-D cameras. Its map consists of keyframes and 3D landmarks refined through bundle adjustment.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Track visual landmarks

For world landmark $P_j$ and world-to-camera pose $T_{CW,i}$, the reprojection residual is
$$r_{ij}=u_{ij}-\pi(T_{CW,i}P_j).$$
$u_{ij}$ is a measured pixel. Reject points behind the camera and use the calibrated camera model. ORB descriptor matches supply candidate associations, not guaranteed correspondences. The linked matcher uses packed 256-bit descriptors and an explicitly original no-retry collision policy. The inlier exercise scores supplied pose hypotheses; the relocalization exercise gates supplied inliers by unique landmark identities and representative image coverage. These are separate inspectable components, not the complete ORB-SLAM2 matching or relocalization implementation.


**Prerequisite practice:** [Project Camera Points into Pixels](/problems/project-camera-points). These supporting skills do not complete this model stage.

**Implement these components:** [Associate Map Points with Image Features](/problems/pose-guided-binary-feature-association). The exercises state their bounded frame, numerical and diagnostic conventions; they do not reproduce the complete estimator.

### Optimize local geometry

Bundle adjustment minimizes
$$\min_{T,P}\sum_{(i,j)}\rho(r_{ij}^\top\Omega_{ij}r_{ij}),$$
where $\Omega_{ij}$ weights measurement uncertainty. Fix the appropriate gauge. Stereo/RGB-D provides metric scale; monocular geometry alone has an unobservable global scale.


**Implement these components:** [Select Geometric Pose Inliers](/problems/reprojection-pose-hypothesis-inliers). The exercises state their bounded frame, numerical and diagnostic conventions; they do not reproduce the complete estimator.

### Close loops and relocalize

Place recognition proposes loop/relocalization candidates; geometric verification rejects inconsistent matches. Loop correction and subsequent map optimization restore consistency. Similar-looking corridors can generate false candidates, so descriptor similarity alone must not authorize a map merge.


**Implement these components:** [Evaluate a Relocalization Candidate](/problems/relocalization-landmark-coverage). The exercises state their bounded frame, numerical and diagnostic conventions; they do not reproduce the complete estimator.

## Implement the components

- **Related implementation skill:** [Project Camera Points into Pixels](/problems/project-camera-points). This isolates a supporting mechanism, not this paper's complete method.
- **Related implementation skill:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). This isolates a supporting mechanism, not this paper's complete method.

**Runnable components and remaining ideas:**

- [Associate Map Points with Image Features](/problems/pose-guided-binary-feature-association) — runnable bounded component.
- [Select Geometric Pose Inliers](/problems/reprojection-pose-hypothesis-inliers) — runnable bounded component.
- [Evaluate a Relocalization Candidate](/problems/relocalization-landmark-coverage) — runnable bounded component.

[Browse the planned curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md). Planned titles require a reviewed contract and evaluator before becoming runnable.

## Why this matters on a robot

A reusable map supports repeated robot operation and recovery after temporary tracking loss. Dynamic scenes, weak texture, and false loop closures are separate failure mechanisms that require distinct diagnostics.

## Sources and scope

[Primary paper](https://arxiv.org/abs/1610.06475) · [Open-access manuscript](https://arxiv.org/pdf/1610.06475)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
