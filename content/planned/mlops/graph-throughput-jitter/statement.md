# Measure Throughput and Jitter Across a ROS-Style Graph

Implement graph_throughput_jitter(completions, window) -> dict.

completions is a Python dict of 0–128 stage IDs matching ASCII [a-z][a-z0-9_-]{0,63}, each mapping to a nondecreasing Python list of built-in non-bool integer completion timestamps in [0,2**63-1]. Total timestamps <=100000. All stages use one synchronized monotonic clock. window is a tuple(start_ns,end_ns) of those integer bounds with start_ns<end_ns.

For each stage in ASCII ID order, include completions in the half-open interval [start_ns,end_ns). Return exactly count (built-in int), throughput_hz=count*1e9/(end_ns-start_ns), mean_interval_ns, jitter_ns in its new dict. With fewer than two retained events, both interval metrics are None. Otherwise form adjacent retained-event differences, take their arithmetic mean and population standard deviation (divide by number of intervals, not number minus one). Equal timestamps produce zero intervals. Subtract integers before converting differences to floats; timestamps can exceed exact float precision. Preserve all inputs. Invalid containers, IDs, ordering, types or bounds raise ValueError.

Stage throughput is not path latency, sensor rate, or causal request matching. Dropped events and clocks are not inferred; this function summarizes declared completed work only.

## Worked examples

### Uneven completions
`graph_throughput_jitter({"vision":[0,10,30,40]}, (0,40))` returns `{"vision":{"count":3,"throughput_hz":75000000.0,"mean_interval_ns":15.0,"jitter_ns":5.0}}`.

### One retained event
`graph_throughput_jitter({"control":[5,15]}, (0,10))` returns `{"control":{"count":1,"throughput_hz":100000000.0,"mean_interval_ns":None,"jitter_ns":None}}`.

## Source and scope

This original bounded component is motivated by [2023-robotperf](https://arxiv.org/abs/2309.09212). It does not reproduce the full paper, trained model or benchmark protocol.
