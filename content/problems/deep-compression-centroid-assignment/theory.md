# Quantize Shared Weight Centroids

## Intuition

Replace many independent surviving weights with references into a small shared table. The table order defines the deterministic tie rule, while pruned weights remain outside the table.

## Mathematics and conventions

For weight vector $w\in\mathbb R^N$, active mask $m\in\{0,1\}^N$ and centroids $c\in\mathbb R^K$,
$$a_i=\arg\min_{0\le k<K}|w_i-c_k|\quad(m_i=1).$$
Choose the smallest index among equal distances. Then $\widehat w_i=c_{a_i}$ for active entries; inactive entries use $a_i=-1$ and $\widehat w_i=0$. Absolute distance and squared distance give the same nearest centroid; absolute distance avoids unnecessary squaring. This assignment step does not implement trained weight sharing's gradient accumulation.

## Shape and numerical trace

```text
active weight0 -> distances to[-2,2]=[2,2] -> index0; inactive weight3 -> index-1, value0. Output arrays retain N positions.
```

The trace is also the text alternative: each arrow is the ordered operation described above; no animation is required.

## Why this matters on a robot

Shared codebooks reduce edge-model storage only when index and sparse-structure costs are included. Sorting a supplied codebook changes index identity and violates reproducibility.

## Source and prerequisites

Original bounded component inspired by [2015-deep-compression](https://arxiv.org/abs/1510.00149). No pretrained model, paper benchmark result, retraining or hardware latency claim is included. Familiarity with a linear layer and the stated channel convention is assumed.
