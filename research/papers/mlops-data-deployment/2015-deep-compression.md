---
schema_version: 1
paper_id: "2015-deep-compression"
title: "Deep Compression: Compressing Deep Neural Networks with Pruning, Trained Quantization and Huffman Coding"
authors: ["Han, Song","Mao, Huizi","Dally, William J."]
year: 2015
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/1510.00149"
pdf_url: "https://arxiv.org/pdf/1510.00149"
local_pdf: "./2015-deep-compression.pdf"
sha256: "248044bef68e27e22384583a39d0bee743fd614d00e88a8dda6b331b5fd218d3"
bytes: 1055865
pages: 14
topics: ["mlops-data-deployment","deep-compression"]
modalities: ["datasets","model-artifacts","logs","metrics"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Prune and retrain","detail":"Remove weak connections and recover task quality.","column":0,"row":0,"section":"Prune and retrain","problem_slugs":[],"planned_problems":["Apply a Weight-Pruning Mask"]},{"id":"stage-2","title":"Share quantized weights","detail":"Assign remaining weights to learned centroids.","column":1,"row":0,"section":"Share quantized weights","problem_slugs":[],"planned_problems":["Quantize Shared Weight Centroids"]},{"id":"stage-3","title":"Encode and benchmark","detail":"Huffman-code repeated symbols and measure actual deployment.","column":2,"row":0,"section":"Encode and benchmark","problem_slugs":["edge-inference-release-gate"],"planned_problems":["Compute a Compressed Model Storage Budget"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"sparse weights"},{"from":"stage-2","to":"stage-3","label":"quantized representation"}]}
---

## Core paper explanation

Deep Compression combines network pruning, trained weight sharing, and Huffman coding. The stages reduce different kinds of storage redundancy; smaller files do not automatically imply faster inference on hardware without suitable sparse or low-bit kernels.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Prune and retrain

A magnitude mask can be expressed as $m_i=\mathbf1[|w_i|\ge\tau]$, with effective weight $m_iw_i$. Retraining preserves the sparsity pattern while adjusting surviving parameters. Threshold choice is layer-dependent in the actual compression procedure.


**Component practice**

- Apply a Weight-Pruning Mask — unreviewed idea; contract and evaluator required.

### Share quantized weights

For centroid codebook $c_{1:K}$, assign $a_i=\arg\min_k|w_i-c_k|^2$. Shared-centroid training accumulates gradients:
$$\frac{\partial L}{\partial c_k}=\sum_{i:a_i=k}\frac{\partial L}{\partial w_i}.$$
Storage includes indices, sparse structure, and the codebook, not only $\log_2K$ bits per nonzero weight.


**Component practice**

- Quantize Shared Weight Centroids — unreviewed idea; contract and evaluator required.

### Encode and benchmark

For symbol probabilities $p_k$ and code lengths $\ell_k$, average coding cost is $\bar\ell=\sum_kp_k\ell_k$. Entropy coding reduces serialized size but may require decoding before computation. Benchmark accuracy, peak memory, and latency on the intended runtime.


**Component practice**

- Supporting prerequisite: [Gate an Edge Model with Accuracy and Latency](/problems/edge-inference-release-gate). Practices the stated data or mathematical operation; it does not implement this paper-specific stage in full.
- Compute a Compressed Model Storage Budget — unreviewed idea; contract and evaluator required.

## Implement the components

Each execution-flow node links the matching runnable component or names its planned problem. Planned titles are not runnable; labels distinguish reviewed drafts from unreviewed ideas.

- **Supporting prerequisite:** [Gate an Edge Model with Accuracy and Latency](/problems/edge-inference-release-gate).

**Planned component problems:**

- Apply a Weight-Pruning Mask — unreviewed idea; contract and evaluator required.
- Quantize Shared Weight Centroids — unreviewed idea; contract and evaluator required.
- Compute a Compressed Model Storage Budget — unreviewed idea; contract and evaluator required.

These bounded exercises do not claim to reproduce the complete paper or its benchmark results.

## Why this matters on a robot

Compression helps memory-constrained edge computers. Sparse indexing overhead, unsupported kernels, and accuracy loss on rare robot scenes can negate headline compression ratios.

## Sources and scope

[Primary paper](https://arxiv.org/abs/1510.00149) · [Open-access manuscript](https://arxiv.org/pdf/1510.00149)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
