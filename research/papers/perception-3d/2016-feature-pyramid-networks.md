---
schema_version: 1
paper_id: "2016-feature-pyramid-networks"
title: "Feature Pyramid Networks for Object Detection"
authors: ["Lin, Tsung-Yi","Dollár, Piotr","Girshick, Ross","He, Kaiming","Hariharan, Bharath","Belongie, Serge"]
year: 2016
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/1612.03144"
pdf_url: "https://arxiv.org/pdf/1612.03144"
local_pdf: "./2016-feature-pyramid-networks.pdf"
sha256: "3a33e7ad38c17037624defde57f380f49dee918c1c14abd5dbcad032bae91428"
bytes: 789142
pages: 10
topics: ["perception-3d","feature-pyramid-networks"]
modalities: ["rgb","depth","point-clouds"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Read backbone levels, fuse coarse semantics into finer maps, and choose the appropriate pyramid representation for each detection region.","nodes":[{"id":"stage-1","title":"Project backbone levels","detail":"Give different-resolution backbone maps a shared feature width.","column":0,"row":0,"section":"Project backbone levels","problem_slugs":[],"planned_problems":["Project Multi-Scale Backbone Maps to a Shared Channel Width"]},{"id":"stage-2","title":"Fuse top-down features","detail":"Add upsampled coarse features to a corresponding lateral map.","column":1,"row":0,"section":"Fuse top-down features","problem_slugs":[],"planned_problems":["Fuse lateral and top-down maps","Verify odd-resolution shape alignment"]},{"id":"stage-3","title":"Assign region scale","detail":"Choose a feature level according to the region’s image-space size.","column":2,"row":0,"section":"Assign region scale","problem_slugs":[],"planned_problems":["Assign regions to pyramid levels"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"lateral maps"},{"from":"stage-2","to":"stage-3","label":"feature pyramid"}]}
---

## Core paper explanation

Feature Pyramid Networks combine high-level semantic features with higher-resolution spatial features. A top-down pathway upsamples coarse representations and joins them with lateral projections from the backbone. The result provides semantically useful feature maps at several scales without computing separate image pyramids for every input.

## Execution flow

Read backbone levels, fuse coarse semantics into finer maps, and choose the appropriate pyramid representation for each detection region.

### Project backbone levels

Let backbone level $C_\ell\in\mathbb R^{H_\ell\times W_\ell\times d_\ell}$. A lateral1×1convolution creates $L_\ell$ with common width $d$:

$$
L_\ell=\operatorname{Conv}_{1\times1}(C_\ell)\in\mathbb R^{H_\ell\times W_\ell\times d}.
$$

Equal channel width makes addition possible. It does not guarantee spatial alignment when inputs have odd dimensions or a different padding convention.




**Planned component problem:** Project Multi-Scale Backbone Maps to a Shared Channel Width. This is an unreviewed implementation idea for the mechanism above, not a runnable exercise; its precise contract and evaluator must be reviewed before publication.

### Fuse top-down features

A simplified top-down recurrence is

$$
P_\ell=\operatorname{Conv}_{3\times3}\left(L_\ell+
\operatorname{Upsample}(P_{\ell+1};H_\ell,W_\ell)\right).
$$

The explicit target shape avoids relying on a scale factor that can be wrong by one pixel. The3×3convolution reduces artifacts introduced by upsampling/fusion. Backpropagation reaches both the lateral and top-down paths.


**Planned component problems:** Fuse lateral and top-down maps; Verify odd-resolution shape alignment. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

### Assign region scale

The paper’s region assignment uses a logarithmic scale rule of the form

$$
k=\left\lfloor k_0+\log_2\left(\frac{\sqrt{wh}}{224}\right)\right\rfloor,
$$

where $w,h$ are region dimensions in pixels and the canonical level is $k_0=4$. Clamp to available levels. Doubling both region dimensions moves the assignment up one pyramid level. This rule uses image-space geometry; a physical object’s size in meters is not directly substituted.


**Planned component problems:** Assign regions to pyramid levels. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

## Implement the components

The stage-specific implementation ideas above are not runnable yet. A reviewed blueprint and evaluator are required before publication.

**Planned components:**

- Project Multi-Scale Backbone Maps to a Shared Channel Width.
- Fuse lateral and top-down maps.
- Verify odd-resolution shape alignment.
- Assign regions to pyramid levels.

[Browse the planned curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md). Planned titles require a reviewed contract and evaluator before becoming runnable.

## Why this matters on a robot

A feature pyramid helps a single image representation cover distant and nearby objects. Incorrect level assignment or one-pixel alignment errors can affect small-object localization disproportionately. Test odd image dimensions and bounding boxes near scale boundaries.

## Sources and scope

[Primary paper](https://arxiv.org/abs/1612.03144) · [Open-access manuscript](https://arxiv.org/pdf/1612.03144)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
