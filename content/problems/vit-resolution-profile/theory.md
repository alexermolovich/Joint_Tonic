# Profile Token Count, Memory, and Latency by Resolution

## Intuition

Higher image resolution provides more spatial detail but makes dense attention compare many more token pairs. Count that cost explicitly while retaining measured latency as a separate signal.

## Math and scaling table

For image height $H$,width $W$ and square patch side $P$ pixels, token count includes a class token:
$$L=(H/P)(W/P)+1,\qquad M=A L^2 b.$$
Here $A$ is number of heads, $b$ bytes per stored score, and $M$ bytes for one layer's explicit score tensor on one image. No gradients, QKV tensors, model weights or allocator overhead are included.

| Image | Patch | Tokens | Heads | Bytes/value | Score bytes |
|---|---|---|---|---|---|
| 4×4 | 2 | 5 | 2 | 4 | 200 |
| 8×8 | 2 | 17 | 2 | 4 | 2312 |

For $K$ measured latencies sorted ascending, nearest-rank p95 selects rank $\lceil0.95K\rceil$ (one-based). It is a quantile convention, not a confidence bound. With four samples, that rank is4, so p95 equals the largest measurement.

## Why this matters on a robot

An extra camera or finer visual grid can overwhelm an edge device. Memory arithmetic helps plan experiments, but fused kernels may not materialize this matrix and actual latency must be benchmarked. Use comparable preprocessing, batch size and device state when collecting supplied times.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/2010.11929). [vit-patchify-reconstruct](/problems/vit-patchify-reconstruct)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
