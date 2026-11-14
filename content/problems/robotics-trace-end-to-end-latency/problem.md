# Derive End-to-End Latency from Robotics Trace Events

Implement trace_latencies(events: list[tuple[str,str,int,str]]) -> list[tuple[str,int]].

Each event is (request_id,boundary,timestamp_ns,clock_id). events is a Python list of0–200,000 tuples. request_id and clock_id match ASCII [a-z][a-z0-9_-]{0,63}. boundary is exactly the string input or output. timestamp_ns is a built-in non-bool int in[0,2**63-1]. All nonempty events must share one clock_id; no offsets are estimated.

For each request ID require exactly one input event and exactly one output event. Event list order may be arbitrary. Duplicate boundaries are invalid even if their timestamps match. Missing boundaries are invalid; do not silently omit incomplete requests. Output timestamp must be>=input timestamp. Return (request_id,output_ns-input_ns) in ASCII request-ID order, with a built-in integer latency. Zero latency is allowed at the clock's resolution.

Empty events returns[]. Preserve inputs. Every malformed container/tuple/label/type/bound, mixed clock, duplicate/missing boundary or negative correlated latency raises ValueError and rejects the whole trace. No partial results, inferred request IDs, stage-level sum, dropped-message interpolation or clock synchronization occurs.

## Worked examples

### Correlation beats event-list order

~~~python
trace_latencies([("b","output",150,"mono"),("a","input",100,"mono"),
                 ("b","input",110,"mono"),("a","output",160,"mono")])
# [("a",60),("b",40)]
~~~

The earlier output belongs to b, not the earliest input a. Nearest-time matching would change the measurements.

### Preserve small differences at large clock values

~~~python
trace_latencies([("tiny","input",2**63-3,"mono"),
                 ("tiny","output",2**63-1,"mono"),
                 ("same","input",8,"mono"),("same","output",8,"mono")])
# [("same",0),("tiny",2)]
~~~

Integer arithmetic keeps the2ns difference; converting large timestamps to floats could erase it.

## Source and scope

RobotPerf motivates explicit workload boundaries and correlated timing. The strict two-event schema is an original bounded trace-analysis exercise, not a complete ROS trace parser or critical-path reconstruction. [Primary source](https://arxiv.org/html/2309.09212v2).

