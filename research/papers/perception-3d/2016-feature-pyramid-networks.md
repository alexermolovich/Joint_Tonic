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
---

# Feature Pyramid Networks for Object Detection

## Agent brief

Fuse coarse semantic feature maps with finer spatial maps through a top-down feature pyramid. This acquisition card verifies the primary paper identity and local PDF, and proposes components that can become independently testable Joint Tonic problems. Full-text technical review is required before promoting an idea into a reviewed problem blueprint.

## Contribution

Fuse coarse semantic feature maps with finer spatial maps through a top-down feature pyramid.

The proposed exercises below are original teaching decompositions. They do not assert a full reproduction of the paper or any published performance number.

## Prerequisite concepts

- Array broadcasting, coordinate conventions, supervised losses, and detection/reconstruction metrics.

## Method map

| Component candidate | Input | Output | Core invariant | Good exercise boundary |
|---|---|---|---|---|
| Build Top-Down Feature Fusion | Synthetic images, point sets, or feature tensors with documented spatial dimensions | Spatial features, geometric predictions, or per-example metrics | Check tensor dimensions, empty/minimal inputs, permutation or coordinate invariants, and numerical agreement. | One bounded function or validation stage |
| Align Lateral Feature Shapes | Synthetic images, point sets, or feature tensors with documented spatial dimensions | Spatial features, geometric predictions, or per-example metrics | Check tensor dimensions, empty/minimal inputs, permutation or coordinate invariants, and numerical agreement. | One bounded function or validation stage |
| Assign Objects to Pyramid Levels | Synthetic images, point sets, or feature tensors with documented spatial dimensions | Spatial features, geometric predictions, or per-example metrics | Check tensor dimensions, empty/minimal inputs, permutation or coordinate invariants, and numerical agreement. | One bounded function or validation stage |

## Data and evaluation

A small teaching implementation should use synthetic or separately licensed fixtures. Check tensor dimensions, empty/minimal inputs, permutation or coordinate invariants, and numerical agreement. Dataset names, exact protocol details, published metrics, and hardware requirements must be checked in the source PDF during full-text review; they are not inferred from an awesome-list entry. Keep educational component tests distinct from the paper's end-to-end evaluation.

## Limitations and failure modes

- This is a concise acquisition card, not a full-text technical review. Confirm equations, architecture details, and paper-stated limitations in the PDF before authoring theory.
- Passing synthetic component tests does not establish real-robot performance, robustness, or safe deployment.
- Version camera preprocessing and calibration with the model; profile latency, memory, and errors by object scale, lighting, and viewpoint.
- The paper, linked code, datasets, assets, and weights may carry different license conditions.

## Implementation decomposition

1. Build Top-Down Feature Fusion.
2. Align Lateral Feature Shapes.
3. Assign Objects to Pyramid Levels.
4. Integrate the components on a small fixed fixture and record all deviations from the paper.
5. Add failure slices and a reproducible artifact report.

## Problem blueprints

### Problem: Build Top-Down Feature Fusion

- **Type:** component
- **Difficulty:** medium
- **Learning objective:** Implement and explain the build top-down feature fusion component.
- **Inputs:** Synthetic images, point sets, or feature tensors with documented spatial dimensions; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Spatial features, geometric predictions, or per-example metrics; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check tensor dimensions, empty/minimal inputs, permutation or coordinate invariants, and numerical agreement. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Align Lateral Feature Shapes

- **Type:** component
- **Difficulty:** hard
- **Learning objective:** Implement and explain the align lateral feature shapes component.
- **Inputs:** Synthetic images, point sets, or feature tensors with documented spatial dimensions; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Spatial features, geometric predictions, or per-example metrics; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check tensor dimensions, empty/minimal inputs, permutation or coordinate invariants, and numerical agreement. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Assign Objects to Pyramid Levels

- **Type:** pipeline
- **Difficulty:** hard
- **Learning objective:** Implement and explain the assign objects to pyramid levels component.
- **Inputs:** Synthetic images, point sets, or feature tensors with documented spatial dimensions; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Spatial features, geometric predictions, or per-example metrics; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check tensor dimensions, empty/minimal inputs, permutation or coordinate invariants, and numerical agreement. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

## Visual teaching plan

- Draw aligned pyramid levels with live tensor shapes and object-size assignments.
- Provide labeled axes, units, coordinate frames, and an equivalent table/text view. Use discrete steps when reduced motion is requested.
- Author diagrams independently; do not copy paper figures or captions.

## MLOps and deployment extensions

- Version camera preprocessing and calibration with the model; profile latency, memory, and errors by object scale, lighting, and viewpoint.
- Store paper ID, fixture hash, evaluator version, dependency lock, runtime digest, seed, and resource class with every result.
- Use structured failure reasons and per-slice metrics to distinguish implementation mistakes, distribution shifts, and infrastructure failures.

## Canonical sources

- [Primary arXiv record](https://arxiv.org/abs/1612.03144)
- [Open-access author manuscript](https://arxiv.org/pdf/1612.03144)

Identity metadata was read from the primary arXiv record. Local file signature, byte count, page parsing, and SHA-256 were verified on acquisition.

