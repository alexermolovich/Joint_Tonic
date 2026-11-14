---
schema_version: 1
paper_id: "2017-vins-mono"
title: "VINS-Mono: A Robust and Versatile Monocular Visual-Inertial State Estimator"
authors: ["Qin, Tong","Li, Peiliang","Shen, Shaojie"]
year: 2017
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/1708.03852"
pdf_url: "https://arxiv.org/pdf/1708.03852"
local_pdf: "./2017-vins-mono.pdf"
sha256: "1f44f92f057cbb05a6570f14d2fe5cae2b9736198a8eeca7c93438adbc38a087"
bytes: 4382711
pages: 17
topics: ["geometry-calibration-slam","vins-mono"]
modalities: ["camera","imu","lidar","poses"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Initialize visual-inertial state","detail":"Align visual motion with inertial scale, gravity, and bias.","column":0,"row":0,"section":"Initialize visual-inertial state","problem_slugs":[],"planned_problems":["Detect Unobservable Initialization Motion"]},{"id":"stage-2","title":"Optimize coupled residuals","detail":"Combine visual, inertial, and retained-prior information.","column":1,"row":0,"section":"Optimize coupled residuals","problem_slugs":[],"planned_problems":["Preintegrate a Short IMU Window","Build a Visual-Inertial Residual"]},{"id":"stage-3","title":"Marginalize and correct drift","detail":"Retain old information and use loop constraints.","column":2,"row":0,"section":"Marginalize and correct drift","problem_slugs":[],"planned_problems":["Marginalize a Visual-Inertial Window with a Schur Complement"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"initialized state"},{"from":"stage-2","to":"stage-3","label":"optimized window"}]}
---

## Core paper explanation

VINS-Mono tightly couples monocular feature tracks and IMU measurements in a sliding-window estimator. Initialization estimates a physically consistent visual-inertial state before nonlinear optimization, while marginalization keeps the active problem bounded.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Initialize visual-inertial state

Monocular visual positions initially have unknown scale $s$. The physical displacement must satisfy an inertial relation such as
$$p_j-p_i=v_i\Delta t+\tfrac12g\Delta t^2+R_i\Delta p_{ij}.$$
Here $p,v,g$ are world-frame metric position, velocity, and gravity; $R_i$ maps body to world. Exciting motion is required to distinguish scale, gravity, and biases.


**Planned component problems:** Detect Unobservable Initialization Motion. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

### Optimize coupled residuals

A schematic objective is
$$E=\|r_{\mathrm{prior}}\|^2+\sum\|r_{\mathrm{IMU}}\|_{\Sigma^{-1}}^2+\sum\rho(\|r_{\mathrm{vision}}\|^2).$$
States include poses, velocities, IMU biases, and relevant calibration variables. The residual signs must match the declared gravity and transform conventions.


**Planned component problems:** Preintegrate a Short IMU Window; Build a Visual-Inertial Residual. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

### Marginalize and correct drift

For linearized normal equations partitioned into retained $a$ and removed $b$, the Schur complement is
$$H'=H_{aa}-H_{ab}H_{bb}^{-1}H_{ba}.$$
The corresponding right-hand side is reduced consistently. VINS-Mono also uses loop detection and a four-degree-of-freedom pose graph appropriate to its gravity-aligned setting.




**Planned component problem:** Marginalize a Visual-Inertial Window with a Schur Complement. This is an unreviewed implementation idea for the mechanism above, not a runnable exercise; its precise contract and evaluator must be reviewed before publication.

## Implement the components

- **Related implementation skill:** [Project Camera Points into Pixels](/problems/project-camera-points). This isolates a supporting mechanism, not this paper's complete method.
- **Related implementation skill:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). This isolates a supporting mechanism, not this paper's complete method.

**Planned components:**

- Detect Unobservable Initialization Motion.
- Preintegrate a Short IMU Window.
- Build a Visual-Inertial Residual.
- Marginalize a Visual-Inertial Window with a Schur Complement.

[Browse the planned curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md). Planned titles require a reviewed contract and evaluator before becoming runnable.

## Why this matters on a robot

Visual-inertial coupling can preserve motion estimates through weak visual intervals. Insufficient initialization motion, time offsets, and stale linearization in marginalized priors can undermine consistency.

## Sources and scope

[Primary paper](https://arxiv.org/abs/1708.03852) · [Open-access manuscript](https://arxiv.org/pdf/1708.03852)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
