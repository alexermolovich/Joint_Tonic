---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2022-vima",
  "paper_id": "2022-vima",
  "title": "VIMA: General Robot Manipulation with Multimodal Prompts",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/2210.03094",
  "source_cards": [
    "research/papers/vla-generalist/2022-vima.md"
  ],
  "paper_aliases": [],
  "category": "vla-generalist",
  "topics": [
    "vla-generalist",
    "vima"
  ],
  "runnable_problem_slugs": [],
  "proposed_component_count": 3,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2022-vima",
      "node": "stage-1"
    },
    {
      "card": "2022-vima",
      "node": "stage-2"
    },
    {
      "card": "2022-vima",
      "node": "stage-3"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# VIMA: General Robot Manipulation with Multimodal Prompts — implementation track

## Orientation and scope

VIMA learns manipulation from prompts that interleave language and visual examples. Object-centric representations and cross-attention to the prompt support task specifications such as matching an example object or reproducing a demonstrated arrangement.

The implementation path follows **Tokenize objects and prompts → Condition the policy → Imitate manipulation actions**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/2210.03094) · [Paper explanation and graph](/projects/2022-vima) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2022-vima](../../../research/papers/vla-generalist/2022-vima.md).

**Available now:** 0 paper-associated runnable components; 0 supporting runnable components. **Proposed:** 3 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Tokenize objects and prompts** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

There is no independently runnable prerequisite mapped for this source yet. Use the source-card notation and stage contracts as the diagnostic; prerequisite exercises must be authored and reviewed before being presented as runnable.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Tokenize objects and prompts

<!-- source-flow: 2022-vima#stage-1 -->

Represent detected objects and interleaved instructions.

[Study the mechanism and math](/projects/2022-vima#paper-section-tokenize-objects-and-prompts).

- **Proposed component, not runnable:** Build Object-Centric Prompt Tokens.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Condition the policy

<!-- source-flow: 2022-vima#stage-2 -->

Attend to prompt tokens while modeling interaction history.

[Study the mechanism and math](/projects/2022-vima#paper-section-condition-the-policy).

- **Proposed component, not runnable:** Collate Interleaved Multimodal Prompts.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Imitate manipulation actions

<!-- source-flow: 2022-vima#stage-3 -->

Predict structured action distributions from demonstrations.

[Study the mechanism and math](/projects/2022-vima#paper-section-imitate-manipulation-actions).

- **Proposed component, not runnable:** Decode Structured Manipulation Actions.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Tokenize objects and prompts | object tokens | Condition the policy |
| Condition the policy | conditioned history | Imitate manipulation actions |

## Integration exercise

**Proposed exercise — not runnable yet.** Construct a small synthetic instruction/observation stream and structured action or skill records for two task contexts; use fixed model scores or deterministic callbacks. Compose the selected mechanisms in the declared flow, beginning with **Tokenize objects and prompts** and ending with **Imitate manipulation actions**. Save each intermediate artifact so a learner can locate a mismatch at its originating stage.

The integration boundary is the named representation, conditioning and output/control interface; language reasoning quality, large-model training and physical task completion are outside scope. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2022-vima). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** For the **Tokenize objects and prompts → Imitate manipulation actions** fixture, verify each decision against explicit token, skill or action targets and record intermediate conditioning state; evaluate grammar, ordering and latency independently.

Use one clean baseline and a separately recorded fault case: change a task identifier, deliver stale context, or supply an invalid output field; ensure the control interface never silently shifts semantics. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **VIMA: General Robot Manipulation with Multimodal Prompts** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record task/skill vocabulary, action schema, model callback behavior, context freshness policy, chunk schedule and decoder version. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
