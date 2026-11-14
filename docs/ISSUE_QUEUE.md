# Issue and fix queue

This is a coordination record, not a claim that a local draft has been published to GitHub. Confirmed findings need a reproduction, a narrow fix, independent review, and a PR before merge. User authorization covers the main agent reviewing and merging ready fixes.

| Issue | Current state | Next action |
|---|---|---|
| [#2: IoU/NMS visualization](https://github.com/alexermolovich/Joint_Tonic/issues/2) | Earlier local fix; not isolated in a PR | Package the reviewed change without unrelated UI work |
| [#4: draft/note flush](https://github.com/alexermolovich/Joint_Tonic/issues/4) | Confirmed, unresolved | Dedicated fix worker; navigate immediately after editing to prove recovery |
| [#5: saved display name](https://github.com/alexermolovich/Joint_Tonic/issues/5) | Fix pushed on `codex/fix-settings-name`; PR not opened | Publish prepared PR, review current diff, merge |
| [#6: light-theme CLIP labels](https://github.com/alexermolovich/Joint_Tonic/issues/6) | Earlier local contrast fix; not isolated in a PR | Package reviewed palette change |
| [#7: account activity clock](https://github.com/alexermolovich/Joint_Tonic/issues/7) | Confirmed, unresolved | Dedicated fix worker; keep mounted while a newer submission arrives |
| [GR00T objective wording](issues/gr00t-action-loss.md) | Fix pushed as `codex/gr00t-flow-objective` / `12fb5c3`; independently reviewed by research curator | Publish issue and PR; merge after final review |
| [Local storage quota](issues/local-workspace-quota.md) | Reproduced local issue draft | Isolate a fix that preserves completed progress on quota failure |
| [Unicode output budget](issues/unicode-output-budget.md) | Reproduced local issue draft | Separate learner output bytes from bounded report transport |
| [Interrupted worker jobs](issues/interrupted-worker-jobs.md) | Reproduced local issue draft | Resolve persisted pending jobs on restart without duplicating executions |
| [Queued evaluator lineage](issues/queued-evaluator-lineage.md) | Reproduced local issue draft | Pin the executed evaluator artifact to the recorded identity |

The content-validator fix in [PR #3](https://github.com/alexermolovich/Joint_Tonic/pull/3) is merged (`63f77ef`). Other rows must not be marked merged merely because a branch or local file exists.

## Publication boundary

Git push is available. No authenticated issue/PR creation tool is currently available, and an earlier credential-access method was rejected by automatic approval review. Do not repeat it or expose credentials. Keep concrete issue text, PR text, commits, and review evidence ready for an authorized publishing interface.

## Curriculum review loop

Three agents author distinct paper streams and cross-review in a ring: perception → MLOps → VLA → perception. Findings go into a lane's `review-findings.md`, with severity, exact file/section, counterexample or source, proposed correction, and disposition. Authors fix findings; reviewers check the changed contract/math again. Drafts become `reviewed` only after that independent pass. Runtime implementation and publication remain separate gates.

Full scope and current draft links: [curriculum authoring status](../content/AUTHORING_STATUS.md).
