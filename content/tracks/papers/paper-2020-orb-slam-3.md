---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2020-orb-slam-3",
  "paper_id": "2020-orb-slam-3",
  "title": "ORB-SLAM3: An Accurate Open-Source Library for Visual, Visual-Inertial and Multi-Map SLAM",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/2007.11898",
  "source_cards": [
    "research/papers/geometry-calibration-slam/2020-orb-slam-3.md"
  ],
  "paper_aliases": [],
  "category": "geometry-calibration-slam",
  "topics": [
    "geometry-calibration-slam",
    "orb-slam-3"
  ],
  "runnable_problem_slugs": [
    "visual-inertial-initialization-gate",
    "visual-inertial-keyframe-residual",
    "aligned-trajectory-position-error"
  ],
  "proposed_component_count": 1,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2020-orb-slam-3",
      "node": "stage-1"
    },
    {
      "card": "2020-orb-slam-3",
      "node": "stage-2"
    },
    {
      "card": "2020-orb-slam-3",
      "node": "stage-3"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# ORB-SLAM3: An Accurate Open-Source Library for Visual, Visual-Inertial and Multi-Map SLAM — implementation track

## Orientation and scope

ORB-SLAM3 extends feature-based SLAM with tightly integrated visual-inertial estimation and an atlas of multiple maps. It can start a new map after tracking loss and later merge maps when a verified shared place is found.

The implementation path follows **Initialize inertial estimation → Track and refine a map → Reuse and merge maps**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/2007.11898) · [Paper explanation and graph](/projects/2020-orb-slam-3) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2020-orb-slam-3](../../../research/papers/geometry-calibration-slam/2020-orb-slam-3.md).

**Available now:** 2 paper-associated runnable components; 1 supporting runnable component. **Proposed:** 1 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Initialize inertial estimation** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

- **Supporting prerequisite:** [Build a Visual-Inertial Residual](/problems/visual-inertial-keyframe-residual). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Detect Unobservable Initialization Motion](/problems/initialization-observability-rank). Its own contract remains authoritative; it does not implement the entire paper.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Initialize inertial estimation

<!-- source-flow: 2020-orb-slam-3#stage-1 -->

Estimate scale, gravity, velocity, and bias with probabilistic priors.

[Study the mechanism and math](/projects/2020-orb-slam-3#paper-section-initialize-inertial-estimation).

- **Runnable paper-associated component:** [Validate a Visual-Inertial Initialization](/problems/visual-inertial-initialization-gate). `validate_initialization(scale, gravity, gyro_bias, accel_bias, residuals, valid, jacobian, limits)` scale builtinfloat/int[1e-6,1e3];gravity3worldm/s²,gyro_bias3rad/s,accel_bias3m/s²;residuals(R)alreadywhiteneddimensionless,valid(R)bool,R0..4096;jacobian(R,D)dimensionless whitened/scaled gauge-fixed,1<=D<=32,abs<=1000;limits(7)floats = [min_scale,max_scale,gravity_tolerance,max_gyro_norm,max_accel_norm,max_rms,relative_rank_cutoff], scaleintervalwithin[1e-6,1e3]ordered, otherthresholds[0,1000], cutoff[1e-12,.01]. Eligible rowsvalid determine RMSandSVD rank strict sigma>cut*sigma_max. Return countint,rankint,rmsfloat(NaNifnone),gravity_errorfloat abs(normgravity−9.81),checks bool(6) ordered [atleastDvalidrows AND rankD, minscale<=scale<=maxscale, gravityerror<=tol, gyronorm<=max,accelnorm<=max,rms<=max],acceptedbool(allchecks). No-evidence RMScheckFalse. Original inspectable diagnostic over supplied initialization candidate, not optimizer, ORB-SLAM3 exact acceptanceheuristic, or nonlinearobservability proof. Gravity directionnotgated: estimateisworldframe and onlymagnitudecheck. ExampleD1,R1,J[[1]],residual[.2],validTrue,scale1,g[0,0,-9.81],biases0,limits[.5,2,.1,.1,.1,.2,1e-6]=>allTrue,rms.2,rank1. ExampletwoidenticalJrows[[1,0],[1,0]],residual0=>rank1,firstFalse,rejectevenperfectfit.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Track and refine a map

<!-- source-flow: 2020-orb-slam-3#stage-2 -->

Optimize feature reprojection and inertial constraints together.

[Study the mechanism and math](/projects/2020-orb-slam-3#paper-section-track-and-refine-a-map).

- **Runnable supporting prerequisite:** [Build a Visual-Inertial Residual](/problems/visual-inertial-keyframe-residual). Combine a keyframe IMU residual with already computed visual residuals using declared diagonal uncertainties.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Reuse and merge maps

<!-- source-flow: 2020-orb-slam-3#stage-3 -->

Geometrically verify common places across atlas maps.

[Study the mechanism and math](/projects/2020-orb-slam-3#paper-section-reuse-and-merge-maps).

- **Runnable paper-associated component:** [Evaluate Trajectory Error After Alignment](/problems/aligned-trajectory-position-error). Align time-matched estimated and reference camera positions before reporting absolute position error.
- **Proposed component, not runnable:** Merge Consistent Map Transforms.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Initialize inertial estimation | initialized state | Track and refine a map |
| Track and refine a map | keyframe atlas | Reuse and merge maps |

## Integration exercise

**Proposed exercise — not runnable yet.** Construct a short synthetic calibrated sensor sequence with known camera poses, landmark coordinates and optional inertial samples; use a fixed seed and declare world/body/camera transforms, metres, radians and seconds. Compose the selected mechanisms in the declared flow, beginning with **Initialize inertial estimation** and ending with **Reuse and merge maps**. Save each intermediate artifact so a learner can locate a mismatch at its originating stage.

The integration boundary is a bounded estimation or reconstruction component with analytic geometry; learned correspondence outputs may be supplied as fixed synthetic arrays. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2020-orb-slam-3). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** For the **Initialize inertial estimation → Reuse and merge maps** fixture, compare geometric residuals with a direct scalar calculation and compare recovered coordinates with the known synthetic scene; report the chosen alignment and gauge freedoms before giving pose error.

Use one clean baseline and a separately recorded fault case: reverse one transform, perturb one calibration value, or shift one sensor timestamp; report which residual and validity check changes. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **ORB-SLAM3: An Accurate Open-Source Library for Visual, Visual-Inertial and Multi-Map SLAM** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record calibration hash, coordinate-frame convention, sensor clock convention, gauge/alignment choice and residual weights. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
