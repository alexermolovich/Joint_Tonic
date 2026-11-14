---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2021-cliport",
  "paper_id": "2021-cliport",
  "title": "CLIPort: What and Where Pathways for Robotic Manipulation",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/2109.12098",
  "source_cards": [
    "research/papers/robot-learning-rl/2021-cliport.md"
  ],
  "paper_aliases": [],
  "category": "robot-learning-rl",
  "topics": [
    "robot-learning-rl",
    "cliport"
  ],
  "runnable_problem_slugs": [],
  "proposed_component_count": 5,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2021-cliport",
      "node": "stage-1"
    },
    {
      "card": "2021-cliport",
      "node": "stage-2"
    },
    {
      "card": "2021-cliport",
      "node": "stage-3"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# CLIPort: What and Where Pathways for Robotic Manipulation — implementation track

## Orientation and scope

CLIPort combines pretrained vision-language semantics with the spatial action structure of Transporter Networks. One pathway supplies what an instruction refers to, while another preserves the spatial detail needed for precise manipulation.

The implementation path follows **Encode semantic instructions → Fuse spatial and semantic streams → Imitate language-conditioned actions**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/2109.12098) · [Paper explanation and graph](/projects/2021-cliport) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2021-cliport](../../../research/papers/robot-learning-rl/2021-cliport.md).

**Available now:** 0 paper-associated runnable components; 0 supporting runnable components. **Proposed:** 5 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Encode semantic instructions** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

There is no independently runnable prerequisite mapped for this source yet. Use the source-card notation and stage contracts as the diagnostic; prerequisite exercises must be authored and reviewed before being presented as runnable.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Encode semantic instructions

<!-- source-flow: 2021-cliport#stage-1 -->

Use pretrained CLIP representations for visual-language meaning.

[Study the mechanism and math](/projects/2021-cliport#paper-section-encode-semantic-instructions).

- **Proposed component, not runnable:** Align Instruction Embeddings with Manipulation Observations.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Fuse spatial and semantic streams

<!-- source-flow: 2021-cliport#stage-2 -->

Combine language-aware features with precise scene geometry.

[Study the mechanism and math](/projects/2021-cliport#paper-section-fuse-spatial-and-semantic-streams).

- **Proposed component, not runnable:** Fuse Semantic and Spatial Feature Streams.
- **Proposed component, not runnable:** Condition a Place Map on a Language Goal.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Imitate language-conditioned actions

<!-- source-flow: 2021-cliport#stage-3 -->

Train pick and placement classification from demonstrations.

[Study the mechanism and math](/projects/2021-cliport#paper-section-imitate-language-conditioned-actions).

- **Proposed component, not runnable:** Compute Language-Conditioned Pick-and-Place Cross-Entropy.
- **Proposed component, not runnable:** Evaluate Compositional Manipulation Slices.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Encode semantic instructions | semantic features | Fuse spatial and semantic streams |
| Fuse spatial and semantic streams | fused action maps | Imitate language-conditioned actions |

## Integration exercise

**Proposed exercise — not runnable yet.** Construct a few synthetic episodes containing observations, actions, rewards and termination flags, with known targets or an analytic low-dimensional transition function. Compose the selected mechanisms in the declared flow, beginning with **Encode semantic instructions** and ending with **Imitate language-conditioned actions**. Save each intermediate artifact so a learner can locate a mismatch at its originating stage.

The integration boundary is the selected data, objective and update/evaluation calculations; the tiny fixture is not evidence of successful policy learning on the paper benchmark. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2021-cliport). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** For the **Encode semantic instructions → Imitate language-conditioned actions** fixture, compare returns, losses, action outputs or update targets with an independently computed episode trace; report termination/truncation and task slices explicitly.

Use one clean baseline and a separately recorded fault case: cross an episode boundary, shift an action relative to its observation, or alter one reward/goal label; attribute the resulting metric change. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **CLIPort: What and Where Pathways for Robotic Manipulation** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record episode alignment, discount/termination rules, action units, train/evaluation split, update order and policy version. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
