---
schema_version: 1
problem_id: "pi0-flow-action-interpolants"
content_version: "0.1.0"
status: "reviewed"
title: "Sample Flow-Matching Action Interpolants and Targets"
summary: "Construct pi0-style noise-to-action linear interpolants and constant velocity targets from supplied noise, times, and validity masks."
type: "component"
difficulty: "medium"
estimated_minutes: 35
domains: ["VLA and embodied robot learning"]
topics: ["pi0","flow-matching","continuous-actions"]
paper_ids: ["2024-pi0"]
paper_sections: ["arXiv2410.24164v4 SectionIV page5: noised actionsA_tau=tau*A+(1-tau)*noise and targetA-noise","SectionIV: forward Euler integration fromtau=0 to1"]
track_ids: []
prerequisite_problem_ids: ["diffusion-action-noising"]
runtime: {"language":"python","python":"3.10.11","image_digest":null,"publication_note":"Proposed local CPU runtime; exact dependency versions match the inspected authoring environment. No sandbox image has been built or validated for this draft. Pin its OCI digest before publishing.","dependencies":{"numpy":"2.2.4","torch":"2.6.0+cpu"},"limits":{"wall_seconds":10,"cpu_seconds":8,"memory_mb":2048,"output_kb":64}}
entrypoint: "solution.flow_action_interpolants"
physical_contract: {"frames":["Normalized Euclidean action channels in one caller-declared control frame"],"units":{"actions":"dimensionless normalized action coordinates","noise":"dimensionless supplied samples in the same coordinates","tau":"dimensionless flow time in[0,1]","target_velocity":"normalized action coordinate change per unit flow time"},"axes":"actions and noise(B,H,D); tau(B); valid(B,H); both outputs(B,H,D)","timestamp_assumptions":"H indexes future physical control ticks; tau is generative flow time and never a robot timestamp.","batching":"Each batch item has one flow time broadcast across its horizon and action channels. Masking zeros both outputs at invalid horizon positions."}
grading: {"mode":"numerical","seed":20261113,"rtol":0.000001,"atol":1e-7,"public_case_families":["fractional interpolation with two action channels","different endpoint times in one batch"],"hidden_case_families":["all-padding construction","gradient identities","noncontiguous tensors","per-item broadcasting","range/dtype/device validation"],"performance_class":"none; resource budget only, no latency ranking"}
fixtures: {"source":"Independently authored synthetic inputs in examples.md; future evaluator fixtures must use this documented contract.","license":"CC0-1.0","version_or_hash":"vla-draft-fixtures-0.1.0"}
provenance: {"authoring_notes":"The task constructs training samples for the linear interpolation path in pi0 arXiv2410.24164v4 SectionIV page5, whose velocity target is actions-minus-noise. Earlier v1 printed the opposite sign; this exercise pins the corrected v4 equation. Noise and flow times are supplied. Padding masks are an educational extension; no full VLA reproduction is claimed.","primary_urls":["https://arxiv.org/pdf/2410.24164v4"],"implementation_urls":[]}
owners: ["Joint Tonic content"]
reviewers: ["code_issue_scout"]
review_status: {"author":"draft authored; verification recorded in review.md","independent_subject_matter":"approved by code_issue_scout","independent_evaluator":"contract approved by code_issue_scout; implementation pending"}
---

# Sample Flow-Matching Action Interpolants and Targets

## Learning objective

Construct pi0-style noise-to-action linear interpolants and constant velocity targets from supplied noise, times, and validity masks.

## Paper connection and scope

The task constructs training samples for the linear interpolation path described in pi0 SectionIV. Noise and flow times are supplied to make the exercise deterministic; it does not draw the paper’s timestep distribution, train a vector field, integrate an ODE, or reconstruct a full VLA. Padding masks are an explicit educational batching extension.

Verified source: [arXiv2410.24164v4, SectionIV page5](https://arxiv.org/pdf/2410.24164v4): the path goes from noise at tau=0 to actions at tau=1, and its velocity target is actions-minus-noise. Earlier v1 printed the opposite target sign; the component follows the corrected v4 equation.

## Contract

The complete normative function, inputs, outputs, errors, and shape/physical conventions are in [statement.md](statement.md). This blueprint proposes that contract for review; it does not publish it.

Use the explicit noise-to-data conventiontau0=noise,tau1=actions and targetactions-noise. Broadcast one time per batch item, zero both outputs at padding, accept all-padding construction, preserve gradients, and perform no internal sampling.

## Learner prompt draft

Implement the linear flow-matching training pair and explain why its target and coefficients differ from the existing diffusion forward-noising exercise.

## Worked examples

### Case1: fractional time across a two-step action chunk

```text
actions = [[[2,-2],[4,6]]]
noise = [[[0,2],[2,2]]]
tau = [0.25]
valid = [[True,True]]

interpolant = [[[0.5,1],[2.5,3]]]
target_velocity = [[[2,-4],[2,4]]]
```

For the last scalar,0.75*2+0.25*6=3 and its velocity target is6-2=4. The same flow time applies to every action coordinate in this batch item.

### Case2: different endpoints for different batch items

```text
actions = [[[2]], [[-1]]]
noise = [[[6]], [[3]]]
tau = [0,1]
valid = [[True],[True]]

interpolant = [[[6]], [[-1]]]
target_velocity = [[[-4]], [[-4]]]
```

The first item is exactly noise at tau0; the second is exactly clean action at tau1. The velocity target does not vanish at either endpoint.

## Starter-code plan

A future `starter.py` will import torch, provide the signature in statement.md, and leave only the named function body for the learner. No executable starter or evaluator is registered by this draft.

## Reference-solution plan

Validate all four tensors, broadcast times/mask, form the linear mixture and endpoint difference, and mask both outputs into fresh tensors. Do not use detached scalars or internal randomness. ComplexityO(BHD); gradients follow directly from the affine formulas.

## Evaluator plan

| Case family | Visibility | Required evidence |
|---|---|---|
| Fractional time and endpoints | public | Exact stated outputs and target independence fromtau |
| Mask and all-padding pair | public/hidden | Both outputs zero at padding; all-padding succeeds |
| Per-item broadcasting | hidden | DifferentB,H,D sizes prevent accidental alignment |
| Analytical and finite-difference gradients | hidden | dX/dtau=A-E summed over selected coordinates; endpoint/input gradients preserved |
| Noncontiguous and invalid tensors | hidden | Same outputs or documented errors; no aliasing/mutation |

Use seed 20261113 for generated fixtures. Exact shape, dtype, mask, exception class, and immutability checks accompany numerical tolerances in frontmatter. Generate fixtures only inside documented bounds. Dependency/image startup failures are platform errors, not wrong answers. The resource budget is proposed and must be calibrated in the isolated worker before publication.

## Visualization plan

The original Mermaid/shape diagram and its text alternative are written in [theory.md](theory.md). They are static and require no animation or reduced-motion exception. A future interactive adapter may consume only bounded numerical arrays; no learner HTML or simulation process is needed for this component.

## Theory and hints

[Theory](theory.md) provides intuition, defined equations, a worked calculation, the visual, robot failure modes, and three understanding questions. [Hints](hints.md) reveals the mechanism progressively; [review notes](review.md) keeps the question answer key away from the learner prompt.

## MLOps/reproducibility extension

Version interpolation direction, target parameterization, action normalization, supplied-noise distribution, and timestep sampling policy with the checkpoint. Record flow time separately from episode ticks; deployment integration must use the same vector-field direction.

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
