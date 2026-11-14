---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2023-maniskill-2",
  "paper_id": "2023-maniskill-2",
  "title": "ManiSkill2: A Unified Benchmark for Generalizable Manipulation Skills",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/2302.04659",
  "source_cards": [
    "research/papers/simulation-sim2real/2023-maniskill-2.md"
  ],
  "paper_aliases": [],
  "category": "simulation-sim2real",
  "topics": [
    "simulation-sim2real",
    "maniskill-2"
  ],
  "runnable_problem_slugs": [
    "validate-robot-episodes",
    "se3-transform-points"
  ],
  "proposed_component_count": 4,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2023-maniskill-2",
      "node": "stage-1"
    },
    {
      "card": "2023-maniskill-2",
      "node": "stage-2"
    },
    {
      "card": "2023-maniskill-2",
      "node": "stage-3"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# ManiSkill2: A Unified Benchmark for Generalizable Manipulation Skills — implementation track

## Orientation and scope

ManiSkill2 expands manipulation benchmarks across rigid and soft objects, mobile and stationary robots, and multiple observation/controller interfaces. A unified interface supports learning and classical planning while retaining task-specific physical contracts.

The implementation path follows **Choose task and controller → Collect visual experience → Evaluate object and task generalization**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/2302.04659) · [Paper explanation and graph](/projects/2023-maniskill-2) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2023-maniskill-2](../../../research/papers/simulation-sim2real/2023-maniskill-2.md).

**Available now:** 0 paper-associated runnable components; 2 supporting runnable components. **Proposed:** 4 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Choose task and controller** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

- **Supporting prerequisite:** [Validate a Multimodal Robot Episode Schema](/problems/validate-robot-episodes). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). Its own contract remains authoritative; it does not implement the entire paper.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Choose task and controller

<!-- source-flow: 2023-maniskill-2#stage-1 -->

Specify embodiment, object dynamics, and action semantics.

[Study the mechanism and math](/projects/2023-maniskill-2#paper-section-choose-task-and-controller).

- **Proposed component, not runnable:** Validate a Robot-Controller-Task Configuration.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Collect visual experience

<!-- source-flow: 2023-maniskill-2#stage-2 -->

Use RGB-D or point clouds and versioned demonstrations.

[Study the mechanism and math](/projects/2023-maniskill-2#paper-section-collect-visual-experience).

- **Runnable supporting prerequisite:** [Validate a Multimodal Robot Episode Schema](/problems/validate-robot-episodes). A signal's missing fraction is missing_rows / T. A timestamp must be finite numeric, and each valid adjacent pair must strictly increase.
- **Runnable supporting prerequisite:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). Move camera-frame points into the world frame using a rigid transform.
- **Proposed component, not runnable:** Build a Vectorized Manipulation Batch.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Evaluate object and task generalization

<!-- source-flow: 2023-maniskill-2#stage-3 -->

Keep geometry splits and physical success checks explicit.

[Study the mechanism and math](/projects/2023-maniskill-2#paper-section-evaluate-object-and-task-generalization).

- **Proposed component, not runnable:** Validate Task-Specific Success Predicates.
- **Proposed component, not runnable:** Report Generalization by Object Split.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Choose task and controller | environment transitions | Collect visual experience |
| Collect visual experience | policy rollouts | Evaluate object and task generalization |

## Integration exercise

**Proposed exercise — not runnable yet.** Construct a few original scenario/rollout records with bounded physical parameters, seeds and explicit success labels; use analytic dynamics for any required state transition. Compose the selected mechanisms in the declared flow, beginning with **Choose task and controller** and ending with **Evaluate object and task generalization**. Save each intermediate artifact so a learner can locate a mismatch at its originating stage.

The integration boundary is the selected simulation data, metric or transfer mechanism; running the original simulator assets or reproducing reported real-world transfer requires separate reviewed work. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2023-maniskill-2). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** For the **Choose task and controller → Evaluate object and task generalization** fixture, compare scenario coverage, rollout statistics or sampled parameter constraints with a deterministic expected report; keep success, failure and censoring distinct.

Use one clean baseline and a separately recorded fault case: remove a scenario family, violate a parameter bound, or change a reset/termination condition; measure the resulting coverage or metric discrepancy. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **ManiSkill2: A Unified Benchmark for Generalizable Manipulation Skills** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record scenario IDs, reset and termination rules, physical units, parameter distributions, seeds and simulator/backend version if one is later introduced. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
