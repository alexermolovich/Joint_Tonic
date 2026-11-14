---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2022-code-as-policies",
  "paper_id": "2022-code-as-policies",
  "title": "Code as Policies: Language Model Programs for Embodied Control",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/2209.07753",
  "source_cards": [
    "research/papers/vla-generalist/2022-code-as-policies.md"
  ],
  "paper_aliases": [],
  "category": "vla-generalist",
  "topics": [
    "vla-generalist",
    "code-as-policies"
  ],
  "runnable_problem_slugs": [
    "se3-transform-points"
  ],
  "proposed_component_count": 3,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2022-code-as-policies",
      "node": "stage-1"
    },
    {
      "card": "2022-code-as-policies",
      "node": "stage-2"
    },
    {
      "card": "2022-code-as-policies",
      "node": "stage-3"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# Code as Policies: Language Model Programs for Embodied Control — implementation track

## Orientation and scope

Code as Policies uses language-model-generated programs to compose robot perception and control APIs. The generated policy can express geometry, branching, loops, and helper functions, rather than selecting only a single predefined skill.

The implementation path follows **Generate a policy program → Expand helper functions → Execute grounded operations**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/2209.07753) · [Paper explanation and graph](/projects/2022-code-as-policies) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2022-code-as-policies](../../../research/papers/vla-generalist/2022-code-as-policies.md).

**Available now:** 0 paper-associated runnable components; 1 supporting runnable component. **Proposed:** 3 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Generate a policy program** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

- **Supporting prerequisite:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). Its own contract remains authoritative; it does not implement the entire paper.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Generate a policy program

<!-- source-flow: 2022-code-as-policies#stage-1 -->

Translate a task and API context into program tokens.

[Study the mechanism and math](/projects/2022-code-as-policies#paper-section-generate-a-policy-program).

- **Proposed component, not runnable:** Validate a Restricted Robot Program AST.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Expand helper functions

<!-- source-flow: 2022-code-as-policies#stage-2 -->

Recursively define missing functions.

[Study the mechanism and math](/projects/2022-code-as-policies#paper-section-expand-helper-functions).

- **Proposed component, not runnable:** Trace a Composed Robot Policy.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Execute grounded operations

<!-- source-flow: 2022-code-as-policies#stage-3 -->

Call perception and motion primitives with live state.

[Study the mechanism and math](/projects/2022-code-as-policies#paper-section-execute-grounded-operations).

- **Runnable supporting prerequisite:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). Move camera-frame points into the world frame using a rigid transform.
- **Proposed component, not runnable:** Resolve Perception Results into Control Calls.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Generate a policy program | generated program | Expand helper functions |
| Expand helper functions | resolved functions | Execute grounded operations |

## Integration exercise

**Proposed exercise — not runnable yet.** Construct a small synthetic instruction/observation stream and structured action or skill records for two task contexts; use fixed model scores or deterministic callbacks. Compose the selected mechanisms in the declared flow, beginning with **Generate a policy program** and ending with **Execute grounded operations**. Save each intermediate artifact so a learner can locate a mismatch at its originating stage.

The integration boundary is the named representation, conditioning and output/control interface; language reasoning quality, large-model training and physical task completion are outside scope. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2022-code-as-policies). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** For the **Generate a policy program → Execute grounded operations** fixture, verify each decision against explicit token, skill or action targets and record intermediate conditioning state; evaluate grammar, ordering and latency independently.

Use one clean baseline and a separately recorded fault case: change a task identifier, deliver stale context, or supply an invalid output field; ensure the control interface never silently shifts semantics. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **Code as Policies: Language Model Programs for Embodied Control** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record task/skill vocabulary, action schema, model callback behavior, context freshness policy, chunk schedule and decoder version. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
