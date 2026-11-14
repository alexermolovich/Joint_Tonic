---
schema_version: 1
problem_id: "pointnet-symmetric-pooling"
content_version: "0.1.0"
status: "reviewed"
title: "Prove Permutation Invariance with Symmetric Pooling"
summary: "Pool valid point features channel by channel and demonstrate that point order cannot change the result."
type: "function"
difficulty: "easy"
estimated_minutes: 30
domains: ["perception"]
topics: ["point-clouds", "permutation-invariance", "masked-pooling"]
paper_ids: ["2017-pointnet"]
paper_sections: ["Section 4.2: symmetry function for unordered input"]
track_ids: []
prerequisite_problem_ids: ["se3-transform-points"]
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
entrypoint: "solution.symmetric_point_pool"
physical_contract:
  frames: ["features derived from one consistently calibrated point-cloud frame"]
  units: {"features": "dimensionless learned features"}
  axes: "B cloud batch, N unordered point slots, D feature channels; reduce only N."
  timestamp_assumptions: "No timestamp input; any temporal or scene alignment is an upstream caller responsibility."
  batching: "B,N,D positive. A boolean B-by-N mask marks valid point slots; every cloud has at least one valid point."
grading:
  mode: "exact"
  seed: 20261113
  rtol: 0.0
  atol: 0.0
  public_case_families: ["permutation with channel maxima at different points", "negative valid features with high padding", "one valid point"]
  hidden_case_families: ["different masks per cloud", "duplicate features and tied maxima", "all-invalid cloud and empty dimensions rejected", "permutations applied jointly to mask and features", "noncontiguous inputs and independent output"]
  performance_class: "none"
fixtures:
  source: "original synthetic examples in examples.md; future generated fixtures use declared seed"
  license: "CC0-1.0"
  version_or_hash: "synthetic-examples-v0.1.0"
provenance:
  authoring_notes: "Original bounded teaching contract and explanations; source mechanisms checked against the paired paper card and primary sources; no paper figures or implementation code copied."
  primary_urls: ["https://arxiv.org/abs/1612.00593"]
  implementation_urls: []
owners: ["ui_issue_scout"]
reviewers: ["paper_explanations"]
---

# Prove Permutation Invariance with Symmetric Pooling

## Learning objective

Pool valid point features channel by channel and demonstrate that point order cannot change the result.

## Paper connection and scope

Source: [2017-pointnet](https://arxiv.org/abs/1612.00593), Section 4.2: symmetry function for unordered input. Read the [paired paper card](../../../../research/papers/vision-vlm-3d/2017-pointnet.md) and [vision manifest](../../../../research/manifests/vision-vlm-3d.md). The exercise isolates the mechanism described in [theory.md](theory.md); it does not reproduce a trained model or the paper's benchmark results. The original diagrams and synthetic inputs have no dependency on redistributing the research PDF.

## Contract and learner prompt

[statement.md](statement.md) is the complete typed learner contract, including inputs, outputs, errors, frames/units, batching, and aliasing. [examples.md](examples.md) contains two explicit input/output examples. No additional behavior is implied by a library's defaults.

## Starter-code plan

The future `starter.py` supplies the imports and signature(s) in the statement with an empty body. The future `reference.py` and evaluator are not implemented by this draft. The single entry point is declared above. No `meta.json` is published and no runnable catalog entry is created.

## Reference-solution plan

Validate dimensions and masks, broadcast the mask over D, then max-reduce over N. O(BND) time; O(BD) output with at most O(BND) temporary storage. Exact finite-value comparison suffices because max selects existing values.

## Evaluator plan

| Case family | Visibility | Contract evidence |
|---|---|---|
| Worked values: permutation with channel maxima at different points | Public | Match documented outputs and shapes. |
| Boundary: one valid point | Public | Make the declared boundary behavior visible. |
| Generalization: different masks per cloud | Hidden | Exercise the same stated rule on unseen inputs. |
| Full invalid-input contract | Public examples and hidden coverage | Check exception class; never depend on undocumented error precedence. |
| Mutation/aliasing and supported dtype/layout | Hidden | Verify the output contract beyond forward numbers. |

Seed `20261113` fixes generated cases. Value comparisons are exact because operations select or reorder existing numbers. There is no speed leaderboard. The resource limits above are proposed evaluation limits, not benchmarked promises. Image build, clean-sandbox reference execution, public/hidden suites, and resource calibration are pending. Worker/infrastructure failures must remain distinct from learner failures; record content version and evaluator identity with scores only after implementation.

## Visualization and accessibility

The original Mermaid shape/mechanism diagram is already authored in [theory.md](theory.md), alongside a plain-text equivalent and worked values. It is static and does not animate. No stock or paper image is required. Production rendering and keyboard/screen-reader behavior remain an implementation review item; no current app Mermaid support is assumed.

## Theory and hints

[theory.md](theory.md) leads with intuition, defines the mathematics and physical assumptions, traces a numerical example, and explains a robot failure mode. [hints.md](hints.md) provides three progressive hints without a complete solution.

## MLOps and reproducibility extension

Monitor valid-point counts alongside the descriptor; max pooling cannot tell a dense cloud from a sparse cloud with the same extreme features.

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
