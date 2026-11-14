---
schema_version: 1
paper_id: 2017-superpoint
title: 'SuperPoint: Self-Supervised Interest Point Detection and Description'
authors:
  - 'DeTone, Daniel'
  - 'Malisiewicz, Tomasz'
  - 'Rabinovich, Andrew'
year: 2017
venue_or_status: >-
  Author-deposited arXiv manuscript; final venue not asserted by this
  acquisition card.
primary_url: 'https://arxiv.org/abs/1712.07629'
pdf_url: 'https://arxiv.org/pdf/1712.07629'
local_pdf: ./2017-superpoint.pdf
sha256: 69ec3dfaab5d6b6a4f6b21379c47d657b8889150811637684a39a487c813be62
bytes: 9866310
pages: 13
topics:
  - geometry-calibration-slam
  - superpoint
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
      title: Adapt point detections
      detail: Aggregate detections across synthetic homographies.
      column: 0
      row: 0
      section: Adapt point detections
      problem_slugs:
        - homographic-keypoint-adaptation
        - keypoint-repeatability
      planned_problems: []
    - id: stage-2
      title: Supervise descriptors
      detail: Use known geometric correspondence to separate matches and nonmatches.
      column: 1
      row: 0
      section: Supervise descriptors
      problem_slugs:
        - homography-descriptor-targets
      planned_problems: []
    - id: stage-3
      title: Extract usable features
      detail: Suppress nearby peaks and sample normalized descriptors.
      column: 2
      row: 0
      section: Extract usable features
      problem_slugs:
        - sample-keypoint-descriptors
      planned_problems: []
  edges:
    - from: stage-1
      to: stage-2
      label: adapted keypoints
    - from: stage-2
      to: stage-3
      label: detector and descriptor maps
---

## Core paper explanation

SuperPoint jointly predicts interest points and local descriptors. Synthetic corner training and homographic adaptation create self-supervised detection targets on real images, while known image warps supervise descriptor correspondence.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Adapt point detections

For detector $f$ and image homographies $H_k$, a teaching form of homographic adaptation is
$$\bar f(I)=\frac1K\sum_k H_k^{-1}f(H_k I).$$
Inverse warping returns detections to the original image; valid-pixel counts are needed near warped boundaries. Homographies describe planar/projective image warps, not arbitrary 3D scene motion.


**Implement these components:** [Apply Homographic Keypoint Adaptation](/problems/homographic-keypoint-adaptation) · [Evaluate Keypoint Repeatability](/problems/keypoint-repeatability). Each exercise states its bounded numerical contract; completing these components does not reproduce the complete trained model.

### Supervise descriptors

For normalized descriptors $d,d'$, a hinge-style pair loss is
$$\ell=s\max(0,m_+-d^\top d')+(1-s)\max(0,d^\top d'-m_-).$$
$s\in\{0,1\}$ marks a homography-consistent pair; $m_+,m_-$ are margins. The paper balances positive and negative terms and uses cell-level correspondence rules.




**Implement these components:** [Build Homography-Supervised Descriptor Correspondence Targets](/problems/homography-descriptor-targets). Each exercise states its bounded numerical contract; completing these components does not reproduce the complete trained model.

### Extract usable features

At inference, apply confidence filtering and nonmaximum suppression, then interpolate descriptors at retained keypoints and normalize them. Detector coordinates and descriptor-grid coordinates use different resolutions; their scale/offset mapping must be explicit. The linked exercise uses a declared bilinear teaching variant; the paper reports bicubic interpolation. Its validity mask describes grid support separately from a zero descriptor norm.


**Implement these components:** [Sample Descriptors at Keypoint Coordinates](/problems/sample-keypoint-descriptors). Each exercise states its bounded numerical contract; completing these components does not reproduce the complete trained model.

## Implement the components

The linked atomic components are implemented with synthetic fixtures, explicit numerical contracts and reviewed evaluators. Full training, benchmark reproduction and model integration remain outside these exercises.

**Runnable components:**

- [Apply Homographic Keypoint Adaptation](/problems/homographic-keypoint-adaptation) — runnable bounded component.
- [Evaluate Keypoint Repeatability](/problems/keypoint-repeatability) — runnable bounded component.
- [Build Homography-Supervised Descriptor Correspondence Targets](/problems/homography-descriptor-targets) — runnable bounded component.
- [Sample Descriptors at Keypoint Coordinates](/problems/sample-keypoint-descriptors) — runnable bounded component.

[Browse the curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md).

## Why this matters on a robot

Repeatable local features support camera tracking and calibration. Textureless surfaces and viewpoint changes outside the homography training distribution can still defeat matching; point count alone does not measure geometric utility.

## Sources and scope

[Primary paper](https://arxiv.org/abs/1712.07629) · [Open-access manuscript](https://arxiv.org/pdf/1712.07629)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
