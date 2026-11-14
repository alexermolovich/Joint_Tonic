# Associate Map Points with Image Features

## Intuition

A predicted camera pose narrows descriptor search to a local pixel neighborhood. Binary appearance then ranks plausible candidates, and a deterministic collision rule prevents several landmarks from claiming the same observed feature.

## Mathematics and conventions

For world landmark $P_i\in\mathbb R^3$ meters and world-to-camera transform $(R,t)$, form $p_i=RP_i+t$. If $Z_i>10^{-6}$ m, project

$$\hat u_i=(f_xX_i/Z_i+c_x,\ f_yY_i/Z_i+c_y).$$

For observed feature pixel $u_j$, squared geometric error is $d_{ij}^2=\|u_j-\hat u_i\|^2$ in square pixels. Packed descriptor bytes $a_{ib},b_{jb}$ define bit distance

$$h_{ij}=\sum_{b=0}^{31}\operatorname{popcount}(a_{ib}\operatorname{xor}b_{jb}).$$

The distance lies between 0 and 256. Keep candidates with $d_{ij}^2\le r^2$ and $h_{ij}\le h_{max}$, then apply the specified lexicographic proposal and collision rules. This is not a globally optimal bipartite assignment, and rejected proposals intentionally do not fall back to another feature.

## Visual computation trace

| Two identical landmark proposals | Hamming | Pixel error | Decision |
| --- | --- | --- | --- |
| Map0 to feature0 | 0 | 0 | accepted first |
| Map1 to feature0 | 0 | 0 | feature already used: unmatched |

## Worked examples

1. Two map points both `[0.,0.,1.]`, zero descriptors, one feature `[0.,0.]` with zero descriptor, identity pose and intrinsics `[1.,1.,0.,0.]`: radius 0, max_hamming 0 gives feature_indices `[0,-1]`. Map-index order breaks the collision.
2. One map descriptor with first byte 255 and remaining bytes 0 versus an all-zero image descriptor differs by 8 bits. With matching pixels, max_hamming 7 rejects it and max_hamming 8 accepts it.

## Why this matters on a robot

A bad pose can exclude the correct descriptor from the search neighborhood. A descriptor collision can also reduce match count under this no-retry policy; neither failure should be hidden by assigning an arbitrary fallback feature.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1610.06475). [project-camera-points](/problems/project-camera-points)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
