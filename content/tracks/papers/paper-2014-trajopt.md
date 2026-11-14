---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2014-trajopt",
  "paper_id": "2014-trajopt",
  "title": "Motion Planning with Sequential Convex Optimization and Convex Collision Checking",
  "status": "planned",
  "primary_url": "https://rll.berkeley.edu/trajopt/ijrr",
  "source_cards": [
    "research/papers/planning-control-ik/2014-trajopt.md"
  ],
  "paper_aliases": [],
  "category": "planning-control-ik",
  "topics": [
    "trajectory optimization",
    "collision avoidance",
    "sequential convex optimization"
  ],
  "runnable_problem_slugs": [
    "planar-two-link-ik"
  ],
  "proposed_component_count": 4,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2014-trajopt",
      "node": "score"
    },
    {
      "card": "2014-trajopt",
      "node": "convexify"
    },
    {
      "card": "2014-trajopt",
      "node": "swept"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# Motion Planning with Sequential Convex Optimization and Convex Collision Checking — implementation track

## Orientation and scope

TrajOpt improves an initial motion by solving a sequence of simpler optimization problems. Each local problem approximates nonlinear costs and constraints near the current trajectory. Collision penalties and trust-region decisions help decide which candidate updates to accept. A waypoint-only check is insufficient when the robot can cross an obstacle between two safe samples.

The implementation path follows **Score a trajectory → Linearize signed-distance penalties → Check swept motion**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://rll.berkeley.edu/trajopt/ijrr) · [Paper explanation and graph](/projects/2014-trajopt) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2014-trajopt](../../../research/papers/planning-control-ik/2014-trajopt.md).

**Available now:** 0 paper-associated runnable components; 1 supporting runnable component. **Proposed:** 4 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Score a trajectory** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

- **Supporting prerequisite:** [Solve Closed-Form IK for a Planar Two-Link Arm](/problems/planar-two-link-ik). Its own contract remains authoritative; it does not implement the entire paper.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Score a trajectory

<!-- source-flow: 2014-trajopt#score -->

Score a trajectory. See the original explanation and component status below.

[Study the mechanism and math](/projects/2014-trajopt#paper-section-score-a-trajectory).

- **Runnable supporting prerequisite:** [Solve Closed-Form IK for a Planar Two-Link Arm](/problems/planar-two-link-ik). Solve one declared elbow branch, report unreachable targets, and identify singular two-link configurations.
- **Proposed component, not runnable:** Build a Joint-Space Smoothness Cost.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Linearize signed-distance penalties

<!-- source-flow: 2014-trajopt#convexify -->

Linearize signed-distance penalties. See the original explanation and component status below.

[Study the mechanism and math](/projects/2014-trajopt#paper-section-linearize-signed-distance-penalties).

- **Proposed component, not runnable:** Linearize a Signed-Distance Collision Penalty.
- **Proposed component, not runnable:** Bound a Sequential Convex Trust-Region Step.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Check swept motion

<!-- source-flow: 2014-trajopt#swept -->

Check swept motion. See the original explanation and component status below.

[Study the mechanism and math](/projects/2014-trajopt#paper-section-check-swept-motion).

- **Proposed component, not runnable:** Check a Segment Against Occupancy Cells.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Score a trajectory | validated component output | Linearize signed-distance penalties |
| Linearize signed-distance penalties | validated component output | Check swept motion |

## Integration exercise

**Proposed exercise — not runnable yet.** Use a planar point trajectory with fixed endpoints and one analytic circular obstacle. Compose a proposed smoothness cost, signed-distance linearization and trust-region acceptance rule; inspect each accepted trajectory and explicitly check swept segments between waypoints. This is a new teaching formulation, not the original robot collision implementation.

The integration boundary is a deterministic planning/control calculation on analytic toy dynamics or geometry; neither a full simulator port nor a hardware controller is implied. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2014-trajopt). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** Compare the local model with finite differences, reject a step outside the trust region, and include a segment whose endpoints are clear but whose interior intersects the obstacle. Report constraint violation alongside cost decrease.

Use one clean baseline and a separately recorded fault case: introduce an infeasible goal, an obstacle between sampled waypoints, or a saturated actuator; distinguish rejection from a numerically small objective. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **Motion Planning with Sequential Convex Optimization and Convex Collision Checking** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record model equations, time step, joint units, limits, obstacle geometry, solver tolerances and stopping rule. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
