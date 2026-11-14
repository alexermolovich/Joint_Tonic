# Compose orientation while preserving quaternion conventions

## Intuition

A quaternion stores an orientation in four numbers, but a valid rotation lives on the unit sphere in that four-dimensional space. Normalization repairs scale, not a wrong component order or a reversed composition.

This exercise uses scalar-first Hamilton quaternions $q=(w,\mathbf v)$ with $\mathbf v=(x,y,z)\in\mathbb R^3$. All components are dimensionless. They describe active rotations of column vectors in one right-handed basis.

## Normalize without losing tiny rotations to underflow

For nonzero q, let $s=\max_i|q_i|>0$. Compute

$$
\widehat q=\frac{q/s}{\sqrt{\sum_{i=0}^{3}(q_i/s)^2}}.
$$

The scaled components have magnitude at most one and at least one has magnitude exactly one. Squaring them cannot overflow and their sum cannot underflow to zero. A tiny identity-like quaternion is still normalizable.

## The Hamilton product

Let $a=(w_a,\mathbf v_a)$ be the normalized rotation applied after $b=(w_b,\mathbf v_b)$. Their product is

$$
a\otimes b=
\left(w_aw_b-\mathbf v_a^\top\mathbf v_b,\ 
w_a\mathbf v_b+w_b\mathbf v_a+\mathbf v_a\times\mathbf v_b\right).
$$

The dot and cross products use the same fixed basis. Normalize the resulting four-vector to remove rounding drift. The ordering agrees with rotation matrices $R(a\otimes b)=R(a)R(b)$.

## Visual: track a vector through two rotations

| Stage | Active rotation | Vector coordinates |
|---|---|---|
| Start | None | (0,1,0) |
| First | +90° around x | (0,0,1) |
| Second | +90° around z | (0,0,1) |

This static orientation trace is also the text alternative. With both inputs containing sqrt(0.5) in the appropriate scalar/axis positions, the four product components are all 0.5. Reversing order changes the path and the resulting rotation.

## Why this matters on a robot

An IMU library might use scalar-last order while a pose service expects scalar-first. Both arrays have length four, so shape validation alone cannot reveal the mistake. Always declare the convention and multiplication direction.

Quaternions q and -q represent the same rotation. This problem preserves the product's sign rather than inventing a canonical sign. That makes sign behavior explicit; temporal sign-continuity and SLERP are later topics.

## Check your understanding

- Does normalization fix an x-y-z-w versus w-x-y-z mismatch? No.
- Why can q and -q differ numerically but rotate a vector identically? The representation double-covers rotations.

## Sources

SciPy documents [component conventions](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.from_quat.html) and [composition order](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.__mul__.html). Use NumPy here; SciPy is not a runtime dependency.
