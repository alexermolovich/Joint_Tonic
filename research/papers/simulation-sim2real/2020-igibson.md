---
schema_version: 1
paper_id: "2020-igibson"
title: "iGibson 1.0: a Simulation Environment for Interactive Tasks in Large Realistic Scenes"
authors: ["Shen, Bokui","Xia, Fei","Li, Chengshu","Martín-Martín, Roberto","Fan, Linxi","Wang, Guanzhi","Pérez-D'Arpino, Claudia","Buch, Shyamal","Srivastava, Sanjana","Tchapmi, Lyne P.","Tchapmi, Micael E.","Vainio, Kent","Wong, Josiah","Fei-Fei, Li","Savarese, Silvio"]
year: 2020
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2012.02924"
pdf_url: "https://arxiv.org/pdf/2012.02924"
local_pdf: "./2020-igibson.pdf"
sha256: "6b6840463b960afe2f2a095470a90029ff41f0cc26f4717509cb67a1d424d61c"
bytes: 4704504
pages: 11
topics: ["simulation-sim2real","igibson"]
modalities: ["simulator-state","robot-actions","sensor-observations"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
---

# iGibson 1.0: a Simulation Environment for Interactive Tasks in Large Realistic Scenes

## Agent brief

Study interactive indoor robot simulation through scene, object, and sensor contracts. This acquisition card verifies the primary paper identity and local PDF, and proposes components that can become independently testable Joint Tonic problems. Full-text technical review is required before promoting an idea into a reviewed problem blueprint.

## Contribution

Study interactive indoor robot simulation through scene, object, and sensor contracts.

The proposed exercises below are original teaching decompositions. They do not assert a full reproduction of the paper or any published performance number.

## Prerequisite concepts

- Rigid-body state, episode reset/termination, simulation timesteps, observation schemas, and reproducible benchmarking.

## Method map

| Component candidate | Input | Output | Core invariant | Good exercise boundary |
|---|---|---|---|---|
| Validate a Scene Interaction Graph | Seeded scene/task configurations, batched states, actions, and backend capability metadata | Validated transitions, observations, rewards, or simulator benchmark summaries | Check reset determinism, frame/units consistency, batched termination, fixed-step replay, and explicit unsupported capabilities. | One bounded function or validation stage |
| Replay Sensor Streams from a Fixed Seed | Seeded scene/task configurations, batched states, actions, and backend capability metadata | Validated transitions, observations, rewards, or simulator benchmark summaries | Check reset determinism, frame/units consistency, batched termination, fixed-step replay, and explicit unsupported capabilities. | One bounded function or validation stage |
| Measure Domain Shift Between Simulated Scenes | Seeded scene/task configurations, batched states, actions, and backend capability metadata | Validated transitions, observations, rewards, or simulator benchmark summaries | Check reset determinism, frame/units consistency, batched termination, fixed-step replay, and explicit unsupported capabilities. | One bounded function or validation stage |

## Data and evaluation

A small teaching implementation should use synthetic or separately licensed fixtures. Check reset determinism, frame/units consistency, batched termination, fixed-step replay, and explicit unsupported capabilities. Dataset names, exact protocol details, published metrics, and hardware requirements must be checked in the source PDF during full-text review; they are not inferred from an awesome-list entry. Keep educational component tests distinct from the paper's end-to-end evaluation.

## Limitations and failure modes

- This is a concise acquisition card, not a full-text technical review. Confirm equations, architecture details, and paper-stated limitations in the PDF before authoring theory.
- Passing synthetic component tests does not establish real-robot performance, robustness, or safe deployment.
- Pin engine version, assets, physics settings, controller rates, and task success predicates; record simulator crashes separately from policy failures.
- The paper, linked code, datasets, assets, and weights may carry different license conditions.

## Implementation decomposition

1. Validate a Scene Interaction Graph.
2. Replay Sensor Streams from a Fixed Seed.
3. Measure Domain Shift Between Simulated Scenes.
4. Integrate the components on a small fixed fixture and record all deviations from the paper.
5. Add failure slices and a reproducible artifact report.

## Problem blueprints

### Problem: Validate a Scene Interaction Graph

- **Type:** component
- **Difficulty:** medium
- **Learning objective:** Implement and explain the validate a scene interaction graph component.
- **Inputs:** Seeded scene/task configurations, batched states, actions, and backend capability metadata; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Validated transitions, observations, rewards, or simulator benchmark summaries; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check reset determinism, frame/units consistency, batched termination, fixed-step replay, and explicit unsupported capabilities. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Replay Sensor Streams from a Fixed Seed

- **Type:** component
- **Difficulty:** hard
- **Learning objective:** Implement and explain the replay sensor streams from a fixed seed component.
- **Inputs:** Seeded scene/task configurations, batched states, actions, and backend capability metadata; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Validated transitions, observations, rewards, or simulator benchmark summaries; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check reset determinism, frame/units consistency, batched termination, fixed-step replay, and explicit unsupported capabilities. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Measure Domain Shift Between Simulated Scenes

- **Type:** pipeline
- **Difficulty:** hard
- **Learning objective:** Implement and explain the measure domain shift between simulated scenes component.
- **Inputs:** Seeded scene/task configurations, batched states, actions, and backend capability metadata; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Validated transitions, observations, rewards, or simulator benchmark summaries; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check reset determinism, frame/units consistency, batched termination, fixed-step replay, and explicit unsupported capabilities. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

## Visual teaching plan

- Inspect interactive scene objects and their physical parameters.
- Provide labeled axes, units, coordinate frames, and an equivalent table/text view. Use discrete steps when reduced motion is requested.
- Author diagrams independently; do not copy paper figures or captions.

## MLOps and deployment extensions

- Pin engine version, assets, physics settings, controller rates, and task success predicates; record simulator crashes separately from policy failures.
- Store paper ID, fixture hash, evaluator version, dependency lock, runtime digest, seed, and resource class with every result.
- Use structured failure reasons and per-slice metrics to distinguish implementation mistakes, distribution shifts, and infrastructure failures.

## Canonical sources

- [Primary arXiv record](https://arxiv.org/abs/2012.02924)
- [Open-access author manuscript](https://arxiv.org/pdf/2012.02924)

Identity metadata was read from the primary arXiv record. Local file signature, byte count, page parsing, and SHA-256 were verified on acquisition.

