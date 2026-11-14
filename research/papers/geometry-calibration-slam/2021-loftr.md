---
schema_version: 1
paper_id: 2021-loftr
title: 'LoFTR: Detector-Free Local Feature Matching with Transformers'
authors:
  - 'Sun, Jiaming'
  - 'Shen, Zehong'
  - 'Wang, Yuang'
  - 'Bao, Hujun'
  - 'Zhou, Xiaowei'
year: 2021
venue_or_status: >-
  Author-deposited arXiv manuscript; final venue not asserted by this
  acquisition card.
primary_url: 'https://arxiv.org/abs/2104.00680'
pdf_url: 'https://arxiv.org/pdf/2104.00680'
local_pdf: ./2021-loftr.pdf
sha256: d2f18e76fd92f234362f72d01ecf99d37d144f488360aca809bdeefed7fd2cef
bytes: 8175934
pages: 10
topics:
  - geometry-calibration-slam
  - loftr
modalities:
  - camera
  - imu
  - lidar
  - poses
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
      title: Condition dense features
      detail: Use self-attention and cross-attention across image grids.
      column: 0
      row: 0
      section: Condition dense features
      problem_slugs:
        - paired-linear-image-attention
      planned_problems: []
    - id: stage-2
      title: Select coarse matches
      detail: Normalize pair similarities and retain confident mutual pairs.
      column: 1
      row: 0
      section: Select coarse matches
      problem_slugs:
        - dual-softmax-coarse-matches
      planned_problems: []
    - id: stage-3
      title: Refine local positions
      detail: Estimate subpixel correspondence inside fine windows.
      column: 2
      row: 0
      section: Refine local positions
      problem_slugs:
        - local-window-match-expectation
        - sampson-epipolar-match-gate
      planned_problems: []
  edges:
    - from: stage-1
      to: stage-2
      label: conditioned features
    - from: stage-2
      to: stage-3
      label: coarse pairs
---

## Core paper explanation

LoFTR finds image correspondences without first requiring a sparse keypoint detector. Transformer-conditioned coarse features identify candidate matches, and a fine-resolution stage refines their positions.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Condition dense features

Coarse feature grids become sequences $F_A\in\mathbb R^{N\times d}$ and $F_B\in\mathbb R^{M\times d}$ with positional encoding. Cross-attention lets a location in one image use evidence from the other before matching.

The paper uses a positive-feature linear attention variant to keep dense feature processing manageable. The linked exercise isolates its key/value summary and paired information flow with supplied single-head weights, explicit masks, and simultaneous cross updates. It omits the complete encoder layer's normalization and feed-forward blocks.




**Implement these components:** [Apply Paired-Image Self and Cross Attention](/problems/paired-linear-image-attention). Each exercise states its bounded numerical contract; completing these components does not reproduce the complete trained model.

### Select coarse matches

For similarity $S_{ij}=f_i^\top g_j/\tau$, the dual-softmax option uses
$$P_{ij}=\operatorname{softmax}_{j}(S_{ij})\operatorname{softmax}_{i}(S_{ij}).$$
Thresholding and mutual consistency select coarse matches. The paper also investigates an optimal-transport matching alternative; these normalizations are different choices, not simultaneous requirements.

The runnable dual-softmax exercise uses the released feature convention of dividing each descriptor by the square root of channel width before its dot product. Its resulting score denominator is $d\tau$. Invalid descriptors are excluded before normalization, and exact ties have an explicit first-index rule.


**Implement these components:** [Construct Coarse Correspondence Candidates](/problems/dual-softmax-coarse-matches). Each exercise states its bounded numerical contract; completing these components does not reproduce the complete trained model.

### Refine local positions

A local correlation distribution $p_k$ over fine-window offsets $\Delta u_k$ gives an expectation
$$\widehat{\Delta u}=\sum_k p_k\Delta u_k.$$
Map the refined coordinates back to original image pixels with the correct feature-grid scale. A confident local match still requires epipolar or pose verification for geometric use.

The local-window exercise returns pixel-space covariance as an original diagnostic, distinct from the paper's normalized uncertainty output. The separate geometric exercise computes Sampson error from a supplied fundamental matrix, including degeneracy handling; it does not estimate that matrix or perform RANSAC.


**Implement these components:** [Refine a Match in a Local Window](/problems/local-window-match-expectation) · [Filter Geometrically Inconsistent Matches](/problems/sampson-epipolar-match-gate). Each exercise states its bounded numerical contract; completing these components does not reproduce the complete trained model.

## Implement the components

The linked atomic components are implemented with synthetic fixtures, explicit numerical contracts and reviewed evaluators. Full training, benchmark reproduction and model integration remain outside these exercises.

**Runnable components:**

- [Apply Paired-Image Self and Cross Attention](/problems/paired-linear-image-attention) — runnable bounded component.
- [Construct Coarse Correspondence Candidates](/problems/dual-softmax-coarse-matches) — runnable bounded component.
- [Refine a Match in a Local Window](/problems/local-window-match-expectation) — runnable bounded component.
- [Filter Geometrically Inconsistent Matches](/problems/sampson-epipolar-match-gate) — runnable bounded component.

[Browse the curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md).

## Why this matters on a robot

Detector-free matching can help low-texture scenes. Repeated structures and moving objects can create coherent false matches; localization should combine matching evidence with robust geometry.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2104.00680) · [Open-access manuscript](https://arxiv.org/pdf/2104.00680)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
