---
schema_version: 1
problem_id: "vit-patchify-reconstruct"
content_version: "0.1.0"
status: "reviewed"
title: "Patchify and Reconstruct an Image Tensor"
summary: "Convert channels-first images into ordered patch vectors and reconstruct every input pixel."
type: "function"
difficulty: "easy"
estimated_minutes: 30
domains: ["perception"]
topics: ["vision-transformer", "image-layout", "patch-tokens"]
paper_ids: ["2021-vision-transformer"]
paper_sections: ["Section 3.1: Vision Transformer, image patches before linear projection"]
track_ids: []
prerequisite_problem_ids: []
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
entrypoint: "solution.patchify"
physical_contract:
  frames: ["image pixel lattice"]
  units: {"values": "unchanged input intensity units", "patch_size": "pixels"}
  axes: "B,C,H,W input; H increases down, W right; patches row-major; elements channel then local row then local column."
  timestamp_assumptions: "No timestamp input; any temporal or scene alignment is an upstream caller responsibility."
  batching: "0<=B<=1024 independent images; 1<=C,H,W,P<=4096 with divisibility. No temporal dimension, resize, crop, or padding."
grading:
  mode: "exact"
  seed: 20261113
  rtol: 0.0
  atol: 0.0
  public_case_families: ["rectangular two-patch image", "multichannel patch order", "P=1 identity layout"]
  hidden_case_families: ["zero batch and rectangular grids", "noncontiguous arrays", "bad divisibility and mismatched image shape", "input and output memory independence"]
  performance_class: "none"
fixtures:
  source: "original synthetic examples in examples.md; future generated fixtures use declared seed"
  license: "CC0-1.0"
  version_or_hash: "synthetic-examples-v0.1.0"
provenance:
  authoring_notes: "Original bounded teaching contract and explanations; source mechanisms checked against the paired paper card and primary sources; no paper figures or implementation code copied."
  primary_urls: ["https://arxiv.org/abs/2010.11929"]
  implementation_urls: []
owners: ["ui_issue_scout"]
reviewers: ["paper_explanations"]
---

# Patchify and Reconstruct an Image Tensor

## Learning objective

Convert channels-first images into ordered patch vectors and reconstruct every input pixel.

## Paper connection and scope

Source: [2021-vision-transformer](https://arxiv.org/abs/2010.11929), Section 3.1: Vision Transformer, image patches before linear projection. Read the [paired paper card](../../../../research/papers/vision-vlm-3d/2021-vision-transformer.md) and [vision manifest](../../../../research/manifests/vision-vlm-3d.md). The exercise isolates the mechanism described in [theory.md](theory.md); it does not reproduce a trained model or the paper's benchmark results. The original diagrams and synthetic inputs have no dependency on redistributing the research PDF.

## Contract and learner prompt

[statement.md](statement.md) is the complete typed learner contract, including inputs, outputs, errors, frames/units, batching, and aliasing. [examples.md](examples.md) contains two explicit input/output examples. No additional behavior is implied by a library's defaults.

## Starter-code plan

The future `starter.py` supplies the imports and signature(s) in the statement with an empty body. The future `reference.py` and evaluator are not implemented by this draft. Both solution.patchify and solution.unpatchify are required; entrypoint above identifies the first function. No `meta.json` is published and no runnable catalog entry is created.

## Reference-solution plan

Reshape spatial axes, transpose into grid-before-patch order, and reshape to token vectors; invert with the supplied image shape. O(BCHW) time/output storage. No arithmetic modifies pixel values; compare exactly, including noncontiguous inputs.

## Evaluator plan

| Case family | Visibility | Contract evidence |
|---|---|---|
| Worked values: rectangular two-patch image | Public | Match documented outputs and shapes. |
| Boundary: P=1 identity layout | Public | Make the declared boundary behavior visible. |
| Generalization: zero batch and rectangular grids | Hidden | Exercise the same stated rule on unseen inputs. |
| Full invalid-input contract | Public examples and hidden coverage | Check exception class; never depend on undocumented error precedence. |
| Mutation/aliasing and supported dtype/layout | Hidden | Verify the output contract beyond forward numbers. |

Seed `20261113` fixes generated cases. Value comparisons are exact because operations select or reorder existing numbers. There is no speed leaderboard. The resource limits above are proposed evaluation limits, not benchmarked promises. Image build, clean-sandbox reference execution, public/hidden suites, and resource calibration are pending. Worker/infrastructure failures must remain distinct from learner failures; record content version and evaluator identity with scores only after implementation.

## Visualization and accessibility

The original Mermaid shape/mechanism diagram is already authored in [theory.md](theory.md), alongside a plain-text equivalent and worked values. It is static and does not animate. No stock or paper image is required. Production rendering and keyboard/screen-reader behavior remain an implementation review item; no current app Mermaid support is assumed.

## Theory and hints

[theory.md](theory.md) leads with intuition, defines the mathematics and physical assumptions, traces a numerical example, and explains a robot failure mode. [hints.md](hints.md) provides three progressive hints without a complete solution.

## MLOps and reproducibility extension

Store patch size, channel layout, intensity preprocessing, and a synthetic token-order golden fixture with the checkpoint package.

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
