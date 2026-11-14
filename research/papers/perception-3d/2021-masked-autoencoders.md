---
{
  "schema_version": 1,
  "paper_id": "2021-masked-autoencoders",
  "title": "Masked Autoencoders Are Scalable Vision Learners",
  "authors": [
    "Kaiming He",
    "Xinlei Chen",
    "Saining Xie",
    "Yanghao Li",
    "Piotr Dollár",
    "Ross Girshick"
  ],
  "year": 2021,
  "venue_or_status": "CVPR2022; arXiv2021 v3",
  "primary_url": "https://arxiv.org/abs/2111.06377",
  "pdf_url": "https://arxiv.org/pdf/2111.06377v3",
  "local_pdf": "./2021-masked-autoencoders.pdf",
  "sha256": "1b490443925c72a2b7c770f90dd797e248729ae34a57e1abfe9ed36751c4cc5b",
  "bytes": 7445748,
  "pages": 14,
  "topics": [
    "masked image modeling",
    "vision transformer",
    "self-supervised learning"
  ],
  "modalities": [
    "RGB image patches"
  ],
  "track_role": "supporting",
  "open_access_status": "open-access-preprint",
  "redistribution_note": "Local research reference only. Open-access source verified; downstream redistribution rights have not been audited. The PDF is not a public product asset.",
  "acquired_on": "2026-11-13",
  "source_verification": "Primary title/authors and version checked; PDF signature, all-page parser readability, first-page visual render, count and SHA-256 validated.",
  "execution_flow": {
    "title": "Selected mechanism and implementation path",
    "description": "Self-supervised image representation learning with an encoder that processes visible patches and a smaller decoder that reconstructs masked patches.",
    "nodes": [
      {
        "id": "select",
        "title": "Select visible patches",
        "detail": "Select visible patches. See the original explanation and component status below.",
        "column": 0,
        "row": 0,
        "section": "Select visible patches",
        "problem_slugs": [
          "vit-patchify-reconstruct"
        ],
        "planned_problems": [
          "Sample and Restore Masked Image Patches"
        ]
      },
      {
        "id": "encode",
        "title": "Encode visible tokens",
        "detail": "Encode visible tokens. See the original explanation and component status below.",
        "column": 1,
        "row": 0,
        "section": "Encode visible tokens",
        "problem_slugs": [
          "vit-patch-class-tokens"
        ],
        "planned_problems": [
          "Gather Visible Patch Tokens with Position Indices"
        ]
      },
      {
        "id": "reconstruct",
        "title": "Reconstruct masked pixels",
        "detail": "Reconstruct masked pixels. See the original explanation and component status below.",
        "column": 2,
        "row": 0,
        "section": "Reconstruct masked pixels",
        "problem_slugs": [],
        "planned_problems": [
          "Compute a Masked Patch Reconstruction Loss"
        ]
      }
    ],
    "edges": [
      {
        "from": "select",
        "to": "encode",
        "label": "validated component output"
      },
      {
        "from": "encode",
        "to": "reconstruct",
        "label": "validated component output"
      }
    ]
  }
}
---

## Core paper explanation

A masked autoencoder learns visual structure by predicting missing image content. Its expensive encoder processes only visible patches; mask tokens are introduced for decoding. The reconstruction task is a pretraining signal, not a guarantee of object detection, depth estimation or robust robot control.

## Execution flow

### Select visible patches

For an image split into N patches with F pixel scalars each, write $X\in\mathbb R^{N\times F}$. A sampled permutation $\pi$ selects visible index set V and masked set M. At mask fraction r, a declared implementation may retain $\lfloor(1-r)N\rfloor$ patches; rounding must be part of its contract.

$$
X_{\mathrm{vis}}=X[\pi_{0:|V|}],\qquad |V|+|M|=N.
$$

Patch values are normalized image intensities; index order is image-grid order, not a metric robot frame. [Patchify and Reconstruct an Image Tensor](/problems/vit-patchify-reconstruct) is the implemented layout prerequisite. **Sample and Restore Masked Image Patches** is a planned component.

### Encode visible tokens

Project visible patches and add their corresponding positional embeddings before the encoder:

$$
Z_{\mathrm{vis}}=f_\theta(X_{\mathrm{vis}}W+P[V]).
$$

$W\in\mathbb R^{F\times E}$ maps patch width into encoder width E; $P\in\mathbb R^{N\times E}$ identifies original positions. Removing a patch must not relabel the remaining spatial positions. The encoder sees no mask-token placeholders for missing patches.

[Build Learned Patch and Class Tokens](/problems/vit-patch-class-tokens) supplies a related token-assembly component. **Gather Visible Patch Tokens with Position Indices** remains planned. Class-token handling and decoder width must follow the eventual blueprint rather than being inferred from this compact notation.

### Reconstruct masked pixels

The decoder receives encoded visible tokens together with mask tokens and restores original patch order. Let $\widehat X_i$ predict patch i. A masked-only squared objective is

$$
L=\frac{1}{|M|F}\sum_{i\in M}\|\widehat X_i-X_i\|_2^2.
$$

This equation defines an illustrative scalar-mean reduction. The paper also studies targets normalized within each patch; its normalization and variance convention must be pinned before implementing that variant. **Compute a Masked Patch Reconstruction Loss** is a planned component.

| Patch index | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| Visible to encoder | Yes | No | Yes | No |
| Decoder input | Encoded0 | Mask | Encoded2 | Mask |
| Reconstruction loss | Excluded | Included | Excluded | Included |

With two masked patches containing scalar target/prediction pairs(2,1) and(4,6), squared errors are1 and4; the scalar mean is2.5. The table is an original pipeline trace, not a paper figure.

## Why this matters on a robot

The method can use unlabeled camera logs for representation learning. Mask restoration errors can train predictions against the wrong pixels while preserving every tensor shape. Dataset splits must also prevent nearby video frames from leaking across train and validation sets. Track crop, patch, normalization and mask-seed versions.

## Implement the components

Two layout/token prerequisites are runnable; masking/restoration and reconstruction-loss tasks are candidates awaiting blueprint review. No pretrained weights, original training images or headline accuracy are reproduced here.


## Sources and scope

[Canonical primary record](https://arxiv.org/abs/2111.06377) · [Pinned openly accessible manuscript](https://arxiv.org/pdf/2111.06377v3). This is an original selected-mechanism explanation, not a full-text transcription. Linked exercises are identified as direct components or supporting prerequisites. Planned node titles are research/curriculum ideas, not published problems; new ideas require a reviewed blueprint before implementation. PDF provenance and reuse status are recorded above.
