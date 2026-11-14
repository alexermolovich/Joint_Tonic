---
schema_version: 1
paper_id: 2023-grounding-dino
title: >-
  Grounding DINO: Marrying DINO with Grounded Pre-Training for Open-Set Object
  Detection
authors:
  - Shilong Liu
  - Zhaoyang Zeng
  - Tianhe Ren
  - Feng Li
  - Hao Zhang
  - Jie Yang
  - Qing Jiang
  - Chunyuan Li
  - Jianwei Yang
  - Hang Su
  - Jun Zhu
  - Lei Zhang
year: 2023
venue_or_status: ECCV 2024
primary_url: 'https://arxiv.org/abs/2303.05499'
pdf_url: 'https://arxiv.org/pdf/2303.05499'
local_pdf: ./2023-grounding-dino.pdf
sha256: ba1c64ec2ac4fedeb50b269eadc994456a8428dbe64a8dba2673f22df0fa20b3
bytes: 4329735
pages: 33
topics:
  - open-set detection
  - phrase grounding
  - vision-language fusion
  - object detection
modalities:
  - RGB image
  - text prompt
track_role: Language-grounded open-world detection
open_access_status: Open-access arXiv manuscript
redistribution_note: >-
  Retain the original attribution and license metadata; verify source terms
  before redistributing outside this research workspace.
execution_flow:
  title: Core execution flow
  description: >-
    Encode images and text, select language-relevant queries, then decode boxes
    and resolve token scores into the requested phrases.
  nodes:
    - id: stage-1
      title: Encode image and text features
      detail: Represent spatial image tokens and valid language tokens for fusion.
      column: 0
      row: 0
      section: Encode image and text features
      problem_slugs:
        - grounding-bidirectional-cross-attention
      planned_problems: []
    - id: stage-2
      title: Select language-guided queries
      detail: >-
        Use compatibility with valid text tokens to prioritize candidate image
        locations.
      column: 1
      row: 0
      section: Select language-guided queries
      problem_slugs:
        - grounding-language-query-selection
      planned_problems: []
    - id: stage-3
      title: Resolve boxes to phrases
      detail: >-
        Decode spatial predictions and aggregate scores over the requested
        phrase spans.
      column: 2
      row: 0
      section: Resolve boxes to phrases
      problem_slugs:
        - grounding-token-phrase-map
        - grounding-phrase-box-decoding
        - grounded-segmentation-failure-trace
        - grounding-localization-phrase-metrics
      planned_problems: []
  edges:
    - from: stage-1
      to: stage-2
      label: cross-modal features
    - from: stage-2
      to: stage-3
      label: selected queries
---

## Core paper explanation

Grounding DINO makes object detection conditional on text. It combines image and language features, uses language to help select object queries, and predicts boxes associated with relevant text spans. Unlike a fixed classifier with one permanent category vocabulary, the text input participates in the detection process. Token-to-phrase alignment is therefore part of the output contract.

## Execution flow

Encode images and text, select language-relevant queries, then decode boxes and resolve token scores into the requested phrases.

### Encode image and text features

**Implement this component:** [Fuse Masked Image and Text Tokens with Bidirectional Cross-Attention](/problems/grounding-bidirectional-cross-attention). The two directions share scores but normalize independently; this bounded single-head component omits learned projections and residual gates.

Let visual features be $V\in\mathbb R^{N\times d}$ and text features $T\in\mathbb R^{L\times d}$. Their compatibility matrix has shape $N\times L$:

$$
S=VT^\top.
$$

Padding and special tokens need explicit masks. [Symmetric CLIP loss](/problems/clip-symmetric-loss) is useful background for image-text compatibility, but Grounding DINO adds spatial and detection-specific processing; it is not just global CLIP retrieval with boxes attached.


**Prerequisite practice:** [Compute Symmetric CLIP Contrastive Loss](/problems/clip-symmetric-loss). These supporting skills do not complete this model stage.


**Planned components:** Fuse Masked Image and Text Tokens with Bidirectional Cross-Attention. These remain unreviewed ideas without runnable exercises.

### Select language-guided queries

A query-ranking abstraction is

$$
r_i=\max_{j:m_j=1}S_{ij},\qquad
\mathcal Q=\operatorname{TopK}_i(r_i).
$$

Here $m_j$ indicates usable text tokens. The paper’s full model includes feature enhancement and a multimodal decoder; this expression isolates the selection concept. Token masks must not let padding win a top-k selection, and tie behavior should be deterministic in a small implementation exercise.


**Implement these components:** [Select Language-Guided Object Queries](/problems/grounding-language-query-selection). Each exercise specifies its bounded scope; diagnostic and simplified variants do not reproduce the full model.

### Resolve boxes to phrases

**Implement this component:** [Evaluate Localization and Phrase Grounding Separately](/problems/grounding-localization-phrase-metrics). Report paired localization and phrase agreement separately; this is not dataset mAP.

If phrase $g$ occupies token set $J_g$, one explicit teaching aggregation is

$$
s_{ig}=\max_{j\in J_g}\sigma(\ell_{ij}),
$$

where $\ell_{ij}$ is a decoded box-query/token logit. This max rule is an example contract, not a universal phrase-calibration law. Token offsets must map back to the original text span correctly. [Pairwise box IoU](/problems/box-iou-broadcast) supports localization evaluation, while phrase correctness requires its own ground-truth associations.


**Prerequisite practice:** [Compute Pairwise Bounding-Box IoU](/problems/box-iou-broadcast). These supporting skills do not complete this model stage.

**Implement these components:** [Map Text Tokens to Grounded Phrases](/problems/grounding-token-phrase-map) · [Decode Phrase-Labeled Boxes](/problems/grounding-phrase-box-decoding) · [Build a Grounded Segmentation Pipeline and Trace Failures](/problems/grounded-segmentation-failure-trace). Each exercise specifies its bounded scope; diagnostic and simplified variants do not reproduce the full model.

**Planned components:** Evaluate Localization and Phrase Grounding Separately. These remain unreviewed ideas without runnable exercises.

#### Preserve alignment through the perception pipeline

[Token-to-phrase mapping](/problems/grounding-token-phrase-map) adopts a declared half-open character-overlap rule. For token interval $[a_t,b_t)$ and phrase interval $[s_p,e_p)$ in the same original Unicode code-point index space,
$$M_{pt}=\mathbf1[\max(a_t,s_p)<\min(b_t,e_p)].$$
Empty/special-token intervals never overlap. This original alignment rule supplies phrase membership; no tokenizer or phrase parser is hidden inside the exercise.

[Decode phrase-labeled boxes](/problems/grounding-phrase-box-decoding) implements the max-token score above, deterministic phrase ties, score thresholding and normalized-center to unclipped pixel-corner conversion. [Grounded segmentation with failure traces](/problems/grounded-segmentation-failure-trace) then composes supplied query-aligned phrase scores and masks. It reports low grounding, low mask quality and empty masks distinctly, and computes accepted mask areas and pixel-center centroids. This is orchestration of synthetic model outputs, not execution of Grounding DINO or SAM, nor evidence of grasp safety.


## Implement the components

- [Fuse Masked Image and Text Tokens with Bidirectional Cross-Attention](/problems/grounding-bidirectional-cross-attention) — Hard.
- [Evaluate Localization and Phrase Grounding Separately](/problems/grounding-localization-phrase-metrics) — Easy.

The following bounded exercises are runnable. They use original synthetic fixtures; completing them does not reproduce the paper's training scale or headline benchmark. Systems diagnostics are explicitly identified as teaching contracts.

- [Map Text Tokens to Grounded Phrases](/problems/grounding-token-phrase-map) — Easy.
- [Select Language-Guided Object Queries](/problems/grounding-language-query-selection) — Medium.
- [Decode Phrase-Labeled Boxes](/problems/grounding-phrase-box-decoding) — Medium.
- [Build a Grounded Segmentation Pipeline and Trace Failures](/problems/grounded-segmentation-failure-trace) — Medium.

## Why this matters on a robot

Language-conditioned detection can identify task-relevant objects from an instruction, but pronouns, spatial relations, and ambiguous noun phrases remain failure modes. A high box/token score is not proof that the detected object is graspable. Preserve text spans and image transforms through the grounding-to-control interface.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2303.05499) · [Open-access manuscript](https://arxiv.org/pdf/2303.05499)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
