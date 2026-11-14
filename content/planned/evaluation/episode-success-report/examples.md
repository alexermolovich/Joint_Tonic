# Hand-verified worked examples

**Planning examples, not executable tests.** Values below define the intended contract and must be reproduced by the future reference implementation.

## Example 1: imbalanced task counts

Expected tasks=[A,B].

Records:
- A, success, collision=False
- A, timeout, collision=False
- B, success, collision=True

Expected: A count=2, success=0.5, timeout=0.5, intervention=0, collision=0. B count=1, success=1, timeout=0, intervention=0, collision=1.

Aggregate: total=3; micro_success=2/3; macro_success=0.75; coverage=1; missing_tasks=[].

A successful episode can still carry collision evidence.

## Example 2: an expected task has no evidence

Expected tasks=[A,B]. One record: A, success, collision=False.

Expected: A count=1 and success=1; B count=0 and every rate=None.

Aggregate: total=1; micro_success=1; macro_success=None; coverage=0.5; missing_tasks=[B].

## Boundary

With no records, both aggregate success rates are None, coverage=0, and missing_tasks preserves [A,B].

