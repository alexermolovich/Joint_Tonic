# Simulate Single-Stream and Server Load

## Intuition

Fast isolated inference does not imply low request latency under load. A request can wait behind earlier work. Single-stream closes the loop between completion and next issuance; an externally driven server workload can build a queue.

## One deterministic server

Let $a_i$ be arrival time, $d_i>0$ service duration, $b_i$ start and $c_i$ completion, all in integer nanoseconds. Set $c_{-1}=0$. The FCFS recurrence is

$$
b_i=\max(a_i,c_{i-1}),\qquad c_i=b_i+d_i,\qquad L_i=c_i-a_i.
$$

Waiting is $W_i=b_i-a_i$, so $L_i=W_i+d_i$. For single-stream, $a_0=0$ and $a_i=c_{i-1}$ afterward. For server mode, the caller supplies nondecreasing arrivals.

## Visual: waiting appears in end-to-end latency

| Request | Arrival | Service | Start | Finish | Wait | Latency |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 3 | 0 | 3 | 0 | 3 |
| 1 | 1 | 2 | 3 | 5 | 2 | 4 |
| 2 | 8 | 4 | 8 | 12 | 0 | 4 |

All values are ns. The table is the original schedule trace and text alternative. The second request's service is2ns while its experienced latency is4ns.

## Scope of the simulation

Real benchmark scenarios can specify arrival distributions, batching, concurrency, duration and statistical requirements. Here service durations and arrivals are fixed inputs, allowing exact repeatable queue reasoning. Do not interpret these toy times as measured model performance.

## Why this matters on a robot

A camera can produce observations faster than a model consumes them. Even unchanged inference service time then produces older predictions. Queue waiting belongs in an observation-to-result latency boundary when that is the declared contract.

## Questions

1. Why does request1 in server mode have latency4 rather than2?
2. Does single-stream measure behavior under arbitrary backlog?

## Sources and prerequisites

The historical MLPerf2019 paper motivates scenario-dependent query issuance. The supplied-arrival, single-server FCFS recurrence is an original teaching simulator, not the official LoadGen or compliance protocol. [Primary source](https://arxiv.org/html/1911.02549v1), Section4.5 Scenarios and Metrics; Section4.7 Load Generator. Prerequisites: the component conventions defined in the statement; no Python or mathematics tutorial is assumed.

