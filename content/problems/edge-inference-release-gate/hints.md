# Progressive hints

## Hint 1

Exclude warmup and invalid measurements before inspecting their measurement fields, then group included records by hardware class. A fast machine must not mask a different machine's tail latency.

## Hint 2

Accuracy is a mean of correctness flags. Sequential throughput uses total queries divided by total measured service time. Compute latency quantiles with the declared linear interpolation; the mean of reciprocal latencies is a different quantity.

## Hint 3

Calculate all metrics before checking policy. Append every failed rule in the prescribed order, followed by sorted missing/regressed baseline slices. Equality passes, but no evidence must produce the explicit `no_samples` result rather than an accidental success.
