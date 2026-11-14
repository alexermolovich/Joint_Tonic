---
schema_version: 1
paper_id: "2023-curobo"
title: "cuRobo: Parallelized Collision-Free Minimum-Jerk Robot Motion Generation"
authors: ["Sundaralingam, Balakumar","Hari, Siva Kumar Sastry","Fishman, Adam","Garrett, Caelan","Van Wyk, Karl","Blukis, Valts","Millane, Alexander","Oleynikova, Helen","Handa, Ankur","Ramos, Fabio","Ratliff, Nathan","Fox, Dieter"]
year: 2023
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2310.17274"
pdf_url: "https://arxiv.org/pdf/2310.17274"
local_pdf: "./2023-curobo.pdf"
sha256: "cffeaf2d4e7a396f0d0ae99b2213688f19a24f756cccb828bd16fca223abc561"
bytes: 12464082
pages: 62
topics: ["planning-control-ik","curobo"]
modalities: ["joint-state","poses","obstacles","trajectories"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
---

# cuRobo: Parallelized Collision-Free Minimum-Jerk Robot Motion Generation

## Agent brief

Study parallel collision-free robot motion generation through batched kinematics and trajectory costs. This acquisition card verifies the primary paper identity and local PDF, and proposes components that can become independently testable Joint Tonic problems. Full-text technical review is required before promoting an idea into a reviewed problem blueprint.

## Contribution

Study parallel collision-free robot motion generation through batched kinematics and trajectory costs.

The proposed exercises below are original teaching decompositions. They do not assert a full reproduction of the paper or any published performance number.

## Prerequisite concepts

- Forward kinematics, Jacobians, joint limits, collision geometry, optimization, and derivative constraints.

## Method map

| Component candidate | Input | Output | Core invariant | Good exercise boundary |
|---|---|---|---|---|
| Batch Forward-Kinematics Queries | Joint states, robot kinematic parameters, target poses, obstacle geometry, and a time horizon | Joint configurations, feasible paths, trajectory costs, or control updates | Check forward-kinematics residuals, collisions, joint/velocity limits, singular or unreachable goals, and seeded search behavior. | One bounded function or validation stage |
| Compute a Signed-Distance Collision Cost | Joint states, robot kinematic parameters, target poses, obstacle geometry, and a time horizon | Joint configurations, feasible paths, trajectory costs, or control updates | Check forward-kinematics residuals, collisions, joint/velocity limits, singular or unreachable goals, and seeded search behavior. | One bounded function or validation stage |
| Rank Multi-Seed Motion Trajectories | Joint states, robot kinematic parameters, target poses, obstacle geometry, and a time horizon | Joint configurations, feasible paths, trajectory costs, or control updates | Check forward-kinematics residuals, collisions, joint/velocity limits, singular or unreachable goals, and seeded search behavior. | One bounded function or validation stage |

## Data and evaluation

A small teaching implementation should use synthetic or separately licensed fixtures. Check forward-kinematics residuals, collisions, joint/velocity limits, singular or unreachable goals, and seeded search behavior. Dataset names, exact protocol details, published metrics, and hardware requirements must be checked in the source PDF during full-text review; they are not inferred from an awesome-list entry. Keep educational component tests distinct from the paper's end-to-end evaluation.

## Limitations and failure modes

- This is a concise acquisition card, not a full-text technical review. Confirm equations, architecture details, and paper-stated limitations in the PDF before authoring theory.
- Passing synthetic component tests does not establish real-robot performance, robustness, or safe deployment.
- Pin robot/scene assets, collision margins, solver tolerances, timestep, and seed; report feasibility and tail latency with replay evidence. Integrate through the MuJoCo/Isaac sidecar adapter.
- The paper, linked code, datasets, assets, and weights may carry different license conditions.

## Implementation decomposition

1. Batch Forward-Kinematics Queries.
2. Compute a Signed-Distance Collision Cost.
3. Rank Multi-Seed Motion Trajectories.
4. Integrate the components on a small fixed fixture and record all deviations from the paper.
5. Add failure slices and a reproducible artifact report.

## Problem blueprints

### Problem: Batch Forward-Kinematics Queries

- **Type:** component
- **Difficulty:** medium
- **Learning objective:** Implement and explain the batch forward-kinematics queries component.
- **Inputs:** Joint states, robot kinematic parameters, target poses, obstacle geometry, and a time horizon; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Joint configurations, feasible paths, trajectory costs, or control updates; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check forward-kinematics residuals, collisions, joint/velocity limits, singular or unreachable goals, and seeded search behavior. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Compute a Signed-Distance Collision Cost

- **Type:** component
- **Difficulty:** hard
- **Learning objective:** Implement and explain the compute a signed-distance collision cost component.
- **Inputs:** Joint states, robot kinematic parameters, target poses, obstacle geometry, and a time horizon; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Joint configurations, feasible paths, trajectory costs, or control updates; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check forward-kinematics residuals, collisions, joint/velocity limits, singular or unreachable goals, and seeded search behavior. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Rank Multi-Seed Motion Trajectories

- **Type:** pipeline
- **Difficulty:** hard
- **Learning objective:** Implement and explain the rank multi-seed motion trajectories component.
- **Inputs:** Joint states, robot kinematic parameters, target poses, obstacle geometry, and a time horizon; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Joint configurations, feasible paths, trajectory costs, or control updates; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check forward-kinematics residuals, collisions, joint/velocity limits, singular or unreachable goals, and seeded search behavior. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

## Visual teaching plan

- Show many candidate arm paths and the chosen collision-free trajectory.
- Provide labeled axes, units, coordinate frames, and an equivalent table/text view. Use discrete steps when reduced motion is requested.
- Author diagrams independently; do not copy paper figures or captions.

## MLOps and deployment extensions

- Pin robot/scene assets, collision margins, solver tolerances, timestep, and seed; report feasibility and tail latency with replay evidence. Integrate through the MuJoCo/Isaac sidecar adapter.
- Store paper ID, fixture hash, evaluator version, dependency lock, runtime digest, seed, and resource class with every result.
- Use structured failure reasons and per-slice metrics to distinguish implementation mistakes, distribution shifts, and infrastructure failures.

## Canonical sources

- [Primary arXiv record](https://arxiv.org/abs/2310.17274)
- [Open-access author manuscript](https://arxiv.org/pdf/2310.17274)

Identity metadata was read from the primary arXiv record. Local file signature, byte count, page parsing, and SHA-256 were verified on acquisition.

