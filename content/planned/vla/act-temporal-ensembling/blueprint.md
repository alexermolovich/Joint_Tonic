---
schema_version: 1
problem_id: "act-temporal-ensembling"
content_version: "0.1.0"
status: "reviewed"
title: "Blend Overlapping Action Chunks with Temporal Ensembling"
summary: "Align predictions to one target control tick and combine eligible chunks with ACT’s oldest-first exponential weighting."
type: "component"
difficulty: "medium"
estimated_minutes: 45
domains: ["VLA and embodied robot learning"]
topics: ["act","temporal-ensembling","action-alignment"]
paper_ids: ["2023-aloha-act"]
paper_sections: ["SectionIV.A: exponential temporal ensemble, w0 is the oldest action","SectionVI.A: action chunking and temporal ensembling ablation"]
track_ids: []
prerequisite_problem_ids: []
runtime: {"language":"python","python":"3.10.11","image_digest":null,"publication_note":"Proposed local CPU runtime; exact dependency versions match the inspected authoring environment. No sandbox image has been built or validated for this draft. Pin its OCI digest before publishing.","dependencies":{"numpy":"2.2.4"},"limits":{"wall_seconds":10,"cpu_seconds":8,"memory_mb":512,"output_kb":64}}
entrypoint: "solution.temporal_ensemble"
physical_contract: {"frames":["All chunks share one caller-declared action frame and channel schema"],"units":{"predictions":"per-channel normalized Euclidean action values","start_ticks":"integer control ticks","target_tick":"integer control tick","decay":"dimensionless weight decay per eligible prediction rank"},"axes":"predictions(C,H,D), valid(C,H), start_ticks(C), output(D), weights(C)","timestamp_assumptions":"Strictly increasing chunk start ticks, fixed control period, horizon offset h predicts start_tick+h. Only chunks available no later than target_tick are eligible.","batching":"C indexes overlapping chunk predictions for one robot episode, not independent robots. D channels are averaged independently."}
grading: {"mode":"numerical","seed":20261113,"rtol":0.000001,"atol":1e-7,"public_case_families":["three aligned predictions with geometric weights","zero-valued valid prediction and mean weighting"],"hidden_case_families":["masked candidates and rank compression","target outside all chunks","future chunks","nonconsecutive start ticks","large decay","dtype/shape/value errors"],"performance_class":"none; resource budget only, no latency ranking"}
fixtures: {"source":"Independently authored synthetic inputs in examples.md; future evaluator fixtures must use this documented contract.","license":"CC0-1.0","version_or_hash":"vla-draft-fixtures-0.1.0"}
provenance: {"authoring_notes":"This exercise implements ACT’s temporal ensembling after chunk predictions already exist. It follows the primary paper’s oldest-first rank convention. Explicit validity masks, nonconsecutive start ticks, and returned diagnostic weights are teaching extensions; normalized Euclidean channels exclude quaternion averaging and wrapped-angle interpolation.","primary_urls":["https://arxiv.org/abs/2304.13705"],"implementation_urls":[]}
owners: ["Joint Tonic content"]
reviewers: ["code_issue_scout"]
review_status: {"author":"draft authored; verification recorded in review.md","independent_subject_matter":"approved by code_issue_scout","independent_evaluator":"contract approved by code_issue_scout; implementation pending"}
---

# Blend Overlapping Action Chunks with Temporal Ensembling

## Learning objective

Align predictions to one target control tick and combine eligible chunks with ACT’s oldest-first exponential weighting.

## Paper connection and scope

This exercise implements ACT’s temporal ensembling after chunk predictions already exist. It follows the primary paper’s oldest-first rank convention. Explicit validity masks, nonconsecutive start ticks, and returned diagnostic weights are teaching extensions; normalized Euclidean channels exclude quaternion averaging and wrapped-angle interpolation.

Verified source locations: SectionIV.A: exponential temporal ensemble, w0 is the oldest action; SectionVI.A: action chunking and temporal ensembling ablation. [Primary paper](https://arxiv.org/abs/2304.13705).

## Contract

The complete normative function, inputs, outputs, errors, and shape/physical conventions are in [statement.md](statement.md). This blueprint proposes that contract for review; it does not publish it.

Align by target_tick-start_tick before weighting; use oldest-first rank over eligible rows, not age in ticks. The valid mask permits genuine zero actions. Return the blended vector and full-length diagnostic weights, with no-candidate ValueError and float64 accumulation before casting.

## Learner prompt draft

Combine predictions for one physical control tick while preserving ACT’s original oldest-first weighting convention and exposing which chunks contributed.

## Worked examples

### Case1: three chunks predicting tick2

```text
predictions = [[[0],[0],[2]], [[0],[4],[0]], [[8],[0],[0]]]
start_ticks = [0,1,2]   # int64
valid = [[True,True,True], [True,True,True], [True,True,True]]
target_tick = 2
decay = ln(2)

action = [24/7]         # approximately3.4285714286
weights = [4/7,2/7,1/7]
```

Selected entries are predictions[0,2]=2, predictions[1,1]=4, and predictions[2,0]=8. Raw weights are1,1/2,1/4. The oldest prediction receives the largest weight.

### Case2: a real zero prediction remains eligible

```text
predictions = [[[7],[7],[0]], [[10],[20],[30]]]
start_ticks = [5,7]   # int64
valid = [[True,True,True], [True,True,True]]
target_tick = 7
decay = 0

action = [5]
weights = [0.5,0.5]
```

The selected values are0 and10. Their mean is5; excluding a zero-valued prediction would incorrectly return10.

## Starter-code plan

A future `starter.py` will import numpy as np, provide the signature in statement.md, and leave only the named function body for the learner. No executable starter or evaluator is registered by this draft.

## Reference-solution plan

Validate all inputs and strict start order. Compute offsets and eligibility; gather the selected vectors in existing chronological order. Generate rank-based exp(-m*i) in float64, normalize, scatter weights into lengthC, and reduce selected actions in float64. Cast outputs without aliasing. No candidate produces ValueError.

## Evaluator plan

| Case family | Visibility | Required evidence |
|---|---|---|
| Three aligned chunks | public | Exact selection and4:2:1 weighting |
| Zero action and masked candidate | public | Validity independent of numeric values; invalid weights exactly zero |
| Gapped starts and masked middle row | hidden | Rank compression rather than timestamp-age weighting |
| No candidates/future starts/expired windows | hidden | Documented eligibility and ValueError |
| Large decay and dtype casting | hidden | Finite normalized result; weight sum near1 |
| Noncontiguous and invalid inputs | hidden | No mutation or aliasing; proper error classes |

Use seed 20261113 for generated fixtures. Exact shape, dtype, mask, exception class, and immutability checks accompany numerical tolerances in frontmatter. Generate fixtures only inside documented bounds. Dependency/image startup failures are platform errors, not wrong answers. The resource budget is proposed and must be calibrated in the isolated worker before publication.

## Visualization plan

The original Mermaid/shape diagram and its text alternative are written in [theory.md](theory.md). They are static and require no animation or reduced-motion exception. A future interactive adapter may consume only bounded numerical arrays; no learner HTML or simulation process is needed for this component.

## Theory and hints

[Theory](theory.md) provides intuition, defined equations, a worked calculation, the visual, robot failure modes, and three understanding questions. [Hints](hints.md) reveals the mechanism progressively; [review notes](review.md) keeps the question answer key away from the learner prompt.

## MLOps/reproducibility extension

Persist action schema, chunk start tick, observation capture time, normalization version, decay, and validity convention. Log effective contribution weights when investigating control lag; a smooth command can still be based mostly on stale observations.

## Editorial checklist

- [x] Draft paper ID, canonical source, scope, and fixture license are recorded.
- [x] Shapes, dtypes, units, frames, time, errors, and batch axes are specified.
- [x] Statement, theory, hints, examples, diagram, and questions are independently authored.
- [x] Exact candidate dependency versions are recorded; OCI image remains explicitly pending.
- [ ] Independent subject-matter review approved.
- [ ] Independent evaluator review approved.
- [ ] Starter, reference implementation, public tests, and hidden tests implemented.
- [ ] Reference passes public/hidden cases in a pinned clean sandbox.
- [ ] Published renderer accessibility and narrow-screen presentation reviewed.
