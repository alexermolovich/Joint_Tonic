---
schema_version: 1
paper_id: "2020-once-for-all"
title: "Once-for-All: Train One Network and Specialize it for Efficient Deployment"
authors:
  - "Han Cai"
  - "Chuang Gan"
  - "Tianzhe Wang"
  - "Zhekai Zhang"
  - "Song Han"
year: 2020
venue_or_status: "ICLR 2020"
primary_url: "https://arxiv.org/abs/1908.09791"
pdf_url: "https://arxiv.org/pdf/1908.09791"
local_pdf: "./2020-once-for-all.pdf"
sha256: "ed04dfd495ca56610bf19a6ae6a9974489ff0e9720a3349a47a3abc009c3935f"
bytes: 3616911
pages: 15
topics:
  - "efficient-inference"
  - "neural-architecture-search"
  - "weight-sharing"
  - "edge-deployment"
  - "pareto-optimization"
modalities:
  - "network-architectures"
  - "model-weights"
  - "device-latency"
  - "accuracy"
track_role: "advanced"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
---

## Agent brief

Teach supernet specialization with a small elastic CNN or synthetic architecture table. The key exercises are legal subnetwork extraction and constrained accuracy/latency search, not full ImageNet training.

## Contribution

Once-for-All trains a weight-sharing network supporting many depths, widths, kernel sizes, and resolutions, then selects a specialized subnetwork for a target device without retraining each candidate.

## Prerequisite concepts

- Convolution shapes and channels
- Weight sharing and knowledge distillation concepts
- Multi-objective and constrained search
- Latency lookup tables or predictors

## Essential theory

Given an elastic architecture space \(\mathcal{A}\), predicted accuracy \(A(a)\), and measured or predicted device latency \(L_h(a)\), specialization solves

$$
a_h^*=\arg\max_{a\in\mathcal{A}} A(a)
\quad\text{subject to}\quad L_h(a)\le \tau_h.
$$

The weights are inherited from a shared supernet, so extraction rules must map each architecture choice to a consistent tensor slice.

## Method map

| Component | Input | Output | Core invariant | Good exercise boundary |
| --- | --- | --- | --- | --- |
| Subnetwork extractor | Supernet weights and architecture tuple | Specialized network tensors | Tensor slices match the requested depth/width/kernel choices | Extract one elastic layer family |
| Device predictor | Architecture and target hardware | Accuracy and latency estimates | Predictions use the declared device/model version | Query one lookup or predictor interface |
| Constrained search | Candidate space, predictors, and latency cap | Best feasible architecture | Returned architecture satisfies every hard constraint | Search a small discrete space |

- Elastic supernet across depth, width, kernel size, and resolution
- Progressive shrinking training schedule
- Weight and channel selection rules
- Accuracy predictor
- Device-specific latency model
- Evolutionary constrained search

## Data and evaluation

For an approachable track, provide pretrained toy weights and a candidate table with measured/synthetic latency. Validate subnetwork equivalence, constraint satisfaction, Pareto quality, and deterministic search.

## Limitations and failure modes

Training the full method is expensive and architecture-specific. Predicted latency may not match deployed latency, and the best image-classification subnetwork may not preserve downstream robot-policy behavior.

## Implementation decomposition

1. Represent elastic layer choices and validity constraints.
2. Extract weights for a selected subnetwork.
3. Build latency and accuracy lookup/prediction interfaces.
4. Search candidates under a target constraint.
5. Re-measure finalists and emit a deployment record.

## Problem blueprints

| Title | Type | Difficulty | Inputs | Outputs | Grading |
| --- | --- | --- | --- | --- | --- |
| Elastic Subnetwork Extraction | Neural-network coding | Medium | Supernet tensors and architecture tuple | Sliced tensors and shapes | Correct center kernels/channels/depth, no mutation |
| Progressive Shrinking Sampler | Training utility | Medium | Stage, search space, seed | Legal sampled architectures | Stage constraints, reproducibility, boundary coverage |
| Device-Constrained Search | Optimization | Hard | Candidate space, predictors, latency cap | Best architecture and metrics | Feasibility, score quality, deterministic tie-break |

## Visual teaching plan

- Nested-network diagram showing elastic depth, width, kernel, and input resolution.
- Interactive architecture controls that update parameter count, predicted accuracy, and device latency.
- Accuracy-latency Pareto frontier with a movable latency cap \(\tau_h\).
- Progressive-shrinking stage timeline showing which choices become active during training.

## MLOps and deployment extensions

Search against end-to-end control latency and peak memory, then re-evaluate task success, rare safety slices, and energy on each robot SKU. Track the selected architecture as a versioned child of the source supernet.

## Canonical sources

- [arXiv landing page](https://arxiv.org/abs/1908.09791)
- [arXiv PDF](https://arxiv.org/pdf/1908.09791)

