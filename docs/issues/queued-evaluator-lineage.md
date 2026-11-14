# Freeze evaluator content for queued jobs so lineage matches execution

**Status:** Local issue draft; GitHub creation was blocked by automatic approval review with `blocked by policy`. Do not retry posting through another surface without root direction.

A queued job can run different tests from the evaluator revision recorded in its lineage. In `apps/worker/server.py`, `Handler.do_POST` hashes `cases.py` at acceptance, but `evaluate` calls `sandbox`, which reloads and copies the current problem files by slug when execution starts.

## Reproduction

Confirmed using temporary content, an ephemeral HTTP service, and the real WSL bubblewrap runner. The live website, worker, and repository problem files were not changed.

1. Create a temporary problem with version `1.0.0` and one public check: `assert solution.value == 1`.
2. Hold executor dispatch and POST a run containing `value = 1`.
3. After acceptance, change the temporary check to `assert solution.value == 2`.
4. Release the held evaluation callback and inspect the persisted result.

**Expected:** Execute the evaluator snapshot accepted with the job, or reject it explicitly as stale before grading.

**Actual:** The result is `completed` with `passed: false` from the new assertion, while `lineage.evaluator_sha256` still identifies the old test file.

- Recorded/original SHA-256: `6df20f9c4010cd30ce8333aba1331cdb1fa07e3be9a1a94a64c9ac4c6db1e004`
- Executed file SHA-256: `ffa0e373d5113404e93074f29bc2e889625a7051fdd2c1f679fe049ce7e3906d`

This breaks score reproducibility if content changes while a job waits behind the two active workers. Source code is already snapshotted; evaluator content and metadata are not frozen with it.

## Proposed change and focused check

Bind each accepted job to immutable evaluator/content artifacts. A smaller interim guard may verify the accepted version/hash immediately before execution and report an explicit platform error on mismatch. Ensure the reported lineage describes the files actually used.

Add one queued-job regression that changes the live problem files after acceptance and verifies snapshot execution or explicit stale-job rejection. Keep live learner jobs and repository content isolated from this regression.
