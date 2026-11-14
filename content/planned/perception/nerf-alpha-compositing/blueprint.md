---
schema_version: 1
problem_id: "nerf-alpha-compositing"
content_version: "0.1.0"
status: "reviewed"
title: "Compute Transmittance and Alpha Compositing Weights"
summary: "Turn ordered ray densities and metric interval lengths into sample visibility weights and remaining background mass."
type: "function"
difficulty: "medium"
estimated_minutes: 35
domains: ["perception"]
topics: ["neural-rendering", "volume-rendering", "visibility"]
paper_ids: ["2020-nerf"]
paper_sections: ["Section 4: volume rendering with radiance fields, discrete rendering equation"]
track_ids: []
prerequisite_problem_ids: ["project-camera-points"]
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
entrypoint: "solution.alpha_compositing_weights"
physical_contract:
  frames: ["one scene frame per ray; unit ray direction assumed upstream"]
  units: {"density": "inverse metres", "deltas": "metres", "weights": "dimensionless", "background": "dimensionless"}
  axes: "R independent rays, S intervals ordered near-to-far; no spatial coordinate axis in the supplied arrays."
  timestamp_assumptions: "No timestamp input; any temporal or scene alignment is an upstream caller responsibility."
  batching: "R,S positive; equal (R,S) arrays; last interval explicitly supplied; no padding or implicit infinite tail."
grading:
  mode: "numerical"
  seed: 20261113
  rtol: 1.0e-6
  atol: 1.0e-7
  public_case_families: ["two half-opaque intervals", "different interval lengths", "zero length and zero density"]
  hidden_case_families: ["near-opaque front interval", "tiny thickness stability", "ray-independent batching", "empty and invalid inputs", "noncontiguous arrays and mass conservation"]
  performance_class: "none"
fixtures:
  source: "original synthetic examples in examples.md; future generated fixtures use declared seed"
  license: "CC0-1.0"
  version_or_hash: "synthetic-examples-v0.1.0"
provenance:
  authoring_notes: "Original bounded teaching contract and explanations; source mechanisms checked against the paired paper card and primary sources; no paper figures or implementation code copied."
  primary_urls: ["https://arxiv.org/abs/2003.08934"]
  implementation_urls: []
owners: ["ui_issue_scout"]
reviewers: ["paper_explanations"]
---

# Compute Transmittance and Alpha Compositing Weights

## Learning objective

Turn ordered ray densities and metric interval lengths into sample visibility weights and remaining background mass.

## Paper connection and scope

Source: [2020-nerf](https://arxiv.org/abs/2003.08934), Section 4: volume rendering with radiance fields, discrete rendering equation. Read the [paired paper card](../../../../research/papers/vision-vlm-3d/2020-nerf.md) and [vision manifest](../../../../research/manifests/vision-vlm-3d.md). The exercise isolates the mechanism described in [theory.md](theory.md); it does not reproduce a trained model or the paper's benchmark results. The original diagrams and synthetic inputs have no dependency on redistributing the research PDF.

## Contract and learner prompt

[statement.md](statement.md) is the complete typed learner contract, including inputs, outputs, errors, frames/units, batching, and aliasing. [examples.md](examples.md) contains two explicit input/output examples. No additional behavior is implied by a library's defaults.

## Starter-code plan

The future `starter.py` supplies the imports and signature(s) in the statement with an empty body. The future `reference.py` and evaluator are not implemented by this draft. The single entry point is declared above. No `meta.json` is published and no runnable catalog entry is created.

## Reference-solution plan

Compute optical thickness, stable -expm1(-q), exclusive cumulative thickness, exponentials, and pointwise weights. O(RS) time/storage. No epsilon added to probabilities; underflow is allowed, while all supplied bounds keep cumulative sums finite.

## Evaluator plan

| Case family | Visibility | Contract evidence |
|---|---|---|
| Worked values: two half-opaque intervals | Public | Match documented outputs and shapes. |
| Boundary: zero length and zero density | Public | Make the declared boundary behavior visible. |
| Generalization: near-opaque front interval | Hidden | Exercise the same stated rule on unseen inputs. |
| Full invalid-input contract | Public examples and hidden coverage | Check exception class; never depend on undocumented error precedence. |
| Mutation/aliasing and supported dtype/layout | Hidden | Verify the output contract beyond forward numbers. |

Seed `20261113` fixes generated cases. Compare numerical values with rtol=1e-6 and atol=1e-7; shapes, dtypes, keys, and exception classes are exact. There is no speed leaderboard. The resource limits above are proposed evaluation limits, not benchmarked promises. Image build, clean-sandbox reference execution, public/hidden suites, and resource calibration are pending. Worker/infrastructure failures must remain distinct from learner failures; record content version and evaluator identity with scores only after implementation.

## Visualization and accessibility

The original Mermaid shape/mechanism diagram is already authored in [theory.md](theory.md), alongside a plain-text equivalent and worked values. It is static and does not animate. No stock or paper image is required. Production rendering and keyboard/screen-reader behavior remain an implementation review item; no current app Mermaid support is assumed.

## Theory and hints

[theory.md](theory.md) leads with intuition, defines the mathematics and physical assumptions, traces a numerical example, and explains a robot failure mode. [hints.md](hints.md) provides three progressive hints without a complete solution.

## MLOps and reproducibility extension

Save scene-length normalization, camera-pose version, near/far conventions, and background policy with a radiance-field artifact so rendering runs remain comparable.

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
