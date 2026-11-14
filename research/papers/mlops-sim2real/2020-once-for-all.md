---
schema_version: 1
paper_id: 2020-once-for-all
title: 'Once-for-All: Train One Network and Specialize it for Efficient Deployment'
authors:
  - Han Cai
  - Chuang Gan
  - Tianzhe Wang
  - Zhekai Zhang
  - Song Han
year: 2020
venue_or_status: ICLR 2020
primary_url: 'https://arxiv.org/abs/1908.09791'
pdf_url: 'https://arxiv.org/pdf/1908.09791'
local_pdf: ./2020-once-for-all.pdf
sha256: ed04dfd495ca56610bf19a6ae6a9974489ff0e9720a3349a47a3abc009c3935f
bytes: 3616911
pages: 15
topics:
  - efficient-inference
  - neural-architecture-search
  - weight-sharing
  - edge-deployment
  - pareto-optimization
modalities:
  - network-architectures
  - model-weights
  - device-latency
  - accuracy
track_role: advanced
open_access_status: open-access-preprint
redistribution_note: Research copy only; verify the source license before redistribution.
execution_flow:
  title: Core execution flow
  description: >-
    Train a shared elastic network, extract legal subnetworks, and select a
    measured accuracy/latency tradeoff for a target device.
  nodes:
    - id: stage-1
      title: Train elastic weights
      detail: Support several architecture choices through staged shared training.
      column: 0
      row: 0
      section: Train elastic weights
      problem_slugs:
        - progressive-shrinking-curriculum
      planned_problems: []
    - id: stage-2
      title: Extract a valid subnetwork
      detail: >-
        Select coherent depths, widths, kernels, and resolution with appropriate
        statistics.
      column: 1
      row: 0
      section: Extract a valid subnetwork
      problem_slugs:
        - extract-elastic-subnetwork
      planned_problems: []
    - id: stage-3
      title: Specialize for hardware
      detail: Search for a high-quality subnetwork under a measured device constraint.
      column: 2
      row: 0
      section: Specialize for hardware
      problem_slugs:
        - edge-inference-release-gate
        - pareto-edge-model-selection
        - package-edge-model-artifact
      planned_problems: []
  edges:
    - from: stage-1
      to: stage-2
      label: elastic supernetwork
    - from: stage-2
      to: stage-3
      label: candidate subnetworks
---

## Core paper explanation

Once-for-All trains an elastic network that contains many candidate subnetworks, then specializes a suitable subnetwork for a hardware target. Progressive shrinking introduces smaller depth, width, kernel, and resolution choices after larger configurations have learned useful weights. This separates expensive shared training from cheaper device-specific architecture selection.

## Execution flow

Train a shared elastic network, extract legal subnetworks, and select a measured accuracy/latency tradeoff for a target device.

### Train elastic weights

Let architecture choice $a$ select a subnetwork from shared parameters $W$. Training can be described as

$$
\min_W\mathbb E_{a\sim p(a)}\mathcal L(f_{W,a}(x),y),
$$

with the allowed architecture set expanded progressively toward smaller configurations. Distillation from the largest trained network supplies soft targets. This expectation summarizes shared training; the progressive schedule is an essential implementation detail, not interchangeable with sampling all sizes from the start.


**Component practice**

- Runnable component: [Sample a Progressive-Shrinking Curriculum](/problems/progressive-shrinking-curriculum). Implements the bounded learning contract linked here, not the complete paper.

### Extract a valid subnetwork

An architecture tuple $a=(d,w,k,r)$ must satisfy the model’s legal choices. Channel slicing and kernel transformations must agree across adjacent layers. Batch-normalization statistics may need recalibration for the selected subnetwork; inherited weights alone do not imply that all running statistics are correct.


**Component practice**

- Runnable component: [Extract a Depth, Width, and Kernel Subnetwork](/problems/extract-elastic-subnetwork). Implements the bounded learning contract linked here, not the complete paper.

### Specialize for hardware

A specialization objective is

$$
a^*=\arg\max_{a\in\mathcal A}\operatorname{Accuracy}(a)
\quad\text{subject to}\quad\operatorname{Latency}(a;h)\le L_h.
$$

$h$ identifies the target hardware/runtime. FLOPs are not a substitute for latency. [Edge release gating](/problems/edge-inference-release-gate) is a related component for validating measured candidates; it does not implement the supernetwork training or search.


**Component practice**

- Supporting prerequisite: [Gate an Edge Model with Accuracy and Latency](/problems/edge-inference-release-gate). Practices the stated data or mathematical operation; it does not implement this paper-specific stage in full.
- Runnable component: [Select a Pareto Model Under Accuracy and Latency Limits](/problems/pareto-edge-model-selection). Implements the bounded learning contract linked here, not the complete paper.
- Runnable component: [Package and Verify an Edge Model Artifact](/problems/package-edge-model-artifact). Implements the bounded learning contract linked here, not the complete paper.

## Implement the components

Execution-flow nodes link runnable component exercises. Any additional research ideas remain explicitly labeled as future work and do not imply a complete paper reproduction.

- **Supporting prerequisite:** [Gate an Edge Model with Accuracy and Latency](/problems/edge-inference-release-gate).

**Component implementation map:**

- Runnable component: [Sample a Progressive-Shrinking Curriculum](/problems/progressive-shrinking-curriculum). Implements the bounded learning contract linked here, not the complete paper.
- Runnable component: [Extract a Depth, Width, and Kernel Subnetwork](/problems/extract-elastic-subnetwork). Implements the bounded learning contract linked here, not the complete paper.
- Runnable component: [Select a Pareto Model Under Accuracy and Latency Limits](/problems/pareto-edge-model-selection). Implements the bounded learning contract linked here, not the complete paper.
- Runnable component: [Package and Verify an Edge Model Artifact](/problems/package-edge-model-artifact). Implements the bounded learning contract linked here, not the complete paper.

These bounded exercises do not claim to reproduce the complete paper or its benchmark results.

## Why this matters on a robot

Different robots can have different accelerators and control deadlines, making device-specific specialization useful. Recalibrate and evaluate each extracted configuration on the actual sensor workload. Shared weights do not remove the need for per-configuration correctness and timing evidence.

## Scope of the runnable engineering components

The exercises separate architecture eligibility from deployment evidence. [Subnetwork extraction](/problems/extract-elastic-subnetwork) uses leading channels and centered kernel crops as an original simplification; OFA's learned kernel transformations and batch-normalization recalibration are outside this contract. [Progressive sampling](/problems/progressive-shrinking-curriculum) fixes a reproducible teaching phase schedule rather than reproducing the paper's full training algorithm. [Pareto selection](/problems/pareto-edge-model-selection) uses supplied accuracy/latency measurements. [Artifact packaging](/problems/package-edge-model-artifact) hashes declared in-memory model evidence without parsing or certifying a deployed model.

## Sources and scope

[Primary paper](https://arxiv.org/abs/1908.09791) · [Open-access manuscript](https://arxiv.org/pdf/1908.09791)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
