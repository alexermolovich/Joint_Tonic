# Author review: Select Compact Visual Tokens with Learned Attention

Status: **reviewed contract; implementation and sandbox validation pending**.

## Proof of success

Both worked examples must match tokens and weights; common-logit shifts must preserve results; masked positions must have zero influence; finite-difference checks must confirm differentiability when the evaluator is implemented.

## Source verification and decisions

RT-1 Section5.1 identifies token compression. The official TokenLearnerModule.call, pinned to commit 4569641b8111f3f402c32d8e24becd2a6e952ecc, applies spatial softmax then aggregates original features. This draft supplies the learned logits and adds explicit masked padding; it does not reproduce the MLP or train a policy.

## Author checks

- [x] Paired paper card read before primary-source verification.
- [x] Complete deterministic contract and two worked examples written.
- [x] Original explanation, equations, static diagram, text fallback, and questions written.
- [x] Numerical examples and equation rendering checked after authoring. Author arithmetic: 12 examples across the batch, including masked gradients and exact matrices. Shared validator: 6 packages, 132 LaTeX expressions. This is not executable evaluator approval.
- [ ] Independent subject-matter reviewer approved the source interpretation.
- [ ] Independent evaluator reviewer approved errors, bounds, tolerances, and gradient/aliasing rules.
- [ ] Executable starter/reference/tests and isolated runtime validated.

## Question answer key

1. The common exponential factor cancels between numerator and denominator; max subtraction uses exactly this invariance.
2. Every valid location can contribute a nonzero normalized weight; no discrete location subset is selected by the function.
3. Exclude it from the normalization maximum/denominator and set its final weight to zero; masking only the returned token is too late.

## Risks for the next reviewer

Reviewer should check that K<=N is a declared educational bound rather than a universal TokenLearner restriction; test max-shift stability, gradient behavior, and the all-masked rejection. Review image-grid flattening language and avoid claiming compact tokens correspond one-to-one to named objects.

The original contract review is retained above. This implementation directory now contains application metadata, reference code and an evaluator.

## Independent review — code_issue_scout

Read all six files, the RT-1 card and manifest, and pinned official TokenLearner code. Confirmed spatial normalization and aggregation of original features. Independently recomputed both examples in WSL PyTorch, checked masked feature/logit gradients are zero, and verified the first attention row logit gradient against the analytic derivative. Supplied logits and padding are honestly scoped; no blocking contract issue.

Approved for implementation. The draft runtime is a proposal: use the actual CPython3.12.3 local baseline and its enforced caps for a runnable package. Approval does not certify unimplemented cases, an OCI image, or the rendered UI.


## Runtime verification — implementation worker

Reference passed 8 unique public/hidden checks in the actual Linux bubblewrap worker, using both public Run and complete Submit. Python3.12.3, NumPy2.2.4 and PyTorch2.6.0CPU where required; shared18s wall/10s CPU/4096MiB/64KiB caps. The checks cover the published contract, not full-paper reproduction. The evaluator source SHA-256 is pinned in blueprint.md; no OCI digest is claimed for the local environment. Static theory tables and original LaTeX are present; no source figure or paper code was copied.
