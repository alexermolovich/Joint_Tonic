# Build a Gaussian-Process Smoothness Factor

## Intuition

A state that follows its starting velocity exactly agrees with the prior. Position and velocity errors are correlated, so dividing them independently by their marginal standard deviations gives the wrong cost.

## Mathematics and conventions

For joint $d$, initial and final states $z_0=(q_0,v_0)$ and $z_1=(q_1,v_1)$, duration $t>0$, and acceleration-noise spectral density $c_d>0$,

$$e_d=\begin{bmatrix}q_1-q_0-tv_0\\v_1-v_0\end{bmatrix},\quad Q_d=c_d\begin{bmatrix}t^3/3&t^2/2\\t^2/2&t\end{bmatrix}.$$

Define $L_dL_d^T=Q_d$ with lower triangular $L_d$ and positive diagonal. Then

$$r_d=L_d^{-1}e_d,\qquad E=\tfrac12\sum_d r_d^Tr_d.$$

The residual has shape $D\times2$ and mixed position/velocity units; whitening removes those units. The noise density is rad²/s³, so every covariance block has the corresponding pair of residual units. A diagonal covariance approximation discards the position/velocity coupling.

## Visual computation trace

| Stage | One-joint value |
| --- | --- |
| Position/velocity residual | `[1,0]` |
| Covariance | `[[1/3,1/2],[1/2,1]]` |
| Lower-factor whitening | `[sqrt(3),-3]` |
| Half squared norm | `6` |

## Worked examples

1. Start and end `[[0.,0.]]`, duration `1`, spectral density `[1.]` yield residual `[[0.,0.]]`, covariance `[[[1/3,1/2],[1/2,1]]]`, whitened residual zero and cost `0`.
2. Start `[[0.,0.]]`, end `[[1.,0.]]`, duration `1`, density `[1.]` yield residual `[[1.,0.]]`, whitened `[[sqrt(3),-3]]`, and cost `6`.

## Why this matters on a robot

A prior encourages smooth motion but cannot certify collisions or actuator limits. Treating seconds as milliseconds changes different covariance blocks by different powers and can dominate an optimizer incorrectly.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1707.07383). Read the typed contract and coordinate conventions above.

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
