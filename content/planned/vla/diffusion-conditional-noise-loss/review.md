# Author review: Compute a Conditional Noise-Prediction Loss

Status: **reviewed contract; implementation checks remain separate**.

## Proof of success

Reproduce the two loss values, the Case1 gradient, and all-padding rejection. Future evaluator must additionally check dtype, scalar shape, finite-difference gradients, masked zeros, and immutability without invoking a model.

## Source verification and decisions

Diffusion Policy trains a conditional noise predictor against the known sampled corruption noise. The paired card and published forward-noising exercise establish theB,H,D andB,H mask interface. The new task isolates reduction and autograd; its global valid-scalar mean is explicitly specified rather than inferred from a framework default.

## Author checks

- [x] Paired paper card read before primary-source verification.
- [x] Complete deterministic contract and two worked examples written.
- [x] Original explanation, equations, static diagram, text fallback, and questions written.
- [x] Numerical examples and equation rendering checked after authoring. Author arithmetic: 12 examples across the batch, including masked gradients and exact matrices. Shared validator: 6 packages, 132 LaTeX expressions. This is not executable evaluator approval.
- [ ] Independent subject-matter reviewer approved the source interpretation.
- [ ] Independent evaluator reviewer approved errors, bounds, tolerances, and gradient/aliasing rules.
- [ ] Executable starter/reference/tests and isolated runtime validated.

## Question answer key

1. The declared denoiser parameterization predicts the known corruption noise; clean-action or velocity prediction defines a different model target and sampler contract.
2. Each valid horizon slot containsD scalar residuals; the task averages scalar errors, not vector sums.
3. It gives an item with one valid timestep the same total weight as an item with many, whereas this contract weights every valid scalar equally.

## Risks for the next reviewer

Reviewer should confirm the scalar denominator, all-padding behavior, target-gradient convention, and distinction from clean-action/flow-velocity losses. A future implementation must not infer validity from whether target noise equals zero.

This directory has no `meta.json`, runnable route, or registered execution-flow problem slug. Publication requires an implemented and reviewed evaluator, not only approved prose.

## Independent review — code_issue_scout

Read all six files and Diffusion Policy card/primary manuscript. Verified conditional noise-regression objective; masking/global scalar reduction are explicit teaching additions. Independently recomputed losses2.5 and8, checked prediction and target gradients including masked zeros in WSL PyTorch, and confirmed the all-padding rejection and tensor/shape contracts. No blocking contract issue.

Approved for implementation. Use the actual CPython3.12.3 baseline and enforced worker caps; draft approval does not certify an unpublished evaluator or OCI image.
