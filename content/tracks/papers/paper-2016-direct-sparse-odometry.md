---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2016-direct-sparse-odometry",
  "paper_id": "2016-direct-sparse-odometry",
  "title": "Direct Sparse Odometry",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/1607.02565",
  "source_cards": [
    "research/papers/geometry-calibration-slam/2016-direct-sparse-odometry.md"
  ],
  "paper_aliases": [],
  "category": "geometry-calibration-slam",
  "topics": [
    "geometry-calibration-slam",
    "direct-sparse-odometry"
  ],
  "runnable_problem_slugs": [],
  "proposed_component_count": 3,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2016-direct-sparse-odometry",
      "node": "stage-1"
    },
    {
      "card": "2016-direct-sparse-odometry",
      "node": "stage-2"
    },
    {
      "card": "2016-direct-sparse-odometry",
      "node": "stage-3"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# Direct Sparse Odometry — implementation track

## Orientation and scope

Direct Sparse Odometry estimates camera motion and sparse inverse depths directly from image intensities. It optimizes photometric consistency with exposure and brightness modeling, instead of relying on descriptor matching for every observation.

The implementation path follows **Warp a depth hypothesis → Measure photometric error → Optimize a sparse window**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/1607.02565) · [Paper explanation and graph](/projects/2016-direct-sparse-odometry) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2016-direct-sparse-odometry](../../../research/papers/geometry-calibration-slam/2016-direct-sparse-odometry.md).

**Available now:** 0 paper-associated runnable components; 0 supporting runnable components. **Proposed:** 3 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Warp a depth hypothesis** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

There is no independently runnable prerequisite mapped for this source yet. Use the source-card notation and stage contracts as the diagnostic; prerequisite exercises must be authored and reviewed before being presented as runnable.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Warp a depth hypothesis

<!-- source-flow: 2016-direct-sparse-odometry#stage-1 -->

Project a reference pixel into another camera.

[Study the mechanism and math](/projects/2016-direct-sparse-odometry#paper-section-warp-a-depth-hypothesis).

- **Proposed component, not runnable:** Warp a Point Between Calibrated Frames.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Measure photometric error

<!-- source-flow: 2016-direct-sparse-odometry#stage-2 -->

Account for exposure and affine brightness changes.

[Study the mechanism and math](/projects/2016-direct-sparse-odometry#paper-section-measure-photometric-error).

- **Proposed component, not runnable:** Compute an Exposure-Corrected Photometric Residual.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Optimize a sparse window

<!-- source-flow: 2016-direct-sparse-odometry#stage-3 -->

Jointly update poses, depths, and brightness parameters.

[Study the mechanism and math](/projects/2016-direct-sparse-odometry#paper-section-optimize-a-sparse-window).

- **Proposed component, not runnable:** Select High-Gradient Image Points.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Warp a depth hypothesis | warped pixels | Measure photometric error |
| Measure photometric error | weighted residuals | Optimize a sparse window |

## Integration exercise

**Proposed exercise — not runnable yet.** Construct a short synthetic calibrated sensor sequence with known camera poses, landmark coordinates and optional inertial samples; use a fixed seed and declare world/body/camera transforms, metres, radians and seconds. Compose the selected mechanisms in the declared flow, beginning with **Warp a depth hypothesis** and ending with **Optimize a sparse window**. Save each intermediate artifact so a learner can locate a mismatch at its originating stage.

The integration boundary is a bounded estimation or reconstruction component with analytic geometry; learned correspondence outputs may be supplied as fixed synthetic arrays. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2016-direct-sparse-odometry). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** For the **Warp a depth hypothesis → Optimize a sparse window** fixture, compare geometric residuals with a direct scalar calculation and compare recovered coordinates with the known synthetic scene; report the chosen alignment and gauge freedoms before giving pose error.

Use one clean baseline and a separately recorded fault case: reverse one transform, perturb one calibration value, or shift one sensor timestamp; report which residual and validity check changes. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **Direct Sparse Odometry** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record calibration hash, coordinate-frame convention, sensor clock convention, gauge/alignment choice and residual weights. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
