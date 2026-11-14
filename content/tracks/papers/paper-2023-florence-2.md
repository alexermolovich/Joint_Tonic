---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2023-florence-2",
  "paper_id": "2023-florence-2",
  "title": "Florence-2: Advancing a Unified Representation for a Variety of Vision Tasks",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/2311.06242",
  "source_cards": [
    "research/papers/vlm-grounding/2023-florence-2.md"
  ],
  "paper_aliases": [],
  "category": "vlm-grounding",
  "topics": [
    "vlm-grounding",
    "florence-2"
  ],
  "runnable_problem_slugs": [],
  "proposed_component_count": 3,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2023-florence-2",
      "node": "stage-1"
    },
    {
      "card": "2023-florence-2",
      "node": "stage-2"
    },
    {
      "card": "2023-florence-2",
      "node": "stage-3"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# Florence-2: Advancing a Unified Representation for a Variety of Vision Tasks — implementation track

## Orientation and scope

Florence-2 represents diverse vision tasks as prompted sequence generation. Its vocabulary contains location tokens, allowing one encoder–decoder to describe images and produce structured boxes, OCR quadrilaterals, or polygons.

The implementation path follows **Encode task and image → Generate spatial tokens → Train and parse outputs**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/2311.06242) · [Paper explanation and graph](/projects/2023-florence-2) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2023-florence-2](../../../research/papers/vlm-grounding/2023-florence-2.md).

**Available now:** 0 paper-associated runnable components; 0 supporting runnable components. **Proposed:** 3 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Encode task and image** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

There is no independently runnable prerequisite mapped for this source yet. Use the source-card notation and stage contracts as the diagnostic; prerequisite exercises must be authored and reviewed before being presented as runnable.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Encode task and image

<!-- source-flow: 2023-florence-2#stage-1 -->

Combine visual evidence with the requested task.

[Study the mechanism and math](/projects/2023-florence-2#paper-section-encode-task-and-image).

- **Proposed component, not runnable:** Route Task Prompts to Output Schemas.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Generate spatial tokens

<!-- source-flow: 2023-florence-2#stage-2 -->

Represent coordinates inside the output vocabulary.

[Study the mechanism and math](/projects/2023-florence-2#paper-section-generate-spatial-tokens).

- **Proposed component, not runnable:** Normalize Spatial Coordinates into Tokens.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Train and parse outputs

<!-- source-flow: 2023-florence-2#stage-3 -->

Apply token loss, then validate the task grammar.

[Study the mechanism and math](/projects/2023-florence-2#paper-section-train-and-parse-outputs).

- **Proposed component, not runnable:** Parse Structured Detection Tokens.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Encode task and image | multimodal context | Generate spatial tokens |
| Generate spatial tokens | text and location tokens | Train and parse outputs |

## Integration exercise

**Proposed exercise — not runnable yet.** Construct synthetic image/region features, a small declared token vocabulary and hand-authored phrase-to-region or answer labels. Compose the selected mechanisms in the declared flow, beginning with **Encode task and image** and ending with **Train and parse outputs**. Save each intermediate artifact so a learner can locate a mismatch at its originating stage.

The integration boundary is the model interface, attention/label structure and selected objective or decoding logic; fluent language generation and real-image generalization are outside the fixture. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2023-florence-2). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** For the **Encode task and image → Train and parse outputs** fixture, check exact token/region correspondence and masks first, then compare loss or retrieval/grounding metrics with a small enumerated oracle.

Use one clean baseline and a separately recorded fault case: swap an image-text pairing, truncate a phrase, or introduce an unavailable region; report affected labels, masks and per-query scores. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **Florence-2: Advancing a Unified Representation for a Variety of Vision Tasks** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record tokenizer/vocabulary mapping, image feature schema, text spans, label masks, prompt template and normalization. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
