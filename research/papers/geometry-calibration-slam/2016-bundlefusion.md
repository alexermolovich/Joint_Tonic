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
---

# BundleFusion: Real-time Globally Consistent 3D Reconstruction using On-the-fly Surface Re-integration

## Agent brief

Study dense reconstruction with online global pose optimization and surface integration. This acquisition card verifies the primary paper identity and local PDF, and proposes components that can become independently testable Joint Tonic problems. Full-text technical review is required before promoting an idea into a reviewed problem blueprint.

## Contribution

Study dense reconstruction with online global pose optimization and surface integration.

The proposed exercises below are original teaching decompositions. They do not assert a full reproduction of the paper or any published performance number.

## Prerequisite concepts

- SE(3)/SO(3), camera projection, least-squares residuals, covariance, timestamp alignment, and geometric matching.

## Method map

| Component candidate | Input | Output | Core invariant | Good exercise boundary |
|---|---|---|---|---|
| Integrate a Depth Frame into a TSDF | Calibrated measurements, feature matches, sensor timestamps, poses, and uncertainty models | Residuals, correspondences, pose constraints, maps, or trajectory errors | Check frame direction, meters/radians, degenerate geometry, invalid depth, covariance symmetry, and numerical residual/Jacobian agreement. | One bounded function or validation stage |
| Update a Global Pose Graph | Calibrated measurements, feature matches, sensor timestamps, poses, and uncertainty models | Residuals, correspondences, pose constraints, maps, or trajectory errors | Check frame direction, meters/radians, degenerate geometry, invalid depth, covariance symmetry, and numerical residual/Jacobian agreement. | One bounded function or validation stage |
| Reintegrate Geometry After a Pose Correction | Calibrated measurements, feature matches, sensor timestamps, poses, and uncertainty models | Residuals, correspondences, pose constraints, maps, or trajectory errors | Check frame direction, meters/radians, degenerate geometry, invalid depth, covariance symmetry, and numerical residual/Jacobian agreement. | One bounded function or validation stage |

## Data and evaluation

A small teaching implementation should use synthetic or separately licensed fixtures. Check frame direction, meters/radians, degenerate geometry, invalid depth, covariance symmetry, and numerical residual/Jacobian agreement. Dataset names, exact protocol details, published metrics, and hardware requirements must be checked in the source PDF during full-text review; they are not inferred from an awesome-list entry. Keep educational component tests distinct from the paper's end-to-end evaluation.

## Limitations and failure modes

- This is a concise acquisition card, not a full-text technical review. Confirm equations, architecture details, and paper-stated limitations in the PDF before authoring theory.
- Passing synthetic component tests does not establish real-robot performance, robustness, or safe deployment.
- Version calibration and sensor timing with logs; monitor residuals, inlier ratio, drift, relocalization, and compute latency across scene/motion conditions.
- The paper, linked code, datasets, assets, and weights may carry different license conditions.

## Implementation decomposition

1. Integrate a Depth Frame into a TSDF.
2. Update a Global Pose Graph.
3. Reintegrate Geometry After a Pose Correction.
4. Integrate the components on a small fixed fixture and record all deviations from the paper.
5. Add failure slices and a reproducible artifact report.

## Problem blueprints

### Problem: Integrate a Depth Frame into a TSDF

- **Type:** component
- **Difficulty:** medium
- **Learning objective:** Implement and explain the integrate a depth frame into a tsdf component.
- **Inputs:** Calibrated measurements, feature matches, sensor timestamps, poses, and uncertainty models; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Residuals, correspondences, pose constraints, maps, or trajectory errors; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check frame direction, meters/radians, degenerate geometry, invalid depth, covariance symmetry, and numerical residual/Jacobian agreement. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Update a Global Pose Graph

- **Type:** component
- **Difficulty:** hard
- **Learning objective:** Implement and explain the update a global pose graph component.
- **Inputs:** Calibrated measurements, feature matches, sensor timestamps, poses, and uncertainty models; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Residuals, correspondences, pose constraints, maps, or trajectory errors; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check frame direction, meters/radians, degenerate geometry, invalid depth, covariance symmetry, and numerical residual/Jacobian agreement. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Reintegrate Geometry After a Pose Correction

- **Type:** pipeline
- **Difficulty:** hard
- **Learning objective:** Implement and explain the reintegrate geometry after a pose correction component.
- **Inputs:** Calibrated measurements, feature matches, sensor timestamps, poses, and uncertainty models; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Residuals, correspondences, pose constraints, maps, or trajectory errors; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check frame direction, meters/radians, degenerate geometry, invalid depth, covariance symmetry, and numerical residual/Jacobian agreement. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

## Visual teaching plan

- Compare fused surfaces before and after global pose correction.
- Provide labeled axes, units, coordinate frames, and an equivalent table/text view. Use discrete steps when reduced motion is requested.
- Author diagrams independently; do not copy paper figures or captions.

## MLOps and deployment extensions

- Version calibration and sensor timing with logs; monitor residuals, inlier ratio, drift, relocalization, and compute latency across scene/motion conditions.
- Store paper ID, fixture hash, evaluator version, dependency lock, runtime digest, seed, and resource class with every result.
- Use structured failure reasons and per-slice metrics to distinguish implementation mistakes, distribution shifts, and infrastructure failures.

## Canonical sources

- [Primary arXiv record](https://arxiv.org/abs/1604.01093)
- [Open-access author manuscript](https://arxiv.org/pdf/1604.01093)

Identity metadata was read from the primary arXiv record. Local file signature, byte count, page parsing, and SHA-256 were verified on acquisition.

