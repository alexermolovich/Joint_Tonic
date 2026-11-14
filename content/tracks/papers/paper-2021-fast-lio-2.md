---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2021-fast-lio-2",
  "paper_id": "2021-fast-lio-2",
  "title": "FAST-LIO2: Fast Direct LiDAR-inertial Odometry",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/2107.06829",
  "source_cards": [
    "research/papers/geometry-calibration-slam/2021-fast-lio-2.md"
  ],
  "paper_aliases": [],
  "category": "geometry-calibration-slam",
  "topics": [
    "geometry-calibration-slam",
    "fast-lio-2"
  ],
  "runnable_problem_slugs": [
    "associate-local-map-planes",
    "lidar-feature-residuals",
    "incremental-voxel-local-map"
  ],
  "proposed_component_count": 1,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2021-fast-lio-2",
      "node": "stage-1"
    },
    {
      "card": "2021-fast-lio-2",
      "node": "stage-2"
    },
    {
      "card": "2021-fast-lio-2",
      "node": "stage-3"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# FAST-LIO2: Fast Direct LiDAR-inertial Odometry — implementation track

## Orientation and scope

FAST-LIO2 registers raw lidar points directly to a map using a tightly coupled iterated Kalman filter. An incremental k-d tree supports fast nearest-neighbor lookup, map insertion, deletion, and local-map maintenance.

The implementation path follows **Propagate the inertial state → Iterate point-to-map updates → Maintain the local map**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/2107.06829) · [Paper explanation and graph](/projects/2021-fast-lio-2) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2021-fast-lio-2](../../../research/papers/geometry-calibration-slam/2021-fast-lio-2.md).

**Available now:** 3 paper-associated runnable components; 0 supporting runnable components. **Proposed:** 1 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Propagate the inertial state** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

- **Supporting prerequisite:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). Its own contract remains authoritative; it does not implement the entire paper.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Propagate the inertial state

<!-- source-flow: 2021-fast-lio-2#stage-1 -->

Predict pose, velocity, biases, and covariance.

[Study the mechanism and math](/projects/2021-fast-lio-2#paper-section-propagate-the-inertial-state).

- **Proposed component, not runnable:** Propagate an Error-State IMU Mean and Covariance.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Iterate point-to-map updates

<!-- source-flow: 2021-fast-lio-2#stage-2 -->

Use raw-point geometric residuals without a feature-extraction stage.

[Study the mechanism and math](/projects/2021-fast-lio-2#paper-section-iterate-point-to-map-updates).

- **Runnable paper-associated component:** [Associate Scan Points with Local Map Planes](/problems/associate-local-map-planes). Associate each deskewed world-frame scan query with a deterministic local plane fitted to nearby map points.
- **Runnable paper-associated component:** [Compute Point-to-Line and Point-to-Plane Scan Residuals](/problems/lidar-feature-residuals). Compute signed point-to-plane and unsigned point-to-line residuals after transforming scan features into the map frame.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Maintain the local map

<!-- source-flow: 2021-fast-lio-2#stage-3 -->

Update an incremental spatial index.

[Study the mechanism and math](/projects/2021-fast-lio-2#paper-section-maintain-the-local-map).

- **Runnable paper-associated component:** [Update an Incremental Local Map](/problems/incremental-voxel-local-map). `update_local_map(existing, scan, world_from_lidar, center, half_extent, voxel_size)` existing(M,3)worldpoints,scan(N,3)lidarpoints,M/N0..16384, abs<=1e4; transformproper withtranslationabs<=1e4;center(3)worldmetersabs<=1e4;half_extent(3)meters[1e-3,1e4],voxelscalar[1e-3,1000]meters. Transformscanintoworld; merge candidates in existing-then-scan index order. Keep points in inclusive axis-aligned center±extent. Voxel key=floor(worldpoint/size),globaloriginfixedzero,negativecoordsfloor. Within each occupied voxel retain candidate closest in squaredmeters to voxelcenter (key+.5)*size, tie lower mergedcandidateindex. Return points(V,3),voxel_keys(V,3)int64,source_indices(V)int64(sortedlexicographicvoxelkeys),removed_existing(M)bool true iff existing point notretained (outsideorlosesvoxel). Candidateidentity from concatenation. Deterministic batch teaching equivalent of pruning/downsampling decisions; no incremental ikd-tree, runtimeclaim or scan deskew. Exampleexisting[[.1,0,0],[.4,0,0]],scan[[.6,0,0]],I,center0,extent2,voxel1=>selectexistingindex1 (equal .4/.6 center distances tie earlier),key[0,0,0],removed[True,False]. Exampleexisting[[-.1,0,0]],scanzero,I,size1=>keys[-1,0,0],[0,0,0] distinct. Implementation should handle up to32768candidates without quadraticpairwisearrays.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Propagate the inertial state | predicted state | Iterate point-to-map updates |
| Iterate point-to-map updates | corrected scan pose | Maintain the local map |

## Integration exercise

**Proposed exercise — not runnable yet.** Construct a short synthetic calibrated sensor sequence with known camera poses, landmark coordinates and optional inertial samples; use a fixed seed and declare world/body/camera transforms, metres, radians and seconds. Compose the selected mechanisms in the declared flow, beginning with **Propagate the inertial state** and ending with **Maintain the local map**. Save each intermediate artifact so a learner can locate a mismatch at its originating stage.

The integration boundary is a bounded estimation or reconstruction component with analytic geometry; learned correspondence outputs may be supplied as fixed synthetic arrays. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2021-fast-lio-2). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** For the **Propagate the inertial state → Maintain the local map** fixture, compare geometric residuals with a direct scalar calculation and compare recovered coordinates with the known synthetic scene; report the chosen alignment and gauge freedoms before giving pose error.

Use one clean baseline and a separately recorded fault case: reverse one transform, perturb one calibration value, or shift one sensor timestamp; report which residual and validity check changes. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **FAST-LIO2: Fast Direct LiDAR-inertial Odometry** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record calibration hash, coordinate-frame convention, sensor clock convention, gauge/alignment choice and residual weights. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
