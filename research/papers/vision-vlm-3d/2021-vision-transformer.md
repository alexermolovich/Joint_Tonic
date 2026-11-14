---
schema_version: 1
paper_id: "2021-vision-transformer"
title: "An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale"
authors: ["Alexey Dosovitskiy", "Lucas Beyer", "Alexander Kolesnikov", "Dirk Weissenborn", "Xiaohua Zhai", "Thomas Unterthiner", "Mostafa Dehghani", "Matthias Minderer", "Georg Heigold", "Sylvain Gelly", "Jakob Uszkoreit", "Neil Houlsby"]
year: 2021
venue_or_status: "ICLR 2021"
primary_url: "https://arxiv.org/abs/2010.11929"
pdf_url: "https://arxiv.org/pdf/2010.11929"
local_pdf: "./2021-vision-transformer.pdf"
sha256: "8ce7b83971a14508ca711a27c875c9b6914c4f6767cf3150fb1ca6c07aa056d6"
bytes: 3743814
pages: 22
topics: ["vision transformers", "image classification", "patch embeddings", "transfer learning"]
modalities: ["RGB image"]
track_role: "Backbone prerequisite for transformer-based perception"
open_access_status: "Open-access arXiv manuscript"
redistribution_note: "Retain the original attribution and license metadata; verify source terms before redistributing outside this research workspace."
---

## Agent brief

Use ViT as the backbone bridge between image tensors and token-based architectures. The most transferable tasks are patchification, position-embedding resize, pre-norm encoder blocks, attention masks, and representation extraction.

## Contribution

ViT applies a largely standard Transformer encoder to a sequence of non-overlapping image-patch embeddings. With large-scale pretraining, the model transfers effectively without a convolutional feature hierarchy.

## Prerequisite concepts

- Image tensor layout and convolution/linear equivalence for patch projection
- Multi-head self-attention and residual connections
- Layer normalization, MLP blocks, and classification tokens
- Pretraining, fine-tuning, and resolution changes

## Method map

1. Split an image into fixed-size, non-overlapping patches.
2. Flatten/project each patch to the model dimension.
3. Prepend a learned classification token and add learned position embeddings.
4. Apply repeated pre-normalized attention and feed-forward blocks.
5. Use the classification-token representation for the task head.

## Essential equations

For image height (H), width (W), and square patch size (P), the patch count is

$$
N=\frac{HW}{P^2}.
$$

The initial token sequence can be expressed as

$$
z_0=[x_{\mathrm{cls}};\,x_1E;\ldots;x_NE]+E_{\mathrm{pos}}.
$$

A pre-normalized encoder block applies

$$
u=z+\operatorname{MSA}(\operatorname{LN}(z)),\qquad
z'=u+\operatorname{MLP}(\operatorname{LN}(u)).
$$

## Visual teaching plan

- **Patch/token map:** Hover over a patch to highlight its token and attention connections; adjust patch size to reveal token-count growth.
- **Position-resize explorer:** Compare the old/new 2D position grids and interpolated embeddings when resolution changes.
- **Attention-cost chart:** An interactive resolution/patch-size control plots (N) and an (N^2) attention-cost proxy.

## Data and evaluation

The paper studies large-scale pretraining followed by transfer to ImageNet, CIFAR, VTAB, and related benchmarks. A practical teaching track should compare scratch versus pretrained behavior, resolution transfer, accuracy, throughput, and token-count scaling.

## Limitations and failure modes

- Strong results rely on substantial pretraining data and compute.
- Self-attention cost grows quadratically with patch count.
- Fixed patch size can lose fine detail important for small objects.
- Learned positions require careful interpolation when input resolution changes.

## Implementation decomposition

1. Patchify/unpatchify operations and shape validation.
2. Patch projection and classification token insertion.
3. Learned positions plus 2D interpolation.
4. Pre-norm attention/MLP encoder block.
5. Stack, pool/head, checkpoint loading, and resolution-transfer tests.

## Problem blueprints

### Patchify and reconstruct an image

- **Type:** Tensor reshaping
- **Difficulty:** Easy
- **Inputs:** Batched images and patch height/width
- **Outputs:** Ordered patch sequence and exact unpatchified reconstruction
- **Grading:** Pixel-perfect round trip; row-major ordering; non-divisible dimension validation; channel-layout contract

### Resize learned position embeddings

- **Type:** Model surgery
- **Difficulty:** Medium
- **Inputs:** Class-token position, square/grid patch positions, old/new grid shapes
- **Outputs:** Position tensor for the new token sequence
- **Grading:** Class token unchanged; correct 2D interpolation axes; non-square grids; dtype/device preserved

### Implement a pre-norm ViT block

- **Type:** PyTorch module
- **Difficulty:** Medium
- **Inputs:** Token batch and optional padding mask
- **Outputs:** Same-shaped transformed tokens
- **Grading:** Norm-before-sublayer order; two residual paths; mask behavior; dropout disabled deterministically in eval; gradient checks

## MLOps and deployment extensions

- Record input resolution, patch size, token count, interpolation method, and normalization statistics in the model signature.
- Benchmark latency and memory across resolutions; token growth can dominate deployment cost.
- Test checkpoint conversions with layer-by-layer numerical comparisons.
- Monitor downstream camera shifts by embedding distribution and task-specific slice metrics, not classifier confidence alone.

## Canonical sources

- [Primary record](https://arxiv.org/abs/2010.11929)
- [Open-access PDF](https://arxiv.org/pdf/2010.11929)

