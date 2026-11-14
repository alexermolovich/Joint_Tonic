# Author review: Build a Causal Action-Token Mask

Status: **reviewed contract; implementation and sandbox validation pending**.

## Proof of success

Exact matrices must match both examples and the minimal case; every returned cell must satisfy the stated predicate. Independent review must verify the distinction between this raw structural mask and the complete model’s zeroed action embeddings/readout shifts.

## Source verification and decisions

The official _generate_masks at commit 4569641b8111f3f402c32d8e24becd2a6e952ecc starts from a causal mask and removes causal action/action pairs. _assemble_input_token_sequence zeroes action embeddings. The draft preserves that unusual visual-row behavior and explicitly excludes teacher-forced labels, unlike a generic block-causal teaching simplification.

## Author checks

- [x] Paired paper card read before primary-source verification.
- [x] Complete deterministic contract and two worked examples written.
- [x] Original explanation, equations, static diagram, text fallback, and questions written.
- [x] Numerical examples and equation rendering checked after authoring. Author arithmetic: 12 examples across the batch, including masked gradients and exact matrices. Shared validator: 6 packages, 132 LaTeX expressions. This is not executable evaluator approval.
- [ ] Independent subject-matter reviewer approved the source interpretation.
- [ ] Independent evaluator reviewer approved errors, bounds, tolerances, and gradient/aliasing rules.
- [ ] Executable starter/reference/tests and isolated runtime validated.

## Question answer key

1. Its own action diagonal is blocked; the query can still attend to earlier visual slots.
2. The extra prohibition applies only when both query and key are action slots. V1 is visual, so only causality applies.
3. No. Later visual rows can read earlier action slots and transmit that information indirectly; the reference also zeroes input action embeddings.

## Risks for the next reviewer

Reviewer should verify the source mask against all cells of a two-timestep layout and ensure no claim of full-model leakage prevention. The reference includes shifted prediction readouts; this draft intentionally returns only the raw input mask.

This directory has no `meta.json`, runnable route, or registered execution-flow problem slug. Publication requires an implemented and reviewed evaluator, not only approved prose.

## Independent review — code_issue_scout

Read all six files, the RT-1 card and manifest, and pinned official mask/input-assembly code. Independently enumerated every cell of both examples. Confirmed action/action exclusion, retained causal action-placeholder access by visual queries, zeroed official input action embeddings, and explicit exclusion of teacher-forced-label safety claims. No blocking contract issue.

Approved for implementation. The draft runtime is a proposal: use the actual CPython3.12.3 local baseline and its enforced caps for a runnable package. Approval does not certify unimplemented cases, an OCI image, or the rendered UI.
