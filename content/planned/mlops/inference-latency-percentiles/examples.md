# Worked percentile calculations

The full timestamp lists are in statement.md.

| Trace | Sorted ms | p50 rank/value | p90 rank/value | p99 rank/value |
|---|---|---|---|---|
| Long tail | 1,2,3,4,20 | 3 / 3 ms | 5 / 20 ms | 5 / 20 ms |
| Even size | 1,2,3,4 | 2 / 2 ms | 4 / 4 ms | 4 / 4 ms |

~~~python
latency_percentiles([], [])
# {"p50_ms": None, "p90_ms": None, "p99_ms": None}
latency_percentiles([123], [123])
# {"p50_ms": 0.0, "p90_ms": 0.0, "p99_ms": 0.0}
latency_percentiles([2], [1])  # ValueError
~~~

The equal timestamps case is valid zero latency. Theory answers: the exercise explicitly selects an observed nearest rank; asynchronous launch returns before device execution completes. These are public examples, not claims of benchmark certification.
