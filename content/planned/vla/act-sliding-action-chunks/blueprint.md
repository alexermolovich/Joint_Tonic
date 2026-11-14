---
schema_version: 1
problem_id: "act-sliding-action-chunks"
content_version: "0.1.0"
status: "reviewed"
title: "Build Sliding Action Chunks with Padding Masks"
summary: "Extract fixed-horizon action windows from one episode while marking right-padding and preserving requested start order."
type: "component"
difficulty: "medium"
estimated_minutes: 35
domains: ["VLA and embodied robot learning"]
topics: ["act","action-chunking","episode-boundaries"]
paper_ids: ["2023-aloha-act"]
paper_sections: ["SectionIV.A: Action Chunking and Temporal Ensemble; action-sequence prediction","SectionIV.B: demonstration chunks used by the conditional VAE"]
track_ids: []
prerequisite_problem_ids: ["validate-robot-episodes"]
runtime: {"language":"python","python":"3.10.11","image_digest":null,"publication_note":"Proposed local CPU runtime; exact dependency versions match the inspected authoring environment. No sandbox image has been built or validated for this draft. Pin its OCI digest before publishing.","dependencies":{"numpy":"2.2.4"},"limits":{"wall_seconds":10,"cpu_seconds":8,"memory_mb":512,"output_kb":64}}
entrypoint: "solution.sliding_action_chunks"
physical_contract: {"frames":["Per-channel caller-declared controller frame; no coordinate transform"],"units":{"actions":"per-channel caller units or declared normalized coordinates","start_indices":"integer control ticks","horizon":"number of control ticks"},"axes":"actions(T,D); start_indices(S); chunks(S,H,D); valid(S,H)","timestamp_assumptions":"Exactly one episode sampled at a fixed control period; index0 is its first action. No window crosses into another episode.","batching":"S is the requested-window axis, not separate episodes. Start order and duplicates are preserved; empty S is allowed."}
grading: {"mode":"numerical","seed":20261113,"rtol":0.000001,"atol":1e-7,"public_case_families":["ordinary and end-of-episode windows","reordered duplicate starts with horizon beyond episode"],"hidden_case_families":["empty start list","long horizon","noncontiguous arrays","duplicate order","dtype/shape/range validation","no aliasing"],"performance_class":"none; resource budget only, no latency ranking"}
fixtures: {"source":"Independently authored synthetic inputs in examples.md; future evaluator fixtures must use this documented contract.","license":"CC0-1.0","version_or_hash":"vla-draft-fixtures-0.1.0"}
provenance: {"authoring_notes":"ACT motivates predicting future action chunks. This exercise only builds supervised target windows from one recorded episode. Zero right-padding and True=valid masks are explicit educational conventions; no CVAE, policy inference, or cross-episode concatenation is implemented.","primary_urls":["https://arxiv.org/abs/2304.13705"],"implementation_urls":[]}
owners: ["Joint Tonic content"]
reviewers: ["code_issue_scout"]
review_status: {"author":"draft authored; verification recorded in review.md","independent_subject_matter":"approved by code_issue_scout","independent_evaluator":"contract approved by code_issue_scout; implementation pending"}
---

# Build Sliding Action Chunks with Padding Masks

## Learning objective

Extract fixed-horizon action windows from one episode while marking right-padding and preserving requested start order.

## Paper connection and scope

ACT motivates predicting future action chunks. This exercise only builds supervised target windows from one recorded episode. Zero right-padding and True=valid masks are explicit educational conventions; no CVAE, policy inference, or cross-episode concatenation is implemented.

Verified source locations: SectionIV.A: Action Chunking and Temporal Ensemble; action-sequence prediction; SectionIV.B: demonstration chunks used by the conditional VAE. [Primary paper](https://arxiv.org/abs/2304.13705).

## Contract

The complete normative function, inputs, outputs, errors, and shape/physical conventions are in [statement.md](statement.md). This blueprint proposes that contract for review; it does not publish it.

Single-episode target extraction preserves requested order and duplicate starts. Only the window axis may be empty. Right-padding is zero with False validity; original zero actions stay True. Input float dtype is preserved, int64 starts are required, and outputs must not alias the recorded episode.

## Learner prompt draft

Build fixed-horizon demonstration targets and a validity mask so short episode tails can train action-chunk predictors without pretending padding is observed behavior.

## Worked examples

### Case1: a complete window and a padded tail

```text
actions = [[1],[2],[3]]
start_indices = [0,2]   # int64
horizon = 2

chunks = [[[1],[2]], [[3],[0]]]
valid = [[True,True], [True,False]]
```

The second window begins at the last real action. Its second slot has no target, so it is zero and invalid.

### Case2: preserve unsorted duplicate starts

```text
actions = [[2,-1],[4,3]]
start_indices = [1,0,1]   # int64
horizon = 3

chunks = [
  [[4,3],[0,0],[0,0]],
  [[2,-1],[4,3],[0,0]],
  [[4,3],[0,0],[0,0]]
]
valid = [[True,False,False], [True,True,False], [True,False,False]]
```

There is no deduplication or sorting. Every output row corresponds to the same-position entry of start_indices.

## Starter-code plan

A future `starter.py` will import numpy as np, provide the signature in statement.md, and leave only the named function body for the learner. No executable starter or evaluator is registered by this draft.

## Reference-solution plan

Validate the input episode and starts. Build an(S,H) index grid and validity relation, gather only safe indices, and zero invalid outputs. Ensure fresh storage even for trivial windows. ConstructionO(SHD), validationO(TD+S); outputO(SHD).

## Evaluator plan

| Case family | Visibility | Required evidence |
|---|---|---|
| Two worked examples | public | Exact copying, padding, order, duplicates |
| Empty S and valid zero action | public | Empty output shapes; zeros do not imply padding |
| Episode tails and H>T | hidden | No out-of-range reads and exact masks |
| Noncontiguous inputs and alias probes | hidden | Correct values; changes to outputs cannot change inputs |
| Input/budget errors | hidden | Documented dtype, rank, index, scalar, and size rejection |

Use seed 20261113 for generated fixtures. Exact shape, dtype, mask, exception class, and immutability checks accompany numerical tolerances in frontmatter. Generate fixtures only inside documented bounds. Dependency/image startup failures are platform errors, not wrong answers. The resource budget is proposed and must be calibrated in the isolated worker before publication.

## Visualization plan

The original Mermaid/shape diagram and its text alternative are written in [theory.md](theory.md). They are static and require no animation or reduced-motion exception. A future interactive adapter may consume only bounded numerical arrays; no learner HTML or simulation process is needed for this component.

## Theory and hints

[Theory](theory.md) provides intuition, defined equations, a worked calculation, the visual, robot failure modes, and three understanding questions. [Hints](hints.md) reveals the mechanism progressively; [review notes](review.md) keeps the question answer key away from the learner prompt.

## MLOps/reproducibility extension

Store episode ID, start tick, control period, horizon, channel schema, and mask convention with generated windows. Any cache key for chunked targets must include these fields; changing horizon or episode segmentation invalidates the derived targets.

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
