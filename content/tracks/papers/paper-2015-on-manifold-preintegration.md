---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2015-on-manifold-preintegration",
  "paper_id": "2015-on-manifold-preintegration",
  "title": "On-Manifold Preintegration for Real-Time Visual-Inertial Odometry",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/1512.02363",
  "source_cards": [
    "research/papers/geometry-calibration-slam/2015-on-manifold-preintegration.md"
  ],
  "paper_aliases": [],
  "category": "geometry-calibration-slam",
  "topics": [
    "geometry-calibration-slam",
    "on-manifold-preintegration"
  ],
  "runnable_problem_slugs": [
    "integrate-imu-rotation",
    "match-approximate-sensor-timestamps",
    "estimate-clock-offset-paired-events",
    "preintegrate-imu-translation",
    "first-order-imu-bias-correction"
  ],
  "proposed_component_count": 1,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2015-on-manifold-preintegration",
      "node": "stage-1"
    },
    {
      "card": "2015-on-manifold-preintegration",
      "node": "stage-2"
    },
    {
      "card": "2015-on-manifold-preintegration",
      "node": "stage-3"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# On-Manifold Preintegration for Real-Time Visual-Inertial Odometry — implementation track

## Orientation and scope

On-manifold IMU preintegration summarizes many high-rate inertial samples into a constraint between keyframes. Rotation is integrated on SO(3), and bias Jacobians allow small bias corrections without replaying every sample.

The implementation path follows **Integrate relative rotation → Integrate velocity and position → Form a keyframe factor**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/1512.02363) · [Paper explanation and graph](/projects/2015-on-manifold-preintegration) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2015-on-manifold-preintegration](../../../research/papers/geometry-calibration-slam/2015-on-manifold-preintegration.md).

**Available now:** 3 paper-associated runnable components; 2 supporting runnable components. **Proposed:** 1 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Integrate relative rotation** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

- **Supporting prerequisite:** [Match Approximate Sensor Timestamps](/problems/match-approximate-sensor-timestamps). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Estimate Clock Offset from Paired Events](/problems/estimate-clock-offset-paired-events). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Apply SE(3) Exponential and Logarithm Maps](/problems/se3-exponential-logarithm). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Integrate IMU Rotation Increments on SO3](/problems/integrate-imu-rotation). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Preintegrate Bias-Corrected IMU Velocity and Position](/problems/preintegrate-imu-translation). Its own contract remains authoritative; it does not implement the entire paper.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Integrate relative rotation

<!-- source-flow: 2015-on-manifold-preintegration#stage-1 -->

Accumulate bias-corrected angular increments.

[Study the mechanism and math](/projects/2015-on-manifold-preintegration#paper-section-integrate-relative-rotation).

- **Runnable paper-associated component:** [Integrate IMU Rotation Increments on SO3](/problems/integrate-imu-rotation). Integrate bias-corrected body angular velocities with right-multiplied SO(3) increments.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Integrate velocity and position

<!-- source-flow: 2015-on-manifold-preintegration#stage-2 -->

Accumulate specific force in the starting body frame.

[Study the mechanism and math](/projects/2015-on-manifold-preintegration#paper-section-integrate-velocity-and-position).

- **Runnable supporting prerequisite:** [Match Approximate Sensor Timestamps](/problems/match-approximate-sensor-timestamps). Associate each query with its nearest reference timestamp within a fixed tolerance.
- **Runnable supporting prerequisite:** [Estimate Clock Offset from Paired Events](/problems/estimate-clock-offset-paired-events). Estimate a constant clock offset from corresponding event timestamps using a robust median.
- **Runnable paper-associated component:** [Preintegrate Bias-Corrected IMU Velocity and Position](/problems/preintegrate-imu-translation). Preintegrate accelerometer velocity and position increments in the initial keyframe body frame.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Form a keyframe factor

<!-- source-flow: 2015-on-manifold-preintegration#stage-3 -->

Compare predicted state change with preintegrated measurements.

[Study the mechanism and math](/projects/2015-on-manifold-preintegration#paper-section-form-a-keyframe-factor).

- **Runnable paper-associated component:** [Apply a First-Order Bias Correction](/problems/first-order-imu-bias-correction). Apply supplied first-order bias Jacobians to an existing preintegrated measurement.
- **Proposed component, not runnable:** Propagate Preintegration Covariance.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Integrate relative rotation | relative rotations | Integrate velocity and position |
| Integrate velocity and position | preintegrated measurements | Form a keyframe factor |

## Integration exercise

**Proposed exercise — not runnable yet.** Construct a short synthetic calibrated sensor sequence with known camera poses, landmark coordinates and optional inertial samples; use a fixed seed and declare world/body/camera transforms, metres, radians and seconds. Compose the selected mechanisms in the declared flow, beginning with **Integrate relative rotation** and ending with **Form a keyframe factor**. Save each intermediate artifact so a learner can locate a mismatch at its originating stage.

The integration boundary is a bounded estimation or reconstruction component with analytic geometry; learned correspondence outputs may be supplied as fixed synthetic arrays. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2015-on-manifold-preintegration). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** For the **Integrate relative rotation → Form a keyframe factor** fixture, compare geometric residuals with a direct scalar calculation and compare recovered coordinates with the known synthetic scene; report the chosen alignment and gauge freedoms before giving pose error.

Use one clean baseline and a separately recorded fault case: reverse one transform, perturb one calibration value, or shift one sensor timestamp; report which residual and validity check changes. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **On-Manifold Preintegration for Real-Time Visual-Inertial Odometry** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record calibration hash, coordinate-frame convention, sensor clock convention, gauge/alignment choice and residual weights. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
