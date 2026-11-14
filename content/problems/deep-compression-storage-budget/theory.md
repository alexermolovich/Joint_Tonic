# Compute a Compressed Model Storage Budget

## Intuition

A compressed file stores more than its weight symbols. Sparse positions, the shared codebook and headers can dominate a tiny model, so budget each stream explicitly.

## Mathematics and conventions

Let $f_k$ count centroid symbol $k$, $\ell_k$ its supplied prefix-code length in bits, and $n=\sum_k f_k$. With $b_i$ index bits, $b_c$ centroid bits, $H$ header bytes and $P$ dense parameter count,
$$B=\left\lceil\frac{\sum_k f_k\ell_k}{8}\right\rceil+\left\lceil\frac{nb_i}{8}\right\rceil+\frac{Kb_c}{8}+H,\qquad R=\frac{4P}{B}.$$
A feasible binary prefix-length set obeys $\sum_k2^{-\ell_k}\le1$ (Kraft inequality). It checks possible lengths, not a particular supplied codeword table. The original synthetic serialization budget does not replicate the paper's exact sparse index codec.

## Shape and numerical trace

```text
5 symbol bits ->1byte; 5 positions*3bits ->2bytes; 2 centroids*4bytes ->8bytes; header2bytes; total13bytes vs dense40bytes.
```

The trace is also the text alternative: each arrow is the ordered operation described above; no animation is required.

## Why this matters on a robot

Robot flash and RAM budgets can be tight even after weight pruning. Ignoring sparse indices exaggerates compression; fewer disk bytes do not automatically reduce runtime peak memory.

## Source and prerequisites

Original bounded component inspired by [2015-deep-compression](https://arxiv.org/abs/1510.00149). No pretrained model, paper benchmark result, retraining or hardware latency claim is included. Familiarity with a linear layer and the stated channel convention is assumed.
