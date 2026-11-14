---
schema_version: 1
paper_id: "2023-florence-2"
title: "Florence-2: Advancing a Unified Representation for a Variety of Vision Tasks"
authors: ["Xiao, Bin","Wu, Haiping","Xu, Weijian","Dai, Xiyang","Hu, Houdong","Lu, Yumao","Zeng, Michael","Liu, Ce","Yuan, Lu"]
year: 2023
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2311.06242"
pdf_url: "https://arxiv.org/pdf/2311.06242"
local_pdf: "./2023-florence-2.pdf"
sha256: "403d820e5ea7a1d7e2f95d4b2facef3ea37e2a5f12354a8a50164b10a057708a"
bytes: 56176792
pages: 35
topics: ["vlm-grounding","florence-2"]
modalities: ["rgb","text","spatial-tokens"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
---

# Florence-2: Advancing a Unified Representation for a Variety of Vision Tasks

## Agent brief

Represent several vision tasks through a prompt-based sequence-to-sequence interface. This acquisition card verifies the primary paper identity and local PDF, and proposes components that can become independently testable Joint Tonic problems. Full-text technical review is required before promoting an idea into a reviewed problem blueprint.

## Contribution

Represent several vision tasks through a prompt-based sequence-to-sequence interface.

The proposed exercises below are original teaching decompositions. They do not assert a full reproduction of the paper or any published performance number.

## Prerequisite concepts

- Attention masks, embedding normalization, tokenization, cross-entropy, and visual coordinate conventions.

## Method map

| Component candidate | Input | Output | Core invariant | Good exercise boundary |
|---|---|---|---|---|
| Parse Structured Detection Tokens | Image features, token IDs, sequence lengths, and validity masks | Aligned features, structured spatial outputs, or an alignment loss | Check masks, padding, token order, shape compatibility, boundary coordinates, and stable numerical loss. | One bounded function or validation stage |
| Normalize Spatial Coordinates into Tokens | Image features, token IDs, sequence lengths, and validity masks | Aligned features, structured spatial outputs, or an alignment loss | Check masks, padding, token order, shape compatibility, boundary coordinates, and stable numerical loss. | One bounded function or validation stage |
| Route Task Prompts to Output Schemas | Image features, token IDs, sequence lengths, and validity masks | Aligned features, structured spatial outputs, or an alignment loss | Check masks, padding, token order, shape compatibility, boundary coordinates, and stable numerical loss. | One bounded function or validation stage |

## Data and evaluation

A small teaching implementation should use synthetic or separately licensed fixtures. Check masks, padding, token order, shape compatibility, boundary coordinates, and stable numerical loss. Dataset names, exact protocol details, published metrics, and hardware requirements must be checked in the source PDF during full-text review; they are not inferred from an awesome-list entry. Keep educational component tests distinct from the paper's end-to-end evaluation.

## Limitations and failure modes

- This is a concise acquisition card, not a full-text technical review. Confirm equations, architecture details, and paper-stated limitations in the PDF before authoring theory.
- Passing synthetic component tests does not establish real-robot performance, robustness, or safe deployment.
- Version tokenizer, image preprocessing, prompt templates, and output grammar together; monitor retrieval/grounding by language, object, and scene slice.
- The paper, linked code, datasets, assets, and weights may carry different license conditions.

## Implementation decomposition

1. Parse Structured Detection Tokens.
2. Normalize Spatial Coordinates into Tokens.
3. Route Task Prompts to Output Schemas.
4. Integrate the components on a small fixed fixture and record all deviations from the paper.
5. Add failure slices and a reproducible artifact report.

## Problem blueprints

### Problem: Parse Structured Detection Tokens

- **Type:** component
- **Difficulty:** medium
- **Learning objective:** Implement and explain the parse structured detection tokens component.
- **Inputs:** Image features, token IDs, sequence lengths, and validity masks; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Aligned features, structured spatial outputs, or an alignment loss; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check masks, padding, token order, shape compatibility, boundary coordinates, and stable numerical loss. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Normalize Spatial Coordinates into Tokens

- **Type:** component
- **Difficulty:** hard
- **Learning objective:** Implement and explain the normalize spatial coordinates into tokens component.
- **Inputs:** Image features, token IDs, sequence lengths, and validity masks; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Aligned features, structured spatial outputs, or an alignment loss; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check masks, padding, token order, shape compatibility, boundary coordinates, and stable numerical loss. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Route Task Prompts to Output Schemas

- **Type:** pipeline
- **Difficulty:** hard
- **Learning objective:** Implement and explain the route task prompts to output schemas component.
- **Inputs:** Image features, token IDs, sequence lengths, and validity masks; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Aligned features, structured spatial outputs, or an alignment loss; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check masks, padding, token order, shape compatibility, boundary coordinates, and stable numerical loss. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

## Visual teaching plan

- Toggle task prompts and show the corresponding parsed spatial output.
- Provide labeled axes, units, coordinate frames, and an equivalent table/text view. Use discrete steps when reduced motion is requested.
- Author diagrams independently; do not copy paper figures or captions.

## MLOps and deployment extensions

- Version tokenizer, image preprocessing, prompt templates, and output grammar together; monitor retrieval/grounding by language, object, and scene slice.
- Store paper ID, fixture hash, evaluator version, dependency lock, runtime digest, seed, and resource class with every result.
- Use structured failure reasons and per-slice metrics to distinguish implementation mistakes, distribution shifts, and infrastructure failures.

## Canonical sources

- [Primary arXiv record](https://arxiv.org/abs/2311.06242)
- [Open-access author manuscript](https://arxiv.org/pdf/2311.06242)

Identity metadata was read from the primary arXiv record. Local file signature, byte count, page parsing, and SHA-256 were verified on acquisition.

