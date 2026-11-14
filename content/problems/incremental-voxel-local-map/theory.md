# Update an Incremental Local Map

## Intuition

A local map needs bounded spatial coverage and enough geometric detail without retaining every duplicate point. Transform the new scan, prune the local box, and select one representative nearest each voxel center.

## Mathematics and conventions

A new lidar point $p^L\in\mathbb R^3$ becomes world point $p^W=R_{WL}p^L+t_{WL}$ in meters. Concatenate existing world points before transformed scan points, assigning stable candidate indices. For local center $c$ and positive half extents $h$, keep points satisfying $|p^W_j-c_j|\le h_j$ for each world axis $j$. With voxel width $s>0$ meters and fixed world origin,
$$k(p)=\lfloor p^W/s\rfloor\in\mathbb Z^3,\qquad v_k=s(k+\tfrac12\mathbf1).$$
For every occupied key, choose
$$i_k=\arg\min_{i:k(p_i)=k}\big(\|p_i-v_k\|_2^2,i\big).$$
The lexicographic pair makes exact distance ties choose the earlier candidate index. Output keys in lexicographic coordinate order. An old point is removed if it lies outside the box or loses the representative selection. This deterministic batch operation teaches map pruning and downsampling decisions, not an incremental k-d tree implementation.

## Visual computation trace

```text
existing world points -- concatenate first --+
scan -- lidar-to-world transform ------------+--> inclusive local box
 -> global-origin voxel keys -> center-nearest winner -> sorted local map
old candidate IDs not selected -> removed_existing
```

## Worked examples

1. Existing points [[0.1,0,0],[0.4,0,0]], incoming [[0.6,0,0]], identity pose, center [0,0,0], half extents [2,2,2] and voxel size 1 select existing index 1. Points 0.4 and 0.6 tie around center 0.5, so the earlier candidate wins. Removed-existing flags are [True,False].
2. Existing [-0.1,0,0] and incoming [0,0,0] belong to voxel keys [-1,0,0] and [0,0,0]. Negative coordinates use floor, not truncation toward zero.

## Why this matters on a robot

Truncating negative coordinates merges points on opposite sides of the origin. Choosing an arbitrary first point can retain poorer voxel representatives. A local map update assumes scans are already deskewed and calibrated; downsampling cannot repair motion distortion.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/2107.06829). [se3-transform-points](/problems/se3-transform-points)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
