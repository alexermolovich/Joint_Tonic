---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2015-faster-r-cnn",
  "paper_id": "2015-faster-r-cnn",
  "title": "Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/1506.01497",
  "source_cards": [
    "research/papers/perception-3d/2015-faster-r-cnn.md"
  ],
  "paper_aliases": [],
  "category": "perception-3d",
  "topics": [
    "perception-3d",
    "faster-r-cnn"
  ],
  "runnable_problem_slugs": [
    "box-iou-broadcast",
    "class-aware-nms"
  ],
  "proposed_component_count": 4,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2015-faster-r-cnn",
      "node": "stage-1"
    },
    {
      "card": "2015-faster-r-cnn",
      "node": "stage-2"
    },
    {
      "card": "2015-faster-r-cnn",
      "node": "stage-3"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks — implementation track

## Orientation and scope

Faster R-CNN uses a region-proposal network to suggest object regions from shared image features, then a second stage classifies and refines those regions. Sharing the feature backbone avoids running a separate expensive proposal system. The two-stage design creates clear implementation boundaries: anchors and regression targets, proposal filtering, and region-based prediction.

The implementation path follows **Encode anchor targets → Select region proposals → Classify and refine regions**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/1506.01497) · [Paper explanation and graph](/projects/2015-faster-r-cnn) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2015-faster-r-cnn](../../../research/papers/perception-3d/2015-faster-r-cnn.md).

**Available now:** 0 paper-associated runnable components; 2 supporting runnable components. **Proposed:** 4 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Encode anchor targets** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

- **Supporting prerequisite:** [Compute Pairwise Bounding-Box IoU](/problems/box-iou-broadcast). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Run Class-Aware Non-Maximum Suppression](/problems/class-aware-nms). Its own contract remains authoritative; it does not implement the entire paper.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Encode anchor targets

<!-- source-flow: 2015-faster-r-cnn#stage-1 -->

Represent target boxes as offsets relative to an anchor’s center and size.

[Study the mechanism and math](/projects/2015-faster-r-cnn#paper-section-encode-anchor-targets).

- **Proposed component, not runnable:** Generate dense anchors.
- **Proposed component, not runnable:** Encode and decode proposal regression targets.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Select region proposals

<!-- source-flow: 2015-faster-r-cnn#stage-2 -->

Use foreground scores, box decoding, clipping, and duplicate removal.

[Study the mechanism and math](/projects/2015-faster-r-cnn#paper-section-select-region-proposals).

- **Runnable supporting prerequisite:** [Compute Pairwise Bounding-Box IoU](/problems/box-iou-broadcast). Build a pairwise overlap matrix for two sets of image-space boxes.
- **Runnable supporting prerequisite:** [Run Class-Aware Non-Maximum Suppression](/problems/class-aware-nms). Suppress redundant same-class boxes with deterministic greedy ordering.
- **Proposed component, not runnable:** Filter proposals and test region-feature alignment.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Classify and refine regions

<!-- source-flow: 2015-faster-r-cnn#stage-3 -->

Convert variable regions into fixed-size features for a second prediction head.

[Study the mechanism and math](/projects/2015-faster-r-cnn#paper-section-classify-and-refine-regions).

- **Proposed component, not runnable:** Pool Proposal Regions and Apply Class-Specific Box Deltas.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Encode anchor targets | anchor predictions | Select region proposals |
| Select region proposals | regions of interest | Classify and refine regions |

## Integration exercise

**Proposed exercise — not runnable yet.** Construct a tiny analytic scene or point set with known positions, synthetic features and declared visibility; provide original images only where the mechanism needs them. Compose the selected mechanisms in the declared flow, beginning with **Encode anchor targets** and ending with **Classify and refine regions**. Save each intermediate artifact so a learner can locate a mismatch at its originating stage.

The integration boundary is selected representation, geometry or rendering operations; large learned backbones can be represented by explicitly supplied synthetic features. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2015-faster-r-cnn). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** For the **Encode anchor targets → Classify and refine regions** fixture, compare reconstruction, matching or aggregation outputs with hand-computable scene quantities and an independent implementation on tiny arrays.

Use one clean baseline and a separately recorded fault case: remove observations, change point order, or insert an occluded surface; record the geometric or representation error by condition. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record scene scale, camera convention, point ordering policy, visibility masks, interpolation rule and feature-generation seed. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
