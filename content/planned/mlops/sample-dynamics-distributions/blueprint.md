---
schema_version: 1
problem_id: "sample-dynamics-distributions"
content_version: "0.1.0"
status: "reviewed"
title: "Sample Mass, Friction, Delay, and Gain Distributions"
summary: "Convert reproducible unit draws into valid, explicitly typed per-episode physical parameter configurations."
type: "function"
difficulty: "medium"
estimated_minutes: 35
domains: ["robotics-mlops"]
topics: ["dynamics-randomization","reproducible-simulation"]
paper_ids: ["2018-dynamics-randomization"]
paper_sections: ["Section V and Table I: physical parameter distributions and per-episode sampling"]
track_ids: []
prerequisite_problem_ids: []
runtime:
  language: "python"
  python: "3.12.3"
  image_digest: null
  image_status: "pending-build-and-verification"
  dependencies: {numpy: "2.2.4"}
  platform: "linux-x86_64-cpu"
  limits: {wall_seconds: 3, cpu_seconds: 2, memory_mb: 512, output_kb: 64}
  budget_status: "planned; not measured"
entrypoint: "solution.sample_dynamics"
physical_contract:
  frames: []
  units: {"mass_kg":"kg","friction":"dimensionless Coulomb coefficient","gain_scale":"dimensionless multiplier","delay_ticks":"integer control ticks","dt_s":"seconds per control tick","delay_s":"seconds"}
  axes: "Columns ordered mass, friction, delay, gain; scalars have no spatial axis."
  timestamp_assumptions: "One draw row per episode reset; hold parameters fixed for that episode. Delay is integer control ticks of a supplied fixed dt_s."
  batching: "float64 unit_draws shape (B,4); outputs each shape (B,)."
grading:
  mode: "numerical"
  seed: 20261113
  rtol: 1.0e-12
  atol: 1.0e-12
  public_case_families: ["lower and geometric midpoint draws","fixed bounds","empty batch"]
  hidden_case_families: ["half-open upper draw rejected","nonpositive log bounds","reversed bounds","wrong column count/dtype","near-upper integer delay bucket","unknown/missing bounds"]
  performance_class: "none; no timing leaderboard"
fixtures:
  source: "original synthetic examples"
  license: "CC0-1.0"
  version_or_hash: "synthetic-mlops-0.1.0"
  generated_fixture_hash: null
provenance:
  authoring_notes: "Original instructional contract, examples, and diagrams; no copied paper code or figures."
  primary_urls: ["https://arxiv.org/abs/1710.06537"]
  implementation_urls: []
  paper_card: "research/papers/mlops-sim2real/2018-dynamics-randomization.md"
  manifest: "research/manifests/mlops-sim2real.md"
owners: ["code_issue_scout"]
reviewers: ["ui_issue_scout"]
---
# Sample Mass, Friction, Delay, and Gain Distributions

## Learning objective

Convert reproducible unit draws into valid, explicitly typed per-episode physical parameter configurations.

## Paper connection and scope

The source uses log-sampled physical parameters. This exercise deliberately uses fixed integer action-delay ticks instead of reproducing its time-varying action-timestep process; ranges are synthetic. Source location: Section V and Table I: physical parameter distributions and per-episode sampling. [Primary source](https://arxiv.org/abs/1710.06537).

## Contract and worked examples

Map columns0/1/3 through bounded log-uniform transforms and column2 into an inclusive discrete uniform tick interval. Return physical arrays plus delay_s; no simulator or internal RNG call. statement.md is the normative input/error/output specification; examples.md expands its two public examples. Inputs must not be mutated. No published implementation or evaluator exists yet.

## Starter-code plan

Provide the signature and necessary types/imports from statement.md. Leave the component body as the learner's task. No networking, filesystem access, or simulator control belongs in learner code.

## Reference-solution plan

Validate all bounds/draws first. For a positive range [a,b], compute exp(log(a)+u*(log(b)-log(a))); for delay use lo+floor(u*(hi-lo+1)). Multiply integer delays by dt_s for seconds. O(B) time and memory. Use float64 and int64 outputs, not a mixed float matrix.

## Evaluator plan

Public families: lower and geometric midpoint draws; fixed bounds; empty batch. Hidden families: half-open upper draw rejected; nonpositive log bounds; reversed bounds; wrong column count/dtype; near-upper integer delay bucket; unknown/missing bounds. Compare order, shape, and dtype exactly; apply the stated numerical tolerances where relevant. Validate errors by exception type rather than message. Check input immutability. Seed generated fixtures with 20261113; no wall-clock timing or network enters correctness grading. Report platform setup failures separately from learner failures. Image digest, fixture hashes, implementation, and isolated evaluator checks remain pending.

## Visualization plan

Original four-column shape/transform diagram and output table; static and text-described. This is a Markdown diagram specification, not a claim that today's renderer supports Mermaid. Keep the static text/table fallback usable before publication.

## Theory, hints, and reproducibility

Read theory.md for intuition, defined math, a worked example, robot failure modes, and conceptual questions. hints.md provides progressive help. Preserve input artifact versions, configuration, evaluator version, and seed with future scores. Review risk: Independent parameter draws do not ensure a valid full robot inertia tensor or real-world safety. Fixed per-episode delay is a declared teaching deviation; do not claim paper reproduction or resample every control step.

## Editorial status

- [x] Paper card and manifest checked against the primary source.
- [x] Original contract, two examples, theory, visual, and text alternative drafted.
- [x] Exact Python/dependency versions specified; image digest honestly pending.
- [x] Independent draft-contract, mathematics, and pedagogy cross-review approved; implementation/evaluator review remains pending.
- [ ] Reference, public tests, and hidden tests implemented and isolated.
- [ ] Runtime image, measured limits, fixture hashes, and rendered accessibility approved.
- [ ] Publication authorized; this remains planned content.
