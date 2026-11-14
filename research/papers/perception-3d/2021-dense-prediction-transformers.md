---
schema_version: 1
paper_id: "2021-dense-prediction-transformers"
title: "Vision Transformers for Dense Prediction"
authors: ["Ranftl, René","Bochkovskiy, Alexey","Koltun, Vladlen"]
year: 2021
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2103.13413"
pdf_url: "https://arxiv.org/pdf/2103.13413"
local_pdf: "./2021-dense-prediction-transformers.pdf"
sha256: "ecd8826047fcd4e5e36ead0e1eb72e884c2e0a01cf62f01d247473d91beeb403"
bytes: 10253725
pages: 15
topics: ["perception-3d","dense-prediction-transformers"]
modalities: ["rgb","depth","point-clouds"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Extract intermediate image tokens, reassemble spatial maps, and fuse them into a dense prediction.","nodes":[{"id":"stage-1","title":"Extract intermediate tokens","detail":"Retain several backbone depths rather than only a final classifier token.","column":0,"row":0,"section":"Extract intermediate tokens","problem_slugs":[],"planned_problems":["Collect Intermediate Transformer Tokens with Patch-Grid Metadata"]},{"id":"stage-2","title":"Reassemble and fuse maps","detail":"Project token channels, reshape the patch grid, and create multiple spatial scales.","column":1,"row":0,"section":"Reassemble and fuse maps","problem_slugs":[],"planned_problems":["Reassemble tokens into feature maps","Fuse multi-resolution dense features"]},{"id":"stage-3","title":"Evaluate dense outputs","detail":"Choose metrics that match the output semantics, especially relative versus metric depth.","column":2,"row":0,"section":"Evaluate dense outputs","problem_slugs":[],"planned_problems":["Compare aligned and metric depth errors"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"intermediate tokens"},{"from":"stage-2","to":"stage-3","label":"fused features"}]}
---

## Core paper explanation

Dense Prediction Transformers adapt transformer image features to pixel-wise tasks such as depth and segmentation. Intermediate transformer tokens are reassembled into spatial feature maps at several resolutions, then fused by a dense decoder. This bridges global-context token processing with outputs that must remain aligned to individual image locations.

## Execution flow

Extract intermediate image tokens, reassemble spatial maps, and fuse them into a dense prediction.

### Extract intermediate tokens

For patch grid $h\times w$ and feature width $d$, an intermediate token sequence has $hw$ spatial entries plus any readout token. A readout-processing operator combines or removes the global token before spatial reconstruction:

$$
Z_\ell=\operatorname{Readout}(T_\ell)\in\mathbb R^{hw\times d_\ell}.
$$

Patch order must be preserved. Treating the readout token as one extra image patch shifts every subsequent location.




**Planned component problem:** Collect Intermediate Transformer Tokens with Patch-Grid Metadata. This is an unreviewed implementation idea for the mechanism above, not a runnable exercise; its precise contract and evaluator must be reviewed before publication.

### Reassemble and fuse maps

A reassembly operator can be written

$$
F_\ell=\operatorname{Resample}_\ell
\left(\operatorname{Reshape}_{h,w}(Z_\ell W_\ell)\right).
$$

The decoder progressively fuses these maps through residual convolutional processing and resampling. Target shapes, interpolation conventions, and padding must be consistent across levels. Global context does not remove the need for correct pixel alignment.


**Planned component problems:** Reassemble tokens into feature maps; Fuse multi-resolution dense features. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

### Evaluate dense outputs

For a relative-depth predictor, scale/shift ambiguity can be analyzed with a teaching alignment objective

$$
(s^*,t^*)=\arg\min_{s,t}\sum_{i\in\Omega}(s\hat d_i+t-d_i)^2.
$$

$\Omega$ is the valid-pixel set; $d$ must use the same depth or inverse-depth convention as $\hat d$. This least-squares alignment is a diagnostic, not a substitute for the exact training loss of every DPT configuration. A metric-depth application must evaluate unaligned physical accuracy as well.


**Planned component problems:** Compare aligned and metric depth errors. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

## Implement the components

The stage-specific implementation ideas above are not runnable yet. A reviewed blueprint and evaluator are required before publication.

**Planned components:**

- Collect Intermediate Transformer Tokens with Patch-Grid Metadata.
- Reassemble tokens into feature maps.
- Fuse multi-resolution dense features.
- Compare aligned and metric depth errors.

[Browse the planned curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md). Planned titles require a reviewed contract and evaluator before becoming runnable.

## Why this matters on a robot

A visually sharp relative-depth map can still have the wrong metric scale for navigation or grasping. Preserve camera preprocessing and output interpretation, and distinguish edge quality from absolute range accuracy. Missing depth targets require masks, not zero-valued supervision.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2103.13413) · [Open-access manuscript](https://arxiv.org/pdf/2103.13413)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
