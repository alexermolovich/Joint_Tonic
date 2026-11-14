---
schema_version: 1
problem_id: "diffusion-conditional-noise-loss"
content_version: "0.1.0"
status: "reviewed"
title: "Compute a Conditional Noise-Prediction Loss"
summary: "Reduce predicted-versus-supplied diffusion noise errors over exactly the valid action scalars while preserving training gradients."
type: "component"
difficulty: "medium"
estimated_minutes: 30
domains: ["VLA and embodied robot learning"]
topics: ["diffusion-policy","noise-prediction","masked-loss"]
paper_ids: ["2023-diffusion-policy"]
paper_sections: ["SectionIII: conditional denoising diffusion training objective","Joint Tonic published diffusion-action-noising contract supplies target noise and validity masks"]
track_ids: []
prerequisite_problem_ids: ["diffusion-action-noising"]
runtime: {"language":"python","python":"3.10.11","image_digest":null,"publication_note":"Proposed local CPU runtime; exact dependency versions match the inspected authoring environment. No sandbox image has been built or validated for this draft. Pin its OCI digest before publishing.","dependencies":{"numpy":"2.2.4","torch":"2.6.0+cpu"},"limits":{"wall_seconds":10,"cpu_seconds":8,"memory_mb":2048,"output_kb":64}}
entrypoint: "solution.conditional_noise_loss"
physical_contract: {"frames":["Normalized action coordinates associated with the caller’s controller schema; no coordinate conversion"],"units":{"prediction":"dimensionless noise in normalized action space","target_noise":"dimensionless supplied corruption noise","loss":"mean squared normalized-noise error"},"axes":"prediction and target_noise(B,H,D); valid(B,H); output is a scalar tensor","timestamp_assumptions":"H is a future control horizon; diffusion level and observation context already condition the upstream prediction and are not function arguments.","batching":"One global mean over all valid scalar channels across B and H; not an equal-weight mean of per-item losses."}
grading: {"mode":"numerical","seed":20261113,"rtol":0.000001,"atol":1e-7,"public_case_families":["masked two-channel prediction","unequal valid horizons across two batch items"],"hidden_case_families":["all-padding rejection","gradient scaling and masked gradients","noncontiguous tensors","dtype/device/value errors","target gradients preserved"],"performance_class":"none; resource budget only, no latency ranking"}
fixtures: {"source":"Independently authored synthetic inputs in examples.md; future evaluator fixtures must use this documented contract.","license":"CC0-1.0","version_or_hash":"vla-draft-fixtures-0.1.0"}
provenance: {"authoring_notes":"This component computes the masked noise-regression reduction after a conditional denoiser has run. It does not build that network, sample timesteps/noise, construct noised actions, or duplicate the published forward-noising problem. Validity masking and the exact global reduction are explicit teaching contracts.","primary_urls":["https://arxiv.org/abs/2303.04137"],"implementation_urls":[]}
owners: ["Joint Tonic content"]
reviewers: ["code_issue_scout"]
review_status: {"author":"draft authored; verification recorded in review.md","independent_subject_matter":"approved by code_issue_scout","independent_evaluator":"contract approved by code_issue_scout; implementation pending"}
---

# Compute a Conditional Noise-Prediction Loss

## Learning objective

Reduce predicted-versus-supplied diffusion noise errors over exactly the valid action scalars while preserving training gradients.

## Paper connection and scope

This component computes the masked noise-regression reduction after a conditional denoiser has run. It does not build that network, sample timesteps/noise, construct noised actions, or duplicate the published forward-noising problem. Validity masking and the exact global reduction are explicit teaching contracts.

Verified source locations: SectionIII: conditional denoising diffusion training objective; Joint Tonic published diffusion-action-noising contract supplies target noise and validity masks. [Primary paper](https://arxiv.org/abs/2303.04137).

## Contract

The complete normative function, inputs, outputs, errors, and shape/physical conventions are in [statement.md](statement.md). This blueprint proposes that contract for review; it does not publish it.

Global masked MSE uses denominatorD*number_of_valid_horizon_slots, returns a differentiable scalar tensor, and rejects all-padding batches. No noise generation or denoiser call occurs. Both floating inputs retain gradients; invalid scalar locations contribute exactly zero.

## Learner prompt draft

Implement the noise-prediction training loss so padding and unequal valid horizons do not silently change the intended weighting.

## Worked examples

### Case1: padding does not contribute

```text
prediction = [[[1,3],[100,100]]]
target_noise = [[[0,1],[0,0]]]
valid = [[True,False]]

loss = scalar tensor2.5
```

The valid residual is[1,2], giving(1²+2²)/2=2.5. When prediction requires gradients, its gradient is[[[1,2],[0,0]]]. The padded100 values are finite but ignored by the objective.

### Case2: one global mean with unequal valid horizons

```text
prediction = [[[2],[0]], [[2],[4]]]
target_noise = [[[0],[0]], [[0],[0]]]
valid = [[True,False], [True,True]]

loss = scalar tensor8
```

There are three valid scalar errors:4,4,16. Their mean is8. Averaging per-item means would instead yield(4+10)/2=7, which is not this contract.

## Starter-code plan

A future `starter.py` will import torch, provide the signature in statement.md, and leave only the named function body for the learner. No executable starter or evaluator is registered by this draft.

## Reference-solution plan

Validate CPU tensors and bounds; count valid slots and reject zero. Form squared residuals, apply the broadcast validity mask, sum globally, and divide byD*valid_count using tensor arithmetic. Preserve both input computation graphs. ComplexityO(BHD), bounded temporary storageO(BHD).

## Evaluator plan

| Case family | Visibility | Required evidence |
|---|---|---|
| Two numerical reductions | public | 2.5 and8; scalar shape and matching dtype |
| Known prediction gradient | public/hidden | Masked zeros and exact denominator scaling |
| Float64 finite differences | hidden | Gradients through prediction and target agree with analytical residual derivative |
| Unequal valid lengths | hidden | Global scalar mean, not per-item mean |
| All-padding and malformed tensors | public/hidden | Explicit rejection and no mutation |

Use seed 20261113 for generated fixtures. Exact shape, dtype, mask, exception class, and immutability checks accompany numerical tolerances in frontmatter. Generate fixtures only inside documented bounds. Dependency/image startup failures are platform errors, not wrong answers. The resource budget is proposed and must be calibrated in the isolated worker before publication.

## Visualization plan

The original Mermaid/shape diagram and its text alternative are written in [theory.md](theory.md). They are static and require no animation or reduced-motion exception. A future interactive adapter may consume only bounded numerical arrays; no learner HTML or simulation process is needed for this component.

## Theory and hints

[Theory](theory.md) provides intuition, defined equations, a worked calculation, the visual, robot failure modes, and three understanding questions. [Hints](hints.md) reveals the mechanism progressively; [review notes](review.md) keeps the question answer key away from the learner prompt.

## MLOps/reproducibility extension

Log valid scalar count with loss aggregates so different padding fractions remain interpretable. Version prediction_type=noise, action normalization, mask convention, and reduction with checkpoints; comparing a vector-summed loss with a scalar mean is misleading.

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
