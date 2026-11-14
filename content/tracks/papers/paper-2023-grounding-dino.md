---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2023-grounding-dino",
  "paper_id": "2023-grounding-dino",
  "title": "Grounding DINO: Marrying DINO with Grounded Pre-Training for Open-Set Object Detection",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/2303.05499",
  "source_cards": [
    "research/papers/vision-vlm-3d/2023-grounding-dino.md"
  ],
  "paper_aliases": [],
  "category": "vision-vlm-3d",
  "topics": [
    "open-set detection",
    "phrase grounding",
    "vision-language fusion",
    "object detection"
  ],
  "runnable_problem_slugs": [
    "grounding-language-query-selection",
    "grounding-token-phrase-map",
    "grounding-phrase-box-decoding",
    "grounded-segmentation-failure-trace"
  ],
  "proposed_component_count": 2,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2023-grounding-dino",
      "node": "stage-1"
    },
    {
      "card": "2023-grounding-dino",
      "node": "stage-2"
    },
    {
      "card": "2023-grounding-dino",
      "node": "stage-3"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# Grounding DINO: Marrying DINO with Grounded Pre-Training for Open-Set Object Detection — implementation track

## Orientation and scope

Grounding DINO makes object detection conditional on text. It combines image and language features, uses language to help select object queries, and predicts boxes associated with relevant text spans. Unlike a fixed classifier with one permanent category vocabulary, the text input participates in the detection process. Token-to-phrase alignment is therefore part of the output contract.

The implementation path follows **Encode image and text features → Select language-guided queries → Resolve boxes to phrases**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/2303.05499) · [Paper explanation and graph](/projects/2023-grounding-dino) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2023-grounding-dino](../../../research/papers/vision-vlm-3d/2023-grounding-dino.md).

**Available now:** 4 paper-associated runnable components; 0 supporting runnable components. **Proposed:** 2 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Encode image and text features** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

- **Supporting prerequisite:** [Map Text Tokens to Grounded Phrases](/problems/grounding-token-phrase-map). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Decode Phrase-Labeled Boxes](/problems/grounding-phrase-box-decoding). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Rank Candidate Masks with Predicted IoU](/problems/sam-mask-ranking). Its own contract remains authoritative; it does not implement the entire paper.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Encode image and text features

<!-- source-flow: 2023-grounding-dino#stage-1 -->

Represent spatial image tokens and valid language tokens for fusion.

[Study the mechanism and math](/projects/2023-grounding-dino#paper-section-encode-image-and-text-features).

- **Proposed component, not runnable:** Fuse Masked Image and Text Tokens with Bidirectional Cross-Attention.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Select language-guided queries

<!-- source-flow: 2023-grounding-dino#stage-2 -->

Use compatibility with valid text tokens to prioritize candidate image locations.

[Study the mechanism and math](/projects/2023-grounding-dino#paper-section-select-language-guided-queries).

- **Runnable paper-associated component:** [Select Language-Guided Object Queries](/problems/grounding-language-query-selection). Select visual queries by their strongest usable text-token compatibility.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Resolve boxes to phrases

<!-- source-flow: 2023-grounding-dino#stage-3 -->

Decode spatial predictions and aggregate scores over the requested phrase spans.

[Study the mechanism and math](/projects/2023-grounding-dino#paper-section-resolve-boxes-to-phrases).

- **Runnable paper-associated component:** [Map Text Tokens to Grounded Phrases](/problems/grounding-token-phrase-map). Map character spans to tokens with an explicit half-open overlap rule.
- **Runnable paper-associated component:** [Decode Phrase-Labeled Boxes](/problems/grounding-phrase-box-decoding). Associate each normalized box with its strongest phrase, then return thresholded pixel boxes.
- **Runnable paper-associated component:** [Build a Grounded Segmentation Pipeline and Trace Failures](/problems/grounded-segmentation-failure-trace). Compose supplied grounding and segmentation outputs while preserving failure reasons per query.
- **Proposed component, not runnable:** Evaluate Localization and Phrase Grounding Separately.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Encode image and text features | cross-modal features | Select language-guided queries |
| Select language-guided queries | selected queries | Resolve boxes to phrases |

## Integration exercise

**Proposed exercise — not runnable yet.** Construct small synthetic images, boxes, embeddings or rays chosen to match the first mechanism; retain ground-truth geometry and any correspondence labels. Compose the selected mechanisms in the declared flow, beginning with **Encode image and text features** and ending with **Resolve boxes to phrases**. Save each intermediate artifact so a learner can locate a mismatch at its originating stage.

The integration boundary is a small perception component pipeline with supplied model outputs or tiny original weights; pretrained feature quality and paper-scale training are outside this exercise. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2023-grounding-dino). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** For the **Encode image and text features → Resolve boxes to phrases** fixture, compare tensor outputs with an independent scalar or exhaustive oracle and report the relevant matching, reconstruction or retrieval metric on the declared synthetic labels.

Use one clean baseline and a separately recorded fault case: permute an input ordering, corrupt one coordinate convention, or remove a valid observation; check the method-specific invariance or rejection rule. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **Grounding DINO: Marrying DINO with Grounded Pre-Training for Open-Set Object Detection** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record image/ray/box conventions, normalization, feature widths, class mapping, numeric tolerances and fixture seed. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
