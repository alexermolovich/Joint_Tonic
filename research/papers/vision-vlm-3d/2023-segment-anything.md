---
schema_version: 1
paper_id: "2023-segment-anything"
title: "Segment Anything"
authors: ["Alexander Kirillov", "Eric Mintun", "Nikhila Ravi", "Hanzi Mao", "Chloe Rolland", "Laura Gustafson", "Tete Xiao", "Spencer Whitehead", "Alexander C. Berg", "Wan-Yen Lo", "Piotr Dollar", "Ross Girshick"]
year: 2023
venue_or_status: "ICCV 2023"
primary_url: "https://arxiv.org/abs/2304.02643"
pdf_url: "https://arxiv.org/pdf/2304.02643"
local_pdf: "./2023-segment-anything.pdf"
sha256: "c6ca524e47200c3e542587ca76ac1dbc89cc67340f948c819250d16fdbd90cfb"
bytes: 15644599
pages: 30
topics: ["image segmentation", "promptable models", "foundation models", "data engine"]
modalities: ["RGB image", "point prompts", "box prompts", "mask prompts"]
track_role: "Promptable pixel-level perception"
open_access_status: "Open-access arXiv manuscript"
redistribution_note: "Retain the original attribution and license metadata; verify source terms before redistributing outside this research workspace. The SA-1B dataset has separate access terms and is not included here."
---

## Agent brief

Use SAM to teach a split inference architecture: compute an expensive image embedding once, encode many lightweight prompts, decode several candidate masks, and rank/filter them. Distinguish the paper PDF, model weights, and SA-1B dataset licenses.

## Contribution

SAM defines a promptable segmentation task and couples a large image encoder with prompt encoders and a small mask decoder. A data engine uses the evolving model to scale mask annotation, producing a broad zero-shot segmentation system.

## Prerequisite concepts

- Vision Transformer features and 2D positional encodings
- Point, box, and dense-mask representations
- Cross-attention and dynamic mask prediction
- IoU, mask stability, NMS, and segmentation metrics

## Method map

1. Resize/pad an image and compute a reusable image embedding.
2. Encode sparse prompts with type and position embeddings; encode masks densely.
3. Use two-way attention between prompt tokens and image features.
4. Upscale features and predict multiple masks from mask tokens.
5. Predict mask quality so ambiguous outputs can be ranked.
6. For automatic generation, sample point grids, filter, crop, and suppress duplicate masks.

## Essential equations

SAM's dynamic mask prediction can be summarized as a dot product between an upscaled image feature (F(x,y)) and a mask-token-derived vector (w_k):

$$
M_k(x,y)=w_k^{\mathsf T}F(x,y).
$$

A useful automatic-mask stability measure compares two nearby logit thresholds:

$$
\operatorname{stab}(M)=
\frac{|\{M>\theta+\delta\}|}{|\{M>\theta-\delta\}|},
$$

with a defined zero-denominator policy.

## Visual teaching plan

- **Prompt-to-mask path:** Toggle point, box, and mask prompts and show their embeddings entering the lightweight decoder beside a cached image embedding.
- **Multimask explorer:** Display candidate masks, predicted IoU, true IoU when labels exist, and the selected result.
- **Automatic generator:** Animate point grids, crop pyramids, stability filtering, and mask NMS as successive layers of a funnel.

## Data and evaluation

The paper describes a three-stage data engine and the SA-1B dataset, then evaluates zero-shot transfer on many segmentation tasks. An educational implementation can focus on prompt transforms, decoder post-processing, IoU/stability scores, boundary metrics, and latency split between image encoding and prompt decoding.

## Limitations and failure modes

- The system segments regions but does not inherently assign semantic class labels.
- Fine structures, ambiguous boundaries, and unfamiliar imaging domains can fail.
- Automatic generation can produce duplicates and requires several thresholds.
- The dataset/model scale is impractical to reproduce in a small course environment.

## Implementation decomposition

1. Long-side resize, padding, and coordinate transforms.
2. Point/label and box prompt encoding.
3. Candidate mask upscaling and thresholding.
4. Predicted-IoU ranking and stability scoring.
5. Crop-grid generation, uncropping, and mask NMS.
6. Cached-embedding API with latency and memory instrumentation.

## Problem blueprints

### Transform prompts through resize and padding

- **Type:** Geometry/preprocessing
- **Difficulty:** Medium
- **Inputs:** Original image shape, target long side, points/labels and boxes
- **Outputs:** Model-space prompt coordinates and padding metadata
- **Grading:** Aspect ratio; half-open box convention; round-trip tolerance; empty prompts; batched shapes

### Rank multimask predictions

- **Type:** Mask post-processing
- **Difficulty:** Medium
- **Inputs:** Low-resolution mask logits, predicted IoU, original/resized shapes, thresholds
- **Outputs:** Restored binary masks, scores, selected mask index
- **Grading:** Crop-before-resize order; threshold in logit space; deterministic ranking; exact output dimensions

### Compute mask stability and suppress duplicates

- **Type:** Segmentation filtering
- **Difficulty:** Hard
- **Inputs:** Mask logits, two close thresholds, mask boxes, quality scores
- **Outputs:** Stability scores and kept mask indices
- **Grading:** Intersection/union definition; zero-union handling; box NMS order; stable ties; vectorization

## MLOps and deployment extensions

- Cache image embeddings under a key containing model, preprocessing, and image-content hashes.
- Measure encoder latency separately from prompt-to-mask latency and track prompts per image.
- Monitor mask-count, area, stability, boundary complexity, and human-correction rates by domain.
- Establish dataset/model license gates and privacy review before using automatic masks in retraining loops.

## Canonical sources

- [Primary record](https://arxiv.org/abs/2304.02643)
- [Open-access PDF](https://arxiv.org/pdf/2304.02643)
- [Official project](https://segment-anything.com/)

