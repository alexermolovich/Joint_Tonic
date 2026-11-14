# Resolve persisted pending jobs when the local worker restarts

**Status:** Local issue draft. No GitHub issue was created; the existing remote publishing block remains in effect.

`apps/worker/server.py` persists accepted jobs but stores execution state only in the process-local `EXECUTOR` and `ACTIVE` set. Startup creates an empty executor/set and serves existing job files without reconciling pending states. A queued job from the prior process remains queued with no task capable of completing it.

## Reproduction and evidence

Verified using two child processes, ephemeral loopback ports, and one temporary job directory. The live development worker and its job store were untouched; no learner code was executed by the probe.

1. Import the actual worker module in a child process and point `STORE` at a fresh temporary directory.
2. Replace dispatch with a held executor whose `submit` does not run its callback. Serve the actual `Handler` on an ephemeral port. This represents a job waiting behind existing work.
3. POST a valid job with a workspace owner. The worker returns HTTP 202; GET returns `queued`, and the job JSON exists in the temporary store.
4. Terminate this owned child process.
5. Start a fresh child with the normal worker module, the same store, and a new ephemeral port. Do not replace the new executor.
6. GET the same job with its workspace owner.

Observed result:

```json
{"accepted_http":202,"before_restart":"queued","after_restart_http":200,"after_restart":"queued","new_worker_active_jobs":0,"job_id_unchanged":true}
```

**Expected:** Resolve persisted pending jobs through safe recovery or an explicit terminal interruption state. A completed job must remain unchanged.

**Actual:** GET keeps returning the old pending state, and no task was scheduled in the new process. The workspace polls it until its retry budget expires and suggests refreshing; refreshing reconnects to the same orphaned job.

## Proposed scope and focused regression

Add startup reconciliation for queued/running records. If replay is not safe or supported, mark them as interrupted platform failures and allow a fresh submission. Preserve completed records and ownership checks. Verify one pending job across a real worker restart with an isolated store, then check that completed history is unchanged.

This is separate from `queued-evaluator-lineage.md`: that issue concerns which evaluator version a live queued task executes; this issue concerns tasks lost when the worker process exits.
