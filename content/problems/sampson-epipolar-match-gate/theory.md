# Filter Geometrically Inconsistent Matches

## Intuition

Corresponding image points should lie on each other's epipolar lines. Sampson error divides the squared algebraic constraint error by a local sensitivity term, giving a more useful pixel-scale diagnostic than the raw residual.

## Mathematics and conventions

Let $a=[x,y,1]^\top$ and $b=[u,v,1]^\top$ be homogeneous matched pixels and F the normalized fundamental matrix. The ideal constraint is $b^\top Fa=0$. Its first-order coordinate sensitivity is

$$d=(Fa)_x^2+(Fa)_y^2+(F^\top b)_x^2+(F^\top b)_y^2.$$

For a valid pair with $d>10^{-12}$, define

$$E=\frac{(b^\top Fa)^2}{d},\qquad \text{accept}\iff E\le\tau^2.$$

E approximates a squared pixel correction and tau is a pixel threshold. Scaling F multiplies numerator and denominator by the same squared factor; normalization makes the degeneracy cutoff scale-invariant too. If d vanishes, a zero algebraic residual still does not provide a usable first-order distance, so the error is +Inf and the pair is rejected.

## Visual computation trace

| Horizontal epipolar example | Vertical mismatch | Squared Sampson error |
| --- | --- | --- |
| Sourcey0,targety0 | 0 | 0 |
| Sourcey0,targety2 | 2 | 2 |
| Masked match | any | undefined: +Inf |

## Worked examples

1. F=`[[0.,0.,0.],[0.,0.,-1.],[0.,1.,0.]]`, source `[[0.,0.]]`, target `[[3.,2.]]`: squared Sampson error is 2 square pixels. Threshold sqrt(2) accepts the pair; threshold 1 rejects it.
2. Change the target to `[[3.,0.]]`: the epipolar residual and squared error are zero, so threshold 0 accepts. With valid=False, squared_error is +Inf and the pair is rejected despite zero residual.

## Why this matters on a robot

Purely algebraic error depends on the arbitrary scale of F. Even Sampson error is only a local approximation and can be unreliable near epipoles or with an incorrectly estimated fundamental matrix.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/2104.00680). [local-window-match-expectation](/problems/local-window-match-expectation)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
