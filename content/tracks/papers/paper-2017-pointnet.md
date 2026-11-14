---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2017-pointnet",
  "paper_id": "2017-pointnet",
  "title": "PointNet: Deep Learning on Point Sets for 3D Classification and Segmentation",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/1612.00593",
  "source_cards": [
    "research/papers/vision-vlm-3d/2017-pointnet.md"
  ],
  "paper_aliases": [],
  "category": "vision-vlm-3d",
  "topics": [
    "point clouds",
    "3D classification",
    "3D segmentation",
    "permutation invariance"
  ],
  "runnable_problem_slugs": [
    "pointnet-transform-regularizer",
    "pointnet-symmetric-pooling",
    "pointnet-local-global-features"
  ],
  "proposed_component_count": 2,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2017-pointnet",
      "node": "stage-1"
    },
    {
      "card": "2017-pointnet",
      "node": "stage-2"
    },
    {
      "card": "2017-pointnet",
      "node": "stage-3"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# PointNet: Deep Learning on Point Sets for 3D Classification and Segmentation — implementation track

## Orientation and scope

PointNet learns directly from an unordered point set. A shared network maps each point to features, a symmetric pooling operation creates a global description, and task heads predict a set label or per-point labels. The central requirement is permutation invariance: changing the order of the same physical points must not change a global prediction. This differs from placing points into a regular voxel grid.

The implementation path follows **Encode each point → Pool the point set → Classify or segment**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/1612.00593) · [Paper explanation and graph](/projects/2017-pointnet) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2017-pointnet](../../../research/papers/vision-vlm-3d/2017-pointnet.md).

**Available now:** 3 paper-associated runnable components; 0 supporting runnable components. **Proposed:** 2 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Encode each point** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

- **Supporting prerequisite:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Prove Permutation Invariance with Symmetric Pooling](/problems/pointnet-symmetric-pooling). Its own contract remains authoritative; it does not implement the entire paper.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Encode each point

<!-- source-flow: 2017-pointnet#stage-1 -->

Apply one shared feature map to every point in the cloud.

[Study the mechanism and math](/projects/2017-pointnet#paper-section-encode-each-point).

- **Runnable paper-associated component:** [Regularize a Learned Feature Transform](/problems/pointnet-transform-regularizer). Regularize a Learned Feature Transform
- **Proposed component, not runnable:** Build a Shared Point MLP and Global Feature.
- **Proposed component, not runnable:** Validate Point-Cloud Density and Coordinate Conventions.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Pool the point set

<!-- source-flow: 2017-pointnet#stage-2 -->

Channel-wise maximum removes dependence on point ordering.

[Study the mechanism and math](/projects/2017-pointnet#paper-section-pool-the-point-set).

- **Runnable paper-associated component:** [Prove Permutation Invariance with Symmetric Pooling](/problems/pointnet-symmetric-pooling). Pool valid point features channel by channel and demonstrate that point order cannot change the result.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Classify or segment

<!-- source-flow: 2017-pointnet#stage-3 -->

Use a global head or combine local and global features at every point.

[Study the mechanism and math](/projects/2017-pointnet#paper-section-classify-or-segment).

- **Runnable paper-associated component:** [Concatenate Local and Global Features for Segmentation](/problems/pointnet-local-global-features). Concatenate Local and Global Features for Segmentation

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Encode each point | point features | Pool the point set |
| Pool the point set | global descriptor | Classify or segment |

## Integration exercise

**Proposed exercise — not runnable yet.** Construct small synthetic images, boxes, embeddings or rays chosen to match the first mechanism; retain ground-truth geometry and any correspondence labels. Compose the selected mechanisms in the declared flow, beginning with **Encode each point** and ending with **Classify or segment**. Save each intermediate artifact so a learner can locate a mismatch at its originating stage.

The integration boundary is a small perception component pipeline with supplied model outputs or tiny original weights; pretrained feature quality and paper-scale training are outside this exercise. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2017-pointnet). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** For the **Encode each point → Classify or segment** fixture, compare tensor outputs with an independent scalar or exhaustive oracle and report the relevant matching, reconstruction or retrieval metric on the declared synthetic labels.

Use one clean baseline and a separately recorded fault case: permute an input ordering, corrupt one coordinate convention, or remove a valid observation; check the method-specific invariance or rejection rule. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **PointNet: Deep Learning on Point Sets for 3D Classification and Segmentation** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record image/ray/box conventions, normalization, feature widths, class mapping, numeric tolerances and fixture seed. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
