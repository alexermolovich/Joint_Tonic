---
schema_version: 1
paper_id: "2016-bundlefusion"
title: "BundleFusion: Real-time Globally Consistent 3D Reconstruction using On-the-fly Surface Re-integration"
authors: ["Dai, Angela","Nießner, Matthias","Zollhöfer, Michael","Izadi, Shahram","Theobalt, Christian"]
year: 2016
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/1604.01093"
pdf_url: "https://arxiv.org/pdf/1604.01093"
local_pdf: "./2016-bundlefusion.pdf"
sha256: "16a8b5e3b0f8dab1210b092ef60b31a4c075d62bf6af15bf2c8f4455c02aefe8"
bytes: 5927692
pages: 19
topics: ["geometry-calibration-slam","bundlefusion"]
modalities: ["camera","imu","lidar","poses"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Estimate frame alignment","detail":"Combine sparse matches and dense geometric/photometric constraints.","column":0,"row":0,"section":"Estimate frame alignment","problem_slugs":[],"planned_problems":["Assemble Sparse and Dense RGB-D Alignment Residuals"]},{"id":"stage-2","title":"Optimize global poses","detail":"Revisit trajectory consistency across matched frames.","column":1,"row":0,"section":"Optimize global poses","problem_slugs":[],"planned_problems":["Update a Global Pose Graph"]},{"id":"stage-3","title":"Reintegrate the surface","detail":"Remove old weighted contributions and insert corrected ones.","column":2,"row":0,"section":"Reintegrate the surface","problem_slugs":[],"planned_problems":["Integrate a Depth Frame into a TSDF","Reintegrate Geometry After a Pose Correction"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"frame constraints"},{"from":"stage-2","to":"stage-3","label":"corrected poses"}]}
---

## Core paper explanation

BundleFusion combines global RGB-D pose optimization with online surface reconstruction. When camera poses change, previously fused measurements are removed and reintegrated so the map reflects the corrected trajectory.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Estimate frame alignment

For a depth point $p$ in one camera frame and correspondence $q$ in another, a point-to-plane residual is
$$r=n_q^\top(Tp-q).$$
$T\in SE(3)$ maps source to target coordinates, $n_q$ is a unit target normal, and $r$ is in meters. Dense photometric and sparse feature terms provide complementary evidence.




**Planned component problem:** Assemble Sparse and Dense RGB-D Alignment Residuals. This is an unreviewed implementation idea for the mechanism above, not a runnable exercise; its precise contract and evaluator must be reviewed before publication.

### Optimize global poses

A schematic joint objective is $\min_{\{T_i\}}\lambda_sE_s+\lambda_gE_g+\lambda_pE_p$. Terms represent sparse correspondence, dense geometry, and photometry; their scales and robustification must follow the implementation. Global pose correction affects more than the latest frame.


**Planned component problems:** Update a Global Pose Graph. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

### Reintegrate the surface

For a TSDF voxel with value $D$ and weight $W$, integrating signed-distance sample $d$ with weight $w$ gives
$$D'=\frac{WD+wd}{W+w},\qquad W'=W+w.$$
Deintegration reverses stored contributions before reinserting them at corrected poses. Weight saturation and missing history complicate exact reversal; this equation is the unsaturated weighted-average core.


**Planned component problems:** Integrate a Depth Frame into a TSDF; Reintegrate Geometry After a Pose Correction. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

## Implement the components

- **Related implementation skill:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). This isolates a supporting mechanism, not this paper's complete method.

**Planned components:**

- Assemble Sparse and Dense RGB-D Alignment Residuals.
- Update a Global Pose Graph.
- Integrate a Depth Frame into a TSDF.
- Reintegrate Geometry After a Pose Correction.

[Browse the planned curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md). Planned titles require a reviewed contract and evaluator before becoming runnable.

## Why this matters on a robot

A globally corrected mesh avoids duplicated walls and warped surfaces. Dynamic objects, bad loop matches, and inconsistent reintegration can produce geometry that is visually plausible but unsafe for collision checking.

## Sources and scope

[Primary paper](https://arxiv.org/abs/1604.01093) · [Open-access manuscript](https://arxiv.org/pdf/1604.01093)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
