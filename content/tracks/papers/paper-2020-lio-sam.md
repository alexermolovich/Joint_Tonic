---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2020-lio-sam",
  "paper_id": "2020-lio-sam",
  "title": "LIO-SAM: Tightly-coupled Lidar Inertial Odometry via Smoothing and Mapping",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/2007.00258",
  "source_cards": [
    "research/papers/geometry-calibration-slam/2020-lio-sam.md"
  ],
  "paper_aliases": [],
  "category": "geometry-calibration-slam",
  "topics": [
    "geometry-calibration-slam",
    "lio-sam"
  ],
  "runnable_problem_slugs": [],
  "proposed_component_count": 4,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2020-lio-sam",
      "node": "stage-1"
    },
    {
      "card": "2020-lio-sam",
      "node": "stage-2"
    },
    {
      "card": "2020-lio-sam",
      "node": "stage-3"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# LIO-SAM: Tightly-coupled Lidar Inertial Odometry via Smoothing and Mapping — implementation track

## Orientation and scope

LIO-SAM couples lidar and IMU through factor-graph smoothing. IMU preintegration supplies motion estimates for scan deskewing and initialization, while lidar alignment constrains drift and helps estimate inertial biases.

The implementation path follows **Deskew lidar measurements → Align local scan features → Smooth sensor factors**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/2007.00258) · [Paper explanation and graph](/projects/2020-lio-sam) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2020-lio-sam](../../../research/papers/geometry-calibration-slam/2020-lio-sam.md).

**Available now:** 0 paper-associated runnable components; 0 supporting runnable components. **Proposed:** 4 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Deskew lidar measurements** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

There is no independently runnable prerequisite mapped for this source yet. Use the source-card notation and stage contracts as the diagnostic; prerequisite exercises must be authored and reviewed before being presented as runnable.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Deskew lidar measurements

<!-- source-flow: 2020-lio-sam#stage-1 -->

Move points captured at different times into one scan frame.

[Study the mechanism and math](/projects/2020-lio-sam#paper-section-deskew-lidar-measurements).

- **Proposed component, not runnable:** Deskew a Lidar Scan with Motion Estimates.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Align local scan features

<!-- source-flow: 2020-lio-sam#stage-2 -->

Match edge and surface features against a local map.

[Study the mechanism and math](/projects/2020-lio-sam#paper-section-align-local-scan-features).

- **Proposed component, not runnable:** Compute Point-to-Line and Point-to-Plane Scan Residuals.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Smooth sensor factors

<!-- source-flow: 2020-lio-sam#stage-3 -->

Combine inertial, lidar, GPS, and loop constraints when available.

[Study the mechanism and math](/projects/2020-lio-sam#paper-section-smooth-sensor-factors).

- **Proposed component, not runnable:** Assemble an IMU-Lidar Pose Constraint.
- **Proposed component, not runnable:** Reject Inconsistent Loop Closures.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Deskew lidar measurements | deskewed scan | Align local scan features |
| Align local scan features | relative pose factors | Smooth sensor factors |

## Integration exercise

**Proposed exercise — not runnable yet.** Construct a short synthetic calibrated sensor sequence with known camera poses, landmark coordinates and optional inertial samples; use a fixed seed and declare world/body/camera transforms, metres, radians and seconds. Compose the selected mechanisms in the declared flow, beginning with **Deskew lidar measurements** and ending with **Smooth sensor factors**. Save each intermediate artifact so a learner can locate a mismatch at its originating stage.

The integration boundary is a bounded estimation or reconstruction component with analytic geometry; learned correspondence outputs may be supplied as fixed synthetic arrays. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2020-lio-sam). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** For the **Deskew lidar measurements → Smooth sensor factors** fixture, compare geometric residuals with a direct scalar calculation and compare recovered coordinates with the known synthetic scene; report the chosen alignment and gauge freedoms before giving pose error.

Use one clean baseline and a separately recorded fault case: reverse one transform, perturb one calibration value, or shift one sensor timestamp; report which residual and validity check changes. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **LIO-SAM: Tightly-coupled Lidar Inertial Odometry via Smoothing and Mapping** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record calibration hash, coordinate-frame convention, sensor clock convention, gauge/alignment choice and residual weights. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
