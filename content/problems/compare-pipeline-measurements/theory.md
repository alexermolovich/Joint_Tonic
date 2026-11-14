# Compare Black-Box and Grey-Box Pipeline Measurements

## Intuition

External request timing includes intervals that internal probes may not cover. Adding all internal spans overcounts parallel work; subtracting their union gives the portion of the boundary not instrumented.

## Interval evidence

For request boundary [a,b) and internal spans $S_i$, define

$$L=b-a,\quad C=\left|\bigcup_i S_i\right|,\quad U=L-C,\quad O=\sum_i|S_i|-C.$$

L,C,U,O are integer nanoseconds. O measures excess counted duration from overlapping spans. Sort spans by start and merge overlaps or touching boundaries; touching intervals add no overlap.

## Visual: parallel work

| Evidence | Interval ns | Duration ns |
|---|---|---:|
| External request | [0,10) | 10 |
| Stage a | [1,6) | 5 |
| Stage b | [4,8) | 4 |
| Union | [1,8) | 7 |

Thus C=7,U=3,O=9-7=2. The table is the static interval diagram and text alternative.

## Why this matters on a robot

Camera preprocessing and accelerator work can overlap. Summing spans and calling it end-to-end latency is misleading. Conversely, uninstrumented time may include transport, waiting, or missing probes; this exercise does not assign an unsupported cause.

## Source and scope

This original bounded component is motivated by [2023-robotperf](https://arxiv.org/abs/2309.09212). It does not reproduce the full paper, trained model or benchmark protocol.
