---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2023-eureka",
  "paper_id": "2023-eureka",
  "title": "Eureka: Human-Level Reward Design via Coding Large Language Models",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/2310.12931",
  "source_cards": [
    "research/papers/robot-learning-rl/2023-eureka.md"
  ],
  "paper_aliases": [],
  "category": "robot-learning-rl",
  "topics": [
    "robot-learning-rl",
    "eureka"
  ],
  "runnable_problem_slugs": [
    "validation-loss-rollout-ranking"
  ],
  "proposed_component_count": 3,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2023-eureka",
      "node": "stage-1"
    },
    {
      "card": "2023-eureka",
      "node": "stage-2"
    },
    {
      "card": "2023-eureka",
      "node": "stage-3"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# Eureka: Human-Level Reward Design via Coding Large Language Models — implementation track

## Orientation and scope

Eureka uses a language model to generate reward programs, trains policies with those rewards, and feeds performance diagnostics back into reward revision. The language model designs a learning signal; reinforcement learning still produces the motor policy.

The implementation path follows **Generate reward candidates → Train and evaluate policies → Reflect and revise**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/2310.12931) · [Paper explanation and graph](/projects/2023-eureka) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2023-eureka](../../../research/papers/robot-learning-rl/2023-eureka.md).

**Available now:** 0 paper-associated runnable components; 1 supporting runnable component. **Proposed:** 3 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Generate reward candidates** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

- **Supporting prerequisite:** [Compare Validation Loss with Rollout Success](/problems/validation-loss-rollout-ranking). Its own contract remains authoritative; it does not implement the entire paper.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Generate reward candidates

<!-- source-flow: 2023-eureka#stage-1 -->

Use task description and environment code to propose executable rewards.

[Study the mechanism and math](/projects/2023-eureka#paper-section-generate-reward-candidates).

- **Proposed component, not runnable:** Validate a Reward Function Contract.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Train and evaluate policies

<!-- source-flow: 2023-eureka#stage-2 -->

Optimize each reward and score behavior with an independent task metric.

[Study the mechanism and math](/projects/2023-eureka#paper-section-train-and-evaluate-policies).

- **Runnable supporting prerequisite:** [Compare Validation Loss with Rollout Success](/problems/validation-loss-rollout-ranking). Expose when offline-loss ordering disagrees with the ordering of observed rollout success.
- **Proposed component, not runnable:** Rank Reward Candidates by Rollout Evidence.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Reflect and revise

<!-- source-flow: 2023-eureka#stage-3 -->

Use learning curves and reward-component statistics to improve candidates.

[Study the mechanism and math](/projects/2023-eureka#paper-section-reflect-and-revise).

- **Proposed component, not runnable:** Aggregate Reward-Component Diagnostics.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Generate reward candidates | reward programs | Train and evaluate policies |
| Train and evaluate policies | training diagnostics | Reflect and revise |

## Integration exercise

**Proposed exercise — not runnable yet.** Construct a few synthetic episodes containing observations, actions, rewards and termination flags, with known targets or an analytic low-dimensional transition function. Compose the selected mechanisms in the declared flow, beginning with **Generate reward candidates** and ending with **Reflect and revise**. Save each intermediate artifact so a learner can locate a mismatch at its originating stage.

The integration boundary is the selected data, objective and update/evaluation calculations; the tiny fixture is not evidence of successful policy learning on the paper benchmark. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2023-eureka). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** For the **Generate reward candidates → Reflect and revise** fixture, compare returns, losses, action outputs or update targets with an independently computed episode trace; report termination/truncation and task slices explicitly.

Use one clean baseline and a separately recorded fault case: cross an episode boundary, shift an action relative to its observation, or alter one reward/goal label; attribute the resulting metric change. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **Eureka: Human-Level Reward Design via Coding Large Language Models** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record episode alignment, discount/termination rules, action units, train/evaluation split, update order and policy version. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
