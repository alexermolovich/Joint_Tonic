---
schema_version: 1
paper_id: "2022-flamingo"
title: "Flamingo: a Visual Language Model for Few-Shot Learning"
authors: ["Alayrac, Jean-Baptiste","Donahue, Jeff","Luc, Pauline","Miech, Antoine","Barr, Iain","Hasson, Yana","Lenc, Karel","Mensch, Arthur","Millican, Katie","Reynolds, Malcolm","Ring, Roman","Rutherford, Eliza","Cabi, Serkan","Han, Tengda","Gong, Zhitao","Samangooei, Sina","Monteiro, Marianne","Menick, Jacob","Borgeaud, Sebastian","Brock, Andrew","Nematzadeh, Aida","Sharifzadeh, Sahand","Binkowski, Mikolaj","Barreira, Ricardo","Vinyals, Oriol","Zisserman, Andrew","Simonyan, Karen"]
year: 2022
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2204.14198"
pdf_url: "https://arxiv.org/pdf/2204.14198"
local_pdf: "./2022-flamingo.pdf"
sha256: "27af622bf50987fd98a03451a27a670adfaeefd5218a3e990b37abc326ba63f0"
bytes: 31579390
pages: 54
topics: ["vlm-grounding","flamingo"]
modalities: ["rgb","text","spatial-tokens"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
---

# Flamingo: a Visual Language Model for Few-Shot Learning

## Agent brief

Condition a language model on interleaved visual inputs through resampled visual features and cross-attention. This acquisition card verifies the primary paper identity and local PDF, and proposes components that can become independently testable Joint Tonic problems. Full-text technical review is required before promoting an idea into a reviewed problem blueprint.

## Contribution

Condition a language model on interleaved visual inputs through resampled visual features and cross-attention.

The proposed exercises below are original teaching decompositions. They do not assert a full reproduction of the paper or any published performance number.

## Prerequisite concepts

- Attention masks, embedding normalization, tokenization, cross-entropy, and visual coordinate conventions.

## Method map

| Component candidate | Input | Output | Core invariant | Good exercise boundary |
|---|---|---|---|---|
| Resample Variable Visual Features | Image features, token IDs, sequence lengths, and validity masks | Aligned features, structured spatial outputs, or an alignment loss | Check masks, padding, token order, shape compatibility, boundary coordinates, and stable numerical loss. | One bounded function or validation stage |
| Mask Cross-Attention by Image Position | Image features, token IDs, sequence lengths, and validity masks | Aligned features, structured spatial outputs, or an alignment loss | Check masks, padding, token order, shape compatibility, boundary coordinates, and stable numerical loss. | One bounded function or validation stage |
| Gate a Multimodal Residual Update | Image features, token IDs, sequence lengths, and validity masks | Aligned features, structured spatial outputs, or an alignment loss | Check masks, padding, token order, shape compatibility, boundary coordinates, and stable numerical loss. | One bounded function or validation stage |

## Data and evaluation

A small teaching implementation should use synthetic or separately licensed fixtures. Check masks, padding, token order, shape compatibility, boundary coordinates, and stable numerical loss. Dataset names, exact protocol details, published metrics, and hardware requirements must be checked in the source PDF during full-text review; they are not inferred from an awesome-list entry. Keep educational component tests distinct from the paper's end-to-end evaluation.

## Limitations and failure modes

- This is a concise acquisition card, not a full-text technical review. Confirm equations, architecture details, and paper-stated limitations in the PDF before authoring theory.
- Passing synthetic component tests does not establish real-robot performance, robustness, or safe deployment.
- Version tokenizer, image preprocessing, prompt templates, and output grammar together; monitor retrieval/grounding by language, object, and scene slice.
- The paper, linked code, datasets, assets, and weights may carry different license conditions.

## Implementation decomposition

1. Resample Variable Visual Features.
2. Mask Cross-Attention by Image Position.
3. Gate a Multimodal Residual Update.
4. Integrate the components on a small fixed fixture and record all deviations from the paper.
5. Add failure slices and a reproducible artifact report.

## Problem blueprints

### Problem: Resample Variable Visual Features

- **Type:** component
- **Difficulty:** medium
- **Learning objective:** Implement and explain the resample variable visual features component.
- **Inputs:** Image features, token IDs, sequence lengths, and validity masks; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Aligned features, structured spatial outputs, or an alignment loss; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check masks, padding, token order, shape compatibility, boundary coordinates, and stable numerical loss. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Mask Cross-Attention by Image Position

- **Type:** component
- **Difficulty:** hard
- **Learning objective:** Implement and explain the mask cross-attention by image position component.
- **Inputs:** Image features, token IDs, sequence lengths, and validity masks; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Aligned features, structured spatial outputs, or an alignment loss; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check masks, padding, token order, shape compatibility, boundary coordinates, and stable numerical loss. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Gate a Multimodal Residual Update

- **Type:** pipeline
- **Difficulty:** hard
- **Learning objective:** Implement and explain the gate a multimodal residual update component.
- **Inputs:** Image features, token IDs, sequence lengths, and validity masks; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Aligned features, structured spatial outputs, or an alignment loss; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check masks, padding, token order, shape compatibility, boundary coordinates, and stable numerical loss. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

## Visual teaching plan

- Draw interleaved images and text with visible attention boundaries.
- Provide labeled axes, units, coordinate frames, and an equivalent table/text view. Use discrete steps when reduced motion is requested.
- Author diagrams independently; do not copy paper figures or captions.

## MLOps and deployment extensions

- Version tokenizer, image preprocessing, prompt templates, and output grammar together; monitor retrieval/grounding by language, object, and scene slice.
- Store paper ID, fixture hash, evaluator version, dependency lock, runtime digest, seed, and resource class with every result.
- Use structured failure reasons and per-slice metrics to distinguish implementation mistakes, distribution shifts, and infrastructure failures.

## Canonical sources

- [Primary arXiv record](https://arxiv.org/abs/2204.14198)
- [Open-access author manuscript](https://arxiv.org/pdf/2204.14198)

Identity metadata was read from the primary arXiv record. Local file signature, byte count, page parsing, and SHA-256 were verified on acquisition.

