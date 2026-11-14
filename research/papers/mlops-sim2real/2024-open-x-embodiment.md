---
schema_version: 1
paper_id: "2024-open-x-embodiment"
title: "Open X-Embodiment: Robotic Learning Datasets and RT-X Models"
authors:
  - "Open X-Embodiment Collaboration (Abby O'Neill et al.)"
year: 2024
venue_or_status: "IEEE ICRA 2024"
primary_url: "https://arxiv.org/abs/2310.08864"
pdf_url: "https://arxiv.org/pdf/2310.08864"
local_pdf: "./2024-open-x-embodiment.pdf"
sha256: "13f16aff5afdee583dc25b3c570e9bb0cf6baefb59b539928d919588cd8d9246"
bytes: 4011306
pages: 12
topics:
  - "robot-data"
  - "cross-embodiment"
  - "dataset-mixtures"
  - "generalist-policies"
  - "transfer"
modalities:
  - "rgb"
  - "language"
  - "proprioception"
  - "actions"
  - "multi-robot-trajectories"
track_role: "core"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
---

## Agent brief

Teach the data-engineering problem behind cross-robot learning: heterogeneous observation keys, action spaces, control rates, task labels, and dataset sizes must be mapped into a common interface without erasing provenance.

## Contribution

Open X-Embodiment standardizes datasets from many robot embodiments and demonstrates that training across them can yield transfer to multiple robots and tasks. The operational contribution is a shared data format plus mixture-scale experimentation.

## Prerequisite concepts

- Robot poses, actions, and coordinate frames
- Sequence datasets and data loaders
- Multitask learning and sampling distributions
- Per-dataset and macro/micro evaluation

## Essential theory

Let \(D_k\) be dataset \(k\), \(w_k\) its sampling weight, and \(\ell\) a policy loss. A generic mixture objective is

$$
\mathcal{L}(\theta)=\sum_{k=1}^{K} w_k\;\mathbb{E}_{(o,a)\sim D_k}[\ell(\pi_\theta(o),a)],
\qquad w_k\ge 0,\quad \sum_k w_k=1.
$$

Uniform-over-examples weights large datasets heavily; uniform-over-datasets gives each embodiment equal mass. The choice changes what the model learns.

## Method map

| Component | Input | Output | Core invariant | Good exercise boundary |
| --- | --- | --- | --- | --- |
| Source adapter | Source episode and schema mapping | Canonical episode with provenance | Unit, frame, mask, and source identity are never implicit | Adapt one source dataset |
| Mixture sampler | Dataset sizes, weights, and seed | Dataset/example indices | Observed sampling follows declared weights reproducibly | Sample one finite epoch |
| Transfer evaluator | Per-task and per-robot outcomes | Macro, micro, and transfer metrics | Every aggregate exposes its denominator and embodiment slices | Compute one transfer matrix |

- Source-dataset adapters and provenance
- Shared episode/step representation
- Observation and action standardization
- Language/task normalization
- Multi-dataset sampling mixture
- Per-embodiment and transfer evaluation

## Data and evaluation

Use a synthetic set of robot datasets with different action dimensions, control rates, camera keys, and sizes. Verify round-trip adapters, mixture frequencies, masked dimensions, and both micro-averaged and macro-averaged metrics.

## Limitations and failure modes

Nominally shared fields can have different semantics, frames, units, and collection biases. Aggregate gains can hide regressions on smaller embodiments. Standardization does not eliminate licensing or consent constraints.

## Implementation decomposition

1. Define canonical episode, observation, action, task, and provenance schemas.
2. Write source adapters with unit/frame declarations.
3. Normalize or mask heterogeneous action spaces.
4. Implement configurable mixture sampling.
5. Report per-dataset, per-robot, and aggregate transfer metrics.

## Problem blueprints

| Title | Type | Difficulty | Inputs | Outputs | Grading |
| --- | --- | --- | --- | --- | --- |
| Canonical Episode Adapter | Data engineering | Hard | Source episode and adapter spec | Canonical episode plus provenance | Units/keys/timestamps, no information loss, schema validity |
| Normalize Action Spaces | Robotics data | Hard | Actions, bounds, masks, frame metadata | Canonical actions and validity mask | Correct scaling, masked dimensions, invalid-bound errors |
| Balanced Dataset Mixture | Sampling | Medium | Dataset sizes, weights, seed, sample count | Dataset/example indices | Reproducibility, observed frequencies, no out-of-range indices |
| Macro vs Micro Transfer Metrics | Evaluation | Medium | Per-task successes and counts | Both aggregates and gap report | Correct weighting, missing task handling, transparent denominators |

## Visual teaching plan

- Sankey diagram from heterogeneous source schemas into one canonical episode format.
- Interactive simplex or sliders for \(w_k\), updating expected samples per dataset.
- Heatmap of train-embodiment to test-embodiment transfer scores.
- Action-vector view showing active, normalized, and masked dimensions for each robot.

## MLOps and deployment extensions

Store source license, consent, robot model, frame convention, calibration, control rate, and transformation version with every episode. Make dataset-mixture weights and adapter hashes first-class training artifacts.

## Canonical sources

- [arXiv landing page](https://arxiv.org/abs/2310.08864)
- [arXiv PDF](https://arxiv.org/pdf/2310.08864)
- [Project page](https://robotics-transformer-x.github.io/)

