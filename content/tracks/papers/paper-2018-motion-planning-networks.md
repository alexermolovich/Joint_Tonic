---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2018-motion-planning-networks",
  "paper_id": "2018-motion-planning-networks",
  "title": "Motion Planning Networks",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/1806.05767",
  "source_cards": [
    "research/papers/planning-control-ik/2018-motion-planning-networks.md"
  ],
  "paper_aliases": [],
  "category": "planning-control-ik",
  "topics": [
    "planning-control-ik",
    "motion-planning-networks"
  ],
  "runnable_problem_slugs": [],
  "proposed_component_count": 3,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2018-motion-planning-networks",
      "node": "stage-1"
    },
    {
      "card": "2018-motion-planning-networks",
      "node": "stage-2"
    },
    {
      "card": "2018-motion-planning-networks",
      "node": "stage-3"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# Motion Planning Networks — implementation track

## Orientation and scope

MPNet encodes obstacles and predicts successive path waypoints. Its neural planner proposes paths quickly, while explicit collision checking, path contraction, and replanning handle feasibility.

The implementation path follows **Encode the environment → Predict bidirectional waypoints → Validate and repair**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/1806.05767) · [Paper explanation and graph](/projects/2018-motion-planning-networks) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2018-motion-planning-networks](../../../research/papers/planning-control-ik/2018-motion-planning-networks.md).

**Available now:** 0 paper-associated runnable components; 0 supporting runnable components. **Proposed:** 3 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Encode the environment** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

There is no independently runnable prerequisite mapped for this source yet. Use the source-card notation and stage contracts as the diagnostic; prerequisite exercises must be authored and reviewed before being presented as runnable.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Encode the environment

<!-- source-flow: 2018-motion-planning-networks#stage-1 -->

Compress an obstacle point cloud into a planning representation.

[Study the mechanism and math](/projects/2018-motion-planning-networks#paper-section-encode-the-environment).

- **Proposed component, not runnable:** Encode Obstacles into a Fixed Feature.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Predict bidirectional waypoints

<!-- source-flow: 2018-motion-planning-networks#stage-2 -->

Grow paths from start and goal toward one another.

[Study the mechanism and math](/projects/2018-motion-planning-networks#paper-section-predict-bidirectional-waypoints).

- **Proposed component, not runnable:** Predict and Validate an Intermediate Waypoint.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Validate and repair

<!-- source-flow: 2018-motion-planning-networks#stage-3 -->

Check every edge and replan infeasible segments.

[Study the mechanism and math](/projects/2018-motion-planning-networks#paper-section-validate-and-repair).

- **Proposed component, not runnable:** Repair an Infeasible Planned Segment.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Encode the environment | environment code | Predict bidirectional waypoints |
| Predict bidirectional waypoints | candidate path | Validate and repair |

## Integration exercise

**Proposed exercise — not runnable yet.** Construct a short planar or low-dimensional joint trajectory and explicitly defined obstacles, costs and actuator limits; fix the initial state and reference sequence. Compose the selected mechanisms in the declared flow, beginning with **Encode the environment** and ending with **Validate and repair**. Save each intermediate artifact so a learner can locate a mismatch at its originating stage.

The integration boundary is a deterministic planning/control calculation on analytic toy dynamics or geometry; neither a full simulator port nor a hardware controller is implied. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2018-motion-planning-networks). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** For the **Encode the environment → Validate and repair** fixture, compare a tiny search space or analytic solution with the selected cost, constraint and rollout outputs; report feasibility separately from objective improvement.

Use one clean baseline and a separately recorded fault case: introduce an infeasible goal, an obstacle between sampled waypoints, or a saturated actuator; distinguish rejection from a numerically small objective. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **Motion Planning Networks** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record model equations, time step, joint units, limits, obstacle geometry, solver tolerances and stopping rule. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
