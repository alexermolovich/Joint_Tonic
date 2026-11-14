# Worked examples

tasks=[{task_id:"a", replay_safe:True},{task_id:"b", replay_safe:False}], events=[{task_id:"a", attempt:1, status:"failed", digest:None}], max_attempts=3 gives a:state "retry", next_attempt=2 and b:state "pending", next_attempt=1; both digest=None.

For one replay-safe task a, successful attempt 1 with digest"1"*64 plus failed attempt 2 under max_attempts=3 gives state "succeeded", next_attempt=None, digest"1"*64. Repeating either event does not change the result.
