# Estimate Memory, Latency, and Quantized Serving Budgets

## Intuition

Four-bit weights occupy fewer bytes, but packed storage and kernel speed are separate questions. Combine exact weight-byte arithmetic with measured latency and explicitly supplied runtime overhead to decide whether a configuration fits both limits.

## Mathematical mechanism

For N parameters at b bits, $$M_w=\lceil Nb/8\rceil,\qquad M_{total}=M_w+M_{overhead}+M_{KV}.$$ A configuration is feasible iff $M_{total}\le M_{limit}$ and measured $t_{.95}\le T$. N counts scalars, all M terms use bytes and t,T use milliseconds. Bit width alone cannot predict kernel latency.

## Visual computation trace

| Format | N=3 weight bytes | overhead+KV | total |
|---|---|---|---|
| 4bit | 2 | 3+4 | 9 |
| 8bit | 3 | 3+4 | 10 |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

N=3,bits=[4,8],overhead=[3,3],KV=[4,4],latencies=[[2,3],[2,4]],memory_limit9,deadline3 gives weights[2,3],total[9,10],p95[3,4],feasible[True,False].

## Why this matters on a robot

A numerically plausible result can still represent the wrong action channel or calibration. Preserve preprocessing metadata and evaluate boundary behavior before closing the control loop.

## Physical contract and limits

Memory bytes; latency/deadline milliseconds; parameter and token counts dimensionless. Caller-synchronized observations; generation time and physical control time are distinct. Original bounded engineering component motivated by the paper; no pretrained model or benchmark reproduction is implied.

Source: [primary paper](https://arxiv.org/abs/2406.09246). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
