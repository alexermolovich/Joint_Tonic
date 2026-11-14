---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2023-rt-2",
  "paper_id": "2023-rt-2",
  "title": "RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/2307.15818",
  "source_cards": [
    "research/papers/vla-embodied/2023-rt-2.md"
  ],
  "paper_aliases": [],
  "category": "vla-embodied",
  "topics": [
    "vision-language-action",
    "action tokens",
    "co-fine-tuning",
    "semantic generalization"
  ],
  "runnable_problem_slugs": [
    "rt1-action-codec",
    "rt2-serialize-action-tokens",
    "rt2-mix-web-robot-batches",
    "rt2-parse-action-grammar",
    "rt2-constrained-action-decoding",
    "rt2-action-generalization-slices"
  ],
  "proposed_component_count": 0,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2023-rt-2",
      "node": "stage-1"
    },
    {
      "card": "2023-rt-2",
      "node": "stage-2"
    },
    {
      "card": "2023-rt-2",
      "node": "stage-3"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control — implementation track

## Orientation and scope

RT-2 adapts pretrained vision-language models into vision-language-action models by expressing robot actions in the model’s output-token space. Training mixes robot demonstrations with vision-language examples so visual and semantic knowledge can influence control predictions. The important interface is the action vocabulary: the text tokenizer, ordered action fields, and physical decoder must agree exactly.

The implementation path follows **Represent actions as tokens → Co-fine-tune the model → Parse and execute actions**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/2307.15818) · [Paper explanation and graph](/projects/2023-rt-2) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2023-rt-2](../../../research/papers/vla-embodied/2023-rt-2.md).

**Available now:** 5 paper-associated runnable components; 1 supporting runnable component. **Proposed:** 0 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Represent actions as tokens** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

- **Supporting prerequisite:** [Quantize and Decode Robot Actions](/problems/rt1-action-codec). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Serialize Robot Actions as Discrete Tokens](/problems/rt2-serialize-action-tokens). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Parse and Validate an Action-Token Grammar](/problems/rt2-parse-action-grammar). Its own contract remains authoritative; it does not implement the entire paper.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Represent actions as tokens

<!-- source-flow: 2023-rt-2#stage-1 -->

Bind bounded action bins to actual tokens in the chosen VLM vocabulary.

[Study the mechanism and math](/projects/2023-rt-2#paper-section-represent-actions-as-tokens).

- **Runnable supporting prerequisite:** [Quantize and Decode Robot Actions](/problems/rt1-action-codec). Scale to [0,1], take floor(bins * scaled), clamp bin IDs to [0,bins-1], add offset, reconstruct bin centers.
- **Runnable paper-associated component:** [Serialize Robot Actions as Discrete Tokens](/problems/rt2-serialize-action-tokens). Serialize Robot Actions as Discrete Tokens

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Co-fine-tune the model

<!-- source-flow: 2023-rt-2#stage-2 -->

Train robot-action sequences alongside retained vision-language examples.

[Study the mechanism and math](/projects/2023-rt-2#paper-section-co-fine-tune-the-model).

- **Runnable paper-associated component:** [Mix Web and Robot Batches at a Target Ratio](/problems/rt2-mix-web-robot-batches). Co-training mixes robot examples with web supervision, but a ratio alone does not specify finite batch rounding or what happens when a source is small.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Parse and execute actions

<!-- source-flow: 2023-rt-2#stage-3 -->

Validate field order, category membership, and physical command bounds.

[Study the mechanism and math](/projects/2023-rt-2#paper-section-parse-and-execute-actions).

- **Runnable paper-associated component:** [Parse and Validate an Action-Token Grammar](/problems/rt2-parse-action-grammar). Parse and Validate an Action-Token Grammar
- **Runnable paper-associated component:** [Constrain Autoregressive Decoding to Valid Actions](/problems/rt2-constrained-action-decoding). Mask language-model logits to valid action tokens and decode one deterministic action field.
- **Runnable paper-associated component:** [Monitor Invalid Actions and Semantic Generalization Slices](/problems/rt2-action-generalization-slices). An overall success percentage can hide a policy that emits malformed commands on unfamiliar instructions.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Represent actions as tokens | action-token targets | Co-fine-tune the model |
| Co-fine-tune the model | generated tokens | Parse and execute actions |

## Integration exercise

**Proposed exercise — not runnable yet.** Choose a tiny injective token vocabulary, two bounded action examples and fixed robot/web target records. Serialize action fields, form a declared task mixture and parse synthetic model outputs back into named fields. The vocabulary is an educational grammar, not a claim to reproduce either RT-2 pretrained tokenizer.

The integration boundary is selected observation-to-action mechanisms with supplied features and deterministic model callbacks; a learned robot policy and real-world success claims are outside scope. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2023-rt-2). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** Check serializer/parser round trips, mixture counts and rejection of unknown or misplaced tokens. Keep semantic task accuracy separate from grammar validity; a syntactically valid command can still be physically inappropriate.

Use one clean baseline and a separately recorded fault case: remove a modality, alter one action scale, or delay an observation; identify the exact component that rejects or masks the inconsistent input. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record action bounds and units, embodiment channel mapping, control period, observation/action horizon, normalization statistics and model-call schedule. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
