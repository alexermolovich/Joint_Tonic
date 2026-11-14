---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2021-clip",
  "paper_id": "2021-clip",
  "title": "Learning Transferable Visual Models From Natural Language Supervision",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/2103.00020",
  "source_cards": [
    "research/papers/vision-vlm-3d/2021-clip.md"
  ],
  "paper_aliases": [],
  "category": "vision-vlm-3d",
  "topics": [
    "vision-language models",
    "contrastive learning",
    "zero-shot transfer",
    "multimodal embeddings"
  ],
  "runnable_problem_slugs": [
    "clip-normalize-embeddings",
    "clip-symmetric-loss",
    "clip-retrieval-recall",
    "clip-prompt-ensemble",
    "clip-prompt-class-drift"
  ],
  "proposed_component_count": 0,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2021-clip",
      "node": "stage-1"
    },
    {
      "card": "2021-clip",
      "node": "stage-2"
    },
    {
      "card": "2021-clip",
      "node": "stage-3"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# Learning Transferable Visual Models From Natural Language Supervision — implementation track

## Orientation and scope

CLIP learns an image encoder and a text encoder by asking which caption matches each image in a batch. It maps both modalities into a shared space where paired examples should have larger similarity than mismatched examples. Once learned, that space supports image-text retrieval and classifiers made from text descriptions. The essential mechanism is the two-direction contrastive objective; the semantics available at deployment also depend strongly on the training data and prompt wording.

The implementation path follows **Encode and normalize → Train on paired similarities → Retrieve or classify**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/2103.00020) · [Paper explanation and graph](/projects/2021-clip) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2021-clip](../../../research/papers/vision-vlm-3d/2021-clip.md).

**Available now:** 5 paper-associated runnable components; 0 supporting runnable components. **Proposed:** 0 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Encode and normalize** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

- **Supporting prerequisite:** [Normalize Image and Text Embeddings](/problems/clip-normalize-embeddings). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Build a Prompt-Ensembled Zero-Shot Classifier](/problems/clip-prompt-ensemble). Its own contract remains authoritative; it does not implement the entire paper.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Encode and normalize

<!-- source-flow: 2021-clip#stage-1 -->

Map images and text into equal-width, unit-length embeddings.

[Study the mechanism and math](/projects/2021-clip#paper-section-encode-and-normalize).

- **Runnable paper-associated component:** [Normalize Image and Text Embeddings](/problems/clip-normalize-embeddings). Normalize paired image and text feature rows while preserving the PyTorch gradient path.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Train on paired similarities

<!-- source-flow: 2021-clip#stage-2 -->

Use each diagonal pair as a positive in both retrieval directions.

[Study the mechanism and math](/projects/2021-clip#paper-section-train-on-paired-similarities).

- **Runnable paper-associated component:** [Compute Symmetric CLIP Contrastive Loss](/problems/clip-symmetric-loss). Normalize rows, form image/text dot-product logits divided by temperature, and average cross-entropy in both directions.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Retrieve or classify

<!-- source-flow: 2021-clip#stage-3 -->

Compare an image against candidate text descriptions.

[Study the mechanism and math](/projects/2021-clip#paper-section-retrieve-or-classify).

- **Runnable paper-associated component:** [Evaluate Cross-Modal Retrieval Recall at K](/problems/clip-retrieval-recall). Evaluate Cross-Modal Retrieval Recall at K
- **Runnable paper-associated component:** [Build a Prompt-Ensembled Zero-Shot Classifier](/problems/clip-prompt-ensemble). Build a Prompt-Ensembled Zero-Shot Classifier
- **Runnable paper-associated component:** [Detect Prompt and Class Distribution Drift](/problems/clip-prompt-class-drift). Separate changed text prototypes from changed predicted-class frequencies.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Encode and normalize | unit embeddings | Train on paired similarities |
| Train on paired similarities | trained encoders | Retrieve or classify |

## Integration exercise

**Proposed exercise — not runnable yet.** Start from a small paired image/text embedding table. Normalize features, compute the symmetric contrastive objective and retrieve matching partners; a proposed prompt ensemble can extend the same fixture to class prototypes. Learned encoders are supplied features rather than claimed reproductions.

The integration boundary is a small perception component pipeline with supplied model outputs or tiny original weights; pretrained feature quality and paper-scale training are outside this exercise. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2021-clip). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** Check both retrieval directions, duplicate-similarity ties and a swapped pairing. Compare per-prompt normalization followed by mean-and-renormalize against the explicitly incorrect normalize-only-after-averaging baseline once that component is reviewed.

Use one clean baseline and a separately recorded fault case: permute an input ordering, corrupt one coordinate convention, or remove a valid observation; check the method-specific invariance or rejection rule. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **Learning Transferable Visual Models From Natural Language Supervision** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record image/ray/box conventions, normalization, feature widths, class mapping, numeric tolerances and fixture seed. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
