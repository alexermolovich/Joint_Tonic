---
schema_version: 1
paper_id: "2018-motion-planning-networks"
title: "Motion Planning Networks"
authors: ["Qureshi, Ahmed H.","Simeonov, Anthony","Bency, Mayur J.","Yip, Michael C."]
year: 2018
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/1806.05767"
pdf_url: "https://arxiv.org/pdf/1806.05767"
local_pdf: "./2018-motion-planning-networks.pdf"
sha256: "f473ab377fe93612b351a1181c788fd9b8a21d576b5ee699b37bf6bb8c9f0686"
bytes: 1204399
pages: 7
topics: ["planning-control-ik","motion-planning-networks"]
modalities: ["joint-state","poses","obstacles","trajectories"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
---

# Motion Planning Networks

## Agent brief

Study learned motion planning through environment encodings and waypoint prediction interfaces. This acquisition card verifies the primary paper identity and local PDF, and proposes components that can become independently testable Joint Tonic problems. Full-text technical review is required before promoting an idea into a reviewed problem blueprint.

## Contribution

Study learned motion planning through environment encodings and waypoint prediction interfaces.

The proposed exercises below are original teaching decompositions. They do not assert a full reproduction of the paper or any published performance number.

## Prerequisite concepts

- Forward kinematics, Jacobians, joint limits, collision geometry, optimization, and derivative constraints.

## Method map

| Component candidate | Input | Output | Core invariant | Good exercise boundary |
|---|---|---|---|---|
| Encode Obstacles into a Fixed Feature | Joint states, robot kinematic parameters, target poses, obstacle geometry, and a time horizon | Joint configurations, feasible paths, trajectory costs, or control updates | Check forward-kinematics residuals, collisions, joint/velocity limits, singular or unreachable goals, and seeded search behavior. | One bounded function or validation stage |
| Predict and Validate an Intermediate Waypoint | Joint states, robot kinematic parameters, target poses, obstacle geometry, and a time horizon | Joint configurations, feasible paths, trajectory costs, or control updates | Check forward-kinematics residuals, collisions, joint/velocity limits, singular or unreachable goals, and seeded search behavior. | One bounded function or validation stage |
| Repair an Infeasible Planned Segment | Joint states, robot kinematic parameters, target poses, obstacle geometry, and a time horizon | Joint configurations, feasible paths, trajectory costs, or control updates | Check forward-kinematics residuals, collisions, joint/velocity limits, singular or unreachable goals, and seeded search behavior. | One bounded function or validation stage |

## Data and evaluation

A small teaching implementation should use synthetic or separately licensed fixtures. Check forward-kinematics residuals, collisions, joint/velocity limits, singular or unreachable goals, and seeded search behavior. Dataset names, exact protocol details, published metrics, and hardware requirements must be checked in the source PDF during full-text review; they are not inferred from an awesome-list entry. Keep educational component tests distinct from the paper's end-to-end evaluation.

## Limitations and failure modes

- This is a concise acquisition card, not a full-text technical review. Confirm equations, architecture details, and paper-stated limitations in the PDF before authoring theory.
- Passing synthetic component tests does not establish real-robot performance, robustness, or safe deployment.
- Pin robot/scene assets, collision margins, solver tolerances, timestep, and seed; report feasibility and tail latency with replay evidence. Integrate through the MuJoCo/Isaac sidecar adapter.
- The paper, linked code, datasets, assets, and weights may carry different license conditions.

## Implementation decomposition

1. Encode Obstacles into a Fixed Feature.
2. Predict and Validate an Intermediate Waypoint.
3. Repair an Infeasible Planned Segment.
4. Integrate the components on a small fixed fixture and record all deviations from the paper.
5. Add failure slices and a reproducible artifact report.

## Problem blueprints

### Problem: Encode Obstacles into a Fixed Feature

- **Type:** component
- **Difficulty:** medium
- **Learning objective:** Implement and explain the encode obstacles into a fixed feature component.
- **Inputs:** Joint states, robot kinematic parameters, target poses, obstacle geometry, and a time horizon; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Joint configurations, feasible paths, trajectory costs, or control updates; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check forward-kinematics residuals, collisions, joint/velocity limits, singular or unreachable goals, and seeded search behavior. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Predict and Validate an Intermediate Waypoint

- **Type:** component
- **Difficulty:** hard
- **Learning objective:** Implement and explain the predict and validate an intermediate waypoint component.
- **Inputs:** Joint states, robot kinematic parameters, target poses, obstacle geometry, and a time horizon; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Joint configurations, feasible paths, trajectory costs, or control updates; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check forward-kinematics residuals, collisions, joint/velocity limits, singular or unreachable goals, and seeded search behavior. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Repair an Infeasible Planned Segment

- **Type:** pipeline
- **Difficulty:** hard
- **Learning objective:** Implement and explain the repair an infeasible planned segment component.
- **Inputs:** Joint states, robot kinematic parameters, target poses, obstacle geometry, and a time horizon; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Joint configurations, feasible paths, trajectory costs, or control updates; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check forward-kinematics residuals, collisions, joint/velocity limits, singular or unreachable goals, and seeded search behavior. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

## Visual teaching plan

- Show learned waypoints, collision checks, and repaired path segments.
- Provide labeled axes, units, coordinate frames, and an equivalent table/text view. Use discrete steps when reduced motion is requested.
- Author diagrams independently; do not copy paper figures or captions.

## MLOps and deployment extensions

- Pin robot/scene assets, collision margins, solver tolerances, timestep, and seed; report feasibility and tail latency with replay evidence. Integrate through the MuJoCo/Isaac sidecar adapter.
- Store paper ID, fixture hash, evaluator version, dependency lock, runtime digest, seed, and resource class with every result.
- Use structured failure reasons and per-slice metrics to distinguish implementation mistakes, distribution shifts, and infrastructure failures.

## Canonical sources

- [Primary arXiv record](https://arxiv.org/abs/1806.05767)
- [Open-access author manuscript](https://arxiv.org/pdf/1806.05767)

Identity metadata was read from the primary arXiv record. Local file signature, byte count, page parsing, and SHA-256 were verified on acquisition.

