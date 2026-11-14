---
schema_version: 1
paper_id: "2017-mask-r-cnn"
title: "Mask R-CNN"
authors: ["He, Kaiming","Gkioxari, Georgia","Dollár, Piotr","Girshick, Ross"]
year: 2017
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/1703.06870"
pdf_url: "https://arxiv.org/pdf/1703.06870"
local_pdf: "./2017-mask-r-cnn.pdf"
sha256: "b595a882b763d55d933543131f32a2c4b6f41d0818d418ef46a2b66f946b67a8"
bytes: 7723886
pages: 12
topics: ["perception-3d","mask-r-cnn"]
modalities: ["rgb","depth","point-clouds"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
---

# Mask R-CNN

## Agent brief

Add an instance-mask branch to region-based detection and preserve feature alignment. This acquisition card verifies the primary paper identity and local PDF, and proposes components that can become independently testable Joint Tonic problems. Full-text technical review is required before promoting an idea into a reviewed problem blueprint.

## Contribution

Add an instance-mask branch to region-based detection and preserve feature alignment.

The proposed exercises below are original teaching decompositions. They do not assert a full reproduction of the paper or any published performance number.

## Prerequisite concepts

- Array broadcasting, coordinate conventions, supervised losses, and detection/reconstruction metrics.

## Method map

| Component candidate | Input | Output | Core invariant | Good exercise boundary |
|---|---|---|---|---|
| Implement Bilinear ROI Align | Synthetic images, point sets, or feature tensors with documented spatial dimensions | Spatial features, geometric predictions, or per-example metrics | Check tensor dimensions, empty/minimal inputs, permutation or coordinate invariants, and numerical agreement. | One bounded function or validation stage |
| Construct Instance Mask Targets | Synthetic images, point sets, or feature tensors with documented spatial dimensions | Spatial features, geometric predictions, or per-example metrics | Check tensor dimensions, empty/minimal inputs, permutation or coordinate invariants, and numerical agreement. | One bounded function or validation stage |
| Evaluate Per-Instance Mask IoU | Synthetic images, point sets, or feature tensors with documented spatial dimensions | Spatial features, geometric predictions, or per-example metrics | Check tensor dimensions, empty/minimal inputs, permutation or coordinate invariants, and numerical agreement. | One bounded function or validation stage |

## Data and evaluation

A small teaching implementation should use synthetic or separately licensed fixtures. Check tensor dimensions, empty/minimal inputs, permutation or coordinate invariants, and numerical agreement. Dataset names, exact protocol details, published metrics, and hardware requirements must be checked in the source PDF during full-text review; they are not inferred from an awesome-list entry. Keep educational component tests distinct from the paper's end-to-end evaluation.

## Limitations and failure modes

- This is a concise acquisition card, not a full-text technical review. Confirm equations, architecture details, and paper-stated limitations in the PDF before authoring theory.
- Passing synthetic component tests does not establish real-robot performance, robustness, or safe deployment.
- Version camera preprocessing and calibration with the model; profile latency, memory, and errors by object scale, lighting, and viewpoint.
- The paper, linked code, datasets, assets, and weights may carry different license conditions.

## Implementation decomposition

1. Implement Bilinear ROI Align.
2. Construct Instance Mask Targets.
3. Evaluate Per-Instance Mask IoU.
4. Integrate the components on a small fixed fixture and record all deviations from the paper.
5. Add failure slices and a reproducible artifact report.

## Problem blueprints

### Problem: Implement Bilinear ROI Align

- **Type:** component
- **Difficulty:** medium
- **Learning objective:** Implement and explain the implement bilinear roi align component.
- **Inputs:** Synthetic images, point sets, or feature tensors with documented spatial dimensions; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Spatial features, geometric predictions, or per-example metrics; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check tensor dimensions, empty/minimal inputs, permutation or coordinate invariants, and numerical agreement. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Construct Instance Mask Targets

- **Type:** component
- **Difficulty:** hard
- **Learning objective:** Implement and explain the construct instance mask targets component.
- **Inputs:** Synthetic images, point sets, or feature tensors with documented spatial dimensions; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Spatial features, geometric predictions, or per-example metrics; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check tensor dimensions, empty/minimal inputs, permutation or coordinate invariants, and numerical agreement. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Evaluate Per-Instance Mask IoU

- **Type:** pipeline
- **Difficulty:** hard
- **Learning objective:** Implement and explain the evaluate per-instance mask iou component.
- **Inputs:** Synthetic images, point sets, or feature tensors with documented spatial dimensions; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Spatial features, geometric predictions, or per-example metrics; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check tensor dimensions, empty/minimal inputs, permutation or coordinate invariants, and numerical agreement. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

## Visual teaching plan

- Show the same ROI sampled with aligned and rounded coordinates.
- Provide labeled axes, units, coordinate frames, and an equivalent table/text view. Use discrete steps when reduced motion is requested.
- Author diagrams independently; do not copy paper figures or captions.

## MLOps and deployment extensions

- Version camera preprocessing and calibration with the model; profile latency, memory, and errors by object scale, lighting, and viewpoint.
- Store paper ID, fixture hash, evaluator version, dependency lock, runtime digest, seed, and resource class with every result.
- Use structured failure reasons and per-slice metrics to distinguish implementation mistakes, distribution shifts, and infrastructure failures.

## Canonical sources

- [Primary arXiv record](https://arxiv.org/abs/1703.06870)
- [Open-access author manuscript](https://arxiv.org/pdf/1703.06870)

Identity metadata was read from the primary arXiv record. Local file signature, byte count, page parsing, and SHA-256 were verified on acquisition.

