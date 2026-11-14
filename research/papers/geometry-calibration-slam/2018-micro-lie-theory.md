---
schema_version: 1
paper_id: 2018-micro-lie-theory
title: A micro Lie theory for state estimation in robotics
authors:
  - Joan Solà
  - Jeremie Deray
  - Dinesh Atchuthan
year: 2018
venue_or_status: Technical report IRI-TR-18-01; arXiv v9 (2021 revision)
primary_url: 'https://arxiv.org/abs/1812.01537'
pdf_url: 'https://arxiv.org/pdf/1812.01537v9'
local_pdf: ./2018-micro-lie-theory.pdf
sha256: 93190a60ad5f390006970f684ba8590bf55ce21adc3c1cb675adc55ead17f869
bytes: 1576616
pages: 17
topics:
  - Lie groups
  - state estimation
  - SE(3)
  - geometry
modalities:
  - poses
  - inertial state
  - geometric measurements
track_role: supporting
open_access_status: open-access-preprint
redistribution_note: >-
  Local research reference only. Open-access source verified; downstream
  redistribution rights have not been audited. The PDF is not a public product
  asset.
acquired_on: '2026-11-13'
source_verification: >-
  Primary title/authors and version checked; PDF signature, all-page parser
  readability, first-page visual render, count and SHA-256 validated.
execution_flow:
  title: Selected mechanism and implementation path
  description: >-
    A compact treatment of Lie-group perturbations, Jacobians and uncertainty
    for robot state estimation. It helps make pose-update conventions executable
    rather than treating a rotation matrix as an unconstrained array.
  nodes:
    - id: pose
      title: Represent a pose
      detail: >-
        Represent a pose. See the original explanation and component status
        below.
      column: 0
      row: 0
      section: Represent a pose
      problem_slugs:
        - compose-frame-transforms
        - normalize-multiply-quaternions
        - interpolate-pose-slerp
      planned_problems: []
    - id: update
      title: Apply a tangent update
      detail: >-
        Apply a tangent update. See the original explanation and component
        status below.
      column: 1
      row: 0
      section: Apply a tangent update
      problem_slugs:
        - se3-exponential-logarithm
      planned_problems: []
    - id: linearize
      title: Linearize an estimation residual
      detail: >-
        Linearize an estimation residual. See the original explanation and
        component status below.
      column: 2
      row: 0
      section: Linearize an estimation residual
      problem_slugs:
        - kalman-filter-measurement-update
        - finite-difference-gradient-check
      planned_problems: []
  edges:
    - from: pose
      to: update
      label: validated component output
    - from: update
      to: linearize
      label: validated component output
---

## Core paper explanation

Rigid poses live on a constrained space: adding arbitrary entries to a rotation matrix generally stops it being a rotation. The paper organizes local perturbations, Jacobians and covariance propagation around small tangent vectors. A practical implementation must choose which side receives an update and which frame expresses its coordinates.

## Execution flow

### Represent a pose

Let $T_{ab}\in SE(3)$ map a column point from frame b into frame a. Its rotation $R_{ab}\in SO(3)$ is dimensionless and translation $\mathbf t_{ab}\in\mathbb R^3$ is in meters:

$$
T_{ab}=\begin{bmatrix}R_{ab}&\mathbf t_{ab}\\0&1\end{bmatrix},
\qquad \mathbf p_a=R_{ab}\mathbf p_b+\mathbf t_{ab}.
$$

All poses and measurements must refer to a declared time. [Compose and Invert Coordinate Transforms](/problems/compose-frame-transforms) and [Normalize and Multiply Quaternions](/problems/normalize-multiply-quaternions) are implemented prerequisites, not the complete Lie-estimation method.

[Interpolate a Pose with SLERP](/problems/interpolate-pose-slerp) is now runnable. It interpolates translation linearly and unit quaternions on the shortest arc; it is a prerequisite in pose representation, not an implementation of the paper's general Lie-group exponential and logarithm maps.


### Apply a tangent update

Use a six-vector $\delta\boldsymbol\xi=(\delta\boldsymbol\rho,\delta\boldsymbol\phi)$ with translation coordinates in meters and rotation coordinates in radians. The hat operator places these in a matrix:

$$
\delta\boldsymbol\xi^\wedge=
\begin{bmatrix}[\delta\boldsymbol\phi]_\times&\delta\boldsymbol\rho\\0&0\end{bmatrix},
\qquad T^+=T\exp(\delta\boldsymbol\xi^\wedge).
$$

This is a right perturbation, so the increment is local to the current pose. A left perturbation instead uses $\exp(\delta\boldsymbol\xi^\wedge)T$ and a different coordinate convention. Translation in the exponential is coupled to rotation; copying the tangent translation into T's final column is only a special-case simplification.

For a pure local x translation of0.1m after a90-degree rotation about world z, right composition moves the world point by0.1m along world y. Left composition with a world-x increment moves it along world x. This is a convention test, not merely a numerical tolerance.

Implement [Apply SE(3) Exponential and Logarithm Maps](/problems/se3-exponential-logarithm). The exercise supports a stated principal-angle range and explicitly excludes the ambiguous pi branch.

### Linearize an estimation residual

Let $\mathbf r(T)\in\mathbb R^m$ be a measurement residual in declared sensor units. Define its right-perturbation Jacobian $J\in\mathbb R^{m\times6}$ by

$$
\mathbf r(T\exp(\delta\boldsymbol\xi^\wedge))
\approx \mathbf r(T)+J\,\delta\boldsymbol\xi,
\qquad P_y\approx J P_\xi J^\top.
$$

$P_\xi$ is tangent-space covariance; its translation, rotation and cross blocks carry corresponding squared or mixed units. A finite-difference check must perturb T on the same side used in the derivation. [Finite-Difference Gradient Check](/problems/finite-difference-gradient-check) is a runnable numerical prerequisite; a pose-residual Jacobian must still use the same perturbation side as its derivation. The linear Kalman prerequisite is available below.

| Convention | Increment coordinates | Update |
|---|---|---|
| Right | Local/body tangent | T followed by exponential |
| Left | Reference/world tangent | Exponential followed by T |

The table is an original text alternative to the execution graph.

[One Kalman Filter Measurement Update](/problems/kalman-filter-measurement-update) implements a Euclidean linear-Gaussian update with explicit covariance validation. Its uncertainty bookkeeping is useful prerequisite practice; replacing a pose with an unconstrained Euclidean vector does not implement this Lie-group estimator.


## Why this matters on a robot

Mixing left/right Jacobians can make an estimator appear stable near identity and diverge after a turn. Track frame names, perturbation order, covariance convention and calibration version with every log. Small-angle approximations also need explicit near-zero handling.

## Implement the components

The linked pose exercises and bounded exponential/logarithm maps are available now. General estimator residuals remain further implementation work; none of these exercises claims to reproduce a full SLAM or filtering system. This card summarizes selected mechanisms from the versioned technical report rather than its complete formula catalog.


## Sources and scope

[Canonical primary record](https://arxiv.org/abs/1812.01537) · [Pinned openly accessible manuscript](https://arxiv.org/pdf/1812.01537v9). This is an original selected-mechanism explanation, not a full-text transcription. Linked exercises are identified as direct components or supporting prerequisites. Planned node titles are research/curriculum ideas, not published problems; new ideas require a reviewed blueprint before implementation. PDF provenance and reuse status are recorded above.
