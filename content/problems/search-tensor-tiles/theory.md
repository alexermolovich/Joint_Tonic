# Search Tensor Tile Sizes with a Toy Cost Model

## Intuition

A tile trades fewer launches against padding and working memory. The best tile under one explicit cost need not be the fastest on real hardware, but a deterministic model makes the tradeoff inspectable.

## Tail tiles and a bounded search

For positive integer dimensions, $\lceil M/t_m\rceil=(M+t_m-1)//t_m$. With Q total tiles, use

$$F=4(t_mt_k+t_kt_n+t_mt_n),\qquad C=Q(t_mt_nt_k+h).$$

F is bytes for three float32 tiles; h is a caller-supplied dimensionless launch penalty. M,N,K count matrix rows, output columns and reduction entries. Feasibility is inclusive at the memory bound. Tie-breaking uses the smallest footprint then tile tuple.

## Visual: launches versus padding

| Shape | Tile | Q | Padded MACs | F bytes | C with h=10 |
|---|---|---:|---:|---:|---:|
| (3,3,3) | (1,1,1) | 27 | 27 | 12 | 297 |
| (3,3,3) | (2,2,2) | 8 | 64 | 48 | 144 |

The larger tile wastes arithmetic but wins this toy launch model. The table is an original cost trace and text alternative.

## Why this matters on a robot

Hardware memory limits can rule out a promising schedule. Ignoring tail tiles underestimates work on unusual sensor shapes. Validate correctness and measure the final schedule on the target device; this score does not predict real latency.

## Source and scope

This original bounded component is motivated by [2018-tvm](https://www.usenix.org/conference/osdi18/presentation/chen). It does not reproduce the full paper, trained model or benchmark protocol.
