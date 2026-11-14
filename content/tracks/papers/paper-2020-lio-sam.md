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
  "runnable_problem_slugs": [
    "interpolate-pose-slerp",
    "trace-perception-frame-graph",
    "deskew-lidar-points",
    "lidar-feature-residuals",
    "imu-lidar-extrinsic-pose-residual",
    "loop-closure-consistency-gate"
  ],
  "proposed_component_count": 0,
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

**Available now:** 4 paper-associated runnable components; 2 supporting runnable components. **Proposed:** 0 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Deskew lidar measurements** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

- **Supporting prerequisite:** [Interpolate a Pose with SLERP](/problems/interpolate-pose-slerp). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Trace Frames Through a Robot Perception Graph](/problems/trace-perception-frame-graph). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Compose and Invert Coordinate Transforms](/problems/compose-frame-transforms). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Apply SE(3) Exponential and Logarithm Maps](/problems/se3-exponential-logarithm). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Gate Measurements with Mahalanobis Distance](/problems/mahalanobis-measurement-gate). Its own contract remains authoritative; it does not implement the entire paper.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Deskew lidar measurements

<!-- source-flow: 2020-lio-sam#stage-1 -->

Move points captured at different times into one scan frame.

[Study the mechanism and math](/projects/2020-lio-sam#paper-section-deskew-lidar-measurements).

- **Runnable supporting prerequisite:** [Interpolate a Pose with SLERP](/problems/interpolate-pose-slerp). Interpolate translation linearly and orientation along the shortest quaternion arc.
- **Runnable supporting prerequisite:** [Trace Frames Through a Robot Perception Graph](/problems/trace-perception-frame-graph). Resolve a rigid transform between two frames in a validated acyclic frame forest.
- **Runnable paper-associated component:** [Deskew a Lidar Scan with Motion Estimates](/problems/deskew-lidar-points). Express points captured at different instants in one reference lidar frame using supplied per-point poses.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Align local scan features

<!-- source-flow: 2020-lio-sam#stage-2 -->

Match edge and surface features against a local map.

[Study the mechanism and math](/projects/2020-lio-sam#paper-section-align-local-scan-features).

- **Runnable paper-associated component:** [Compute Point-to-Line and Point-to-Plane Scan Residuals](/problems/lidar-feature-residuals). Compute signed point-to-plane and unsigned point-to-line residuals after transforming scan features into the map frame.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Smooth sensor factors

<!-- source-flow: 2020-lio-sam#stage-3 -->

Combine inertial, lidar, GPS, and loop constraints when available.

[Study the mechanism and math](/projects/2020-lio-sam#paper-section-smooth-sensor-factors).

- **Runnable paper-associated component:** [Assemble an IMU-Lidar Pose Constraint](/problems/imu-lidar-extrinsic-pose-residual). `imu_lidar_residual(world_from_imu, imu_from_lidar, lidar_relative, std)` world_from_imu(2,4,4),sharedextrinsic(4,4),lidar_relative(4,4) maps lidar-j into lidar-i;std(6)in[1e-6,1000], translationmeters thenrotationradians. Predicted lidarrelative=(Ti Til)^-1(Tj Til). E=lidar_relative^-1 predicted. Return predicted(4,4),translation=E[:3,3] with shape (3,),rotation=Log(E.R)(3),whitened(6)=concattranslation,rotation/std,costhalf norm². Requireprincipalrotationerror<=pi−1e-4. Translation is in measured residual frame; split translation/rotation residual is explicitly NOT full SE3Log translational Jacobian or complete LIO-SAM IMU velocity/bias factor. ExampleextrinsicI,posesI andtranslationx2,measuredtranslationx1,std1=>translation[1,0,0],rotation0,cost.5. ExamplepureIMURz90 with lidarleverarm[1,0,0]=>predictedRz90,translation[-1,1,0],matchingmeasurement giveszero. Knownextrinsics are essential.
- **Runnable paper-associated component:** [Reject Inconsistent Loop Closures](/problems/loop-closure-consistency-gate). `gate_loop_closures(residuals, covariance, overlap, elapsed, threshold, min_overlap, min_elapsed)` residuals(K,6),0<=K<=8192, translationmeters+rotationradians supplied same tangent convention; covariance(K,6,6),symmetricatol1e-9 thenaverage,positive eigenvalues satisfy lambda_min>=max(1e-9,lambda_max*1e-8). overlap(K)fraction[0,1],elapsed(K)seconds[0,1e6];thresholdscalar[0,1e6]on squaredMahalanobis,min_overlap[0,1],min_elapsed[0,1e6]. Return squared_distance(K)=r.Tsolve(C,r),accepted(K)=(d<=threshold)&(overlap>=min)&(elapsed>=min),reason int64(K) priority1 elapsed too short,2 overlap low,3 Mahalanobis too large,0 accepted. All values validated even rejected for earlierreasons. Covariance cross terms matter. Original operational consistency gate for supplied registration evidence; not LIO-SAM's actual ICP fitness heuristic, a probability guarantee, or loop proposal/registration. Example r=[2,0,0,0,0,0],C=I,threshold4,overlap.5,min.5,elapsed10,min10=>d4accepted. Exampleelapsed9 andoverlap0 andlargeerror=>reason1; empty arrayscorrectshapes. Covariance entry C[i,j] has the product of residual coordinate i and j units (m², m·rad, or rad²).

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
