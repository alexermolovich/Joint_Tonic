# Package and Gate an Edge Perception Release

## Intuition

Deployment selection connects accuracy, measured latency, memory ownership, and artifact identity. A fast model is unusable if its tensors overlap in memory while simultaneously live. A valid artifact can still fail a monitored drift policy.

## Reuse with explicit lifetimes

For request $i$, $[s_i,e_i)$ is a half-open operation-index lifetime and $b_i$ is its size in bytes. Buffer $j$ with capacity $C_j$ and previous end $E_j$ can be reused when

$$E_j\le s_i\quad\text{and}\quad C_j\ge b_i,\qquad B_{arena}=\sum_j C_j.$$

Choose smallest sufficient capacity, then buffer ID. The total arena capacity differs from instantaneous live-byte demand because buffers remain allocated. In Example 1 the 8-byte buffer can hold the later 4-byte tensor at the exact lifetime boundary, so total capacity stays 8 bytes.

## Selection and identity

Let $q_m$ be dimensionless measured quality, $l_m$ p95 latency in milliseconds, and $B_m$ allocated bytes for model $m$. Eligible models satisfy all three supplied bounds; selection orders $(-q_m,l_m,m)$ lexicographically. Only after selection is its drift score compared to the drift limit.

$$h=\operatorname{SHA256}(\operatorname{canonicalJSON}(manifest)),\qquad s=\operatorname{HMAC}_{k}(\operatorname{canonicalJSON}(manifest)).$$

The manifest includes the model-byte hash and preprocessing convention. Here $k$ is deliberately public synthetic data, so the signature demonstrates deterministic binding, not protection against an attacker. Real signing requires managed private keys and trust verification outside learner sandboxes.

| Stage | Example 1 | Failure exposed |
| --- | --- | --- |
| Lifetime allocation | IDs 0 then 0 | Aliasing overlapping tensors |
| Measured gate | candidate 0 | Wrong p95 or quality tie policy |
| Canonical package | model and preprocessing bound | Untracked preprocessing change |
| Drift gate | promote | Previously valid release degrades |

## Why this matters on a robot

Changing color order can invalidate an otherwise identical model file. Recording only model weights misses this dependency. Supplied latency samples must come from comparable hardware and workload measurements; this exercise deliberately cannot turn fabricated samples into trustworthy performance evidence.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1908.09791). [reuse-tensor-buffers](/problems/reuse-tensor-buffers) · [pareto-edge-model-selection](/problems/pareto-edge-model-selection) · [package-edge-model-artifact](/problems/package-edge-model-artifact)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
