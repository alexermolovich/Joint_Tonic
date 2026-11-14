# Compute p50, p90, and p99 Inference Latency

**Local Python exercise · content version 1.0.0.**

Given paired query arrival and completion timestamps, report the latency distribution's median-position and tail observations.

## Function contract

~~~python
def latency_percentiles(start_ns: list[int], end_ns: list[int]
                        ) -> dict[str, float | None]:
    ...
~~~

Both inputs are lists of the same length N, at most 1,000,000. Each item is a built-in Python int, excluding bool, in [0, 2**63 - 1]. Row i pairs the arrival of one request with completion of that same request. All timestamps share one monotonic clock and arbitrary origin. Completions may be out of input order; requests may overlap. No sorting or pairing by timestamp is performed.

For every pair, require 0 ≤ end_ns[i] - start_ns[i] ≤ 10**12 nanoseconds. Compute exact integer durations first. Sort durations ascending into x with one-based positions 1 through N. For p in {0.50, 0.90, 0.99}, select position ceil(p*N). **Do not interpolate or average central values.** Divide the selected nanosecond duration by 1,000,000 to obtain milliseconds.

Return exactly keys "p50_ms", "p90_ms", and "p99_ms", with Python float values for nonempty input. Inputs remain unchanged. Outputs are checked with rtol=0 and atol=1e-9 milliseconds. No coordinate frames apply; latency is a scalar duration. This function neither warms up a device nor synchronizes GPU work: the supplied completion timestamps must already represent completed queries.

## Errors and empty inputs

Raise ValueError for wrong list types, unequal lengths, invalid integer/range values, negative/excessive durations, or exceeded size limits. Error text is not graded. For empty lists, return:
~~~python
{"p50_ms": None, "p90_ms": None, "p99_ms": None}
~~~

Warmup filtering, failed-query filtering, clock synchronization, and percentile confidence intervals are outside this component. The caller supplies the measured query set; silently dropping a slow query is not permitted.

## Worked example 1 — a long tail

~~~python
start_ns = [0, 10000000, 20000000, 30000000, 40000000]
end_ns =   [1000000, 12000000, 23000000, 34000000, 60000000]
# Durations in milliseconds: [1, 2, 3, 4, 20]
# Output: {"p50_ms": 3.0, "p90_ms": 20.0, "p99_ms": 20.0}
~~~

Ranks are 3, 5, and 5. A small trace cannot distinguish these two tail levels.

## Worked example 2 — an even-sized trace

~~~python
start_ns = [0, 0, 0, 0]
end_ns = [1000000, 4000000, 2000000, 3000000]
# Output: {"p50_ms": 2.0, "p90_ms": 4.0, "p99_ms": 4.0}
~~~

Sorted durations are [1,2,3,4] ms. The p50 rank is 2, so its value is 2 ms rather than the interpolated median 2.5 ms.

## Runtime budget

CPython 3.12.3 on the isolated local CPU worker. Limits: 10 CPU seconds, 18 wall seconds, 4 GiB address space per process, and 64 KiB output. No simulator or network access is required.
