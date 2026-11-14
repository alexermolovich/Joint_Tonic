---
schema_version: 1
paper_id: "2023-eureka"
title: "Eureka: Human-Level Reward Design via Coding Large Language Models"
authors: ["Ma, Yecheng Jason","Liang, William","Wang, Guanzhi","Huang, De-An","Bastani, Osbert","Jayaraman, Dinesh","Zhu, Yuke","Fan, Linxi","Anandkumar, Anima"]
year: 2023
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2310.12931"
pdf_url: "https://arxiv.org/pdf/2310.12931"
local_pdf: "./2023-eureka.pdf"
sha256: "aa3b6350a92e4e8b1d894d0879d0af72df2fe76b3fe5d9341151924cb5884f74"
bytes: 3896844
pages: 45
topics: ["robot-learning-rl","eureka"]
modalities: ["robot-state","rgb","actions","rewards"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
---

# Eureka: Human-Level Reward Design via Coding Large Language Models

## Agent brief

Use generated reward programs and iterative feedback to improve reinforcement-learning task specification. This acquisition card verifies the primary paper identity and local PDF, and proposes components that can become independently testable Joint Tonic problems. Full-text technical review is required before promoting an idea into a reviewed problem blueprint.

## Contribution

Use generated reward programs and iterative feedback to improve reinforcement-learning task specification.

The proposed exercises below are original teaching decompositions. They do not assert a full reproduction of the paper or any published performance number.

## Prerequisite concepts

- Behavior cloning, Bellman targets, stochastic optimization, episode termination, and rollout evaluation.

## Method map

| Component candidate | Input | Output | Core invariant | Good exercise boundary |
|---|---|---|---|---|
| Validate a Reward Function Contract | Batched transitions or trajectories with observations, actions, rewards, and termination masks | Training targets, loss components, action candidates, or evaluation summaries | Check terminal-versus-truncated semantics, tensor broadcasting, seeded sampling, finite gradients, and per-episode aggregation. | One bounded function or validation stage |
| Aggregate Reward-Component Diagnostics | Batched transitions or trajectories with observations, actions, rewards, and termination masks | Training targets, loss components, action candidates, or evaluation summaries | Check terminal-versus-truncated semantics, tensor broadcasting, seeded sampling, finite gradients, and per-episode aggregation. | One bounded function or validation stage |
| Rank Reward Candidates by Rollout Evidence | Batched transitions or trajectories with observations, actions, rewards, and termination masks | Training targets, loss components, action candidates, or evaluation summaries | Check terminal-versus-truncated semantics, tensor broadcasting, seeded sampling, finite gradients, and per-episode aggregation. | One bounded function or validation stage |

## Data and evaluation

A small teaching implementation should use synthetic or separately licensed fixtures. Check terminal-versus-truncated semantics, tensor broadcasting, seeded sampling, finite gradients, and per-episode aggregation. Dataset names, exact protocol details, published metrics, and hardware requirements must be checked in the source PDF during full-text review; they are not inferred from an awesome-list entry. Keep educational component tests distinct from the paper's end-to-end evaluation.

## Limitations and failure modes

- This is a concise acquisition card, not a full-text technical review. Confirm equations, architecture details, and paper-stated limitations in the PDF before authoring theory.
- Passing synthetic component tests does not establish real-robot performance, robustness, or safe deployment.
- Keep replay/data versions, training seeds, policy versions, interventions, and simulator/robot configuration in one lineage record; compare offline losses with rollout outcomes.
- The paper, linked code, datasets, assets, and weights may carry different license conditions.

## Implementation decomposition

1. Validate a Reward Function Contract.
2. Aggregate Reward-Component Diagnostics.
3. Rank Reward Candidates by Rollout Evidence.
4. Integrate the components on a small fixed fixture and record all deviations from the paper.
5. Add failure slices and a reproducible artifact report.

## Problem blueprints

### Problem: Validate a Reward Function Contract

- **Type:** component
- **Difficulty:** medium
- **Learning objective:** Implement and explain the validate a reward function contract component.
- **Inputs:** Batched transitions or trajectories with observations, actions, rewards, and termination masks; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Training targets, loss components, action candidates, or evaluation summaries; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check terminal-versus-truncated semantics, tensor broadcasting, seeded sampling, finite gradients, and per-episode aggregation. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Aggregate Reward-Component Diagnostics

- **Type:** component
- **Difficulty:** hard
- **Learning objective:** Implement and explain the aggregate reward-component diagnostics component.
- **Inputs:** Batched transitions or trajectories with observations, actions, rewards, and termination masks; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Training targets, loss components, action candidates, or evaluation summaries; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check terminal-versus-truncated semantics, tensor broadcasting, seeded sampling, finite gradients, and per-episode aggregation. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Rank Reward Candidates by Rollout Evidence

- **Type:** pipeline
- **Difficulty:** hard
- **Learning objective:** Implement and explain the rank reward candidates by rollout evidence component.
- **Inputs:** Batched transitions or trajectories with observations, actions, rewards, and termination masks; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Training targets, loss components, action candidates, or evaluation summaries; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check terminal-versus-truncated semantics, tensor broadcasting, seeded sampling, finite gradients, and per-episode aggregation. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

## Visual teaching plan

- Plot reward components and task success across candidate iterations.
- Provide labeled axes, units, coordinate frames, and an equivalent table/text view. Use discrete steps when reduced motion is requested.
- Author diagrams independently; do not copy paper figures or captions.

## MLOps and deployment extensions

- Keep replay/data versions, training seeds, policy versions, interventions, and simulator/robot configuration in one lineage record; compare offline losses with rollout outcomes.
- Store paper ID, fixture hash, evaluator version, dependency lock, runtime digest, seed, and resource class with every result.
- Use structured failure reasons and per-slice metrics to distinguish implementation mistakes, distribution shifts, and infrastructure failures.

## Canonical sources

- [Primary arXiv record](https://arxiv.org/abs/2310.12931)
- [Open-access author manuscript](https://arxiv.org/pdf/2310.12931)

Identity metadata was read from the primary arXiv record. Local file signature, byte count, page parsing, and SHA-256 were verified on acquisition.

