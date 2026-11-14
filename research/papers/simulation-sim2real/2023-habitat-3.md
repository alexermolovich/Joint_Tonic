---
schema_version: 1
paper_id: "2023-habitat-3"
title: "Habitat 3.0: A Co-Habitat for Humans, Avatars and Robots"
authors: ["Puig, Xavier","Undersander, Eric","Szot, Andrew","Cote, Mikael Dallaire","Yang, Tsung-Yen","Partsey, Ruslan","Desai, Ruta","Clegg, Alexander William","Hlavac, Michal","Min, So Yeon","Vondruš, Vladimír","Gervet, Theophile","Berges, Vincent-Pierre","Turner, John M.","Maksymets, Oleksandr","Kira, Zsolt","Kalakrishnan, Mrinal","Malik, Jitendra","Chaplot, Devendra Singh","Jain, Unnat","Batra, Dhruv","Rai, Akshara","Mottaghi, Roozbeh"]
year: 2023
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2310.13724"
pdf_url: "https://arxiv.org/pdf/2310.13724"
local_pdf: "./2023-habitat-3.pdf"
sha256: "6383018901acbf7677050585da9a30707437cf7119def797be500f33a68021af"
bytes: 8852187
pages: 30
topics: ["simulation-sim2real","habitat-3"]
modalities: ["simulator-state","robot-actions","sensor-observations"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
---

# Habitat 3.0: A Co-Habitat for Humans, Avatars and Robots

## Agent brief

Study human-robot interaction simulation through multi-agent state and evaluation contracts. This acquisition card verifies the primary paper identity and local PDF, and proposes components that can become independently testable Joint Tonic problems. Full-text technical review is required before promoting an idea into a reviewed problem blueprint.

## Contribution

Study human-robot interaction simulation through multi-agent state and evaluation contracts.

The proposed exercises below are original teaching decompositions. They do not assert a full reproduction of the paper or any published performance number.

## Prerequisite concepts

- Rigid-body state, episode reset/termination, simulation timesteps, observation schemas, and reproducible benchmarking.

## Method map

| Component candidate | Input | Output | Core invariant | Good exercise boundary |
|---|---|---|---|---|
| Synchronize Human and Robot Agent States | Seeded scene/task configurations, batched states, actions, and backend capability metadata | Validated transitions, observations, rewards, or simulator benchmark summaries | Check reset determinism, frame/units consistency, batched termination, fixed-step replay, and explicit unsupported capabilities. | One bounded function or validation stage |
| Measure Human-Robot Proximity Events | Seeded scene/task configurations, batched states, actions, and backend capability metadata | Validated transitions, observations, rewards, or simulator benchmark summaries | Check reset determinism, frame/units consistency, batched termination, fixed-step replay, and explicit unsupported capabilities. | One bounded function or validation stage |
| Evaluate a Cooperative Interaction Episode | Seeded scene/task configurations, batched states, actions, and backend capability metadata | Validated transitions, observations, rewards, or simulator benchmark summaries | Check reset determinism, frame/units consistency, batched termination, fixed-step replay, and explicit unsupported capabilities. | One bounded function or validation stage |

## Data and evaluation

A small teaching implementation should use synthetic or separately licensed fixtures. Check reset determinism, frame/units consistency, batched termination, fixed-step replay, and explicit unsupported capabilities. Dataset names, exact protocol details, published metrics, and hardware requirements must be checked in the source PDF during full-text review; they are not inferred from an awesome-list entry. Keep educational component tests distinct from the paper's end-to-end evaluation.

## Limitations and failure modes

- This is a concise acquisition card, not a full-text technical review. Confirm equations, architecture details, and paper-stated limitations in the PDF before authoring theory.
- Passing synthetic component tests does not establish real-robot performance, robustness, or safe deployment.
- Pin engine version, assets, physics settings, controller rates, and task success predicates; record simulator crashes separately from policy failures.
- The paper, linked code, datasets, assets, and weights may carry different license conditions.

## Implementation decomposition

1. Synchronize Human and Robot Agent States.
2. Measure Human-Robot Proximity Events.
3. Evaluate a Cooperative Interaction Episode.
4. Integrate the components on a small fixed fixture and record all deviations from the paper.
5. Add failure slices and a reproducible artifact report.

## Problem blueprints

### Problem: Synchronize Human and Robot Agent States

- **Type:** component
- **Difficulty:** medium
- **Learning objective:** Implement and explain the synchronize human and robot agent states component.
- **Inputs:** Seeded scene/task configurations, batched states, actions, and backend capability metadata; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Validated transitions, observations, rewards, or simulator benchmark summaries; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check reset determinism, frame/units consistency, batched termination, fixed-step replay, and explicit unsupported capabilities. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Measure Human-Robot Proximity Events

- **Type:** component
- **Difficulty:** hard
- **Learning objective:** Implement and explain the measure human-robot proximity events component.
- **Inputs:** Seeded scene/task configurations, batched states, actions, and backend capability metadata; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Validated transitions, observations, rewards, or simulator benchmark summaries; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check reset determinism, frame/units consistency, batched termination, fixed-step replay, and explicit unsupported capabilities. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Evaluate a Cooperative Interaction Episode

- **Type:** pipeline
- **Difficulty:** hard
- **Learning objective:** Implement and explain the evaluate a cooperative interaction episode component.
- **Inputs:** Seeded scene/task configurations, batched states, actions, and backend capability metadata; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Validated transitions, observations, rewards, or simulator benchmark summaries; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check reset determinism, frame/units consistency, batched termination, fixed-step replay, and explicit unsupported capabilities. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

## Visual teaching plan

- Replay two agents with shared task state and proximity overlays.
- Provide labeled axes, units, coordinate frames, and an equivalent table/text view. Use discrete steps when reduced motion is requested.
- Author diagrams independently; do not copy paper figures or captions.

## MLOps and deployment extensions

- Pin engine version, assets, physics settings, controller rates, and task success predicates; record simulator crashes separately from policy failures.
- Store paper ID, fixture hash, evaluator version, dependency lock, runtime digest, seed, and resource class with every result.
- Use structured failure reasons and per-slice metrics to distinguish implementation mistakes, distribution shifts, and infrastructure failures.

## Canonical sources

- [Primary arXiv record](https://arxiv.org/abs/2310.13724)
- [Open-access author manuscript](https://arxiv.org/pdf/2310.13724)

Identity metadata was read from the primary arXiv record. Local file signature, byte count, page parsing, and SHA-256 were verified on acquisition.

