---
schema_version: 1
paper_id: "2015-on-manifold-preintegration"
title: "On-Manifold Preintegration for Real-Time Visual-Inertial Odometry"
authors: ["Forster, Christian","Carlone, Luca","Dellaert, Frank","Scaramuzza, Davide"]
year: 2015
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/1512.02363"
pdf_url: "https://arxiv.org/pdf/1512.02363"
local_pdf: "./2015-on-manifold-preintegration.pdf"
sha256: "214b8bee53e1fb6218c1cec1352d74c24951feec815517e6a0cc6dfcf1fd8f32"
bytes: 3816161
pages: 21
topics: ["geometry-calibration-slam","on-manifold-preintegration"]
modalities: ["camera","imu","lidar","poses"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Integrate relative rotation","detail":"Accumulate bias-corrected angular increments.","column":0,"row":0,"section":"Integrate relative rotation","problem_slugs":[],"planned_problems":["Integrate IMU Rotation Increments on SO3"]},{"id":"stage-2","title":"Integrate velocity and position","detail":"Accumulate specific force in the starting body frame.","column":1,"row":0,"section":"Integrate velocity and position","problem_slugs":[],"planned_problems":["Preintegrate Bias-Corrected IMU Velocity and Position"]},{"id":"stage-3","title":"Form a keyframe factor","detail":"Compare predicted state change with preintegrated measurements.","column":2,"row":0,"section":"Form a keyframe factor","problem_slugs":[],"planned_problems":["Propagate Preintegration Covariance","Apply a First-Order Bias Correction"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"relative rotations"},{"from":"stage-2","to":"stage-3","label":"preintegrated measurements"}]}
---

## Core paper explanation

On-manifold IMU preintegration summarizes many high-rate inertial samples into a constraint between keyframes. Rotation is integrated on SO(3), and bias Jacobians allow small bias corrections without replaying every sample.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Integrate relative rotation

Let $R_i$ map body-frame vectors to world coordinates. For angular rate $\omega_k$ in radians per second, gyro bias $b_g$, and sample duration $\Delta t$,
$$\Delta R_{i,k+1}=\Delta R_{ik}\operatorname{Exp}((\omega_k-b_g)\Delta t).$$
$\operatorname{Exp}$ maps a rotation vector into SO(3). Multiplication order follows this body-frame convention.


**Planned component problems:** Integrate IMU Rotation Increments on SO3. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

### Integrate velocity and position

With accelerometer specific force $a_k$ and bias $b_a$ in meters per second squared,
$$\Delta v_{i,k+1}=\Delta v_{ik}+\Delta R_{ik}(a_k-b_a)\Delta t,$$
$$\Delta p_{i,k+1}=\Delta p_{ik}+\Delta v_{ik}\Delta t+\tfrac12\Delta R_{ik}(a_k-b_a)\Delta t^2.$$
These first-order discrete updates show the mechanism. Covariance and bias Jacobians propagate alongside the mean.




**Planned component problem:** Preintegrate Bias-Corrected IMU Velocity and Position. This is an unreviewed implementation idea for the mechanism above, not a runnable exercise; its precise contract and evaluator must be reviewed before publication.

### Form a keyframe factor

For world gravity $g$, the velocity residual is
$$r_v=R_i^\top(v_j-v_i-g\Delta t_{ij})-\Delta v_{ij}.$$
Rotation, position, and bias residuals complete the factor; whiten with the propagated covariance. Small bias changes use analytic first-order correction, while large changes may require reintegration.


**Planned component problems:** Propagate Preintegration Covariance; Apply a First-Order Bias Correction. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

## Implement the components

- **Related implementation skill:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). This isolates a supporting mechanism, not this paper's complete method.

**Planned components:**

- Integrate IMU Rotation Increments on SO3.
- Preintegrate Bias-Corrected IMU Velocity and Position.
- Propagate Preintegration Covariance.
- Apply a First-Order Bias Correction.

[Browse the planned curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md). Planned titles require a reviewed contract and evaluator before becoming runnable.

## Why this matters on a robot

Preintegration makes visual-inertial optimization practical without discarding high-rate IMU information. Wrong gravity sign, timestamp intervals, or IMU-to-camera extrinsics cause systematic drift that an optimizer cannot repair by adding more iterations.

## Sources and scope

[Primary paper](https://arxiv.org/abs/1512.02363) · [Open-access manuscript](https://arxiv.org/pdf/1512.02363)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
