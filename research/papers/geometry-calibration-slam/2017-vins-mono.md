---
schema_version: 1
paper_id: 2017-vins-mono
title: 'VINS-Mono: A Robust and Versatile Monocular Visual-Inertial State Estimator'
authors:
  - 'Qin, Tong'
  - 'Li, Peiliang'
  - 'Shen, Shaojie'
year: 2017
venue_or_status: >-
  Author-deposited arXiv manuscript; final venue not asserted by this
  acquisition card.
primary_url: 'https://arxiv.org/abs/1708.03852'
pdf_url: 'https://arxiv.org/pdf/1708.03852'
local_pdf: ./2017-vins-mono.pdf
sha256: 1f44f92f057cbb05a6570f14d2fe5cae2b9736198a8eeca7c93438adbc38a087
bytes: 4382711
pages: 17
topics:
  - geometry-calibration-slam
  - vins-mono
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
      title: Initialize visual-inertial state
      detail: 'Align visual motion with inertial scale, gravity, and bias.'
      column: 0
      row: 0
      section: Initialize visual-inertial state
      problem_slugs:
        - trace-perception-frame-graph
        - estimate-clock-offset-paired-events
        - initialization-observability-rank
      planned_problems: []
    - id: stage-2
      title: Optimize coupled residuals
      detail: 'Combine visual, inertial, and retained-prior information.'
      column: 1
      row: 0
      section: Optimize coupled residuals
      problem_slugs:
        - short-window-imu-preintegration
        - visual-inertial-keyframe-residual
      planned_problems: []
    - id: stage-3
      title: Marginalize and correct drift
      detail: Retain old information and use loop constraints.
      column: 2
      row: 0
      section: Marginalize and correct drift
      problem_slugs:
        - schur-window-marginalization
      planned_problems: []
  edges:
    - from: stage-1
      to: stage-2
      label: initialized state
    - from: stage-2
      to: stage-3
      label: optimized window
---

## Core paper explanation

VINS-Mono tightly couples monocular feature tracks and IMU measurements in a sliding-window estimator. Initialization estimates a physically consistent visual-inertial state before nonlinear optimization, while marginalization keeps the active problem bounded.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Initialize visual-inertial state

Monocular visual positions initially have unknown scale $s$. The physical displacement must satisfy an inertial relation such as
$$p_j-p_i=v_i\Delta t+\tfrac12g\Delta t^2+R_i\Delta p_{ij}.$$
Here $p,v,g$ are world-frame metric position, velocity, and gravity; $R_i$ maps body to world. Exciting motion is required to distinguish scale, gravity, and biases. The linked initialization exercise diagnoses a supplied, gauge-fixed linearization after physical column scaling and measurement whitening; it is not the paper's exact initialization motion heuristic.


**Implement these components:** [Detect Unobservable Initialization Motion](/problems/initialization-observability-rank). The exercises state their bounded frame, numerical and diagnostic conventions; they do not reproduce the complete estimator.

Here $p_i,p_j,v_i,g\in\mathbb R^3$, $R_i\in\mathbb R^{3\times3}$, and the interval $\Delta t$ is in seconds. The preintegrated $\Delta p_{ij}$ is in the initial body frame and excludes gravity; multiplying by $R_i$ puts it in the world frame. For $v_i=0$, $\Delta t=0.1$, world gravity $(0,0,-9.81)$, identity $R_i$, and stationary-sensor increment $\Delta p_{ij}=(0,0,0.04905)$ meters, the gravity and specific-force contributions cancel, giving zero displacement. This checks a sign convention, not initialization observability.

[Trace Frames Through a Robot Perception Graph](/problems/trace-perception-frame-graph) practices composition of sensor extrinsics, and [Estimate Clock Offset from Paired Events](/problems/estimate-clock-offset-paired-events) practices synchronization before combining camera and inertial evidence. These supporting exercises do not solve monocular scale or the sliding-window estimator.


### Optimize coupled residuals

A schematic objective is
$$E=\|r_{\mathrm{prior}}\|^2+\sum\|r_{\mathrm{IMU}}\|_{\Sigma^{-1}}^2+\sum\rho(\|r_{\mathrm{vision}}\|^2).$$
States include poses, velocities, IMU biases, and relevant calibration variables. The residual signs must match the declared gravity and transform conventions. The linked window integrator uses an explicit zero-order hold, and the keyframe factor uses supplied visual residuals with diagonal uncertainties. Full covariance, bias-state residuals and nonlinear optimization remain outside these components.


**Implement these components:** [Preintegrate a Short IMU Window](/problems/short-window-imu-preintegration) · [Build a Visual-Inertial Residual](/problems/visual-inertial-keyframe-residual). The exercises state their bounded frame, numerical and diagnostic conventions; they do not reproduce the complete estimator.

### Marginalize and correct drift

For linearized normal equations partitioned into retained $a$ and removed $b$, the Schur complement is
$$H'=H_{aa}-H_{ab}H_{bb}^{-1}H_{ba}.$$
The corresponding right-hand side is reduced consistently. The runnable marginalization exercise also preserves the minimized quadratic constant, reconstructs the removed-state optimum, and requires a gauge-fixed system with bounded condition number. VINS-Mono also uses loop detection and a four-degree-of-freedom pose graph appropriate to its gravity-aligned setting.




**Implement these components:** [Marginalize a Visual-Inertial Window with a Schur Complement](/problems/schur-window-marginalization). The exercises state their bounded frame, numerical and diagnostic conventions; they do not reproduce the complete estimator.

## Implement the components

- **Related implementation skill:** [Project Camera Points into Pixels](/problems/project-camera-points). This isolates a supporting mechanism, not this paper's complete method.
- **Related implementation skill:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). This isolates a supporting mechanism, not this paper's complete method.

**Runnable components and remaining ideas:**

- [Detect Unobservable Initialization Motion](/problems/initialization-observability-rank) — runnable bounded component.
- [Preintegrate a Short IMU Window](/problems/short-window-imu-preintegration) — runnable bounded component.
- [Build a Visual-Inertial Residual](/problems/visual-inertial-keyframe-residual) — runnable bounded component.
- [Marginalize a Visual-Inertial Window with a Schur Complement](/problems/schur-window-marginalization) — runnable bounded component.

[Browse the planned curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md). Planned titles require a reviewed contract and evaluator before becoming runnable.

## Why this matters on a robot

Visual-inertial coupling can preserve motion estimates through weak visual intervals. Insufficient initialization motion, time offsets, and stale linearization in marginalized priors can undermine consistency.

## Sources and scope

[Primary paper](https://arxiv.org/abs/1708.03852) · [Open-access manuscript](https://arxiv.org/pdf/1708.03852)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
