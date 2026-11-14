# Measure Simulation and Learning Throughput

## Intuition

Compilation and initialization can dominate a short simulator benchmark. Exclude declared warmup iterations, count completed environment steps once, and divide by the measured iteration time. Gaps in the supplied trace are not silently charged as computation.

## Mathematics and physical contract

For retained iteration set $I$, synchronized integer endpoints $s_i<e_i$ are in nanoseconds. Counts $n_i$ and $u_i$ denote completed environment steps and learner updates. Compute exact integer totals before converting rates:
$$T=\sum_{i\in I}(e_i-s_i),\quad N=\sum_{i\in I}n_i,\quad U=\sum_{i\in I}u_i,\quad f_N=\frac{10^9N}{T},\quad f_U=\frac{10^9U}{T}.$$
Rates have steps/second and updates/second units. Iterations must be chronological and nonoverlapping; gaps are excluded. Empty retained evidence has zero totals and NaN rates. Counts already include batch size and repeats. This teaching trace assumes serialized measurements; asynchronous device timings require a different synchronization contract.

## Worked pipeline and shape trace

```text
iteration0: [0,1s), steps100, updates1 -> excluded warmup
iteration1: [2s,4s), steps400, updates6 -> duration2s
retained rates: 400/2=200 steps/s; 6/2=3 updates/s
1-second gap is outside measured intervals
```

The text trace is the visual and accessible alternative; no animation is required.

## Why this matters on a robot

A large samples-per-second number can coexist with poor sample efficiency or unrealistic simulation. Mixing CPU launch times with asynchronous GPU completion times makes even the throughput denominator unreliable.

## Prerequisites and source

The problem statement supplies the exact array, unit and boundary conventions. [Episode validity masks](/problems/build-robot-sequence-validity-masks) provide related context for preserving episode boundaries.

Original bounded component associated with [2021-isaac-gym](https://arxiv.org/abs/2108.10470). The scope and finite-sample or simulation conventions above are part of this exercise, not a claim of full-paper reproduction.
