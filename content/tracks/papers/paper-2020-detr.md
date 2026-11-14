---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2020-detr",
  "paper_id": "2020-detr",
  "title": "End-to-End Object Detection with Transformers",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/2005.12872",
  "source_cards": [
    "research/papers/vision-vlm-3d/2020-detr.md"
  ],
  "paper_aliases": [],
  "category": "vision-vlm-3d",
  "topics": [
    "object detection",
    "transformers",
    "set prediction",
    "bipartite matching"
  ],
  "runnable_problem_slugs": [
    "detr-matching-cost",
    "detr-no-object-targets",
    "detr-hungarian-assignment"
  ],
  "proposed_component_count": 4,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2020-detr",
      "node": "stage-1"
    },
    {
      "card": "2020-detr",
      "node": "stage-2"
    },
    {
      "card": "2020-detr",
      "node": "stage-3"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# End-to-End Object Detection with Transformers — implementation track

## Orientation and scope

DETR treats detection as predicting a set of objects rather than assigning a label to every anchor. A transformer decoder receives learned object queries and emits a fixed-size set of class and box predictions. During training, bipartite matching assigns each ground-truth object to one prediction; unmatched predictions learn the no-object label. This removes the need for hand-designed anchor matching and duplicate-suppression rules in the original detection pipeline.

The implementation path follows **Encode spatial features → Decode object queries → Match and train the set**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/2005.12872) · [Paper explanation and graph](/projects/2020-detr) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2020-detr](../../../research/papers/vision-vlm-3d/2020-detr.md).

**Available now:** 3 paper-associated runnable components; 0 supporting runnable components. **Proposed:** 4 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Encode spatial features** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

- **Supporting prerequisite:** [Compute Pairwise Bounding-Box IoU](/problems/box-iou-broadcast). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Build a Detection Bipartite-Matching Cost Matrix](/problems/detr-matching-cost). Its own contract remains authoritative; it does not implement the entire paper.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Encode spatial features

<!-- source-flow: 2020-detr#stage-1 -->

Combine image features with positions so attention retains location.

[Study the mechanism and math](/projects/2020-detr#paper-section-encode-spatial-features).

- **Proposed component, not runnable:** Flatten Spatial Features with Position and Padding Metadata.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Decode object queries

<!-- source-flow: 2020-detr#stage-2 -->

A fixed query set predicts categories and normalized boxes.

[Study the mechanism and math](/projects/2020-detr#paper-section-decode-object-queries).

- **Proposed component, not runnable:** Decode Normalized Boxes and Classes from Object Queries.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Match and train the set

<!-- source-flow: 2020-detr#stage-3 -->

Assign each target once, then supervise matched boxes and unused queries.

[Study the mechanism and math](/projects/2020-detr#paper-section-match-and-train-the-set).

- **Runnable paper-associated component:** [Build a Detection Bipartite-Matching Cost Matrix](/problems/detr-matching-cost). Build pairwise query-to-target costs from class probabilities, normalized box distances, and generalized IoU.
- **Runnable paper-associated component:** [Handle the No-Object Class and Padding Masks](/problems/detr-no-object-targets). Handle the No-Object Class and Padding Masks
- **Runnable paper-associated component:** [Match Object Queries with the Hungarian Algorithm](/problems/detr-hungarian-assignment). Match Object Queries with the Hungarian Algorithm
- **Proposed component, not runnable:** Compute DETR Classification, L1, and GIoU Losses.
- **Proposed component, not runnable:** Diagnose Query Collapse and Missed Small Objects.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Encode spatial features | image tokens | Decode object queries |
| Decode object queries | prediction set | Match and train the set |

## Integration exercise

**Proposed exercise — not runnable yet.** Use a tiny query set and two synthetic image-frame boxes. Construct matching costs, solve the proposed injective assignment, then build no-object-aware class targets and matched box terms. The assignment component must accept any optimal result when costs tie.

The integration boundary is a small perception component pipeline with supplied model outputs or tiny original weights; pretrained feature quality and paper-scale training are outside this exercise. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2020-detr). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** Compare assignment cost with exhaustive enumeration, include an empty target set, and verify unmatched queries receive the declared no-object treatment. Keep target padding separate from image padding.

Use one clean baseline and a separately recorded fault case: permute an input ordering, corrupt one coordinate convention, or remove a valid observation; check the method-specific invariance or rejection rule. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **End-to-End Object Detection with Transformers** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record image/ray/box conventions, normalization, feature widths, class mapping, numeric tolerances and fixture seed. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
