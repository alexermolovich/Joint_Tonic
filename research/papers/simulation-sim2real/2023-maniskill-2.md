---
schema_version: 1
paper_id: "2023-maniskill-2"
title: "ManiSkill2: A Unified Benchmark for Generalizable Manipulation Skills"
authors: ["Gu, Jiayuan","Xiang, Fanbo","Li, Xuanlin","Ling, Zhan","Liu, Xiqiang","Mu, Tongzhou","Tang, Yihe","Tao, Stone","Wei, Xinyue","Yao, Yunchao","Yuan, Xiaodi","Xie, Pengwei","Huang, Zhiao","Chen, Rui","Su, Hao"]
year: 2023
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2302.04659"
pdf_url: "https://arxiv.org/pdf/2302.04659"
local_pdf: "./2023-maniskill-2.pdf"
sha256: "89fb794345d860ee696ca2f4d7a75059b15352b615794eeadb0e6075426136f0"
bytes: 7635048
pages: 30
topics: ["simulation-sim2real","maniskill-2"]
modalities: ["simulator-state","robot-actions","sensor-observations"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
---

# ManiSkill2: A Unified Benchmark for Generalizable Manipulation Skills

## Agent brief

Study a manipulation benchmark with broader task and object interfaces. This acquisition card verifies the primary paper identity and local PDF, and proposes components that can become independently testable Joint Tonic problems. Full-text technical review is required before promoting an idea into a reviewed problem blueprint.

## Contribution

Study a manipulation benchmark with broader task and object interfaces.

The proposed exercises below are original teaching decompositions. They do not assert a full reproduction of the paper or any published performance number.

## Prerequisite concepts

- Rigid-body state, episode reset/termination, simulation timesteps, observation schemas, and reproducible benchmarking.

## Method map

| Component candidate | Input | Output | Core invariant | Good exercise boundary |
|---|---|---|---|---|
| Build a Vectorized Manipulation Batch | Seeded scene/task configurations, batched states, actions, and backend capability metadata | Validated transitions, observations, rewards, or simulator benchmark summaries | Check reset determinism, frame/units consistency, batched termination, fixed-step replay, and explicit unsupported capabilities. | One bounded function or validation stage |
| Validate Task-Specific Success Predicates | Seeded scene/task configurations, batched states, actions, and backend capability metadata | Validated transitions, observations, rewards, or simulator benchmark summaries | Check reset determinism, frame/units consistency, batched termination, fixed-step replay, and explicit unsupported capabilities. | One bounded function or validation stage |
| Report Generalization by Object Split | Seeded scene/task configurations, batched states, actions, and backend capability metadata | Validated transitions, observations, rewards, or simulator benchmark summaries | Check reset determinism, frame/units consistency, batched termination, fixed-step replay, and explicit unsupported capabilities. | One bounded function or validation stage |

## Data and evaluation

A small teaching implementation should use synthetic or separately licensed fixtures. Check reset determinism, frame/units consistency, batched termination, fixed-step replay, and explicit unsupported capabilities. Dataset names, exact protocol details, published metrics, and hardware requirements must be checked in the source PDF during full-text review; they are not inferred from an awesome-list entry. Keep educational component tests distinct from the paper's end-to-end evaluation.

## Limitations and failure modes

- This is a concise acquisition card, not a full-text technical review. Confirm equations, architecture details, and paper-stated limitations in the PDF before authoring theory.
- Passing synthetic component tests does not establish real-robot performance, robustness, or safe deployment.
- Pin engine version, assets, physics settings, controller rates, and task success predicates; record simulator crashes separately from policy failures.
- The paper, linked code, datasets, assets, and weights may carry different license conditions.

## Implementation decomposition

1. Build a Vectorized Manipulation Batch.
2. Validate Task-Specific Success Predicates.
3. Report Generalization by Object Split.
4. Integrate the components on a small fixed fixture and record all deviations from the paper.
5. Add failure slices and a reproducible artifact report.

## Problem blueprints

### Problem: Build a Vectorized Manipulation Batch

- **Type:** component
- **Difficulty:** medium
- **Learning objective:** Implement and explain the build a vectorized manipulation batch component.
- **Inputs:** Seeded scene/task configurations, batched states, actions, and backend capability metadata; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Validated transitions, observations, rewards, or simulator benchmark summaries; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check reset determinism, frame/units consistency, batched termination, fixed-step replay, and explicit unsupported capabilities. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Validate Task-Specific Success Predicates

- **Type:** component
- **Difficulty:** hard
- **Learning objective:** Implement and explain the validate task-specific success predicates component.
- **Inputs:** Seeded scene/task configurations, batched states, actions, and backend capability metadata; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Validated transitions, observations, rewards, or simulator benchmark summaries; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check reset determinism, frame/units consistency, batched termination, fixed-step replay, and explicit unsupported capabilities. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Report Generalization by Object Split

- **Type:** pipeline
- **Difficulty:** hard
- **Learning objective:** Implement and explain the report generalization by object split component.
- **Inputs:** Seeded scene/task configurations, batched states, actions, and backend capability metadata; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Validated transitions, observations, rewards, or simulator benchmark summaries; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check reset determinism, frame/units consistency, batched termination, fixed-step replay, and explicit unsupported capabilities. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

## Visual teaching plan

- Display task families, object instances, and success criteria.
- Provide labeled axes, units, coordinate frames, and an equivalent table/text view. Use discrete steps when reduced motion is requested.
- Author diagrams independently; do not copy paper figures or captions.

## MLOps and deployment extensions

- Pin engine version, assets, physics settings, controller rates, and task success predicates; record simulator crashes separately from policy failures.
- Store paper ID, fixture hash, evaluator version, dependency lock, runtime digest, seed, and resource class with every result.
- Use structured failure reasons and per-slice metrics to distinguish implementation mistakes, distribution shifts, and infrastructure failures.

## Canonical sources

- [Primary arXiv record](https://arxiv.org/abs/2302.04659)
- [Open-access author manuscript](https://arxiv.org/pdf/2302.04659)

Identity metadata was read from the primary arXiv record. Local file signature, byte count, page parsing, and SHA-256 were verified on acquisition.

