---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2021-maniskill",
  "paper_id": "2021-maniskill",
  "title": "ManiSkill: Generalizable Manipulation Skill Benchmark with Large-Scale Demonstrations",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/2107.14483",
  "source_cards": [
    "research/papers/simulation-sim2real/2021-maniskill.md"
  ],
  "paper_aliases": [],
  "category": "simulation-sim2real",
  "topics": [
    "simulation-sim2real",
    "maniskill"
  ],
  "runnable_problem_slugs": [
    "se3-transform-points",
    "unproject-depth-map"
  ],
  "proposed_component_count": 4,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2021-maniskill",
      "node": "stage-1"
    },
    {
      "card": "2021-maniskill",
      "node": "stage-2"
    },
    {
      "card": "2021-maniskill",
      "node": "stage-3"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# ManiSkill: Generalizable Manipulation Skill Benchmark with Large-Scale Demonstrations — implementation track

## Orientation and scope

ManiSkill benchmarks manipulation across articulated objects with substantial geometric and topological variation. Point-cloud/RGB-D observations and demonstrations support studying generalizable perception and policy learning.

The implementation path follows **Sample an object instance → Construct 3D observations → Learn and test manipulation**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/2107.14483) · [Paper explanation and graph](/projects/2021-maniskill) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2021-maniskill](../../../research/papers/simulation-sim2real/2021-maniskill.md).

**Available now:** 0 paper-associated runnable components; 2 supporting runnable components. **Proposed:** 4 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Sample an object instance** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

- **Supporting prerequisite:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Unproject a Depth Map into a Point Cloud](/problems/unproject-depth-map). Its own contract remains authoritative; it does not implement the entire paper.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Sample an object instance

<!-- source-flow: 2021-maniskill#stage-1 -->

Choose a task and articulated asset with declared geometry.

[Study the mechanism and math](/projects/2021-maniskill#paper-section-sample-an-object-instance).

- **Proposed component, not runnable:** Stratify Manipulation Object Instances.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Construct 3D observations

<!-- source-flow: 2021-maniskill#stage-2 -->

Transform visible depth into the policy point-cloud frame.

[Study the mechanism and math](/projects/2021-maniskill#paper-section-construct-3d-observations).

- **Runnable supporting prerequisite:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). Move camera-frame points into the world frame using a rigid transform.
- **Runnable supporting prerequisite:** [Unproject a Depth Map into a Point Cloud](/problems/unproject-depth-map). Turn optical-axis depth into an organized camera-frame point cloud while preserving missing-pixel masks.
- **Proposed component, not runnable:** Validate Manipulation Task Observations.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Learn and test manipulation

<!-- source-flow: 2021-maniskill#stage-3 -->

Evaluate policies on held-out object geometries.

[Study the mechanism and math](/projects/2021-maniskill#paper-section-learn-and-test-manipulation).

- **Proposed component, not runnable:** Normalize Action Bounds Across Tasks.
- **Proposed component, not runnable:** Evaluate Skill Success Across Object Instances.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Sample an object instance | camera observations | Construct 3D observations |
| Construct 3D observations | point clouds and demonstrations | Learn and test manipulation |

## Integration exercise

**Proposed exercise — not runnable yet.** Construct a few original scenario/rollout records with bounded physical parameters, seeds and explicit success labels; use analytic dynamics for any required state transition. Compose the selected mechanisms in the declared flow, beginning with **Sample an object instance** and ending with **Learn and test manipulation**. Save each intermediate artifact so a learner can locate a mismatch at its originating stage.

The integration boundary is the selected simulation data, metric or transfer mechanism; running the original simulator assets or reproducing reported real-world transfer requires separate reviewed work. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2021-maniskill). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** For the **Sample an object instance → Learn and test manipulation** fixture, compare scenario coverage, rollout statistics or sampled parameter constraints with a deterministic expected report; keep success, failure and censoring distinct.

Use one clean baseline and a separately recorded fault case: remove a scenario family, violate a parameter bound, or change a reset/termination condition; measure the resulting coverage or metric discrepancy. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **ManiSkill: Generalizable Manipulation Skill Benchmark with Large-Scale Demonstrations** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record scenario IDs, reset and termination rules, physical units, parameter distributions, seeds and simulator/backend version if one is later introduced. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
