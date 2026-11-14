---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2022-ik-geo",
  "paper_id": "2022-ik-geo",
  "title": "IK-Geo: Unified Robot Inverse Kinematics Using Subproblem Decomposition",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/2211.05737",
  "source_cards": [
    "research/papers/planning-control-ik/2022-ik-geo.md"
  ],
  "paper_aliases": [],
  "category": "planning-control-ik",
  "topics": [
    "planning-control-ik",
    "ik-geo"
  ],
  "runnable_problem_slugs": [
    "se3-transform-points"
  ],
  "proposed_component_count": 4,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2022-ik-geo",
      "node": "stage-1"
    },
    {
      "card": "2022-ik-geo",
      "node": "stage-2"
    },
    {
      "card": "2022-ik-geo",
      "node": "stage-3"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# IK-Geo: Unified Robot Inverse Kinematics Using Subproblem Decomposition — implementation track

## Orientation and scope

IK-Geo solves inverse kinematics by decomposing robot geometry into canonical circle-intersection subproblems. Kinematic families defined by intersecting or parallel joint axes determine which analytic reductions or low-dimensional searches apply.

The implementation path follows **Express axis geometry → Solve geometric subproblems → Assemble and verify branches**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/2211.05737) · [Paper explanation and graph](/projects/2022-ik-geo) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2022-ik-geo](../../../research/papers/planning-control-ik/2022-ik-geo.md).

**Available now:** 0 paper-associated runnable components; 1 supporting runnable component. **Proposed:** 4 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Express axis geometry** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

- **Supporting prerequisite:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). Its own contract remains authoritative; it does not implement the entire paper.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Express axis geometry

<!-- source-flow: 2022-ik-geo#stage-1 -->

Represent revolute joints through axes and link offsets.

[Study the mechanism and math](/projects/2022-ik-geo#paper-section-express-axis-geometry).

- **Runnable supporting prerequisite:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). Move camera-frame points into the world frame using a rigid transform.
- **Proposed component, not runnable:** Express Revolute Joint-Axis Geometry.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Solve geometric subproblems

<!-- source-flow: 2022-ik-geo#stage-2 -->

Reduce joint angles to circle and plane intersections.

[Study the mechanism and math](/projects/2022-ik-geo#paper-section-solve-geometric-subproblems).

- **Proposed component, not runnable:** Solve a Circle-Plane Rotation Subproblem.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Assemble and verify branches

<!-- source-flow: 2022-ik-geo#stage-3 -->

Combine subproblem roots into full joint solutions.

[Study the mechanism and math](/projects/2022-ik-geo#paper-section-assemble-and-verify-branches).

- **Proposed component, not runnable:** Enumerate Valid Joint-Angle Branches.
- **Proposed component, not runnable:** Verify IK Solutions with Forward Kinematics.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Express axis geometry | axis relationships | Solve geometric subproblems |
| Solve geometric subproblems | candidate angles | Assemble and verify branches |

## Integration exercise

**Proposed exercise — not runnable yet.** Construct a short planar or low-dimensional joint trajectory and explicitly defined obstacles, costs and actuator limits; fix the initial state and reference sequence. Compose the selected mechanisms in the declared flow, beginning with **Express axis geometry** and ending with **Assemble and verify branches**. Save each intermediate artifact so a learner can locate a mismatch at its originating stage.

The integration boundary is a deterministic planning/control calculation on analytic toy dynamics or geometry; neither a full simulator port nor a hardware controller is implied. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2022-ik-geo). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** For the **Express axis geometry → Assemble and verify branches** fixture, compare a tiny search space or analytic solution with the selected cost, constraint and rollout outputs; report feasibility separately from objective improvement.

Use one clean baseline and a separately recorded fault case: introduce an infeasible goal, an obstacle between sampled waypoints, or a saturated actuator; distinguish rejection from a numerically small objective. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **IK-Geo: Unified Robot Inverse Kinematics Using Subproblem Decomposition** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record model equations, time step, joint units, limits, obstacle geometry, solver tolerances and stopping rule. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
