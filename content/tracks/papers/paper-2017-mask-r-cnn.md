---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2017-mask-r-cnn",
  "paper_id": "2017-mask-r-cnn",
  "title": "Mask R-CNN",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/1703.06870",
  "source_cards": [
    "research/papers/perception-3d/2017-mask-r-cnn.md"
  ],
  "paper_aliases": [],
  "category": "perception-3d",
  "topics": [
    "perception-3d",
    "mask-r-cnn"
  ],
  "runnable_problem_slugs": [],
  "proposed_component_count": 4,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2017-mask-r-cnn",
      "node": "stage-1"
    },
    {
      "card": "2017-mask-r-cnn",
      "node": "stage-2"
    },
    {
      "card": "2017-mask-r-cnn",
      "node": "stage-3"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# Mask R-CNN — implementation track

## Orientation and scope

Mask R-CNN extends region-based detection with a per-instance mask branch. Its ROIAlign operation preserves spatial correspondence by sampling continuous feature coordinates rather than quantizing region boundaries. Classification, box refinement, and mask prediction share the region features but solve different tasks.

The implementation path follows **Map regions to features → Sample with ROIAlign → Predict an instance mask**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/1703.06870) · [Paper explanation and graph](/projects/2017-mask-r-cnn) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2017-mask-r-cnn](../../../research/papers/perception-3d/2017-mask-r-cnn.md).

**Available now:** 0 paper-associated runnable components; 0 supporting runnable components. **Proposed:** 4 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Map regions to features** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

There is no independently runnable prerequisite mapped for this source yet. Use the source-card notation and stage contracts as the diagnostic; prerequisite exercises must be authored and reviewed before being presented as runnable.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Map regions to features

<!-- source-flow: 2017-mask-r-cnn#stage-1 -->

Convert image-space proposals into continuous feature-map coordinates.

[Study the mechanism and math](/projects/2017-mask-r-cnn#paper-section-map-regions-to-features).

- **Proposed component, not runnable:** Map Proposal Boxes to Feature-Map Coordinates.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Sample with ROIAlign

<!-- source-flow: 2017-mask-r-cnn#stage-2 -->

Use bilinear interpolation at planned points within each pooled bin.

[Study the mechanism and math](/projects/2017-mask-r-cnn#paper-section-sample-with-roialign).

- **Proposed component, not runnable:** Implement bilinear ROI sampling.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Predict an instance mask

<!-- source-flow: 2017-mask-r-cnn#stage-3 -->

Supervise the target class’s mask independently of category competition.

[Study the mechanism and math](/projects/2017-mask-r-cnn#paper-section-predict-an-instance-mask).

- **Proposed component, not runnable:** Construct class-specific mask targets.
- **Proposed component, not runnable:** Compare instance-mask IoU and box IoU.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Map regions to features | continuous regions | Sample with ROIAlign |
| Sample with ROIAlign | aligned region features | Predict an instance mask |

## Integration exercise

**Proposed exercise — not runnable yet.** Construct a tiny analytic scene or point set with known positions, synthetic features and declared visibility; provide original images only where the mechanism needs them. Compose the selected mechanisms in the declared flow, beginning with **Map regions to features** and ending with **Predict an instance mask**. Save each intermediate artifact so a learner can locate a mismatch at its originating stage.

The integration boundary is selected representation, geometry or rendering operations; large learned backbones can be represented by explicitly supplied synthetic features. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2017-mask-r-cnn). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** For the **Map regions to features → Predict an instance mask** fixture, compare reconstruction, matching or aggregation outputs with hand-computable scene quantities and an independent implementation on tiny arrays.

Use one clean baseline and a separately recorded fault case: remove observations, change point order, or insert an occluded surface; record the geometric or representation error by condition. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **Mask R-CNN** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record scene scale, camera convention, point ordering policy, visibility masks, interpolation rule and feature-generation seed. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
