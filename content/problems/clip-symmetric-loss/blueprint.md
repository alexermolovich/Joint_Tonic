---
schema_version: 1
problem_id: "clip-symmetric-loss"
content_version: "1.0.0"
status: "implemented"
title: "Compute Symmetric CLIP Contrastive Loss"
summary: "Normalize rows, form image/text dot-product logits divided by temperature, and average cross-entropy in both directions."
type: "component"
difficulty: "medium"
estimated_minutes: 40
domains: ["VLM"]
topics: ["contrastive-learning","embeddings","temperature"]
paper_ids: ["2021-clip"]
paper_sections: ["Primary-paper mechanism; teaching scope verified against paired paper card"]
track_ids: []
prerequisite_problem_ids: []
runtime:
  language: "python"
  python: "3.10"
  image_digest: null
  publication_note: "Local evaluator fixture; pin OCI digest before publishing."
  dependencies:
    numpy: "2.2.4"
    torch: "2.6.0+cpu"
  limits: {wall_seconds: 10, cpu_seconds: 8, memory_mb: 2048, output_kb: 64}
entrypoint: "solution.clip_loss"
physical_contract:
  frames: ["Declared by caller; no implicit frame conversion"]
  units: {actions: "per-dimension caller units", timestamps: "seconds", latency: "milliseconds"}
  axes: "not-applicable"
  timestamp_assumptions: "Ordered timestamps only for episode-validation; otherwise not-applicable"
  batching: "B,D paired rows"
grading:
  mode: "numerical"
  seed: 20261113
  rtol: 1.0e-6
  atol: 1.0e-7
  public_case_families: ["Worked nominal examples", "One visible edge case"]
  hidden_case_families: ["aligned pairs","swapped pairs","singleton","scale invariance","extreme logits","gradients","invalid inputs"]
  performance_class: "local-cpu"
fixtures:
  source: "Original synthetic fixtures in cases.py"
  license: "CC0-1.0"
  version_or_hash: "synthetic-v1"
provenance:
  authoring_notes: "Original teaching exercise; reduced component, not a full paper reproduction."
  primary_urls: ["https://arxiv.org/abs/2103.00020"]
  implementation_urls: []
owners: ["Joint Tonic content"]
reviewers: []
---

# Compute Symmetric CLIP Contrastive Loss

## Learning objective

Normalize rows, form image/text dot-product logits divided by temperature, and average cross-entropy in both directions.

## Paper connection and scope

Paper IDs: 2021-clip. This exercise isolates the numerical or operational mechanism described in the paired paper cards. It omits model training, real robot execution and paper-scale evaluation.

## Contract

Paired finite, nonzero floating tensors image_features and text_features have identical (B,D) shape, B,D >= 1, dtype and device. temperature is a finite real scalar > 0. Return a scalar tensor with the input dtype/device and autograd intact. Raise ValueError for invalid values, shape, dtype/device mismatch or zero-norm rows; raise TypeError for non-tensor features. Inputs are never modified.

### Errors and edge cases

The learner-facing problem.md is the full normative argument, output and error specification. Cases cover aligned pairs, swapped pairs, singleton, scale invariance, extreme logits, gradients, invalid inputs. Every output is reproducible from supplied inputs; no network or external data is required.

## Learner prompt draft

Implement `clip_loss` as described in problem.md. Explain the reasoning in theory.md before presenting the independent reference solution.

## Worked examples

At least two complete numerical/structured examples are supplied in problem.md. Public tests mirror their contracts without exposing hidden fixtures.

## Starter-code plan

`starter.py` imports the permitted library and declares the exact function signature; the function body raises NotImplementedError.

## Reference-solution plan

`reference.py` validates boundaries, implements the declared mechanism directly, and avoids changing caller inputs. The solution explanation records complexity and failure modes.

## Evaluator plan

| Case family | Public/hidden | Invariant | Tolerance | Purpose |
|---|---|---|---|---|
| Worked examples | Public | Contract outputs | rtol 1e-6 / atol 1e-7 | Establish the behavior |
| Edge/value/shape cases | Hidden | Documented boundary behavior | Exact metadata, numerical tolerance | Prevent silent contract errors |
| Autograd or immutability | Hidden | Preserve computation graph and/or inputs | Finite gradients / unchanged snapshots | Fit the component into a pipeline |

All fixtures are synthetic and deterministic. cases.py exports TESTS triples. Missing dependencies and evaluator crashes are platform errors, distinct from assertions about learner outputs.

## Visualization plan

The `clip` adapter receives bounded numerical examples, never arbitrary HTML. The lesson outline in theory.md describes the visualization. A linked numerical table is the screen-reader and reduced-motion fallback.

## Theory and hints

Start from intuition and units, then derive the operation in LaTeX, trace a small example, and show the robot failure mode. Hint one names the required invariant; hint two names the relevant library primitive without providing the entire solution.

## MLOps/reproducibility extension

Version preprocessing, numerical settings and all physical units with the evaluator. Include this component's errors and timing in a structured pipeline report; never interpret a single passing component as a robot safety claim.

## Editorial checklist

- [x] Metadata and existing paper IDs resolve.
- [x] Original prompt and theory are authored with worked examples.
- [x] Synthetic fixtures have a declared license.
- [x] Reference solution passes all public and hidden local checks (2026-11-13).
- [ ] Runtime image digest pinned for publication.
- [ ] Human subject-matter review approved.

