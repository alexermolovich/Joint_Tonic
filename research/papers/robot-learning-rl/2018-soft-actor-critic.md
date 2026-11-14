---
schema_version: 1
paper_id: "2018-soft-actor-critic"
title: "Soft Actor-Critic: Off-Policy Maximum Entropy Deep Reinforcement Learning with a Stochastic Actor"
authors: ["Haarnoja, Tuomas","Zhou, Aurick","Abbeel, Pieter","Levine, Sergey"]
year: 2018
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/1801.01290"
pdf_url: "https://arxiv.org/pdf/1801.01290"
local_pdf: "./2018-soft-actor-critic.pdf"
sha256: "5c33fae017d02f7025730f05198d4a6b103402822c8bbf48cbc5d8a0474c336a"
bytes: 4388102
pages: 14
topics: ["robot-learning-rl","soft-actor-critic"]
modalities: ["robot-state","rgb","actions","rewards"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
---

# Soft Actor-Critic: Off-Policy Maximum Entropy Deep Reinforcement Learning with a Stochastic Actor

## Agent brief

Optimize a stochastic policy with entropy-regularized value learning for continuous control. This acquisition card verifies the primary paper identity and local PDF, and proposes components that can become independently testable Joint Tonic problems. Full-text technical review is required before promoting an idea into a reviewed problem blueprint.

## Contribution

Optimize a stochastic policy with entropy-regularized value learning for continuous control.

The proposed exercises below are original teaching decompositions. They do not assert a full reproduction of the paper or any published performance number.

## Prerequisite concepts

- Behavior cloning, Bellman targets, stochastic optimization, episode termination, and rollout evaluation.

## Method map

| Component candidate | Input | Output | Core invariant | Good exercise boundary |
|---|---|---|---|---|
| Compute an Entropy-Regularized Bellman Target | Batched transitions or trajectories with observations, actions, rewards, and termination masks | Training targets, loss components, action candidates, or evaluation summaries | Check terminal-versus-truncated semantics, tensor broadcasting, seeded sampling, finite gradients, and per-episode aggregation. | One bounded function or validation stage |
| Apply Tanh Action Log-Probability Correction | Batched transitions or trajectories with observations, actions, rewards, and termination masks | Training targets, loss components, action candidates, or evaluation summaries | Check terminal-versus-truncated semantics, tensor broadcasting, seeded sampling, finite gradients, and per-episode aggregation. | One bounded function or validation stage |
| Update a Temperature Objective | Batched transitions or trajectories with observations, actions, rewards, and termination masks | Training targets, loss components, action candidates, or evaluation summaries | Check terminal-versus-truncated semantics, tensor broadcasting, seeded sampling, finite gradients, and per-episode aggregation. | One bounded function or validation stage |

## Data and evaluation

A small teaching implementation should use synthetic or separately licensed fixtures. Check terminal-versus-truncated semantics, tensor broadcasting, seeded sampling, finite gradients, and per-episode aggregation. Dataset names, exact protocol details, published metrics, and hardware requirements must be checked in the source PDF during full-text review; they are not inferred from an awesome-list entry. Keep educational component tests distinct from the paper's end-to-end evaluation.

## Limitations and failure modes

- This is a concise acquisition card, not a full-text technical review. Confirm equations, architecture details, and paper-stated limitations in the PDF before authoring theory.
- Passing synthetic component tests does not establish real-robot performance, robustness, or safe deployment.
- Keep replay/data versions, training seeds, policy versions, interventions, and simulator/robot configuration in one lineage record; compare offline losses with rollout outcomes.
- The paper, linked code, datasets, assets, and weights may carry different license conditions.

## Implementation decomposition

1. Compute an Entropy-Regularized Bellman Target.
2. Apply Tanh Action Log-Probability Correction.
3. Update a Temperature Objective.
4. Integrate the components on a small fixed fixture and record all deviations from the paper.
5. Add failure slices and a reproducible artifact report.

## Problem blueprints

### Problem: Compute an Entropy-Regularized Bellman Target

- **Type:** component
- **Difficulty:** medium
- **Learning objective:** Implement and explain the compute an entropy-regularized bellman target component.
- **Inputs:** Batched transitions or trajectories with observations, actions, rewards, and termination masks; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Training targets, loss components, action candidates, or evaluation summaries; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check terminal-versus-truncated semantics, tensor broadcasting, seeded sampling, finite gradients, and per-episode aggregation. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Apply Tanh Action Log-Probability Correction

- **Type:** component
- **Difficulty:** hard
- **Learning objective:** Implement and explain the apply tanh action log-probability correction component.
- **Inputs:** Batched transitions or trajectories with observations, actions, rewards, and termination masks; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Training targets, loss components, action candidates, or evaluation summaries; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check terminal-versus-truncated semantics, tensor broadcasting, seeded sampling, finite gradients, and per-episode aggregation. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Update a Temperature Objective

- **Type:** pipeline
- **Difficulty:** hard
- **Learning objective:** Implement and explain the update a temperature objective component.
- **Inputs:** Batched transitions or trajectories with observations, actions, rewards, and termination masks; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Training targets, loss components, action candidates, or evaluation summaries; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check terminal-versus-truncated semantics, tensor broadcasting, seeded sampling, finite gradients, and per-episode aggregation. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

## Visual teaching plan

- Plot the tradeoff between policy entropy and predicted return.
- Provide labeled axes, units, coordinate frames, and an equivalent table/text view. Use discrete steps when reduced motion is requested.
- Author diagrams independently; do not copy paper figures or captions.

## MLOps and deployment extensions

- Keep replay/data versions, training seeds, policy versions, interventions, and simulator/robot configuration in one lineage record; compare offline losses with rollout outcomes.
- Store paper ID, fixture hash, evaluator version, dependency lock, runtime digest, seed, and resource class with every result.
- Use structured failure reasons and per-slice metrics to distinguish implementation mistakes, distribution shifts, and infrastructure failures.

## Canonical sources

- [Primary arXiv record](https://arxiv.org/abs/1801.01290)
- [Open-access author manuscript](https://arxiv.org/pdf/1801.01290)

Identity metadata was read from the primary arXiv record. Local file signature, byte count, page parsing, and SHA-256 were verified on acquisition.

