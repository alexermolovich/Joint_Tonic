# Apply SE(3) Exponential and Logarithm Maps

## Intuition

A rigid-motion tangent combines translation and rotation during the same infinitesimal flow. The exponential integrates that flow, so its translation bends with the rotation instead of being copied unchanged.

## Mathematics and conventions

Let $\xi=(\rho,\phi)\in\mathbb R^6$, with $\rho$ in meters and $\phi$ in radians, $\theta=\|\phi\|$, and $\Omega=[\phi]_\times$. Then

$$R=I+\frac{\sin\theta}{\theta}\Omega+\frac{1-\cos\theta}{\theta^2}\Omega^2,\quad V=I+\frac{1-\cos\theta}{\theta^2}\Omega+\frac{\theta-\sin\theta}{\theta^3}\Omega^2,$$
$$\operatorname{Exp}(\xi)=\begin{bmatrix}R&V\rho\\0&1\end{bmatrix},\qquad\operatorname{Log}(T)=\begin{bmatrix}V(\phi)^{-1}t\\\phi\end{bmatrix}.$$

At zero angle the three scalar coefficients approach 1, 1/2 and 1/6 respectively. The skew operator satisfies $[\phi]_\times x=\phi\times x$. The principal rotation logarithm is unique on the supported branch below pi; solving with V recovers the translation tangent.

## Visual computation trace

| Tangent | Rotation | Exponential translation |
| --- | --- | --- |
| rho=(1,0,0), phi=0 | identity | (1,0,0) m |
| rho=(1,0,0), phi=(0,0,pi/2) | z rotation 90° | (2/pi,2/pi,0) m |

## Worked examples

1. Tangent `[1.,0.,0.,0.,0.,0.]` and identity transform yield an exponential that translates one meter along x, and a zero logarithm.
2. Tangent `[1.,0.,0.,0.,0.,pi/2]` yields a 90-degree z rotation with translation `[2/pi,2/pi,0]`, not `[1,0,0]`. Supplying this resulting transform to Log recovers the same six-vector.

## Why this matters on a robot

Copying rho into the transform translation passes pure-translation tests but fails coupled motion. Near-zero coefficients need stable limits; the unsupported pi branch requires additional axis conventions in a general-purpose library.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1812.01537). [compose-frame-transforms](/problems/compose-frame-transforms)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
