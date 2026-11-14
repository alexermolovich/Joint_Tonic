---
schema_version: 1
paper_id: "2022-bevformer"
title: "BEVFormer: Learning Bird's-Eye-View Representation from Multi-Camera Images via Spatiotemporal Transformers"
authors: ["Zhiqi Li", "Wenhai Wang", "Hongyang Li", "Enze Xie", "Chonghao Sima", "Tong Lu", "Qiao Yu", "Jifeng Dai"]
year: 2022
venue_or_status: "ECCV 2022"
primary_url: "https://arxiv.org/abs/2203.17270"
pdf_url: "https://arxiv.org/pdf/2203.17270"
local_pdf: "./2022-bevformer.pdf"
sha256: "641561d0e4c1d46d6883a3d38c68b475030de5bbbcdf747af268366f47f97a6b"
bytes: 4739748
pages: 20
topics: ["bird's-eye view", "multi-camera perception", "3D detection", "temporal fusion", "autonomous driving"]
modalities: ["synchronized multi-camera RGB", "camera calibration", "ego motion"]
track_role: "Multi-view and temporal perception for autonomy"
open_access_status: "Open-access arXiv manuscript"
redistribution_note: "Retain the original attribution and license metadata; verify source terms before redistributing outside this research workspace."
execution_flow: {"title":"Core execution flow","description":"Create ego-frame reference points, gather visible multi-camera features, and fuse aligned temporal state before task-specific prediction.","nodes":[{"id":"stage-1","title":"Project BEV reference points","detail":"Use extrinsics and intrinsics to find where a 3D reference point is visible.","column":0,"row":0,"section":"Project BEV reference points","problem_slugs":["se3-transform-points","project-camera-points","bev-project-reference-points","bev-visibility-mask","bev-camera-health-diagnostics"],"planned_problems":[]},{"id":"stage-2","title":"Gather camera evidence","detail":"Sample features around projected references in the cameras that can see them.","column":1,"row":0,"section":"Gather camera evidence","problem_slugs":["bev-weighted-camera-features"],"planned_problems":["Sample Calibrated Multi-Camera Feature Maps"]},{"id":"stage-3","title":"Fuse temporal BEV state","detail":"Align earlier BEV features to the current ego frame and combine them with current evidence.","column":2,"row":0,"section":"Fuse temporal BEV state","problem_slugs":["bev-ego-motion-warp","bev-temporal-fusion"],"planned_problems":[]}],"edges":[{"from":"stage-1","to":"stage-2","label":"visible projections"},{"from":"stage-2","to":"stage-3","label":"camera features"}]}
---

## Core paper explanation

BEVFormer builds a bird’s-eye-view representation from multiple calibrated cameras and previous BEV features. Each BEV query corresponds to a location in an ego-centered spatial grid. Spatial cross-attention gathers image evidence near projected 3D reference points, while temporal attention incorporates aligned history. The result supports tasks such as 3D detection and map segmentation in a shared spatial representation.

## Execution flow

Create ego-frame reference points, gather visible multi-camera features, and fuse aligned temporal state before task-specific prediction.

### Project BEV reference points

For homogeneous ego-frame point $\tilde p_e\in\mathbb R^4$, camera transform $T_{c\leftarrow e}\in\mathbb R^{4\times4}$, and intrinsics $K_c\in\mathbb R^{3\times3}$,

$$
\tilde q_c=K_c[I_3\;0]T_{c\leftarrow e}\tilde p_e,
\quad u_c=\tilde q_{c,x}/\tilde q_{c,z},\quad v_c=\tilde q_{c,y}/\tilde q_{c,z}.
$$

The $[I_3\;0]$ factor selects the 3D camera coordinates, making matrix dimensions explicit. Check positive camera depth and image bounds. [SE(3) transforms](/problems/se3-transform-points) and [camera projection](/problems/project-camera-points) implement these prerequisite mechanisms with declared frame conventions.


**Implement this component:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points) · [Project Camera Points into Pixels](/problems/project-camera-points). These are the transform and pinhole-projection substeps. They do not implement BEV reference-grid generation or the complete multi-camera projection contract.

**Implement these components:** [Project BEV Reference Points into Calibrated Cameras](/problems/bev-project-reference-points) · [Mask Out-of-View and Behind-Camera Samples](/problems/bev-visibility-mask) · [Diagnose Camera Dropout and Calibration Drift in BEV](/problems/bev-camera-health-diagnostics). Each exercise specifies its bounded scope; diagnostic and simplified variants do not reproduce the full model.

### Gather camera evidence

A compact description of deformable spatial sampling for query $q$ is

$$
f_q=\sum_{c\in\mathcal V_q}\sum_k a_{qck}\,\mathcal B(F_c,p_{qc}+\Delta p_{qck}),
$$

where $\mathcal V_q$ is its visible-camera set, $F_c$ is a camera feature map, $\mathcal B$ denotes bilinear sampling, and learned offsets/weights choose nearby evidence. This expression suppresses multi-head and height-anchor indices for clarity. Pixel coordinates must be converted to feature-map coordinates consistently; an incorrect scale can sample a plausible but unrelated location.



**New runnable component:** [Aggregate Multi-Camera Features with Attention Weights](/problems/bev-weighted-camera-features). This is an explicitly simplified visibility-masked global weighted mean, not the full BEVFormer attention block.

**Planned components:** Sample Calibrated Multi-Camera Feature Maps. These remain unreviewed ideas without runnable exercises.

### Fuse temporal BEV state

A previous grid location must be transformed using ego motion before temporal lookup. For a planar grid transform $T_{t\leftarrow t-1}$,

$$
\tilde p_t=T_{t\leftarrow t-1}\tilde p_{t-1}.
$$

The aligned history and current queries then participate in temporal attention. Ego-motion alignment compensates camera/vehicle motion, not independently moving objects; learned temporal processing still has to interpret those changes. Reset history at sequence boundaries and define behavior when a previous frame is missing.


**Implement these components:** [Fuse Temporal BEV State](/problems/bev-temporal-fusion). Each exercise specifies its bounded scope; diagnostic and simplified variants do not reproduce the full model.


**Runnable component:** [Warp a Previous BEV with Ego Motion](/problems/bev-ego-motion-warp). This aligns a planar feature grid with explicit cell centers and zero-padded bilinear sampling; temporal attention and moving-object compensation remain separate.

#### Implement a bounded temporal state interface

[Fuse temporal BEV state](/problems/bev-temporal-fusion) is explicitly a deterministic gated teaching substitute for learned temporal attention. At each aligned grid cell, let $x,h\in\mathbb R^D$ be current/history feature vectors, $g\in[0,1]$ a supplied history weight, $v\in\{0,1\}$ history validity and $r\in\{0,1\}$ sequence reset:
$$a=g v(1-r),\qquad y=(1-a)x+ah.$$
Features and weights are dimensionless. Invalid history or reset forces $a=0$, preserving current evidence. The [ego-motion warp](/problems/bev-ego-motion-warp) must already align history; this formula does not compensate moving objects.

[Multi-camera projection](/problems/bev-project-reference-points) and [visibility masking](/problems/bev-visibility-mask) now implement the full stated bounded projection interface, beyond their SE(3)/pinhole prerequisites. [Camera health diagnostics](/problems/bev-camera-health-diagnostics) separates reception dropout from reprojection residuals, retaining an explicit no-evidence flag rather than interpreting missing frames as accurate calibration.


## Implement the components

The following bounded exercises are runnable. They use original synthetic fixtures; completing them does not reproduce the paper's training scale or headline benchmark. Systems diagnostics are explicitly identified as teaching contracts.

- [Aggregate Multi-Camera Features with Attention Weights](/problems/bev-weighted-camera-features) — Easy.
- [Warp a Previous BEV with Ego Motion](/problems/bev-ego-motion-warp) — Hard.
- [Project BEV Reference Points into Calibrated Cameras](/problems/bev-project-reference-points) — Medium.
- [Mask Out-of-View and Behind-Camera Samples](/problems/bev-visibility-mask) — Easy.
- [Fuse Temporal BEV State](/problems/bev-temporal-fusion) — Medium.
- [Diagnose Camera Dropout and Calibration Drift in BEV](/problems/bev-camera-health-diagnostics) — Medium.

**Further ideas outside the approved runnable scope:**

- Sample Calibrated Multi-Camera Feature Maps.

## Why this matters on a robot

Calibration and timing errors can look like genuine object motion in BEV space. A model may fuse sharp image features into a geometrically wrong map if frame direction, camera latency, or resize intrinsics are incorrect. Validate projection and temporal alignment before debugging the attention weights.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2203.17270) · [Open-access manuscript](https://arxiv.org/pdf/2203.17270)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
