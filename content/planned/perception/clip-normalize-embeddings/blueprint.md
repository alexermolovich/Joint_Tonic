---
schema_version: 1
problem_id: "clip-normalize-embeddings"
content_version: "0.1.0"
status: "reviewed"
title: "Normalize Image and Text Embeddings"
summary: "Normalize paired image and text feature rows while preserving the PyTorch gradient path."
type: "function"
difficulty: "easy"
estimated_minutes: 25
domains: ["perception"]
topics: ["vision-language", "embeddings", "cosine-similarity"]
paper_ids: ["2021-clip"]
paper_sections: ["Section 2.3 and Figure 3: normalized image/text feature comparison"]
track_ids: []
prerequisite_problem_ids: []
runtime:
  language: "python"
  python: "3.12.3"
  image_digest: null
  image_status: "pending-build-and-independent-evaluator-review"
  platform: "linux-x86_64-cpu"
  dependencies:
    torch: "2.6.0"
  limits:
    wall_seconds: 3
    cpu_seconds: 2
    memory_mb: 512
    output_kb: 64
entrypoint: "solution.normalize_clip_embeddings"
physical_contract:
  frames: ["learned embedding coordinates, not a spatial frame"]
  units: {"features": "dimensionless"}
  axes: "B rows are paired samples in preserved order; D columns are embedding components."
  timestamp_assumptions: "No timestamp input; any temporal or scene alignment is an upstream caller responsibility."
  batching: "Both inputs share nonempty (B,D); no masks, padding, time axis, or independent retrieval collection."
grading:
  mode: "numerical"
  seed: 20261113
  rtol: 1.0e-6
  atol: 1.0e-7
  public_case_families: ["3-4-5 vectors with signs", "positive rescaling invariance", "one-row one-component case"]
  hidden_case_families: ["row versus column normalization", "zero and nonfinite norm rejection", "noncontiguous equal-shape input", "analytic first-component gradient and independent storage"]
  performance_class: "none"
fixtures:
  source: "original synthetic examples in examples.md; future generated fixtures use declared seed"
  license: "CC0-1.0"
  version_or_hash: "synthetic-examples-v0.1.0"
provenance:
  authoring_notes: "Original bounded teaching contract and explanations; source mechanisms checked against the paired paper card and primary sources; no paper figures or implementation code copied."
  primary_urls: ["https://arxiv.org/abs/2103.00020"]
  implementation_urls: []
owners: ["ui_issue_scout"]
reviewers: ["paper_explanations"]
---

# Normalize Image and Text Embeddings

## Learning objective

Normalize paired image and text feature rows while preserving the PyTorch gradient path.

## Paper connection and scope

Source: [2021-clip](https://arxiv.org/abs/2103.00020), Section 2.3 and Figure 3: normalized image/text feature comparison. Read the [paired paper card](../../../../research/papers/vision-vlm-3d/2021-clip.md) and [vision manifest](../../../../research/manifests/vision-vlm-3d.md). The exercise isolates the mechanism described in [theory.md](theory.md); it does not reproduce a trained model or the paper's benchmark results. The original diagrams and synthetic inputs have no dependency on redistributing the research PDF.

## Contract and learner prompt

[statement.md](statement.md) is the complete typed learner contract, including inputs, outputs, errors, frames/units, batching, and aliasing. [examples.md](examples.md) contains two explicit input/output examples. No additional behavior is implied by a library's defaults.

## Starter-code plan

The future `starter.py` supplies the imports and signature(s) in the statement with an empty body. The future `reference.py` and evaluator are not implemented by this draft. The single entry point is declared above. No `meta.json` is published and no runnable catalog entry is created.

## Reference-solution plan

Validate the bounded CPU contract, reduce squared components over D, and divide each row using a kept dimension; equivalent torch.linalg.vector_norm or torch.nn.functional.normalize is permitted within the declared range. O(BD) time/output storage. Use float64 only for range validation if needed; output computation keeps input dtype and gradient connection.

## Evaluator plan

| Case family | Visibility | Contract evidence |
|---|---|---|
| Worked values: 3-4-5 vectors with signs | Public | Match documented outputs and shapes. |
| Boundary: one-row one-component case | Public | Make the declared boundary behavior visible. |
| Generalization: row versus column normalization | Hidden | Exercise the same stated rule on unseen inputs. |
| Full invalid-input contract | Public examples and hidden coverage | Check exception class; never depend on undocumented error precedence. |
| Mutation/aliasing and supported dtype/layout | Hidden | Verify the output contract beyond forward numbers. |

Seed `20261113` fixes generated cases. Compare numerical values with rtol=1e-6 and atol=1e-7; shapes, dtypes, keys, and exception classes are exact. There is no speed leaderboard. The resource limits above are proposed evaluation limits, not benchmarked promises. Image build, clean-sandbox reference execution, public/hidden suites, and resource calibration are pending. Worker/infrastructure failures must remain distinct from learner failures; record content version and evaluator identity with scores only after implementation.

## Visualization and accessibility

The original Mermaid shape/mechanism diagram is already authored in [theory.md](theory.md), alongside a plain-text equivalent and worked values. It is static and does not animate. No stock or paper image is required. Production rendering and keyboard/screen-reader behavior remain an implementation review item; no current app Mermaid support is assumed.

## Theory and hints

[theory.md](theory.md) leads with intuition, defines the mathematics and physical assumptions, traces a numerical example, and explains a robot failure mode. [hints.md](hints.md) provides three progressive hints without a complete solution.

## MLOps and reproducibility extension

Record preprocessing and exported-encoder versions; monitor norm histograms before normalization to detect failed or drifting feature production.

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
