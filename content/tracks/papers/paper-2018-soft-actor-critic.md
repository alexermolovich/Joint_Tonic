---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2018-soft-actor-critic",
  "paper_id": "2018-soft-actor-critic",
  "title": "Soft Actor-Critic: Off-Policy Maximum Entropy Deep Reinforcement Learning with a Stochastic Actor",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/1801.01290",
  "source_cards": [
    "research/papers/robot-learning-rl/2018-soft-actor-critic.md"
  ],
  "paper_aliases": [],
  "category": "robot-learning-rl",
  "topics": [
    "robot-learning-rl",
    "soft-actor-critic"
  ],
  "runnable_problem_slugs": [
    "sac-soft-state-value",
    "soft-value-bellman-target",
    "sac-tanh-logprob-correction",
    "sac-temperature-objective-update"
  ],
  "proposed_component_count": 0,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2018-soft-actor-critic",
      "node": "stage-1"
    },
    {
      "card": "2018-soft-actor-critic",
      "node": "stage-2"
    },
    {
      "card": "2018-soft-actor-critic",
      "node": "stage-3"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# Soft Actor-Critic: Off-Policy Maximum Entropy Deep Reinforcement Learning with a Stochastic Actor — implementation track

## Orientation and scope

Soft Actor-Critic learns a stochastic continuous-control policy with entropy-regularized value learning and off-policy replay. The original paper includes a separate soft value network; later SAC variants often eliminate it.

The implementation path follows **Define entropy-regularized value → Fit soft critic targets → Improve the stochastic actor**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/1801.01290) · [Paper explanation and graph](/projects/2018-soft-actor-critic) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2018-soft-actor-critic](../../../research/papers/robot-learning-rl/2018-soft-actor-critic.md).

**Available now:** 4 paper-associated runnable components; 0 supporting runnable components. **Proposed:** 0 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Define entropy-regularized value** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

There is no independently runnable prerequisite mapped for this source yet. Use the source-card notation and stage contracts as the diagnostic; prerequisite exercises must be authored and reviewed before being presented as runnable.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Define entropy-regularized value

<!-- source-flow: 2018-soft-actor-critic#stage-1 -->

Reward both task performance and policy entropy.

[Study the mechanism and math](/projects/2018-soft-actor-critic#paper-section-define-entropy-regularized-value).

- **Runnable paper-associated component:** [Compute an Entropy-Regularized State Value](/problems/sac-soft-state-value). A stochastic robot policy values both task reward and action entropy.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Fit soft critic targets

<!-- source-flow: 2018-soft-actor-critic#stage-2 -->

Bootstrap from a target soft-value estimate.

[Study the mechanism and math](/projects/2018-soft-actor-critic#paper-section-fit-soft-critic-targets).

- **Runnable paper-associated component:** [Compute an Entropy-Regularized Bellman Target](/problems/soft-value-bellman-target). One-step critic targets combine immediate reward with a value estimate of the next physical state.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Improve the stochastic actor

<!-- source-flow: 2018-soft-actor-critic#stage-3 -->

Trade high value against entropy using reparameterized actions.

[Study the mechanism and math](/projects/2018-soft-actor-critic#paper-section-improve-the-stochastic-actor).

- **Runnable paper-associated component:** [Apply Tanh Action Log-Probability Correction](/problems/sac-tanh-logprob-correction). Squashing a Gaussian sample into an action interval changes its probability density.
- **Runnable paper-associated component:** [Update a Temperature Objective (later SAC extension)](/problems/sac-temperature-objective-update). The entropy temperature should increase when the sampled policy is less random than the declared target and decrease when it is more random.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Define entropy-regularized value | replay transitions | Fit soft critic targets |
| Fit soft critic targets | critic estimates | Improve the stochastic actor |

## Integration exercise

**Proposed exercise — not runnable yet.** Construct a few synthetic episodes containing observations, actions, rewards and termination flags, with known targets or an analytic low-dimensional transition function. Compose the selected mechanisms in the declared flow, beginning with **Define entropy-regularized value** and ending with **Improve the stochastic actor**. Save each intermediate artifact so a learner can locate a mismatch at its originating stage.

The integration boundary is the selected data, objective and update/evaluation calculations; the tiny fixture is not evidence of successful policy learning on the paper benchmark. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2018-soft-actor-critic). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** For the **Define entropy-regularized value → Improve the stochastic actor** fixture, compare returns, losses, action outputs or update targets with an independently computed episode trace; report termination/truncation and task slices explicitly.

Use one clean baseline and a separately recorded fault case: cross an episode boundary, shift an action relative to its observation, or alter one reward/goal label; attribute the resulting metric change. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **Soft Actor-Critic: Off-Policy Maximum Entropy Deep Reinforcement Learning with a Stochastic Actor** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record episode alignment, discount/termination rules, action units, train/evaluation split, update order and policy version. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
