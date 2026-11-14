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
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Generate goal configurations","detail":"Solve collision-aware IK from multiple seeds.","column":0,"row":0,"section":"Generate goal configurations","problem_slugs":["se3-transform-points"],"planned_problems":["Batch Forward-Kinematics Queries"]},{"id":"stage-2","title":"Optimize parallel trajectories","detail":"Combine endpoint, collision, and smoothness costs.","column":1,"row":0,"section":"Optimize parallel trajectories","problem_slugs":[],"planned_problems":["Compute a Signed-Distance Collision Cost"]},{"id":"stage-3","title":"Validate and time the motion","detail":"Check refined trajectories and produce executable samples.","column":2,"row":0,"section":"Validate and time the motion","problem_slugs":["edge-inference-release-gate"],"planned_problems":["Rank Multi-Seed Motion Trajectories"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"trajectory seeds"},{"from":"stage-2","to":"stage-3","label":"optimized candidates"}]}
---

## Core paper explanation

cuRobo accelerates manipulator motion generation with GPU-parallel inverse kinematics, collision checking, trajectory optimization, and geometric planning. Many seeds and efficient optimization improve the chance of quickly finding a valid smooth motion.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Generate goal configurations

For desired end-effector pose $T^*$, IK penalizes translation and orientation residuals while respecting joint limits and collision geometry. Candidate configurations $q^*_k$ seed trajectories from the current state. A successful endpoint solve does not validate the path to it.


**Component practice**

- Supporting prerequisite: [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). Practices the stated data or mathematical operation; it does not implement this paper-specific stage in full.
- Batch Forward-Kinematics Queries — unreviewed idea; contract and evaluator required.

### Optimize parallel trajectories

A schematic cost is
$$J(q_{0:H})=J_{\mathrm{goal}}+\lambda_cJ_{\mathrm{collision}}+\lambda_j\sum_t\|\dddot q_t\|_2^2.$$
Finite-difference jerk includes the timestep cubed in its denominator; omitting time changes the physical meaning. The paper combines particle-based optimization and L-BFGS with a parallel noisy line search.


**Component practice**

- Compute a Signed-Distance Collision Cost — unreviewed idea; contract and evaluator required.

### Validate and time the motion

Collision costs rely on the declared robot collision model and environment representation. Check interpolated motion, limits, and timing after optimization; use a geometric planner when needed for better initialization. Published GPU timing is workload-specific, not a deadline guarantee for arbitrary scenes.


**Component practice**

- Supporting prerequisite: [Gate an Edge Model with Accuracy and Latency](/problems/edge-inference-release-gate). Practices the stated data or mathematical operation; it does not implement this paper-specific stage in full.
- Rank Multi-Seed Motion Trajectories — unreviewed idea; contract and evaluator required.

## Implement the components

Each execution-flow node links the matching runnable component or names its planned problem. Planned titles are not runnable; labels distinguish reviewed drafts from unreviewed ideas.

- **Supporting prerequisite:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points).
- **Supporting prerequisite:** [Gate an Edge Model with Accuracy and Latency](/problems/edge-inference-release-gate).

**Planned component problems:**

- Batch Forward-Kinematics Queries — unreviewed idea; contract and evaluator required.
- Compute a Signed-Distance Collision Cost — unreviewed idea; contract and evaluator required.
- Rank Multi-Seed Motion Trajectories — unreviewed idea; contract and evaluator required.

These bounded exercises do not claim to reproduce the complete paper or its benchmark results.

## Why this matters on a robot

Parallel seeds can make difficult manipulation planning practical. Simplified collision spheres, stale obstacles, and missed thin geometry can invalidate an otherwise smooth path.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2310.17274) · [Open-access manuscript](https://arxiv.org/pdf/2310.17274)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
