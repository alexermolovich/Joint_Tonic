---
schema_version: 1
paper_id: "2017-superpoint"
title: "SuperPoint: Self-Supervised Interest Point Detection and Description"
authors: ["DeTone, Daniel","Malisiewicz, Tomasz","Rabinovich, Andrew"]
year: 2017
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/1712.07629"
pdf_url: "https://arxiv.org/pdf/1712.07629"
local_pdf: "./2017-superpoint.pdf"
sha256: "69ec3dfaab5d6b6a4f6b21379c47d657b8889150811637684a39a487c813be62"
bytes: 9866310
pages: 13
topics: ["geometry-calibration-slam","superpoint"]
modalities: ["camera","imu","lidar","poses"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
---

# SuperPoint: Self-Supervised Interest Point Detection and Description

## Agent brief

Study self-supervised interest-point detection and description through geometric consistency. This acquisition card verifies the primary paper identity and local PDF, and proposes components that can become independently testable Joint Tonic problems. Full-text technical review is required before promoting an idea into a reviewed problem blueprint.

## Contribution

Study self-supervised interest-point detection and description through geometric consistency.

The proposed exercises below are original teaching decompositions. They do not assert a full reproduction of the paper or any published performance number.

## Prerequisite concepts

- SE(3)/SO(3), camera projection, least-squares residuals, covariance, timestamp alignment, and geometric matching.

## Method map

| Component candidate | Input | Output | Core invariant | Good exercise boundary |
|---|---|---|---|---|
| Apply Homographic Keypoint Adaptation | Calibrated measurements, feature matches, sensor timestamps, poses, and uncertainty models | Residuals, correspondences, pose constraints, maps, or trajectory errors | Check frame direction, meters/radians, degenerate geometry, invalid depth, covariance symmetry, and numerical residual/Jacobian agreement. | One bounded function or validation stage |
| Sample Descriptors at Keypoint Coordinates | Calibrated measurements, feature matches, sensor timestamps, poses, and uncertainty models | Residuals, correspondences, pose constraints, maps, or trajectory errors | Check frame direction, meters/radians, degenerate geometry, invalid depth, covariance symmetry, and numerical residual/Jacobian agreement. | One bounded function or validation stage |
| Evaluate Keypoint Repeatability | Calibrated measurements, feature matches, sensor timestamps, poses, and uncertainty models | Residuals, correspondences, pose constraints, maps, or trajectory errors | Check frame direction, meters/radians, degenerate geometry, invalid depth, covariance symmetry, and numerical residual/Jacobian agreement. | One bounded function or validation stage |

## Data and evaluation

A small teaching implementation should use synthetic or separately licensed fixtures. Check frame direction, meters/radians, degenerate geometry, invalid depth, covariance symmetry, and numerical residual/Jacobian agreement. Dataset names, exact protocol details, published metrics, and hardware requirements must be checked in the source PDF during full-text review; they are not inferred from an awesome-list entry. Keep educational component tests distinct from the paper's end-to-end evaluation.

## Limitations and failure modes

- This is a concise acquisition card, not a full-text technical review. Confirm equations, architecture details, and paper-stated limitations in the PDF before authoring theory.
- Passing synthetic component tests does not establish real-robot performance, robustness, or safe deployment.
- Version calibration and sensor timing with logs; monitor residuals, inlier ratio, drift, relocalization, and compute latency across scene/motion conditions.
- The paper, linked code, datasets, assets, and weights may carry different license conditions.

## Implementation decomposition

1. Apply Homographic Keypoint Adaptation.
2. Sample Descriptors at Keypoint Coordinates.
3. Evaluate Keypoint Repeatability.
4. Integrate the components on a small fixed fixture and record all deviations from the paper.
5. Add failure slices and a reproducible artifact report.

## Problem blueprints

### Problem: Apply Homographic Keypoint Adaptation

- **Type:** component
- **Difficulty:** medium
- **Learning objective:** Implement and explain the apply homographic keypoint adaptation component.
- **Inputs:** Calibrated measurements, feature matches, sensor timestamps, poses, and uncertainty models; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Residuals, correspondences, pose constraints, maps, or trajectory errors; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check frame direction, meters/radians, degenerate geometry, invalid depth, covariance symmetry, and numerical residual/Jacobian agreement. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Sample Descriptors at Keypoint Coordinates

- **Type:** component
- **Difficulty:** hard
- **Learning objective:** Implement and explain the sample descriptors at keypoint coordinates component.
- **Inputs:** Calibrated measurements, feature matches, sensor timestamps, poses, and uncertainty models; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Residuals, correspondences, pose constraints, maps, or trajectory errors; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check frame direction, meters/radians, degenerate geometry, invalid depth, covariance symmetry, and numerical residual/Jacobian agreement. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Evaluate Keypoint Repeatability

- **Type:** pipeline
- **Difficulty:** hard
- **Learning objective:** Implement and explain the evaluate keypoint repeatability component.
- **Inputs:** Calibrated measurements, feature matches, sensor timestamps, poses, and uncertainty models; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Residuals, correspondences, pose constraints, maps, or trajectory errors; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check frame direction, meters/radians, degenerate geometry, invalid depth, covariance symmetry, and numerical residual/Jacobian agreement. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

## Visual teaching plan

- Show corresponding keypoints across a homography-transformed image pair.
- Provide labeled axes, units, coordinate frames, and an equivalent table/text view. Use discrete steps when reduced motion is requested.
- Author diagrams independently; do not copy paper figures or captions.

## MLOps and deployment extensions

- Version calibration and sensor timing with logs; monitor residuals, inlier ratio, drift, relocalization, and compute latency across scene/motion conditions.
- Store paper ID, fixture hash, evaluator version, dependency lock, runtime digest, seed, and resource class with every result.
- Use structured failure reasons and per-slice metrics to distinguish implementation mistakes, distribution shifts, and infrastructure failures.

## Canonical sources

- [Primary arXiv record](https://arxiv.org/abs/1712.07629)
- [Open-access author manuscript](https://arxiv.org/pdf/1712.07629)

Identity metadata was read from the primary arXiv record. Local file signature, byte count, page parsing, and SHA-256 were verified on acquisition.

