# Fix oversized scalar validation in four perception exercises

Passing a built-in integer such as `10**1000` as the threshold/epsilon previously raised `OverflowError`. The four affected exercises now check bounds before converting through `math.isfinite`, preserving the documented `ValueError` contract and all valid numerical behavior.

Addresses the local issue [Oversized integer scalars](../issues/oversized-scalar-validation.md). This is a local PR draft; no remote issue or PR was created.

The affected packages are `detr-decode-object-queries`, `vit-class-token-linear-head`, `dinov2-neighbor-feature-spreading`, and `grounding-localization-phrase-metrics`. Their content versions advance from 1.0.0 to 1.0.1 because the regression changes grading coverage. Reference snippets and evaluator digests match the corrected files. Unused helper copies are unchanged.

Validation: reproduced the original exception through all four public entrypoints; actual bubblewrap Run passed 8 public cases and Submit passed 20 case families, including positive/negative oversized integers. Reintroducing the original helper failed the new evaluator in all four packages. The content/schema validator passed 274 problems and 157 paper cards in the isolated base worktree. `git diff --check` passed. No hosted resources or learner data were touched.

Main reviewed the exact code/test/version diff and merged branch `codex/oversized-scalar-validation` in `f4c5b05`. The separate canonical-hash fix does not modify these four packages; their digests use UTF-8/LF evaluator bytes. This records a local branch merge, not a GitHub PR merge.
