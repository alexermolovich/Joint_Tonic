---
schema_version: 1
paper_id: "2023-grounding-dino"
title: "Grounding DINO: Marrying DINO with Grounded Pre-Training for Open-Set Object Detection"
authors: ["Shilong Liu", "Zhaoyang Zeng", "Tianhe Ren", "Feng Li", "Hao Zhang", "Jie Yang", "Qing Jiang", "Chunyuan Li", "Jianwei Yang", "Hang Su", "Jun Zhu", "Lei Zhang"]
year: 2023
venue_or_status: "ECCV 2024"
primary_url: "https://arxiv.org/abs/2303.05499"
pdf_url: "https://arxiv.org/pdf/2303.05499"
local_pdf: "./2023-grounding-dino.pdf"
sha256: "ba1c64ec2ac4fedeb50b269eadc994456a8428dbe64a8dba2673f22df0fa20b3"
bytes: 4329735
pages: 33
topics: ["open-set detection", "phrase grounding", "vision-language fusion", "object detection"]
modalities: ["RGB image", "text prompt"]
track_role: "Language-grounded open-world detection"
open_access_status: "Open-access arXiv manuscript"
redistribution_note: "Retain the original attribution and license metadata; verify source terms before redistributing outside this research workspace."
---

## Agent brief

Use Grounding DINO after DETR and CLIP. Focus exercises on text-span supervision, language-guided query selection, cross-modal features, and converting token-level scores into phrase-labeled detections.

## Contribution

Grounding DINO adapts transformer detection to arbitrary text inputs through early vision-language feature enhancement, language-aware query selection, and cross-modal decoding. Grounded pretraining enables open-set detection and referring-expression grounding.

## Prerequisite concepts

- DETR-style object queries, matching, and box losses
- Tokenization, attention masks, and text spans
- Contrastive alignment of regions and tokens
- Open-vocabulary and referring-expression metrics

## Method map

1. Tokenize a caption or category list and retain token/phrase boundaries.
2. Extract visual and language features, then enhance them with cross-modal attention.
3. Score encoder positions against language to select decoder queries.
4. Refine boxes and token alignment through a cross-modal decoder.
5. Aggregate token logits into requested phrases and threshold final detections.

## Essential equations

For query feature (q_i) and token features (t_j), a simple language-guided proposal score is

$$
r_i=\max_{j:\,m_j=1}\sigma(q_i^{\mathsf T}t_j),
$$

where (m_j) excludes padding and special tokens. If phrase (g) maps to token set (J_g), one transparent phrase score is

$$
s_{ig}=\max_{j\in J_g}\sigma(\ell_{ij}),
$$

provided the implementation documents this aggregation rule; alternative calibrated aggregations are valid but must not be mixed silently.

## Visual teaching plan

- **Token-span map:** Highlight caption character spans, tokenizer pieces, and the resulting positive-map rows together.
- **Cross-modal query selector:** A heatmap of encoder-position/token similarity shows which visual positions enter the decoder as top queries.
- **Phrase decoder:** Editing a phrase updates token scores, aggregated phrase scores, thresholds, and labeled boxes in real time.

## Data and evaluation

The paper combines detection, grounding, and caption data, and evaluates zero-shot transfer on COCO, LVIS, ODinW, and RefCOCO-family tasks. Reproductions must document prompt construction, dataset overlap, tokenization, thresholds, and whether evaluation is category or phrase based.

## Limitations and failure modes

- Output quality is prompt- and tokenizer-sensitive.
- Text supervision/data mixture can introduce biases and ambiguous negatives.
- Similar phrases and attributes may compete for the same region.
- Open-set scores are not automatically calibrated across prompts or domains.

## Implementation decomposition

1. Caption normalization, special-token masking, and phrase spans.
2. Positive maps from boxes/phrases to text tokens.
3. Text-conditioned top-query selection.
4. Cross-modal attention mask and decoder plumbing.
5. Phrase-score aggregation, box post-processing, and grounded evaluation.

## Problem blueprints

### Create a phrase-to-token positive map

- **Type:** Token alignment
- **Difficulty:** Medium
- **Inputs:** Caption, tokenizer offsets, character spans for each target phrase
- **Outputs:** Normalized target-by-token positive matrix
- **Grading:** Subword overlap; special tokens excluded; repeated phrases; truncation policy; rows normalized

### Select language-guided object queries

- **Type:** Vectorized ranking
- **Difficulty:** Medium
- **Inputs:** Encoder image features, token embeddings/masks, requested query count
- **Outputs:** Selected feature rows, indices, and reference boxes
- **Grading:** Masked-token exclusion; score aggregation; stable top-k; fewer-valid-position case; batch correctness

### Decode phrase-grounded detections

- **Type:** Multimodal post-processing
- **Difficulty:** Hard
- **Inputs:** Token logits, boxes, token-to-phrase map, thresholds, image sizes
- **Outputs:** Phrase, score, and image-space box records
- **Grading:** Sigmoid/aggregation semantics; box conversion/clipping; multiple phrases; deterministic sorting; empty prompts

## MLOps and deployment extensions

- Version tokenizer, prompt templates, phrase separators, thresholds, and post-processing with the checkpoint.
- Log per-prompt detection count, score calibration, vocabulary coverage, latency, and human correction rate.
- Create adversarial prompt suites for negation, synonyms, attributes, and unsafe/ambiguous requests.
- Cache text embeddings only with exact tokenizer/checkpoint/prompt hashes and monitor domain-specific open-set false positives.

## Canonical sources

- [Primary record](https://arxiv.org/abs/2303.05499)
- [Open-access PDF](https://arxiv.org/pdf/2303.05499)
- [ECCV 2024 paper](https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/06319.pdf)

