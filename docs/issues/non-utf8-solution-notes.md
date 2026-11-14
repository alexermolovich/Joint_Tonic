# Eight legacy solution notes are not UTF-8

Status: fixed in c835fc3, exact diff reviewed and merged into main. No remote issue/PR was created.

Strict canonical source hashing fails with `solution.md: source text must be valid UTF-8`. A byte-validation scan found exactly eight affected solution notes under these problem slugs: `aggregate-policy-returns`, `compare-pipeline-measurements`, `extract-elastic-subnetwork`, `finite-difference-gradient-check`, `pareto-edge-model-selection`, `reuse-tensor-buffers`, `robot-episode-confidence-intervals`, `seed-deterministic-evaluation`.

Fix worker: inspect their encoding, preserve the intended text/code, and convert only the affected Markdown files to UTF-8/LF in an isolated `codex/` worktree. Add a focused source-encoding regression so canonical catalog generation reaches all problem packages. Do not weaken the strict UTF-8 guard or change evaluator/reference code. The five focused canonical-source tests passed on all321 packages; catalog publication subsequently succeeded with all321 remote identities verified.
