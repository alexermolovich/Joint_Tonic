# Detect Unobservable Initialization Motion

## Intuition

An initializer can fit measured motion while leaving scale, gravity or bias directions unresolved. Normalize the units first, then inspect which combinations of parameters the linearized measurements can actually constrain.

## Mathematics and conventions

For parameter perturbation $\delta x$, choose physical scales $s_j>0$ and dimensionless coordinates $\delta z_j=\delta x_j/s_j$. With row standard deviations $\sigma_i>0$, the whitened sensitivity is

$$A_{ij}=J_{ij}s_j/\sigma_i,\qquad A=U\Sigma V^\top.$$

J has shape $(R,D)$, A is dimensionless, and singular values measure normalized measurement sensitivity to scaled parameter motion. Retain $\sigma_k>\epsilon\sigma_{max}$, where epsilon is the supplied relative cutoff. If retained right singular vectors form rows of $V_r$, then

$$P_{null}=I-V_r^\top V_r.$$

This basis-independent projector maps scaled parameter perturbations into the numerically unsupported subspace. It is symmetric and idempotent up to floating error. Its trace is $D-rank$. The zero-row case has no measured directions, hence the identity projector.

## Visual computation trace

| Jacobian columns | Supported direction | Null projector |
| --- | --- | --- |
| [[1,0]] | first parameter | diag(0,1) |
| [[2,0],[0,1]] | both parameters | zero matrix |
| No rows | none | identity |

## Worked examples

1. J=`[[2.,0.],[0.,1.]]`, scales and standard deviations all 1, cutoff 0.001: singular values `[2.,1.]`, rank 2, condition 2 and zero unobservable projector.
2. J=`[[1.,0.]]` with unit scales/std gives rank 1, singular values `[1.,0.]`, condition +Inf and projector `[[0.,0.],[0.,1.]]`. The second scaled parameter direction has no measurement support.

## Why this matters on a robot

A stationary or weakly excited motion window may leave initialization parameters coupled. A high rank computed with inappropriate physical scaling can be misleading, and known pose gauge freedoms must be handled before this diagnostic.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1708.03852). Read the typed contract and coordinate conventions above.

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
