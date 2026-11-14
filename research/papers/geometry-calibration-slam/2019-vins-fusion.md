---
schema_version: 1
paper_id: 2019-vins-fusion
title: >-
  A General Optimization-based Framework for Global Pose Estimation with
  Multiple Sensors
authors:
  - 'Qin, Tong'
  - 'Cao, Shaozu'
  - 'Pan, Jie'
  - 'Shen, Shaojie'
year: 2019
venue_or_status: >-
  Author-deposited arXiv manuscript; final venue not asserted by this
  acquisition card.
primary_url: 'https://arxiv.org/abs/1901.03642'
pdf_url: 'https://arxiv.org/pdf/1901.03642'
local_pdf: ./2019-vins-fusion.pdf
sha256: ca2210ff843cb9e37d441165ded11296257ecc17600cf46596eea19526621783
bytes: 5289163
pages: 7
topics:
  - geometry-calibration-slam
  - vins-fusion
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
      title: Obtain local odometry
      detail: Use relative motion from an existing local estimator.
      column: 0
      row: 0
      section: Obtain local odometry
      problem_slugs:
        - relative-odometry-edges
      planned_problems: []
    - id: stage-2
      title: Add global measurements
      detail: Align the local trajectory to a global reference.
      column: 1
      row: 0
      section: Add global measurements
      problem_slugs:
        - global-sensor-pose-factors
        - match-approximate-sensor-timestamps
      planned_problems: []
    - id: stage-3
      title: Optimize the pose graph
      detail: Balance local consistency with globally anchored observations.
      column: 2
      row: 0
      section: Optimize the pose graph
      problem_slugs:
        - sensor-configuration-drift
      planned_problems: []
  edges:
    - from: stage-1
      to: stage-2
      label: relative poses
    - from: stage-2
      to: stage-3
      label: local and global factors
---

## Core paper explanation

This paper presents global pose estimation by fusing locally accurate odometry with globally referenced sensors. The existing card ID is VINS-Fusion, but the primary paper specifically concerns the global optimization layer combining local pose estimates with GPS and other global measurements.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Obtain local odometry

For local odometry poses $\hat T_i$, relative motion is $\hat T_{ij}=\hat T_i^{-1}\hat T_j$. Local estimates may come from visual, inertial, or other odometry; the global layer does not replace their raw sensor processing. The relative-edge exercise takes supplied temporal indices and maps body-j coordinates into body-i coordinates; its displacement-over-duration output is chord speed, not traveled-path speed.




**Implement these components:** [Construct Relative Pose Measurements from Local Odometry](/problems/relative-odometry-edges). Each linked exercise declares its bounded numerical and physical contract; these are not full estimator reproductions.

### Add global measurements

For world position $p_i$ and GPS position $g_i$, a position residual is $r_i^{\mathrm{GPS}}=p_i-g_i$. Sensor lever arms and coordinate conversions must be included when measurement locations differ. GPS covariance is in squared meters and should determine the residual weighting. The sensor-factor exercise uses a shared calibrated sensor mounting frame, ENU coordinates, measured-minus-predicted residuals, and diagonal standard deviations for GPS position, magnetic direction and converted barometric height. Its magnetic model normalizes field directions rather than treating them as positions. The reused timestamp exercise only associates independent queries to nearest keyframes on an already synchronized clock, with inclusive tolerance and lower-index ties; it does not interpolate measurements or correct clocks.


**Implement these components:** [Assemble Sensor-Specific Pose Factors](/problems/global-sensor-pose-factors) · [Match Approximate Sensor Timestamps](/problems/match-approximate-sensor-timestamps). Each linked exercise declares its bounded numerical and physical contract; these are not full estimator reproductions.

### Optimize the pose graph

A teaching objective is
$$E=\sum_{ij}\|\operatorname{Log}(\hat T_{ij}^{-1}T_i^{-1}T_j)\|_{\Omega_{ij}}^2+\sum_i\|p_i-g_i\|_{\Sigma_i^{-1}}^2.$$
Rotation/translation weights must have consistent units. Magnetometer and barometer observations add their own measurement models; they cannot be treated as interchangeable 3D positions. The drift comparison evaluates supplied, time-matched positions on common support across every configuration. It reports coverage, position RMSE and final common-sample error without fitting an alignment; these diagnostics do not reproduce pose-graph optimization or isolate drift from every other error source.


**Implement these components:** [Compare Drift Across Sensor Configurations](/problems/sensor-configuration-drift). Each linked exercise declares its bounded numerical and physical contract; these are not full estimator reproductions.

## Implement the components

- **Related implementation skill:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). This isolates a supporting mechanism, not this paper's complete method.

**Runnable components and remaining ideas:**

- [Construct Relative Pose Measurements from Local Odometry](/problems/relative-odometry-edges) — runnable bounded component.
- [Assemble Sensor-Specific Pose Factors](/problems/global-sensor-pose-factors) — runnable bounded component.
- [Match Approximate Sensor Timestamps](/problems/match-approximate-sensor-timestamps) — runnable bounded component.
- [Compare Drift Across Sensor Configurations](/problems/sensor-configuration-drift) — runnable bounded component.

[Browse the planned curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md). Planned titles require a reviewed contract and evaluator before becoming runnable.

## Why this matters on a robot

Global observations limit accumulated odometry drift. Multipath GPS, magnetic disturbance, and mismatched timestamps can pull an otherwise good local trajectory toward incorrect global constraints.

## Sources and scope

[Primary paper](https://arxiv.org/abs/1901.03642) · [Open-access manuscript](https://arxiv.org/pdf/1901.03642)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
