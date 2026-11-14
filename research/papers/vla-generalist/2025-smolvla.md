---
schema_version: 1
paper_id: "2025-smolvla"
title: "SmolVLA: A Vision-Language-Action Model for Affordable and Efficient Robotics"
authors: ["Shukor, Mustafa","Aubakirova, Dana","Capuano, Francesco","Kooijmans, Pepijn","Palma, Steven","Zouitine, Adil","Aractingi, Michel","Pascal, Caroline","Russi, Martino","Marafioti, Andres","Alibert, Simon","Cord, Matthieu","Wolf, Thomas","Cadene, Remi"]
year: 2025
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2506.01844"
pdf_url: "https://arxiv.org/pdf/2506.01844"
local_pdf: "./2025-smolvla.pdf"
sha256: "cb1bb9a8f824187fcdc32af8c290214487c524f139a3c2def1c6d97adb1fa40c"
bytes: 8921356
pages: 24
topics: ["vla-generalist","smolvla"]
modalities: ["rgb","text","robot-state","actions"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
---

# SmolVLA: A Vision-Language-Action Model for Affordable and Efficient Robotics

## Agent brief

Study a compact VLA and practical policy inference pipeline for affordable robotics. This acquisition card verifies the primary paper identity and local PDF, and proposes components that can become independently testable Joint Tonic problems. Full-text technical review is required before promoting an idea into a reviewed problem blueprint.

## Contribution

Study a compact VLA and practical policy inference pipeline for affordable robotics.

The proposed exercises below are original teaching decompositions. They do not assert a full reproduction of the paper or any published performance number.

## Prerequisite concepts

- Sequence modeling, action units, control frequencies, multimodal batching, and policy evaluation.

## Method map

| Component candidate | Input | Output | Core invariant | Good exercise boundary |
|---|---|---|---|---|
| Normalize a Compact VLA Observation Batch | Timestamped observations, instruction tokens, action chunks, and embodiment metadata | Policy-ready token sequences, bounded actions, or rollout diagnostics | Check episode boundaries, action limits, reserved tokens, missing modalities, timestamp ordering, and deterministic replay. | One bounded function or validation stage |
| Schedule Asynchronous Policy Chunks | Timestamped observations, instruction tokens, action chunks, and embodiment metadata | Policy-ready token sequences, bounded actions, or rollout diagnostics | Check episode boundaries, action limits, reserved tokens, missing modalities, timestamp ordering, and deterministic replay. | One bounded function or validation stage |
| Measure Stale-Action Latency | Timestamped observations, instruction tokens, action chunks, and embodiment metadata | Policy-ready token sequences, bounded actions, or rollout diagnostics | Check episode boundaries, action limits, reserved tokens, missing modalities, timestamp ordering, and deterministic replay. | One bounded function or validation stage |

## Data and evaluation

A small teaching implementation should use synthetic or separately licensed fixtures. Check episode boundaries, action limits, reserved tokens, missing modalities, timestamp ordering, and deterministic replay. Dataset names, exact protocol details, published metrics, and hardware requirements must be checked in the source PDF during full-text review; they are not inferred from an awesome-list entry. Keep educational component tests distinct from the paper's end-to-end evaluation.

## Limitations and failure modes

- This is a concise acquisition card, not a full-text technical review. Confirm equations, architecture details, and paper-stated limitations in the PDF before authoring theory.
- Passing synthetic component tests does not establish real-robot performance, robustness, or safe deployment.
- Package the action codec and observation schema with checkpoints; measure stale observations, control latency, invalid actions, and task success by embodiment.
- The paper, linked code, datasets, assets, and weights may carry different license conditions.

## Implementation decomposition

1. Normalize a Compact VLA Observation Batch.
2. Schedule Asynchronous Policy Chunks.
3. Measure Stale-Action Latency.
4. Integrate the components on a small fixed fixture and record all deviations from the paper.
5. Add failure slices and a reproducible artifact report.

## Problem blueprints

### Problem: Normalize a Compact VLA Observation Batch

- **Type:** component
- **Difficulty:** medium
- **Learning objective:** Implement and explain the normalize a compact vla observation batch component.
- **Inputs:** Timestamped observations, instruction tokens, action chunks, and embodiment metadata; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Policy-ready token sequences, bounded actions, or rollout diagnostics; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check episode boundaries, action limits, reserved tokens, missing modalities, timestamp ordering, and deterministic replay. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Schedule Asynchronous Policy Chunks

- **Type:** component
- **Difficulty:** hard
- **Learning objective:** Implement and explain the schedule asynchronous policy chunks component.
- **Inputs:** Timestamped observations, instruction tokens, action chunks, and embodiment metadata; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Policy-ready token sequences, bounded actions, or rollout diagnostics; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check episode boundaries, action limits, reserved tokens, missing modalities, timestamp ordering, and deterministic replay. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Measure Stale-Action Latency

- **Type:** pipeline
- **Difficulty:** hard
- **Learning objective:** Implement and explain the measure stale-action latency component.
- **Inputs:** Timestamped observations, instruction tokens, action chunks, and embodiment metadata; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Policy-ready token sequences, bounded actions, or rollout diagnostics; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check episode boundaries, action limits, reserved tokens, missing modalities, timestamp ordering, and deterministic replay. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

## Visual teaching plan

- Animate observation capture, inference, and action execution on one timeline.
- Provide labeled axes, units, coordinate frames, and an equivalent table/text view. Use discrete steps when reduced motion is requested.
- Author diagrams independently; do not copy paper figures or captions.

## MLOps and deployment extensions

- Package the action codec and observation schema with checkpoints; measure stale observations, control latency, invalid actions, and task success by embodiment.
- Store paper ID, fixture hash, evaluator version, dependency lock, runtime digest, seed, and resource class with every result.
- Use structured failure reasons and per-slice metrics to distinguish implementation mistakes, distribution shifts, and infrastructure failures.

## Canonical sources

- [Primary arXiv record](https://arxiv.org/abs/2506.01844)
- [Open-access author manuscript](https://arxiv.org/pdf/2506.01844)

Identity metadata was read from the primary arXiv record. Local file signature, byte count, page parsing, and SHA-256 were verified on acquisition.

