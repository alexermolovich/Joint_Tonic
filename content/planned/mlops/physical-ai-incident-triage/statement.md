# Triage a Physical-AI Deployment Incident

Implement:

~~~python
def triage_events(events: list[tuple[int, str, str]],
                  now_ms: int, window_ms: int
                  ) -> list[tuple[str, str, int, int]]:
    ...
~~~

Each event tuple is (timestamp_ms, component_id, kind). Component IDs match ASCII [a-z][a-z0-9_-]{0,63}. Kinds and their severity are:

| kind | severity |
|---|---|
| safety_stop | P0 |
| sensor_stale | P1 |
| deadline_miss | P1 |
| model_error | P2 |

These are reporting labels, not instructions to control hardware. events must be a Python list of at most100,000 exact three-item tuples. Timestamps, now_ms and window_ms must be built-in non-bool ints in [0,2**63-1]. Every event timestamp must be <=now_ms; a future event makes the entire call invalid even if other events are usable. Validate all records before filtering.

Retain records whose timestamp is >=now_ms-window_ms. Group by component. Return (component_id, strongest_severity, retained_count, first_retained_ms) for each nonempty group. Strongest means the smallest severity number; first_retained_ms is the minimum retained timestamp. Sort groups by severity number, then first_retained_ms, then component_id. Counts and timestamps are Python ints.

Input order is irrelevant. Identical tuples count as separate observed records; there is no event-ID deduplication. An empty input or no retained events returns []. A zero-width window includes only events exactly at now_ms. All contract violations raise ValueError. Preserve input data; use no implicit clock, external I/O or randomness.

## Worked examples

### Strongest event sets the component priority

~~~python
events = [(900,"arm","model_error"),(950,"arm","safety_stop"),
          (920,"camera","sensor_stale"),(800,"camera","model_error"),
          (980,"planner","deadline_miss")]
triage_events(events,1000,150)
# [("arm","P0",2,900),("camera","P1",1,920),("planner","P1",1,980)]
~~~

The cutoff is850ms. Camera's800ms event is excluded. Arm's earliest retained event is900ms even though the strongest event occurred later.

### Inclusive cutoff and duplicate records

~~~python
events = [(90,"b","model_error"),(100,"a","model_error"),
          (90,"b","model_error"),(89,"a","safety_stop")]
triage_events(events,100,10)
# [("b","P2",2,90),("a","P2",1,100)]
~~~

Both90ms records count. The stale P0 record does not raise the retained priority of a.

## Source and scope

The paper motivates monitored operational evidence. The event taxonomy, severity mapping and queue ordering are original educational policy; this function summarizes synthetic events and cannot stop, recover or approve a real robot. [Primary source](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/).
