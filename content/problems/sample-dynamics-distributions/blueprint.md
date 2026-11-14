---
schema_version: 1
problem_id: sample-dynamics-distributions
content_version: 1.0.1
status: implemented
title: 'Sample Mass, Friction, Delay, and Gain Distributions'
summary: >-
  Convert reproducible unit draws into valid, explicitly typed per-episode
  physical parameter configurations.
type: function
difficulty: medium
estimated_minutes: 35
domains:
  - robotics-mlops
topics:
  - dynamics-randomization
  - reproducible-simulation
paper_ids:
  - 2018-dynamics-randomization
paper_sections:
  - >-
    Section V and Table I: physical parameter distributions and per-episode
    sampling
track_ids: []
prerequisite_problem_ids: []
runtime:
  language: python
  python: 3.12.3
  image_digest: null
  image_status: pending-image-build; tested using the local bubblewrap baseline
  dependencies:
    numpy: 2.2.4
    torch: 2.6.0+cpu
  platform: linux-x86_64-cpu
  limits:
    wall_seconds: 18
    cpu_seconds: 10
    memory_mb: 4096
    output_kb: 64
  budget_status: actual shared worker caps; per-process address-space limit
  solution_dependencies:
    - numpy
  baseline_id: python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2
entrypoint: solution.sample_dynamics
physical_contract:
  frames: []
  units:
    mass_kg: kg
    friction: dimensionless Coulomb coefficient
    gain_scale: dimensionless multiplier
    delay_ticks: integer control ticks
    dt_s: seconds per control tick
    delay_s: seconds
  axes: 'Columns ordered mass, friction, delay, gain; scalars have no spatial axis.'
  timestamp_assumptions: >-
    One draw row per episode reset; hold parameters fixed for that episode.
    Delay is integer control ticks of a supplied fixed dt_s.
  batching: 'float64 unit_draws shape (B,4); outputs each shape (B,).'
grading:
  mode: numerical
  seed: 20261113
  rtol: 1.e-12
  atol: 1.e-12
  public_case_families:
    - lower and geometric midpoint draws
    - fixed bounds
    - empty batch
  hidden_case_families:
    - half-open upper draw rejected
    - nonpositive log bounds
    - reversed bounds
    - wrong column count/dtype
    - near-upper integer delay bucket
    - unknown/missing bounds
  performance_class: none; no timing leaderboard
  evaluator_sha256: e9453331d8d8cc7f88036078e50701d47eccfc6b490ed184f3c434db25492b62
fixtures:
  source: original synthetic examples
  license: CC0-1.0
  version_or_hash: 'sha256:e9453331d8d8cc7f88036078e50701d47eccfc6b490ed184f3c434db25492b62'
  generated_fixture_hash: e9453331d8d8cc7f88036078e50701d47eccfc6b490ed184f3c434db25492b62
provenance:
  authoring_notes: >-
    Original instructional contract, examples, and diagrams; no copied paper
    code or figures.
  primary_urls:
    - 'https://arxiv.org/abs/1710.06537'
  implementation_urls: []
  paper_card: research/papers/mlops-sim2real/2018-dynamics-randomization.md
  manifest: research/manifests/mlops-sim2real.md
owners:
  - code_issue_scout
reviewers:
  - ui_issue_scout
derived_draft_version: 0.1.0
---
# Sample Mass, Friction, Delay, and Gain Distributions

## Learning objective

Convert reproducible unit draws into valid, explicitly typed per-episode physical parameter configurations.

## Paper connection and scope

The source uses log-sampled physical parameters. This exercise deliberately uses fixed integer action-delay ticks instead of reproducing its time-varying action-timestep process; ranges are synthetic. Source location: Section V and Table I: physical parameter distributions and per-episode sampling. [Primary source](https://arxiv.org/abs/1710.06537).

## Contract and worked examples

Map columns0/1/3 through bounded log-uniform transforms and column2 into an inclusive discrete uniform tick interval. Return physical arrays plus delay_s; no simulator or internal RNG call. problem.md is the normative input/error/output specification; examples.md expands its two public examples. Inputs must not be mutated. The reference and public/hidden cases passed the local isolated worker.

## Starter code

starter.py supplies the signature; reference.py implements the reviewed contract. No networking, filesystem access, or simulator control belongs in learner code.

## Reference solution

Validate all bounds/draws first. For a positive range [a,b], compute exp(log(a)+u*(log(b)-log(a))); for delay use lo+floor(u*(hi-lo+1)). Multiply integer delays by dt_s for seconds. O(B) time and memory. Use float64 and int64 outputs, not a mixed float matrix.

## Evaluator plan

Public families: lower and geometric midpoint draws; fixed bounds; empty batch. Hidden families: half-open upper draw rejected; nonpositive log bounds; reversed bounds; wrong column count/dtype; near-upper integer delay bucket; unknown/missing bounds. Compare order, shape, and dtype exactly; apply the stated numerical tolerances where relevant. Validate errors by exception type rather than message. Check input immutability. Seed generated fixtures with 20261113; no wall-clock timing or network enters correctness grading. Report platform setup failures separately from learner failures. The reference passed eight public/hidden cases in submit mode and three public cases in run mode; the starter was rejected. cases.py pins evaluator and synthetic fixture source. The OCI image digest remains pending; execution used the stated local baseline.

## Visualization plan

Original four-column shape/transform diagram and output table; static and text-described. This is a Markdown diagram specification, not a claim that today's renderer supports Mermaid. Keep the static text/table fallback usable before publication.

## Theory, hints, and reproducibility

Read theory.md for intuition, defined math, a worked example, robot failure modes, and conceptual questions. hints.md provides progressive help. Preserve input artifact versions, configuration, evaluator version, and seed with future scores. Review risk: Independent parameter draws do not ensure a valid full robot inertia tensor or real-world safety. Fixed per-episode delay is a declared teaching deviation; do not claim paper reproduction or resample every control step.

## Editorial status

- [x] Paper card and manifest checked against the primary source.
- [x] Original contract, two examples, theory, visual, and text alternative drafted.
- [x] Exact Python/dependency versions specified; image digest honestly pending.
- [x] Independent draft-contract, mathematics, and pedagogy cross-review approved; implementation/evaluator review remains pending.
- [x] Reference, public tests, and hidden tests passed the actual local bubblewrap worker.
- [ ] Runtime image, measured limits, fixture hashes, and rendered accessibility approved.
- [x] Local runnable integration authorized; production publication remains separate.
