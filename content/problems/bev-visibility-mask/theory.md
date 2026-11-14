# Mask Out-of-View and Behind-Camera Samples

## Intuition

Projection alone does not prove a camera can observe a point. Test the continuous pixel rectangle and the forward half-space independently, then combine them.

## Math and decision trace

For camera $c$ and point $n$, let $(u_{cn},v_{cn})$ be pixels, $z_{cn}$ signed optical depth in meters, and $(H_c,W_c)$ the image height and width.
$$m_{cn}=\mathbf1[z_{cn}>10^{-6}]\mathbf1[0\le u_{cn}<W_c]\mathbf1[0\le v_{cn}<H_c].$$

| Check | Passing condition | Failure example |
|---|---|---|
| Depth | z > 1e-6 meters | Behind camera or near-zero division |
| Horizontal | 0 ≤ u < width | u exactly width |
| Vertical | 0 ≤ v < height | v below zero |

With width 4,height 3, point $(3.9,2.9)$ passes, while $(4,2)$ fails. Flooring coordinates before this test can accidentally admit a tiny negative coordinate. For $z=10^{-6}$, equality fails by the declared cutoff.

## Why this matters on a robot

Invalid camera samples must not contribute attention mass. This mask detects geometric field-of-view validity, not occlusion: a point behind an obstacle may pass every test. A zero projection sentinel cannot distinguish a valid image origin without its depth.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/2203.17270). [bev-project-reference-points](/problems/bev-project-reference-points)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
