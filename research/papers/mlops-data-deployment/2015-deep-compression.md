---
schema_version: 1
paper_id: 2015-deep-compression
title: >-
  Deep Compression: Compressing Deep Neural Networks with Pruning, Trained
  Quantization and Huffman Coding
authors:
  - 'Han, Song'
  - 'Mao, Huizi'
  - 'Dally, William J.'
year: 2015
venue_or_status: >-
  Author-deposited arXiv manuscript; final venue not asserted by this
  acquisition card.
primary_url: 'https://arxiv.org/abs/1510.00149'
pdf_url: 'https://arxiv.org/pdf/1510.00149'
local_pdf: ./2015-deep-compression.pdf
sha256: 248044bef68e27e22384583a39d0bee743fd614d00e88a8dda6b331b5fd218d3
bytes: 1055865
pages: 14
topics:
  - mlops-data-deployment
  - deep-compression
modalities:
  - datasets
  - model-artifacts
  - logs
  - metrics
track_role: supporting
open_access_status: open-access-preprint
redistribution_note: Research copy only; verify the source license before redistribution.
execution_flow:
  title: Core execution flow
  description: >-
    Follow the data through the mechanism. Training objectives and inference
    behavior are distinguished in the linked explanations.
  nodes:
    - id: stage-1
      title: Prune and retrain
      detail: Remove weak connections and recover task quality.
      column: 0
      row: 0
      section: Prune and retrain
      problem_slugs:
        - deep-compression-pruning-mask
      planned_problems: []
    - id: stage-2
      title: Share quantized weights
      detail: Assign remaining weights to learned centroids.
      column: 1
      row: 0
      section: Share quantized weights
      problem_slugs:
        - deep-compression-centroid-assignment
      planned_problems: []
    - id: stage-3
      title: Encode and benchmark
      detail: Huffman-code repeated symbols and measure actual deployment.
      column: 2
      row: 0
      section: Encode and benchmark
      problem_slugs:
        - edge-inference-release-gate
        - deep-compression-storage-budget
      planned_problems: []
  edges:
    - from: stage-1
      to: stage-2
      label: sparse weights
    - from: stage-2
      to: stage-3
      label: quantized representation
---

## Core paper explanation

Deep Compression combines network pruning, trained weight sharing, and Huffman coding. The stages reduce different kinds of storage redundancy; smaller files do not automatically imply faster inference on hardware without suitable sparse or low-bit kernels.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Prune and retrain

A magnitude mask can be expressed as $m_i=\mathbf1[|w_i|\ge\tau]$, with effective weight $m_iw_i$. Retraining preserves the sparsity pattern while adjusting surviving parameters. Threshold choice is layer-dependent in the actual compression procedure.


**Component practice**

- Runnable component: [Apply a Weight-Pruning Mask](/problems/deep-compression-pruning-mask). Uses the bounded contract; no full paper reproduction is claimed.

### Share quantized weights

For centroid codebook $c_{1:K}$, assign $a_i=\arg\min_k|w_i-c_k|^2$. Shared-centroid training accumulates gradients:
$$\frac{\partial L}{\partial c_k}=\sum_{i:a_i=k}\frac{\partial L}{\partial w_i}.$$
Storage includes indices, sparse structure, and the codebook, not only $\log_2K$ bits per nonzero weight.


**Component practice**

- Runnable component: [Quantize Shared Weight Centroids](/problems/deep-compression-centroid-assignment). Uses the bounded contract; no full paper reproduction is claimed.

### Encode and benchmark

For symbol probabilities $p_k$ and code lengths $\ell_k$, average coding cost is $\bar\ell=\sum_kp_k\ell_k$. Entropy coding reduces serialized size but may require decoding before computation. Benchmark accuracy, peak memory, and latency on the intended runtime.


**Component practice**

- Supporting prerequisite: [Gate an Edge Model with Accuracy and Latency](/problems/edge-inference-release-gate). Practices the stated data or mathematical operation; it does not implement this paper-specific stage in full.
- Runnable component: [Compute a Compressed Model Storage Budget](/problems/deep-compression-storage-budget). Uses the bounded contract; no full paper reproduction is claimed.

## Implement the components

Runnable components and supporting prerequisites are attached to their matching execution-flow stages. Remaining titles are planned ideas requiring implementation and review.

- **Runnable component:** [Apply a Weight-Pruning Mask](/problems/deep-compression-pruning-mask).
- **Runnable component:** [Quantize Shared Weight Centroids](/problems/deep-compression-centroid-assignment).
- **Supporting prerequisite:** [Gate an Edge Model with Accuracy and Latency](/problems/edge-inference-release-gate).
- **Runnable component:** [Compute a Compressed Model Storage Budget](/problems/deep-compression-storage-budget).

These exercises implement their stated contracts, not a complete paper reproduction.


## Why this matters on a robot

Compression helps memory-constrained edge computers. Sparse indexing overhead, unsupported kernels, and accuracy loss on rare robot scenes can negate headline compression ratios.

## Scope of the runnable components

[Magnitude pruning](/problems/deep-compression-pruning-mask) returns an explicit inclusive-threshold mask; it does not retrain surviving weights. [Centroid assignment](/problems/deep-compression-centroid-assignment) chooses from a supplied codebook, retaining the first supplied centroid on ties, and does not fit or train that codebook. [Storage budgeting](/problems/deep-compression-storage-budget) accepts feasible prefix-code lengths and separately rounds symbol and sparse-index streams to bytes. It checks Kraft feasibility but does not build a Huffman tree or replicate the paper's sparse index format. The budget is a synthetic serialization model, not measured peak RAM or kernel latency.

## Sources and scope

[Primary paper](https://arxiv.org/abs/1510.00149) · [Open-access manuscript](https://arxiv.org/pdf/1510.00149)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
