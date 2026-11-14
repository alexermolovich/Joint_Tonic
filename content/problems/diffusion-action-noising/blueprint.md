---
schema_version: 1
problem_id: "diffusion-action-noising"
content_version: "1.0.0"
status: "implemented"
title: "Add Noise to an Action Sequence"
summary: "Gather one cumulative signal coefficient per batch item and broadcast over horizon/action axes; mix clean actions and supplied noise with square-root weights."
type: "component"
difficulty: "medium"
estimated_minutes: 45
domains: ["Robot learning"]
topics: ["diffusion","action-sequences","masking"]
paper_ids: ["2023-diffusion-policy"]
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
entrypoint: "solution.diffuse_actions"
physical_contract:
  frames: ["Declared by caller; no implicit frame conversion"]
  units: {actions: "per-dimension caller units", timestamps: "seconds", latency: "milliseconds"}
  axes: "not-applicable"
  timestamp_assumptions: "Ordered timestamps only for episode-validation; otherwise not-applicable"
  batching: "B,H,D with B,H mask"
grading:
  mode: "numerical"
  seed: 20261113
  rtol: 1.0e-6
  atol: 1.0e-7
  public_case_families: ["Worked nominal examples", "One visible edge case"]
  hidden_case_families: ["schedule endpoints","manual mixture","masked padding","per-batch steps","gradients","dtype","invalid schedule/mask/index"]
  performance_class: "local-cpu"
fixtures:
  source: "Original synthetic fixtures in cases.py"
  license: "CC0-1.0"
  version_or_hash: "synthetic-v1"
provenance:
  authoring_notes: "Original teaching exercise; reduced component, not a full paper reproduction."
  primary_urls: ["https://arxiv.org/abs/2303.04137"]
  implementation_urls: []
owners: ["Joint Tonic content"]
reviewers: []
---

# Add Noise to an Action Sequence

## Learning objective

Gather one cumulative signal coefficient per batch item and broadcast over horizon/action axes; mix clean actions and supplied noise with square-root weights.

## Paper connection and scope

Paper IDs: 2023-diffusion-policy. This exercise isolates the numerical or operational mechanism described in the paired paper cards. It omits model training, real robot execution and paper-scale evaluation.

## Contract

actions and supplied noise are finite floating tensors of identical (B,H,D) shape, positive dimensions, dtype and device. alpha_bar is a finite nonincreasing 1-D tensor in [0,1] on the same dtype/device. timesteps is int64 (B,) on that device with valid schedule indices. mask is None or bool (B,H) on that device; False padding yields zero in both outputs. Return (noised,target_noise), same shape/dtype/device; preserve autograd and inputs. TypeError covers non-tensors; ValueError covers tensor contract violations. Do not draw randomness.

### Errors and edge cases

The learner-facing problem.md is the full normative argument, output and error specification. Cases cover schedule endpoints, manual mixture, masked padding, per-batch steps, gradients, dtype, invalid schedule/mask/index. Every output is reproducible from supplied inputs; no network or external data is required.

## Learner prompt draft

Implement `diffuse_actions` as described in problem.md. Explain the reasoning in theory.md before presenting the independent reference solution.

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

The `diffusion` adapter receives bounded numerical examples, never arbitrary HTML. The lesson outline in theory.md describes the visualization. A linked numerical table is the screen-reader and reduced-motion fallback.

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

