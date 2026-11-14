# Measure Throughput and Jitter Across a ROS-Style Graph

## Intuition

A pipeline can complete work regularly at one stage while producing bursts at another. Counts measure work rate; variability between completions exposes irregular scheduling.

## Rate and interval variability

Let the window length be T=e-s nanoseconds and N the count satisfying s<=t<e. Throughput in completions per second is $f=N10^9/T$. For N>=2, let $d_i=t_{i+1}-t_i$ in ns and M=N-1. Define

$$\mu=\frac1M\sum_i d_i,\qquad \sigma=\sqrt{\frac1M\sum_i(d_i-\mu)^2}.$$

The returned jitter is population standard deviation sigma, not maximum latency or percentile jitter. There is no interval estimate when M=0.

## Visual: one stage, one observation window

| Retained completions ns | Intervals ns | Mean ns | Jitter ns |
|---|---|---:|---:|
| 0,10,30 | 10,20 | 15 | 5 |
| 5,5,5 | 0,0 | 0 | 0 |

This original table is also the text alternative. In [0,40), the first row completes three items, giving75000000Hz in this synthetic nanosecond example.

## Why this matters on a robot

Regular camera arrivals do not guarantee regular action updates. Compare stage boundaries consistently. A failure mode is counting an end-boundary event in two adjacent windows; half-open intervals prevent that duplication. Extremely small toy timestamps teach arithmetic, not realistic robot rates.

## Source and scope

This original bounded component is motivated by [2023-robotperf](https://arxiv.org/abs/2309.09212). It does not reproduce the full paper, trained model or benchmark protocol.
