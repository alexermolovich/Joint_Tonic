---
schema_version: 1
paper_id: "2017-pointnet-plus-plus"
title: "PointNet++: Deep Hierarchical Feature Learning on Point Sets in a Metric Space"
authors: ["Qi, Charles R.","Yi, Li","Su, Hao","Guibas, Leonidas J."]
year: 2017
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/1706.02413"
pdf_url: "https://arxiv.org/pdf/1706.02413"
local_pdf: "./2017-pointnet-plus-plus.pdf"
sha256: "5cd120458cd481078aaf927f0bfed0ef646423e107f5cc2750b9c59f5b8e3795"
bytes: 4083329
pages: 14
topics: ["perception-3d","pointnet-plus-plus"]
modalities: ["rgb","depth","point-clouds"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Select centroids, group metric neighborhoods, and aggregate local features hierarchically; feature propagation supports point-wise outputs.","nodes":[{"id":"stage-1","title":"Sample representative centroids","detail":"Use farthest-point sampling to spread a bounded set of representatives.","column":0,"row":0,"section":"Sample representative centroids","problem_slugs":[],"planned_problems":["Implement farthest-point sampling"]},{"id":"stage-2","title":"Group local neighborhoods","detail":"Find nearby points and express their offsets relative to a centroid.","column":1,"row":0,"section":"Group local neighborhoods","problem_slugs":[],"planned_problems":["Perform bounded-radius neighborhood grouping"]},{"id":"stage-3","title":"Aggregate and propagate features","detail":"Pool shared local features, then interpolate coarser information when point-wise output is needed.","column":2,"row":0,"section":"Aggregate and propagate features","problem_slugs":[],"planned_problems":["Interpolate coarse features onto fine points"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"centroids"},{"from":"stage-2","to":"stage-3","label":"local point groups"}]}
---

## Core paper explanation

PointNet++ builds hierarchical point-cloud features by applying PointNet-style aggregation to local neighborhoods. It samples representative centroids, groups nearby points in metric space, and learns local features before repeating at a coarser scale. This introduces local spatial structure that a single global PointNet pooling operation does not explicitly capture.

## Execution flow

Select centroids, group metric neighborhoods, and aggregate local features hierarchically; feature propagation supports point-wise outputs.

### Sample representative centroids

For selected centroid set $S$, select the next point by

$$
x_{\mathrm{next}}=\arg\max_{x_i}\min_{s\in S}\|x_i-s\|_2.
$$

Distances are measured in the cloud’s coordinate units. Initialize deterministically for a reproducible exercise and specify tie order. Farthest-point sampling depends on geometry, so rescaling coordinates changes meaningful neighborhood radii even if the selected order is unchanged.


**Planned component problems:** Implement farthest-point sampling. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

### Group local neighborhoods

For centroid $c$ and radius $r>0$,

$$
\mathcal N_r(c)=\{i:\|x_i-c\|_2\le r\},
\qquad \Delta x_i=x_i-c.
$$

Ball queries differ from fixed-count nearest neighbors: they preserve a metric radius but yield variable neighborhood sizes. Define truncation, padding, and empty-neighborhood behavior. Multi-scale grouping combines information from several radii to improve robustness to density variation.


**Planned component problems:** Perform bounded-radius neighborhood grouping. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

### Aggregate and propagate features

A local set feature is $g_c=\max_{i\in\mathcal N_r(c)}h(\Delta x_i,f_i)$. A typical propagation step uses inverse-distance interpolation:

$$
\hat f(x)=\frac{\sum_{j\in\mathcal N_k(x)}w_jf_j}{\sum_jw_j},
\qquad w_j=\frac1{\|x-c_j\|_2^p}.
$$

Exact coincident points need an explicit rule instead of division by zero. Skip-connected fine features can supplement the interpolated coarse features. [SE(3) transforms](/problems/se3-transform-points) help ensure all grouped points share the intended frame.


**Planned component problems:** Interpolate coarse features onto fine points. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

## Implement the components

- **Related implementation skill:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). This isolates a supporting mechanism, not this paper's complete method.

**Planned components:**

- Implement farthest-point sampling.
- Perform bounded-radius neighborhood grouping.
- Interpolate coarse features onto fine points.

[Browse the planned curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md). Planned titles require a reviewed contract and evaluator before becoming runnable.

## Why this matters on a robot

Depth sensors produce nonuniform point density, missing returns, and range-dependent noise. Neighborhood radii encode a physical scale, so a meters-versus-millimeters mismatch can collapse local structure. Test sparse and occluded regions alongside uniformly sampled synthetic clouds.

## Sources and scope

[Primary paper](https://arxiv.org/abs/1706.02413) · [Open-access manuscript](https://arxiv.org/pdf/1706.02413)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
