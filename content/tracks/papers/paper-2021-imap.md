---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2021-imap",
  "paper_id": "2021-imap",
  "title": "iMAP: Implicit Mapping and Positioning in Real-Time",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/2103.12352",
  "source_cards": [
    "research/papers/geometry-calibration-slam/2021-imap.md"
  ],
  "paper_aliases": [],
  "category": "geometry-calibration-slam",
  "topics": [
    "geometry-calibration-slam",
    "imap"
  ],
  "runnable_problem_slugs": [
    "nerf-alpha-compositing"
  ],
  "proposed_component_count": 4,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2021-imap",
      "node": "stage-1"
    },
    {
      "card": "2021-imap",
      "node": "stage-2"
    },
    {
      "card": "2021-imap",
      "node": "stage-3"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# iMAP: Implicit Mapping and Positioning in Real-Time — implementation track

## Orientation and scope

iMAP represents a scene with a neural network and jointly estimates camera poses and the map from RGB-D observations. Rendering predicts color and depth, allowing tracking and mapping to use the same scene representation.

The implementation path follows **Query the implicit scene → Render color and depth → Track and update the map**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/2103.12352) · [Paper explanation and graph](/projects/2021-imap) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2021-imap](../../../research/papers/geometry-calibration-slam/2021-imap.md).

**Available now:** 0 paper-associated runnable components; 1 supporting runnable component. **Proposed:** 4 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Query the implicit scene** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

- **Supporting prerequisite:** [Compute Transmittance and Alpha Compositing Weights](/problems/nerf-alpha-compositing). Its own contract remains authoritative; it does not implement the entire paper.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Query the implicit scene

<!-- source-flow: 2021-imap#stage-1 -->

Map world points to color and volume density.

[Study the mechanism and math](/projects/2021-imap#paper-section-query-the-implicit-scene).

- **Proposed component, not runnable:** Query Color and Density from a Coordinate MLP.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Render color and depth

<!-- source-flow: 2021-imap#stage-2 -->

Accumulate transmittance-weighted samples.

[Study the mechanism and math](/projects/2021-imap#paper-section-render-color-and-depth).

- **Runnable supporting prerequisite:** [Compute Transmittance and Alpha Compositing Weights](/problems/nerf-alpha-compositing). Turn ordered ray densities and metric interval lengths into sample visibility weights and remaining background mass.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Track and update the map

<!-- source-flow: 2021-imap#stage-3 -->

Optimize poses and network parameters using keyframes.

[Study the mechanism and math](/projects/2021-imap#paper-section-track-and-update-the-map).

- **Proposed component, not runnable:** Sample Informative Mapping Pixels.
- **Proposed component, not runnable:** Optimize a Camera Pose Against a Neural Map.
- **Proposed component, not runnable:** Choose Keyframes by Reconstruction Error.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Query the implicit scene | ray samples | Render color and depth |
| Render color and depth | rendered observations | Track and update the map |

## Integration exercise

**Proposed exercise — not runnable yet.** Construct a short synthetic calibrated sensor sequence with known camera poses, landmark coordinates and optional inertial samples; use a fixed seed and declare world/body/camera transforms, metres, radians and seconds. Compose the selected mechanisms in the declared flow, beginning with **Query the implicit scene** and ending with **Track and update the map**. Save each intermediate artifact so a learner can locate a mismatch at its originating stage.

The integration boundary is a bounded estimation or reconstruction component with analytic geometry; learned correspondence outputs may be supplied as fixed synthetic arrays. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2021-imap). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** For the **Query the implicit scene → Track and update the map** fixture, compare geometric residuals with a direct scalar calculation and compare recovered coordinates with the known synthetic scene; report the chosen alignment and gauge freedoms before giving pose error.

Use one clean baseline and a separately recorded fault case: reverse one transform, perturb one calibration value, or shift one sensor timestamp; report which residual and validity check changes. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **iMAP: Implicit Mapping and Positioning in Real-Time** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record calibration hash, coordinate-frame convention, sensor clock convention, gauge/alignment choice and residual weights. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
