---
schema_version: 1
paper_id: "2020-transporter-networks"
title: "Transporter Networks: Rearranging the Visual World for Robotic Manipulation"
authors: ["Zeng, Andy","Florence, Pete","Tompson, Jonathan","Welker, Stefan","Chien, Jonathan","Attarian, Maria","Armstrong, Travis","Krasin, Ivan","Duong, Dan","Wahid, Ayzaan","Sindhwani, Vikas","Lee, Johnny"]
year: 2020
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2010.14406"
pdf_url: "https://arxiv.org/pdf/2010.14406"
local_pdf: "./2020-transporter-networks.pdf"
sha256: "3a5e78b5c8881863845c46bda0bf8c9071aa79a59a6f9a9f4d8732690482b228"
bytes: 3781112
pages: 23
topics: ["robot-learning-rl","transporter-networks"]
modalities: ["robot-state","rgb","actions","rewards"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
---

# Transporter Networks: Rearranging the Visual World for Robotic Manipulation

## Agent brief

Use spatially structured visual features and cross-correlation to predict pick-and-place actions. This acquisition card verifies the primary paper identity and local PDF, and proposes components that can become independently testable Joint Tonic problems. Full-text technical review is required before promoting an idea into a reviewed problem blueprint.

## Contribution

Use spatially structured visual features and cross-correlation to predict pick-and-place actions.

The proposed exercises below are original teaching decompositions. They do not assert a full reproduction of the paper or any published performance number.

## Prerequisite concepts

- Behavior cloning, Bellman targets, stochastic optimization, episode termination, and rollout evaluation.

## Method map

| Component candidate | Input | Output | Core invariant | Good exercise boundary |
|---|---|---|---|---|
| Build a Pick Heatmap | Batched transitions or trajectories with observations, actions, rewards, and termination masks | Training targets, loss components, action candidates, or evaluation summaries | Check terminal-versus-truncated semantics, tensor broadcasting, seeded sampling, finite gradients, and per-episode aggregation. | One bounded function or validation stage |
| Correlate a Pick Feature Crop with a Place Map | Batched transitions or trajectories with observations, actions, rewards, and termination masks | Training targets, loss components, action candidates, or evaluation summaries | Check terminal-versus-truncated semantics, tensor broadcasting, seeded sampling, finite gradients, and per-episode aggregation. | One bounded function or validation stage |
| Decode a Spatial Action Distribution | Batched transitions or trajectories with observations, actions, rewards, and termination masks | Training targets, loss components, action candidates, or evaluation summaries | Check terminal-versus-truncated semantics, tensor broadcasting, seeded sampling, finite gradients, and per-episode aggregation. | One bounded function or validation stage |

## Data and evaluation

A small teaching implementation should use synthetic or separately licensed fixtures. Check terminal-versus-truncated semantics, tensor broadcasting, seeded sampling, finite gradients, and per-episode aggregation. Dataset names, exact protocol details, published metrics, and hardware requirements must be checked in the source PDF during full-text review; they are not inferred from an awesome-list entry. Keep educational component tests distinct from the paper's end-to-end evaluation.

## Limitations and failure modes

- This is a concise acquisition card, not a full-text technical review. Confirm equations, architecture details, and paper-stated limitations in the PDF before authoring theory.
- Passing synthetic component tests does not establish real-robot performance, robustness, or safe deployment.
- Keep replay/data versions, training seeds, policy versions, interventions, and simulator/robot configuration in one lineage record; compare offline losses with rollout outcomes.
- The paper, linked code, datasets, assets, and weights may carry different license conditions.

## Implementation decomposition

1. Build a Pick Heatmap.
2. Correlate a Pick Feature Crop with a Place Map.
3. Decode a Spatial Action Distribution.
4. Integrate the components on a small fixed fixture and record all deviations from the paper.
5. Add failure slices and a reproducible artifact report.

## Problem blueprints

### Problem: Build a Pick Heatmap

- **Type:** component
- **Difficulty:** medium
- **Learning objective:** Implement and explain the build a pick heatmap component.
- **Inputs:** Batched transitions or trajectories with observations, actions, rewards, and termination masks; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Training targets, loss components, action candidates, or evaluation summaries; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check terminal-versus-truncated semantics, tensor broadcasting, seeded sampling, finite gradients, and per-episode aggregation. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Correlate a Pick Feature Crop with a Place Map

- **Type:** component
- **Difficulty:** hard
- **Learning objective:** Implement and explain the correlate a pick feature crop with a place map component.
- **Inputs:** Batched transitions or trajectories with observations, actions, rewards, and termination masks; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Training targets, loss components, action candidates, or evaluation summaries; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check terminal-versus-truncated semantics, tensor broadcasting, seeded sampling, finite gradients, and per-episode aggregation. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Decode a Spatial Action Distribution

- **Type:** pipeline
- **Difficulty:** hard
- **Learning objective:** Implement and explain the decode a spatial action distribution component.
- **Inputs:** Batched transitions or trajectories with observations, actions, rewards, and termination masks; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Training targets, loss components, action candidates, or evaluation summaries; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check terminal-versus-truncated semantics, tensor broadcasting, seeded sampling, finite gradients, and per-episode aggregation. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

## Visual teaching plan

- Move a pick crop over a feature map and visualize placement correlation.
- Provide labeled axes, units, coordinate frames, and an equivalent table/text view. Use discrete steps when reduced motion is requested.
- Author diagrams independently; do not copy paper figures or captions.

## MLOps and deployment extensions

- Keep replay/data versions, training seeds, policy versions, interventions, and simulator/robot configuration in one lineage record; compare offline losses with rollout outcomes.
- Store paper ID, fixture hash, evaluator version, dependency lock, runtime digest, seed, and resource class with every result.
- Use structured failure reasons and per-slice metrics to distinguish implementation mistakes, distribution shifts, and infrastructure failures.

## Canonical sources

- [Primary arXiv record](https://arxiv.org/abs/2010.14406)
- [Open-access author manuscript](https://arxiv.org/pdf/2010.14406)

Identity metadata was read from the primary arXiv record. Local file signature, byte count, page parsing, and SHA-256 were verified on acquisition.

