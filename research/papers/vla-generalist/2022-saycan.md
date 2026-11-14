---
schema_version: 1
paper_id: "2022-saycan"
title: "Do As I Can, Not As I Say: Grounding Language in Robotic Affordances"
authors: ["Ahn, Michael","Brohan, Anthony","Brown, Noah","Chebotar, Yevgen","Cortes, Omar","David, Byron","Finn, Chelsea","Fu, Chuyuan","Gopalakrishnan, Keerthana","Hausman, Karol","Herzog, Alex","Ho, Daniel","Hsu, Jasmine","Ibarz, Julian","Ichter, Brian","Irpan, Alex","Jang, Eric","Ruano, Rosario Jauregui","Jeffrey, Kyle","Jesmonth, Sally","Joshi, Nikhil J","Julian, Ryan","Kalashnikov, Dmitry","Kuang, Yuheng","Lee, Kuang-Huei","Levine, Sergey","Lu, Yao","Luu, Linda","Parada, Carolina","Pastor, Peter","Quiambao, Jornell","Rao, Kanishka","Rettinghouse, Jarek","Reyes, Diego","Sermanet, Pierre","Sievers, Nicolas","Tan, Clayton","Toshev, Alexander","Vanhoucke, Vincent","Xia, Fei","Xiao, Ted","Xu, Peng","Xu, Sichun","Yan, Mengyuan","Zeng, Andy"]
year: 2022
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2204.01691"
pdf_url: "https://arxiv.org/pdf/2204.01691"
local_pdf: "./2022-saycan.pdf"
sha256: "48c22d36a044bbbd34e640beb1db4fb4ba57e74d97fefa0fb121d55c31282312"
bytes: 12827088
pages: 34
topics: ["vla-generalist","saycan"]
modalities: ["rgb","text","robot-state","actions"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
---

# Do As I Can, Not As I Say: Grounding Language in Robotic Affordances

## Agent brief

Combine language-model skill preferences with learned action feasibility when selecting robot skills. This acquisition card verifies the primary paper identity and local PDF, and proposes components that can become independently testable Joint Tonic problems. Full-text technical review is required before promoting an idea into a reviewed problem blueprint.

## Contribution

Combine language-model skill preferences with learned action feasibility when selecting robot skills.

The proposed exercises below are original teaching decompositions. They do not assert a full reproduction of the paper or any published performance number.

## Prerequisite concepts

- Sequence modeling, action units, control frequencies, multimodal batching, and policy evaluation.

## Method map

| Component candidate | Input | Output | Core invariant | Good exercise boundary |
|---|---|---|---|---|
| Combine Skill Likelihood and Feasibility Scores | Timestamped observations, instruction tokens, action chunks, and embodiment metadata | Policy-ready token sequences, bounded actions, or rollout diagnostics | Check episode boundaries, action limits, reserved tokens, missing modalities, timestamp ordering, and deterministic replay. | One bounded function or validation stage |
| Rank Grounded Skill Candidates | Timestamped observations, instruction tokens, action chunks, and embodiment metadata | Policy-ready token sequences, bounded actions, or rollout diagnostics | Check episode boundaries, action limits, reserved tokens, missing modalities, timestamp ordering, and deterministic replay. | One bounded function or validation stage |
| Stop a Skill Sequence at Completion | Timestamped observations, instruction tokens, action chunks, and embodiment metadata | Policy-ready token sequences, bounded actions, or rollout diagnostics | Check episode boundaries, action limits, reserved tokens, missing modalities, timestamp ordering, and deterministic replay. | One bounded function or validation stage |

## Data and evaluation

A small teaching implementation should use synthetic or separately licensed fixtures. Check episode boundaries, action limits, reserved tokens, missing modalities, timestamp ordering, and deterministic replay. Dataset names, exact protocol details, published metrics, and hardware requirements must be checked in the source PDF during full-text review; they are not inferred from an awesome-list entry. Keep educational component tests distinct from the paper's end-to-end evaluation.

## Limitations and failure modes

- This is a concise acquisition card, not a full-text technical review. Confirm equations, architecture details, and paper-stated limitations in the PDF before authoring theory.
- Passing synthetic component tests does not establish real-robot performance, robustness, or safe deployment.
- Package the action codec and observation schema with checkpoints; measure stale observations, control latency, invalid actions, and task success by embodiment.
- The paper, linked code, datasets, assets, and weights may carry different license conditions.

## Implementation decomposition

1. Combine Skill Likelihood and Feasibility Scores.
2. Rank Grounded Skill Candidates.
3. Stop a Skill Sequence at Completion.
4. Integrate the components on a small fixed fixture and record all deviations from the paper.
5. Add failure slices and a reproducible artifact report.

## Problem blueprints

### Problem: Combine Skill Likelihood and Feasibility Scores

- **Type:** component
- **Difficulty:** medium
- **Learning objective:** Implement and explain the combine skill likelihood and feasibility scores component.
- **Inputs:** Timestamped observations, instruction tokens, action chunks, and embodiment metadata; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Policy-ready token sequences, bounded actions, or rollout diagnostics; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check episode boundaries, action limits, reserved tokens, missing modalities, timestamp ordering, and deterministic replay. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Rank Grounded Skill Candidates

- **Type:** component
- **Difficulty:** hard
- **Learning objective:** Implement and explain the rank grounded skill candidates component.
- **Inputs:** Timestamped observations, instruction tokens, action chunks, and embodiment metadata; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Policy-ready token sequences, bounded actions, or rollout diagnostics; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check episode boundaries, action limits, reserved tokens, missing modalities, timestamp ordering, and deterministic replay. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Stop a Skill Sequence at Completion

- **Type:** pipeline
- **Difficulty:** hard
- **Learning objective:** Implement and explain the stop a skill sequence at completion component.
- **Inputs:** Timestamped observations, instruction tokens, action chunks, and embodiment metadata; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Policy-ready token sequences, bounded actions, or rollout diagnostics; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check episode boundaries, action limits, reserved tokens, missing modalities, timestamp ordering, and deterministic replay. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

## Visual teaching plan

- Compare linguistic and feasibility score bars for candidate robot skills.
- Provide labeled axes, units, coordinate frames, and an equivalent table/text view. Use discrete steps when reduced motion is requested.
- Author diagrams independently; do not copy paper figures or captions.

## MLOps and deployment extensions

- Package the action codec and observation schema with checkpoints; measure stale observations, control latency, invalid actions, and task success by embodiment.
- Store paper ID, fixture hash, evaluator version, dependency lock, runtime digest, seed, and resource class with every result.
- Use structured failure reasons and per-slice metrics to distinguish implementation mistakes, distribution shifts, and infrastructure failures.

## Canonical sources

- [Primary arXiv record](https://arxiv.org/abs/2204.01691)
- [Open-access author manuscript](https://arxiv.org/pdf/2204.01691)

Identity metadata was read from the primary arXiv record. Local file signature, byte count, page parsing, and SHA-256 were verified on acquisition.

