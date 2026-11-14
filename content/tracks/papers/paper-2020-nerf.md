---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2020-nerf",
  "paper_id": "2020-nerf",
  "title": "NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/2003.08934",
  "source_cards": [
    "research/papers/vision-vlm-3d/2020-nerf.md"
  ],
  "paper_aliases": [],
  "category": "vision-vlm-3d",
  "topics": [
    "neural rendering",
    "novel-view synthesis",
    "volume rendering",
    "3D scene representation"
  ],
  "runnable_problem_slugs": [
    "nerf-stratified-samples",
    "nerf-fourier-features",
    "nerf-alpha-compositing",
    "nerf-render-color-depth"
  ],
  "proposed_component_count": 4,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2020-nerf",
      "node": "stage-1"
    },
    {
      "card": "2020-nerf",
      "node": "stage-2"
    },
    {
      "card": "2020-nerf",
      "node": "stage-3"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis — implementation track

## Orientation and scope

NeRF represents a scene with a neural function that predicts density and view-dependent color at 3D locations. A camera pixel defines a ray; sampling the field along that ray and accumulating light produces its color. Training adjusts the field so rendered images agree with observed images from known camera poses. The useful implementation boundary is the rendering computation, which can be tested before any neural network is trained.

The implementation path follows **Construct camera rays → Query the radiance field → Composite and train**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/2003.08934) · [Paper explanation and graph](/projects/2020-nerf) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2020-nerf](../../../research/papers/vision-vlm-3d/2020-nerf.md).

**Available now:** 4 paper-associated runnable components; 0 supporting runnable components. **Proposed:** 4 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Construct camera rays** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

- **Supporting prerequisite:** [Project Camera Points into Pixels](/problems/project-camera-points). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Compute Transmittance and Alpha Compositing Weights](/problems/nerf-alpha-compositing). Its own contract remains authoritative; it does not implement the entire paper.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Construct camera rays

<!-- source-flow: 2020-nerf#stage-1 -->

Use intrinsics and camera pose to express a pixel ray in the scene frame.

[Study the mechanism and math](/projects/2020-nerf#paper-section-construct-camera-rays).

- **Runnable paper-associated component:** [Stratify Samples Along Near and Far Bounds](/problems/nerf-stratified-samples). Stratify Samples Along Near and Far Bounds
- **Proposed component, not runnable:** Generate Calibrated Camera Rays.
- **Proposed component, not runnable:** Sample Hierarchical Depth Intervals.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Query the radiance field

<!-- source-flow: 2020-nerf#stage-2 -->

Predict density from position and color from position plus viewing direction.

[Study the mechanism and math](/projects/2020-nerf#paper-section-query-the-radiance-field).

- **Runnable paper-associated component:** [Encode 3D Positions with Fourier Features](/problems/nerf-fourier-features). Encode 3D Positions with Fourier Features

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Composite and train

<!-- source-flow: 2020-nerf#stage-3 -->

Accumulate visible colors in depth order and compare rendered pixels.

[Study the mechanism and math](/projects/2020-nerf#paper-section-composite-and-train).

- **Runnable paper-associated component:** [Compute Transmittance and Alpha Compositing Weights](/problems/nerf-alpha-compositing). Turn ordered ray densities and metric interval lengths into sample visibility weights and remaining background mass.
- **Runnable paper-associated component:** [Render Color and Expected Depth Along a Ray](/problems/nerf-render-color-depth). Render Color and Expected Depth Along a Ray
- **Proposed component, not runnable:** Detect Bad Poses with Reprojection and Render Residuals.
- **Proposed component, not runnable:** Differentiate Rendered Color on a Small Synthetic Field.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Construct camera rays | ray samples | Query the radiance field |
| Query the radiance field | density and color | Composite and train |

## Integration exercise

**Proposed exercise — not runnable yet.** Define two analytic camera rays with a few known density/color samples. Compose stratified sample placement, alpha/transmittance weights and RGB plus conditional foreground depth rendering. A coordinate-feature encoder may feed a small analytic field; training a photorealistic scene is outside this integration.

The integration boundary is a small perception component pipeline with supplied model outputs or tiny original weights; pretrained feature quality and paper-scale training are outside this exercise. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2020-nerf). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** Compare color against the exact weighted sum and separate background-only rays from rays with valid foreground depth. Check zero density and nearly opaque samples, and state that conditional depth differs from an unnormalized expected depth moment.

Use one clean baseline and a separately recorded fault case: permute an input ordering, corrupt one coordinate convention, or remove a valid observation; check the method-specific invariance or rejection rule. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record image/ray/box conventions, normalization, feature widths, class mapping, numeric tolerances and fixture seed. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
