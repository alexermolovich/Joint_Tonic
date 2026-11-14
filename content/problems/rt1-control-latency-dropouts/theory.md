# Measure Closed-Loop Latency and Action Dropouts

## Intuition

An inference that finishes after its control deadline is not equivalent to an action applied on time. Keep missing commands separate from delivered-but-late commands while reporting their combined effect on the loop.

## Mathematical mechanism

For delivered row i, latency is 

$$\ell_i=a_i-o_i$$

 milliseconds. For T observations, dropout rate is $\sum_i\mathbf1[a_i=-1]/T$ and deadline-miss rate is $\sum_i\mathbf1[a_i=-1\ \mathrm{or}\ \ell_i>d]/T$, where d is the deadline. Equality with d is on time. The delivered mean excludes the missing sentinel rather than treating it as a negative duration.

## Visual computation trace

| Observation | Applied | Latency | Outcome |
|---|---|---|---|
| 0 | 5 | 5 | on time |
| 10 | -1 | -1 sentinel | missing |
| 20 | 35 | 15 | late for10ms |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

observed_ms=[0,10,20], applied_ms=[5,-1,35], deadline_ms=10 returns latency_ms=[5,-1,15], dropout_rate=1/3, deadline_miss_rate=2/3 and mean_latency_ms=10.

## Why this matters on a robot

Averaging only delivered commands can conceal frequent dropouts. Clock offsets can also produce impossible negative delays. The function rejects applied-before-observed pairs, but it cannot determine whether two clocks were calibrated correctly.

## Physical contract and limits

All times and deadline are milliseconds on one synchronized monotonic clock; rates dimensionless. Each applied entry corresponds to exactly its observed entry; no timestamp matching is inferred. Original measurement exercise motivated by RT-1 control-time efficiency; no proprietary robot telemetry or published latency number is reproduced.

Source: [primary paper](https://arxiv.org/abs/2212.06817). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
