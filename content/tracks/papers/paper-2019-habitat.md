---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2019-habitat",
  "paper_id": "2019-habitat",
  "title": "Habitat: A Platform for Embodied AI Research",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/1904.01201",
  "source_cards": [
    "research/papers/simulation-sim2real/2019-habitat.md"
  ],
  "paper_aliases": [],
  "category": "simulation-sim2real",
  "topics": [
    "simulation-sim2real",
    "habitat"
  ],
  "runnable_problem_slugs": [
    "se3-transform-points"
  ],
  "proposed_component_count": 3,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2019-habitat",
      "node": "stage-1"
    },
    {
      "card": "2019-habitat",
      "node": "stage-2"
    },
    {
      "card": "2019-habitat",
      "node": "stage-3"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# Habitat: A Platform for Embodied AI Research — implementation track

## Orientation and scope

Habitat separates fast configurable 3D simulation from task definitions and embodied-agent evaluation. The original paper emphasizes scalable visual navigation and cross-dataset generalization.

The implementation path follows **Configure agent sensors → Run a navigation episode → Measure success and efficiency**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/1904.01201) · [Paper explanation and graph](/projects/2019-habitat) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2019-habitat](../../../research/papers/simulation-sim2real/2019-habitat.md).

**Available now:** 0 paper-associated runnable components; 1 supporting runnable component. **Proposed:** 3 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Configure agent sensors** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

- **Supporting prerequisite:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). Its own contract remains authoritative; it does not implement the entire paper.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Configure agent sensors

<!-- source-flow: 2019-habitat#stage-1 -->

Render observations from a calibrated agent pose.

[Study the mechanism and math](/projects/2019-habitat#paper-section-configure-agent-sensors).

- **Runnable supporting prerequisite:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). Move camera-frame points into the world frame using a rigid transform.
- **Proposed component, not runnable:** Validate a Navigation Episode.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Run a navigation episode

<!-- source-flow: 2019-habitat#stage-2 -->

Follow a task goal using only permitted observations.

[Study the mechanism and math](/projects/2019-habitat#paper-section-run-a-navigation-episode).

- **Proposed component, not runnable:** Replay a Seeded Navigation Trajectory.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Measure success and efficiency

<!-- source-flow: 2019-habitat#stage-3 -->

Use path-length-aware evaluation and held-out scenes.

[Study the mechanism and math](/projects/2019-habitat#paper-section-measure-success-and-efficiency).

- **Proposed component, not runnable:** Compute Success and SPL.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Configure agent sensors | sensor observations | Run a navigation episode |
| Run a navigation episode | episode paths | Measure success and efficiency |

## Integration exercise

**Proposed exercise — not runnable yet.** Construct a few original scenario/rollout records with bounded physical parameters, seeds and explicit success labels; use analytic dynamics for any required state transition. Compose the selected mechanisms in the declared flow, beginning with **Configure agent sensors** and ending with **Measure success and efficiency**. Save each intermediate artifact so a learner can locate a mismatch at its originating stage.

The integration boundary is the selected simulation data, metric or transfer mechanism; running the original simulator assets or reproducing reported real-world transfer requires separate reviewed work. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2019-habitat). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** For the **Configure agent sensors → Measure success and efficiency** fixture, compare scenario coverage, rollout statistics or sampled parameter constraints with a deterministic expected report; keep success, failure and censoring distinct.

Use one clean baseline and a separately recorded fault case: remove a scenario family, violate a parameter bound, or change a reset/termination condition; measure the resulting coverage or metric discrepancy. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **Habitat: A Platform for Embodied AI Research** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record scenario IDs, reset and termination rules, physical units, parameter distributions, seeds and simulator/backend version if one is later introduced. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
