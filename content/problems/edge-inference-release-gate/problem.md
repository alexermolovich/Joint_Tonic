# Gate an Edge Model with Accuracy and Latency

A new perception model improves average accuracy but occasionally misses a control deadline. Build a transparent release gate that evaluates quality, tail latency, throughput, peak memory and scenario regressions separately for each hardware class.

~~~python
release_gate(samples, thresholds) -> dict
~~~

## Samples

samples is a list of dictionaries. valid defaults to True and warmup defaults to False; both flags must be Python booleans. Exclude a record when valid=False or warmup=True before validating its measurement fields.

Included records require hardware (nonempty string), latency_ms (finite >0), memory_mb (finite ≥0), and correct (Python bool). slice is an optional string, default "all". Repeated records are independent sequential measurements.

## Thresholds

Required fields:

- min_samples: positive Python integer, excluding bool.
- min_accuracy: finite value in [0,1].
- max_p99_ms, min_throughput_qps, max_memory_mb: finite nonnegative values.

Optional baseline_accuracy maps slice strings to baseline accuracy in [0,1]. max_slice_drop is in [0,1], default 1. A required baseline slice missing on a hardware class fails that hardware. A regression occurs when baseline−current exceeds max_slice_drop + 1e−12.

## Output

~~~python
{
  "passed": True,
  "metrics": {
    "cpu": {
      "count": 2, "accuracy": 1.0,
      "p50_ms": 15.0, "p90_ms": 19.0, "p99_ms": 19.9,
      "throughput_qps": 66.66666666666667,
      "peak_memory_mb": 120.0,
      "slices": {"all": 1.0}
    }
  },
  "reasons": []
}
~~~

Use NumPy's linear quantile convention. Sequential throughput is 1000×count/sum(latency_ms); do not use sum of per-sample reciprocal latencies. Peak memory is a maximum. Slice values are mean correct indicators.

metrics uses hardware keys in sorted order. Reasons are strings ordered by hardware, then the fixed rule order sample_count, accuracy, p99_ms, throughput_qps, memory_mb, then sorted baseline slice names. Baseline reasons are slice_missing:name or slice_regression:name. Prefix each reason with hardware:, for example "gpu:p99_ms".

Equality to a configured threshold passes. No measured records returns {"passed":False,"metrics":{},"reasons":["no_samples"]}. Invalid included inputs, flags or thresholds raise ValueError. Inputs remain unchanged.

## Examples

**Example 1 — a passing sequential benchmark**

Two cpu records with latencies 10 and 20 ms, both correct and using memory 100 and 120 MB, produce the metrics shown above. Thresholds min_samples=2, min_accuracy=0.9, max_p99_ms=20, min_throughput_qps=60, max_memory_mb=128 pass.

**Example 2 — tail latency fails**

Use those records with max_p99_ms=19. The result keeps all metrics and sets passed=False, reasons=["cpu:p99_ms"]. The p50 is 15 ms, but that does not override a p99 failure.

**Example 3 — warmup is excluded**

A record {"warmup":True} is ignored even without hardware/latency fields. If every record is excluded, return the no_samples decision.

## Scope

This is an original teaching gate for sequential synthetic measurements. It is not an official MLPerf submission checker. A concurrent request load requires an explicit wall-clock measurement window; the formula here must not be reused without adapting that contract.

Sources: [MLPerf Inference](https://arxiv.org/abs/1911.02549), [ML Test Score](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/).
