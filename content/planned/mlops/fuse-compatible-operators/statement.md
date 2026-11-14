# Fuse Compatible Operators in a Compute Graph

Implement fuse_operator_chains(nodes) -> list[tuple[str,...]].

nodes is a Python list of 0–10000 tuples(id,op,parent,shape) in topological order. IDs match ASCII [a-z][a-z0-9_-]{0,63} and are unique. op is input,scale,relu,sigmoid or barrier. input requires parent=None; every other op has exactly one earlier node ID as parent. shape is a tuple of 1–4 built-in non-bool ints in [1,4096]; its product <=1000000. A child may declare a different shape only when its op is barrier. Inputs and barriers are never fused.

Partition every node into groups. Fuse a fusible child(scale,relu,sigmoid) into its parent's group iff the parent is also fusible and has exactly one direct consumer in the COMPLETE graph. Otherwise start a new group. Group members follow input/topological order; groups are ordered by the first member's input position. Return fresh tuples in a fresh list. Empty graph returns[]. Preserve inputs. Invalid containers, labels, dimensions, duplicate IDs, forward/missing references or unsupported shape changes raise ValueError.

This conservative unary-chain partition does not execute tensors, combine arbitrary branches, reorder computations, or claim TVM's full fusion algorithm. The same declared shape means the same caller-supplied layout/dtype; this function does not infer equivalence across layouts.

## Worked examples

### A fusible chain
For `nodes=[("x","input",None,(4,)),("a","scale","x",(4,)),("b","relu","a",(4,))]`, return `[("x",),("a","b")]`.

### A later branch blocks fusion
Appending `("c","sigmoid","a",(4,))` to that graph returns `[("x",),("a",),("b",),("c",)]`.

## Source and scope

This original bounded component is motivated by [2018-tvm](https://www.usenix.org/conference/osdi18/presentation/chen). It does not reproduce the full paper, trained model or benchmark protocol.
