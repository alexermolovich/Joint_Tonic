---
schema_version: 1
paper_id: "2022-ik-geo"
title: "IK-Geo: Unified Robot Inverse Kinematics Using Subproblem Decomposition"
authors: ["Elias, Alexander J.","Wen, John T."]
year: 2022
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2211.05737"
pdf_url: "https://arxiv.org/pdf/2211.05737"
local_pdf: "./2022-ik-geo.pdf"
sha256: "992017dc0e28ecfb0739bc93621416cbcf6cf8c705594f5febf71b507050170f"
bytes: 868675
pages: 19
topics: ["planning-control-ik","ik-geo"]
modalities: ["joint-state","poses","obstacles","trajectories"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Express axis geometry","detail":"Represent revolute joints through axes and link offsets.","column":0,"row":0,"section":"Express axis geometry","problem_slugs":["se3-transform-points"],"planned_problems":["Express Revolute Joint-Axis Geometry"]},{"id":"stage-2","title":"Solve geometric subproblems","detail":"Reduce joint angles to circle and plane intersections.","column":1,"row":0,"section":"Solve geometric subproblems","problem_slugs":["serial-chain-forward-kinematics","joint-limit-collision-ik-candidates"],"planned_problems":["Solve a Circle-Plane Rotation Subproblem"]},{"id":"stage-3","title":"Assemble and verify branches","detail":"Combine subproblem roots into full joint solutions.","column":2,"row":0,"section":"Assemble and verify branches","problem_slugs":[],"planned_problems":["Enumerate Valid Joint-Angle Branches","Verify IK Solutions with Forward Kinematics"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"axis relationships"},{"from":"stage-2","to":"stage-3","label":"candidate angles"}]}
---

## Core paper explanation

IK-Geo solves inverse kinematics by decomposing robot geometry into canonical circle-intersection subproblems. Kinematic families defined by intersecting or parallel joint axes determine which analytic reductions or low-dimensional searches apply.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Express axis geometry

Rotation about unit axis $k$ uses Rodrigues' formula:
$$R(k,\theta)=I+\sin\theta[k]_\times+(1-\cos\theta)[k]_\times^2.$$
$[k]_\times v=k\times v$. Axis directions and link offsets must be expressed in the frames required by the robot's forward-kinematics convention.


**Component practice**

- Supporting prerequisite: [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). Practices the stated data or mathematical operation; it does not implement this paper-specific stage in full.
- Express Revolute Joint-Axis Geometry — unreviewed idea; contract and evaluator required.

### Solve geometric subproblems

A basic subproblem seeks $\theta$ with $R(k,\theta)p_1=p_2$. Project perpendicular to $k$: $u=p_1-k(k^\top p_1)$ and $v=p_2-k(k^\top p_2)$. When compatible and nondegenerate,
$$\theta=\operatorname{atan2}(k^\top(u\times v),u^\top v).$$
Axial components and perpendicular lengths must agree for an exact solution; singular and least-squares cases require separate handling.


**Component practice**

- Solve a Circle-Plane Rotation Subproblem — unreviewed idea; contract and evaluator required.

Here $p_1,p_2,u,v\in\mathbb R^3$ are offset vectors in meters, expressed in one common right-handed frame about the chosen axis origin. The axis $k\in\mathbb R^3$ is dimensionless with unit norm, and the returned $\theta$ is in radians. With $k=(0,0,1)$, $p_1=(1,0,0)$, and $p_2=(0,1,0)$, the numerator is one square meter and the denominator zero, so $\theta=\pi/2$. If both perpendicular vectors vanish, the displayed atan2 expression cannot determine a unique angle.

[Compute Forward Kinematics for a Serial Chain](/problems/serial-chain-forward-kinematics) and [Enforce Joint Limits and Collision Constraints in IK](/problems/joint-limit-collision-ik-candidates) practice forward verification and bounded candidate filtering. The latter uses a planar teaching arm and explicit obstacles, not IK-Geo's full six-axis branch enumeration.


### Assemble and verify branches

Enumerate applicable branches, enforce joint limits, and recompute forward kinematics. Position error is measured in meters and orientation error in radians. Some kinematic families permit closed-form solutions; general cases use the paper's reduced searches rather than one universal formula.


**Component practice**

- Enumerate Valid Joint-Angle Branches — unreviewed idea; contract and evaluator required.
- Verify IK Solutions with Forward Kinematics — unreviewed idea; contract and evaluator required.

## Implement the components

Each execution-flow node links the matching runnable component or names its planned problem. Planned titles are not runnable; labels distinguish reviewed drafts from unreviewed ideas.

- **Supporting prerequisite:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points).

**Planned component problems:**

- Express Revolute Joint-Axis Geometry — unreviewed idea; contract and evaluator required.
- Solve a Circle-Plane Rotation Subproblem — unreviewed idea; contract and evaluator required.
- Enumerate Valid Joint-Angle Branches — unreviewed idea; contract and evaluator required.
- Verify IK Solutions with Forward Kinematics — unreviewed idea; contract and evaluator required.

These bounded exercises do not claim to reproduce the complete paper or its benchmark results.

## Why this matters on a robot

Geometric decomposition exposes multiple IK branches and singularities clearly. An algebraically valid solution may collide or require an unsafe transition; trajectory feasibility remains separate from endpoint IK.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2211.05737) · [Open-access manuscript](https://arxiv.org/pdf/2211.05737)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
