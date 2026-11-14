# Build Homography-Supervised Descriptor Correspondence Targets

## Intuition

Known synthetic image geometry supplies labels without hand-matching descriptors. It defines which target centers lie near the transformed source center, including cases with several positive centers.

## Mathematics and conventions

For source center $a_i\in\mathbb R^2$ pixels, apply the source-to-target homography H to $[a_{ix},a_{iy},1]^\top$ and dehomogenize to $\hat a_i$. Let $m_i,n_j$ be source and target validity masks and $v_i$ the supported-denominator flag. For target center $b_j$,

$$d_{ij}=\|\hat a_i-b_j\|_2,\qquad s_{ij}=m_i\land n_j\land v_i\land(d_{ij}\le\tau).$$

The distance matrix has shape $(N,M)$ and pixel units; s is Boolean. Unsupported distances are NaN rather than large sentinel distances, distinguishing missing geometry from an observed negative pair. Tolerance tau is explicit because grid resolution and cell-center choices affect the target labels.

## Visual computation trace

| Source center | Target0 at x=0 | Target1 at x=1 |
| --- | --- | --- |
| x=0 | distance0: positive | distance1: positive |
| x=2 | distance2: negative | distance1: positive |

## Worked examples

1. Identity warp, source centers `[[0.,0.],[2.,0.]]`, target centers `[[0.,0.],[1.,0.]]`, all valid, tolerance 1: distances `[[0.,1.],[2.,1.]]`, labels `[[True,True],[False,True]]`.
2. With the first source marked invalid, its entire distance row is NaN and its labels are False. The second row is unchanged.

## Why this matters on a robot

A wrong grid stride can turn correct correspondences into negative training labels. Masking invalid centers and stating full-resolution pixel coordinates prevents this mismatch; labels alone do not guarantee useful descriptors.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1712.07629). [homographic-keypoint-adaptation](/problems/homographic-keypoint-adaptation)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
