---
schema_version: 1
problem_id: "detr-matching-cost"
content_version: "0.1.0"
status: "reviewed"
title: "Build a Detection Bipartite-Matching Cost Matrix"
summary: "Build pairwise query-to-target costs from class probabilities, normalized box distances, and generalized IoU."
type: "function"
difficulty: "medium"
estimated_minutes: 50
domains: ["perception"]
topics: ["object-detection", "set-prediction", "generalized-iou"]
paper_ids: ["2020-detr"]
paper_sections: ["Section 3.1: object detection set prediction loss; Appendix A.2: box loss"]
track_ids: []
prerequisite_problem_ids: ["box-iou-broadcast"]
runtime:
  language: "python"
  python: "3.12.3"
  image_digest: null
  image_status: "pending-build-and-independent-evaluator-review"
  platform: "linux-x86_64-cpu"
  dependencies:
    numpy: "2.2.4"
  limits:
    wall_seconds: 3
    cpu_seconds: 2
    memory_mb: 512
    output_kb: 64
entrypoint: "solution.detr_matching_cost"
physical_contract:
  frames: ["normalized image plane"]
  units: {"boxes": "dimensionless image fractions", "probabilities": "dimensionless", "cost": "dimensionless"}
  axes: "x increases right; y increases down; boxes are (cx,cy,width,height)."
  timestamp_assumptions: "No timestamp input; any temporal or scene alignment is an upstream caller responsibility."
  batching: "One image per call. Q queries, M real targets; no padding or batch axis."
grading:
  mode: "numerical"
  seed: 20261113
  rtol: 1.0e-6
  atol: 1.0e-7
  public_case_families: ["identical and touching boxes", "disjoint boxes with negative GIoU", "empty target set"]
  hidden_case_families: ["background label rejected", "repeated classes and unequal Q/M", "individual cost weights disabled", "noncontiguous inputs and invalid dtype/range", "corner extension without clipping"]
  performance_class: "none"
fixtures:
  source: "original synthetic examples in examples.md; future generated fixtures use declared seed"
  license: "CC0-1.0"
  version_or_hash: "synthetic-examples-v0.1.0"
provenance:
  authoring_notes: "Original bounded teaching contract and explanations; source mechanisms checked against the paired paper card and primary sources; no paper figures or implementation code copied."
  primary_urls: ["https://arxiv.org/abs/2005.12872"]
  implementation_urls: ["https://github.com/facebookresearch/detr/blob/main/models/matcher.py"]
owners: ["ui_issue_scout"]
reviewers: ["paper_explanations"]
---

# Build a Detection Bipartite-Matching Cost Matrix

## Learning objective

Build pairwise query-to-target costs from class probabilities, normalized box distances, and generalized IoU.

## Paper connection and scope

Source: [2020-detr](https://arxiv.org/abs/2005.12872), Section 3.1: object detection set prediction loss; Appendix A.2: box loss. Read the [paired paper card](../../../../research/papers/vision-vlm-3d/2020-detr.md) and [vision manifest](../../../../research/manifests/vision-vlm-3d.md). The exercise isolates the mechanism described in [theory.md](theory.md); it does not reproduce a trained model or the paper's benchmark results. The original diagrams and synthetic inputs have no dependency on redistributing the research PDF.

## Contract and learner prompt

[statement.md](statement.md) is the complete typed learner contract, including inputs, outputs, errors, frames/units, batching, and aliasing. [examples.md](examples.md) contains two explicit input/output examples. No additional behavior is implied by a library's defaults.

## Starter-code plan

The future `starter.py` supplies the imports and signature(s) in the statement with an empty body. The future `reference.py` and evaluator are not implemented by this draft. The single entry point is declared above. No `meta.json` is published and no runnable catalog entry is created.

## Reference-solution plan

Vectorized target-column gathering, broadcast L1, corner conversion, intersection/union/enclosure, and weighted addition. Time O(QK + QM) including input validation; auxiliary O(QM), output O(QM). The declared 1e-6 minimum box size avoids collapsed float64 corners and zero union; no epsilon changes the specified GIoU.

## Evaluator plan

| Case family | Visibility | Contract evidence |
|---|---|---|
| Worked values: identical and touching boxes | Public | Match documented outputs and shapes. |
| Boundary: empty target set | Public | Make the declared boundary behavior visible. |
| Generalization: background label rejected | Hidden | Exercise the same stated rule on unseen inputs. |
| Full invalid-input contract | Public examples and hidden coverage | Check exception class; never depend on undocumented error precedence. |
| Mutation/aliasing and supported dtype/layout | Hidden | Verify the output contract beyond forward numbers. |

Seed `20261113` fixes generated cases. Compare numerical values with rtol=1e-6 and atol=1e-7; shapes, dtypes, keys, and exception classes are exact. There is no speed leaderboard. The resource limits above are proposed evaluation limits, not benchmarked promises. Image build, clean-sandbox reference execution, public/hidden suites, and resource calibration are pending. Worker/infrastructure failures must remain distinct from learner failures; record content version and evaluator identity with scores only after implementation.

## Visualization and accessibility

The original Mermaid shape/mechanism diagram is already authored in [theory.md](theory.md), alongside a plain-text equivalent and worked values. It is static and does not animate. No stock or paper image is required. Production rendering and keyboard/screen-reader behavior remain an implementation review item; no current app Mermaid support is assumed.

## Theory and hints

[theory.md](theory.md) leads with intuition, defines the mathematics and physical assumptions, traces a numerical example, and explains a robot failure mode. [hints.md](hints.md) provides three progressive hints without a complete solution.

## MLOps and reproducibility extension

Log separate class/L1/GIoU distributions with dataset and annotation-transform versions. A cost-scale change can alter assignments even when the model architecture is unchanged.

## Editorial checklist

- [x] Named curriculum candidate and paired source paper resolve.
- [x] Original contract, theory, diagrams, and synthetic examples authored.
- [x] Shapes, dtype/device, units, frames, time, batching, errors, and aliasing stated.
- [x] Exact proposed Python/dependency versions recorded; image digest honestly pending.
- [x] Text alternative accompanies each static diagram.
- [x] Numerical author checks and shared structural validator recorded in review.md.
- [ ] Independent source, pedagogy, and evaluator reviewer approved.
- [ ] Starter/reference/public/hidden implementation built and validated in the pinned sandbox.

See [review.md](review.md) for status. Draft status must not be promoted based on authored prose alone.
