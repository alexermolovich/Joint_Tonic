---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2018-micro-lie-theory",
  "paper_id": "2018-micro-lie-theory",
  "title": "A micro Lie theory for state estimation in robotics",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/1812.01537",
  "source_cards": [
    "research/papers/geometry-calibration-slam/2018-micro-lie-theory.md"
  ],
  "paper_aliases": [],
  "category": "geometry-calibration-slam",
  "topics": [
    "Lie groups",
    "state estimation",
    "SE(3)",
    "geometry"
  ],
  "runnable_problem_slugs": [
    "compose-frame-transforms",
    "normalize-multiply-quaternions",
    "interpolate-pose-slerp",
    "kalman-filter-measurement-update",
    "finite-difference-gradient-check"
  ],
  "proposed_component_count": 1,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2018-micro-lie-theory",
      "node": "pose"
    },
    {
      "card": "2018-micro-lie-theory",
      "node": "update"
    },
    {
      "card": "2018-micro-lie-theory",
      "node": "linearize"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# A micro Lie theory for state estimation in robotics — implementation track

## Orientation and scope

Rigid poses live on a constrained space: adding arbitrary entries to a rotation matrix generally stops it being a rotation. The paper organizes local perturbations, Jacobians and covariance propagation around small tangent vectors. A practical implementation must choose which side receives an update and which frame expresses its coordinates.

The implementation path follows **Represent a pose → Apply a tangent update → Linearize an estimation residual**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/1812.01537) · [Paper explanation and graph](/projects/2018-micro-lie-theory) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2018-micro-lie-theory](../../../research/papers/geometry-calibration-slam/2018-micro-lie-theory.md).

**Available now:** 0 paper-associated runnable components; 5 supporting runnable components. **Proposed:** 1 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Represent a pose** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

- **Supporting prerequisite:** [Compose and Invert Coordinate Transforms](/problems/compose-frame-transforms). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Normalize and Multiply Quaternions](/problems/normalize-multiply-quaternions). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Interpolate a Pose with SLERP](/problems/interpolate-pose-slerp). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [One Kalman Filter Measurement Update](/problems/kalman-filter-measurement-update). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Finite-Difference Gradient Check](/problems/finite-difference-gradient-check). Its own contract remains authoritative; it does not implement the entire paper.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Represent a pose

<!-- source-flow: 2018-micro-lie-theory#pose -->

Represent a pose. See the original explanation and component status below.

[Study the mechanism and math](/projects/2018-micro-lie-theory#paper-section-represent-a-pose).

- **Runnable supporting prerequisite:** [Compose and Invert Coordinate Transforms](/problems/compose-frame-transforms). Compose timestamped, frame-labeled rigid transforms and construct the inverse in the correct frame.
- **Runnable supporting prerequisite:** [Normalize and Multiply Quaternions](/problems/normalize-multiply-quaternions). Normalize scalar-first quaternions safely and compose active rotations in the declared order.
- **Runnable supporting prerequisite:** [Interpolate a Pose with SLERP](/problems/interpolate-pose-slerp). Interpolate translation linearly and orientation along the shortest quaternion arc.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Apply a tangent update

<!-- source-flow: 2018-micro-lie-theory#update -->

Apply a tangent update. See the original explanation and component status below.

[Study the mechanism and math](/projects/2018-micro-lie-theory#paper-section-apply-a-tangent-update).

- **Proposed component, not runnable:** Apply SE(3) Exponential and Logarithm Maps.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Linearize an estimation residual

<!-- source-flow: 2018-micro-lie-theory#linearize -->

Linearize an estimation residual. See the original explanation and component status below.

[Study the mechanism and math](/projects/2018-micro-lie-theory#paper-section-linearize-an-estimation-residual).

- **Runnable supporting prerequisite:** [One Kalman Filter Measurement Update](/problems/kalman-filter-measurement-update). Fuse a linear sensor measurement using a stable Kalman gain and Joseph covariance update.
- **Runnable supporting prerequisite:** [Finite-Difference Gradient Check](/problems/finite-difference-gradient-check). Finite-Difference Gradient Check

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Represent a pose | validated component output | Apply a tangent update |
| Apply a tangent update | validated component output | Linearize an estimation residual |

## Integration exercise

**Proposed exercise — not runnable yet.** Use a single synthetic pose and small tangent perturbations under one explicitly declared left- or right-update convention. Compose pose operations with proposed exponential/logarithm maps and a finite-difference residual check. The exercise must state the twist coordinate order and frame before defining a Jacobian.

The integration boundary is a bounded estimation or reconstruction component with analytic geometry; learned correspondence outputs may be supplied as fixed synthetic arrays. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2018-micro-lie-theory). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** Test identity and small-angle cases, round-trip within a declared logarithm branch, and compare analytic and numerical Jacobians. Deliberately exchange left/right updates to demonstrate a frame-dependent residual error.

Use one clean baseline and a separately recorded fault case: reverse one transform, perturb one calibration value, or shift one sensor timestamp; report which residual and validity check changes. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **A micro Lie theory for state estimation in robotics** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record calibration hash, coordinate-frame convention, sensor clock convention, gauge/alignment choice and residual weights. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
