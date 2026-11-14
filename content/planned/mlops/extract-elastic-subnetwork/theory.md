# Extract a Depth, Width, and Kernel Subnetwork

## Intuition

An elastic network stores weights that can be shared by smaller configurations. Selecting a subnetwork must keep adjacent channel dimensions consistent and keep the spatial kernel centered.

## A precise teaching slice

Let $W_l\in\mathbb R^{C\times C\times K\times K}$ be layer l with output channels first. For requested width w, odd kernel k and depth d, offset $o=(K-k)/2$ is an integer. Extract

$$\widetilde W_l=W_l[0:w,0:w,o:o+k,o:o+k],\qquad 0\le l<d.$$

All values are dimensionless learned weights. The first and second channel axes both shrink; taking only one creates an incompatible hidden stack. Copies isolate extracted variants from later changes to shared storage.

## Visual: centered 3×3 to 1×1

| Original kernel row0 | row1 | row2 |
|---|---|---|
| 0,1,2 | 3,4,5 | 6,7,8 |

The retained1×1 value is4, not0. This original table is a static crop diagram and text alternative. Spatial indices, not camera pixels, index the learned kernel here.

## Why this matters on a robot

A deployable smaller model must match its channel interfaces and be evaluated again. Center cropping alone does not reproduce OFA's learned transformations or recalibrated batch-normalization behavior. Forgetting those boundaries can produce an apparently valid artifact with poor accuracy.

## Source and scope

This original bounded component is motivated by [2020-once-for-all](https://arxiv.org/abs/1908.09791). It does not reproduce the full paper, trained model or benchmark protocol.
