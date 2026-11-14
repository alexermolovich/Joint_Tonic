# Local isolated evaluation worker

The worker listens on loopback and executes learner Python in a disposable Linux bubblewrap namespace. Start it in WSL from the repository root using the project's Python 3.12 environment:

```bash
JOINT_TONIC_VENV=/home/alex/.venvs/joint-tonic \
  /home/alex/.venvs/joint-tonic/bin/python apps/worker/server.py
```

The environment contains NumPy 2.2.4 and PyTorch 2.6.0+cpu. The current report/runtime revision is `bwrap-v2`. `JOINT_TONIC_VENV` can select an equivalent environment elsewhere; this directory is mounted read-only as `/opt/venv`.

## Verification

For a content change, check just the affected author-owned references in both public Run and full Submit:

~~~bash
/home/alex/.venvs/joint-tonic/bin/python apps/worker/check_references.py --sandbox unproject-depth-map pid-anti-windup
~~~

Omit the slugs to check all published metadata entries. Omit --sandbox only for a fast trusted-reference arithmetic check; learner submissions must always use the isolated worker. Missing evaluator files and empty/public-only/hidden-only test sets fail validation. The checker discovers the catalog rather than assuming ten problems. Use the broader containment suite below when the execution boundary changes or a failure warrants it.

```bash
PYTHONDONTWRITEBYTECODE=1 \
  /home/alex/.venvs/joint-tonic/bin/python tests/worker_checks.py
```

This runs every content reference through the actual sandbox, checks public-only Run behavior, and probes network isolation, host-home visibility, read-only work files, cleared credentials, resource limits, invalid code, incorrect solutions, output bounds, CPU termination, wall timeout, and HTTP job ownership/persistence. The HTTP test uses an ephemeral port and leaves the normal development service alone.

## Enforced local bounds

- Separate network/PID/user/mount namespaces and dropped capabilities.
- Read-only Python runtime and work files; temporary writes under a disposable `/tmp`.
- No mounted host home or Windows filesystem and a minimal environment.
- 10 CPU seconds, 18 seconds of wall time, 4 GiB address space per process, 1 MiB per written file, 64 open files, 64 processes, and disabled core dumps.
- 64 KiB stdout/stderr transport limit. Python print output has the same cumulative byte limit, with at most 16 KiB retained for diagnostics.
- A successful report must match the expected evaluator case sequence and contain complete passing case results. Nonzero process exits cannot report success.

## Scope of trust

This is a single-user local development runner. The tests and learner module currently share a Python interpreter and namespace. Learner code can inspect mounted evaluator files and Python process state; structural report checks do not prevent a determined submission from manipulating that interpreter. Hidden cases are hidden from ordinary UI responses, not confidential from code inside this process.

Before accepting public hostile submissions, separate trusted grading from untrusted execution using an explicit data-only protocol and keep hidden fixtures outside learner-visible mounts. Add an audited syscall policy and aggregate cgroup limits; the current resource limits apply per process rather than to the full process tree. The loopback workspace identifier is local ownership bookkeeping, not production authentication. Production execution remains outside Vercel and Supabase functions.
