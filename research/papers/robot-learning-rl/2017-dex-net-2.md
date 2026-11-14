---
schema_version: 1
paper_id: "2017-dex-net-2"
title: "Dex-Net 2.0: Deep Learning to Plan Robust Grasps with Synthetic Point Clouds and Analytic Grasp Metrics"
authors: ["Mahler, Jeffrey","Liang, Jacky","Niyaz, Sherdil","Laskey, Michael","Doan, Richard","Liu, Xinyu","Ojea, Juan Aparicio","Goldberg, Ken"]
year: 2017
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/1703.09312"
pdf_url: "https://arxiv.org/pdf/1703.09312"
local_pdf: "./2017-dex-net-2.pdf"
sha256: "d61ceb68e54cf8496eed5c8bb76b783b59774d8a4e5ee914ff8db60f1f85f1a3"
bytes: 8096768
pages: 12
topics: ["robot-learning-rl","dex-net-2"]
modalities: ["robot-state","rgb","actions","rewards"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
---

# Dex-Net 2.0: Deep Learning to Plan Robust Grasps with Synthetic Point Clouds and Analytic Grasp Metrics

## Agent brief

Learn grasp quality from synthetic depth observations and analytic grasp labels. This acquisition card verifies the primary paper identity and local PDF, and proposes components that can become independently testable Joint Tonic problems. Full-text technical review is required before promoting an idea into a reviewed problem blueprint.

## Contribution

Learn grasp quality from synthetic depth observations and analytic grasp labels.

The proposed exercises below are original teaching decompositions. They do not assert a full reproduction of the paper or any published performance number.

## Prerequisite concepts

- Behavior cloning, Bellman targets, stochastic optimization, episode termination, and rollout evaluation.

## Method map

| Component candidate | Input | Output | Core invariant | Good exercise boundary |
|---|---|---|---|---|
| Extract a Grasp-Aligned Depth Patch | Batched transitions or trajectories with observations, actions, rewards, and termination masks | Training targets, loss components, action candidates, or evaluation summaries | Check terminal-versus-truncated semantics, tensor broadcasting, seeded sampling, finite gradients, and per-episode aggregation. | One bounded function or validation stage |
| Rank Grasp Candidates by Predicted Quality | Batched transitions or trajectories with observations, actions, rewards, and termination masks | Training targets, loss components, action candidates, or evaluation summaries | Check terminal-versus-truncated semantics, tensor broadcasting, seeded sampling, finite gradients, and per-episode aggregation. | One bounded function or validation stage |
| Evaluate Grasp Precision Under a Safety Threshold | Batched transitions or trajectories with observations, actions, rewards, and termination masks | Training targets, loss components, action candidates, or evaluation summaries | Check terminal-versus-truncated semantics, tensor broadcasting, seeded sampling, finite gradients, and per-episode aggregation. | One bounded function or validation stage |

## Data and evaluation

A small teaching implementation should use synthetic or separately licensed fixtures. Check terminal-versus-truncated semantics, tensor broadcasting, seeded sampling, finite gradients, and per-episode aggregation. Dataset names, exact protocol details, published metrics, and hardware requirements must be checked in the source PDF during full-text review; they are not inferred from an awesome-list entry. Keep educational component tests distinct from the paper's end-to-end evaluation.

## Limitations and failure modes

- This is a concise acquisition card, not a full-text technical review. Confirm equations, architecture details, and paper-stated limitations in the PDF before authoring theory.
- Passing synthetic component tests does not establish real-robot performance, robustness, or safe deployment.
- Keep replay/data versions, training seeds, policy versions, interventions, and simulator/robot configuration in one lineage record; compare offline losses with rollout outcomes.
- The paper, linked code, datasets, assets, and weights may carry different license conditions.

## Implementation decomposition

1. Extract a Grasp-Aligned Depth Patch.
2. Rank Grasp Candidates by Predicted Quality.
3. Evaluate Grasp Precision Under a Safety Threshold.
4. Integrate the components on a small fixed fixture and record all deviations from the paper.
5. Add failure slices and a reproducible artifact report.

## Problem blueprints

### Problem: Extract a Grasp-Aligned Depth Patch

- **Type:** component
- **Difficulty:** medium
- **Learning objective:** Implement and explain the extract a grasp-aligned depth patch component.
- **Inputs:** Batched transitions or trajectories with observations, actions, rewards, and termination masks; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Training targets, loss components, action candidates, or evaluation summaries; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check terminal-versus-truncated semantics, tensor broadcasting, seeded sampling, finite gradients, and per-episode aggregation. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Rank Grasp Candidates by Predicted Quality

- **Type:** component
- **Difficulty:** hard
- **Learning objective:** Implement and explain the rank grasp candidates by predicted quality component.
- **Inputs:** Batched transitions or trajectories with observations, actions, rewards, and termination masks; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Training targets, loss components, action candidates, or evaluation summaries; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check terminal-versus-truncated semantics, tensor broadcasting, seeded sampling, finite gradients, and per-episode aggregation. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Evaluate Grasp Precision Under a Safety Threshold

- **Type:** pipeline
- **Difficulty:** hard
- **Learning objective:** Implement and explain the evaluate grasp precision under a safety threshold component.
- **Inputs:** Batched transitions or trajectories with observations, actions, rewards, and termination masks; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Training targets, loss components, action candidates, or evaluation summaries; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check terminal-versus-truncated semantics, tensor broadcasting, seeded sampling, finite gradients, and per-episode aggregation. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

## Visual teaching plan

- Display candidate gripper poses over a depth crop with quality scores.
- Provide labeled axes, units, coordinate frames, and an equivalent table/text view. Use discrete steps when reduced motion is requested.
- Author diagrams independently; do not copy paper figures or captions.

## MLOps and deployment extensions

- Keep replay/data versions, training seeds, policy versions, interventions, and simulator/robot configuration in one lineage record; compare offline losses with rollout outcomes.
- Store paper ID, fixture hash, evaluator version, dependency lock, runtime digest, seed, and resource class with every result.
- Use structured failure reasons and per-slice metrics to distinguish implementation mistakes, distribution shifts, and infrastructure failures.

## Canonical sources

- [Primary arXiv record](https://arxiv.org/abs/1703.09312)
- [Open-access author manuscript](https://arxiv.org/pdf/1703.09312)

Identity metadata was read from the primary arXiv record. Local file signature, byte count, page parsing, and SHA-256 were verified on acquisition.

