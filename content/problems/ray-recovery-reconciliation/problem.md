# Recover Failed Worker Tasks Idempotently

## Contract

`reconcile_task_attempts(tasks, events, max_attempts) -> list[dict]`. tasks is a list of 1..10000 exact {task_id, replay_safe} records with unique IDs and Boolean replay_safe. events is a list of 0..50000 exact {task_id, attempt, status, digest} records. Each task must be declared; attempt is int in 1..max_attempts; status is "failed" or "succeeded"; a failed event has digest=None, a succeeded event has a valid SHA256. max_attempts is int in 1..16. Repeated identical events are ignored; contradictory status/digest records for the same(task, attempt) raise ValueError. Multiple successful attempts for one task must agree on digest or raise ValueError. Event order has no meaning.

For each task: any success commits state "succeeded", digest agreed, next_attempt=None, regardless of later failed attempts. Without success, no observed attempts gives state "pending", next_attempt=1, even if replay_safe=False. Otherwise highest attempt==max_attempts gives state "exhausted", next_attempt=None. Otherwise replay_safe=False gives state "blocked", next_attempt=None; otherwise state "retry", next_attempt=highest+1. Non-success digest=None. Return exact {task_id, state, next_attempt, digest} rows sorted by task_id. This reconciles supplied terminal evidence, not an executor or exactly-once side-effect guarantee.

## Common operational contract

Identifiers are ASCII strings matching [a-z][a-z0-9_-]{0,31}; digests are exactly 64 lowercase hexadecimal characters. Unless the task explicitly reports malformed field values as issues, invalid argument types, fields, bounds, IDs or unknown references raise ValueError. Built-in integer scalars exclude bool. Preserve all input arrays/records and return fresh containers. No network, filesystem reads, wall clock, randomness or physical robot commands are used. These are original bounded operational policies inspired by the source paper, not its released API or a certification.

## Worked examples

tasks=[{task_id:"a", replay_safe:True},{task_id:"b", replay_safe:False}], events=[{task_id:"a", attempt:1, status:"failed", digest:None}], max_attempts=3 gives a:state "retry", next_attempt=2 and b:state "pending", next_attempt=1; both digest=None.

For one replay-safe task a, successful attempt 1 with digest"1"*64 plus failed attempt 2 under max_attempts=3 gives state "succeeded", next_attempt=None, digest"1"*64. Repeating either event does not change the result.

## Source and scope

Original bounded component inspired by [2017-ray](https://arxiv.org/abs/1712.05889). It does not reproduce the full paper or establish hardware safety or data-use authorization.
