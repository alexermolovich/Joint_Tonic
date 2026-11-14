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
execution_flow: {"title":"Core execution flow","description":"The inference path converts image patches to tokens, applies transformer blocks, and reads a classification representation. Training optimizes the chosen supervised head; robotics reuse may retain patch features instead.","nodes":[{"id":"stage-1","title":"Patchify the image","detail":"Flatten fixed image patches and project them into token embeddings.","column":0,"row":0,"section":"Patchify the image","problem_slugs":["vit-patchify-reconstruct","vit-patch-class-tokens","vit-position-interpolation"],"planned_problems":[]},{"id":"stage-2","title":"Mix patch information","detail":"Attention exchanges information globally; an MLP transforms each token.","column":1,"row":0,"section":"Mix patch information","problem_slugs":[],"planned_problems":["Assemble a Pre-Norm Vision Transformer Block","Profile Token Count, Memory, and Latency by Resolution"]},{"id":"stage-3","title":"Read out a representation","detail":"Use the class token for classification or retain spatial tokens for later tasks.","column":2,"row":0,"section":"Read out a representation","problem_slugs":[],"planned_problems":["Read a Normalized Class Token with a Linear Head"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"patch tokens"},{"from":"stage-2","to":"stage-3","label":"encoded tokens"}]}
---

## Core paper explanation

A Vision Transformer processes an image as a sequence of fixed-size patches. Each patch is projected into an embedding, position information is added, and transformer blocks exchange information between patches. The architecture makes the image-to-token interface explicit: resolution, patch size, token order, and position embeddings determine what the transformer sees. The original work studies image classification; the token representation is also useful inside later VLMs and robot policies.

## Execution flow

The inference path converts image patches to tokens, applies transformer blocks, and reads a classification representation. Training optimizes the chosen supervised head; robotics reuse may retain patch features instead.

### Patchify the image

For $I\in\mathbb R^{H\times W\times C}$ and patch side $P$ dividing $H,W$, there are $N=HW/P^2$ patches. Each flattened patch $x_i\in\mathbb R^{P^2C}$ is projected by $E\in\mathbb R^{P^2C\times d}$:

$$
Z_0=[x_{\mathrm{cls}};x_1E;\ldots;x_NE]+E_{\mathrm{pos}},
\qquad Z_0\in\mathbb R^{(N+1)\times d}.
$$

The class token is learned, and $E_{\mathrm{pos}}$ has the same sequence shape. Patch traversal order must agree with position embedding order; a shape-correct transpose can silently scramble the image.


**Implement this component:** [Patchify and Reconstruct an Image Tensor](/problems/vit-patchify-reconstruct) · [Build Learned Patch and Class Tokens](/problems/vit-patch-class-tokens). Each linked exercise implements its stated bounded subcomponent; completing it is not a full-paper reproduction.




**Runnable component:** [Interpolate 2D Positional Embeddings](/problems/vit-position-interpolation). This resizes learned spatial positions with explicit bicubic settings and preserves the class row.


### Mix patch information

The original encoder uses pre-normalized residual blocks:

$$
U_\ell=Z_\ell+\operatorname{MSA}(\operatorname{LN}(Z_\ell)),
\qquad Z_{\ell+1}=U_\ell+\operatorname{MLP}(\operatorname{LN}(U_\ell)).
$$

Each attention head computes $\operatorname{softmax}(QK^\top/\sqrt{d_k})V$. The attention matrix is $(N+1)\times(N+1)$, so doubling both image dimensions at fixed patch size multiplies its element count by approximately sixteen. That resolution choice can dominate an edge robot’s memory budget.


**Planned component problems:** Assemble a Pre-Norm Vision Transformer Block; Profile Token Count, Memory, and Latency by Resolution. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

### Read out a representation

For the normalized final class token $h$, a linear classifier gives

$$
p(y=c\mid I)=\frac{\exp(w_c^\top h+b_c)}{\sum_j\exp(w_j^\top h+b_j)}.
$$

Changing image resolution changes the patch grid. When interpolating learned spatial position embeddings, reshape only the patch positions into a 2D grid, interpolate that grid, and keep the class-token embedding separate. A downstream robot policy may use all patch tokens rather than the classifier; that changes the output contract, not the patchification rules.




**Planned component problem:** Read a Normalized Class Token with a Linear Head. This is an unreviewed implementation idea for the mechanism above, not a runnable exercise; its precise contract and evaluator must be reviewed before publication.

## Implement the components

- **Runnable component:** [Build Learned Patch and Class Tokens](/problems/vit-patch-class-tokens). This is a bounded synthetic component, not a complete trained model.

- **Runnable component:** [Patchify and Reconstruct an Image Tensor](/problems/vit-patchify-reconstruct). This isolates one reviewed mechanism with synthetic fixtures; it does not reproduce the paper’s complete model or benchmark.

The component below is runnable. The other ideas remain planned and do not yet have published evaluators.

**Planned components:**

- Assemble a Pre-Norm Vision Transformer Block.
- Profile Token Count, Memory, and Latency by Resolution.
- Read a Normalized Class Token with a Linear Head.

[Browse the planned curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md). Planned titles require a reviewed contract and evaluator before becoming runnable.

## Why this matters on a robot

Patch size trades spatial precision for computation. Fine manipulations can depend on edges smaller than a patch, while higher-resolution attention increases latency. Preserve preprocessing and positional interpolation with the checkpoint, and benchmark the exact image resolution used by the robot.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2010.11929) · [Open-access manuscript](https://arxiv.org/pdf/2010.11929)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
