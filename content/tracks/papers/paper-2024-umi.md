---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2024-umi",
  "paper_id": "2024-umi",
  "title": "Universal Manipulation Interface: In-The-Wild Robot Teaching Without In-The-Wild Robots",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/2402.10329",
  "source_cards": [
    "research/papers/robot-learning-rl/2024-umi.md"
  ],
  "paper_aliases": [],
  "category": "robot-learning-rl",
  "topics": [
    "robot-learning-rl",
    "umi"
  ],
  "runnable_problem_slugs": [
    "se3-transform-points"
  ],
  "proposed_component_count": 3,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2024-umi",
      "node": "stage-1"
    },
    {
      "card": "2024-umi",
      "node": "stage-2"
    },
    {
      "card": "2024-umi",
      "node": "stage-3"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# Universal Manipulation Interface: In-The-Wild Robot Teaching Without In-The-Wild Robots — implementation track

## Orientation and scope

Universal Manipulation Interface collects demonstrations with a handheld gripper and transfers them to robot policies through a shared sensing/action interface. Relative trajectories and latency matching reduce dependence on one fixed robot installation.

The implementation path follows **Capture handheld demonstrations → Represent relative action chunks → Match timing at deployment**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/2402.10329) · [Paper explanation and graph](/projects/2024-umi) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2024-umi](../../../research/papers/robot-learning-rl/2024-umi.md).

**Available now:** 0 paper-associated runnable components; 1 supporting runnable component. **Proposed:** 3 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Capture handheld demonstrations** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

- **Supporting prerequisite:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). Its own contract remains authoritative; it does not implement the entire paper.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Capture handheld demonstrations

<!-- source-flow: 2024-umi#stage-1 -->

Record camera observations, gripper motion, and timing.

[Study the mechanism and math](/projects/2024-umi#paper-section-capture-handheld-demonstrations).

- **Runnable supporting prerequisite:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). Move camera-frame points into the world frame using a rigid transform.
- **Proposed component, not runnable:** Validate a Demonstration Replay Bundle.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Represent relative action chunks

<!-- source-flow: 2024-umi#stage-2 -->

Express future motion relative to the current gripper pose.

[Study the mechanism and math](/projects/2024-umi#paper-section-represent-relative-action-chunks).

- **Proposed component, not runnable:** Transform Demonstrations into a Shared Tool Frame.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Match timing at deployment

<!-- source-flow: 2024-umi#stage-3 -->

Align camera, inference, and actuator delays before execution.

[Study the mechanism and math](/projects/2024-umi#paper-section-match-timing-at-deployment).

- **Proposed component, not runnable:** Align Camera and Gripper Timestamps.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Capture handheld demonstrations | tracked trajectories | Represent relative action chunks |
| Represent relative action chunks | predicted relative chunks | Match timing at deployment |

## Integration exercise

**Proposed exercise — not runnable yet.** Construct a few synthetic episodes containing observations, actions, rewards and termination flags, with known targets or an analytic low-dimensional transition function. Compose the selected mechanisms in the declared flow, beginning with **Capture handheld demonstrations** and ending with **Match timing at deployment**. Save each intermediate artifact so a learner can locate a mismatch at its originating stage.

The integration boundary is the selected data, objective and update/evaluation calculations; the tiny fixture is not evidence of successful policy learning on the paper benchmark. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2024-umi). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** For the **Capture handheld demonstrations → Match timing at deployment** fixture, compare returns, losses, action outputs or update targets with an independently computed episode trace; report termination/truncation and task slices explicitly.

Use one clean baseline and a separately recorded fault case: cross an episode boundary, shift an action relative to its observation, or alter one reward/goal label; attribute the resulting metric change. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **Universal Manipulation Interface: In-The-Wild Robot Teaching Without In-The-Wild Robots** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record episode alignment, discount/termination rules, action units, train/evaluation split, update order and policy version. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
