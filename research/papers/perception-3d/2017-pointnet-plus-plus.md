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
---

# PointNet++: Deep Hierarchical Feature Learning on Point Sets in a Metric Space

## Agent brief

Build hierarchical point features by combining sampled centroids, metric neighborhoods, and local feature aggregation. This acquisition card verifies the primary paper identity and local PDF, and proposes components that can become independently testable Joint Tonic problems. Full-text technical review is required before promoting an idea into a reviewed problem blueprint.

## Contribution

Build hierarchical point features by combining sampled centroids, metric neighborhoods, and local feature aggregation.

The proposed exercises below are original teaching decompositions. They do not assert a full reproduction of the paper or any published performance number.

## Prerequisite concepts

- Array broadcasting, coordinate conventions, supervised losses, and detection/reconstruction metrics.

## Method map

| Component candidate | Input | Output | Core invariant | Good exercise boundary |
|---|---|---|---|---|
| Farthest-Point Sampling | Synthetic images, point sets, or feature tensors with documented spatial dimensions | Spatial features, geometric predictions, or per-example metrics | Check tensor dimensions, empty/minimal inputs, permutation or coordinate invariants, and numerical agreement. | One bounded function or validation stage |
| Ball-Query Neighborhood Grouping | Synthetic images, point sets, or feature tensors with documented spatial dimensions | Spatial features, geometric predictions, or per-example metrics | Check tensor dimensions, empty/minimal inputs, permutation or coordinate invariants, and numerical agreement. | One bounded function or validation stage |
| Pool Local Point Features | Synthetic images, point sets, or feature tensors with documented spatial dimensions | Spatial features, geometric predictions, or per-example metrics | Check tensor dimensions, empty/minimal inputs, permutation or coordinate invariants, and numerical agreement. | One bounded function or validation stage |

## Data and evaluation

A small teaching implementation should use synthetic or separately licensed fixtures. Check tensor dimensions, empty/minimal inputs, permutation or coordinate invariants, and numerical agreement. Dataset names, exact protocol details, published metrics, and hardware requirements must be checked in the source PDF during full-text review; they are not inferred from an awesome-list entry. Keep educational component tests distinct from the paper's end-to-end evaluation.

## Limitations and failure modes

- This is a concise acquisition card, not a full-text technical review. Confirm equations, architecture details, and paper-stated limitations in the PDF before authoring theory.
- Passing synthetic component tests does not establish real-robot performance, robustness, or safe deployment.
- Version camera preprocessing and calibration with the model; profile latency, memory, and errors by object scale, lighting, and viewpoint.
- The paper, linked code, datasets, assets, and weights may carry different license conditions.

## Implementation decomposition

1. Farthest-Point Sampling.
2. Ball-Query Neighborhood Grouping.
3. Pool Local Point Features.
4. Integrate the components on a small fixed fixture and record all deviations from the paper.
5. Add failure slices and a reproducible artifact report.

## Problem blueprints

### Problem: Farthest-Point Sampling

- **Type:** component
- **Difficulty:** medium
- **Learning objective:** Implement and explain the farthest-point sampling component.
- **Inputs:** Synthetic images, point sets, or feature tensors with documented spatial dimensions; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Spatial features, geometric predictions, or per-example metrics; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check tensor dimensions, empty/minimal inputs, permutation or coordinate invariants, and numerical agreement. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Ball-Query Neighborhood Grouping

- **Type:** component
- **Difficulty:** hard
- **Learning objective:** Implement and explain the ball-query neighborhood grouping component.
- **Inputs:** Synthetic images, point sets, or feature tensors with documented spatial dimensions; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Spatial features, geometric predictions, or per-example metrics; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check tensor dimensions, empty/minimal inputs, permutation or coordinate invariants, and numerical agreement. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Pool Local Point Features

- **Type:** pipeline
- **Difficulty:** hard
- **Learning objective:** Implement and explain the pool local point features component.
- **Inputs:** Synthetic images, point sets, or feature tensors with documented spatial dimensions; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Spatial features, geometric predictions, or per-example metrics; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check tensor dimensions, empty/minimal inputs, permutation or coordinate invariants, and numerical agreement. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

## Visual teaching plan

- Color each sampled centroid and its neighborhood in a point-cloud viewer.
- Provide labeled axes, units, coordinate frames, and an equivalent table/text view. Use discrete steps when reduced motion is requested.
- Author diagrams independently; do not copy paper figures or captions.

## MLOps and deployment extensions

- Version camera preprocessing and calibration with the model; profile latency, memory, and errors by object scale, lighting, and viewpoint.
- Store paper ID, fixture hash, evaluator version, dependency lock, runtime digest, seed, and resource class with every result.
- Use structured failure reasons and per-slice metrics to distinguish implementation mistakes, distribution shifts, and infrastructure failures.

## Canonical sources

- [Primary arXiv record](https://arxiv.org/abs/1706.02413)
- [Open-access author manuscript](https://arxiv.org/pdf/1706.02413)

Identity metadata was read from the primary arXiv record. Local file signature, byte count, page parsing, and SHA-256 were verified on acquisition.

