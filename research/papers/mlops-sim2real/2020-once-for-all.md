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
execution_flow: {"title":"Core execution flow","description":"Train a shared elastic network, extract legal subnetworks, and select a measured accuracy/latency tradeoff for a target device.","nodes":[{"id":"stage-1","title":"Train elastic weights","detail":"Support several architecture choices through staged shared training.","column":0,"row":0,"section":"Train elastic weights","problem_slugs":[],"planned_problems":["Sample a Progressive-Shrinking Curriculum"]},{"id":"stage-2","title":"Extract a valid subnetwork","detail":"Select coherent depths, widths, kernels, and resolution with appropriate statistics.","column":1,"row":0,"section":"Extract a valid subnetwork","problem_slugs":[],"planned_problems":["Extract a Depth, Width, and Kernel Subnetwork"]},{"id":"stage-3","title":"Specialize for hardware","detail":"Search for a high-quality subnetwork under a measured device constraint.","column":2,"row":0,"section":"Specialize for hardware","problem_slugs":["edge-inference-release-gate"],"planned_problems":["Select a Pareto Model Under Accuracy and Latency Limits","Package and Verify an Edge Model Artifact"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"elastic supernetwork"},{"from":"stage-2","to":"stage-3","label":"candidate subnetworks"}]}
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

- Sample a Progressive-Shrinking Curriculum — unreviewed idea; contract and evaluator required.

### Extract a valid subnetwork

An architecture tuple $a=(d,w,k,r)$ must satisfy the model’s legal choices. Channel slicing and kernel transformations must agree across adjacent layers. Batch-normalization statistics may need recalibration for the selected subnetwork; inherited weights alone do not imply that all running statistics are correct.


**Component practice**

- Extract a Depth, Width, and Kernel Subnetwork — unreviewed idea; contract and evaluator required.

### Specialize for hardware

A specialization objective is

$$
a^*=\arg\max_{a\in\mathcal A}\operatorname{Accuracy}(a)
\quad\text{subject to}\quad\operatorname{Latency}(a;h)\le L_h.
$$

$h$ identifies the target hardware/runtime. FLOPs are not a substitute for latency. [Edge release gating](/problems/edge-inference-release-gate) is a related component for validating measured candidates; it does not implement the supernetwork training or search.


**Component practice**

- Supporting prerequisite: [Gate an Edge Model with Accuracy and Latency](/problems/edge-inference-release-gate). Practices the stated data or mathematical operation; it does not implement this paper-specific stage in full.
- Select a Pareto Model Under Accuracy and Latency Limits — unreviewed idea; contract and evaluator required.
- Package and Verify an Edge Model Artifact — unreviewed idea; contract and evaluator required.

## Implement the components

Each execution-flow node links the matching runnable component or names its planned problem. Planned titles are not runnable; labels distinguish reviewed drafts from unreviewed ideas.

- **Supporting prerequisite:** [Gate an Edge Model with Accuracy and Latency](/problems/edge-inference-release-gate).

**Planned component problems:**

- Sample a Progressive-Shrinking Curriculum — unreviewed idea; contract and evaluator required.
- Extract a Depth, Width, and Kernel Subnetwork — unreviewed idea; contract and evaluator required.
- Select a Pareto Model Under Accuracy and Latency Limits — unreviewed idea; contract and evaluator required.
- Package and Verify an Edge Model Artifact — unreviewed idea; contract and evaluator required.

These bounded exercises do not claim to reproduce the complete paper or its benchmark results.

## Why this matters on a robot

Different robots can have different accelerators and control deadlines, making device-specific specialization useful. Recalibrate and evaluate each extracted configuration on the actual sensor workload. Shared weights do not remove the need for per-configuration correctness and timing evidence.

## Sources and scope

[Primary paper](https://arxiv.org/abs/1908.09791) · [Open-access manuscript](https://arxiv.org/pdf/1908.09791)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
