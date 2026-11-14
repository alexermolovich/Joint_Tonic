---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2017-proximal-policy-optimization",
  "paper_id": "2017-proximal-policy-optimization",
  "title": "Proximal Policy Optimization Algorithms",
  "status": "bounded-integration-available",
  "primary_url": "https://arxiv.org/abs/1707.06347",
  "source_cards": [
    "research/papers/robot-learning-rl/2017-proximal-policy-optimization.md"
  ],
  "paper_aliases": [],
  "category": "robot-learning-rl",
  "topics": [
    "robot-learning-rl",
    "proximal-policy-optimization"
  ],
  "runnable_problem_slugs": [
    "ppo-normalize-batched-advantages",
    "ppo-clipped-policy-surrogate",
    "ppo-policy-update-clip-fractions",
    "ppo-boundary-value-targets",
    "ppo-joint-controller-integration"
  ],
  "proposed_component_count": 0,
  "source_flow_node_count": 4,
  "source_flow_nodes": [
    {
      "card": "2017-proximal-policy-optimization",
      "node": "stage-1"
    },
    {
      "card": "2017-proximal-policy-optimization",
      "node": "stage-2"
    },
    {
      "card": "2017-proximal-policy-optimization",
      "node": "stage-3"
    },
    {
      "card": "2017-proximal-policy-optimization",
      "node": "bounded-controller-integration"
    }
  ],
  "integration_status": "runnable",
  "assessment_status": "runnable",
  "integration_problem_slug": "ppo-joint-controller-integration"
}
---

# Proximal Policy Optimization Algorithms — implementation track

## Orientation and scope

PPO reuses a batch of on-policy experience for several optimization epochs while clipping the policy-ratio surrogate. The clipping discourages excessive improvement claims from large probability changes without imposing an exact trust-region constraint.

The implementation path follows **Collect advantages and old probabilities → Optimize the clipped surrogate → Update value and collect again → Train and evaluate a bounded controller**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/1707.06347) · [Paper explanation and graph](/projects/2017-proximal-policy-optimization) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2017-proximal-policy-optimization](../../../research/papers/robot-learning-rl/2017-proximal-policy-optimization.md).

**Available now:** 5 paper-associated runnable components; 0 supporting runnable components. **Proposed:** 0 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Collect advantages and old probabilities** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

- **Supporting prerequisite:** [Compute Value Targets Across Episode Boundaries](/problems/ppo-boundary-value-targets). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Normalize Batched Advantages](/problems/ppo-normalize-batched-advantages). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Compute the Clipped Policy Surrogate](/problems/ppo-clipped-policy-surrogate). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Report Policy Update Clip Fractions](/problems/ppo-policy-update-clip-fractions). Its own contract remains authoritative; it does not implement the entire paper.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Collect advantages and old probabilities

<!-- source-flow: 2017-proximal-policy-optimization#stage-1 -->

Freeze the behavior policy for a rollout batch.

[Study the mechanism and math](/projects/2017-proximal-policy-optimization#paper-section-collect-advantages-and-old-probabilities).

- **Runnable paper-associated component:** [Normalize Batched Advantages](/problems/ppo-normalize-batched-advantages). Different rollout batches can have very different advantage scales.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Optimize the clipped surrogate

<!-- source-flow: 2017-proximal-policy-optimization#stage-2 -->

Limit the benefit of large policy-ratio changes.

[Study the mechanism and math](/projects/2017-proximal-policy-optimization#paper-section-optimize-the-clipped-surrogate).

- **Runnable paper-associated component:** [Compute the Clipped Policy Surrogate](/problems/ppo-clipped-policy-surrogate). PPO compares the new policy with the policy that collected each action.
- **Runnable paper-associated component:** [Report Policy Update Clip Fractions](/problems/ppo-policy-update-clip-fractions). A probability ratio outside the clipping interval does not always change PPO’s objective.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Update value and collect again

<!-- source-flow: 2017-proximal-policy-optimization#stage-3 -->

Fit value targets, monitor policy change, and refresh experience.

[Study the mechanism and math](/projects/2017-proximal-policy-optimization#paper-section-update-value-and-collect-again).

- **Runnable paper-associated component:** [Compute Value Targets Across Episode Boundaries](/problems/ppo-boundary-value-targets). A robot rollout can end because the task terminates or because collection hits a time limit.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 4. Train and evaluate a bounded controller

<!-- source-flow: 2017-proximal-policy-optimization#bounded-controller-integration -->

Compose fixed-policy rollouts, terminal returns, clipped updates and held-out evaluation in a scalar synthetic joint environment.

[Study the mechanism and math](/projects/2017-proximal-policy-optimization#paper-section-bounded-executable-controller-integration).

- **Runnable paper-associated component:** [Train and Evaluate a Tiny PPO Joint Controller](/problems/ppo-joint-controller-integration). A policy loss is only one part of reinforcement learning.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Collect advantages and old probabilities | rollout batch | Optimize the clipped surrogate |
| Optimize the clipped surrogate | updated policy | Update value and collect again |
| Update value and collect again | reviewed update components | Train and evaluate a bounded controller |

## Integration exercise

**Runnable bounded integration:** [Train and Evaluate a Tiny PPO Joint Controller](/problems/ppo-joint-controller-integration). This exercises its declared synthetic contract, not the full paper benchmark.

A scalar joint starts at zero and must approach a supplied target. A linear Gaussian policy chooses velocity commands; an explicit integrator advances the synthetic state. You will collect trajectories, compute terminal discounted returns, normalize advantages, take repeated clipped-surrogate updates and evaluate held-out goals.

```text
training goals + supplied noise -> fixed-policy rollouts
  -> terminal returns -> normalized advantages
  -> frozen behavior likelihoods + PPO epochs
  -> updated controller -> separate held-out goal evaluation
```

Each arrow is a data dependency, and the written sequence is also the text alternative to the pipeline. No animation is required.

This is a real bounded parameter-update loop on a deliberately small environment. It does not include neural perception, a learned critic, MuJoCo, contact dynamics, real-hardware execution or PPO's published locomotion experiments. The reward, dynamics, Gaussian scale, norm clipping and parameter projection are fully specified teaching choices. Read the integration contract before composing the atomic components.

## Evaluation and failure analysis

**Runnable assessment:** public/hidden cases for the linked integration.

The isolated worker checks collected return traces, parameter updates, clip diagnostics and held-out deterministic outcomes using fixed supplied noise. It also checks no-update and empty-learning-signal cases. Passing means the declared pipeline is implemented correctly; it does not require claiming the policy always improves.

Report training return and held-out final position error separately. Training return includes the exploration noise and action penalty; evaluation uses mean actions and independent target positions. A rising training return can coexist with asymmetric held-out error because the linear policy shares one bias across goals.

Compare at least one positive-only training-goal set with symmetric held-out targets. Inspect whether the learned bias helps one direction while hurting the other. Keep the iteration budget, supplied noise, reward scale and target sets fixed when comparing runs.

## Reproducibility deliverable

**Runnable project deliverable:** save the following report in the integration exercise’s Notes. The report is learner-authored, not automatically certified.

Copy this template into the integration workspace Notes after running the project:

- Content version and worker runtime:
- Initial gain and bias:
- Training/evaluation goal arrays:
- Supplied noise seed or exact fixture identity:
- Iterations, horizon, PPO epochs, step size and clip width:
- Final parameter vector:
- Training return trace:
- Held-out final error per target:
- Clip-fraction trace:
- Failure case observed:
- Deliberate simplifications relative to the primary PPO paper:

Synthetic coordinates are normalized joint positions and normalized velocity commands at a fixed0.1-second interval. There are no external datasets, pretrained weights or robot safety claims. The exact fixture and content version are necessary to reproduce an update trace.
