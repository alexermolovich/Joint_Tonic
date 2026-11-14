---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2020-nerf",
  "paper_id": "2020-nerf",
  "title": "NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis",
  "status": "bounded-integration-available",
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
    "nerf-calibrated-camera-rays",
    "nerf-hierarchical-depth-sampling",
    "nerf-fourier-features",
    "nerf-alpha-compositing",
    "nerf-render-color-depth",
    "nerf-pose-residual-diagnostics",
    "nerf-rendered-color-gradients",
    "nerf-tiny-field-training"
  ],
  "proposed_component_count": 0,
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
  "integration_status": "runnable",
  "assessment_status": "runnable",
  "integration_problem_slug": "nerf-tiny-field-training"
}
---

# NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis — implementation track

## Orientation and scope

NeRF represents a scene with a neural function that predicts density and view-dependent color at 3D locations. A camera pixel defines a ray; sampling the field along that ray and accumulating light produces its color. Training adjusts the field so rendered images agree with observed images from known camera poses. The useful implementation boundary is the rendering computation, which can be tested before any neural network is trained.

The implementation path follows **Construct camera rays → Query the radiance field → Composite and train**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/2003.08934) · [Paper explanation and graph](/projects/2020-nerf) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2020-nerf](../../../research/papers/vision-vlm-3d/2020-nerf.md).

**Available now:** 9 paper-associated runnable components; 0 supporting runnable components. **Proposed:** 0 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Construct camera rays** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

- **Supporting prerequisite:** [Project Camera Points into Pixels](/problems/project-camera-points). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Compute Transmittance and Alpha Compositing Weights](/problems/nerf-alpha-compositing). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Sample Hierarchical Depth Intervals](/problems/nerf-hierarchical-depth-sampling). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Encode 3D Positions with Fourier Features](/problems/nerf-fourier-features). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Render Color and Expected Depth Along a Ray](/problems/nerf-render-color-depth). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Differentiate Rendered Color on a Small Synthetic Field](/problems/nerf-rendered-color-gradients). Its own contract remains authoritative; it does not implement the entire paper.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Construct camera rays

<!-- source-flow: 2020-nerf#stage-1 -->

Use intrinsics and camera pose to express a pixel ray in the scene frame.

[Study the mechanism and math](/projects/2020-nerf#paper-section-construct-camera-rays).

- **Runnable paper-associated component:** [Stratify Samples Along Near and Far Bounds](/problems/nerf-stratified-samples). Stratify Samples Along Near and Far Bounds
- **Runnable paper-associated component:** [Generate Calibrated Camera Rays](/problems/nerf-calibrated-camera-rays). Turn supplied continuous pixel coordinates into world-space unit rays.
- **Runnable paper-associated component:** [Sample Hierarchical Depth Intervals](/problems/nerf-hierarchical-depth-sampling). Coarse rendering weights tell a fine sampler where useful mass lies along a ray.

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
- **Runnable paper-associated component:** [Detect Bad Poses with Reprojection and Render Residuals](/problems/nerf-pose-residual-diagnostics). Compute separate per-view geometric and photometric residual summaries with explicit missing-data flags.
- **Runnable paper-associated component:** [Differentiate Rendered Color on a Small Synthetic Field](/problems/nerf-rendered-color-gradients). Increasing one sample's density makes its own color more visible and hides everything behind it.
- **Runnable paper-associated component:** [Fit a Tiny Coordinate-Feature Radiance Field](/problems/nerf-tiny-field-training). Train a shared affine density/color field through volume rendering, then evaluate held-out rays.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Construct camera rays | ray samples | Query the radiance field |
| Query the radiance field | density and color | Composite and train |

## Integration exercise

**Runnable bounded integration:** [Fit a Tiny Coordinate-Feature Radiance Field](/problems/nerf-tiny-field-training). This exercises its declared synthetic contract, not the full paper benchmark.

Reproduce a small executable image-to-field learning loop: supplied coordinate features feed a shared density/color function, ordered volume rendering produces RGB, and analytic image gradients update the field. Finish by rendering held-out rays.

The integration uses an affine, view-independent field, fixed supplied samples, synthetic data and an explicit clipped SGD recipe. It omits the deep NeRF MLP, coarse/fine network training, view-direction conditioning, real camera datasets and headline benchmark comparisons. The separate hierarchical sampler is a stretch exercise, not an implicit feature of this task.

Before starting, check that you can explain why density attenuates downstream color and background. Use the renderer and gradient problems to diagnose that prerequisite. Keep one scene coordinate convention, normalized ray directions, metric intervals and linear RGB throughout.

## Evaluation and failure analysis

**Runnable assessment:** public/hidden cases for the linked integration.

Run checks a zero-error field and one analytically worked SGD update. Submit adds an independent scalar renderer, finite-difference parameter gradients, an active global-clipping case, held-out data isolation, maximum shapes, zero-step behavior and malformed inputs. Passing validates the declared bounded training loop; it is not evidence that a real scene has been reconstructed.

Inspect training loss and held-out RGB MSE separately. Change only evaluation targets and verify that learned parameters and training traces stay identical. Compare a bright background with a black one to expose missing background gradients. Inspect clipping norms; frequent clipping can mask a poor scale or learning-rate choice. Image agreement alone does not certify surface geometry, free space or robot safety.

Record the limitations of fixed features and sample locations. A future extension can compare supplied hierarchical samples or a deeper field, but it must introduce a reviewed contract and its own reproducibility evidence.

## Reproducibility deliverable

**Runnable project deliverable:** save the following report in the integration exercise’s Notes. The report is learner-authored, not automatically certified.

Record the problem/content version, Python/NumPy versions, coordinate-feature definition, scene frame, normalized ray convention, metric interval units, RGB preprocessing, exact synthetic fixture identity, initial weights/bias, step count, learning rate and gradient-clipping rule. The function draws no random values; record the seed used by any upstream fixture generator.

Report training loss before/after updates, raw gradient norms and held-out RGB MSE. State that evaluation data was excluded from optimization and selection. Describe the affine/view-independent field, fixed samples and clipped SGD as deviations from the source paper. Record compute and wall time without extrapolating toy results to full NeRF training or physical safety.

Source: [NeRF](https://arxiv.org/abs/2003.08934). Code, explanations and synthetic fixtures are original; local source PDFs remain authoring references.
