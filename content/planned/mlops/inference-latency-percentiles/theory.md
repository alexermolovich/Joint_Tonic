# Theory: robot responsiveness lives in a latency distribution

## Intuition

An average can look acceptable while a robot occasionally acts on an old observation. A distribution summary separates a typical-position request from the slow tail. The measurement boundary matters just as much: timing a GPU launch call is not the same as timing a completed model query.

Our input pairs each arrival with its actual completion on one monotonic clock. Queueing and preprocessing are included when they lie between those two chosen events.

## Durations before floating-point conversion

For request index $i$, let $a_i$ and $c_i$ be integer arrival and completion timestamps in nanoseconds. Define

$$
\ell_i=c_i-a_i,\qquad \ell_i^{\mathrm{ms}}=\ell_i/10^6.
$$

The clock origin can be large even when the interval is short. Subtracting integers first preserves that small difference; converting both timestamps to binary floating point before subtraction can erase nanoseconds.

Let $N>0$ be the number of requests and $x_{(1)}\le\cdots\le x_{(N)}$ their sorted nanosecond durations. Our nearest-rank empirical quantile is

$$
k_p=\lceil pN\rceil,\qquad q_p=x_{(k_p)}/10^6,
\qquad p\in\{0.50,0.90,0.99\}.
$$

The rank is one-based. Each $q_p$ is in milliseconds. This estimator returns an observed duration, not an interpolated value. Integer percentage arithmetic avoids rounding ambiguity when calculating the rank.

## Visual: define the timing boundary

~~~mermaid
flowchart LR
  A["Arrival: a_i ns"] --> Q["Queue"]
  Q --> P["Preprocess"]
  P --> I["Inference completes"]
  I --> C["Completion: c_i ns"]
  C --> D["Subtract paired timestamps"]
  D --> S["Sort durations and select ranks"]
~~~

**Text alternative:** the chosen interval spans arrival, queueing, preprocessing, and inference through completion. Subtract each matched pair, then sort those intervals. The diagram is static.

For durations [1,2,3,4,20] ms:

| Statistic | Rank calculation | Selected duration |
|---|---:|---:|
| p50 | ceil(0.50×5) = 3 | 3 ms |
| p90 | ceil(0.90×5) = 5 | 20 ms |
| p99 | ceil(0.99×5) = 5 | 20 ms |

Equal p90 and p99 here describe a small finite sample, not certainty that the true population tail ends at 20 ms. More observations and a confidence procedure would be needed for such a statement.

## Why this matters on a robot

A delayed perception result can make an otherwise accurate model feed stale state to a controller. Report the workload, hardware, model/runtime versions, timing boundary, and sample count alongside these numbers. Mixing clocks, excluding queueing unintentionally, or silently removing slow requests can make comparisons misleading.

MLPerf provides the scenario-aware benchmarking context. The historical paper's single-stream scenario uses a 90th-percentile measure; the three summaries here do not establish official benchmark validity. [MLPerf Inference Benchmark](https://arxiv.org/abs/1911.02549).

## Questions

1. Why does a four-request trace return p50=2 ms for [1,2,3,4] rather than 2.5 ms?
2. Why might host-side launch timing miss the delay experienced by a robot?

Prerequisite: distinguish a request's arrival from its completion. No general statistics course is required.
