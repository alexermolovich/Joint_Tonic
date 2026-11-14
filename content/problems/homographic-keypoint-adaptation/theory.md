# Apply Homographic Keypoint Adaptation

## Intuition

Warping a detector response back does not mean scattering its samples. For each reference pixel, find where it lands in the warped response, interpolate there, and average the available evidence.

## Mathematics and conventions

Let $P_k\in[0,1]^{H\times W}$ be a supplied detector map and $H_k\in\mathbb R^{3\times3}$ its reference-to-warped homography. For reference center $u=(x,y)$, compute $q=H_k[x,y,1]^\top$ and $v_k=(q_x/q_z,q_y/q_z)$ when $|q_z|>10^{-9}$. For cell fractions $a=v_x-\lfloor v_x\rfloor$ and $b=v_y-\lfloor v_y\rfloor$, interpolation is

$$s_k=(1-a)(1-b)P_{00}+a(1-b)P_{10}+(1-a)bP_{01}+abP_{11}.$$

All probabilities are dimensionless; image coordinates are pixels. Let $m_k(u)$ indicate supported projection and sampling. Then

$$c(u)=\sum_km_k(u),\qquad \bar P(u)=\frac{\sum_km_k(u)s_k(u)}{c(u)}.$$

When c is zero, the estimate is undefined. A fixed divisor K would depress responses near boundaries and confuse unsupported views with negative evidence.

## Visual computation trace

| Reference x | Warped x under +1 translation | Sample | Count |
| --- | --- | --- | --- |
| 0 | 1 | .8 | 1 |
| 1 | 2 | outside the two-center map | 0 |

## Worked examples

1. Two identity-warped `2x2` constant maps, with values 0.2 and 0.8, produce a `2x2` map of 0.5 and counts 2.
2. One map `[[0.2,0.8]]`, reference-to-warped x translation +1, output size `[1,2]`, gives probability `[[0.8,NaN]]` and count `[[1,0]]`. The missing sample is not a zero detection.

## Why this matters on a robot

Repeated views can reveal stable corners, but a homography is only appropriate for its declared planar/projective relationship. Wrong warp direction or counting missing border samples as zeros creates biased detector targets.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1712.07629). Read the typed contract and coordinate conventions above.

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
