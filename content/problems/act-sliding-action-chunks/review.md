# Author review: Build Sliding Action Chunks with Padding Masks

Status: **reviewed contract; implementation checks remain separate**.

## Proof of success

Every nonpadding scalar must equal the source action at the documented index, padding must be zero/False, and no output may alias inputs. The two supplied examples and empty-S case establish the expected behavior before an evaluator is implemented.

## Source verification and decisions

ACT SectionIV.A predicts action sequences from the current observation; SectionIV.B trains on demonstrated chunks. The primary paper does not prescribe this NumPy function or a general dataset-padding API. Zero padding, masks, order preservation, and bounds are explicit independent teaching contracts.

## Author checks

- [x] Paired paper card read before primary-source verification.
- [x] Complete deterministic contract and two worked examples written.
- [x] Original explanation, equations, static diagram, text fallback, and questions written.
- [x] Numerical examples and equation rendering checked after authoring. Author arithmetic: 12 examples across the batch, including masked gradients and exact matrices. Shared validator: 6 packages, 132 LaTeX expressions. This is not executable evaluator approval.
- [ ] Independent subject-matter reviewer approved the source interpretation.
- [ ] Independent evaluator reviewer approved errors, bounds, tolerances, and gradient/aliasing rules.
- [ ] Executable starter/reference/tests and isolated runtime validated.

## Question answer key

1. Validity describes whether the target was recorded, not whether its numeric magnitude is nonzero.
2. Indices3 and4 are valid;5 and6 are padding, giving mask[True,True,False,False].
3. The next episode is a different temporal context, often after a reset; concatenation creates false observation/action pairs.

## Risks for the next reviewer

Reviewer should inspect episode-boundary handling, empty-window behavior, and aliasing guarantees. Confirm that the description never suggests padded zeros are commands or that arbitrary irregular timestamps can be chunked without resampling.

The original contract review is retained above. This implementation directory now contains application metadata, reference code and an evaluator.

## Independent review — code_issue_scout

Read all six files and ACT card/primary paper. Independently generated both window examples by direct index lookup. Confirmed terminal padding, valid zeros, ordered duplicate starts, empty start batch, exact copy semantics, input storage independence, channel units/frame preservation and documented TypeError/ValueError split. This is the explicit teaching data contract, not a claim to reproduce the full ACT loader. No blocking contract issue.

Approved for implementation. Use the actual CPython3.12.3 baseline and enforced worker caps; draft approval does not certify an unpublished evaluator or OCI image.


## Runtime verification — implementation worker

Reference passed 7 unique public/hidden checks in the actual Linux bubblewrap worker, using both public Run and complete Submit. Python3.12.3, NumPy2.2.4 and PyTorch2.6.0CPU where required; shared18s wall/10s CPU/4096MiB/64KiB caps. The checks cover the published contract, not full-paper reproduction. The evaluator source SHA-256 is pinned in blueprint.md; no OCI digest is claimed for the local environment. Static theory tables and original LaTeX are present; no source figure or paper code was copied.
