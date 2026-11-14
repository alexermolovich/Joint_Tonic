---
schema_version: 1
problem_id: "validate-robot-episodes"
content_version: "1.0.0"
status: "implemented"
title: "Validate a Multimodal Robot Episode Schema"
summary: "A signal's missing fraction is missing_rows / T. A timestamp must be finite numeric, and each valid adjacent pair must strictly increase."
type: "pipeline"
difficulty: "hard"
estimated_minutes: 70
domains: ["MLOps"]
topics: ["robot-data","schema-validation","sensor-timing"]
paper_ids: ["2019-data-validation-for-ml","2023-open-x-embodiment"]
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
  limits: {wall_seconds: 10, cpu_seconds: 8, memory_mb: 2048, output_kb: 64}
entrypoint: "solution.validate_episodes"
physical_contract:
  frames: ["Declared by caller; no implicit frame conversion"]
  units: {actions: "per-dimension caller units", timestamps: "seconds", latency: "milliseconds"}
  axes: "not-applicable"
  timestamp_assumptions: "Ordered timestamps only for episode-validation; otherwise not-applicable"
  batching: "Independent episodes or independent hardware groups"
grading:
  mode: "exact"
  seed: 20261113
  rtol: 1.0e-6
  atol: 1.0e-7
  public_case_families: ["Worked nominal examples", "One visible edge case"]
  hidden_case_families: ["valid data","missing signal","timestamps","range","optional/extra signals","shape/dtype/nonfinite","metadata","missing fraction","sorting"]
  performance_class: "local-cpu"
fixtures:
  source: "Original synthetic fixtures in cases.py"
  license: "CC0-1.0"
  version_or_hash: "synthetic-v1"
provenance:
  authoring_notes: "Original teaching exercise; reduced component, not a full paper reproduction."
  primary_urls: ["https://research.google/pubs/data-validation-for-machine-learning/","https://arxiv.org/abs/2310.08864"]
  implementation_urls: []
owners: ["Joint Tonic content"]
reviewers: []
---

# Validate a Multimodal Robot Episode Schema

## Learning objective

A signal's missing fraction is missing_rows / T. A timestamp must be finite numeric, and each valid adjacent pair must strictly increase.

## Paper connection and scope

Paper IDs: 2019-data-validation-for-ml, 2023-open-x-embodiment. This exercise isolates the numerical or operational mechanism described in the paired paper cards. It omits model training, real robot execution and paper-scale evaluation.

## Contract

episodes is a list. Each episode contains timestamps (list, seconds) and signals (dictionary). schema.signals maps names to shape (positive dimensions, [] means scalar), dtype ('float','int','bool'), required (default True), optional unit/frame/min/max, and max_missing_fraction (default 0). schema.allow_extra_signals defaults True. A signal contains values (length-T list, rows may be None), unit/frame metadata. Return issues as {episode: zero-based integer,path: JSON-like dotted/index path,code: stable string}, sorted by episode,path,code. Invalid schema/top-level arguments raise ValueError; malformed episode data produces issues. No mutation.

### Errors and edge cases

The learner-facing problem.md is the full normative argument, output and error specification. Cases cover valid data, missing signal, timestamps, range, optional/extra signals, shape/dtype/nonfinite, metadata, missing fraction, sorting. Every output is reproducible from supplied inputs; no network or external data is required.

## Learner prompt draft

Implement `validate_episodes` as described in problem.md. Explain the reasoning in theory.md before presenting the independent reference solution.

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

The `schema` adapter receives bounded numerical examples, never arbitrary HTML. The lesson outline in theory.md describes the visualization. A linked numerical table is the screen-reader and reduced-motion fallback.

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

