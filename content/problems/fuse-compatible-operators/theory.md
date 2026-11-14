# Fuse Compatible Operators in a Compute Graph

## Intuition

Consecutive elementwise operations can share one kernel traversal. A branching producer may still be needed elsewhere, so a conservative partition stops before fusing across that dependency.

## A legal local rule

For edge u→v, define F={scale,relu,sigmoid}, and let deg+(u) count direct consumers in the complete graph. Fuse only when

$$\mathrm{op}(u),\mathrm{op}(v)\in F\quad\land\quad\deg^+(u)=1.$$

All such nodes have the same declared shape. The graph remains topological; no numerical reassociation is performed. Count consumers before making any grouping decisions so a later branch cannot be missed.

## Visual: branching changes the partition

| Graph | Groups after singleton input |
|---|---|
| input→scale→relu→sigmoid | (scale,relu,sigmoid) |
| input→scale→relu and scale→sigmoid | (scale), (relu), (sigmoid) |

This original graph table is the visual and text alternative. A barrier always starts its own group, even when the output shape matches.

## Why this matters on a robot

Fewer memory passes can help edge inference, but optimizing away a value still consumed by another branch breaks the graph. This problem proves a conservative structural grouping, not a speedup or generated-kernel correctness.

## Source and scope

This original bounded component is motivated by [2018-tvm](https://www.usenix.org/conference/osdi18/presentation/chen). It does not reproduce the full paper, trained model or benchmark protocol.
