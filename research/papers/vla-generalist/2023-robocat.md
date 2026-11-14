---
schema_version: 1
paper_id: "2023-robocat"
title: "RoboCat: A Self-Improving Generalist Agent for Robotic Manipulation"
authors: ["Bousmalis, Konstantinos","Vezzani, Giulia","Rao, Dushyant","Devin, Coline","Lee, Alex X.","Bauza, Maria","Davchev, Todor","Zhou, Yuxiang","Gupta, Agrim","Raju, Akhil","Laurens, Antoine","Fantacci, Claudio","Dalibard, Valentin","Zambelli, Martina","Martins, Murilo","Pevceviciute, Rugile","Blokzijl, Michiel","Denil, Misha","Batchelor, Nathan","Lampe, Thomas","Parisotto, Emilio","Żołna, Konrad","Reed, Scott","Colmenarejo, Sergio Gómez","Scholz, Jon","Abdolmaleki, Abbas","Groth, Oliver","Regli, Jean-Baptiste","Sushkov, Oleg","Rothörl, Tom","Chen, José Enrique","Aytar, Yusuf","Barker, Dave","Ortiz, Joy","Riedmiller, Martin","Springenberg, Jost Tobias","Hadsell, Raia","Nori, Francesco","Heess, Nicolas"]
year: 2023
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2306.11706"
pdf_url: "https://arxiv.org/pdf/2306.11706"
local_pdf: "./2023-robocat.pdf"
sha256: "ec66c1579baaada787820abf4ce99a9a59143b583ddcc6dfc4814623d1969831"
bytes: 26404959
pages: 60
topics: ["vla-generalist","robocat"]
modalities: ["rgb","text","robot-state","actions"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
---

# RoboCat: A Self-Improving Generalist Agent for Robotic Manipulation

## Agent brief

Study generalist visual robot control through task mixtures and iterative policy adaptation. This acquisition card verifies the primary paper identity and local PDF, and proposes components that can become independently testable Joint Tonic problems. Full-text technical review is required before promoting an idea into a reviewed problem blueprint.

## Contribution

Study generalist visual robot control through task mixtures and iterative policy adaptation.

The proposed exercises below are original teaching decompositions. They do not assert a full reproduction of the paper or any published performance number.

## Prerequisite concepts

- Sequence modeling, action units, control frequencies, multimodal batching, and policy evaluation.

## Method map

| Component candidate | Input | Output | Core invariant | Good exercise boundary |
|---|---|---|---|---|
| Balance Robot-Task Training Mixtures | Timestamped observations, instruction tokens, action chunks, and embodiment metadata | Policy-ready token sequences, bounded actions, or rollout diagnostics | Check episode boundaries, action limits, reserved tokens, missing modalities, timestamp ordering, and deterministic replay. | One bounded function or validation stage |
| Construct Goal-Conditioned Policy Batches | Timestamped observations, instruction tokens, action chunks, and embodiment metadata | Policy-ready token sequences, bounded actions, or rollout diagnostics | Check episode boundaries, action limits, reserved tokens, missing modalities, timestamp ordering, and deterministic replay. | One bounded function or validation stage |
| Track Adaptation Data Lineage | Timestamped observations, instruction tokens, action chunks, and embodiment metadata | Policy-ready token sequences, bounded actions, or rollout diagnostics | Check episode boundaries, action limits, reserved tokens, missing modalities, timestamp ordering, and deterministic replay. | One bounded function or validation stage |

## Data and evaluation

A small teaching implementation should use synthetic or separately licensed fixtures. Check episode boundaries, action limits, reserved tokens, missing modalities, timestamp ordering, and deterministic replay. Dataset names, exact protocol details, published metrics, and hardware requirements must be checked in the source PDF during full-text review; they are not inferred from an awesome-list entry. Keep educational component tests distinct from the paper's end-to-end evaluation.

## Limitations and failure modes

- This is a concise acquisition card, not a full-text technical review. Confirm equations, architecture details, and paper-stated limitations in the PDF before authoring theory.
- Passing synthetic component tests does not establish real-robot performance, robustness, or safe deployment.
- Package the action codec and observation schema with checkpoints; measure stale observations, control latency, invalid actions, and task success by embodiment.
- The paper, linked code, datasets, assets, and weights may carry different license conditions.

## Implementation decomposition

1. Balance Robot-Task Training Mixtures.
2. Construct Goal-Conditioned Policy Batches.
3. Track Adaptation Data Lineage.
4. Integrate the components on a small fixed fixture and record all deviations from the paper.
5. Add failure slices and a reproducible artifact report.

## Problem blueprints

### Problem: Balance Robot-Task Training Mixtures

- **Type:** component
- **Difficulty:** medium
- **Learning objective:** Implement and explain the balance robot-task training mixtures component.
- **Inputs:** Timestamped observations, instruction tokens, action chunks, and embodiment metadata; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Policy-ready token sequences, bounded actions, or rollout diagnostics; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check episode boundaries, action limits, reserved tokens, missing modalities, timestamp ordering, and deterministic replay. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Construct Goal-Conditioned Policy Batches

- **Type:** component
- **Difficulty:** hard
- **Learning objective:** Implement and explain the construct goal-conditioned policy batches component.
- **Inputs:** Timestamped observations, instruction tokens, action chunks, and embodiment metadata; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Policy-ready token sequences, bounded actions, or rollout diagnostics; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check episode boundaries, action limits, reserved tokens, missing modalities, timestamp ordering, and deterministic replay. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Track Adaptation Data Lineage

- **Type:** pipeline
- **Difficulty:** hard
- **Learning objective:** Implement and explain the track adaptation data lineage component.
- **Inputs:** Timestamped observations, instruction tokens, action chunks, and embodiment metadata; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Policy-ready token sequences, bounded actions, or rollout diagnostics; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check episode boundaries, action limits, reserved tokens, missing modalities, timestamp ordering, and deterministic replay. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

## Visual teaching plan

- Show a policy-data collection loop with dataset and model versions.
- Provide labeled axes, units, coordinate frames, and an equivalent table/text view. Use discrete steps when reduced motion is requested.
- Author diagrams independently; do not copy paper figures or captions.

## MLOps and deployment extensions

- Package the action codec and observation schema with checkpoints; measure stale observations, control latency, invalid actions, and task success by embodiment.
- Store paper ID, fixture hash, evaluator version, dependency lock, runtime digest, seed, and resource class with every result.
- Use structured failure reasons and per-slice metrics to distinguish implementation mistakes, distribution shifts, and infrastructure failures.

## Canonical sources

- [Primary arXiv record](https://arxiv.org/abs/2306.11706)
- [Open-access author manuscript](https://arxiv.org/pdf/2306.11706)

Identity metadata was read from the primary arXiv record. Local file signature, byte count, page parsing, and SHA-256 were verified on acquisition.

