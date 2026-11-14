# Author review: Sample Flow-Matching Action Interpolants and Targets

Status: **reviewed contract; implementation checks remain separate**.

## Proof of success

Reproduce both numerical cases and mask variant, then verify the affine gradient identities. Source review must confirmtau0=noise,tau1=data and the target sign before the draft can be promoted.

## Source verification and decisions

The checked-in pi0 manuscript SectionIV explicitly constructsA_tau=tau*A+(1-tau)*noise, targetsA-noise, and integrates from0 to1 with a positive Euler step. This is used as the normative sample formula. The Gaussian covariance implied by that formula is(1-tau)^2I; the draft avoids copying the manuscript’s potentially confusing variance notation.

## Author checks

- [x] Paired paper card read before primary-source verification.
- [x] Complete deterministic contract and two worked examples written.
- [x] Original explanation, equations, static diagram, text fallback, and questions written.
- [x] Numerical examples and equation rendering checked after authoring. Author arithmetic: 12 examples across the batch, including masked gradients and exact matrices. Shared validator: 6 packages, 132 LaTeX expressions. This is not executable evaluator approval.
- [ ] Independent subject-matter reviewer approved the source interpretation.
- [ ] Independent evaluator reviewer approved errors, bounds, tolerances, and gradient/aliasing rules.
- [ ] Executable starter/reference/tests and isolated runtime validated.

## Question answer key

1. At0 the point isE; at1 it isA. The target isA-E at both endpoints.
2. Broadcasting aligns trailing axes; reshape(B,1,1) makes each batch time apply to all of that item’s horizon/channel entries without accidental channel alignment.
3. The path derivative becomesE-A; the integration direction and sign must be changed consistently.

## Risks for the next reviewer

Reviewer should check endpoint/sign convention, flow-time versus robot-time language, masking of both outputs, and the supplied-randomness scope. This task is distinct from the existing square-root diffusion noising exercise.

This directory has no `meta.json`, runnable route, or registered execution-flow problem slug. Publication requires an implemented and reviewed evaluator, not only approved prose.

## Independent review — code_issue_scout

Read all six files, paired card and primary manuscript. Independently recomputed both worked pairs and analytic gradients in WSL PyTorch. Confirmed noise-at0/action-at1 endpoints, actions-minus-noise derivative, per-item time broadcasting, zeroed padding, and acceptance of all-padding construction. Found a version-specific source discrepancy: v1 prints the opposite target sign; canonical v4 SectionIV page5 corrects it. Author pinned v4 in blueprint, statement and theory; independently rechecked those edits. No blocking contract issue remains.

Approved for implementation using the actual baseline runtime/caps. Sandbox/evaluator approval remains separate.
