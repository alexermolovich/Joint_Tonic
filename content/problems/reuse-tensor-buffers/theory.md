# Reuse Tensor Buffers with Liveness Analysis

## Intuition

A temporary tensor stops needing its storage after its last consumer. Another tensor can reuse those bytes only once the first lifetime ends, and only if the buffer is large enough.

## Half-open liveness

For interval $I_i=[s_i,e_i)$, a previous allocation j is free at s_i when $e_j\le s_i$. Among free capacities c_b satisfying $c_b\ge n_i$, choose the lexicographically smallest $(c_b,b)$. Otherwise allocate a new buffer. Sizes and capacities are bytes; s,e are logical indices.

$$R=\sum_b c_b.$$

R reports reserved storage, including currently free buffers. It is different from $\max_t\sum_{i:t\in I_i}n_i$, the peak live tensor size.

## Visual: reuse at the boundary

| Tensor | Bytes | Lifetime | Buffer |
|---|---:|---|---:|
| a | 8 | [0,2) | 0 |
| b | 4 | [2,3) | 0 |
| c | 8 | [2,4) | 1 |

At time2, b wins first by name. Buffer0 is then live, so c needs buffer1. Reserved memory is16bytes. The table is the static liveness trace and text alternative.

## Why this matters on a robot

Camera and model intermediates can dominate edge memory. Reusing a still-live buffer corrupts values without changing tensor shapes. A deterministic allocator makes such aliasing rules testable; it does not prove a whole compiler's memory correctness.

## Source and scope

This original bounded component is motivated by [2018-tvm](https://www.usenix.org/conference/osdi18/presentation/chen). It does not reproduce the full paper, trained model or benchmark protocol.
