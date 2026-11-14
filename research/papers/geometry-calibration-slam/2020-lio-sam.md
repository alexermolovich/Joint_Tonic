---
schema_version: 1
paper_id: "2020-lio-sam"
title: "LIO-SAM: Tightly-coupled Lidar Inertial Odometry via Smoothing and Mapping"
authors: ["Shan, Tixiao","Englot, Brendan","Meyers, Drew","Wang, Wei","Ratti, Carlo","Rus, Daniela"]
year: 2020
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2007.00258"
pdf_url: "https://arxiv.org/pdf/2007.00258"
local_pdf: "./2020-lio-sam.pdf"
sha256: "8ad11438fc0849de88b1604932f8bfd2732aee640aaf5fb41974b34f555c86f6"
bytes: 4368703
pages: 8
topics: ["geometry-calibration-slam","lio-sam"]
modalities: ["camera","imu","lidar","poses"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
---

# LIO-SAM: Tightly-coupled Lidar Inertial Odometry via Smoothing and Mapping

## Agent brief

Study tightly coupled lidar-inertial odometry with factor-graph state estimation. This acquisition card verifies the primary paper identity and local PDF, and proposes components that can become independently testable Joint Tonic problems. Full-text technical review is required before promoting an idea into a reviewed problem blueprint.

## Contribution

Study tightly coupled lidar-inertial odometry with factor-graph state estimation.

The proposed exercises below are original teaching decompositions. They do not assert a full reproduction of the paper or any published performance number.

## Prerequisite concepts

- SE(3)/SO(3), camera projection, least-squares residuals, covariance, timestamp alignment, and geometric matching.

## Method map

| Component candidate | Input | Output | Core invariant | Good exercise boundary |
|---|---|---|---|---|
| Deskew a Lidar Scan with Motion Estimates | Calibrated measurements, feature matches, sensor timestamps, poses, and uncertainty models | Residuals, correspondences, pose constraints, maps, or trajectory errors | Check frame direction, meters/radians, degenerate geometry, invalid depth, covariance symmetry, and numerical residual/Jacobian agreement. | One bounded function or validation stage |
| Assemble an IMU-Lidar Pose Constraint | Calibrated measurements, feature matches, sensor timestamps, poses, and uncertainty models | Residuals, correspondences, pose constraints, maps, or trajectory errors | Check frame direction, meters/radians, degenerate geometry, invalid depth, covariance symmetry, and numerical residual/Jacobian agreement. | One bounded function or validation stage |
| Reject Inconsistent Loop Closures | Calibrated measurements, feature matches, sensor timestamps, poses, and uncertainty models | Residuals, correspondences, pose constraints, maps, or trajectory errors | Check frame direction, meters/radians, degenerate geometry, invalid depth, covariance symmetry, and numerical residual/Jacobian agreement. | One bounded function or validation stage |

## Data and evaluation

A small teaching implementation should use synthetic or separately licensed fixtures. Check frame direction, meters/radians, degenerate geometry, invalid depth, covariance symmetry, and numerical residual/Jacobian agreement. Dataset names, exact protocol details, published metrics, and hardware requirements must be checked in the source PDF during full-text review; they are not inferred from an awesome-list entry. Keep educational component tests distinct from the paper's end-to-end evaluation.

## Limitations and failure modes

- This is a concise acquisition card, not a full-text technical review. Confirm equations, architecture details, and paper-stated limitations in the PDF before authoring theory.
- Passing synthetic component tests does not establish real-robot performance, robustness, or safe deployment.
- Version calibration and sensor timing with logs; monitor residuals, inlier ratio, drift, relocalization, and compute latency across scene/motion conditions.
- The paper, linked code, datasets, assets, and weights may carry different license conditions.

## Implementation decomposition

1. Deskew a Lidar Scan with Motion Estimates.
2. Assemble an IMU-Lidar Pose Constraint.
3. Reject Inconsistent Loop Closures.
4. Integrate the components on a small fixed fixture and record all deviations from the paper.
5. Add failure slices and a reproducible artifact report.

## Problem blueprints

### Problem: Deskew a Lidar Scan with Motion Estimates

- **Type:** component
- **Difficulty:** medium
- **Learning objective:** Implement and explain the deskew a lidar scan with motion estimates component.
- **Inputs:** Calibrated measurements, feature matches, sensor timestamps, poses, and uncertainty models; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Residuals, correspondences, pose constraints, maps, or trajectory errors; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check frame direction, meters/radians, degenerate geometry, invalid depth, covariance symmetry, and numerical residual/Jacobian agreement. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Assemble an IMU-Lidar Pose Constraint

- **Type:** component
- **Difficulty:** hard
- **Learning objective:** Implement and explain the assemble an imu-lidar pose constraint component.
- **Inputs:** Calibrated measurements, feature matches, sensor timestamps, poses, and uncertainty models; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Residuals, correspondences, pose constraints, maps, or trajectory errors; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check frame direction, meters/radians, degenerate geometry, invalid depth, covariance symmetry, and numerical residual/Jacobian agreement. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Reject Inconsistent Loop Closures

- **Type:** pipeline
- **Difficulty:** hard
- **Learning objective:** Implement and explain the reject inconsistent loop closures component.
- **Inputs:** Calibrated measurements, feature matches, sensor timestamps, poses, and uncertainty models; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Residuals, correspondences, pose constraints, maps, or trajectory errors; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check frame direction, meters/radians, degenerate geometry, invalid depth, covariance symmetry, and numerical residual/Jacobian agreement. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

## Visual teaching plan

- Overlay raw and deskewed scans with pose-graph constraints.
- Provide labeled axes, units, coordinate frames, and an equivalent table/text view. Use discrete steps when reduced motion is requested.
- Author diagrams independently; do not copy paper figures or captions.

## MLOps and deployment extensions

- Version calibration and sensor timing with logs; monitor residuals, inlier ratio, drift, relocalization, and compute latency across scene/motion conditions.
- Store paper ID, fixture hash, evaluator version, dependency lock, runtime digest, seed, and resource class with every result.
- Use structured failure reasons and per-slice metrics to distinguish implementation mistakes, distribution shifts, and infrastructure failures.

## Canonical sources

- [Primary arXiv record](https://arxiv.org/abs/2007.00258)
- [Open-access author manuscript](https://arxiv.org/pdf/2007.00258)

Identity metadata was read from the primary arXiv record. Local file signature, byte count, page parsing, and SHA-256 were verified on acquisition.

