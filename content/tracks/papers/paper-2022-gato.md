---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2022-gato",
  "paper_id": "2022-gato",
  "title": "A Generalist Agent",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/2205.06175",
  "source_cards": [
    "research/papers/vla-generalist/2022-gato.md"
  ],
  "paper_aliases": [],
  "category": "vla-generalist",
  "topics": [
    "vla-generalist",
    "gato"
  ],
  "runnable_problem_slugs": [],
  "proposed_component_count": 3,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2022-gato",
      "node": "stage-1"
    },
    {
      "card": "2022-gato",
      "node": "stage-2"
    },
    {
      "card": "2022-gato",
      "node": "stage-3"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# A Generalist Agent — implementation track

## Orientation and scope

Gato casts diverse text, visual, and embodied tasks into sequences processed by one causal transformer. Modality-specific tokenization and carefully masked output supervision make a shared model possible without pretending every input has the same semantics.

The implementation path follows **Serialize observations and actions → Train masked prediction → Decode an action sequence**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/2205.06175) · [Paper explanation and graph](/projects/2022-gato) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2022-gato](../../../research/papers/vla-generalist/2022-gato.md).

**Available now:** 0 paper-associated runnable components; 0 supporting runnable components. **Proposed:** 3 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Serialize observations and actions** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

There is no independently runnable prerequisite mapped for this source yet. Use the source-card notation and stage contracts as the diagnostic; prerequisite exercises must be authored and reviewed before being presented as runnable.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Serialize observations and actions

<!-- source-flow: 2022-gato#stage-1 -->

Preserve modality and temporal ordering.

[Study the mechanism and math](/projects/2022-gato#paper-section-serialize-observations-and-actions).

- **Proposed component, not runnable:** Tokenize Mixed Observation Modalities.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Train masked prediction

<!-- source-flow: 2022-gato#stage-2 -->

Supervise actions and text, not every observation token.

[Study the mechanism and math](/projects/2022-gato#paper-section-train-masked-prediction).

- **Proposed component, not runnable:** Build Task-Aware Sequence Masks.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Decode an action sequence

<!-- source-flow: 2022-gato#stage-3 -->

Generate the next action under the current embodiment contract.

[Study the mechanism and math](/projects/2022-gato#paper-section-decode-an-action-sequence).

- **Proposed component, not runnable:** Decode Actions from a Shared Token Space.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Serialize observations and actions | multimodal sequence | Train masked prediction |
| Train masked prediction | trained transformer | Decode an action sequence |

## Integration exercise

**Proposed exercise — not runnable yet.** Construct a small synthetic instruction/observation stream and structured action or skill records for two task contexts; use fixed model scores or deterministic callbacks. Compose the selected mechanisms in the declared flow, beginning with **Serialize observations and actions** and ending with **Decode an action sequence**. Save each intermediate artifact so a learner can locate a mismatch at its originating stage.

The integration boundary is the named representation, conditioning and output/control interface; language reasoning quality, large-model training and physical task completion are outside scope. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2022-gato). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** For the **Serialize observations and actions → Decode an action sequence** fixture, verify each decision against explicit token, skill or action targets and record intermediate conditioning state; evaluate grammar, ordering and latency independently.

Use one clean baseline and a separately recorded fault case: change a task identifier, deliver stale context, or supply an invalid output field; ensure the control interface never silently shifts semantics. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **A Generalist Agent** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record task/skill vocabulary, action schema, model callback behavior, context freshness policy, chunk schedule and decoder version. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
