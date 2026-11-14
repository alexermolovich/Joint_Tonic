---
schema_version: 1
paper_id: 2016-direct-sparse-odometry
title: Direct Sparse Odometry
authors:
  - 'Engel, Jakob'
  - 'Koltun, Vladlen'
  - 'Cremers, Daniel'
year: 2016
venue_or_status: >-
  Author-deposited arXiv manuscript; final venue not asserted by this
  acquisition card.
primary_url: 'https://arxiv.org/abs/1607.02565'
pdf_url: 'https://arxiv.org/pdf/1607.02565'
local_pdf: ./2016-direct-sparse-odometry.pdf
sha256: cd85260a38b0b5d0e82c85c37c3540c498a953e39a501d9af5192a35b8284223
bytes: 7990289
pages: 17
topics:
  - geometry-calibration-slam
  - direct-sparse-odometry
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
      title: Warp a depth hypothesis
      detail: Project a reference pixel into another camera.
      column: 0
      row: 0
      section: Warp a depth hypothesis
      problem_slugs:
        - warp-calibrated-pixels
      planned_problems: []
    - id: stage-2
      title: Measure photometric error
      detail: Account for exposure and affine brightness changes.
      column: 1
      row: 0
      section: Measure photometric error
      problem_slugs:
        - exposure-photometric-residual
      planned_problems: []
    - id: stage-3
      title: Optimize a sparse window
      detail: 'Jointly update poses, depths, and brightness parameters.'
      column: 2
      row: 0
      section: Optimize a sparse window
      problem_slugs:
        - select-gradient-image-points
      planned_problems: []
  edges:
    - from: stage-1
      to: stage-2
      label: warped pixels
    - from: stage-2
      to: stage-3
      label: weighted residuals
---

## Core paper explanation

Direct Sparse Odometry estimates camera motion and sparse inverse depths directly from image intensities. It optimizes photometric consistency with exposure and brightness modeling, instead of relying on descriptor matching for every observation.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Warp a depth hypothesis

For reference pixel $u$, inverse depth $\rho>0$, and source-to-target transform $T_{ji}$,
$$u'=\pi\!\left(T_{ji}\,\pi^{-1}(u,\rho)\right).$$
$\pi^{-1}$ returns a 3D point in meters when $\rho$ is inverse meters. Visibility, positive target depth, and valid sampling bounds are required.


**Prerequisite practice:** [Project Camera Points into Pixels](/problems/project-camera-points). These supporting skills do not complete this model stage.

**Implement these components:** [Warp a Point Between Calibrated Frames](/problems/warp-calibrated-pixels). Each exercise states its bounded numerical and frame conventions; it does not reproduce the complete estimator.

### Measure photometric error

A DSO brightness residual has the form
$$r=I_j(u')-b_j-\frac{t_j e^{a_j}}{t_i e^{a_i}}(I_i(u)-b_i).$$
$t_i,t_j$ are exposure times, $a$ log-gain parameters, and $b$ brightness offsets. Calibrated image response and vignetting are part of the direct-method assumptions.


**Implement these components:** [Compute an Exposure-Corrected Photometric Residual](/problems/exposure-photometric-residual). Each exercise states its bounded numerical and frame conventions; it does not reproduce the complete estimator.

### Optimize a sparse window

The objective sums robust weighted residuals, $E=\sum_p w_p\rho_H(r_p)$, over selected high-gradient pixel neighborhoods. $\rho_H$ denotes the Huber penalty, not inverse depth. Marginalization retains prior information as old states leave the active window.


**Implement these components:** [Select High-Gradient Image Points](/problems/select-gradient-image-points). Each exercise states its bounded numerical and frame conventions; it does not reproduce the complete estimator.

## Implement the components

- **Related implementation skill:** [Project Camera Points into Pixels](/problems/project-camera-points). This isolates a supporting mechanism, not this paper's complete method.
- **Related implementation skill:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). This isolates a supporting mechanism, not this paper's complete method.

**Runnable components and remaining ideas:**

- [Warp a Point Between Calibrated Frames](/problems/warp-calibrated-pixels) — runnable bounded component.
- [Compute an Exposure-Corrected Photometric Residual](/problems/exposure-photometric-residual) — runnable bounded component.
- [Select High-Gradient Image Points](/problems/select-gradient-image-points) — runnable bounded component.

[Browse the planned curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md). Planned titles require a reviewed contract and evaluator before becoming runnable.

## Why this matters on a robot

Direct tracking can use edges and smooth intensity changes where repeatable keypoints are scarce. Rolling shutter, changing illumination, and low texture violate or weaken the photometric model.

## Sources and scope

[Primary paper](https://arxiv.org/abs/1607.02565) · [Open-access manuscript](https://arxiv.org/pdf/1607.02565)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
