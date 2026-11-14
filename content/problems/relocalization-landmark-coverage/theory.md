# Evaluate a Relocalization Candidate

## Intuition

Many matches can be repeated observations of one landmark or concentrated in one small image region. Count independent landmark identities before asking whether their geometric evidence covers the image.

## Mathematics and conventions

For candidate k, let $I_k$ be its inlier feature indices with nonnegative landmark identities $\ell_{ki}$. Define one representative per identity as the lowest i carrying that identity. Let the representative set be $R_k$. Its landmark count is

$$n_k=|R_k|.$$

For image height H, width W and grid dimensions G_y,G_x, point $(x_i,y_i)$ occupies

$$c_i=\left\lfloor y_iG_y/H\right\rfloor G_x+\left\lfloor x_iG_x/W\right\rfloor,\qquad v_k=|\{c_i:i\in R_k\}|.$$

All coordinates are pixels; counts and cell indices are dimensionless. Eligibility requires both $n_k\ge n_{min}$ and $v_k\ge v_{min}$. Duplicates must not increase either count, so coverage uses the same canonical representatives as the identity count.

## Visual computation trace

| Inlier IDs at opposite image corners | Distinct landmarks | Counted coverage |
| --- | --- | --- |
| [7,7] | 1 | first representative only: 1 cell |
| [7,8] | 2 | both representatives: 2 cells |

## Worked examples

1. Keypoints `[[0.,0.],[3.,3.]]` in a `[4,4]` image and `[2,2]` grid, candidate landmark IDs `[[7,7]]`, both geometric inliers: unique_landmarks=1 and covered_cells=1. Only feature index 0 represents landmark 7.
2. Change IDs to `[[7,8]]`: both counts become 2. With min_landmarks=2 and min_cells=2 this candidate becomes eligible; the duplicated-ID candidate does not.

## Why this matters on a robot

A false place-recognition candidate can accumulate many ambiguous descriptor matches. These identity and coverage gates expose some weak evidence patterns, but supplied geometric inliers must still come from an appropriate pose-verification process.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1610.06475). [reprojection-pose-hypothesis-inliers](/problems/reprojection-pose-hypothesis-inliers)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
