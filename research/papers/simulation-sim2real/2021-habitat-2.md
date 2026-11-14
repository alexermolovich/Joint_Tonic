---
schema_version: 1
paper_id: "2021-habitat-2"
title: "Habitat 2.0: Training Home Assistants to Rearrange their Habitat"
authors: ["Szot, Andrew","Clegg, Alex","Undersander, Eric","Wijmans, Erik","Zhao, Yili","Turner, John","Maestre, Noah","Mukadam, Mustafa","Chaplot, Devendra","Maksymets, Oleksandr","Gokaslan, Aaron","Vondrus, Vladimir","Dharur, Sameer","Meier, Franziska","Galuba, Wojciech","Chang, Angel","Kira, Zsolt","Koltun, Vladlen","Malik, Jitendra","Savva, Manolis","Batra, Dhruv"]
year: 2021
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2106.14405"
pdf_url: "https://arxiv.org/pdf/2106.14405"
local_pdf: "./2021-habitat-2.pdf"
sha256: "92f9c30479fe4203f656c218fa228c7e5fd71f23a9821b3afa47e06dbe5ab317"
bytes: 45408472
pages: 32
topics: ["simulation-sim2real","habitat-2"]
modalities: ["simulator-state","robot-actions","sensor-observations"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
---

# Habitat 2.0: Training Home Assistants to Rearrange their Habitat

## Agent brief

Study interactive rearrangement simulation with task, physics, and performance interfaces. This acquisition card verifies the primary paper identity and local PDF, and proposes components that can become independently testable Joint Tonic problems. Full-text technical review is required before promoting an idea into a reviewed problem blueprint.

## Contribution

Study interactive rearrangement simulation with task, physics, and performance interfaces.

The proposed exercises below are original teaching decompositions. They do not assert a full reproduction of the paper or any published performance number.

## Prerequisite concepts

- Rigid-body state, episode reset/termination, simulation timesteps, observation schemas, and reproducible benchmarking.

## Method map

| Component candidate | Input | Output | Core invariant | Good exercise boundary |
|---|---|---|---|---|
| Construct a Rearrangement Goal Graph | Seeded scene/task configurations, batched states, actions, and backend capability metadata | Validated transitions, observations, rewards, or simulator benchmark summaries | Check reset determinism, frame/units consistency, batched termination, fixed-step replay, and explicit unsupported capabilities. | One bounded function or validation stage |
| Validate Object Reset States | Seeded scene/task configurations, batched states, actions, and backend capability metadata | Validated transitions, observations, rewards, or simulator benchmark summaries | Check reset determinism, frame/units consistency, batched termination, fixed-step replay, and explicit unsupported capabilities. | One bounded function or validation stage |
| Measure End-to-End Simulation Throughput | Seeded scene/task configurations, batched states, actions, and backend capability metadata | Validated transitions, observations, rewards, or simulator benchmark summaries | Check reset determinism, frame/units consistency, batched termination, fixed-step replay, and explicit unsupported capabilities. | One bounded function or validation stage |

## Data and evaluation

A small teaching implementation should use synthetic or separately licensed fixtures. Check reset determinism, frame/units consistency, batched termination, fixed-step replay, and explicit unsupported capabilities. Dataset names, exact protocol details, published metrics, and hardware requirements must be checked in the source PDF during full-text review; they are not inferred from an awesome-list entry. Keep educational component tests distinct from the paper's end-to-end evaluation.

## Limitations and failure modes

- This is a concise acquisition card, not a full-text technical review. Confirm equations, architecture details, and paper-stated limitations in the PDF before authoring theory.
- Passing synthetic component tests does not establish real-robot performance, robustness, or safe deployment.
- Pin engine version, assets, physics settings, controller rates, and task success predicates; record simulator crashes separately from policy failures.
- The paper, linked code, datasets, assets, and weights may carry different license conditions.

## Implementation decomposition

1. Construct a Rearrangement Goal Graph.
2. Validate Object Reset States.
3. Measure End-to-End Simulation Throughput.
4. Integrate the components on a small fixed fixture and record all deviations from the paper.
5. Add failure slices and a reproducible artifact report.

## Problem blueprints

### Problem: Construct a Rearrangement Goal Graph

- **Type:** component
- **Difficulty:** medium
- **Learning objective:** Implement and explain the construct a rearrangement goal graph component.
- **Inputs:** Seeded scene/task configurations, batched states, actions, and backend capability metadata; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Validated transitions, observations, rewards, or simulator benchmark summaries; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check reset determinism, frame/units consistency, batched termination, fixed-step replay, and explicit unsupported capabilities. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Validate Object Reset States

- **Type:** component
- **Difficulty:** hard
- **Learning objective:** Implement and explain the validate object reset states component.
- **Inputs:** Seeded scene/task configurations, batched states, actions, and backend capability metadata; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Validated transitions, observations, rewards, or simulator benchmark summaries; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check reset determinism, frame/units consistency, batched termination, fixed-step replay, and explicit unsupported capabilities. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Measure End-to-End Simulation Throughput

- **Type:** pipeline
- **Difficulty:** hard
- **Learning objective:** Implement and explain the measure end-to-end simulation throughput component.
- **Inputs:** Seeded scene/task configurations, batched states, actions, and backend capability metadata; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Validated transitions, observations, rewards, or simulator benchmark summaries; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check reset determinism, frame/units consistency, batched termination, fixed-step replay, and explicit unsupported capabilities. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

## Visual teaching plan

- Show object-goal relationships and agent manipulation progress.
- Provide labeled axes, units, coordinate frames, and an equivalent table/text view. Use discrete steps when reduced motion is requested.
- Author diagrams independently; do not copy paper figures or captions.

## MLOps and deployment extensions

- Pin engine version, assets, physics settings, controller rates, and task success predicates; record simulator crashes separately from policy failures.
- Store paper ID, fixture hash, evaluator version, dependency lock, runtime digest, seed, and resource class with every result.
- Use structured failure reasons and per-slice metrics to distinguish implementation mistakes, distribution shifts, and infrastructure failures.

## Canonical sources

- [Primary arXiv record](https://arxiv.org/abs/2106.14405)
- [Open-access author manuscript](https://arxiv.org/pdf/2106.14405)

Identity metadata was read from the primary arXiv record. Local file signature, byte count, page parsing, and SHA-256 were verified on acquisition.

