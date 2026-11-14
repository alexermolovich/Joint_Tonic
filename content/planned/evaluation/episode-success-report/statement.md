# Report Robot Policy Success Without Hiding Missing Tasks

**Status: planned; no runnable implementation yet.**

A robot policy is evaluated on several tasks. Summarize its episode outcomes while keeping missing task coverage and collision evidence visible.

## Contract

Planned function: episode_report(records, expected_tasks).

Expected tasks is a nonempty ordered list of unique nonempty task names. Each record contains a known task, outcome from success/failure/timeout/intervention, and a boolean collision flag. Records are independent completed episodes. Reject malformed records, unknown tasks, duplicate expected tasks, and nonboolean collision flags.

Return per_task metrics in expected-task order: count, success_rate, timeout_rate, intervention_rate, and collision_rate. An unobserved task has count=0 and all rates=None. Return total count, micro_success over observed episodes, macro_success averaged equally across tasks only when every expected task has evidence, coverage as the observed-task fraction, and missing_tasks in expected order. With no episodes, both aggregate success rates are None.

## Scope and assessment

Success is outcome=success; collision is reported independently and never silently rewrites the recorded outcome. No safety certification or confidence interval is inferred from this small sample. Grade imbalanced counts, missing tasks, empty evidence, and contradictory-looking but valid success/collision combinations. See [examples.md](examples.md). Status: planned.

