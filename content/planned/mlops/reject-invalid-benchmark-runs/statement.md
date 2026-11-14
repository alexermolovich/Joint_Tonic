# Reject Invalid Benchmark Runs

Implement benchmark_run_rejections(run: dict, protocol: dict) -> list[str].

run has exactly scenario,model_sha256,expected_queries,completed_queries,failed_queries,duration_ns,quality. protocol has exactly scenario,model_sha256,min_queries,min_duration_ns,min_quality.
- scenario is the string single_stream or server.
- model_sha256 is64 lowercase hexadecimal characters. It is a supplied identity, not a claim that this function hashes model bytes.
- Run counters are built-in non-bool ints in[0,10**9], with completed_queries+failed_queries<=expected_queries. Completed counts successful completed queries; failed counts distinct failed queries. Unaccounted expected queries are unfinished.
- Run duration_ns is a built-in non-bool int in[0,2**63-1].
- Protocol min_queries is a built-in non-bool int in[1,10**9]; min_duration_ns in[1,2**63-1].
- quality/min_quality are built-in non-bool int/float, finite in[0,1], using the same declared metric.

Return all applicable reason strings in ASCII sorted order:
- scenario: run scenario differs from protocol.
- model: model hashes differ.
- incomplete: completed+failed<expected.
- failed_queries: failed>0.
- insufficient_queries: completed<min_queries.
- insufficient_duration: duration_ns<min_duration_ns.
- quality: quality<min_quality.

Threshold equality passes; conditions are independent so several reasons may apply. Fully matching evidence returns[]. Preserve both inputs. Malformed schema/types/values or inconsistent counter accounting raise ValueError, even if the run would otherwise fail a gate. No latency percentile, warmup removal, confidence interval, signature verification, deployment or external I/O is performed.

## Worked examples

### Exact thresholds are accepted

~~~python
protocol={"scenario":"server","model_sha256":"a"*64,
          "min_queries":10,"min_duration_ns":100,"min_quality":0.8}
run={"scenario":"server","model_sha256":"a"*64,"expected_queries":10,
     "completed_queries":10,"failed_queries":0,"duration_ns":100,"quality":0.8}
benchmark_run_rejections(run,protocol)
# []
~~~

The evidence matches identity, accounting, coverage, duration and quality.

### One failed query and one unfinished query

~~~python
run={"scenario":"server","model_sha256":"a"*64,"expected_queries":10,
     "completed_queries":8,"failed_queries":1,"duration_ns":99,"quality":0.79}
protocol={"scenario":"server","model_sha256":"a"*64,
          "min_queries":9,"min_duration_ns":100,"min_quality":0.8}
benchmark_run_rejections(run,protocol)
# ["failed_queries","incomplete","insufficient_duration",
#  "insufficient_queries","quality"]
~~~

A failure and an unfinished query are different evidence. Neither is counted as successful completed work.

## Source and scope

MLPerf motivates comparable workloads and valid quality-constrained measurements. This small evidence validator and its supplied thresholds are original; it is not an official MLPerf submission, statistical confidence or audit checker. [Primary source](https://arxiv.org/html/1911.02549v1).

