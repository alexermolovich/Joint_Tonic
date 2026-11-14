# Evaluator metadata and catalog digests differ across line endings

Status: fixed and locally merged in `fc5e5d3` after exact-diff review and focused regression checks. No authenticated GitHub issue API is available in this workspace; this issue draft was not posted remotely.

## Reproduction

The repository uses `core.autocrlf=true` on this Windows workspace and has no `.gitattributes` policy. Git stores Python text as LF while some authoring scripts calculated `grading.evaluator_sha256` over CRLF working files. At checkpoint `d045b0e`, an audit found 105 existing packages whose declared evaluator hash differs from SHA-256 of their LF-normalized `cases.py`. Examples: `act-chunk-compounding-error`, `bev-camera-health-diagnostics`, `broadcast-batched-sensor-features`.

Read each metadata field, normalize CRLF to LF in the corresponding evaluator, and compare SHA-256. The 65 newly added packages in that checkpoint were normalized before commit and match their shipped evaluator bytes. This correction did not change their test semantics.

`scripts/sync-supabase-catalog.mjs` also hashes raw working-tree bytes for the complete source manifest. Equivalent Windows/Linux checkouts can therefore produce different immutable catalog digests. No hosted catalog sync has been applied from this workspace.

## Impact and scope

Local grading uses the actual evaluator and computes actual source lineage; this finding is not evidence of incorrect reference results or an authorization bypass. The defect is inconsistent provenance metadata and non-reproducible release catalog planning across platforms.

## Proposed fix worker task

Use an isolated `codex/` worktree. Establish an explicit LF convention for versioned source text, correct inaccurate declared hashes without changing tests or learner contracts, and make catalog planning consistently hash the canonical source representation or reject a noncanonical checkout with an actionable message. Preserve published semantic contracts and do not overwrite remote immutable versions. Include a focused LF/CRLF equivalence regression and metadata-integrity validation; do not rerun every unchanged numerical evaluator solely for newline changes.

Prepare a PR linking the issue once remote issue/PR access is available. The main worker must review the exact diff and focused evidence before merging. Existing unrelated feature work remains in the shared main checkout.
