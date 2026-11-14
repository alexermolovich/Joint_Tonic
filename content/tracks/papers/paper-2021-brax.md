---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2021-brax",
  "paper_id": "2021-brax",
  "title": "Brax -- A Differentiable Physics Engine for Large Scale Rigid Body Simulation",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/2106.13281",
  "source_cards": [
    "research/papers/simulation-sim2real/2021-brax.md"
  ],
  "paper_aliases": [],
  "category": "simulation-sim2real",
  "topics": [
    "simulation-sim2real",
    "brax"
  ],
  "runnable_problem_slugs": [
    "brax-functional-damped-step",
    "simulator-selective-environment-reset"
  ],
  "proposed_component_count": 1,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2021-brax",
      "node": "stage-1"
    },
    {
      "card": "2021-brax",
      "node": "stage-2"
    },
    {
      "card": "2021-brax",
      "node": "stage-3"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# Brax -- A Differentiable Physics Engine for Large Scale Rigid Body Simulation — implementation track

## Orientation and scope

Brax expresses rigid-body simulation and learning in an accelerator-friendly JAX workflow. Vectorization, compilation, and automatic differentiation allow many environments and policy updates to remain on the same device.

The implementation path follows **Express a functional simulation step → Batch and compile rollouts → Optimize policies**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/2106.13281) · [Paper explanation and graph](/projects/2021-brax) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2021-brax](../../../research/papers/simulation-sim2real/2021-brax.md).

**Available now:** 2 paper-associated runnable components; 0 supporting runnable components. **Proposed:** 1 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Express a functional simulation step** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

There is no independently runnable prerequisite mapped for this source yet. Use the source-card notation and stage contracts as the diagnostic; prerequisite exercises must be authored and reviewed before being presented as runnable.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Express a functional simulation step

<!-- source-flow: 2021-brax#stage-1 -->

Map explicit state and action to the next state.

[Study the mechanism and math](/projects/2021-brax#paper-section-express-a-functional-simulation-step).

- **Runnable paper-associated component:** [Implement a Functional Physics Step Contract](/problems/brax-functional-damped-step). A functional step receives every state variable explicitly and returns a new state.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Batch and compile rollouts

<!-- source-flow: 2021-brax#stage-2 -->

Vectorize independent environments on accelerators.

[Study the mechanism and math](/projects/2021-brax#paper-section-batch-and-compile-rollouts).

- **Runnable paper-associated component:** [Reset Completed Environments Selectively](/problems/simulator-selective-environment-reset). Only completed environments should restart.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Optimize policies

<!-- source-flow: 2021-brax#stage-3 -->

Use RL or differentiate through the rollout when appropriate.

[Study the mechanism and math](/projects/2021-brax#paper-section-optimize-policies).

- **Proposed component, not runnable:** Check Gradient Consistency for a Small Dynamics Model.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Express a functional simulation step | state batches | Batch and compile rollouts |
| Batch and compile rollouts | device-resident trajectories | Optimize policies |

## Integration exercise

**Proposed exercise — not runnable yet.** Construct a few original scenario/rollout records with bounded physical parameters, seeds and explicit success labels; use analytic dynamics for any required state transition. Compose the selected mechanisms in the declared flow, beginning with **Express a functional simulation step** and ending with **Optimize policies**. Save each intermediate artifact so a learner can locate a mismatch at its originating stage.

The integration boundary is the selected simulation data, metric or transfer mechanism; running the original simulator assets or reproducing reported real-world transfer requires separate reviewed work. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2021-brax). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** For the **Express a functional simulation step → Optimize policies** fixture, compare scenario coverage, rollout statistics or sampled parameter constraints with a deterministic expected report; keep success, failure and censoring distinct.

Use one clean baseline and a separately recorded fault case: remove a scenario family, violate a parameter bound, or change a reset/termination condition; measure the resulting coverage or metric discrepancy. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **Brax -- A Differentiable Physics Engine for Large Scale Rigid Body Simulation** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record scenario IDs, reset and termination rules, physical units, parameter distributions, seeds and simulator/backend version if one is later introduced. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
