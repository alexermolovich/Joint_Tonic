---
schema_version: 1
paper_id: "2021-robomimic"
title: "What Matters in Learning from Offline Human Demonstrations for Robot Manipulation"
authors:
  - "Ajay Mandlekar"
  - "Danfei Xu"
  - "Josiah Wong"
  - "Soroush Nasiriany"
  - "Chen Wang"
  - "Rohun Kulkarni"
  - "Li Fei-Fei"
  - "Silvio Savarese"
  - "Yuke Zhu"
  - "Roberto Martin-Martin"
year: 2021
venue_or_status: "CoRL 2021 (PMLR proceedings 2022)"
primary_url: "https://arxiv.org/abs/2108.03298"
pdf_url: "https://arxiv.org/pdf/2108.03298"
local_pdf: "./2021-robomimic.pdf"
sha256: "18283ff9cbb9645de4ccf32ca2de472f452e89761287e7ed578e3a1066bea5f1"
bytes: 10782355
pages: 36
topics:
  - "imitation-learning"
  - "offline-rl"
  - "robot-demonstrations"
  - "reproducibility"
  - "evaluation"
modalities:
  - "rgb"
  - "wrist-camera"
  - "proprioception"
  - "actions"
  - "trajectories"
track_role: "foundation"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
---

## Agent brief

Build reliable dataset and evaluation utilities for imitation learning from variable-quality human demonstrations. The best first problems cover trajectories, batching, policy selection, and success metrics rather than reproducing every algorithm.

## Contribution

The work compares offline learning choices across simulated and real manipulation tasks, demonstration qualities, observation types, and algorithms. It shows that temporal models, data quality, observation design, and checkpoint selection materially affect results.

## Prerequisite concepts

- Supervised learning and recurrent networks
- Markov decision processes and behavior cloning
- Variable-length sequence batching
- Train/validation splits and rollout evaluation

## Essential theory

For a trajectory dataset \(D\) containing observation-action pairs, a basic behavior-cloning objective is

$$
\mathcal{L}_{\mathrm{BC}}(\theta)=\frac{1}{|D|}\sum_{(o_t,a_t)\in D}\lVert \pi_\theta(o_{\le t})-a_t\rVert_2^2.
$$

The history \(o_{\le t}\) matters when demonstrations are non-Markovian. Rollout success is estimated separately from training loss:

$$
\widehat{S}=\frac{1}{N}\sum_{i=1}^{N}\mathbf{1}[\text{task }i\text{ succeeds}].
$$

The two metrics need not rank checkpoints the same way.

## Method map

| Component | Input | Output | Core invariant | Good exercise boundary |
| --- | --- | --- | --- | --- |
| Episode indexer | Demonstration trajectories and metadata | Leakage-safe dataset splits | No episode appears in more than one split | Implement deterministic stratified splitting |
| Sequence loader | Variable-length episodes | Padded tensors, masks, and lengths | Padding never contributes to the learning loss | Batch one observation/action modality |
| Policy evaluator | Checkpoints and rollout outcomes | Success metrics with uncertainty | Evaluation preserves task, seed, and quality slices | Compare checkpoints under one declared rule |

- Standardized demonstration datasets and task metadata
- Low-dimensional and image observation pipelines
- Behavior cloning, recurrent, hierarchical, and offline-RL baselines
- Dataset-quality and size ablations
- Fixed-seed training plus rollout evaluation
- Checkpoint selection analysis

## Data and evaluation

Use complete trajectories and split by episode, never by individual time step. Preserve operator and quality labels for slices. Evaluate mean success across seeds and tasks, variance, checkpoint sensitivity, and results by data quality.

## Limitations and failure modes

Benchmark tasks and robot setups do not cover open-world deployment. Online rollout evaluation can be expensive and unsafe, while offline validation loss is an imperfect substitute. Results depend on observation and action conventions.

## Implementation decomposition

1. Validate and index episodes without cross-split leakage.
2. Build padded sequence batches and masks.
3. Train a feed-forward or recurrent behavior-cloning baseline.
4. Evaluate checkpoints by loss and recorded rollout outcomes.
5. Report quality, operator, task, and seed slices.

## Problem blueprints

| Title | Type | Difficulty | Inputs | Outputs | Grading |
| --- | --- | --- | --- | --- | --- |
| Episode-Safe Split | Data engineering | Easy | Trajectory IDs, operator/task labels, seed | Train/validation/test episode sets | No leakage, requested ratios, deterministic stratification |
| Pad Demonstration Sequences | Tensor coding | Medium | Variable-length observations/actions | Padded tensors, mask, lengths | Shape, mask accuracy, empty/maximum-length handling |
| Select a Policy Checkpoint | Evaluation | Hard | Loss curves and rollout success samples | Selected checkpoint and evidence | Correct aggregation, uncertainty handling, declared rule |
| Mixed-Quality Sampler | Data loader | Medium | Episode quality labels and target weights | Seeded epoch indices | Exact weights within tolerance, reproducibility, full validity |

## Visual teaching plan

- Interactive episode timeline showing observation, action, padding mask, and split membership.
- Scatter plot of validation loss versus rollout success with a checkpoint selector slider.
- Small-multiples success chart by task, data quality, and random seed.
- Toggle between feed-forward context \(o_t\) and recurrent context \(o_{\le t}\) to illustrate ambiguity.

## MLOps and deployment extensions

Version demonstrations with robot, sensor, calibration, operator, site, and intervention metadata. Add automatic leakage checks, dataset cards, checkpoint lineage, offline-policy-evaluation warnings, and staged rollout approvals.

## Canonical sources

- [arXiv landing page](https://arxiv.org/abs/2108.03298)
- [arXiv PDF](https://arxiv.org/pdf/2108.03298)
- [robomimic project](https://robomimic.github.io/)

