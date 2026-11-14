---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2016-yolo-v1",
  "paper_id": "2016-yolo-v1",
  "title": "You Only Look Once: Unified, Real-Time Object Detection",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/1506.02640",
  "source_cards": [
    "research/papers/vision-vlm-3d/2016-yolo-v1.md"
  ],
  "paper_aliases": [],
  "category": "vision-vlm-3d",
  "topics": [
    "object detection",
    "single-stage detection",
    "bounding boxes",
    "real-time inference"
  ],
  "runnable_problem_slugs": [
    "yolo-responsible-cell-targets",
    "yolo-coordinate-objectness-class-loss",
    "decode-yolo-grid",
    "box-iou-broadcast",
    "class-aware-nms",
    "detection-precision-recall-map",
    "detector-accuracy-latency-frontier"
  ],
  "proposed_component_count": 0,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2016-yolo-v1",
      "node": "stage-1"
    },
    {
      "card": "2016-yolo-v1",
      "node": "stage-2"
    },
    {
      "card": "2016-yolo-v1",
      "node": "stage-3"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# You Only Look Once: Unified, Real-Time Object Detection — implementation track

## Orientation and scope

YOLO v1 predicts an image’s object boxes and categories in one network evaluation. A spatial grid divides responsibility: the cell containing an object’s center predicts that object, while multiple box predictors within a cell compete to fit its shape. This design connects localization and classification directly, but its grid assignment limits crowded scenes and small nearby objects. Joint Tonic implements cell assignment, loss components, decoding, overlap, class-aware suppression and evaluation as separate components; its decoder contract is a teaching interface rather than a claim that every later YOLO version uses the same parameterization.

The implementation path follows **Predict the grid → Decode image boxes → Score and suppress**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/1506.02640) · [Paper explanation and graph](/projects/2016-yolo-v1) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2016-yolo-v1](../../../research/papers/vision-vlm-3d/2016-yolo-v1.md).

**Available now:** 7 paper-associated runnable components; 0 supporting runnable components. **Proposed:** 0 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Predict the grid** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

- **Supporting prerequisite:** [Decode YOLO Grid Predictions](/problems/decode-yolo-grid). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Assign Ground-Truth Objects to Responsible Cells](/problems/yolo-responsible-cell-targets). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Project Camera Points into Pixels](/problems/project-camera-points). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Compute Pairwise Bounding-Box IoU](/problems/box-iou-broadcast). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Run Class-Aware Non-Maximum Suppression](/problems/class-aware-nms). Its own contract remains authoritative; it does not implement the entire paper.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Predict the grid

<!-- source-flow: 2016-yolo-v1#stage-1 -->

Each cell predicts box coordinates, confidence, and class probabilities.

[Study the mechanism and math](/projects/2016-yolo-v1#paper-section-predict-the-grid).

- **Runnable paper-associated component:** [Assign Ground-Truth Objects to Responsible Cells](/problems/yolo-responsible-cell-targets). Build one ground-truth target per YOLO-v1 grid cell with an explicit crowded-cell policy.
- **Runnable paper-associated component:** [Compute YOLO Coordinate, Objectness, and Class Losses](/problems/yolo-coordinate-objectness-class-loss). Compute the squared-error components of a bounded YOLO-v1 training objective from supplied responsibilities.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Decode image boxes

<!-- source-flow: 2016-yolo-v1#stage-2 -->

Convert cell-relative centers and predicted sizes into pixel corners.

[Study the mechanism and math](/projects/2016-yolo-v1#paper-section-decode-image-boxes).

- **Runnable paper-associated component:** [Decode YOLO Grid Predictions](/problems/decode-yolo-grid). Decode grid-relative boxes and class scores into a stable detector output.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Score and suppress

<!-- source-flow: 2016-yolo-v1#stage-3 -->

Combine class confidence with overlap-based duplicate removal.

[Study the mechanism and math](/projects/2016-yolo-v1#paper-section-score-and-suppress).

- **Runnable paper-associated component:** [Compute Pairwise Bounding-Box IoU](/problems/box-iou-broadcast). Build a pairwise overlap matrix for two sets of image-space boxes.
- **Runnable paper-associated component:** [Run Class-Aware Non-Maximum Suppression](/problems/class-aware-nms). Suppress redundant same-class boxes with deterministic greedy ordering.
- **Runnable paper-associated component:** [Evaluate Detection with IoU, Precision-Recall, and mAP](/problems/detection-precision-recall-map). Evaluate class-aware image-local detection precision/recall and interpolated AP at ONE IoU threshold.
- **Runnable paper-associated component:** [Benchmark Detector Accuracy Against Edge Latency](/problems/detector-accuracy-latency-frontier). Find accuracy/latency Pareto candidates and choose a feasible detector from supplied measurements.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Predict the grid | grid predictions | Decode image boxes |
| Decode image boxes | pixel boxes | Score and suppress |

## Integration exercise

**Proposed exercise — not runnable yet.** Construct small synthetic images, boxes, embeddings or rays chosen to match the first mechanism; retain ground-truth geometry and any correspondence labels. Compose the selected mechanisms in the declared flow, beginning with **Predict the grid** and ending with **Score and suppress**. Save each intermediate artifact so a learner can locate a mismatch at its originating stage.

The integration boundary is a small perception component pipeline with supplied model outputs or tiny original weights; pretrained feature quality and paper-scale training are outside this exercise. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2016-yolo-v1). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** For the **Predict the grid → Score and suppress** fixture, compare tensor outputs with an independent scalar or exhaustive oracle and report the relevant matching, reconstruction or retrieval metric on the declared synthetic labels.

Use one clean baseline and a separately recorded fault case: permute an input ordering, corrupt one coordinate convention, or remove a valid observation; check the method-specific invariance or rejection rule. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **You Only Look Once: Unified, Real-Time Object Detection** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record image/ray/box conventions, normalization, feature widths, class mapping, numeric tolerances and fixture seed. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
