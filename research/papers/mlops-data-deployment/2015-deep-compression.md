---
schema_version: 1
paper_id: "2015-deep-compression"
title: "Deep Compression: Compressing Deep Neural Networks with Pruning, Trained Quantization and Huffman Coding"
authors: ["Han, Song","Mao, Huizi","Dally, William J."]
year: 2015
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/1510.00149"
pdf_url: "https://arxiv.org/pdf/1510.00149"
local_pdf: "./2015-deep-compression.pdf"
sha256: "248044bef68e27e22384583a39d0bee743fd614d00e88a8dda6b331b5fd218d3"
bytes: 1055865
pages: 14
topics: ["mlops-data-deployment","deep-compression"]
modalities: ["datasets","model-artifacts","logs","metrics"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
---

# Deep Compression: Compressing Deep Neural Networks with Pruning, Trained Quantization and Huffman Coding

## Agent brief

Study pruning and low-bit representation as an inference-storage optimization pipeline. This acquisition card verifies the primary paper identity and local PDF, and proposes components that can become independently testable Joint Tonic problems. Full-text technical review is required before promoting an idea into a reviewed problem blueprint.

## Contribution

Study pruning and low-bit representation as an inference-storage optimization pipeline.

The proposed exercises below are original teaching decompositions. They do not assert a full reproduction of the paper or any published performance number.

## Prerequisite concepts

- Versioned artifacts, data schemas, deterministic splits, latency percentiles, and release gates.

## Method map

| Component candidate | Input | Output | Core invariant | Good exercise boundary |
|---|---|---|---|---|
| Apply a Weight-Pruning Mask | Versioned dataset records, artifact metadata, calibration records, or benchmark samples | Validated records, dependency decisions, compressed tensors, or reproducible evaluation reports | Check deterministic ordering, duplicate handling, missing metadata, leakage boundaries, threshold equality, and invalid measurement windows. | One bounded function or validation stage |
| Quantize Shared Weight Centroids | Versioned dataset records, artifact metadata, calibration records, or benchmark samples | Validated records, dependency decisions, compressed tensors, or reproducible evaluation reports | Check deterministic ordering, duplicate handling, missing metadata, leakage boundaries, threshold equality, and invalid measurement windows. | One bounded function or validation stage |
| Compute a Compressed Model Storage Budget | Versioned dataset records, artifact metadata, calibration records, or benchmark samples | Validated records, dependency decisions, compressed tensors, or reproducible evaluation reports | Check deterministic ordering, duplicate handling, missing metadata, leakage boundaries, threshold equality, and invalid measurement windows. | One bounded function or validation stage |

## Data and evaluation

A small teaching implementation should use synthetic or separately licensed fixtures. Check deterministic ordering, duplicate handling, missing metadata, leakage boundaries, threshold equality, and invalid measurement windows. Dataset names, exact protocol details, published metrics, and hardware requirements must be checked in the source PDF during full-text review; they are not inferred from an awesome-list entry. Keep educational component tests distinct from the paper's end-to-end evaluation.

## Limitations and failure modes

- This is a concise acquisition card, not a full-text technical review. Confirm equations, architecture details, and paper-stated limitations in the PDF before authoring theory.
- Passing synthetic component tests does not establish real-robot performance, robustness, or safe deployment.
- Make every report reproducible from code, data, preprocessing, runtime, and hardware identifiers; separate data/model regressions from platform failures.
- The paper, linked code, datasets, assets, and weights may carry different license conditions.

## Implementation decomposition

1. Apply a Weight-Pruning Mask.
2. Quantize Shared Weight Centroids.
3. Compute a Compressed Model Storage Budget.
4. Integrate the components on a small fixed fixture and record all deviations from the paper.
5. Add failure slices and a reproducible artifact report.

## Problem blueprints

### Problem: Apply a Weight-Pruning Mask

- **Type:** component
- **Difficulty:** medium
- **Learning objective:** Implement and explain the apply a weight-pruning mask component.
- **Inputs:** Versioned dataset records, artifact metadata, calibration records, or benchmark samples; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Validated records, dependency decisions, compressed tensors, or reproducible evaluation reports; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check deterministic ordering, duplicate handling, missing metadata, leakage boundaries, threshold equality, and invalid measurement windows. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Quantize Shared Weight Centroids

- **Type:** component
- **Difficulty:** hard
- **Learning objective:** Implement and explain the quantize shared weight centroids component.
- **Inputs:** Versioned dataset records, artifact metadata, calibration records, or benchmark samples; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Validated records, dependency decisions, compressed tensors, or reproducible evaluation reports; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check deterministic ordering, duplicate handling, missing metadata, leakage boundaries, threshold equality, and invalid measurement windows. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Compute a Compressed Model Storage Budget

- **Type:** pipeline
- **Difficulty:** hard
- **Learning objective:** Implement and explain the compute a compressed model storage budget component.
- **Inputs:** Versioned dataset records, artifact metadata, calibration records, or benchmark samples; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Validated records, dependency decisions, compressed tensors, or reproducible evaluation reports; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check deterministic ordering, duplicate handling, missing metadata, leakage boundaries, threshold equality, and invalid measurement windows. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

## Visual teaching plan

- Compare dense, pruned, and quantized weight distributions.
- Provide labeled axes, units, coordinate frames, and an equivalent table/text view. Use discrete steps when reduced motion is requested.
- Author diagrams independently; do not copy paper figures or captions.

## MLOps and deployment extensions

- Make every report reproducible from code, data, preprocessing, runtime, and hardware identifiers; separate data/model regressions from platform failures.
- Store paper ID, fixture hash, evaluator version, dependency lock, runtime digest, seed, and resource class with every result.
- Use structured failure reasons and per-slice metrics to distinguish implementation mistakes, distribution shifts, and infrastructure failures.

## Canonical sources

- [Primary arXiv record](https://arxiv.org/abs/1510.00149)
- [Open-access author manuscript](https://arxiv.org/pdf/1510.00149)

Identity metadata was read from the primary arXiv record. Local file signature, byte count, page parsing, and SHA-256 were verified on acquisition.

